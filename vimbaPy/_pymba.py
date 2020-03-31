from pymba import Vimba, VimbaException, Frame
from time import sleep
import os
import cv2
import datetime
import threading


def getCameraID():

	"""
	Obtain the ID's of all connected Allied Vision cameras. 

	"""

	with Vimba() as vimba:
			cameras = vimba.camera_ids()

	return cameras

class createInstance:

	"""
	Create an independent instance for operating a given camera.

	Arguments:
		- cameraID: Character string. Camera ID for a specific camera. 
		- liveViewWidth: Numeric. Width of live camera view in pixels. Default is 520 px. 
		- liveViewHeight: Numeric. Height of live camera view in pixels. Default is 400 px.
		- path: Character string. Path to save frames. Default is current working directory.

	"""

	def __init__(self, cameraID, liveViewWidth=520, liveViewHeight=400, path=os.getcwd()):

		self.cameraID = cameraID
		self.pixelFormatConversions = {'BayerRG8': cv2.COLOR_BAYER_RG2RGB}
		self.liveViewWidth = liveViewWidth
		self.liveViewHeight = liveViewHeight
		self.path = path

	def setPath(self, path):

		"""
		Set a new path for saving frames.

		Arguments:
			- path: Character string. File path for saving frames. 

		"""

		self.path = path

	def listFeatures(self):

		"""
		List all features for the given camera. 

			Note that not all features will be adjustable. 

		"""

		with Vimba() as vimba:

			camera = vimba.camera(self.cameraID)
			camera.open()

			features = []

			for feature_name in camera.feature_names():
				features.append(feature_name)

			camera.close()

		return features

	def getFeatureInfo(self, feature):

		"""
		Retrieve some basic feature information for a given feature.

		Values are returned as a nested list, with the first slot being the 
		current value, and the second being the range. Min and max are the 
		first and second slots respectively for the latter.

		Arguments:
			- feature: Character string. Name of feature to retrieve info from.

		"""

		with Vimba() as vimba:
			camera = vimba.camera(self.cameraID)
			camera.open()

			feature = camera.feature(feature)

			try:
				value = feature.value
				range_ = feature.range
			except VimbaException as e:
				value = e
				range_ = None

			feature_info = [value, range_]

			camera.close()

		return feature_info

	def setSingleFeature(self, feature, value, verbose=False):

		"""
		Set the value for a given feature.

		Arguments:
			- feature: Character string. Name of feature to set value for.
			- value: Numeric or character string. New value to set feature to.
			- verbose: Boolean. Whether to print additional information. Default is False.

		"""

		with Vimba() as vimba:
			camera = vimba.camera(self.cameraID)
			camera.open()

			feat = camera.feature(feature)

			if verbose == True:
				initial = feat.value
				feat.value = value

				print(str(feature) + " is now: " + str(value) + ", was " + str(initial))

			elif verbose == False:
				feat.value = value

			else:
				print("Expected value of type Boolean. Available values for 'verbose' are True or False.")


			camera.close()

	def setMultiFeature(self, features, verbose=False):

		"""
		Set the value for a given set of features

		Arguments:
			- features: Dictionary. Feature names and corresponding values to set them to.
			- verbose: Boolean. Whether to print additional information. Default is False.

		"""

		with Vimba() as vimba:
			camera = vimba.camera(self.cameraID)
			camera.open()

			for feature in features:
				if verbose == True:
					feat = camera.feature(feature)
					initial = feat.value
					feat.value = features[feature]

					print(str(feature) + " is now: " + str(features[feature]) + ", was " + str(initial))

				elif verbose == False:
					feat = camera.feature(feature)
					feat.value = features[feature]

				else:
					print("Expected value of type Boolean. Available values for 'verbose' are True or False.")

			camera.close()

	def incompleteFrameErrorMsg(self):

		"""
		Helper function for printing a basic error message if a frame is incomplete.

		"""

		print("Acquisition at " + str(self.cameraID) + " returned incomplete frame(s).")

	def acquire_frame(self, features=None, path=None, filename=None, returnFilename=False):

		"""
		Acquire a frame and export to a given path.

		The path argument is optional for users who would like to export to a specific path.
		If left empty, the frame will be exported to the path specified in the given instance.
		This will be the current working directory if you did not specify path when creating the instance
		or set a new path with .setPath().

		Arguments:
			- features: Dictionary. Feature names and corresponding values to set them to.
			- path: Character string. File path to save frames. Default is None.
			- filename: Character string. Filename to save frame by. Default is the current time if left as None.
			- returnFilename: Boolean. Whether to return the full file-path to the saved frame. Default is False.

		"""

		if path == None:
			path = self.path

		with Vimba() as vimba:

			camera = vimba.camera(self.cameraID)
			camera.open()

			if not features == None:
				for feature in features:
					feat = camera.feature(feature)
					feat.value = features[feature]

			camera.arm(mode="SingleFrame")

			frame = camera.acquire_frame()
					
			if frame.data.receiveStatus == -1:

				self.incompleteFrameErrorMsg()

			else:

				image = frame.buffer_data_numpy()

				try:
					image = cv2.cvtColor(image, self.pixelFormatConversions[frame.pixel_format])
				except:
					pass

				if filename == None:
					timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss%fµs')
					filename = str(timestamp) + ".jpg"

				cv2.imwrite(path + filename, image)

			camera.disarm()
			camera.close()	

		if returnFilename == True:
			return path + filename		

	def display(self, frame: Frame):

		"""
		Frame handler that displays frames.

		"""

		if frame.data.receiveStatus == -1:

			self.incompleteFrameErrorMsg()

		else:

			image = frame.buffer_data_numpy()

			try:
				image = cv2.cvtColor(image, self.pixelFormatConversions[frame.pixel_format])

			except:
				pass

			msg = "Capturing from \'{}\'."
			im_resize = cv2.resize(image, (self.liveViewWidth, self.liveViewHeight))
			cv2.imshow(msg.format(self.cameraID), im_resize)

			key = cv2.waitKey(1)

	def export(self, frame: Frame):

		"""
		Frame handler that exports frames to a given path.

		"""

		if self._frame_limit == None:

			if frame.data.receiveStatus == -1:

				self.incompleteFrameErrorMsg()

			else:

				image = frame.buffer_data_numpy()

				try:
					image = cv2.cvtColor(image, self.pixelFormatConversions[frame.pixel_format])
				except:
				 	pass

				timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss%fµs')
				filename = str(timestamp) + ".jpg"

				cv2.imwrite(os.path.join(self.path + filename), image)

				self._counter += 1

		else: 

			if self._counter <= self._frame_limit:

				if frame.data.receiveStatus == -1:

					self.incompleteFrameErrorMsg()

				else:

					image = frame.buffer_data_numpy()

					try:
						image = cv2.cvtColor(image, self.pixelFormatConversions[frame.pixel_format])
					except:
					 	pass

					timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss%fµs')
					filename = str(timestamp) + ".jpg"

					cv2.imwrite(os.path.join(self.path + filename), image)

					self._counter += 1

			elif self._counter > self._frame_limit:

				self.shutdown_event.set()

				return

	def export_withCounter(self, frame: Frame):

		"""
		Frame handler that exports frames to a given path with 
		a counter for numbering frames.

		"""

		if self._frame_limit == None:

			if frame.data.receiveStatus == -1:

				self.incompleteFrameErrorMsg()

			else:

				image = frame.buffer_data_numpy()

				try:
					image = cv2.cvtColor(image, self.pixelFormatConversions[frame.pixel_format])
				except:
				 	pass

				filename = str(self._counter) + ".jpg"

				cv2.imwrite(os.path.join(self.path + filename), image)

				self._counter += 1

		else:

			if self._counter <= self._frame_limit: 

				if frame.data.receiveStatus == -1:

					self.incompleteFrameErrorMsg()

				else:

					image = frame.buffer_data_numpy()

					try:
						image = cv2.cvtColor(image, self.pixelFormatConversions[frame.pixel_format])
					except:
					 	pass

					filename = str(self._counter) + ".jpg"

					cv2.imwrite(os.path.join(self.path + filename), image)

					self._counter += 1

			elif self._counter > self._frame_limit:

				self.shutdown_event.set()

				return

	def stream(self, time, callback, frame_buffer, frame_limit=None, features=None, path=None):

		"""
		Stream frames with a given callback (Asynchronous).

		Arguments:
			- time: Numeric. Time to stream frames.
			- callback: Class object. Callback for handling individual frames.
			- frame_buffer: Numeric. Size of frame buffer. 
			- frame_limit: Numeric. Number frames to acquire. Default is None.
			- features: Dictionary. Feature names and corresponding values to set them to.
			- path: Character string. File path to save frames. Default is path specified for the current instance.

		"""

		if not path == None:
			self.path = path

		if time != None and frame_limit == None:
			self._frame_limit = None
		elif time == None and frame_limit != None:
			self._frame_limit = frame_limit
		else:
			raise ValueError("Must specify either time or frame_limit, with the other = None. Cannot specify both at once.")

		self._counter = 1

		with Vimba() as vimba:
			camera = vimba.camera(self.cameraID)
			camera.open()

			if not features == None:
				for feature in features:
					feat = camera.feature(feature)
					feat.value = features[feature]

			camera.arm('Continuous', callback, frame_buffer_size=frame_buffer)

			if self._frame_limit == None:

				camera.start_frame_acquisition()

				sleep(time)

				camera.stop_frame_acquisition()

			else:
				
				if self.display == callback:
					raise ValueError("Cannot use the 'display' callback with a frame limit.")					

				self._frame_limit = frame_limit
				self.shutdown_event = threading.Event()

				try:
					camera.start_frame_acquisition()
					self.shutdown_event.wait()

				finally:
					camera.stop_frame_acquisition()

			# Required to stop the session crashing
			sleep(0.01)

			camera.disarm()
			camera.close()




# # Tests
# cams = getCameraID()
# cam = cams[0]
# cam_1 = createInstance(cam)

# # cam_1.stream(
# # 	time=5,
# # 	frame_buffer=100,
# # 	callback=cam_1.display)

# # for i in range(1, 5, 1):	

# # 	print("Stream: " + str(i))

# cam_1.stream(
# 	time=None,
# 	callback=cam_1.export,
# 	frame_buffer=100,
# 	frame_limit=100,
# 	path="/home/z/Documents/testFrames/")

# 	# sleep(1)

