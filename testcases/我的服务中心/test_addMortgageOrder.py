# coding:utf-8

__author__ = "ligeit"

from airtest.core.api import *
import time
import allure
from setting import P1, P2, P3, DINGZHI13, CSCP6
from utils.step_for_uuids import step_for_uuids
from utils.log_report import log_report


@allure.feature("我的-我的服务中心")
@allure.story("我的-我的服务中心-定制品押货")
class TestClass:
    """
    我的-我的服务中心-定制品押货
    """

    @allure.severity(P1)            
    @allure.title("我的-我的服务中心-定制品押货：定制品押货主路径检查")
    @log_report()
    def test_01(self):
                
        @step_for_uuids()
        def step_01(poco):
            
            poco("定制品押货").click()
            # 配置了分配量的定制品押货
            if poco(nameMatches="^.+\n.+\n￥\d+\.\d+\n当前库存 \d+\n最大可押 \d+\n押货下单$").exists():
                for star in poco(nameMatches="^.+\n.+\n￥\d+\.\d+\n当前库存 \d+\n最大可押 \d+\n押货下单$"):
                    t = star.get_name()
                    if DINGZHI13 in t:
                        star.click([0.9,0.8]) # 押货下单
                        time.sleep(1)
                        poco(nameMatches="^.+\n产品编号：.+\n当前库存：\d+$").child("android.view.View").click() # +数量，押货数量=1
                        poco(nameMatches="^.+\n产品编号：.+\n当前库存：\d+$").child("android.view.View")[1].click() # +数量，押货数量=2

                        poco(name="android.view.View", touchable=True).wait(1).click()
                        poco(nameMatches="^押货下单\(\d+\)$").click()

                        assert_equal(poco("押货单提交成功", touchable=False).get_name(), "押货单提交成功", msg="押货单提交成功", snapshot=True)
                        assert_equal(poco("查看详情", touchable=True).get_name(), "查看详情", msg="查看详情")
                        assert_equal(poco("再下一单", touchable=True).get_name(), "再下一单", msg="再下一单")
                        assert_equal(poco("返回服务中心首页", touchable=True).get_name(), "返回服务中心首页", msg="返回服务中心首页")

                        poco("返回服务中心首页").click()
                        break
            # 未配置分配量的定制品押货
            poco("定制品押货").click()
            for star in poco(nameMatches="^.+\n.+\n￥\d+\.\d+\n当前库存 \d+\n押货下单$"):
                t = star.get_name()
                if CSCP6 in t:
                    star.click([0.9,0.8]) # 进入详情
                    time.sleep(1)
                    for i in poco(nameMatches="^.+\n产品编号：.+\n当前库存：\d+$"):
                        i.child("android.view.View").click() # +数量，押货数量=1
                        i.child("android.view.View")[1].click() # +数量，押货数量=2

                    poco(name="android.view.View", touchable=True).wait(1).click() 
                    poco(nameMatches="^押货下单\(\d+\)$").click()

                    assert_equal(poco("押货单提交成功", touchable=False).get_name(), "押货单提交成功", msg="押货单提交成功", snapshot=True)
                    assert_equal(poco("查看详情", touchable=True).get_name(), "查看详情", msg="查看详情")
                    assert_equal(poco("再下一单", touchable=True).get_name(), "再下一单", msg="再下一单")
                    assert_equal(poco("返回服务中心首页", touchable=True).get_name(), "返回服务中心首页", msg="返回服务中心首页")

                    poco("返回服务中心首页").click()
                    break  
            
        step_01()
        
    @allure.severity(P2)            
    @allure.title("我的-我的服务中心-定制品押货：[+][-]增减定制品押货数量操作检查")
    @log_report()
    def test_02(self):
                
        @step_for_uuids()
        def step_01(poco):
            
            poco("定制品押货").click()
            # 没有配置分配量的定制品押货
            stars01 = poco(nameMatches="^.+\n.+\n￥\d+\.\d+\n当前库存 \d+\n押货下单$")
            for star in stars01:
                t = star.get_name()
                if CSCP6 in t:
                    star.click([0.9,0.8]) # 押货下单
                    time.sleep(1)
                    for i in poco(nameMatches="^.+\n产品编号：.+\n当前库存：\d+$"):
                        i.child("android.view.View").click() # +数量，押货数量=1
                        assert_equal(poco("1", type="android.view.View").get_name(), "1", msg="押货数量=1")

                        i.child("android.view.View")[1].click() # +数量，押货数量=2
                        assert_equal(poco("2", type="android.view.View").get_name(), "2", msg="押货数量=2")

                        i.child("android.view.View").click() # -数量，押货数量=1
                        assert_equal(poco("1", type="android.view.View").get_name(), "1", msg="押货数量=1")

                        i.child("android.view.View").click() # -数量，押货数量=0
                        assert_equal(poco("温馨提示").get_name(), "温馨提示", msg="温馨提示")
                        assert_equal(poco("确定要删除该商品？").get_name(), "确定要删除该商品？", msg="确定要删除该商品？")
                        # 押货数量减为0时，弹窗确认
                        poco("取消").click()
                        assert_equal(poco("1", type="android.view.View").get_name(), "1", msg="押货数量=1")

                        i.child("android.view.View").click() # -数量，押货数量=0
                        assert_equal(poco("温馨提示").get_name(), "温馨提示", msg="温馨提示")
                        assert_equal(poco("确定要删除该商品？").get_name(), "确定要删除该商品？", msg="确定要删除该商品？")
                        # 押货数量减为0时，弹窗确认
                        poco("确认").click()
                        assert_equal(poco("0", type="android.view.View").get_name(), "0", msg="押货数量=0")
                    # 返回服务中心首页
                    for i in range(2):
                        poco(name="android.view.View", touchable=True).wait(1).click() 
                    break
            
        step_01()
        
    @allure.severity(P3)            
    @allure.title("我的-我的服务中心-定制品押货：直接输入定制品押货数量操作检查")
    @log_report()
    def test_03(self):
                
        @step_for_uuids()
        def step_01(poco):
            
            poco("定制品押货").click()
            # 没有配置分配量的定制品押货
            stars01 = poco(nameMatches="^.+\n.+\n￥\d+\.\d+\n当前库存 \d+\n押货下单$")
            for star in stars01:
                t = star.get_name()
                if "CSCP6" in t:
                    star.click([0.9,0.8]) # 押货下单
                    time.sleep(1)
                    for i in poco(nameMatches="^.+\n产品编号：.+\n当前库存：\d+$"):
                        poco("0").click()
                        assert_equal(poco("请输入数量").get_name(), "请输入数量", msg="请输入数量")
                        assert_equal(poco("android.widget.EditText", text="0").get_text(), "0", msg="0")
                        poco("android.widget.EditText").click()
                        poco("android.widget.EditText").set_text("2")
                        poco("取消").click()
                        assert_equal(poco("0", type="android.view.View").get_name(), "0", msg="押货数量=0")

                        poco("0").click()
                        assert_equal(poco("请输入数量").get_name(), "请输入数量", msg="请输入数量")
                        assert_equal(poco("android.widget.EditText", text="0").get_text(), "0", msg="0")
                        poco("android.widget.EditText").click()
                        poco("android.widget.EditText").set_text("2")
                        poco("确定").click()
                        assert_equal(poco("2", type="android.view.View").get_name(), "2", msg="押货数量=2")

                        poco("2").click()
                        assert_equal(poco("请输入数量").get_name(), "请输入数量", msg="请输入数量")
                        assert_equal(poco("android.widget.EditText", text="2").get_text(), "2", msg="2")
                        poco("android.widget.EditText").click()
                        poco("android.widget.EditText").set_text("0")
                        poco("确定").click()
                        assert_equal(poco("温馨提示").get_name(), "温馨提示", msg="温馨提示")
                        assert_equal(poco("确定要删除该商品？").get_name(), "确定要删除该商品？", msg="确定要删除该商品？")
                        # 押货数量减为0时，弹窗确认
                        poco("取消").click()
                        assert_equal(poco("2", type="android.view.View").get_name(), "2", msg="押货数量=2")

                        poco("2").click()
                        assert_equal(poco("请输入数量").get_name(), "请输入数量", msg="请输入数量")
                        assert_equal(poco("android.widget.EditText", text="2").get_text(), "2", msg="2")
                        poco("android.widget.EditText").click()
                        poco("android.widget.EditText").set_text("0")
                        poco("确定").click()
                        assert_equal(poco("温馨提示").get_name(), "温馨提示", msg="温馨提示")
                        assert_equal(poco("确定要删除该商品？").get_name(), "确定要删除该商品？", msg="确定要删除该商品？")
                        # 押货数量减为0时，弹窗确认
                        poco("确认").click()
                        assert_equal(poco("0", type="android.view.View").get_name(), "0", msg="押货数量=0")
                    # 返回服务中心首页
                    for i in range(2):
                        poco(name="android.view.View", touchable=True).wait(1).click() 
                    break
            
        step_01()
        
    @allure.severity(P3)            
    @allure.title("我的-我的服务中心-定制品押货：押货页面各字段信息变化检查")
    @log_report()
    def test_04(self):
                
        @step_for_uuids()
        def step_01(poco):
            
            poco("定制品押货").click()
            assert_equal(poco("合计：¥0.00").get_name(), "合计：¥0.00", msg="合计：¥0.00")
            assert_equal(poco("押货下单(0)").get_name(), "押货下单(0)", msg="押货下单(0)")

            # 没有配置分配量的定制品押货
            stars01 = poco(nameMatches="^.+\n.+\n￥\d+\.\d+\n当前库存 \d+\n押货下单$")
            for star in stars01:
                t = star.get_name()
                if "CSCP6" in t:
                    star.click([0.9,0.8]) # 押货下单

                    # 押货数量0-->2
                    poco("0").click()
                    poco("android.widget.EditText").click()
                    poco("android.widget.EditText").set_text("2")
                    poco("确定").click()

                    t1 = poco(nameMatches="^￥\d+\.\d{2,2}$").get_name() # 押货价
                    t2 = poco(nameMatches="^\d+$")[0].get_name() # 押货数量
                    t = float(t1[1:]) * int(t2)
                    #返回定制品押货首页
                    poco(name="android.view.View", touchable=True).wait(1).click() 

                    assert_equal(poco(f"合计：¥{t}0").get_name(), f"合计：¥{t}0", msg=f"合计：¥{t}0")
                    assert_equal(poco(f"押货下单({t2})").get_name(), f"押货下单({t2})", msg=f"押货下单({t2})")
                    #返回服务中心首页
                    poco(name="android.view.View", touchable=True).wait(1).click() 
            
        step_01()
        
    @allure.severity(P1)            
    @allure.title("我的-我的服务中心-定制品押货：定制品押货成功后，【再下一单】检查")
    @log_report()
    def test_05(self):
                
        @step_for_uuids()
        def step_01(poco):
            
            # 未配置分配量的定制品押货
            poco("定制品押货").click()
            for star in poco(nameMatches="^.+\n.+\n￥\d+\.\d+\n当前库存 \d+\n押货下单$"):
                t = star.get_name()
                if "CSCP6" in t:
                    star.click([0.9,0.8]) # 进入详情
                    time.sleep(1)
                    for i in poco(nameMatches="^.+\n产品编号：.+\n当前库存：\d+$"):
                        i.child("android.view.View").click() # +数量，押货数量=1
                        i.child("android.view.View")[1].click() # +数量，押货数量=2
                    poco(name="android.view.View", touchable=True).wait(1).click() 
                    poco(nameMatches="^押货下单\(\d+\)$").click()

                    assert_equal(poco("押货单提交成功", touchable=False).get_name(), "押货单提交成功", msg="押货单提交成功")
                    assert_equal(poco("查看详情", touchable=True).get_name(), "查看详情", msg="查看详情")
                    assert_equal(poco("再下一单", touchable=True).get_name(), "再下一单", msg="再下一单")
                    assert_equal(poco("返回服务中心首页", touchable=True).get_name(), "返回服务中心首页", msg="返回服务中心首页")

                    poco("再下一单").click() # 跳转定制品押货首页
                    assert_equal(poco("合计：¥0.00").get_name(), "合计：¥0.00", msg="合计：¥0.00")
                    assert_equal(poco("押货下单(0)").get_name(), "押货下单(0)", msg="押货下单(0)")
                    break 
            #返回服务中心首页
            poco(name="android.view.View", touchable=True).wait(1).click()  
            
        step_01()
        
    @allure.severity(P1)            
    @allure.title("我的-我的服务中心-定制品押货：定制品押货成功后，【查看详情】检查")
    @log_report()
    def test_06(self):
                
        @step_for_uuids()
        def step_01(poco):
            
            # 未配置分配量的定制品押货
            poco("定制品押货").click()
            for star in poco(nameMatches="^.+\n.+\n￥\d+\.\d+\n当前库存 \d+\n押货下单$"):
                t = star.get_name()
                if "CSCP6" in t:
                    star.click([0.9,0.8]) # 进入详情
                    time.sleep(1)
                    for i in poco(nameMatches="^.+\n产品编号：.+\n当前库存：\d+$"):
                        i.child("android.view.View").click() # +数量，押货数量=1
                        i.child("android.view.View")[1].click() # +数量，押货数量=2
                    poco(name="android.view.View", touchable=True).wait(1).click() 
                    poco(nameMatches="^押货下单\(\d+\)$").click()

                    assert_equal(poco("押货单提交成功", touchable=False).get_name(), "押货单提交成功", msg="押货单提交成功")
                    assert_equal(poco("查看详情", touchable=True).get_name(), "查看详情", msg="查看详情")
                    assert_equal(poco("再下一单", touchable=True).get_name(), "再下一单", msg="再下一单")
                    assert_equal(poco("返回服务中心首页", touchable=True).get_name(), "返回服务中心首页", msg="返回服务中心首页")

                    poco("查看详情").click()
                    poco("复制").click()
                    assert_equal(poco("押货单详情", touchable=False).get_name(), "押货单详情", msg="押货单详情")
                    assert_equal(poco("待发货", touchable=False).get_name(), "待发货", msg="待发货")
                    assert_equal(poco("复制", touchable=True).get_name(), "复制", msg="复制")
                    assert_equal(poco("修改记录", touchable=True).get_name(), "修改记录", msg="修改记录")
                    assert_equal(poco("修改记录", touchable=True).get_name(), "修改记录", msg="修改记录")
                    assert poco(nameMatches="^押货单号：YH.+\n下单时间：.+$").exists()
                    assert poco(name="测试定制销售分配量定时生效\nCSCP6|\n押货价：￥37.00\n已发数量 0\n押货数量 2")[0].exists()
                    assert poco(name="测试定制销售分配量定时生效\nCSCP6|\n押货价：￥37.00\n已发数量 0\n押货数量 2")[1].exists()
                    assert poco(name="押货合计：￥148.0").exists()
                    break 
            # 返回服务中心首页
            for i in range(2):
                poco(name="android.view.View", touchable=True).wait(1).click() 
        
        step_01()






        


