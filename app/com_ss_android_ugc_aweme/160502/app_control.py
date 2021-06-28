import sys
import time
from time import sleep

import uiautomator2 as u2

from uiautomator2 import Device
import app_utils

sys.path.append("..")
from .. import common

device: Device


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
    # 加入一次滑动 取消蒙板
    width, height = device.window_size()
    device.swipe(0.5 * width, 0.7 * height, 0.5 * width, 0.3 * height)
    return
