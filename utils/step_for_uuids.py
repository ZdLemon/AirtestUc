# coding:utf-8


from functools import wraps
import allure
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from setting import UUIDS
import asyncio


def step_for_uuids():
    """
    遍历设备，依次在各台设备上执行step
    """
    def decorate(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            for uuid in UUIDS:
                set_current(uuid)
                poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
                # 手机品牌
                Manufacturer = shell('getprop ro.product.manufacturer')
                # 手机型号
                Version = shell('getprop ro.product.model')

                log(f"执行设备：{Manufacturer}:{Version}:{uuid}")
                
                with allure.step(f"{Manufacturer}:{Version}:{uuid}"):             
                    func(*args, **kwargs, poco=poco)
        return wrapper
    return decorate