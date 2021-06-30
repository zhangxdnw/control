import datetime
import re

from adbutils import AdbDevice, AdbClient
import uiautomator2 as u2


def launch_app(device: u2.Device, package_name: str, activity: str):
    device.app_start(package_name=package_name, activity=activity)


def top_app(device: u2.Device) -> str:
    return device.app_current()['package']


def top_activity(device: u2.Device) -> str:
    return device.app_current()['package'] + device.app_current()['activity']


def activity_window(device: u2.Device, activity: str) -> list:
    wins = device.shell("dumpsys window " + activity + " | grep \"Window #\"")
    return wins.output.strip().split('\n')


def input_shown(device: u2.Device) -> bool:
    input_info = device.shell('dumpsys input_method | grep mInputShown').output.strip()
    return re.compile(r"mInputShown=(\S+)").findall(input_info)[0] == 'true'


def deal_with_permission() -> int:
    return 0


def deal_with_common_dialog() -> int:
    return 0


def deal_with_upgrade_dialog() -> int:
    return 0


if __name__ == '__main__':
    current_device = u2.connect()
    print(input_shown(current_device))
