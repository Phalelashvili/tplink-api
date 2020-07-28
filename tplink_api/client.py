import time
import base64
import hashlib
import requests
import urllib.parse
from threading import Thread
from .exceptions import *
from .requestconstructor import RequestConstructor
from .models import *


def login_required(func):
    def func_wrapper(self, *args, **kwargs):
        if not self.logged_in:
            raise NotLoggedInException("You need to be logged in to use this method")
        else:
            return func(self, *args, **kwargs)

    return func_wrapper


class Client:

    def __init__(self, username=None, password=None, url="http://192.168.0.1"):
        """initializes session and sets base url

        Parameters:
            username(str)
            password(str)
            url(str): full url, including HTTP scheme
        """
        self.base_url = url if url[-1] != "/" else url[:-1]  # remove last slash if exists
        self._session = requests.Session()
        self._requests = RequestConstructor(self.base_url)
        self.logged_in = False
        self._username = None
        self._password = None
        self._key = None

    @staticmethod
    def prepare_credentials(username, password):
        """encoded credentials are passed through cookies, because TP-Link is a fucking genius

        Args:
            username(str)
            password(str)
        Returns:
            str: md5 hashed password, base64 encoded and URL escaped cookie "Basic username:password"
        """
        password_md5 = hashlib.md5(password.encode()).hexdigest()
        base64_credentials = base64.encodebytes(f"{username}:{password_md5}".encode())[:-1]  # b64 encode adds \n
        escaped_credentials = urllib.parse.quote(f"Basic {base64_credentials.decode()}")

        return escaped_credentials

    @staticmethod
    def check_errors(html):
        """checks HTML content for LoginFailedException, TooManyAttemptsException and TooManyAdminsException.
        returns nothing if checks pass"""

        try:
            error_msg = html.split("var httpAutErrorArray = new Array(\n")[1].split(",")[0]
        except IndexError:  # httpAutErrorArray is not present (login succeeded)
            error_msg = -1

        exc = EXCEPTIONS.get(error_msg, None)

        if exc is not None:  # no errors detected
            raise exc(exc.MESSAGE)

    def login(self, username, password, keepalive=False):
        """logs into portal

        Args:
            username(str)
            password(str)
        Parameters:
            keepalive(bool): start thread to send keep-alive requests every 3 seconds
        Raises:
            LoginFailedException: username or password is incorrect
            InvalidCredentials: username and password can contain between 1 - 15 characters and may not include spaces.
            TooManyAttemptsException: before attempting login, ban status is checked on login page
        """
        # save credentials for renewing session
        self._username = username
        self._password = password

        if len(username) < 1 or len(username) > 15:
            raise InvalidCredentialsException("Username must contain between 1 - 15 characters")
        if " " in username:
            raise InvalidCredentialsException("Username characters must not include spaces")

        if len(password) < 1 or len(password) > 15:
            raise InvalidCredentialsException("Username must contain between 1 - 15 characters")
        if " " in password:
            raise InvalidCredentialsException("Username characters may not include spaces")

        # check for login ban status
        content = self._session.get(self.base_url).content.decode()
        self.check_errors(content)

        self._session.cookies.set("Authorization", self.prepare_credentials(self._username, self._password))
        req = self._session.get(**self._requests.login)
        content = req.content.decode()
        # check for login error messages
        self.check_errors(content)

        # login successful, parse key from response
        self._key = content.split("window.parent.location.href = \"")[1].split("/")[3]

        self.logged_in = True
        self._requests = RequestConstructor(self.base_url, self._key)

        if keepalive:
            Thread(target=self._keepalive_thread, daemon=True) \
                .start()

    def _keepalive_thread(self):
        """sends request every 3 second. started by login method"""
        while self.logged_in:
            self.get_display_status()
            time.sleep(3)

    @login_required
    def logout(self):
        """you might need to log out, router prevents other devices from logging in"""
        self._session.get(**self._requests.logout)
        self.logged_in = False

    @login_required
    def reboot(self):
        """reboots router

        Returns:
            requests.Response
        """
        self.logged_in = False  # session is lost
        return self._session.get(**self._requests.reboot)

    @login_required
    def get_wireless_clients(self):
        """
        Returns:
            List[models.Device]
        """
        data_json = self._session.post(**self._requests.wireless_clients).json()

        return [Device(**i) for i in data_json["data"]]

    @login_required
    def get_wired_clients(self):
        """
        Returns:
            List[models.Device]
        """
        data_json = self._session.post(**self._requests.wired_clients).json()

        return [Device(**i) for i in data_json["data"]]

    @login_required
    def get_display_status(self):
        """
        Returns:
            models.DisplayStatus
        """
        return DisplayStatus(**self._session.post(**self._requests.display_status).json())

    @login_required
    def get_internet_info(self):
        """
        Returns:
            models.InternetInfo
        """
        return InternetInfo(**self._session.post(**self._requests.internet_info).json()["data"])

    @login_required
    def set_wireless_settings(self, ssid, password, wireless_enabled=True, hide_ssid=False):
        """

        Args:
            ssid(str): new/current SSID
            password(str): new/current password. pass empty string to disable password
        Parameters:
            wireless_enabled(bool): *enable or disable wireless
            hide_ssid(bool): hide or *show ssid
        Returns:
            requests.Response
        """
        # TODO: scrape current SSID & Password and allow not re-setting it
        params = {
            "radioSwitch_2G": "on" if wireless_enabled else "off",
            "SSID_2G": ssid,
            "password_2G": password,
            "password_2G_disabled": "true" if len(password) == 0 else "",
            "Save": "Save"
        }
        if hide_ssid:
            params["hideSSID_2G"] = "true"

        return self._session.get(**self._requests.wireless_settings, params=params)
