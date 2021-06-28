import datetime

from adbutils import AdbDevice, AdbClient
import uiautomator2 as u2


def launch_app(device: u2.Device, package_name: str, activity: str):
    device.app_start(package_name=package_name, activity=activity)


def top_app(device: u2.Device) -> str:
    return device.app_current()['package']


def top_activity(device: u2.Device) -> str:
    return device.app_current()['package'] + device.app_current()['activity']


def activity_window(device: u2.Device, activity: str) -> list:
    result = device.shell("dumpsys window " + activity + " | grep \"Window #\"")
    return result.output.strip().split('\n')


def deal_with_permission() -> int:
    return 0


def deal_with_common_dialog() -> int:
    return 0


def deal_with_upgrade_dialog() -> int:
    return 0


if __name__ == '__main__':
    current_device = u2.connect()
    result = top_app(current_device)
    # act = top_activity(current_device)
    # count = activity_window(current_device, act)
    print(current_device.app_info(result))
