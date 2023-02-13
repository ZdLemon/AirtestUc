# coding: utf-8

import pytest
import re
import os
import allure
from utils.logger import logger
from airtest.core.api import *
from airtest.core.helper import set_logdir
from airtest.report.report import LogToHtml
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from utils.to_home import to_home
from setting import PACKAGE, UUIDS

UUID = ""
FILE = ""
DIRPATH = ""


def pytest_runtest_setup(item):
    
    # 设置链接的设备
    global UUID
    try:
        restr = re.search(r"testclass\.test_\d+\[(.+)\]", item.__dict__['location'][2], re.I)
        uuid = restr.group(1)
        set_current(uuid) 
        UUID = uuid
    except AttributeError as e:
        raise AttributeError(f"缺失uuid：{e}")

    global FILE, DIRPATH
    # 获取函数所在文件地址
    location = item.__dict__["location"]
    file = location[0]
    file = os.path.abspath(file)
    FILE = file
    # 组装测试用例报告，日志存储文件夹
    if file.find("testcases_app") == -1:
        raise Exception("测试用例文件夹错误！！")
    p1 = file.replace("testcases_app", "logs")
    p1 = p1.replace(".py", "")
    p2 = location[2].replace("TestClass.", "")
    p2 = p2.replace("[", "\\")[:-1]
    dirpath = os.path.join(p1, p2)
    DIRPATH = dirpath

    # 组装报告文件路径
    reportpath = re.match(r".+:(\\.+)+(\\.+\.py)$", file)
    reportpath = reportpath.group(2).replace("py", r"log\log.html")
    reportpath = dirpath + reportpath
    allure.dynamic.link(reportpath)

    # 文件已存在则清空
    if os.path.exists(dirpath):
        for path in os.listdir(dirpath):
            if os.path.isfile(os.path.join(dirpath, path)):
                os.remove(os.path.join(dirpath, path))
    # 文件不存在则新建
    else:
        os.makedirs(dirpath)
        
    set_logdir(dirpath)
    log(f"setup {uuid}", snapshot=True)    


def pytest_runtest_call(item):
    log(f"执行用例 {UUID}", snapshot=True)


def pytest_runtest_teardown(item):
    
    global FILE, DIRPATH
    file = FILE
    dirpath = DIRPATH
    log(f"teardown {UUID}", snapshot=True)  
            
    LogToHtml(
        script_root=file, 
        log_root= dirpath,
        export_dir= dirpath, 
        logfile= os.path.join(dirpath, "log.txt"),
        lang="en", 
        plugins=["poco.utils.airtest.report"],
    ).report() 


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    out = yield

    report = out.get_result()
    
    if report.__dict__["outcome"] == "failed" and report.__dict__["longrepr"].__dict__["reprcrash"].__dict__["message"].find("poco.exceptions.PocoNoSuchNodeException") != -1:
        log(report.__dict__["longrepr"].__dict__["reprtraceback"], desc="poco.exceptions.PocoNoSuchNodeException", snapshot=True)


@allure.title("关闭app")
@pytest.fixture(scope="session")
def stop_app():
   
    yield 
    for uuid in UUIDS:
        set_current(uuid)
        stop_app(PACKAGE)
        clear_app(PACKAGE)
        uninstall(PACKAGE)

  
@allure.title("app首页")
@pytest.fixture(scope="class", autouse=True)
def to_app_home():

    for uuid in UUIDS:
        set_current(uuid)
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        try:
            # 进入APP首页
            while poco(nameMatches="^首页\n.+").exists() is False:         
                poco(name="android.view.View", touchable=True).wait(1).click() 
        except Exception as e:
            to_home(poco)
            raise e
    yield
    
    for uuid in UUIDS:
        set_current(uuid)
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        try:
            # 进入APP首页
            while poco(nameMatches="^首页\n.+").exists() is False:         
                poco(name="android.view.View", touchable=True).wait(1).click() 
        except Exception as e:
            to_home(poco)
            raise e


