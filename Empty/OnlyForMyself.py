from __future__ import absolute_import
import sys, argparse
import logging
from autologging import logged
import os.path
import time


# __foo__: 定义的是特殊方法，一般是系统定义名字。
# _foo: 单下划线开头的是protected类型的变量，只允许这个类本身和子类进行访问，不能用于 from module import *。
# __foo: 双下划线开头的是private类型的变量, 只允许这个类本身进行访问。


@logged(logging.getLogger("Empty.OnlyForMyself"))

class Shopping():
	def __init__(self, year=0, month=0, day=0):
		self.day = day
		self.month = month
		self.year = year
		self.__log.info("I only shop for myself, never for my girlfriend.")
		self.error_mark = "Error"

	def approach0(self):
		self.__log.debug("I shop for my parents as they do too.")
		return str(self.year)+'/'+str(self.month)+'/'+str(self.day)
	def _approach1(self):
		self.__log.warning("Shopping is good for our health.")
		return "Shopping is good for our health."
	def __approach2(self):
		self.__log.error("Health is good for our shopping.")
		return "Health is good for our shopping."
