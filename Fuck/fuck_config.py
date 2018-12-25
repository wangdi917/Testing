import os
import ConfigParser

class ConfigFactory(dict): # 输入一个字典，然后从任何外部文件中load configuration entries。
	# config_env = os.getenv('env')
	config_file_defined = "/etc/consumer/shit.ini"
	# config_file_defined = "/etc/consumer/shit_" + config_env + '.ini'
	CONFIG = None

	def __init__(self, config_file_specified=None):

		if config_file_specified is not None:
			self.config_file_defined = config_file_specified
			
		if self.config_file_defined.lower().endswith('.ini'):
			self.CONFIG = ConfigParser.ConfigParser()
			self.CONFIG.read(self.config_file_defined)

	def get_config(self):
		return self.CONFIG
