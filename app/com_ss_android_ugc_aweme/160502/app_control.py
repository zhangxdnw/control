import sys
import time

import uiautomator2 as u2

from uiautomator2 import Device
import app_utils

sys.path.append("..")
from .. import common

device: Device
target_app_package: str


def init(serial: str):
    global device
    device = u2.connect(serial)


def launch_app(app_package: str, activity: str):
    count: int = 0
    try1: bool = False
    try2: bool = False
    while count < 10:
        # 尝试启动主界面
        print('while loop')
        common.common_launch_app(device, app_package, activity)
        # 等待页面启动
        time.sleep(2)
        # 获取校验信息
        top_app = app_utils.top_app(device)
        top_activity = app_utils.top_activity(device)
        if top_app == app_package:  # 应用被其他应用遮盖
            if top_activity == activity:  # 其他界面遮盖
                window_count = len(app_utils.activity_window(device, activity))
                if window_count == 1:  # 完成启动
                    print('完成启动检测')
                    break
                else:  # 不止一个窗口，被其他弹窗遮盖
                    if not try1:
                        print('尝试隐私点击隐私声明弹窗')
                        device(resourceId='com.ss.android.ugc.aweme:id/bb_').click_exists()
                        try1 = True
                    elif not try2:
                        print('尝试点击个人信息保护')
                        device(resourceId='com.ss.android.ugc.aweme:id/bb1').click_exists()
                        try2 = True
                    else:
                        print('已尝试完')
            else:
                print('目标界面被遮盖:%s, 重试次数：%d' % (top_activity, count))
        elif top_app == 'com.android.permissioncontroller':
            print('权限弹窗界面,尝试点击同意')
            device(resourceId='com.android.permissioncontroller:id/permission_allow_button').click_exists()
        else:
            print('目标应用被遮盖:%s, 重试次数：%d' % (top_app, count))
        count += 1
    print(count)
    top_app = app_utils.top_app(device)
    top_activity = app_utils.top_activity(device)
    window_count = len(app_utils.activity_window(device, activity))
    assert top_app == app_package and top_activity == activity and window_count == 1
    global target_app_package
    target_app_package = top_app
    # 加入一次滑动 取消蒙板
    width, height = device.window_size()
    device.swipe(0.5 * width, 0.7 * height, 0.5 * width, 0.3 * height)
    return


def logout():
    width, height = device.window_size()
    #
    device.click(int(width * 0.9), int(height * 0.95))
    time.sleep(0.5)
    #
    device(resourceId='com.ss.android.ugc.aweme:id/fqo').click_exists()
    time.sleep(0.5)
    #
    device(resourceId='com.ss.android.ugc.aweme:id/kry').click_exists()
    time.sleep(0.5)
    #
    device.swipe(0.5 * width, 0.9 * height, 0.5 * width, 0.1 * height)
    time.sleep(0.5)
    #
    device(resourceId='com.ss.android.ugc.aweme:id/logout').click_exists()
    time.sleep(0.5)
    #
    device(resourceId='android:id/button1').click_exists()
    time.sleep(3)


def login(account: str, password: str, phone: str):
    width, height = device.window_size()
    #
    device.click(int(width * 0.9), int(height * 0.95))
    time.sleep(1)
    #
    device.click(int(width) * 0.591, int(height * 0.941))
    time.sleep(1)
    #
    device(resourceId='com.ss.android.ugc.aweme:id/fa4').click_exists(timeout=3)
    time.sleep(1)
    #
    device(resourceId='com.ss.android.ugc.aweme:id/gdm').send_keys(account)
    device(resourceId='com.ss.android.ugc.aweme:id/gtc').click_exists()
    device(resourceId='com.ss.android.ugc.aweme:id/gax').send_keys(password)
    device(resourceId='com.ss.android.ugc.aweme:id/login').click()
    #
    time.sleep(1)
    device(resourceId='com.ss.android.ugc.aweme:id/h85').click_exists()


def find_friend(account: str):
    return


def star():
    return


def like():
    return


def play():
    return
