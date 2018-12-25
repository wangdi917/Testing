from __future__ import absolute_import, unicode_literals
import os, sys
import numpy as np
import pandas as pd
import math
import re
import matplotlib as mpl
import matplotlib.pyplot as plt

from collections import namedtuple


# Pandas中主要有两种数据结构：Series和DataFrame。 Series可以使用单独的数字来索引；Dataframe必须使用Python的slice对象形式来索引！
# Series类似于一维数组，由一组数据以及一组与之相关的数据标签(即索引)组成。仅由一组数据也可产生简单的Series对象。注意：Series中的索引值是可以重复的！
# DataFrame类似于一个表格型的数据结构，包含有一组有序的列，每列可以是不同的值类型。DataFrame既有行索引也有列索引，可以被看做是由Series组成的字典。
# 打印Pandas中的Series和DataFrame数据结构，永远都会带着行或者列的索引。


def data_series():
	# 通过一维数组创建series。
	array_np = np.array([1, 3, 5, np.NaN, 10])
	series1 = pd.Series(array_np)
	print ("\nThe series created from an array is:\n{}\nIts type is: {}, indices are: {}, and values are: {}.".format(series1, series1.dtype, series1.index, series1.values))

	# 通过字典创建series。字典的key为series的索引，字典的values为series的元素。
	dict_example = {'Maths':99, 'Chinese':98, 'English':97}
	series2 = pd.Series(dict_example)
	print ("\nThe series created from a dictionary is:\n{}\n".format(series2))

	# 通过字典创建series。字典的key为series的索引，字典的values为series的元素。
	series3 = pd.Series(data=[99,98,97], dtype=np.float64, index=['Maths','Chinese','English'])
	print ("\nThe series created from an appointment is:\n{}\n".format(series3))
	
	# 通过截取dataframe创建series。
	df = pd.DataFrame(np.arange(6).reshape((3,2)), index=list(("John","Jack","Jane")), columns=['abc','ooo'])
	'''
			abc  ooo
	John     0    1
	Jack     2    3
	Jane     4    5
	'''
	series4 = df['ooo']; series5 = df['abc']
	series4[:] = 100; series5 = series4+series5
	'''
	John    100
	Jack    102
	Jane    104
	'''
	print ("\nThe series created from a copy is:\n{}\n".format(series5))
	series6 = pd.Series([True, False, True, False])
	print ("\nThe series created from an expression is:\n{}\n".format(series6))
	# 0    True
	# 1    False
	# 2    True
	# 3    False
	print ("\nThe series created from an expression of expression is:\n{}\n".format(series6[series6]))
	# 0    True
	# 2    True


def data_frame():
	df = pd.DataFrame(np.arange(20).reshape((4,5)), index=list(range(4)), columns=['a','b','c','d','ooo'])
	print (df.values) # 剥去行和列的索引，显示成一个4*5的二维数组。
	# dtype查看每个列的数据类型，index查看行索引及其数据类型，columns查看列索引及其数据类型，values以数组形式返回DataFrame的值（避免索引），describe显示数据的总结信息，transpose转置。
	'''
	    a   b   c   d  ooo
	0   0   1   2   3    4
	1   5   6   7   8    9
	2  10  11  12  13   14
	3  15  16  17  18   19
	'''

	# https://blog.csdn.net/ls13552912394/article/details/79349809
	# print ("\nThe outcome of 'df[0]' is:\n{}".format(df[0]))
	print ("\nThe outcome of 'df[0:1]' is:\n{}".format(df[0:1]))
	print ("\nThe outcome of 'df['a']' is:\n{}".format(df['a']))
	print ("\nThe outcome of 'df[['a','b']]' is:\n{}".format(df[['a','b']]))
	print ("\nThe outcome of 'df.iat[1,1]' is:\n{}".format(df.iat[1,1]))
	# 如果要交换两列，直接交换是错误的。因为pandas默认在赋值的时候会匹配列名，所以AB和BA实际上没有区别。
	df.loc[:,['b','a']] = df[['a','b']]
	# 如果要交换两列，应该使用AB两列的值.values作为右值，这样就不带列索引名了。
	df.loc[:,['b','a']] = df[['a','b']].values

	# https://www.cnblogs.com/hhh5460/p/5595616.html
	# loc索引的开闭区间机制和Python的左闭右开不同，而是类似于MatLab的双侧闭区间。索引指的是标签而不是位置，比如1表示标签是1。 iloc索引的开闭区间机制和Python的左闭右开。索引指的是位置而不是标签，比如1表示第2。
	# 如果loc和iloc方括号中直接给定一个数字或者一个slice的话，默认索引的是行，而不能是列，返回一个大小等于列大小的Series。
	print ("\nThe outcome of 'df.loc[1]' is:\n{}".format(df.loc[1]))
	print ("\nThe outcome of 'df.iloc[1]' is:\n{}".format(df.iloc[1]))
	print ("\nThe outcome of 'df.loc[:,['c']]' is:\n{}".format(df.loc[:,['c']])) # 用loc指定列时，必须直接指定列的标签！
	print ("\nThe outcome of 'df.iloc[:,[1]]' is:\n{}".format(df.iloc[:,[1]])) # 用iloc指定列时，必须直接指定列的位置！
	# loc/iloc是基于标签的（行可以接受boolean索引）。
	print ("\nThe outcome of 'df.loc[0:1]' is:\n{}".format(df.loc[0:1]))
	print ("\nThe outcome of 'df.loc[1:3,'a':'c']' is:\n{}".format(df.loc[1:3,'a':'c']))
	print ("\nThe outcome of 'df.loc[1]>=6' is:\n{}".format(df.loc[1]>=6)) # 判断索引是1的那一行，返回一个大小等于行大小的Series。
	print ("\nThe outcome of 'df.loc[:,df.loc[1]>=6]' is:\n{}".format(df.loc[:,df.loc[1]>=6]))
	print ("\nThe outcome of 'df.loc[:,'a']>=9' is:\n{}".format(df.loc[:,'a']>=9)) # 判断索引是a的那一列，返回一个大小等于列大小的Series。
	print ("\nThe outcome of 'df.loc[df.loc[:,'a']>=9]' is:\n{}".format(df.loc[df.loc[:,'a']>=9]))

	def df_loop(df):
		matrix = []
		for index, row in df.iterrows():
			for col in df.columns:
				matrix.append(row[col])
				# print ("The point is: {}".format(row[col]))
			return matrix
	print ("\nThe outcome of looping is:\n{}".format(df_loop(df)))

	def df_iterate(df, cols=None): # 这相当于实现了pd.DataFrame.itertuples，遍历使用for row in df_iterate(df)，但是效率更高。
		if cols is None:
			cols = df.columns.values.tolist()
			matrix = df.values.tolist()
		else:
			cols_indices = [df.columns.get_loc(c) for c in cols]
			matrix = df.values[:, cols_indices].tolist()
		tuple_named = namedtuple('tupling', cols)
		for line in iter(matrix): # 用iter()函数构造迭代器，让构造出来的迭代器对象可以使用next()函数。
			# print ("\nAt this round the line is:\n{}".format(line))
			yield tuple_named(*line)
	# 必须用list()函数将构造出来的tuple迭代器对象[tupling(a=1,b=0,c=2,d=3,ooo=4), ...]转化成数组模式。
	print ("\nThe outcome of iteration is:\n{}".format(list(df_iterate(df))))
	print ("The selected elements of iteration are: {} and {}".format(list(df_iterate(df))[0][:], [getattr(row, 'ooo') for row in df_iterate(df)]))


# Json格式转换：https://blog.csdn.net/data_ada/article/details/72779559

def data_re():
	dict_rule = {'L5':["[^没|^偶尔]有","[^没有|^偶尔]用过"], 'L3':["有时","偶尔","一点"], 'L1':["没有",'']}
	text1Y = "我有用过"; text1O = "我偶尔用过"; text1N = "我没有用过";
	list1 = [text1Y, text1O, text1N]
	for level, rules in dict_rule.items():
		accumulation = [0]*len(list1)
		for rule in rules:
			# Python3的map()函数返回类型为iterators，不再是list！
			# 字典如何根据value值取对应的key值：list(dict_rule.keys())[list(dict_rule.values()).index("001")]
			# 同时在[text1Y, text1O, text1N]中分别逐一匹配L5、L3、L1。正则匹配只能在字符串之间进行，不能直接列表匹配列表，所以必须循环rules，但是可以用map避免循环list1。
			whether_match = list(map(lambda x: len(re.findall(rule, x)) * int(level[-1]), list1))
			print ("When the Regular Expression is {} and when matching the text '我有用过^ 我偶尔用过^ 我没有用过^' to rule '{}', the result is\n{}".format(rules, rule, whether_match))
			# 如果同时匹配了L_low和L_high，那么最终让结果是L_high。
			accumulation = list(map(lambda x: max(x[0],x[1]), zip(accumulation, whether_match))) # sum = [a+b for a, b in zip(l1,l2)] 甚至 map(lambda x: x[0]|x[1], zip(list1, list2)
			print ("So the accumulation and overwriting of high-level over low-lever lists is {}\n".format(accumulation))
	series1 = pd.Series(np.array([text1Y, text1O, text1N]))
	series1 = series1.astype(str)
	for rules in dict_rule.values():
		for rule in rules:
			whether_match = series1.apply(lambda x: len(re.findall(rule, x))>0)
			print ("\nWhen the Regular Expression is {}, the matching result is\n{}".format(rules, whether_match))

'''
def data_const():
	import const # 这是一个文件。
	class_shit = const.Const()
	class_shit.TEST_CONSTANT = 'test'
'''



if __name__ == "__main__":
	# *args表示任何多个无名参数，它是一个tuple或list；**kwargs表示关键字参数，它是一个dict。同时使用*args和**kwargs时，*args必须要在**kwargs前。
	# pragma: no cover
	print ("\nOK!\n")
	# data_series()
	# data_frame()
	data_re()
	# data_const()

	d = {'Name': 'Runoob', 'Age': 27}
	print ("\nSex:%s" %(d.get('Sex', 100) or 1))
	print ("\nPorn:%d" %(2 or 1))

	print ("\nDone!\n")
