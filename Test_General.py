from __future__ import absolute_import, unicode_literals
import os, sys
import numpy as np
import pandas as pd
import math
import re
import matplotlib as mpl
import matplotlib.pyplot as plt

# 在不同层级目录import模块的方法 http://www.cnitblog.com/seeyeah/archive/2009/03/15/55440.html

from Empty.Nonsense import this_is_a_function
from Empty.Nonsense import This_is_a_class
import Empty.Bullshit # 这是一个文件。
from Empty import Fiddledeedee # 这是一个文件。


def regular():
	# https://www.cnblogs.com/tina-python/p/5508402.html, https://www.cnblogs.com/papapython/p/7482349.html
	# *匹配前一个字符0或多次。+匹配前一个字符1次或无限次。?匹配一个字符0次或1次。
	# ^匹配字符串开头，比如^abc匹配abc。$匹配字符串结尾，比如abc$匹配abc。
	# |匹配左右表达式任意一个，从左到右匹配，如果|没有被放在()中那么它的范围是整个正则表达式，比如abc|def匹配abc。
	# {m}匹配前一个字符m次，{m,n}匹配前一个字符m至n次，{m,}匹配前一个字符m至无限次，比如ab{1,2}c匹配abc和abbc。
	# []字符集中的任意字符，比如[abc]或[a-c]表示abc中的某个，[^abc]表示取反即非abc中的某个。所有特殊字符在[]中都失去其原有的特殊含义，可以用\反斜杠转义恢复特殊字符的特殊含义。比如a[bcd]e匹配abe、ace、ade。
	# ()被放在()中的表达式将作为分组，从表达式左边开始，每遇到一个左括号(就编号+1。分组表达式作为一个整体，可以后接数量词。表达式中的|仅在该组中有效。比如(abc){2}匹配abcabc，a(123|456)c匹配a456c。
	# \w匹配包括下划线在内的任何字字符:[A-Za-z0-9_]，比如a\wc匹配abc。
	# \W匹配非字母的特殊字符，比如a\Wc匹配a c。

	# 用compile生成一个正则表达式，返回一个模式对象。然后用findall查找某一个对象。匹配模式有：re.I(re.IGNORECASE)忽略大小写，re.M(MULTILINE)多行模式，re.S(DOTALL)点任意匹配模式。
	text1 = "Who are you, what do you do, when and where?"
	regex1 = re.compile(r"\w*wh\w*", re.IGNORECASE)
	wh = regex1.findall(text1)
	print ("\nThe finding result of the regular expression is: {}.".format(wh))	# ['Who', 'what', 'when', 'where']
	
	# match如果查找到结果，会返回一个MatchObject。MatchObject实例也有几个方法和属性：group()返回被RE匹配的字符串，start()返回匹配开始的位置，end()返回匹配结束的位置，span() 返回一个元组包含匹配 (开始,结束) 的位置。
	text2 = "What are you doing? who is your mate?"
	regex2 = re.compile("\w*wh\w*", re.I)
	wh = regex2.match(text2)
	if wh:
		print ("\nThe matching result of the regular expression is: {}, {}, {}, {}.".format(wh.group(), wh.start(), wh.end(), wh.span()))
	else:
		print ("\nNothing has been matched.")


def logic():
	# and从左到右计算表达式。如果所有值均为真，那么返回最后一个真值；如果存在假值，那么返回第一个假值。
	# or从左到右计算表达式。如果所有值均为假，那么返回最后一个假值；如果存在真值，返回第一个真值。
	print ("\n")
	x, y, z = "x", "y", ""
	print ("The result of '1 and x' is: ", 1 and x)
	print ("The result of 'none or y' is: ", None or y)
	print ("The result of 'z or none' is: ", z or None)
	print ("The result of '1 and x or y' is: ", 1 and x or y)
	print ("The result of '(1 and [x] or [y])[0]' is: ", (1 and [x] or [y])[0]) # 安全用法，因为[x]一定为真、一定至少有一个元素。


def arrays():
	print ("\n")

	# 指数函数y=a^x，指数x是自变量。幂函数y=x^a，幂x是自变量。
	list_dummy = [0, 1, 2, 3, 4]
	list_char = ['0', '1', '2', '3', '4']
	print ("The augmented list is:", list_dummy*2)
	matrix_fake = [list_dummy*3] # 仅仅创建3个指向list的引用，不是一个真正的list of lists！所以一旦list改变，matrix中的3个list也会一齐随之改变。
	matrix_real = [[10 for i in range(3)] for i in range(3)]
	print ("The augmented matrix is:", matrix_real)
	maxima = max( (-i, math.pow(i, 0.5)) for i in list_dummy ) # 这样形成一个list of tuples。先比较tuple的第一个元素，再比较其余元素。
	print ("The maxima among {} is {}.".format(list_dummy, maxima))

	# NumPy大纲：https://www.cnblogs.com/keepgoingon/p/7137448.html
	array_dummy = np.array(list_dummy, dtype=np.float16) # 创建float数组。
	print ("The array of floats is:", array_dummy.dtype, array_dummy)
	array_char = np.array(list_char, dtype=np.int64) # 创建int数组。
	print ("The array of chars is:", array_char.dtype, array_char)
	array_char = np.array(list_char, dtype=np.string_) # 创建string数组。
	print ("The array of chars is:", array_char.dtype, array_char)

	# astype()对ndarray类型对象做强制类型转换，但是原始ndarray类型对象不变、一个新的ndarray类型对象会被创建。
	array_char.astype(float)
	print ("The unconverted array of chars is:", array_char.dtype, array_char)
	array_chars = array_char.astype(float)
	print ("The converted array of chars is:", array_chars.dtype, array_chars)
	# ndarray类型对象直接操作里面的元素，语法和对标量元素的操作一样，比如ndarray**2和ndarray1+ndarray2，但是操作不能是函数形式比如exp(ndarray)或log(ndarray)！
	print ("The powered array is:", array_chars**2)

	cubic_empty = np.empty((2,3,4)) # 创建2*3*4全空三维数组。
	cubic_one = np.ones((2,3,4), dtype=np.int16) # 创建2*3*4全1三维数组。
	cubic_one = np.ones((2,3,4), dtype='int16') # 创建2*3*4全1三维数组。


def loop():
	print ("\n")

	# range用于循环整数，range(0,5)返回一个range类型对象、而不是list类型对象[0,1,2,3,4]！如想返回一个list需要用list转换。
	print ("The range is:", range(-1,8))
	list_range = [i**2 for i in range(-1,8,2)]
	print ("The converted range is:", list_range)

	# arange是numpy模块中的函数，arange(3)返回一个array类型对象。可以指定步长。
	print ("The arange is:", np.arange(-1, 1, 0.4))
	list_arange = [i*1 for i in np.arange(-1, 1, 0.4)]
	print ("The converted arange is:", list_arange)

	# linspace是numpy模块中的函数，arange(3)返回一个array类型对象。可以指定个数。
	print ("The linspace is:", np.linspace(10, 20, 5))
	list_linspace = list(np.linspace(10, 20, 5))
	print ("The converted linspace is:", list_linspace)

	def power2(x):
		return x*x
	list_mapped1 = map(power2, [1, 2, 3, 4, 5, 6, 7])
	print ("The mapped list is: ", list(list_mapped1))
	# Python可以处理类列表长度不一致的情况，但是无法处理列表元素类型不一致的情况。
	list_mapped2 = map(lambda x,y: (x**y, x+y), [1,2,3,4], [1,2,3])
	print ("The forced list is: ", list(list_mapped2))
	# Python可以用map做类型转换。
	list_mapped3 = map(int, "1234")
	print ("The converted list is: ", list(list_mapped3))



if __name__ == "__main__":
	# *args表示任何多个无名参数，它是一个tuple或list；**kwargs表示关键字参数，它是一个dict。同时使用*args和**kwargs时，*args必须要在**kwargs前。
	# pragma: no cover
	print ("\nOK!\n")
	regular()
	# logic()
	arrays()
	# loop()

	result1 = this_is_a_function()
	result2 = this_is_a_function(3)
	print ("\nBy importing the 'this_is_a_function' function in the file, the results are %d and %d." %(result1, result2))
	class_shit1 = This_is_a_class() # 也可以(year=1983, month=9, day=17)或者(1983, 9, 17)或者(1983)。
	result3 = class_shit1.this_is_a_method() # 必须实例化的类class_shit。
	result4 = class_shit1._approach1()
	print ("By importing the 'this_is_a_method' function in the file, the results are %s and %s" %(result3, result4))

	class_shit2 = Empty.Bullshit.This_is_a_class() # 也可以(year=1983, month=9, day=17)或者(1983, 9, 17)或者(1983)。
	result3 = class_shit2.this_is_a_method() # 必须实例化的类class_shit。
	result4 = class_shit2._approach1()
	print ("By importing the 'this_is_a_method' function in the file, the results are %s and %s" %(result3, result4))

	class_shit3 = Fiddledeedee.This_is_a_class() # 也可以(year=1983, month=9, day=17)或者(1983, 9, 17)或者(1983)。
	result3 = class_shit3.this_is_a_method() # 必须实例化的类class_shit。
	result4 = "class_shit3.__approach2()"
	print ("By importing the 'this_is_a_method' function in the file, the results are %s and %s" %(result3, result4))

	print ("\nDone!\n")
