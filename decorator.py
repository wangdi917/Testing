import os

# https://www.cnblogs.com/zh605929205/p/7704902.html

'''
当用@来修饰某个函数func时，
@decorator
def func():
    pass
解释器会解释成func = decorator(func)，这其实就是把一个函数当参数传到另一个函数中然后再回调。但是，由于赋值语句的存在，把decorator这个函数的返回值赋值又赋给了原来的func。
这是因为函数可以被当成变量来使用，所以decorator函数必须返回一个函数出来给func，这就是所谓的higher order function高阶函数。
'''

def greet(func): # 这里的输入是函数！
	def wrapper(): # 这里的输入是变量！
		print ("The function has been accepted here.")
		func() # 这里执行了输入的函数。
		print ("The function has been released here.")
		# return func()
	return wrapper # wrapper函数能够接受任意数量和类型的参数，并把它们回调给被包装的方法，这样我们可以用这个装饰器来装饰任何方法。

@greet
def foo0():
	print ("I have been fooled...")


def globe(func): # 这里的输入是函数！
	def wrapper(*args, **kwargs): # 这里的输入是变量！
		print ("\nArguments 'args' %s and 'kwargs' %s have been accepted by %s." %(args, kwargs, func.__name__))
		return func(*args, **kwargs) # 这里执行了输入的函数。
	return wrapper # wrapper函数能够接受任意数量和类型的参数，并把它们回调给被包装的方法，这样我们可以用这个装饰器来装饰任何方法。

@globe
def foo1(x, y=1): # 这里foo1对应了func和wrapper。
	return x * y

@globe
def foo2(): # 这里foo2对应了func和wrapper。
	return 99



if __name__ == "__main__":
	print ("\nThe current directory is {}.\n".format(os.path.dirname(os.getcwd())))
	foo0()

	# foo1(5, 4)
	print ("Calling the foo1 function yields {}.".format(foo1(5, 4))) # 20
	# foo1(1)
	print ("Calling the foo1 function yields {}.".format(foo1(1))) # 1
	# foo2()
	print ("Calling the foo2 function yields {}.".format(foo2())) # 99
