from __future__ import absolute_import, unicode_literals
import os, sys
import numpy as np
import pandas as pd
import math
import re
import matplotlib as mpl
import matplotlib.pyplot as plt


# 在不同层级目录中import模块：http://www.cnitblog.com/seeyeah/archive/2009/03/15/55440.html


# __foo__: 定义的是特殊方法，一般是系统定义名字。
# _foo: 单下划线开头的是protected类型的变量，只允许这个类本身和子类进行访问，不能用于 from module import *。
# __foo: 双下划线开头的是private类型的变量, 只允许这个类本身进行访问。


class Date(object):
	def __init__(self, day=0, month=0, year=0):
		self.day = day
		self.month = month
		self.year = year

	# 类可以不用实例化就可以调用classmethod方法，但是第一个参数必须是cls，这样就实现了Python的重载。
	# 如果写成Date().func()那么是在实例上调用实例方法，如果写成Date.func()那么是在类上调用classmethod方法和staticmethod方法。
	@classmethod
	def from_string(cls, date_as_string):
		day, month, year = map(int, date_as_string.split('-'))
		date1 = cls(day, month, year) # cls是类本身的对象、而不是类的实例对象，这样继承Date的子类对象都会有from_string这个方法。
		return date1 # 也可以return cls。

	# 类可以不用实例化就可以调用staticmethod方法，staticmethod不访问实例对象和它的内部方法。
	# 如果写成Date().func()那么是在实例上调用实例方法，如果写成Date.func()那么是在类上调用classmethod方法和staticmethod方法。
	@staticmethod
	def whether_date_valid(date_as_string):
		day, month, year = map(int, date_as_string.split('-'))
		return day <= 31 and month <= 12 and year <= 3999

class Dates(Date):
	def __init__(self, hour, day, month, year): # 也可以遵循父类的方式写成(self, hour, day=0, month=0, year=0)。
		# Date.__init__(self, day, month, year) # 调用父类方法一
		super(Date, self).__init__() # 调用父类方法二
		self.hour = hour
	def check_hour(self):
		return self.hour

class Stamp(object):
	def __init__(self, stamp1, stamp2):
		self.stamp1 = stamp1
		self.stamp2 = stamp2
	# 如果想在其他的方法中调用staticmethod方法, 那么不要用classname.staticmethod这种类名硬编码(hard coding)，而是在classmethod中调用cls.staticmethod。
	@staticmethod
	def compute1(stamp1):
		return stamp1**3
	@classmethod
	def compute2(cls, stamp1, stamp2):
		return stamp2 * cls.compute1(stamp1)

	def compute(self):
		return self.compute2(self.stamp1, self.stamp2)



class Circle:
	# 面向对象的封装有三种方式：【public】对外完全公开；【protected】对外不公开，但是对友类(friend)或者子类公开；【private】只对内公开。
	# Python没有在语法上把它们三个内建到自己的class机制中，而是通过property方法实现。

	def __init__(self, stamp, value):
		self.stamp = stamp
		self.__Value = value # 将这个数据属性隐藏起来。

	# @property可以把一个实例方法等效成同名属性，把方法的访问转化为属性的访问即.号访问。
	# @property仅有一个self参数，不需要添加()，调用时会触发执行一段功能再返回一些值。虽然area和perimeter等效于属性，但是不能用obj.area和obj.perimeter赋值！
	@property
	def area(self):
		return math.pi*self.stamp**2
	@property
	def perimeter(self):
		return math.pi*self.stamp*2
	
	# @property也可以设置限制和规范：https://www.cnblogs.com/wangyongsong/p/6750454.html, http://python.jobbole.com/81967/, http://python.jobbole.com/80955/?utm_source=blog.jobbole.com&utm_medium=relatedPosts
	# @property对象有3个方法，getter()、setter()、deleter()，用来在对象创建后设置fget、fset、fdel。
	# @property方法有4个参数。第1个是方法名，“对象.属性”时自动触发执行方法；第2个是方法名，“对象.属性＝XXX”时自动触发执行方法；第3个是方法名，“del 对象.属性”时自动触发执行方法；第4个是字符串，“对象.属性.doc”时描述属性的信息。
	@property
	def evaluation(self):
		return self.__Value
	@evaluation.setter
	def evaluation(self, target):
		if not isinstance(target, float):
			raise TypeError("The type of %s is assigned to be 'float'!" %target)
		self.__Value = target # 一旦target能通过类型检查，那么target会覆盖value。
	@evaluation.deleter
	def evaluation(self):
		del self.__Value


# @property的由来和演化：

class Celsius1:
	def __init__(self, temperature=0):
		self.temperature = temperature
	def convert_celsius_fahrenheit(self):
		return (self.temperature * 1.8) + 32

# measure = Celsius()
# measure.temperature = 37
# 类Celsius1的问题是没有对内部变量的约束。解决方案之一是隐藏内部变量的属性，使内部变量私有化，并且定义用于操作属性的get和set接口。

class Celsius2:
	def __init__(self, temperature=0):
		self.set_temperature(temperature)
	def set_temperature(self, value):
		if value < -273:
			raise ValueError("Temperature below -273 is impossible in this universe.")
		self._Temperature = value
	def get_temperature(self):
		return self._Temperature
	def convert_celsius_fahrenheit(self):
		return (self.get_temperature() * 1.8) + 32

# measure = Celsius(37)
# measure.get_temperature()
# measure.set_temperature(25)
# 类Celsius2的问题是缺乏向后兼容性，所有客户都必须更改他们的代码，比如把obj.temperature改为obj.get_temperature()、把obj.temperature=x改为obj.set_temperature(x)等等。

class Celsius:
	def __init__(self, temperature=36):
		self._Temperature = temperature # 将这个数据属性保护起来。
	def convert_celsius_fahrenheit(self):
		return (self.temperature * 1.8) + 32 # self._Temperature

	@property
	def scale(self):
		return self._Temperature
	@scale.setter
	def scale(self, value):
		if value < -273:
			raise ValueError("Temperature below -273 is impossible in this universe.")
		self._Temperature = value
	@scale.deleter
	def scale(self):
		del self._Temperature

# 类Celsius3不定义get_temperature和set_temperature，避免了污染类的命名空间。类Celsius3定义getter和setter时重用了名字temperature或者起名为scale。
# 总之调用property装饰器分3步：1、在init中声明内部变量，2、在@property下声明method（一般返回声明内部变量即可），3、在@method下声明getter()、setter()、deleter()。



if __name__ == "__main__":
	print ("\nOK!\n")
	
	# 如果写成Date().func()那么是在实例上调用实例方法，如果写成Date.func()那么是在类上不实例化直接调用classmethod方法和staticmethod方法。
	whether_date1 = Date.whether_date_valid("11-09-2001") # 其实类可以不用实例化……
	print ("Whether the class is valid is:", whether_date1)
	class_dating1 = Date.from_string("11-09-2001")
	print ("The re-generated class contains: ", class_dating1.day, class_dating1.month, class_dating1.year)

	# classmethod方法和staticmethod方法虽然是给在类上不实例化直接调用的，但是在实例上调用也是可以的，只不过容易让人混淆。
	whether_date2 = Dates.whether_date_valid("17-09-1983") # 其实类可以不用实例化……
	print ("Whether the class is valid is:", whether_date2)
	class_dating2 = Dates("09:09", "17", "09", "1983")
	print ("The hour is:", class_dating2.check_hour())
	# class_dating3 = Dates.from_string("01-10-1949")
	# print ("The re-generated class contains: ", class_dating3.day, class_dating3.month, class_dating3.year)

	# @property可以把一个实例方法变成其同名属性，也可以设置限制和规范。
	class_circle = Circle(10.00, "ego")
	print ("\nThe circle contains:", class_circle.stamp, class_circle.area, class_circle.perimeter)
	print ("The circle shows {} with type {}.".format(class_circle.evaluation, type(class_circle.evaluation)))
	class_circle.evaluation = 20.00 # 调用setter赋值。
	print ("The circle shows {} with type {}.".format(class_circle.evaluation, type(class_circle.evaluation)))
	del class_circle.evaluation # 调用deleter删除。

	class_measure = Celsius()
	class_measure.temperature = 37
	print ("The temperature converted from %d yields %d." %(class_measure.temperature, class_measure.convert_celsius_fahrenheit()))
	class_measure.temperature = 100
	print ("The temperature converted from %d yields %d." %(class_measure.temperature, class_measure.convert_celsius_fahrenheit()))
	del class_measure.temperature

	print ("The circle shows {} with type {}.".format(class_measure.scale, type(class_measure.scale)))
	class_measure.scale = 36.5 # 调用setter赋值。
	print ("The circle shows {} with type {}.".format(class_measure.scale, type(class_measure.scale)))
	del class_measure.scale # 调用deleter删除。

	print ("\nDone!\n")
