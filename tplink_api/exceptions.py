class LoginFailedException(Exception):
    MESSAGE = "The username or password is incorrect"


class InvalidCredentialsException(Exception):
    MESSAGE = "The username and password can contain between 1 - 15 characters and may not include spaces."
    pass


class TooManyAttemptsException(Exception):
    MESSAGE = "You have exceeded ten attempts, please try again in two hours"


class TooManyAdminsException(Exception):
    MESSAGE = "The router allows only one administrator to login at the same time, please try again later."


class NotLoggedInException(Exception):
    """decorator for methods that require login"""
    pass


# used in reverse searching exceptions based on javascript variable
EXCEPTIONS = {
    "0": TooManyAdminsException,
    "1": TooManyAttemptsException,
    "2": LoginFailedException,
}
