import os
from types import ModuleType
from typing import Optional

import uiautomator2 as u2
import importlib
import str_utils

dir_name = os.path.dirname(os.path.abspath(__file__))
package_name = dir_name[dir_name.rindex(os.path.sep) + 1:]
module: ModuleType


def load_script(device_serial: str, app_package: str, version_code: int):
    assert device_serial != '' and device_serial.strip() != '', '设备序列号为空'
    assert app_package != '' and app_package.strip() != '', '应用包名为空'
    assert package_name == app_package.replace('.', '_'), '应用包名不匹配'
    assert version_code > 0, '应用版本号为0'
    device = u2.connect(device_serial)
    app_info = device.app_info(package_name=app_package)
    assert app_info['versionCode'] == version_code, '应用版本信息不匹配'
    assert os.listdir(dir_name).__contains__(str(app_info['versionCode'])), '找不到对应版本的脚本'
    load_file_path = 'app.' + package_name + '.' + str(app_info['versionCode']) + '.app_control'
    print('加载脚本:' + load_file_path)
    global module
    module = importlib.import_module(load_file_path)
    print(module)


def do_action(action: str, params: Optional[dict] = None):
    if params is not None:
        arg = str_utils.dict2params(params)
        print(arg)
        execute = 'module.' + action + '(' + arg + ')'
    else:
        execute = 'module.' + action + '()'
    print(execute)
    eval(execute)


if __name__ == '__main__':
    load_script('80eeeab9', 'com.ss.android.ugc.aweme', 160502)
    do_action("init", {'serial': '80eeeab9'})
    do_action("launch_app",
              {'app_package': 'com.ss.android.ugc.aweme', 'activity': 'com.ss.android.ugc.aweme.main.MainActivity'})
    do_action("logout")
    do_action("login", {'account': '13243785230', 'password': 'zxd19860731', 'phone': '13243785230'})
    # print(dir_name)
