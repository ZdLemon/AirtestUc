# coding:utf-8

__author__ = "ligeit"

import logging
import re
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.utils.apkparser import APK
from airtest.core.android.adb import ADB
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from setting import PACKAGE, mobile_3, DEV, UUIDS
from utils.logger import logger
import allure
from setting import PACKAGE

mobile_3 = "15876361823"
serialno = "000003f70f0d364e"
adb_path = ADB.builtin_adb_path()

adb = ADB(adb_path=adb_path, serialno=serialno)

out = adb.shell("dumpsys activity")
# out = adb.shell(f"ps -A | findstr {PACKAGE}")

logger.info(out)

