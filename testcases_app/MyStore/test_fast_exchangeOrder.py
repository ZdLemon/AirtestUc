# coding:utf-8

__author__ = "ligeit"

import time
import allure
from airtest.core.api import *
from utils.logger import logger
import pytest
from setting import P1, P2, P3, M7035, UUIDS
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


@allure.feature("我的-我的服务中心")
@allure.story("我的-我的服务中心-快速申请-押货换货申请")
class TestClass:
    """
    我的-我的服务中心-快速申请-押货换货申请
    """
     
    @allure.severity(P1)            
    @allure.title("我的-我的服务中心-快速申请-押货换货申请：押货换货申请主路径检查")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_01(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False) 
        poco("快捷申请").swipe([0, -0.3304])
        poco("押货换货申请").click()

        assert_equal(poco("新建门店换货单", touchable=False).exists(), True, msg="新建门店换货单")
        assert_equal(poco("搜索产品名称编号", touchable=True).exists(), True, msg="搜索产品名称编号")
        assert_equal(poco("下一步", touchable=False).exists(), True, msg="下一步")

        poco("去新建").click()

        # 点击【+】-【去新建】
        poco(text="搜索产品名称或编号").click()
        poco(text="搜索产品名称或编号").set_text(M7035)
        poco("搜索").click()

        # 换货数量
        logger.info(poco(nameMatches="^.+\n.+ \| .?\n¥ \d+\.\d{2,2}$").get_name(), desc="换货产品")
        poco(nameMatches="^.+\n.+ \| .?\n¥ \d+\.\d{2,2}$").child("android.view.View").click() # 0-->1
        poco(nameMatches="^.+\n.+ \| .?\n¥ \d+\.\d{2,2}$").child("android.view.View")[1].click() # 1-->2

        # 返回新建门店换货单页面
        poco(name="android.view.View", touchable=True).click()

        assert_equal(poco("新建门店换货单", touchable=False).exists(), True, msg="新建门店换货单")
        assert_equal(poco("换货数量合计：").exists(), True, msg="换货数量合计：")
        assert_equal(poco("2", touchable=False).exists(), True, msg="2")
        assert_equal(poco("下一步", touchable=True).exists(), True, msg="下一步")

        # 新建押货换货单       
        poco(text="请输入批号").click()
        poco(text="请输入批号").set_text("123456")

        poco(text="请输入生产日期或有限期").click()
        poco(text="请输入生产日期或有限期").set_text("20220101")

        poco(text="请输入详细问题描述").click()
        poco(text="请输入详细问题描述").set_text("过潮，发霉了")
        # 收起键盘
        poco(text="20220101, 请输入生产日期或有限期").click()
        poco(longClickable=True).click([0.91, 0.5])

        # 查看非必填项
        poco("展开（还有4项）").click()
        poco("收起").click()

        poco("下一步").click()

        # 确认押货换货单
        poco(nameMatches=".+\n.+\n换货数量 2\n补充说明（已填3项）$").click([0.5,0.9])

        assert_equal(poco("换货补充说明", touchable=False).exists(), True, msg="换货补充说明")
        assert_equal(poco("批号\n123456", touchable=False).exists(), True, msg="批号\n123456")
        assert_equal(poco("生产日期\n20220101", touchable=False).exists(), True, msg="生产日期\n20220101")
        assert_equal(poco("详细问题描述\n过潮，发霉了", touchable=False).exists(), True, msg="详细问题描述\n过潮，发霉了")

        poco("android.widget.Button", touchable=True).click()

        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).exists(), True, msg="选择原因")
        poco("取消").click()

        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).exists(), True, msg="选择原因")
        poco("净化机/器及配件保修期内质量换货").swipe([-0.1676, -0.1265])
        poco("确定").click()

        poco(text="请说明你遇到的问题").click()
        poco(text="请说明你遇到的问题").set_text("快点发货，3天内必须到")

        # 上传换货凭证
        poco("最多3张").click()
        poco("从手机相册选择").click()
        # huawei,vivo
        if poco(text="允许").exists():
            poco(text="允许").click()
            poco("最多3张").click()
            poco("从手机相册选择").click()

        # huawei,vivo
        if poco(nameMatches="^图片1.+").exists():
            poco(nameMatches="^图片1.+").click()
            poco("确认 (1/3)").click()
        else:
            poco("返回").click()

        # 提交换货申请 
        poco("提交换货申请").click()

        assert_equal(poco("押货换货单提交成功", touchable=False).exists(), True, msg="押货换货单提交成功")
        assert_equal(poco("查看详情", touchable=True).exists(), True, msg="查看详情")
        assert_equal(poco("返回服务中心首页", touchable=True).exists(), True, msg="返回服务中心首页")

        poco("返回服务中心首页").click() 

    @allure.severity(P2)            
    @allure.title("我的-我的服务中心-快速申请-押货换货申请：通过搜索产品名称和编号提交申请检查")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_02(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False) 
        poco("快捷申请").swipe([0, -0.3304])
        poco("押货换货申请").click()

        assert_equal(poco("新建门店换货单", touchable=False).exists(), True, msg="新建门店换货单")
        assert_equal(poco("搜索产品名称编号", touchable=True).exists(), True, msg="搜索产品名称编号")
        assert_equal(poco("下一步", touchable=False).exists(), True, msg="下一步")

        poco("搜索产品名称编号").click()

        # 点击【+】-【去新建】
        poco(text="搜索产品名称或编号").click()
        poco(text="搜索产品名称或编号").set_text(M7035)
        poco("搜索").click()

        # 换货数量
        logger.info(poco(nameMatches="^.+\n.+ \| .?\n¥ \d+\.\d{2,2}$").get_name(), desc="换货产品")
        poco(nameMatches="^.+\n.+ \| .?\n¥ \d+\.\d{2,2}$").child("android.view.View").click() # 0-->1
        poco(nameMatches="^.+\n.+ \| .?\n¥ \d+\.\d{2,2}$").child("android.view.View")[1].click() # 1-->2

        # 返回新建门店换货单页面
        poco(name="android.view.View", touchable=True).click()

        assert_equal(poco("新建门店换货单", touchable=False).exists(), True, msg="新建门店换货单")
        assert_equal(poco("换货数量合计：").exists(), True, msg="换货数量合计：")
        assert_equal(poco("2", touchable=False).exists(), True, msg="2")
        assert_equal(poco("下一步", touchable=True).exists(), True, msg="下一步")

        # 新建押货换货单       
        poco(text="请输入批号").click()
        poco(text="请输入批号").set_text("123456")

        poco(text="请输入生产日期或有限期").click()
        poco(text="请输入生产日期或有限期").set_text("20220101")

        poco(text="请输入详细问题描述").click()
        poco(text="请输入详细问题描述").set_text("过潮，发霉了")
        # 收起键盘
        poco(text="20220101, 请输入生产日期或有限期").click()
        poco(longClickable=True).click([0.91, 0.5])

        # 查看非必填项
        poco("展开（还有4项）").click()
        poco("收起").click()

        poco("下一步").click()

        # 确认押货换货单
        poco(nameMatches=".+\n.+\n换货数量 2\n补充说明（已填3项）$").click([0.5,0.9])

        assert_equal(poco("换货补充说明", touchable=False).exists(), True, msg="换货补充说明")
        assert_equal(poco("批号\n123456", touchable=False).exists(), True, msg="批号\n123456")
        assert_equal(poco("生产日期\n20220101", touchable=False).exists(), True, msg="生产日期\n20220101")
        assert_equal(poco("详细问题描述\n过潮，发霉了", touchable=False).exists(), True, msg="详细问题描述\n过潮，发霉了")

        poco("android.widget.Button", touchable=True).click()

        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).exists(), True, msg="选择原因")
        poco("取消").click()

        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).exists(), True, msg="选择原因")
        poco("净化机/器及配件保修期内质量换货").swipe([-0.1676, -0.1265])
        poco("确定").click()

        poco(text="请说明你遇到的问题").click()
        poco(text="请说明你遇到的问题").set_text("快点发货，3天内必须到")

        # 上传换货凭证
        poco("最多3张").click()
        poco("从手机相册选择").click()
        # huawei,vivo
        if poco(text="允许").exists():
            poco(text="允许").click()
            poco("最多3张").click()
            poco("从手机相册选择").click()

        # huawei,vivo
        if poco(nameMatches="^图片1.+").exists():
            poco(nameMatches="^图片1.+").click()
            poco("确认 (1/3)").click()
        else:
            poco("返回").click()

        # 提交换货申请 
        poco("提交换货申请").click()

        assert_equal(poco("押货换货单提交成功", touchable=False).exists(), True, msg="押货换货单提交成功")
        assert_equal(poco("查看详情", touchable=True).exists(), True, msg="查看详情")
        assert_equal(poco("返回服务中心首页", touchable=True).exists(), True, msg="返回服务中心首页")

        poco("返回服务中心首页").click() 

    @allure.severity(P2)            
    @allure.title("我的-我的服务中心-快速申请-押货换货申请：押货换货申请后【查看详情】检查")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_03(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False) 
        poco("快捷申请").swipe([0, -0.3304])
        poco("押货换货申请").click()

        assert_equal(poco("新建门店换货单", touchable=False).exists(), True, msg="新建门店换货单")
        assert_equal(poco("搜索产品名称编号", touchable=True).exists(), True, msg="搜索产品名称编号")
        assert_equal(poco("下一步", touchable=False).exists(), True, msg="下一步")

        poco("去新建").click()

        # 点击【+】-【去新建】
        poco(text="搜索产品名称或编号").click()
        poco(text="搜索产品名称或编号").set_text(M7035)
        poco("搜索").click()

        # 换货数量
        logger.info(poco(nameMatches="^.+\n.+ \| .?\n¥ \d+\.\d{2,2}$").get_name(), desc="换货产品")
        poco(nameMatches="^.+\n.+ \| .?\n¥ \d+\.\d{2,2}$").child("android.view.View").click() # 0-->1
        poco(nameMatches="^.+\n.+ \| .?\n¥ \d+\.\d{2,2}$").child("android.view.View")[1].click() # 1-->2

        # 返回新建门店换货单页面
        poco(name="android.view.View", touchable=True).click()

        assert_equal(poco("新建门店换货单", touchable=False).exists(), True, msg="新建门店换货单")
        assert_equal(poco("换货数量合计：").exists(), True, msg="换货数量合计：")
        assert_equal(poco("2", touchable=False).exists(), True, msg="2")
        assert_equal(poco("下一步", touchable=True).exists(), True, msg="下一步")

        # 新建押货换货单       
        poco(text="请输入批号").click()
        poco(text="请输入批号").set_text("123456")

        poco(text="请输入生产日期或有限期").click()
        poco(text="请输入生产日期或有限期").set_text("20220101")

        poco(text="请输入详细问题描述").click()
        poco(text="请输入详细问题描述").set_text("过潮，发霉了")
        # 收起键盘
        poco(text="20220101, 请输入生产日期或有限期").click()
        poco(longClickable=True).click([0.91, 0.5])

        # 查看非必填项
        poco("展开（还有4项）").click()
        poco("收起").click()

        poco("下一步").click()

        # 确认押货换货单
        poco(nameMatches=".+\n.+\n换货数量 2\n补充说明（已填3项）$").click([0.5,0.9])

        assert_equal(poco("换货补充说明", touchable=False).exists(), True, msg="换货补充说明")
        assert_equal(poco("批号\n123456", touchable=False).exists(), True, msg="批号\n123456")
        assert_equal(poco("生产日期\n20220101", touchable=False).exists(), True, msg="生产日期\n20220101")
        assert_equal(poco("详细问题描述\n过潮，发霉了", touchable=False).exists(), True, msg="详细问题描述\n过潮，发霉了")

        poco("android.widget.Button", touchable=True).click()

        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).exists(), True, msg="选择原因")
        poco("取消").click()

        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).exists(), True, msg="选择原因")
        poco("净化机/器及配件保修期内质量换货").swipe([-0.1676, -0.1265])
        poco("确定").click()

        poco(text="请说明你遇到的问题").click()
        poco(text="请说明你遇到的问题").set_text("快点发货，3天内必须到")

        # 上传换货凭证
        poco("最多3张").click()
        poco("从手机相册选择").click()
        # huawei,vivo
        if poco(text="允许").exists():
            poco(text="允许").click()
            poco("最多3张").click()
            poco("从手机相册选择").click()

        # huawei,vivo
        if poco(nameMatches="^图片1.+").exists():
            poco(nameMatches="^图片1.+").click()
            poco("确认 (1/3)").click()
        else:
            poco("返回").click()

        # 提交换货申请 
        poco("提交换货申请").click()

        assert_equal(poco("押货换货单提交成功", touchable=False).exists(), True, msg="押货换货单提交成功")
        assert_equal(poco("查看详情", touchable=True).exists(), True, msg="查看详情")
        assert_equal(poco("返回服务中心首页", touchable=True).exists(), True, msg="返回服务中心首页")

        # 查看详情
        poco("查看详情").click()
        assert_equal(poco("门店换货单详情", touchable=False).exists(), True, msg="门店换货单详情")
        assert_equal(poco("待审核", touchable=False).exists(), True, msg="待审核")
        assert_equal(poco("等待公司审核", touchable=False).exists(), True, msg="等待公司审核")
        assert_equal(poco(nameMatches=".+\n.+\n换货数量 2\n补充说明（已填3项）$").exists(), True, msg="换货数量 2")
        assert_equal(poco("取消换货", touchable=True).exists(), True, msg="取消换货")            
        
        # 返回服务中心首页
        poco(name="android.view.View", touchable=True).click() 

    @allure.severity(P2)            
    @allure.title("我的-我的服务中心-快速申请-押货换货申请：押货换货申请后【返回列表】检查")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_04(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False) 
        poco("快捷申请").swipe([0, -0.3304])
        poco("押货换货申请").click()

        assert_equal(poco("新建门店换货单", touchable=False).exists(), True, msg="新建门店换货单")
        assert_equal(poco("搜索产品名称编号", touchable=True).exists(), True, msg="搜索产品名称编号")
        assert_equal(poco("下一步", touchable=False).exists(), True, msg="下一步")

        poco("去新建").click()

        # 点击【+】-【去新建】
        poco(text="搜索产品名称或编号").click()
        poco(text="搜索产品名称或编号").set_text(M7035)
        poco("搜索").click()

        # 换货数量
        logger.info(poco(nameMatches="^.+\n.+ \| .?\n¥ \d+\.\d{2,2}$").get_name(), desc="换货产品")
        poco(nameMatches="^.+\n.+ \| .?\n¥ \d+\.\d{2,2}$").child("android.view.View").click() # 0-->1
        poco(nameMatches="^.+\n.+ \| .?\n¥ \d+\.\d{2,2}$").child("android.view.View")[1].click() # 1-->2

        # 返回新建门店换货单页面
        poco(name="android.view.View", touchable=True).click()

        assert_equal(poco("新建门店换货单", touchable=False).exists(), True, msg="新建门店换货单")
        assert_equal(poco("换货数量合计：").exists(), True, msg="换货数量合计：")
        assert_equal(poco("2", touchable=False).exists(), True, msg="2")
        assert_equal(poco("下一步", touchable=True).exists(), True, msg="下一步")

        # 新建押货换货单       
        poco(text="请输入批号").click()
        poco(text="请输入批号").set_text("123456")

        poco(text="请输入生产日期或有限期").click()
        poco(text="请输入生产日期或有限期").set_text("20220101")

        poco(text="请输入详细问题描述").click()
        poco(text="请输入详细问题描述").set_text("过潮，发霉了")
        # 收起键盘
        poco(text="20220101, 请输入生产日期或有限期").click()
        poco(longClickable=True).click([0.91, 0.5])

        # 查看非必填项
        poco("展开（还有4项）").click()
        poco("收起").click()

        poco("下一步").click()

        # 确认押货换货单
        poco(nameMatches=".+\n.+\n换货数量 2\n补充说明（已填3项）$").click([0.5,0.9])

        assert_equal(poco("换货补充说明", touchable=False).exists(), True, msg="换货补充说明")
        assert_equal(poco("批号\n123456", touchable=False).exists(), True, msg="批号\n123456")
        assert_equal(poco("生产日期\n20220101", touchable=False).exists(), True, msg="生产日期\n20220101")
        assert_equal(poco("详细问题描述\n过潮，发霉了", touchable=False).exists(), True, msg="详细问题描述\n过潮，发霉了")

        poco("android.widget.Button", touchable=True).click()

        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).exists(), True, msg="选择原因")
        poco("取消").click()

        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).exists(), True, msg="选择原因")
        poco("净化机/器及配件保修期内质量换货").swipe([-0.1676, -0.1265])
        poco("确定").click()

        poco(text="请说明你遇到的问题").click()
        poco(text="请说明你遇到的问题").set_text("快点发货，3天内必须到")

        # 上传换货凭证
        poco("最多3张").click()
        poco("从手机相册选择").click()
        # huawei,vivo
        if poco(text="允许").exists():
            poco(text="允许").click()
            poco("最多3张").click()
            poco("从手机相册选择").click()

        # huawei,vivo
        if poco(nameMatches="^图片1.+").exists():
            poco(nameMatches="^图片1.+").click()
            poco("确认 (1/3)").click()
        else:
            poco("返回").click()

        # 提交换货申请 
        poco("提交换货申请").click()

        assert_equal(poco("押货换货单提交成功", touchable=False).exists(), True, msg="押货换货单提交成功")
        assert_equal(poco("查看详情", touchable=True).exists(), True, msg="查看详情")
        assert_equal(poco("返回列表", touchable=True).exists(), True, msg="返回列表")
        assert_equal(poco("返回服务中心首页", touchable=True).exists(), True, msg="返回服务中心首页")

        # 返回列表
        poco("返回列表").click()
        assert_equal(poco("全部\n第 1 个标签，共 8 个").exists(), True, msg="全部\n第 1 个标签，共 8 个")
        assert_equal(poco("待审核\n第 2 个标签，共 8 个").exists(), True, msg="待审核\n第 2 个标签，共 8 个")            
        assert_equal(poco("待退回\n第 3 个标签，共 8 个").exists(), True, msg="待退回\n第 3 个标签，共 8 个")            
        assert_equal(poco("待验货\n第 4 个标签，共 8 个").exists(), True, msg="待验货\n第 4 个标签，共 8 个")
        assert_equal(poco("待发货\n第 5 个标签，共 8 个").exists(), True, msg="待发货\n第 5 个标签，共 8 个")

        # 返回服务中心首页
        poco(name="android.view.View", touchable=True).click()

    @allure.severity(P2)            
    @allure.title("我的-我的服务中心-快速申请-押货换货申请：押货换货申请【查看详情】后【取消换货】检查")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_05(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False) 
        poco("快捷申请").swipe([0, -0.3304])
        poco("押货换货申请").click()

        assert_equal(poco("新建门店换货单", touchable=False).exists(), True, msg="新建门店换货单")
        assert_equal(poco("搜索产品名称编号", touchable=True).exists(), True, msg="搜索产品名称编号")
        assert_equal(poco("下一步", touchable=False).exists(), True, msg="下一步")

        poco("去新建").click()

        # 点击【+】-【去新建】
        poco(text="搜索产品名称或编号").click()
        poco(text="搜索产品名称或编号").set_text(M7035)
        poco("搜索").click()

        # 换货数量
        logger.info(poco(nameMatches="^.+\n.+ \| .?\n¥ \d+\.\d{2,2}$").get_name(), desc="换货产品")
        poco(nameMatches="^.+\n.+ \| .?\n¥ \d+\.\d{2,2}$").child("android.view.View").click() # 0-->1
        poco(nameMatches="^.+\n.+ \| .?\n¥ \d+\.\d{2,2}$").child("android.view.View")[1].click() # 1-->2

        # 返回新建门店换货单页面
        poco(name="android.view.View", touchable=True).click()

        assert_equal(poco("新建门店换货单", touchable=False).exists(), True, msg="新建门店换货单")
        assert_equal(poco("换货数量合计：").exists(), True, msg="换货数量合计：")
        assert_equal(poco("2", touchable=False).exists(), True, msg="2")
        assert_equal(poco("下一步", touchable=True).exists(), True, msg="下一步")

        # 新建押货换货单       
        poco(text="请输入批号").click()
        poco(text="请输入批号").set_text("123456")

        poco(text="请输入生产日期或有限期").click()
        poco(text="请输入生产日期或有限期").set_text("20220101")

        poco(text="请输入详细问题描述").click()
        poco(text="请输入详细问题描述").set_text("过潮，发霉了")
        # 收起键盘
        poco(text="20220101, 请输入生产日期或有限期").click()
        poco(longClickable=True).click([0.91, 0.5])

        # 查看非必填项
        poco("展开（还有4项）").click()
        poco("收起").click()

        poco("下一步").click()

        # 确认押货换货单
        poco(nameMatches=".+\n.+\n换货数量 2\n补充说明（已填3项）$").click([0.5,0.9])

        assert_equal(poco("换货补充说明", touchable=False).exists(), True, msg="换货补充说明")
        assert_equal(poco("批号\n123456", touchable=False).exists(), True, msg="批号\n123456")
        assert_equal(poco("生产日期\n20220101", touchable=False).exists(), True, msg="生产日期\n20220101")
        assert_equal(poco("详细问题描述\n过潮，发霉了", touchable=False).exists(), True, msg="详细问题描述\n过潮，发霉了")

        poco("android.widget.Button", touchable=True).click()

        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).exists(), True, msg="选择原因")
        poco("取消").click()

        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).exists(), True, msg="选择原因")
        poco("净化机/器及配件保修期内质量换货").swipe([-0.1676, -0.1265])
        poco("确定").click()

        poco(text="请说明你遇到的问题").click()
        poco(text="请说明你遇到的问题").set_text("快点发货，3天内必须到")

        # 上传换货凭证
        poco("最多3张").click()
        poco("从手机相册选择").click()
        # huawei,vivo
        if poco(text="允许").exists():
            poco(text="允许").click()
            poco("最多3张").click()
            poco("从手机相册选择").click()

        # huawei,vivo
        if poco(nameMatches="^图片1.+").exists():
            poco(nameMatches="^图片1.+").click()
            poco("确认 (1/3)").click()
        else:
            poco("返回").click()

        # 提交换货申请 
        poco("提交换货申请").click()

        assert_equal(poco("押货换货单提交成功", touchable=False).exists(), True, msg="押货换货单提交成功")
        assert_equal(poco("查看详情", touchable=True).exists(), True, msg="查看详情")
        assert_equal(poco("返回服务中心首页", touchable=True).exists(), True, msg="返回服务中心首页")

        # 查看详情
        poco("查看详情").click()
        assert_equal(poco("门店换货单详情", touchable=False).exists(), True, msg="门店换货单详情")
        assert_equal(poco("待审核", touchable=False).exists(), True, msg="待审核")
        assert_equal(poco("等待公司审核", touchable=False).exists(), True, msg="等待公司审核")
        assert_equal(poco(nameMatches=".+\n.+\n换货数量 2\n补充说明（已填3项）$").exists(), True, msg="换货数量 2")
        assert_equal(poco("取消换货", touchable=True).exists(), True, msg="取消换货") 

        # 取消换货
        poco("取消换货").click() 
        assert_equal(poco("提示", touchable=False).exists(), True, msg="提示")
        assert_equal(poco("确定取消", touchable=False).exists(), True, msg="确定取消")
        poco("取消").click()

        poco("取消换货").click() 
        assert_equal(poco("提示", touchable=False).exists(), True, msg="提示")
        assert_equal(poco("确定取消", touchable=False).exists(), True, msg="确定取消")
        poco("确定").click()

        assert_equal(poco("门店换货单详情", touchable=False).exists(), True, msg="门店换货单详情")
        assert_equal(poco("已取消", touchable=False).exists(), True, msg="已取消")
        assert_equal(poco(nameMatches="^取消时间：.+", touchable=False).exists(), True, msg="取消时间")
        assert_equal(poco(nameMatches=".+\n.+\n换货数量 2\n补充说明（已填3项）$").exists(), True, msg="换货数量 2")

        poco("复制").click()
        poco("广州仓\n复制").click([0.9, 0.5])

        # 返回服务中心首页
        poco(name="android.view.View", touchable=True).click()