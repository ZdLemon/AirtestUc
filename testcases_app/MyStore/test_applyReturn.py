# coding:utf-8

__author__ = "ligeit"

from airtest.core.api import *
import allure
import pytest
from setting import P1, P2, P3, M7035, UUIDS
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from utils.logger import logger


@allure.feature("我的-我的服务中心")
@allure.story("我的-我的服务中心-押货退货")
class TestClass:
    """
    我的-我的服务中心-押货退货
    """
  
    @allure.severity(P1)            
    @allure.title("我的-我的服务中心-押货退货：押货退货主路径检查")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_01(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)   
        poco("押货退货").click()
        # 去新建
        poco(name="android.view.View", touchable=True)[1].wait(1).click()

        assert_equal(poco("新建押货退货单", touchable=False).get_name(), "新建押货退货单", msg="新建押货退货单")
        assert_equal(poco("去新建", touchable=True).get_name(), "去新建", msg="去新建")
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

        poco("结算").click()
        # 选择退货原因
        poco("原因").click()
        poco("选择原因").wait(1)
        poco("结点退货").swipe([0, -0.08]) # 其他原因退货
        poco("确定").click()

        poco("提交退货申请").click()

        assert_equal(poco("押货退货单提交成功", touchable=False).get_name(), "押货退货单提交成功", msg="押货退货单提交成功")
        assert_equal(poco("查看详情", touchable=True).get_name(), "查看详情", msg="查看详情")
        assert_equal(poco("再下一单", touchable=True).get_name(), "再下一单", msg="再下一单")
        assert_equal(poco("返回服务中心首页", touchable=True).get_name(), "返回服务中心首页", msg="返回服务中心首页")

        poco("返回服务中心首页").click()
       
    @allure.severity(P2)            
    @allure.title("我的-我的服务中心-押货退货：押货退货【查看详情】检查")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_02(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)   
        poco("押货退货").click()
        count = 0
        # 押货单个产品
        while poco(nameMatches="^退货单号:TYH.+\n退货\n.+\n产品编号：.+\n押货价：¥\d+\.\d+\n退货数量 \d+\n退货合计：¥.+\.\d+\n[已完成|待审核|待退回|待验货|已取消]{3,3}\n.+$").exists() and count<1:
            for star in poco(nameMatches="^退货单号:TYH.+\n退货\n.+\n产品编号：.+\n押货价：¥\d+\.\d+\n退货数量 \d+\n退货合计：¥.+\.\d+\n[已完成|待审核|待退回|待验货|已取消]{3,3}\n.+$"):
                logger.info(star.get_name(), desc="押货退货单")
                if count % 2 == 0:
                    star.click()
                else:
                    star.child("查看详情").click()
                
                assert_equal(poco("押货退货单详情", touchable=False).get_name(), "押货退货单详情", msg="押货退货单详情")
                if "已完成" in star.get_name():
                    assert poco(nameMatches="^已完成\n完成时间：\d+-\d{2,2}-\d{2,2} \d{2,2}:\d{2,2}$").exists()

                # 退出详情页面
                poco(name="android.view.View", touchable=True).wait(1).click()
                count += 1

        count = 0
        # 押货多个产品
        while poco(nameMatches="^退货单号:TYH.+\n退货\n共\d+件\n退货合计：¥\d+\.\d{2,2}\n[已完成|待审核|待退回|待验货|已取消]{3,3}\n.+$").exists() and count<1:
            for star in poco(nameMatches="^退货单号:TYH.+\n退货\n共\d+件\n退货合计：¥\d+\.\d{2,2}\n[已完成|待审核|待退回|待验货|已取消]{3,3}\n.+$"):
                logger.info(star.get_name(), desc="押货退货单")
                if count % 2 == 0:
                    star.click()
                else:
                    star.child("查看详情").click()

                assert_equal(poco("押货退货单详情", touchable=False).get_name(), "押货退货单详情", msg="押货退货单详情")
                if "已完成" in star.get_name():
                    assert poco(nameMatches="^已完成\n完成时间：\d+-\d{2,2}-\d{2,2} \d{2,2}:\d{2,2}$").exists()

                # 退出详情页面
                poco(name="android.view.View", touchable=True).wait(1).click()
                count += 1
        # 返回我的服务中心
        poco(name="android.view.View", touchable=True).wait(1).click()
        
    @allure.severity(P2)            
    @allure.title("我的-我的服务中心-押货退货：待审核压货退货单【取消申请】检查")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_03(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)   
        poco("押货退货").click()
        poco("待审核\n第 2 个标签，共 6 个", selected=False).click()

        # 押货单个产品
        if poco(nameMatches="^退货单号:TYH.+\n退货\n.+\n产品编号：.+\n押货价：¥\d+\.\d+\n退货数量 \d+\n退货合计：¥.+\.\d+\n[已完成|待审核|待退回|待验货|已取消]{3,3}\n.+$").exists():
            for star in poco(nameMatches="^退货单号:TYH.+\n退货\n.+\n产品编号：.+\n押货价：¥\d+\.\d+\n退货数量 \d+\n退货合计：¥.+\.\d+\n[已完成|待审核|待退回|待验货|已取消]{3,3}\n.+$"):
                logger.info(star.get_name(), desc="押货退货单")
                star.child("取消申请").click()
                assert_equal(poco("提示", touchable=False).get_name(), "提示", msg="提示")
                assert_equal(poco("确定取消？", touchable=False).get_name(), "确定取消？", msg="确定取消？")
                poco("取消").click()

                star.child("取消申请").click()
                assert_equal(poco("提示", touchable=False).get_name(), "提示", msg="提示")
                assert_equal(poco("确定取消？", touchable=False).get_name(), "确定取消？", msg="确定取消？")
                poco("确认").click()

                break
        # 押货多个产品
        if poco(nameMatches="^退货单号:TYH.+\n退货\n共\d+件\n退货合计：¥\d+\.\d{2,2}\n[已完成|待审核|待退回|待验货|已取消]{3,3}\n.+$").exists():
            for star in poco(nameMatches="^退货单号:TYH.+\n退货\n共\d+件\n退货合计：¥\d+\.\d{2,2}\n[已完成|待审核|待退回|待验货|已取消]{3,3}\n.+$"):
                logger.info(star.get_name(), desc="押货退货单")
                star.child("取消申请").click()
                assert_equal(poco("提示", touchable=False).get_name(), "提示", msg="提示")
                assert_equal(poco("确定取消？", touchable=False).get_name(), "确定取消？", msg="确定取消？")
                poco("取消").click()

                star.child("取消申请").click()
                assert_equal(poco("提示", touchable=False).get_name(), "提示", msg="提示")
                assert_equal(poco("确定取消？", touchable=False).get_name(), "确定取消？", msg="确定取消？")
                poco("确认").click()

                break

        # 返回我的服务中心
        poco(name="android.view.View", touchable=True).click()
                
    @allure.severity(P3)            
    @allure.title("我的-我的服务中心-押货退货：押货退货提交后【再下一单】检查")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_04(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)   
        poco("押货退货").click()
        # 去新建
        poco(name="android.view.View", touchable=True)[1].wait(1).click()

        assert_equal(poco("新建押货退货单", touchable=False).get_name(), "新建押货退货单", msg="新建押货退货单")
        assert_equal(poco("去新建", touchable=True).get_name(), "去新建", msg="去新建")
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

        poco("结算").click()
        # 选择退货原因
        poco("原因").click()
        poco("选择原因").wait(1)
        poco("结点退货").swipe([0, -0.08]) # 其他原因退货
        poco("确定").click()

        poco("提交退货申请").click()

        assert_equal(poco("押货退货单提交成功", touchable=False).get_name(), "押货退货单提交成功", msg="押货退货单提交成功")
        assert_equal(poco("查看详情", touchable=True).get_name(), "查看详情", msg="查看详情")
        assert_equal(poco("再下一单", touchable=True).get_name(), "再下一单", msg="再下一单")
        assert_equal(poco("返回服务中心首页", touchable=True).get_name(), "返回服务中心首页", msg="返回服务中心首页")

        poco("再下一单").click()
        assert_equal(poco("新建押货退货单", touchable=False).get_name(), "新建押货退货单", msg="新建押货退货单")
        assert_equal(poco("去新建", touchable=True).get_name(), "去新建", msg="去新建")

        # 退到服务中心首页
        for i in range(2):
            poco(name="android.view.View", touchable=True).click()
              
    @allure.severity(P3)            
    @allure.title("我的-我的服务中心-押货退货：押货退货提交后【查看详情】检查")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_05(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)   
        poco("押货退货").click()
        # 去新建
        poco(name="android.view.View", touchable=True)[1].wait(1).click()

        assert_equal(poco("新建押货退货单", touchable=False).get_name(), "新建押货退货单", msg="新建押货退货单")
        assert_equal(poco("去新建", touchable=True).get_name(), "去新建", msg="去新建")
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

        poco("结算").click()
        # 选择退货原因
        poco("原因").click()
        poco("选择原因").wait(1)
        poco("结点退货").swipe([0, -0.08]) # 其他原因退货
        poco("确定").click()

        poco("提交退货申请").click()

        assert_equal(poco("押货退货单提交成功", touchable=False).get_name(), "押货退货单提交成功", msg="押货退货单提交成功")
        assert_equal(poco("查看详情", touchable=True).get_name(), "查看详情", msg="查看详情")
        assert_equal(poco("再下一单", touchable=True).get_name(), "再下一单", msg="再下一单")
        assert_equal(poco("返回服务中心首页", touchable=True).get_name(), "返回服务中心首页", msg="返回服务中心首页")

        poco("查看详情").click()
        assert_equal(poco("押货退货单详情", touchable=False).get_name(), "押货退货单详情", msg="押货退货单详情")
        assert_equal(poco("待审核\n待分公司审核", touchable=False).get_name(), "待审核\n待分公司审核", msg="待审核\n待分公司审核")

        # 退到服务中心首页
        for i in range(2):
            poco(name="android.view.View", touchable=True).click()
             
    @allure.severity(P3)            
    @allure.title("我的-我的服务中心-押货退货：各个tab列表遍历检查")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_06(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)   
        poco("押货退货").click()
        poco("全部\n第 1 个标签，共 6 个", selected=True).exists()

        poco("待审核\n第 2 个标签，共 6 个", selected=False).exists()
        poco("待审核\n第 2 个标签，共 6 个", selected=False).click()
        poco("待审核\n第 2 个标签，共 6 个", selected=True).exists()

        poco("待退回\n第 3 个标签，共 6 个", selected=False).exists()
        poco("待退回\n第 3 个标签，共 6 个", selected=False).click()
        poco("待退回\n第 3 个标签，共 6 个", selected=True).exists()

        poco("待验货\n第 4 个标签，共 6 个", selected=False).exists()
        poco("待验货\n第 4 个标签，共 6 个", selected=False).click()
        poco("待验货\n第 4 个标签，共 6 个", selected=True).exists()

        poco("已完成\n第 5 个标签，共 6 个", selected=False).exists()
        poco("已完成\n第 5 个标签，共 6 个", selected=False).click()
        poco("已完成\n第 5 个标签，共 6 个", selected=True).exists()

        poco("已取消\n第 6 个标签，共 6 个", selected=False).exists()
        poco("已取消\n第 6 个标签，共 6 个", selected=False).click()
        poco("已取消\n第 6 个标签，共 6 个", selected=True).exists()

        # 返回我的服务中心
        poco(name="android.view.View", touchable=True).wait(1).click()

                    
    @allure.severity(P3)            
    @allure.title("我的-我的服务中心-押货退货：退货原因及取消退货检查")
    @pytest.mark.parametrize("uuid", UUIDS)
    def test_07(self, uuid):
                   
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)               
        poco("押货退货").click()
        # 去新建
        poco(name="android.view.View", touchable=True)[1].click()

        assert_equal(poco("新建押货退货单", touchable=False).get_name(), "新建押货退货单", msg="新建押货退货单")
        assert_equal(poco("去新建", touchable=True).get_name(), "去新建", msg="去新建")
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
        poco(name="android.view.View", touchable=True).click()

        poco("结算").click()
        # 选择退货原因
        poco("原因").click()
        assert_equal(poco("选择原因", touchable=False).get_name(), "选择原因", msg="选择原因")
        poco("取消").click()

        poco("原因").click()
        poco("确定").click()
        poco("原因").click()
        poco("结点退货").swipe([-0.0233, -0.0828])
        poco("确定").click()
        poco("原因").click()
        poco("结点退货").swipe([-0.013, -0.1505])
        poco("确定").click()
        # 退出押货
        poco(name="android.view.View", touchable=True).click()
        poco(name="android.view.View", touchable=True)[0].click()

        assert_equal(poco("提示", touchable=False).get_name(), "提示", msg="提示")
        assert_equal(poco("确定取消押货退货单？", touchable=False).get_name(), "确定取消押货退货单？", msg="确定取消押货退货单？")
        poco("取消").click()

        poco(name="android.view.View", touchable=True)[0].click()
        assert_equal(poco("提示", touchable=False).get_name(), "提示", msg="提示")
        assert_equal(poco("确定取消押货退货单？", touchable=False).get_name(), "确定取消押货退货单？", msg="确定取消押货退货单？")
        poco("确认").click()
        # 退到服务中心首页
        poco(name="android.view.View", touchable=True)[0].click()
        