# coding:utf-8

__author__ = "ligeit"

from airtest.core.api import *
import time
import pytest
import allure
from setting import UUIDS
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from utils.to_home import to_home


@allure.title("我的")
@pytest.fixture(scope="function", autouse=True)
def to_my():
    
    for uuid in UUIDS:
        set_current(uuid)
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        try:
            # 我的页面
            while poco("我的服务中心", touchable=True).exists() is False:
                if poco("我的\n第 5 个标签，共 5 个").exists():
                    poco("我的\n第 5 个标签，共 5 个").click()  
                else:      
                    poco(name="android.view.View", touchable=True).wait(1).click()
        except Exception as e:
            to_home(poco)
            poco("我的\n第 5 个标签，共 5 个").click()
            raise e
    yield
    
    for uuid in UUIDS:
        set_current(uuid)
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        try:
            # 我的页面
            while poco("我的服务中心", touchable=True).exists() is False:
                if poco("我的\n第 5 个标签，共 5 个").exists():
                    poco("我的\n第 5 个标签，共 5 个").click()  
                else:      
                    poco(name="android.view.View", touchable=True).wait(1).click()
        except Exception as e:
            to_home(poco)
            poco("我的\n第 5 个标签，共 5 个").click()
            raise e



