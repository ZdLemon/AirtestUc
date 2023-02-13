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
@allure.story("我的-我的服务中心-订单管理")
class TestClass:
    """
    我的-我的服务中心-订单管理
    """
      
    @allure.severity(P2)            
    @allure.title("我的-我的服务中心-订单管理：遍历所有状态tab列表检查")
    @log_report()
    def test_01(self):

        @step_for_uuids()
        def step_01(poco):  
                
            poco("订单管理").click()
            poco("全部\n第 1 个标签，共 6 个").click()
            assert poco("全部\n第 1 个标签，共 6 个", selected=True).exists() # 全部tab列表是当前活动列表

            assert poco("待发货\n第 2 个标签，共 6 个", selected=False).exists()
            poco("待发货\n第 2 个标签，共 6 个").click()
            assert poco("待发货\n第 2 个标签，共 6 个", selected=True).exists() # 待发货tab列表是当前活动列表

            assert poco("待收货\n第 3 个标签，共 6 个", selected=False).exists()
            poco("待收货\n第 3 个标签，共 6 个").click()
            assert poco("待收货\n第 3 个标签，共 6 个", selected=True).exists() # 待收货tab列表是当前活动列表

            assert poco("已完成\n第 4 个标签，共 6 个", selected=False).exists()
            poco("已完成\n第 4 个标签，共 6 个").click()
            assert poco("已完成\n第 4 个标签，共 6 个", selected=True).exists() # 已完成tab列表是当前活动列表

            assert poco("已退货\n第 5 个标签，共 6 个", selected=False).exists()
            poco("已退货\n第 5 个标签，共 6 个").click()
            assert poco("已退货\n第 5 个标签，共 6 个", selected=True).exists() # 已退货tab列表是当前活动列表

            assert poco("已取消\n第 6 个标签，共 6 个", selected=False).exists()
            poco("已取消\n第 6 个标签，共 6 个").click()
            assert poco("已取消\n第 6 个标签，共 6 个", selected=True).exists() # 已取消tab列表是当前活动列表
            # 退出订单管理，返回服务中心首页
            poco(name="android.view.View", touchable=True).click()

        step_01()
        
    @allure.severity(P2)            
    @allure.title("我的-我的服务中心-订单管理：详情检查")
    @log_report()
    def test_02(self):

        @step_for_uuids()
        def step_01(poco): 
                  
            poco("订单管理").click()
            # 押货一件商品
            if poco(nameMatches="^订单号：SG.+\n[待发货|待收货|已完成|已退货|已取消]+\n购货人：.+ .+\n共\d+件\n合计积分(PV):\d+\.\d{1,1}			实付金额:￥\d+\.\d{1,1}$").exists():
                stars01 = poco(nameMatches="^订单号：SG.+\n[待发货|待收货|已完成|已退货|已取消]+\n购货人：.+ .+\n共\d+件\n合计积分(PV):\d+\.\d{1,1}			实付金额:￥\d+\.\d{1,1}$")
                for star in stars01:
                    logger.info(star.get_name(), desc="押货商品名称")
                    t = star.get_name()
                    star.click(0.5,0.18)
                    assert_equal(poco("订单详情", touchable=False).get_name(), "订单详情", msg="订单详情")
                    # 退出订单详情
                    poco(name="android.view.View", touchable=True).click()
                
            # 退出订单管理，返回服务中心首页
            poco(name="android.view.View", touchable=True).click()

        step_01()
        
    @allure.severity(P2)            
    @allure.title("我的-我的服务中心-订单管理：待发货订单【发货】检查")
    @log_report()
    def test_03(self):

        @step_for_uuids()
        def step_01(poco):  
                
            poco("订单管理").click()
            poco("待发货\n第 2 个标签，共 6 个").click()
            
            # 点击【X】，不发货
            if poco("发货").exists():
                poco("发货").click([0.83, 0.55])
                assert poco(nameMatches="^收货人信息\n交付方式：\n自提\n收货人姓名：\n.+\n收货人手机：\n\d+$").exists()
                poco(nameMatches="^订单号:  SG.+$").click([0.935, 0.4])
                    
                # 确认发货
                poco("发货").click([0.83, 0.55])
                assert poco(nameMatches="^收货人信息\n交付方式：\n自提\n收货人姓名：\n.+\n收货人手机：\n\d+$").exists()
                poco("确认发货").click([0.5, 0.97]) 
                assert_equal(poco("订单管理", touchable=False).get_name(), "订单管理", msg="订单管理")
            else:
                assert_equal(poco("暂无数据").exists(), True, "暂无数据")
    
        step_01()



