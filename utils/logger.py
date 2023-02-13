# coding:utf-8

from loguru import logger
import sys

from setting import LEVEL


logger.remove()
logger.add(sys.stderr, level=LEVEL)