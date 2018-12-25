from __future__ import absolute_import
import sys, argparse
import logging
from autologging import logged
import os.path
import time
# import ConfigParser
import configparser as ConfigParser
import string

from Empty import OnlyForMyself # 这是一个文件。


# https://blog.csdn.net/lis_12/article/details/54618868
# https://blog.csdn.net/guoyajie1990/article/details/76739977

def cmd():
	parser = argparse.ArgumentParser(description="What else can I do?")

	# 运行时必须指定echo和square，比如python Test_Log.py foo 10 9 8 7 -vvvv --sum、或者python Test_Log.py -h调用帮助。
	parser.add_argument("echo", help="Echo the argument string.", choices=['foo', 'shit'])
	parser.add_argument("square", help="Display the square of a given number.", type=int, choices=range(1, 11)) # argparse会将输入当作字符串处理，所以需要重新设置它的类型。
	parser.add_argument("-v", "--verbosity", action='count', default=0, help="Increase the output verbosity.") # 因为count，-vvvv认为v出现了4次、 -v -s -v认为v出现了2次。
	parser.add_argument("integers", metavar='N', type=int, nargs='+', help="Assign an integer for the accumulator.")
	parser.add_argument("-s", "--sum", dest='add_some_integers', action='store_const', const=sum, default=max, help="Sum the integers.") # 用const指定正常function，用default指定无"-s"或"--sum"时默认function。
	args = parser.parse_args()

	print ("Now 'args.echo' has been assigned as {}.".format(args.echo))
	print ("Now 'args.square' has been assigned as {}.".format(args.square**2))
	print ("By giving '-s' or '--sum' in the arguments, the customized function 'args.add_some_integers' yields {}.".format(args.add_some_integers(args.integers)))
	print ("\nAll in all are: {}.\n".format(args))
	FLAGS, unparsed = parser.parse_known_args()
	print ("So 'FLAGS' contains '%s' where its 'echo' is '%s'." %(FLAGS, FLAGS.echo))
	print ("So 'unparsed' contains '%s'." %unparsed)


# https://www.cnblogs.com/CJOKER/p/8295272.html
# https://blog.csdn.net/xsj_blog/article/details/51971964
# http://sinhub.cn/2018/02/logging-the-aesthetics-of-soc/
# Logger是Logging模块的主体，主要工作是：为程序提供记录日志的接口，判断日志所处级别并判断是否要过滤，根据其日志级别将该条日志分发给不同handler。
# Logger的用法有：Logger.setLevel()：设置日志级别，Logger.addHandler()和Logger.removeHandler()：添加和删除一个Handler，Logger.addFilter()：添加一个Filter用作过滤，
# Handler基于日志级别对日志进行分发，默认的级别顺序是critical > error > warning > info > debug，比如设置为warning级别的Handler只会处理warning及以上级别的日志。

def log1():
	logging.basicConfig(level=logging.NOTSET)
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	timestamp = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
	log_file = os.getcwd() + '/message' + timestamp + '.log'
	filesave = logging.FileHandler(log_file, mode='w')
	filesave.setLevel(logging.DEBUG)
	formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
	filesave.setFormatter(formatter)
	logger.addHandler(filesave)

	# 如果只设置logging.basicConfig()就logger，那么只把日志写入到控制台。
	logger.debug("Here is a loggging debug message.")
	logger.info("Here is a loggging info message.")
	logger.warning("Here is a loggging warning message.")
	logger.error("Here is a loggging error message.")
	logger.critical("Here is a loggging critical message.")

def log2():
	logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s", 
					datefmt='%Y-%b-%d, %a, %H:%M:%S', filename='message.log', filemode='w')
	# 只要插入一个handler输出到控制台，就可以同时把日志写入到文件和控制台。
	console = logging.StreamHandler()
	console.setLevel(logging.WARNING)
	formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
	console.setFormatter(formatter)
	logging.getLogger('').addHandler(console)

	logging.debug("This is a loggging debug message.")
	logging.info("This is a loggging info message.")
	logging.warning("This is a loggging warning message.")
	logging.error("This is a loggging error message.")
	logging.critical("This is a loggging critical message.")

def log3(logfile, loglevel):
	logging.basicConfig(level=loglevel, format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s", 
					datefmt='%Y-%b%d-%H:%M:%S', filename=logfile, filemode='w')
	# 只要插入一个handler输出到控制台，就可以同时把日志写入到文件和控制台。
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
	console.setFormatter(formatter)
	logging.getLogger('').addHandler(console)

def log_backroll():
	formatter = logging.Formatter("%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s")
	# S表示秒，M表示分，H表示时，D表示天，W表示工作日，midnight表示Roll over at midnight，interval表示每多少个时间单位产生一个日志文件，backupCount表示日志文件的保留个数。
	log_file_handler = TimedRotatingFileHandler(filename="ds_update", when="M", interval=2, backupCount=2)
	# log_file_handler.suffix = "%Y-%m-%d_%H-%M.log"
	# log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")
	log_file_handler.setFormatter(formatter)
	logging.basicConfig(level=logging.INFO)
	log = logging.getLogger()
	log.addHandler(log_file_handler)

	# 循环打印日志
	log_content = "Testing the log."
	count = 0
	while count < 30:
		log.error(log_content)
		time.sleep(20)
		count = count + 1
	log.removeHandler(log_file_handler)

@logged(logging.getLogger("Test_Log"))

class Blogging():
	def __init__(self, year=0, month=0, day=0):
		self.day = day
		self.month = month
		self.year = year
		self.__log.info("I only blog for myself, yet sometimes for others.")
	def approach0(self):
		self.__log.debug("I blog all the moments between me and my parents.")
		return str(self.year)+'/'+str(self.month)+'/'+str(self.day)
	def _approach1(self):
		self.__log.warning("Blog is good for our health.")
		return "Blog is good for our health."
	def __approach2(self):
		self.__log.error("Health is good for our blog.")
		return "Health is good for our blog."


# https://blog.csdn.net/miner_k/article/details/77857292
# https://www.cnblogs.com/shellshell/p/6947049.html

def config1():
	config = ConfigParser.RawConfigParser()
	config.add_section('Section1')
	config.set('Section1', 'an_int', '100')
	config.set('Section1', 'a_float', '3.1415')
	config.set('Section1', 'a_bool', 'true')
	config.set('Section1', 'baz', 'fun')
	config.set('Section1', 'bar', 'Python')
	config.set('Section1', 'foo', '%(bar)s is %(baz)s!')
	with open("settings.ini", 'w') as configfile:
		config.write(configfile)

	config = ConfigParser.RawConfigParser()
	config.read("settings.ini")
	an_int = config.getint('Section1', 'an_int')
	a_float = config.getfloat('Section1', 'a_float')
	print ("\nBy reading from the config, foo yields {}.".format(config.get('Section1', 'foo')))
	return foo

def config2():
	config = ConfigParser.ConfigParser()
	config.read("settings.ini")
	blank = config.get('data', 'data_path')
	log_path = config.get('log', 'log_path')
	log_file = config.get('log', 'log_file')
	log_levels = config.get('log', 'log_level')
	log_target = os.path.dirname(os.getcwd()) + log_path + log_file + blank
	if os.path.exists(log_target):
		print ("The config file {} is valid.\n".format(log_target))
	else:
		print ("The config file {} is invalid!\n".format(log_target))

	# repr()或%r方法以函数的形式对python机器描述一个对象，str()或%s方法以类型的形式对人描述一个对象。
	if log_levels == 'CRITICAL':
		log_level = logging.CRITICAL
	elif log_levels == 'ERROR':
		log_level = logging.ERROR
	elif log_levels == 'WARNING':
		log_level = logging.WARNING
	elif log_levels == 'INFO':
		log_level = logging.INFO
	else:
		log_level = logging.DEBUG
	return log_target, log_level



if __name__ == "__main__":
	print ("\nThe current directory is {}.\n".format(os.path.dirname(os.getcwd())))
	# cmd()
	# log1()
	# log2()

	log_target, log_level = config2()
	log3(log_target, log_level)
	class_log1 = OnlyForMyself.Shopping() # 也可以(year=1983, month=9, day=17)或者(1983, 9, 17)或者(1983)。
	class_log2 = Blogging(1995, 7, 12) # 也可以(year=1983, month=9, day=17)或者(1983, 9, 17)或者(1983)。
	result1 = class_log1.approach0()
	result2 = class_log1._approach1()
	result1 = class_log2.approach0()
	result2 = class_log2._approach1()
	print ("\n")
