# coding:utf-8

__author__ = "ligeit"

import time
import pytest
import allure
from airtest.core.api import *
from setting import UUIDS
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from utils.to_home import to_home


@allure.title("我的-我的服务中心")
@pytest.fixture(scope="function", autouse=True)
def to_my_store():
    
    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
    try:
        # 我的服务中心页面
        while poco("我的服务中心", touchable=False).exists() is False:
            if poco("我的服务中心", touchable=True).exists():
                poco("我的服务中心", touchable=True).click()
                if poco("提示").wait(2).exists():
                    poco("android.view.View", touchable=True).click()
            elif poco("我的\n第 5 个标签，共 5 个").exists():
                poco("我的\n第 5 个标签，共 5 个").click()
            elif poco("返回服务中心首页").exists():
                poco("返回服务中心首页").click()
            else:      
                poco(name="android.view.View", touchable=True).wait(1).click()
    except Exception as e:
        to_home(poco)
        poco("我的\n第 5 个标签，共 5 个").click()
        poco("我的服务中心", touchable=True).click()
        raise e
    yield
    
    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
    try:
        # 我的服务中心页面
        while poco("我的服务中心", touchable=False).exists() is False:
            if poco("我的服务中心", touchable=True).exists():
                poco("我的服务中心", touchable=True).click()
                if poco("提示").wait(2).exists():
                    poco("android.view.View", touchable=True).click()
            elif poco("我的\n第 5 个标签，共 5 个").exists():
                poco("我的\n第 5 个标签，共 5 个").click()
            elif poco("返回服务中心首页").exists():
                poco("返回服务中心首页").click()
            else:      
                poco(name="android.view.View", touchable=True).wait(1).click()
    except Exception as e:
        to_home(poco)
        poco("我的\n第 5 个标签，共 5 个").click()
        poco("我的服务中心", touchable=True).click()
        raise e



