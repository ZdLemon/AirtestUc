# coding:utf-8

__author__ = "hewei"


import pytest
import allure
from airtest.core.api import *
from airtest.core.android.android import *
from setting import PACKAGE, UUIDS
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from utils.to_home import to_home


def pytest_addoption(parser):
    parser.addoption(
        "--uuid",
        action= "store",
        default= "C7YNW19808003659",
        help= "安卓设备序列号",
    )
    parser.addoption(
        "--mobile",
        action= "store",
        default= "15876361823",
        help= "会员登录手机号",
    )
 

@allure.title("初始化自定义命令行参数")
@pytest.fixture(scope="session", autouse=True)
def init_cmd(request):
    uuid = request.config.getoption("--uuid")
    mobile = request.config.getoption("--mobile")
    dev = f"android://127.0.0.1:5037/{uuid}"
    os.environ["uuid"] = uuid
    os.environ["dev"] = dev
    os.environ["mobile"] = mobile

    return dev


@allure.title("关闭app")
@pytest.fixture(scope="session")
def stop_app():
   
    yield 
    for uuid in UUIDS:
        set_current(uuid)
        stop_app(PACKAGE)
        clear_app(PACKAGE)
        uninstall(PACKAGE)

  
@allure.title("app首页")
@pytest.fixture(scope="class", autouse=True)
def to_app_home():

    for uuid in UUIDS:
        set_current(uuid)
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        try:
            # 进入APP首页
            while poco(nameMatches="^首页\n.+").exists() is False:         
                poco(name="android.view.View", touchable=True).wait(1).click() 
        except Exception as e:
            to_home(poco)
            raise e
    yield
    
    for uuid in UUIDS:
        set_current(uuid)
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        try:
            # 进入APP首页
            while poco(nameMatches="^首页\n.+").exists() is False:         
                poco(name="android.view.View", touchable=True).wait(1).click() 
        except Exception as e:
            to_home(poco)
            raise e


