import uiautomator2 as u2
import app_utils


def common_launch_app(device: u2.Device, app_package: str, activity: str):
    app_utils.launch_app(device, app_package, activity)
