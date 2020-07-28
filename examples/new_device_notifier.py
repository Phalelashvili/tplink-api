#!/usr/bin/env python3
import os
import time
from tplink_api import Client


def diff(list1, list2):
    old_macs = [i.mac_addr for i in list1]
    return [device for device in list2 if device.mac_addr not in old_macs]


if __name__ == '__main__':
    client = Client()
    client.login("admin", "admin")

    old = client.get_wireless_clients()
    while True:
        new = client.get_wireless_clients()
        _diff = diff(old, new)
        if len(_diff) > 0:
            if os.name == "posix":  # doesn't work on mac
                # os.system(f"zenity --info --title='' --text='{_diff}'")
                os.system(f"notify-send 'New device(s) connected' '{_diff}'")
            else:  # windows
                os.system(f"msg %username% {_diff}")
        old = new

        time.sleep(3)
