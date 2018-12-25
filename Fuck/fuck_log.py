import logging, time, sys, os, logging.config, autologging, ConfigParser
from configs.config_factory import ConfigFactory
from const import *

config = ConfigFactory(CONFIG_FILE).get_config()
consumer_log_level = config.get(LOGSECTION, "consumer_log_level")
consumer_log_level = os.getenv('consumer_log_level', consumer_log_level).upper()
if consumer_log_level == 'CRITICAL':
    log_level = logging.CRITICAL
elif consumer_log_level == 'ERROR':
    log_level = logging.ERROR
elif consumer_log_level == 'WARNING':
    log_level = logging.WARNING
elif consumer_log_level == 'INFO':
    log_level = logging.INFO
else:
    log_level = logging.DEBUG

# Handles all the loggers to use across the project
gen_logger = logging.getLogger("blush.consumer.general")
gen_logger.setLevel(log_level)
formatter = logging.Formatter('%(asctime)s: %(name)s: %(levelname)s: %(funcName)s(): process %(process)d: process name %(processName)s: line %(lineno)d: %(message)s')
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
gen_logger.addHandler(stdout_handler)

gen_tracer = logging.getLogger("blush.consumer.trace")
gen_tracer.setLevel(autologging.TRACE)
formatter = logging.Formatter('%(asctime)s: %(name)s: %(levelname)s:process %(process)s:%(filename)s:%(funcName)s():line %(lineno)s:%(message)s')
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
gen_tracer.addHandler(stdout_handler)




import os

# Define all the app level constants here

REKOGNITION = 'rekognition'
TFSERVING = 'tfserving'
# CONFIG_FILE = '/etc/consumer/consumer.ini'
config_env = os.getenv('env', '')
CONFIG_FILE = '/etc/consumer/consumer_' + config_env + '.ini'
# print "The config file is:", CONFIG_FILE

MODERATION_REQUEST_CLASS_SUFFIX = 'ModerationRequest'
MODERATION_CONTROLLER_CLASS_SUFFIX = 'ModerationController'

CONTROLLER_PACKAGE_NAME = 'controllers'
CONTROLLER_MODULE_SUFFIX = '_moderation_controller'

S3 = 'S3'
JSON_KEYS = 'Json_keys'
LOGSECTION = 'LOGSECTION'
