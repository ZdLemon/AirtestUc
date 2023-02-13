# coding:utf-8


from functools import wraps
from airtest.core.api import *
from setting import TESTCASES
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import os
import allure


def log_report():
    """
    每条用例生成独立的airtest报告
    """
    def decorate(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            from airtest.core.helper import set_logdir
            from airtest.report.report import LogToHtml
            
            # 获取函数所在文件地址
            file = os.path.normcase(func.__code__.co_filename)
            # 组装测试用例报告，日志存储文件夹
            dirpath = os.path.join(os.path.splitext(os.path.abspath(file).replace(TESTCASES, 'logs'))[0], func.__name__)
            dirpath = os.path.join(dirpath, "WQCDU19C03004911")
            # 文件已存在则清空
            if os.path.exists(dirpath):
                for path in os.listdir(dirpath):
                    if os.path.isfile(os.path.join(dirpath, path)):
                        os.remove(os.path.join(dirpath, path))
            # 文件不存在则新建
            else:
                os.makedirs(dirpath)
                            
            set_logdir(dirpath)
            try:
                allure.dynamic.link(url=os.path.join(dirpath, os.path.join(os.path.basename(func.__code__.co_filename).replace('.py', '.log'), 'log.html')).lower())
                func(*args, **kwargs)               
            except AttributeError as e:
                raise e
            except AssertionError as e:
                raise e
            except Exception as e:
                assert_is_none(e, msg="UI Node 错误")
            finally:              
                LogToHtml(
                    script_root=file, 
                    log_root= dirpath, 
                    export_dir= dirpath, 
                    logfile= os.path.join(dirpath, "log.txt"),
                    lang="en", 
                    plugins=["poco.utils.airtest.report"]
                ).report()    
                           
        return wrapper
    return decorate

