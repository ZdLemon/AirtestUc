# coding:utf-8

__author__ = "ligeit"

from airtest.core.api import *

import time
import allure
from utils.logger import logger
import pytest
from setting import P1, P2, P3, M7035, UUIDS
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


@allure.feature("我的-我的服务中心")
@allure.story("我的-我的服务中心-快速申请-押货退货申请")
class TestClass:
    """
    我的-我的服务中心-快速申请-押货退货申请
    """
  
    @allure.severity(P1)            
    @allure.title("我的-我的服务中心-快速申请-押货退货申请：押货退货申请主路径检查")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_01(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False) 
        poco("快捷申请").swipe([0, -0.3304])
        poco("押货退货申请").click()

        assert_equal(poco("新建押货退货单", touchable=False).exists(), True, msg="新建押货退货单")
        assert_equal(poco("退货金额合计:￥0.00").exists(), True, msg="退货金额合计:￥0.00")
        assert_equal(poco("结算", touchable=False).exists(), True, msg="结算")

        poco("去新建").click()

        count = 0
        for star in poco(nameMatches="^.+\n.+\n¥\d+\.\d{2,2}\n当前库存：\d+$"):
            logger.info(star.get_name(), desc="押货退货商品")
            star.child("android.view.View").click() # 退货数量 0-->1
            if star.child("android.view.View")[1].exists():
                star.child("android.view.View")[1].click() # 退货数量 1-->2
            count += 1
            if count >= 2:
                break

        # 退到结算页面
        poco(name="android.view.View", touchable=True).wait(1).click()

        # 备注
        poco(text="输入批次号等信息").click()
        poco(text="输入批次号等信息").set_text("123456")
        poco("结算").click()

        # 选择退货原因
        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).wait(1).exists(), True, msg="选择原因")
        poco("结点退货").swipe([0, -0.08]) # 其他原因退货
        poco("取消").click()

        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).wait(1).exists(), True, msg="选择原因")
        poco("结点退货").swipe([0, -0.08]) # 其他原因退货
        poco("确定").click()

        # 备注说明
        poco(text="请说明你遇到的问题").click()
        poco(text="请说明你遇到的问题").set_text("发霉进水了")

        poco("提交退货申请").click()

        assert_equal(poco("押货退货单提交成功", touchable=False).exists(), True, msg="押货退货单提交成功")
        assert_equal(poco("查看详情", touchable=True).exists(), True, msg="查看详情")
        assert_equal(poco("再下一单", touchable=True).exists(), True, msg="再下一单")
        assert_equal(poco("返回服务中心首页", touchable=True).exists(), True, msg="返回服务中心首页")

        poco("返回服务中心首页").click()

    @allure.severity(P1)            
    @allure.title("我的-我的服务中心-快速申请-押货退货申请：直接搜索产品新建压货退货申请检查")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_02(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False) 
        poco("快捷申请").swipe([0, -0.3304])
        poco("押货退货申请").click()

        assert_equal(poco("新建押货退货单", touchable=False).wait(1).exists(), True, msg="新建押货退货单")
        assert_equal(poco("退货金额合计:￥0.00").exists(), True, msg="退货金额合计:￥0.00")
        assert_equal(poco("结算", touchable=False).exists(), True, msg="结算")

        poco("搜索产品名称和编号").click()

        count = 0
        for star in poco(nameMatches="^.+\n.+\n¥\d+\.\d{2,2}\n当前库存：\d+$"):
            logger.info(star.get_name(), desc="押货退货商品")
            star.child("android.view.View").click() # 退货数量 0-->1
            if star.child("android.view.View")[1].exists():
                star.child("android.view.View")[1].click() # 退货数量 1-->2
            count += 1
            if count >= 2:
                break

        # 退到结算页面
        poco(name="android.view.View", touchable=True).wait(1).click()

        # 备注
        poco(text="输入批次号等信息").click()
        poco(text="输入批次号等信息").set_text("123456")
        poco("结算").click()

        # 选择退货原因
        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).wait(1).exists(), True, msg="选择原因")
        poco("结点退货").swipe([0, -0.08]) # 其他原因退货
        poco("取消").click()

        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).wait(1).exists(), True, msg="选择原因")
        poco("结点退货").swipe([0, -0.08]) # 其他原因退货
        poco("确定").click()

        # 备注说明
        poco(text="请说明你遇到的问题").click()
        poco(text="请说明你遇到的问题").set_text("发霉进水了")

        poco("提交退货申请").click()

        assert_equal(poco("押货退货单提交成功", touchable=False).exists(), True, msg="押货退货单提交成功")
        assert_equal(poco("查看详情", touchable=True).exists(), True, msg="查看详情")
        assert_equal(poco("再下一单", touchable=True).exists(), True, msg="再下一单")
        assert_equal(poco("返回服务中心首页", touchable=True).exists(), True, msg="返回服务中心首页")

        poco("返回服务中心首页").click()

    @allure.severity(P3)            
    @allure.title("我的-我的服务中心-快速申请-押货退货申请：押货退货提交后【再下一单】检查")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_03(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False) 
        poco("快捷申请").swipe([0, -0.3304])
        poco("押货退货申请").click()

        assert_equal(poco("新建押货退货单", touchable=False).exists(), True, msg="新建押货退货单")
        assert_equal(poco("退货金额合计:￥0.00").exists(), True, msg="退货金额合计:￥0.00")
        assert_equal(poco("结算", touchable=False).exists(), True, msg="结算")

        poco("去新建").click()

        count = 0
        for star in poco(nameMatches="^.+\n.+\n¥\d+\.\d{2,2}\n当前库存：\d+$"):
            logger.info(star.get_name(), desc="押货退货商品")
            star.child("android.view.View").click() # 退货数量 0-->1
            if star.child("android.view.View")[1].exists():
                star.child("android.view.View")[1].click() # 退货数量 1-->2
            count += 1
            if count >= 2:
                break

        # 退到结算页面
        poco(name="android.view.View", touchable=True).wait(1).click()

        # 备注
        poco(text="输入批次号等信息").click()
        poco(text="输入批次号等信息").set_text("123456")
        poco("结算").click()

        # 选择退货原因
        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).wait(1).exists(), True, msg="选择原因")
        poco("结点退货").swipe([0, -0.08]) # 其他原因退货
        poco("取消").click()

        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).wait(1).exists(), True, msg="选择原因")
        poco("结点退货").swipe([0, -0.08]) # 其他原因退货
        poco("确定").click()

        # 备注说明
        poco(text="请说明你遇到的问题").click()
        poco(text="请说明你遇到的问题").set_text("发霉进水了")

        poco("提交退货申请").click()

        assert_equal(poco("押货退货单提交成功", touchable=False).exists(), True, msg="押货退货单提交成功")
        assert_equal(poco("查看详情", touchable=True).exists(), True, msg="查看详情")
        assert_equal(poco("再下一单", touchable=True).exists(), True, msg="再下一单")
        assert_equal(poco("返回服务中心首页", touchable=True).exists(), True, msg="返回服务中心首页")


        poco("再下一单").click()
        assert_equal(poco("新建押货退货单", touchable=False).exists(), True, msg="新建押货退货单")
        assert_equal(poco("退货金额合计:￥0.00").exists(), True, msg="退货金额合计:￥0.00")
        assert_equal(poco("结算", touchable=False).exists(), True, msg="结算")
        assert_equal(poco("去新建", touchable=True).exists(), True, msg="去新建")

        # 退到服务中心首页
        poco(name="android.view.View", touchable=True).click()
              
    @allure.severity(P3)            
    @allure.title("我的-我的服务中心-快速申请-押货退货申请：押货退货提交后【查看详情】检查")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_04(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False) 
        poco("快捷申请").swipe([0, -0.3304])
        poco("押货退货申请").click()

        assert_equal(poco("新建押货退货单", touchable=False).exists(), True, msg="新建押货退货单")
        assert_equal(poco("退货金额合计:￥0.00").exists(), True, msg="退货金额合计:￥0.00")
        assert_equal(poco("结算", touchable=False).exists(), True, msg="结算")

        poco("去新建").click()

        count = 0
        for star in poco(nameMatches="^.+\n.+\n¥\d+\.\d{2,2}\n当前库存：\d+$"):
            logger.info(star.get_name(), desc="押货退货商品")
            star.child("android.view.View").click() # 退货数量 0-->1
            if star.child("android.view.View")[1].exists():
                star.child("android.view.View")[1].click() # 退货数量 1-->2
            count += 1
            if count >= 2:
                break

        # 退到结算页面
        poco(name="android.view.View", touchable=True).wait(1).click()

        # 备注
        poco(text="输入批次号等信息").click()
        poco(text="输入批次号等信息").set_text("123456")
        poco("结算").click()

        # 选择退货原因
        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).wait(1).exists(), True, msg="选择原因")
        poco("结点退货").swipe([0, -0.08]) # 其他原因退货
        poco("取消").click()

        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).wait(1).exists(), True, msg="选择原因")
        poco("结点退货").swipe([0, -0.08]) # 其他原因退货
        poco("确定").click()

        # 备注说明
        poco(text="请说明你遇到的问题").click()
        poco(text="请说明你遇到的问题").set_text("发霉进水了")

        poco("提交退货申请").click()

        assert_equal(poco("押货退货单提交成功", touchable=False).exists(), True, msg="押货退货单提交成功")
        assert_equal(poco("查看详情", touchable=True).exists(), True, msg="查看详情")
        assert_equal(poco("再下一单", touchable=True).exists(), True, msg="再下一单")
        assert_equal(poco("返回服务中心首页", touchable=True).exists(), True, msg="返回服务中心首页")

        poco("查看详情").click()
        assert_equal(poco("押货退货单详情", touchable=False).exists(), True, msg="押货退货单详情")
        assert_equal(poco("待审核\n待分公司审核", touchable=False).exists(), True, msg="待审核\n待分公司审核")
        assert_equal(poco("取消申请", touchable=True).exists(), True, msg="取消申请")

        # 退到服务中心首页
        poco(name="android.view.View", touchable=True).click()

    @allure.severity(P3)            
    @allure.title("我的-我的服务中心-快速申请-押货退货申请：押货退货提交后【查看详情】并【取消申请】检查")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_05(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)             
        poco("快捷申请").swipe([0, -0.3304])
        poco("押货退货申请").click()

        assert_equal(poco("新建押货退货单", touchable=False).exists(), True, msg="新建押货退货单")
        assert_equal(poco("退货金额合计:￥0.00").exists(), True, msg="退货金额合计:￥0.00")
        assert_equal(poco("结算", touchable=False).exists(), True, msg="结算")

        poco("去新建").click()

        count = 0
        for star in poco(nameMatches="^.+\n.+\n¥\d+\.\d{2,2}\n当前库存：\d+$"):
            logger.info(star.get_name(), desc="押货退货商品")
            star.child("android.view.View").click() # 退货数量 0-->1
            if star.child("android.view.View")[1].exists():
                star.child("android.view.View")[1].click() # 退货数量 1-->2
            count += 1
            if count >= 2:
                break

        # 退到结算页面
        poco(name="android.view.View", touchable=True).wait(1).click()

        # 备注
        poco(text="输入批次号等信息").click()
        poco(text="输入批次号等信息").set_text("123456")
        poco("结算").click()

        # 选择退货原因
        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).wait(1).exists(), True, msg="选择原因")
        poco("结点退货").swipe([0, -0.08]) # 其他原因退货
        poco("取消").click()

        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).wait(1).exists(), True, msg="选择原因")
        poco("结点退货").swipe([0, -0.08]) # 其他原因退货
        poco("确定").click()

        # 备注说明
        poco(text="请说明你遇到的问题").click()
        poco(text="请说明你遇到的问题").set_text("发霉进水了")

        poco("提交退货申请").click()

        assert_equal(poco("押货退货单提交成功", touchable=False).exists(), True, msg="押货退货单提交成功")
        assert_equal(poco("查看详情", touchable=True).exists(), True, msg="查看详情")
        assert_equal(poco("再下一单", touchable=True).exists(), True, msg="再下一单")
        assert_equal(poco("返回服务中心首页", touchable=True).exists(), True, msg="返回服务中心首页")

        poco("查看详情").click()
        assert_equal(poco("押货退货单详情", touchable=False).exists(), True, msg="押货退货单详情")
        assert_equal(poco("待审核\n待分公司审核", touchable=False).exists(), True, msg="待审核\n待分公司审核")
        assert_equal(poco("取消申请", touchable=True).exists(), True, msg="取消申请")

        poco("取消申请").click()
        assert_equal(poco("提示", touchable=False).exists(), True, msg="提示")
        assert_equal(poco("确定取消？", touchable=False).exists(), True, msg="确定取消？")
        poco("取消").click()

        poco("取消申请").click()
        assert_equal(poco("提示", touchable=False).exists(), True, msg="提示")
        assert_equal(poco("确定取消？", touchable=False).exists(), True, msg="确定取消？")
        poco("确认").click()

        assert_equal(poco(nameMatches="^已取消\n取消时间：\d+-\d+-\d+ \d+:\d+", touchable=False).exists(), True, msg="已取消\n取消时间")

        # 退到服务中心首页
        poco(name="android.view.View", touchable=True).click()

    @allure.severity(P3)            
    @allure.title("我的-我的服务中心-快速申请-押货退货申请：遍历退货原因及取消退货检查")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_06(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)             
        poco("快捷申请").swipe([0, -0.3304])
        poco("押货退货申请").click()

        assert_equal(poco("新建押货退货单", touchable=False).exists(), True, msg="新建押货退货单")
        assert_equal(poco("退货金额合计:￥0.00").exists(), True, msg="退货金额合计:￥0.00")
        assert_equal(poco("结算", touchable=False).exists(), True, msg="结算")

        poco("去新建").click()

        count = 0
        for star in poco(nameMatches="^.+\n.+\n¥\d+\.\d{2,2}\n当前库存：\d+$"):
            logger.info(star.get_name(), desc="押货退货商品")
            star.child("android.view.View").click() # 退货数量 0-->1
            if star.child("android.view.View")[1].exists():
                star.child("android.view.View")[1].click() # 退货数量 1-->2
            count += 1
            if count >= 2:
                break

        # 退到结算页面
        poco(name="android.view.View", touchable=True).wait(1).click()

        # 备注
        poco(text="输入批次号等信息").click()
        poco(text="输入批次号等信息").set_text("123456")

        poco("结算").click()

        # 选择退货原因
        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).exists(), True, msg="选择原因")
        poco("取消").click()

        poco("原因").click()
        poco("确定").click()

        poco("原因").click()
        poco("结点退货").swipe([-0.0233, -0.0828])
        poco("确定").click()

        poco("原因").click()
        poco("结点退货").swipe([-0.013, -0.1505])
        poco("确定").click()

        # 退出押货退货
        poco(name="android.view.View", touchable=True).click()
        poco(name="android.view.View", touchable=True)[0].click()

        assert_equal(poco("提示", touchable=False).get_name(), "提示", msg="提示")
        assert_equal(poco("确定取消押货退货单？", touchable=False).get_name(), "确定取消押货退货单？", msg="确定取消押货退货单？")
        poco("取消").click()

        poco(name="android.view.View", touchable=True)[0].click()
        assert_equal(poco("提示", touchable=False).get_name(), "提示", msg="提示")
        assert_equal(poco("确定取消押货退货单？", touchable=False).get_name(), "确定取消押货退货单？", msg="确定取消押货退货单？")
        poco("确认").click()
