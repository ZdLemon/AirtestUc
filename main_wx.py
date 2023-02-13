# coding:utf-8

import pytest
import logging
from airtest.core.api import *
from airtest.core.android.adb import *
from airtest.core.android.android import *
from airtest.utils.apkparser import APK
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from setting import PACKAGE, mobile_3, DEV
from multiprocessing import Process
from threading import Thread


def get_all_device_info():
    "获取所有设备的uuid"
    
    adb = ADB()
    device_list = adb.devices()
    uuids = []
    for dev in device_list:
        if dev[1] != "device":
            continue
        uuids.append(dev[0])
    
    return uuids


def init_dev(uuids):
    "初始化设备"
    
    log(f"uuids : {uuids}")
    auto_setup(
        __file__, 
        devices=[f"Android://127.0.0.1:5037/{uuid}?cap_method=JAVACAP&&ori_method=MINICAPORI&&touch_method=MINITOUCH" for uuid in uuids], 
        # logdir=True, 
        compress=90)
     
 
def init_setting(uuids):
    "初始化setting.py文件"
    with open("setting.py", "rt", encoding="utf-8") as f:
        
        setting = [i for i in f.read().split("\n") if i.startswith("UUIDS") is False]
        # 末尾连续2个空
        if setting[-2:] == ["", ""]:
            setting.pop()
        setting.append(f"UUIDS = {uuids}") 
    
        with open("setting.py", "wt", encoding="utf-8") as f:
            for line in setting:
                if line:
                    f.write(line)
                    f.write("\n")
                else:
                    f.write("\n")
    

def _verify(poco):
    "vivo,oppo安装apk时，需要安全验证,安装输入法时也要"
    verify = 0
    while verify < 2:
        if poco(text="继续安装").exists():
            poco(text="继续安装").click()
            verify += 1

    
def _device_upgrade(poco):
    """
    检查手机中的package版本号，与本地apk版本号进行对比，如果本地文件版本号更高，说明需要覆盖安装
    """
    
    for p in os.listdir(r"data"):
        if p.startswith("YouCongShop") and p.endswith("apk"):
            apk_path = os.path.join("data", p)
            
            wake()
            android = Android()
            apk_version = int(APK(apk_path).androidversion_code) # 本地apk版本号
            installed_version = android.adb.get_package_version(PACKAGE) # 手机已安装apk版本号
            if installed_version is None or apk_version > int(installed_version):
                # 返回设备型号
                d =  shell("getprop ro.product.manufacturer")
                # vivo,oppo安装apk时需要安全验证
                if d.startswith("vivo") or d.startswith("oppo"):
                    t = Thread(target=_verify, args=[poco,])
                    t.setDaemon(True)
                    t.start()
                    # 安装参数 -r 表示覆盖安装
                    install(apk_path, install_options=["-r", "-t"])
                #非vivo,oppo
                else:
                    # 安装参数 -r 表示覆盖安装
                    install(apk_path, install_options=["-r", "-t"])
                        
            break


def _start_app(poco):
    "打开app,并在10秒内设置好权限，跳过引导说明，同意隐私协议"
  
    # 打开APP
    start_app(PACKAGE)
    
    count = 0
    nodes = 0
    while count < 10 and nodes < 5:
        # 隐私协议
        if poco("我同意").exists():
            poco("我同意").click()
            nodes += 1 # 点击一次
        # 指引    
        elif poco("跳过\n欢迎来到油葱商城\n便捷体验 倾力打造").exists():
            stop_app(PACKAGE)
            sleep(1)
            start_app(PACKAGE)
            nodes += 1 # 点击一次
        # 华为打开app授权
        elif poco("com.android.permissioncontroller:id/permission_allow_foreground_only_button").exists():
            poco("com.android.permissioncontroller:id/permission_allow_foreground_only_button").click()
            nodes += 1 # 点击一次
        elif poco(text="仅在使用中允许").exists():
            poco(text="仅在使用中允许").click()   
            nodes += 1 # 点击一次
        # vivo打开app授权
        elif poco(text="允许").exists():
            poco(text="允许").click()   
            nodes += 1 # 点击一次
        # vivo打开app定位授权
        elif poco(text="仅在前台使用应用时允许").exists():
            poco(text="仅在前台使用应用时允许").click()   
            nodes += 1 # 点击一次
        # 关闭分享海报
        elif poco("分享").exists():
            poco("android:id/content").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.View").child("android.view.View")\
                .child("android.view.View").child("android.view.View").child("android.view.View")[0].click()
            nodes += 1 # 点击一次
        else:
            count += 1
            sleep(5)
            if poco(nameMatches="^首页\n.+").exists():
                count = 10
    
    assert_equal(poco(nameMatches="^首页\n.+").exists(), True, msg="首页可点击")         
    

def _set_dev(poco):
    "设置运行环境"
                      
    # 环境设置
    if DEV == "(TES)":
        if poco(DEV).exists():
            return
        else:
            for i in range(5):
                poco('第 1 个标签，共 3 个').click()
                time.sleep(0.1)
            poco("运行环境").wait(2).click()
            poco("预生产环境").wait(2).swipe([0, -0.084])
            poco("确定").wait(2).click()
            poco("确定").wait(2).click()                
    elif DEV == "(UAT)":
        if poco(DEV).exists():
            return
        else:
            for i in range(5):
                poco('第 1 个标签，共 3 个').click()
                time.sleep(0.1)
            poco("运行环境").wait(2).click()
            poco("预生产环境").wait(2).swipe([-0.0804, -0.2636])
            poco("确定").wait(2).click()
            poco("确定").wait(2).click() 

    # 打开APP
    time.sleep(0.5)
    start_app(PACKAGE)
    # 隐私协议
    if poco("我同意").wait(10).exists():
        poco("我同意").click()
                

def _login(mobile, poco):
                      
    # 点击【我的】登录    
    if poco(nameMatches="^首页\n.+").exists() and poco("第 1 个标签，共 3 个").exists():

        # 点击【我的】登录    
        poco("我的\n第 3 个标签，共 3 个").click()
        if poco(text="其它方式登录").wait(5).exists():
            poco(text="其它方式登录").click()
        
        if poco("欢迎登录油葱商城").exists():
            poco(text="请输入手机号").click()
            poco(text="请输入手机号").set_text(mobile)
            time.sleep(0.2)
            
            poco("获取验证码").click()
            if poco("请完成安全验证").wait(2).exists():
                poco("请完成安全验证").child("android.view.View")[1].focus([0.17, 0.55]).swipe([0.68, 0.002], duration=0.5)
                time.sleep(0.2)
                
            poco(text="请输入短信验证码").click()
            poco(text="请输入短信验证码").set_text("666666")
            time.sleep(0.2) 
               
            poco("android.widget.FrameLayout").offspring("android:id/content").child("android.widget.FrameLayout").child("android.widget.FrameLayout")\
                .child("android.view.View").child("android.view.View").child("android.view.View").offspring("其他登录方式").child("android.view.View").child("android.view.View").child("android.view.View").click()
            time.sleep(0.2)    
            poco("登录").click()
            
            # 关闭分享海报
            if poco("分享").wait(5).exists():
                poco("android:id/content").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.View").child("android.view.View")\
                    .child("android.view.View").child("android.view.View").child("android.view.View")[0].click()

        assert poco("我的\n第 5 个标签，共 5 个").exists()
        

def init_all(uuid, mobile):
       
    dev =connect_device(f'Android://127.0.0.1:5037/{uuid}?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MINITOUCH')
    poco = AndroidUiautomationPoco(device=dev, use_airtest_input=True, screenshot_each_action=False) 
    _device_upgrade(poco)
    _start_app(poco)
    _set_dev(poco)
    _login(mobile, poco)
                    

def uninstall_all(uuid):
    "卸载设备上的app"
    
    set_current(uuid)
    stop_app(PACKAGE)
    clear_app(PACKAGE)
    uninstall(PACKAGE)
    
 
if __name__ == "__main__":
    
    UUIDS = get_all_device_info()
    init_setting(UUIDS)

    if len(mobile_3) >= len(UUIDS): # 登录账号数量必须不少于设备数量
        if len(UUIDS) > 1:
            # 多进程安装，升级app,设置测试环境，登录云商
            process_list = []
            for i in range(len(UUIDS)):
                p = Process(target=init_all, args=(UUIDS[i], mobile_3[i]))
                process_list.append(p)            
            for process in process_list:
                process.start()            
            for process in process_list:
                process.join()            
        else:
            # 一台设备，单进程安装，升级app,设置测试环境，登录云商
            init_all(UUIDS[0], mobile_3[0])
    else:
        raise Exception(f"登录账号数量必须不少于设备数量:{len(mobile_3)}>={len(UUIDS)}")

    init_dev(UUIDS)                
    # 开始录屏
    recorder_list = []
    for i in range(len(UUIDS)):
        adb = ADB(serialno=UUIDS[i])
        recorder = Recorder(adb)
        recorder.start_recording(max_time=1800)
        recorder_list.append(recorder)
        
    pytest.main([
        "-v",
        "--alluredir",
        "reports",
        "testcases",
        "--clean-alluredir",
        "--disable-warnings",
        "--color",
        "yes"
    ])
    
    # 结束录屏
    for i in range(len(UUIDS)):
        recorder_list[i].stop_recording(output=f"logs/{UUIDS[i]}.mp4")
        # 卸载app
        uninstall_all(UUIDS[i])

   