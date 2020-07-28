# TODO: include HTTP method in constructor
class RequestConstructor:
    def __init__(self, base_url, key=""):
        self.base_url = base_url
        self.key = key

    @property
    def login(self):
        return {
            "url": f"{self.base_url}/userRpm/LoginRpm.htm",
            "params": {"Save": "Save"}
        }

    @property
    def logout(self):
        return {
            "url": f"{self.base_url}/{self.key}/userRpm/LogoutRpm.htm",
            "headers": {"Referer": f"{self.base_url}/{self.key}/userRpm/BasicNetworkMapRpm.htm"}
        }

    @property
    def reboot(self):
        return {
            "url": f"{self.base_url}/{self.key}/userRpm/SysRebootRpm.htm",
            "params": {"Reboot": "Reboot"},
            "headers": {"Referer": f"{self.base_url}/{self.key}/userRpm/BasicNetworkMapRpm.htm"}
        }

    @property
    def display_status(self):
        return {
            "url": f"{self.base_url}/{self.key}/data/map_display_status_form.json",
            "headers": {"Referer": f"{self.base_url}/{self.key}/userRpm/BasicNetworkMapRpm.htm"},
            "data": {"operation": "load"}
        }

    @property
    def wireless_clients(self):
        return {
            "url": f"{self.base_url}/{self.key}/data/map_access_wireless_client_grid.json",
            "headers": {"Referer": f"{self.base_url}/{self.key}/userRpm/BasicNetworkMapRpm.htm"},
            "data": {"operation": "load"}
        }

    @property
    def wired_clients(self):
        return {
            "url": f"{self.base_url}/{self.key}/data/map_access_wire_client_grid.json",
            "headers": {"Referer": f"{self.base_url}/{self.key}/userRpm/BasicNetworkMapRpm.htm"},
            "data": {"operation": "load"}
        }

    @property
    def internet_info(self):
        return {
            "url": f"{self.base_url}/{self.key}/data/map_internet_info_form.json",
            "headers": {"Referer": f"{self.base_url}/{self.key}/userRpm/BasicNetworkMapRpm.htm"},
            "data": {"operation": "read"}
        }

    @property
    def wireless_settings(self):
        url = f"{self.base_url}/{self.key}/userRpm/BasicWirelessRpm.htm"
        return {
            "url": url,
            "headers": {"Referer": url},
        }
