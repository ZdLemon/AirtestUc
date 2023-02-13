# coding:utf-8

__author__ = "hewei"

from airtest.core.api import *
from airtest.core.android.android import *
from setting import PACKAGE


def to_home(poco):

    # 关闭，打开APP
    stop_app(PACKAGE)
    sleep(1)
    start_app(PACKAGE)
    
    count = 0
    nodes = 0
    while count < 3 and nodes < 3:
        # 隐私协议
        if poco("我同意").exists():
            poco("我同意").click()
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
                count = 3
    
    assert_equal(poco(nameMatches="^首页\n.+").exists(), True, msg="首页可点击")

