# The "Blush moderation controller" is a child/derived class specifically for the Blush project.
# Therefore it has Nudity/Gesture functionalities inside it.

import sys, os, io, shutil, math, json, copy, time, datetime, boto3, numpy as np
import multiprocessing
from PIL import Image
import logging
from autologging import logged
from configs.config_factory import ConfigFactory
from const import *
# import configparser as ConfigParser
import ConfigParser
from helpers.cloudwatch_metric_writer import CloudWatchMetricWriter
from blush_error_codes import *
from controllers.generic_moderation_controller import GenericModerationController
from controllers.blush_nudity_moderation_controller import BlushNudityModerationController
from controllers.blush_gesture_moderation_controller import BlushGestureModerationController


def multiprocessor_hack(instance, name, args=(), kwargs=None):
	"""Indirect caller for instance methods and multiprocessing. It's stupid but it is the only way to get it to work."""
	if kwargs is None:
		kwargs = {}
	return getattr(instance, name)(*args, **kwargs)


@logged(logging.getLogger("blush.consumer.general"))

class BlushModerationController(GenericModerationController):
	def __init__(self, Json_object):
		self.__log.info("Initializing the Blush main controller.")
		GenericModerationController.__init__(self)
		self.request = Json_object
		self.error_mark = "Error"


	def execute(self, models_data):
		""" Send forward requests to Gesture and Nudity controllers and send backward their responses. """
		start_time = time.time()
		self.__log.info("Executing the main controller 'BlushModerationController'. May the Force be with you!...")
		error_controller_list = []

		initialized_response, structure_flag = self.data_initialize(self.request)
		self.__log.info("The Callback, PictureID, and ErrorCode information have been initialized inside the final response.")
		if structure_flag is False:
			return initialized_response

		# Assume that 'ModerationType_key' and 'flow_directions' exist in the input data and have been extracted by initialization as a faith in the API team members.

		data_directions, data_directed = self.request_parse(self.request, self.ModerationType_key, self.flow_directions)
		self.__log.info("The input Json object has been parsed.")
		self.__log.debug("The input Json object has been parsed as {0}.".format(data_directed))

		#### Nandakishore has added the function to read images from local files.

		picture_url = self.request[self.PicturePath_key]
		if picture_url.startswith("file:"):
			image_data, S3_flag = self.loadImageFromLocal(picture_url[5:])
		else:
			image_data, S3_flag = self.loadS3(picture_url)

		# image_data, S3_flag = self.extractS3(self.request[self.PicturePath_key], self.S3_mark, self.S3_region)
		validated_response, picture_flag = self.picture_validate(initialized_response, image_data, S3_flag)
		self.__log.info("The picture has been validated.")
		self.__log.debug("The picture has been validated as {0}.".format(picture_flag))
		# print "The picture validation result is:", picture_flag
		if picture_flag is False:
			return validated_response

		moderation_responses, async_flag = self.async_send_receive(data_directed, image_data, models_data)
		if async_flag is False:
			blush_error = BlushErrorControllerAsyncFailure()
			error_signal = self.__get_error_string(blush_error)
			error_controller_list.append(blush_error.prepare())
		for response in moderation_responses:
			if self.nudity_index in response.keys():
				if response[self.nudity_index] == "moderator unavailable":
					blush_error = BlushErrorControllerNudityModeratorUnavailable()
					error_signal = self.__get_error_string(blush_error)
					error_controller_list.append(blush_error.prepare())
			if self.gesture_index in response.keys():
				if response[self.gesture_index] == "moderator unavailable":
					blush_error = BlushErrorControllerGestureModeratorUnavailable()
					error_signal = self.__get_error_string(blush_error)
					error_controller_list.append(blush_error.prepare())
					
		integrated_responses = self.error_summarize(initialized_response, moderation_responses, error_controller_list)
		self.__log.info("The responses from the Nudity and Gesture controllers have been integrated.")
		self.__log.debug("The integrated response is {0}.".format(integrated_responses))
		
		seconds_to_complete = time.time() - start_time
		self.__log.info("Returning responses took {} seconds.".format(seconds_to_complete))
		try:
			CONFIG = ConfigFactory(CONFIG_FILE).get_config()
			cloudwatch_region = CONFIG.get(LOGSECTION, "cloudwatch_region")
			cloudwatch_namespace = CONFIG.get(LOGSECTION, "cloudwatch_namespace_ctrl_controller")
			CloudWatchMetricWriter(cloudwatch_region).put_metric(cloudwatch_namespace, "Time", seconds_to_complete, "Controller_step", "Forward_and_Backward", "Seconds")
		except Exception as e:
			blush_error = BlushErrorControllerConfigReadFailure()
			error_signal = self.__get_error_string(blush_error)
			self.__log.error(error_signal)
			self.__log.error("Either the external config file 'consumer.ini' cannot be read, or the cloudwatch metrics writing fails!")
			self.__log.error("Exception in cloudwatch metrics writing: {}".format(e))
			# print "Either the external config file 'consumer.ini' cannot be read, or the cloudwatch metrics writing fails!"
		return integrated_responses


	def __get_error_string(self, blush_error):
		""" Combine the error string with the error code. """
		return "{0}! {1}.".format(self.error_mark, blush_error)
	def __use_error_string(self, error_signal, blush_error):
		""" Use the error string as the final response. If called, it means that some severe errors happen in the initialization stage, so fundamental variables such as pictureID cannot be obtained and fedback. """
		dict_failure = {}
		dict_failure[self.error_mark] = [] 
		dict_failure[self.error_mark].append(blush_error.prepare())
		return dict_failure
	def __put_error_string(self, dict_in, error_signal, blush_error):
		""" Put the error string into the final response. If called, it means that some non-severe errors happen in the processing stage, so fundamental variables such as pictureID still exist. """
		dict_out = copy.deepcopy(dict_in)
		dict_out[self.error_mark] = []
		dict_out[self.error_mark].append(blush_error.prepare())
		return dict_out


	def data_initialize(self, data_in):
		""" Read variables from config file /etc/consumer/consumer.ini. Any environmental changes in the Json object should be applied to consumer(sandbox/latest/stage/prod).ini directly. """
		cf = ConfigParser.ConfigParser()
		structure_flag = True
		self.__log.info("Setting the Blush main controller using the external config file '/etc/consumer/consumer(sandbox/latest/stage/prod).ini'.")
		try:
			CONFIG = ConfigFactory(CONFIG_FILE).get_config()
			# print "Setting the Blush main controller using the external config file '/etc/consumer/consumer(sandbox/latest/stage/prod).ini'."
		except Exception as e:
			structure_flag = False
			blush_error = BlushErrorControllerConfigLoadFailure()
			error_signal = self.__get_error_string(blush_error)
			self.__log.error(error_signal)
			self.__log.error("The external config file '/etc/consumer/consumer(sandbox/latest/stage/prod).ini' cannot be found!")
			self.__log.error("Exception in config reading: {}".format(e))
			# print "The external config file '/etc/consumer/consumer(sandbox/latest/stage/prod).ini' cannot be found!"
			return self.__use_error_string(error_signal, blush_error=blush_error), structure_flag
		try:
			self.Callback_key = CONFIG.get(JSON_KEYS, "Callback_key")
			self.ModerationType_key = CONFIG.get(JSON_KEYS, "ModerationType_key")
			self.ModerationAction_key = CONFIG.get(JSON_KEYS, "ModerationAction_key")
			self.PictureID_key = CONFIG.get(JSON_KEYS, "PictureID_key")
			self.PicturePath_key = CONFIG.get(JSON_KEYS, "PicturePath_key")
			self.nudity_index = CONFIG.get(JSON_KEYS, "nudity_index")
			self.gesture_index = CONFIG.get(JSON_KEYS, "gesture_index")
			self.nudityresult_index = CONFIG.get(JSON_KEYS, "nudityresult_index")
			self.gestureresult_index = CONFIG.get(JSON_KEYS, "gestureresult_index")
			self.flow_directions = [self.nudity_index, self.gesture_index]
			self.number_mods = int(CONFIG.get(JSON_KEYS, "number_mods"))
			# print "The variables copied from the external config file are: Callback=%s, ModerationType=%s, ModerationAction=%s, PictureID=%s, PicturePath=%s, Nudity=%s, Gesture=%s." %(self.Callback_key, self.ModerationType_key, self.ModerationAction_key, self.PictureID_key, self.PicturePath_key, self.nudity_index, self.gesture_index)
		except Exception as e:
			structure_flag = False
			blush_error = BlushErrorControllerConfigReadFailure()
			error_signal = self.__get_error_string(blush_error)
			self.__log.error(error_signal)
			self.__log.error("The external config file 'consumer(sandbox/latest/stage/prod).ini' cannot be read!")
			self.__log.error("Exception in Json config reading: {}".format(e))
			# print "The external config file 'consumer(sandbox/latest/stage/prod).ini' cannot be read!"
			return self.__use_error_string(error_signal, blush_error=blush_error), structure_flag
		try:
			self.S3_mark = CONFIG.get(S3, "mark")
			self.S3_region = CONFIG.get(S3, "region")
			self.__log.debug("The S3 variables copied from the external config file are: S3_mark={0}, S3_region={1}.".format(self.S3_mark, self.S3_region))
			# print "The variables copied from the external config file are: number_mods=%d, S3_mark=%s, S3_region=%s." %(self.number_mods, self.S3_mark, self.S3_region)
		except Exception as e:
			structure_flag = False
			blush_error = BlushErrorControllerConfigReadFailure()
			error_signal = self.__get_error_string(blush_error)
			self.__log.error(error_signal)
			self.__log.error("The external config file 'consumer(sandbox/latest/stage/prod).ini' cannot be read!")
			self.__log.error("Exception in S3 config reading: {}".format(e))
			# print "The external config file 'consumer(sandbox/latest/stage/prod).ini' cannot be read!"
			return self.__use_error_string(error_signal, blush_error=blush_error), structure_flag
		self.__log.info("All the variables have been copied from the external config file.")

		""" Establish the data structure of the final response. Assume that the callback_key and pictureID_key exist in the input data as a faith in the API team-member. """
		data_out = {}
		data_out[self.Callback_key] = data_in[self.Callback_key]
		data_out[self.PictureID_key] = data_in[self.PictureID_key]
		data_out[self.nudity_index] = []
		data_out[self.gesture_index] = []
		data_out[self.nudityresult_index] = False
		data_out[self.gestureresult_index] = False
		data_out[self.error_mark] = [] # None
		self.__log.info("The final response has been established.")
		self.__log.debug("The final response contains keys Callback={0}, ModerationAction={1}, PictureID={2}, Nudity={3}, Gesture={4}, NudityResult={5}, GestureResult={6}.".format(self.Callback_key, self.ModerationAction_key, self.PicturePath_key, self.nudity_index, self.gesture_index, self.nudityresult_index, self.gestureresult_index))
		return data_out, structure_flag


	def picture_validate(self, dict_in, image_data, S3_flag):
		""" Validate both the S3 URL and the picture property. S3_flag comes before image_data! """
		picture_flag = True
		if S3_flag is False:
			picture_flag = False
			blush_error = BlushErrorControllerInvalidS3()
			error_signal = self.__get_error_string(blush_error)
			self.__log.info("Due to image S3 loading error, neither the Gesture or Nudity moderator will be called.")
			# print "Due to image S3 loading error, neither the Gesture or Nudity moderator will be called."
			return self.__put_error_string(dict_in, error_signal, blush_error), picture_flag
		elif image_data is None:
			picture_flag = False
			blush_error = BlushErrorControllerInvalidPicture()
			error_signal = self.__get_error_string(blush_error)
			self.__log.info("Due to image convertion error, neither the Gesture or Nudity moderator will be called.")
			# print "Due to image convertion error, neither the Gesture or Nudity moderator will be called."
			return self.__put_error_string(dict_in, error_signal, blush_error), picture_flag
		else:
			dict_out = copy.deepcopy(dict_in)
			return dict_out, picture_flag


	# Call the Nudity controller.
	def moderate_nudity(self, data, image, model_data):
		self.__log.info("The request of calling the Nudity controller is sent.")
		self.__log.debug("The request of calling the Nudity controller consists of Json object: {0} and image: {1}.".format(data, type(image)))
		try:
			class_nud_ctrl = BlushNudityModerationController()
			response_nudity = class_nud_ctrl.execute(data, image, model_data)
			self.__log.debug("The result of calling the Nudity controller is: {0}.".format(response_nudity))
		except Exception as e:
			blush_error = BlushErrorControllerNudityModeratorUnavailable()
			error_signal = self.__get_error_string(blush_error)
			# Here logging is done in the parent class.
			self.__log.error("The Nudity Moderator is unavailable!")
			self.__log.error("Exception in Nudity Moderator calling: {}".format(e))
			response_nudity = "moderator unavailable"
		return response_nudity

	# Call the Gesture controller.
	def moderate_gesture(self, data, image, model_data):
		self.__log.info("The request of calling the Gesture controller is sent.")
		self.__log.debug("The request of calling the Gesture controller consists of Json object: {0} and image: {1}.".format(data, type(image)))
		try:
			class_nud_ctrl = BlushGestureModerationController()
			response_gesture = class_nud_ctrl.execute(data, image, model_data)
			self.__log.debug("The result of calling the Gesture controller is: {0}.".format(response_gesture))
		except Exception as e:
			blush_error = BlushErrorControllerGestureModeratorUnavailable()
			error_signal = self.__get_error_string(blush_error)
			# Here logging is done in the parent class.
			self.__log.error("The Gesture Moderator is unavailable!")
			self.__log.error("Exception in Gesture Moderator calling: {}".format(e))
			response_gesture = "moderator unavailable"
		return response_gesture

	# Integrate the response from Nudity and that from Gesture together into a list. Nodity comes before Gesture!
	# @timeout(self.timeout)
	def async_send_receive(self, data, image, models_data):
		responses = []
		async_flag = True
		pool = multiprocessing.Pool(processes = self.number_mods)
		# timeout_lock = pool.lock()
		# pool.start(timeout_lock)
		self.__log.debug("Async multiprocesses have been set up, now start the pool.")
		results = [pool.apply_async(multiprocessor_hack, args = (self, 'moderate_nudity', (data, image, models_data['nudity']))), pool.apply_async(multiprocessor_hack, args = (self, 'moderate_gesture', (data, image, models_data['gesture'])))]
		# pool.join(self.timeout)
		pool.close()
		self.__log.debug("Waiting for all the async results to finish...")
		map (multiprocessing.pool.ApplyResult.wait, results)
		try:
			responses = [r.get() for r in results]
		except Exception as e:
			self.__log.error("Exception in collecting all the async results: {}".format(e))
			for r in results:
				try:
					responses.append(r.get())
				except Exception as e0:
					blush_error = BlushErrorControllerAsyncFailure()
					error_signal = self.__get_error_string(blush_error)
					self.__log.error("The response of {0} is unavailable!".format(r))
					self.__log.error("Exception in finding one async result: {}".format(e0))
			async_flag = False
		self.__log.info("The responses from the Nudity and Gesture controllers have been received.")
		return responses, async_flag

	# Integrate the error messages from Nudity and that from Gesture together into a list. Nodity comes before Gesture!
	def error_summarize(self, dict_in, moderation_responses, error_controller_list):
		dict_out = copy.deepcopy(dict_in)
		for response in moderation_responses:
			for key in response.keys():
				if key == self.error_mark:
					error_controller_list.append(response[self.error_mark])
				else: # The "else" means that "G/N" and "G/N Result".
					dict_out[key] = response[key]
		dict_out[self.error_mark] = error_controller_list
		return dict_out
