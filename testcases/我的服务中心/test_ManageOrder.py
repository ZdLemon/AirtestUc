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
@allure.story("我的-我的服务中心-押货单管理")
class TestClass:
    """
    我的-我的服务中心-押货单管理
    """
    
    @allure.severity(P2)            
    @allure.title("我的-我的服务中心-押货单管理：遍历所有状态tab列表检查")
    @log_report()
    def test_01(self):

        @step_for_uuids()
        def step_01(poco):   
             
            poco("押货单管理").click()
            poco("全部\n第 1 个标签，共 5 个").click()
            assert poco("全部\n第 1 个标签，共 5 个", selected=True).exists() # 全部tab列表是当前活动列表

            assert poco("待发货\n第 2 个标签，共 5 个", selected=False).exists()
            poco("待发货\n第 2 个标签，共 5 个").click()
            assert poco("待发货\n第 2 个标签，共 5 个", selected=True).exists() # 待发货tab列表是当前活动列表

            assert poco("部分发货\n第 3 个标签，共 5 个", selected=False).exists()
            poco("部分发货\n第 3 个标签，共 5 个").click()
            assert poco("部分发货\n第 3 个标签，共 5 个", selected=True).exists() # 部分发货tab列表是当前活动列表

            assert poco("已完成\n第 4 个标签，共 5 个", selected=False).exists()
            poco("已完成\n第 4 个标签，共 5 个").click()
            assert poco("已完成\n第 4 个标签，共 5 个", selected=True).exists() # 已完成tab列表是当前活动列表

            assert poco("已取消\n第 5 个标签，共 5 个", selected=False).exists()
            poco("已取消\n第 5 个标签，共 5 个").click()
            assert poco("已取消\n第 5 个标签，共 5 个", selected=True).exists() # 已取消tab列表是当前活动列表
            # 退出押货单管理
            poco(name="android.view.View", touchable=True).click()

        step_01()
        
    @allure.severity(P2)            
    @allure.title("我的-我的服务中心-押货单管理：详情检查")
    @log_report()
    def test_02(self):

        @step_for_uuids()
        def step_01(poco):     
            poco("押货单管理").click()
            # 押货一件商品
            if poco(nameMatches="^YH.+\n[待发货|部分发货|已完成|已取消]+\n下单时间：\d{4,4}-\d{2,2}-\d{2,2} \d{2,2}:\d{2,2}:\d{2,2} \n.+\nx\d+\n.+\n押货价：￥\d+\.\d+\n押货合计：￥\d+\.\d+$").exists():
                stars01 = poco(nameMatches="^YH.+\n[待发货|部分发货|已完成|已取消]+\n下单时间：\d{4,4}-\d{2,2}-\d{2,2} \d{2,2}:\d{2,2}:\d{2,2} \n.+\nx\d+\n.+\n押货价：￥\d+\.\d+\n押货合计：￥\d+\.\d+$")
                for star in stars01:
                    logger.info(star.get_name(), desc="押货单")
                    t = star.get_name()
                    star.click()
                    assert poco("押货单详情").wait(1).exists()
                    assert poco("修改记录").wait(1).exists()
                    assert poco(t[19:22]).exists() # 押货单状态
                    assert poco('押货单号：{}{}'.format(t[:18], re.search("\n下单时间：\d{4,4}-\d{2,2}-\d{2,2} \d{2,2}:\d{2,2}:\d{2,2} ", t).group())).exists() # 押货单号+时间
                    assert poco(re.search("押货合计：￥\d+\.\d+", t).group()).exists() # 押货合计金额
                    # 退出押货单详情
                    poco(name="android.view.View", touchable=True).click()
                
            # 押货多件商品
            if poco(nameMatches="^YH.+\n[待发货|部分发货|已完成|已取消]+\n下单时间：\d{4,4}-\d{2,2}-\d{2,2} \d{2,2}:\d{2,2}:\d{2,2} \n共\d+件\n押货合计：￥\d+\.\d+$").exists():
                stars02 = poco(nameMatches="^YH.+\n[待发货|部分发货|已完成|已取消]+\n下单时间：\d{4,4}-\d{2,2}-\d{2,2} \d{2,2}:\d{2,2}:\d{2,2} \n共\d+件\n押货合计：￥\d+\.\d+$")
                for star in stars02:
                    logger.info(star.get_name(), desc="押货单")
                    t = star.get_name()
                    star.click([0.5, 0.2]) # 中心点可能在产品预览图上，所以偏上一点
                    assert poco("押货单详情").wait(1).exists()
                    assert poco("修改记录").wait(1).exists()
                    assert poco(t[19:22]).exists() # 押货单状态
                    assert poco('押货单号：{}{}'.format(t[:18], re.search("\n下单时间：\d{4,4}-\d{2,2}-\d{2,2} \d{2,2}:\d{2,2}:\d{2,2} ", t).group())).exists() # 押货单号+时间
                    assert poco(re.search("押货合计：￥\d+\.\d+", t).group()).exists() # 押货合计金额
                    # 退出押货单详情
                    poco(name="android.view.View", touchable=True).click()
            
            # 退出押货单管理
            poco(name="android.view.View", touchable=True).click()

        step_01()
        
    @allure.severity(P3)            
    @allure.title("我的-我的服务中心-押货单管理：详情修改记录检查")
    @log_report()
    def test_03(self):

        @step_for_uuids()
        def step_01(poco): 
                 
            poco("押货单管理").click()
            # 押货一件商品
            if poco(nameMatches="^YH.+\n[待发货|部分发货|已完成|已取消]+\n下单时间：\d{4,4}-\d{2,2}-\d{2,2} \d{2,2}:\d{2,2}:\d{2,2} \n.+\nx\d+\n.+\n押货价：￥\d+\.\d+\n押货合计：￥\d+\.\d+$").exists():
                stars01 = poco(nameMatches="^YH.+\n[待发货|部分发货|已完成|已取消]+\n下单时间：\d{4,4}-\d{2,2}-\d{2,2} \d{2,2}:\d{2,2}:\d{2,2} \n.+\nx\d+\n.+\n押货价：￥\d+\.\d+\n押货合计：￥\d+\.\d+$")
                for star in stars01:
                    logger.info(star.get_name(), desc="押货单")
                    t = star.get_name()
                    star.click() # 进入详情
                    poco("修改记录").wait(1).click() # 进入修改记录
                    assert poco("押货单修改记录").exists()
                    assert poco(f"押货单号：{t[:18]}").exists()
                    assert poco(re.search("下单时间：\d{4,4}-\d{2,2}-\d{2,2} \d{2,2}:\d{2,2}", t).group()).exists()
                    assert poco("复制").exists()
                    poco("复制").click()
                    poco("复制", touchable=True).exists()
                        
                    # 退出修改记录        
                    poco(name="android.view.View", touchable=True).click()
                    # 退出押货单详情
                    poco(name="android.view.View", touchable=True).click()   
                
            # 押货多件商品
            if poco(nameMatches="^YH.+\n[待发货|部分发货|已完成|已取消]+\n下单时间：\d{4,4}-\d{2,2}-\d{2,2} \d{2,2}:\d{2,2}:\d{2,2} \n共\d+件\n押货合计：￥\d+\.\d+$").exists():
                stars02 = poco(nameMatches="^YH.+\n[待发货|部分发货|已完成|已取消]+\n下单时间：\d{4,4}-\d{2,2}-\d{2,2} \d{2,2}:\d{2,2}:\d{2,2} \n共\d+件\n押货合计：￥\d+\.\d+$")
                for star in stars02:
                    logger.info(star.get_name(), desc="押货单")
                    t = star.get_name()
                    star.click() # 进入详情
                    poco("修改记录").wait(1).click() # 进入修改记录
                    assert poco("押货单修改记录").exists()
                    assert poco(f"押货单号：{t[:18]}").exists()
                    assert poco(re.search("下单时间：\d{4,4}-\d{2,2}-\d{2,2} \d{2,2}:\d{2,2}", t).group()).exists()
                    assert poco("复制").exists()
                    poco("复制").click()
                    poco("复制", touchable=True).exists()
                        
                    # 退出修改记录        
                    poco(name="android.view.View", touchable=True).click()
                    # 退出押货单详情
                    poco(name="android.view.View", touchable=True).click()    

            # 退出押货单管理,返回服务中心首页
            poco(name="android.view.View", touchable=True).click()

        step_01()
        


