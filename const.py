import sys

class Const(object):
	class ConstError(TypeError):
		pass

	def __setattr__(self, key, value):
		if key in self.__dict__:
			raise self.ConstError # "Changing const.%s" %key
		else:
			self.__dict__[key] = value

	def __getattr__(self, key):
		if key in self.__dict__:
			return self.key
		else:
			return None

# 在Python中实现常量的定义：https://www.cnblogs.com/Vito2008/p/5006255.html, http://www.cnblogs.com/current/p/4252516.html


sys.modules[__name__] = Const()