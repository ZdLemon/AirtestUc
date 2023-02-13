# coding:utf-8

__author__ = "ligeit"

import time
import allure
import json
import re
import logging
from airtest.core.api import *
from setting import P1, P2, P3, M7035
from utils.step_for_uuids import step_for_uuids
from utils.log_report import log_report
from utils.logger import logger


@allure.feature("我的-我的服务中心")
@allure.story("我的-我的服务中心-商城退货")
class TestClass:
    """
    我的-我的服务中心-商城退货
    """
      
    @allure.severity(P3)            
    @allure.title("我的-我的服务中心-商城退货：遍历所有状态tab列表检查")
    @log_report()
    def test_01(self):

        @step_for_uuids()
        def step_01(poco):  
                
            poco("商城退货").click()
            assert_equal(poco("商城退换货列表").exists(), True, msg="商城退换货列表")

            poco("全部\n第 1 个标签，共 4 个").click()
            assert_equal(poco("暂无数据").exists(), True, msg="暂无数据")

            poco("待审批\n第 2 个标签，共 4 个").click()
            assert_equal(poco("暂无数据").exists(), True, msg="暂无数据")

            poco("已完成\n第 3 个标签，共 4 个").click()
            assert_equal(poco("暂无数据").exists(), True, msg="暂无数据")

            poco("已取消\n第 4 个标签，共 4 个").click()
            assert_equal(poco("暂无数据").exists(), True, msg="暂无数据")

            # 退出订单管理，返回服务中心首页
            poco(name="android.view.View", touchable=True).click()

        step_01()
        

