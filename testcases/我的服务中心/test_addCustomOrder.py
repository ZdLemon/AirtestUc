# coding:utf-8

__author__ = "ligeit"

import time
import allure
from airtest.core.api import *
from setting import P1, P2, P3, M7035
from utils.step_for_uuids import step_for_uuids
from utils.log_report import log_report


@allure.feature("我的-我的服务中心")
@allure.story("我的-我的服务中心-押货下单")
class TestClass:
    """
    我的-我的服务中心-押货下单
    """

    @allure.severity(P1)            
    @allure.title("我的-我的服务中心-押货下单：押货主路径检查")
    @log_report()
    def test_01(self):
                
        @step_for_uuids()
        def step_01(poco):
            
            poco("押货下单").click()
            for i in poco(nameMatches=".*\n.*\n.*\n当前库存 \d+$"):
                # 有产品图
                if i.child("android.widget.ImageView").exists():
                    # 押货量==0
                    if i.child("0").exists():
                        i.child("android.view.View").click()
                    # 押货量>0
                    elif i.child(nameMatches="^\d+$").exists():
                        i.child("android.view.View")[1].click()
                # 无产品图
                else:
                    # 押货量==0
                    if i.child("0").exists():
                        i.child("android.view.View")[1].click()
                    # 押货量>0
                    elif i.child(nameMatches="^\d+$").exists():
                        i.child("android.view.View")[2].click()

                time.sleep(1)

            poco("押货下单").click()

            assert poco("押货单提交成功", touchable=False).exists()
            assert poco("查看详情", touchable=True).exists()
            assert poco("再下一单", touchable=True).exists()
            assert poco("返回服务中心首页", touchable=True).exists()

            poco("返回服务中心首页", touchable=True).click()

        step_01()
        
    @allure.severity(P3)            
    @allure.title("我的-我的服务中心-押货下单：[+][-]增减押货数量操作检查")
    @log_report()
    def test_02(self):
                
        @step_for_uuids()
        def step_01(poco):
            
            poco("押货下单").click()
            count = 0
            for i in poco(nameMatches=".*\n.*\n.*\n当前库存 \d+$"):
                # 有产品图,押货量==0
                if i.child("android.widget.ImageView").exists() and i.child("0").exists() and count == 0:
                    count += 1
                    i.child("android.view.View").click() # 押货量新增1，押货量==1
                    time.sleep(0.5)
                    i.child("android.view.View")[1].click() # 押货量新增1，押货量==2

                    time.sleep(0.5)
                    i.child("android.view.View")[0].click() # 押货量减1，押货量==1
                    time.sleep(0.5)
                    i.child("android.view.View")[0].click() # 押货量减1，押货量==0
                    poco("确定删除该产品？").wait(1)
                    poco("取消").click()

                    time.sleep(0.5)
                    i.child("android.view.View")[0].click() # 押货量减1，押货量==0
                    poco("确定删除该产品？").wait(1)
                    poco("确认").click()
                    
                    time.sleep(0.5)
                    i.child("android.view.View").click() # 押货量新增1，押货量==1
                elif count > 0:
                    break # 终止循环      

            poco("押货下单").click()
            
            assert poco("押货单提交成功", touchable=False).exists()
            assert poco("查看详情", touchable=True).exists()
            assert poco("再下一单", touchable=True).exists()
            assert poco("返回服务中心首页", touchable=True).exists()

            poco("返回服务中心首页", touchable=True).click()

        step_01()
        
    @allure.severity(P3)            
    @allure.title("我的-我的服务中心-押货下单：直接输入押货数量操作检查")
    @log_report()
    def test_03(self):
                
        @step_for_uuids()
        def step_01(poco):
            
            poco("押货下单").click()
            count = 0
            for i in poco(nameMatches=".*\n.*\n.*\n当前库存 \d+$"):
                # 有产品图,押货量==0
                if i.child("android.widget.ImageView").exists() and i.child("0").exists() and count == 0:
                    count += 1

                    i.child("0").click()
                    poco("请输入数量").wait(1)
                    poco("取消").click()

                    i.child("0").click()
                    poco("请输入数量").wait(1)
                    poco("android.widget.EditText").click()
                    poco("android.widget.EditText").set_text("2") # 押货量新增2，押货量==2
                    poco("确定").click()               

                    i.child("2").click()
                    poco("请输入数量").wait(1)
                    poco("android.widget.EditText").click()
                    poco("android.widget.EditText").set_text("0") # 押货量减少2，押货量==0
                    poco("确定").click()

                    poco("确定删除该产品？").wait(1)
                    poco("确认").click() 

                    i.child("0").click()
                    poco("请输入数量").wait(1)
                    poco("android.widget.EditText").click()
                    poco("android.widget.EditText").set_text("2") # 押货量新增2，押货量==2
                    poco("确定").click()
                elif count > 0:
                    break # 终止循环 

            poco("押货下单").click()
            
            assert poco("押货单提交成功", touchable=False).exists()
            assert poco("查看详情", touchable=True).exists()
            assert poco("再下一单", touchable=True).exists()
            assert poco("返回服务中心首页", touchable=True).exists()

            poco("返回服务中心首页", touchable=True).click()
        
        step_01()

    @allure.severity(P3)            
    @allure.title("我的-我的服务中心-押货下单：购物车操作检查")
    @log_report()
    def test_04(self):

        @step_for_uuids()
        def step_01(poco):
            
            # 购物车为空
            poco("押货下单").click()
            # 如果购物车数量!=0
            while poco(nameMatches="合计：¥ \d+\.\d+\n可用余额：¥ \d+\.\d+").get_name()[:9] != "合计：¥ 0.00":
                # 进入购物车
                poco(nameMatches="合计：¥ \d+\.\d+\n可用余额：¥ \d+\.\d+").child(nameMatches="^\d+$").click()
                
                stars = poco(nameMatches=".*\n.*\n.*\n当前库存 \d+$").child(nameMatches="^\d+$")
                stars[0].click()

                poco("请输入数量").wait(1)
                poco("android.widget.EditText").click()
                poco("android.widget.EditText").set_text("0") # 押货量减少2，押货量==0
                poco("确定").click()

                poco("确定删除该产品？").wait(1)
                poco("确认").click()
                # 退出购物车
                poco(nameMatches="购物车\n合计：¥ \d+\.\d+\n可用余额：¥ \d+\.\d+").child("android.view.View")[0].click()
                # 刷新页面
                poco(nameMatches=".*\n.*\n.*\n当前库存 \d+$")[1].swipe([0, 0.1206])

            # 进入购物车
            poco(nameMatches="合计：¥ \d+\.\d+\n可用余额：¥ \d+\.\d+").child("android.view.View")[1].click()

            assert poco(nameMatches="购物车\n合计：¥ \d+\.\d+\n可用余额：¥ \d+\.\d+").get_name()[:13] == "购物车\n合计：¥ 0.00"
            assert poco(nameMatches=".*\n.*\n.*\n当前库存 \d+$").exists() is False
            # 退出购物车
            poco(nameMatches="购物车\n合计：¥ \d+\.\d+\n可用余额：¥ \d+\.\d+").child("android.view.View")[0].click()


            # 购物车不为空
            # 如果购物车数量==0
            if poco(nameMatches="合计：¥ \d+\.\d+\n可用余额：¥ \d+\.\d+").get_name()[:9] == "合计：¥ 0.00":
                count = 0
                for i in poco(nameMatches=".*\n.*\n.*\n当前库存 \d+$"):
                    # 有产品图,押货量==0
                    if i.child("android.widget.ImageView").exists() and i.child("0").exists() and count <= 1:
                        count += 1
                        i.child("android.view.View").click() # 押货量新增1，押货量==1
                        time.sleep(0.5)
                        i.child("android.view.View")[1].click() # 押货量新增1，押货量==2
                    elif count > 1:
                        break # 终止循环

            # 购物车押货数量
            count01 = int(poco(nameMatches="合计：¥ \d+\.\d+\n可用余额：¥ \d+\.\d+").child(nameMatches="^\d+$").get_name())
            # 进入购物车
            poco(nameMatches="合计：¥ \d+\.\d+\n可用余额：¥ \d+\.\d+").child(nameMatches="^\d+$").click()

            # 押货明细中押货数量
            count02 = 0
            for i in poco(nameMatches=".*\n.*\n.*\n当前库存 \d+$").child(nameMatches="^\d+$"):
                count02 += int(i.get_name())

            assert count01 == count02 # 购物车押货数量==押货明细中押货数量
            assert len(poco(nameMatches=".*\n.*\n.*\n当前库存 \d+$")) >= 1
            # 退出购物车
            poco(nameMatches="购物车\n合计：¥ \d+\.\d+\n可用余额：¥ \d+\.\d+").child("android.view.View")[0].click()
            # 退出押货下单
            poco(name="android.view.View", touchable=True).wait(1).click()

        step_01()

    @allure.severity(P3)            
    @allure.title("我的-我的服务中心-押货下单：搜索全部分类操作检查")
    @log_report()
    def test_05(self):

        @step_for_uuids()
        def step_01(poco):
               
            poco("押货下单").click()
            indexs = ["全部分类", "保洁用品及个人护理品", "化妆品(玛丽艳美容护肤品)", "保健器材", "健康食品", "服务中心物料", "服务中心赠品", "辅销资料", "积分换购", "小型厨具", "赠送资料"]
            y = 0.08
            count = 0
            while count < 11:
                for i in indexs:
                    if poco(i).exists():
                        assert_equal(poco("搜索").get_name(), "搜索", msg="搜索存在")
                        assert_equal(poco("押货下单").get_name(), "押货下单", msg="押货下单存在")
                        assert_in(poco(i).get_name(), indexs, msg= i)

                        poco(i).click()
                        assert_equal(poco("请选择").get_name(), "请选择", msg="请选择存在")
                        assert_equal(poco("取消").get_name(), "取消", msg="取消")

                        poco(indexs[0]).swipe([0, -y])
                        poco("确定").click()
                        sleep(1)

                        y += 0.05
                        count += 1
                        continue

            # 退出押货下单
            poco(name="android.view.View", touchable=True).wait(1).click()

        step_01()

    @allure.severity(P3)            
    @allure.title("我的-我的服务中心-押货下单：搜索输入框检查")
    @log_report()
    def test_06(self):

        @step_for_uuids()
        def step_01(poco):
                
            poco("押货下单").click()
            assert poco("android.widget.EditText").get_text() == "搜索产品名称和编号"
            poco("android.widget.EditText").click()
            poco("android.widget.EditText").set_text(M7035)
            poco("搜索").click()

            for i in poco(nameMatches=".*\n.*\n.*\n当前库存 \d+$"):
                assert M7035 in i.get_name()
            # 删除搜索文本
            poco("android:id/content").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.View").child("android.view.View")\
                .child("android.view.View").child("android.view.View").child("android.view.View").child("android.view.View")[1].child("android.view.View").click()
            
            # 退出押货下单
            poco(name="android.view.View", touchable=True).wait(1).click()

        step_01()          


