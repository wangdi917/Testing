import math


# __foo__: 定义的是特殊方法，一般是系统定义名字。
# _foo: 单下划线开头的是protected类型的变量，只允许这个类本身和子类进行访问，不能用于 from module import *。
# __foo: 双下划线开头的是private类型的变量, 只允许这个类本身进行访问。


def this_is_a_function(value=1):
		return math.pow(value, value)

class This_is_a_class(object):
	def __init__(self, year=0, month=0, day=0):
		self.day = day
		self.month = month
		self.year = year
	def this_is_a_method(self):
		return str(self.year)+'/'+str(self.month)+'/'+str(self.day)
	def _approach1(self):
		return "Sex is good for our health."
	def __approach2(self):
		return "Health is good for our sex."