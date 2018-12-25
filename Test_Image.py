from __future__ import absolute_import, unicode_literals
import os, sys, argparse
import logging
from autologging import logged
import re
import warnings
# import threading
# import subprocess


def log_to_ConsoleAndFile(log_file, log_level_console, log_level_file):
	logging.basicConfig(level=log_level_file, format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s", 
					datefmt='%Y-%b%d-%H:%M:%S', filename=log_file, filemode='w')
	console = logging.StreamHandler()
	console.setLevel(log_level_console)
	formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
	console.setFormatter(formatter)
	logging.getLogger('').addHandler(console)


'''
# SETTING_FILE = const.SETTING_FILE
current_path = os.path.dirname(os.getcwd()) + '/'
CONFIG = ConfigFactory(SETTING_FILE).load_config()
data_path = CONFIG.get("data", "data_path")
QA_record_general = current_path + data_path + CONFIG.get("data", "QA_record_general")
QA_type_general = CONFIG.get("data", "QA_type_general")
QA_record_technical = current_path + data_path + CONFIG.get("data", "QA_record_technical")
QA_type_technical = CONFIG.get("data", "QA_type_technical")
QA_record_simple = current_path + data_path + CONFIG.get("data", "QA_record_simple")
QA_type_simple = CONFIG.get("data", "QA_type_simple")
'''


@logged(logging.getLogger("Test_Image.main"))

def func():
	func._log.info("A function starts here.")
	print ("This is a dummy function.")
	func._log.info("A function ends here.")


@logged(logging.getLogger("Test_Image.main"))

def main():
	main._log.info("The main function starts here.")
	func()
	main._log.info("The main function stops here.")



if __name__ == "__main__":
	print ("\nThe entire program started now. May the force be with you!...\n")
	current_path = os.path.dirname(os.getcwd()) + '/'
	print ("The current path is {}.\n".format(current_path))
	# log_target, log_level_console, log_level_file = log_set_from_config(current_path, SETTING_FILE)
	# print ("The log file is {} with level={}&&{}.\n".format(log_target, log_level_console, log_level_file))
	log_target = "message.log"

	log_to_ConsoleAndFile(log_target, 'DEBUG', 'DEBUG')
	try:
		sys.exit(main())
	except (KeyboardInterrupt, EOFError):
		print("\nThe entire program aborted due to keyboard interruption! Are you still there?\n")
		sys.exit(1)