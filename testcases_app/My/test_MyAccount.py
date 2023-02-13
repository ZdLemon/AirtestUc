# coding:utf-8

__author__ = "ligeit"

import sys
import time
import pytest
import allure
import os
import logging
from airtest.core.api import *
from setting import P1, P2, P3
from airtest.core.android.adb import *
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from setting import UUIDS
               
@allure.feature("我的")
@allure.story("我的-我的账户")
class TestClass():
    """
    我的-我的账户各个功能操作按钮遍历
    """
    
    @allure.severity(P3)        
    @allure.title("我的-我的账户：遍历我的账户")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_01(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        my_account = ["钱包", "优惠券", "礼券", "资产"]
        for i in my_account:
            poco(i).click()
            
            if i == "钱包":
                assert_equal(poco("我的钱包", touchable=False).wait(8).exists(), True, msg=f"成功进入{i}页面")
            elif i == "资产":
                assert_equal(poco("我的账户", touchable=False).wait(8).exists(), True, msg=f"成功进入{i}页面")
            else:
                assert_equal(poco(i).wait(8).exists(), True, msg=f"成功进入{i}页面")
                    
            poco(name="android.view.View", touchable=True).click()
                
    @allure.severity(P3)            
    @allure.title("我的-我的账户-我的钱包：遍历我的钱包")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_02(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
                 
        poco("钱包").click()

        assert_equal(poco("我的钱包", touchable=False).wait(8).exists(), True, msg="我的钱包存在")
        assert_equal(poco("充值").wait(8).exists(), True, msg="充值存在")
        assert_equal(poco("交易明细").wait(8).exists(), True, msg="交易明细存在")
        assert_equal(poco("历史账单").wait(8).exists(), True, msg="历史账单存在")
            
        for i in ["充值", "交易明细", "历史账单", "银行卡签约", "支付管理", "电子礼券", "运费补贴券"]:
            if poco(i).wait(8).exists():
                poco(i).click()
            # 返回我的钱包
            poco(name="android.view.View", touchable=True).wait(8).click()
        # 返回我的
        poco(name="android.view.View", touchable=True).wait(8).click()  
               
    @allure.severity(P3)            
    @allure.title("我的-我的账户-交易明细：遍历交易明细")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_03(self, uuid):

        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
                
        poco("钱包").click()
        poco("交易明细").click()
        assert_equal(poco("交易明细").wait(8).exists(), True, msg="交易明细存在")
        assert_equal(poco("全部交易类型").wait(8).exists(), True, msg="全部交易类型存在")
        assert_equal(poco("统计").wait(8).exists(), True, msg="统计存在")
            
        indexs = ["全部交易类型", "汇入", "退货", "购货", "提现", "退款", "信用额", "转款", "其他", "预售定金", "定金返还"]
        y = 0.08
        count = 0
        while count < 11:
            for i in indexs:
                if poco(i).wait(8).exists():
                    assert_equal(poco("交易明细").wait(8).exists(), True, msg="交易明细存在")
                    assert_in(poco(i).get_name(), indexs, msg= i)

                    poco(i).click()
                    poco(indexs[0]).swipe([0, -y])
                    poco("确定").click()
                    sleep(1)

                    y += 0.05
                    count += 1
                    continue
        # 返回我的钱包
        poco(name="android.view.View", touchable=True).wait(8).click()


