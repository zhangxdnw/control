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
    device.app_stop_all()
    device.screen_on()


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
                device.app_stop(app_package)
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
    # 点击 我
    print('点击我')
    device.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/root_view"]/android.widget.FrameLayout[5]').click()
    time.sleep(1)
    top_activity = app_utils.top_activity(device)
    if top_activity != 'com.ss.android.ugc.aweme.account.business.login.DYLoginActivity':
        assert top_activity == 'com.ss.android.ugc.aweme.main.MainActivity', '当前界面不是主界面:' + top_activity
        print('点击选项按钮')
        device(resourceId='com.ss.android.ugc.aweme:id/fuy').click_exists(2)

        top_activity = app_utils.top_activity(device)
        assert top_activity == 'com.ss.android.ugc.aweme.main.MainActivity', '当前界面不是主界面:' + top_activity
        print('点击设置按钮')
        device(resourceId='com.ss.android.ugc.aweme:id/kx8').click_exists(2)

        top_activity = app_utils.top_activity(device)
        assert top_activity == 'com.ss.android.ugc.aweme.setting.ui.DouYinSettingNewVersionActivity', \
            '当前界面不是设置界面:' + top_activity
        print('滑动到最底部')
        device.swipe(0.5 * width, 0.9 * height, 0.5 * width, 0.1 * height)

        top_activity = app_utils.top_activity(device)
        assert top_activity == 'com.ss.android.ugc.aweme.setting.ui.DouYinSettingNewVersionActivity', \
            '当前界面不是设置界面:' + top_activity
        print('点击退出按钮')
        device(resourceId='com.ss.android.ugc.aweme:id/logout').click_exists(2)

        print('确认退出')
        device(resourceId='android:id/button1').click_exists(2)
    else:
        print('已切换到登录界面，完成退出动作')
    if app_utils.input_shown(device):
        device.press("back")
        time.sleep(1)
    device.press('back')
    time.sleep(2)


def login(account: str, password: str, phone: str):
    width, height = device.window_size()
    # 点击 我
    print('点击我')
    device.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/root_view"]/android.widget.FrameLayout[5]').click()
    time.sleep(1)
    top_activity = app_utils.top_activity(device)
    if top_activity == 'com.ss.android.ugc.aweme.account.business.login.DYLoginActivity':
        if device(resourceId='com.ss.android.ugc.aweme:id/jga').exists:  # 以其他帐号登录
            y_p = device(resourceId='com.ss.android.ugc.aweme:id/jga').center()[1]
            print('点击以其他帐号 登录')
            device.click(int(0.592 * width), y_p)
            time.sleep(3)
        if device(resourceId='com.ss.android.ugc.aweme:id/one_key_login_other_phone_login').exists:  # 其他手机号登录
            print('点击其他手机号码登录')
            device(resourceId='com.ss.android.ugc.aweme:id/one_key_login_other_phone_login').click(3)
        print('点击密码登录')
        device(resourceId='com.ss.android.ugc.aweme:id/fe5').click_exists(timeout=3)  # 密码登录
        print('输入帐号' + account)
        device(resourceId='com.ss.android.ugc.aweme:id/gh=').send_keys(account)  # 输入帐号
        print('点击同意协议')
        device(resourceId='com.ss.android.ugc.aweme:id/gyj').click_exists(1)  # 同意协议
        print('输入密码' + password)
        device(resourceId='com.ss.android.ugc.aweme:id/gfh').send_keys(password)  # 输入密码
        print('点击登录')
        device(resourceId='com.ss.android.ugc.aweme:id/login').click(3)  # 登录
        print('点击跳过')
        device(resourceId='com.ss.android.ugc.aweme:id/iaw').click_exists(3)  # 跳过
    else:
        assert top_activity == 'com.ss.android.ugc.aweme.main.MainActivity', '当前界面不是主界面:' + top_activity
        # 查找指定view 证明已登录


def find_friend(account: str):
    return


def star():
    return


def like():
    return


def play():
    return
