
# Documentation for `vimbaPy`

*Note that additional documentation can be found alongside individual methods in the source code.*

## Example usage

To start, all usage of `vimbaPy` should begin with the following:

*For pymba:*

``` python

from vimbaPy import _pymba

cameras = _pymba.getCameraID() # Retrieve the ID's of all connected cameras.
cam = cameras[0] # Select the first camera

cam_P = _pymba.createInstance(cam) # Create an independent instance of vimbaPy using pymba

```

*For VimbaPython:*

``` python
from vimbaPy import _VimbaPython

cameras = _VimbaPython.getCameraID() 
cam = cameras[0]

cam_VP = _VimbaPython.createInstance(cam) # Same as above except with VimbaPython

```

This creates an independent instance for operating a given camera, in this case the first connected camera. Using this instance, we can then call further operations for this camera:

``` python

# Stream live footage from the camera for 10 seconds
cam_P.stream(time=10, frame_buffer=10, callback=cam_P.display) # using pymba
cam_VP.stream(time=10, frame_buffer=10, callback=cam_VP.display) # using VimbaPython

```

Using this workflow we can streamline acquisition projects like so:

``` python

from vimbaPy import _pymba

cameras = _pymba.getCameraID()
cam = cameras[0]

# Create an instance set to save frames in 'testFrames'
cam_P = _pymba.createInstance(cameraID=cam, path="/home/z/Documents/testFrames/")

# And stream frames to disk for 10 seconds
cam_P.stream(time=10, frame_buffer=10, callback=cam_P.export)

```

Note that we can specify different arguments at whichever stage we choose, so if we wanted to enclose all the arguments in one method call we can:

``` python

from vimbaPy import _pymba

camera = _pymba.getCameraID()
cam = cameras[0]

cam_P = _pymba.createInstance(cam)

# Stream to 'testFrames' with some added feature configuration
cam_P.stream(
	time=10,
	frame_buffer=10,
	callback=cam_P.export,
	features={"ExposureAuto": "Off", "ExposureTime": 5000, "BlackLevel": 0, "Gain": 0},
	path="/home/z/Documents/testFrames/")

```
For continuous acquisition, there are currently several frame handlers implemented: `display` and `export` / `export_withCounter`. These display frames live or export them to a given path respectively. They can be addressed like so:

``` python

# Stream a live view for 10 seconds
cam_P.stream(time=10, frame_buffer=10, callback=cam_P.display)

# Stream frame to disk for 10 seconds
cam_P.stream(time=10, frame_buffer=10, callback=cam_P.export, path="/home/z/Documents/testFrames/")

```

For single frame acquisition, there is currently only support for exporting frames to disk:

``` python

# Acquire a single frame and export to disk
cam_P.acquire_frame(timeout_ms=2000, path="/home/z/Documents/testFrames/", filename="test_1.jpg")

``` 

As with continuous acquisition, we can specify some additional configuration settings:

```python

# Acquire a single frame with an exposure of 5000 (µs)
cam_P.acquire_frame(
	timeout_ms=2000,
	path="/home/z/Documents/testFrames/",
	filename="test_2.jpg",
	features={"ExposureTime": 5000})

```
As with earlier versions, support for configuring camera settings outside of the acquisition methods is still available. Note that there is support for configuring multiple settings at once in addition:

``` python

cam_P.setSingleFeature(feature="ExposureTime", value=5000, verbose=True)

cam_P.setMultiFeature(
	features={"ExposureAuto": "Off",
			  "ExposureTime": 5000, 
			  "BlackLevel": 0,
			  "Gain": 0,
			  "Width": 1600,
			  "Height": 1200},
	verbose=True)

```

## More detailed documentation

Note that unless specified, examples will use the camera instances specified at the beginning of this section. In addition, the naming of specific camera instances is only for clarity on which wrapper is being used under the hood. Lastly, methods for either module can be addressed using the same names. 

### getCameraID

Obtain the ID's of all connected Allied Vision cameras. ID's are returned as a list.

**Arguments:**

NA

**Example usage**

``` python
from vimbaPy import _pymba, _VimbaPython

# For pymba
cameras_P = _pymba.getCameraID()

# For VimbaPython
cameras_VP = _VimbaPython.getCameraID()

```

### createInstance

Create an independent instance for operating a given camera. 

**Arguments**

* cameraID: Character string. Camera ID for a specific camera. 
* liveViewWidth: Numeric. Width of live camera view in pixels. Default is 520 px. 
* liveViewHeight: Numeric. Height of live camera view in pixels. Default is 400 px.
* path: Character string. Path to save frames. Default is current working directory.

**Example usage**

``` python
from vimbaPy import _pymba, _VimbaPython

# For pymba
cameras_P = _pymba.getCameraID()
cam_P = _pymba.createInstance(cameras_P[0])

# For VimbaPython
cameras_VP = _VimbaPython.getCameraID()
cam_VP = _VimbaPython.createInstance(cameras_VP[0])

```

### setPath

Set a new path for saving frames.

**Arguments:**

* path: Character string. File path for saving frames. 

**Example usage**

``` python
# Using the instances set above:

# For pymba
cam_P.setPath(path="/home/z/Desktop/")

# For VimbaPython
cam_VP.setPath(path="/home/z/Desktop/")

```

### listFeatures

List all features for the given camera. Note that not all features will be adjustable.

**Arguments:**

NA

**Example usage:**

``` python

# For pymba
cam_P.listFeatures()

# For VimbaPython
cam_VP.listFeatures()

```

### getFeatureInfo

Retrieve some basic feature information for a given feature. Values are returned as a nested list, with the first slot being the current value, and the second being the range. Min and max are the first and second slots respectively for the latter.

**Arguments:**

* feature: Character string. Name of feature to retrieve info from.

**Example usage:**

``` python

# For pymba
cam_P.getFeatureInfo(feature="ExposureTime")

# For VimbaPython
cam_VP.getFeatureInfo(feature="ExposureTime")

```

### setSingleFeature

Set the value for a given feature.

**Arguments:**

* feature: Character string. Name of feature to set value for.
* value: Numeric or character string. New value to set feature to.
* verbose: Boolean. Whether to print additional information. Default is False.

**Example usage:**

``` python

# For pymba
cam_P.setSingleFeature(feature="ExposureTime", value=5000, verbose=True)

# For VimbaPython
cam_VP.setSingleFeature(feature="ExposureTime", value=5000, verbose=True)

```

### setMultiFeature

Set the value for a given set of features.

**Arguments:**

* features: Dictionary. Feature names and corresponding values to set them to.
* verbose: Boolean. Whether to print additional information. Default is False.

**Example usage:**

```python

# For pymba
cam_P.setMultiFeature(features={"ExposureTime": 5000, "BlackLevel": 0}, verbose=True)

# For VimbaPython
cam_VP.setMultiFeature(features={"ExposureTime": 5000, "BlackLevel": 0}, verbose=True)

```

### acquire_frame

Acquire a frame and export to a given path. The path argument is optional for users who would like to export to a specific path. If left empty, the frame will be exported to the path specified in the given instance. This will be the current working directory if you did not specify a path when creating the instance or set a new path with `setPath()`.

**Arguments:**

* features: Dictionary. Feature names and corresponding values to set them to.
* timeout_ms: Numeric. Camera timeout in miliseconds. Default is 2000.
* path: Character string. File path to save frames. Default is None.
* filename: Character string. Filename to save frame by. Default is the current time if left as None.
* returnFilename: Boolean. Whether to return the full file-path to the saved frame. Default is False.

**Example usage**

``` python

# For pymba
cam_P.acquire_frame(
	timeout_ms=2000,
	path="/home/z/Documents/testFrames/",
	filename="test_2.jpg",
	features={"ExposureTime": 5000})

# For VimbaPython
cam_VP.acquire_frame(
	timeout_ms=2000,
	path="/home/z/Documents/testFrames/",
	filename="test_2.jpg",
	features={"ExposureTime": 5000})


```

### stream

Stream frames with a given callback (Asynchronous).

**Arguments:**

* time: Numeric. Time to stream frames.
* callback: Class object. Callback for handling individual frames.
* frame_buffer: Numeric. Size of frame buffer. 
* frame_limit: Numeric. Number of frames to acquire, only available with `export` and `export_withCounter` frame handlers. Default is None.
* features: Dictionary. Feature names and corresponding values to set them to.
* path: Character string. File path to save frames. Default is path specified for the current instance.

**Example usage**

``` python

# For pymba
cam_P.stream(
	time=10,
	frame_buffer=10,
	callback=cam_P.export,
	features={"ExposureAuto": "Off", "ExposureTime": 5000, "BlackLevel": 0, "Gain": 0},
	path="/home/z/Documents/testFrames/")

# For VimbaPython
cam_VP.stream(
	time=10,
	frame_buffer=10,
	callback=cam_VP.export,
	features={"ExposureAuto": "Off", "ExposureTime": 5000, "BlackLevel": 0, "Gain": 0},
	path="/home/z/Documents/testFrames/")

```

### Frame handlers

There are several frame handlers implemented in this package: `display`, `export` and `export_withCounter`. `export_withCounter` merely uses a counter for numbering individual frames. By comparison, `export` uses the current time down to nanoseconds to give unique names for individual frames. All three can be addressed in the same manner:

``` python

cam_P.stream(
	time=10, 
	frame_buffer=10, 
	callback=cam_P.display)

cam_P.stream(
	time=10, 
	frame_buffer=10, 
	callback=cam_P.export, 
	path="/home/z/Documents/testFrames/")

cam_P.stream(
	time=10, 
	frame_buffer=10, 
	callback=cam_P.export_withCounter, 
	path="/home/z/Documents/testFrames/")

```

To acquire a set number of frames, you can use the acquisition frame handlers like so:

``` python

cam_P.stream(
	time=None, 
	frame_buffer=10, 
	callback=cam_P.export, 
	frame_limit=100, 
	path="/home/z/Documents/testFrames/")

cam_P.stream(
	time=None, 
	frame_buffer=10, 
	callback=cam_P.export_withCounter,
	frame_limit=100, 
	path="/home/z/Documents/testFrames/")

```

Note that you can only specify either time or a frame limit for a given acquisition, not both. In addition, the `display` frame handler will not accept a frame limit. Lastly, for high framerate acquisitions, you will need to increase the frame buffer size or incomplete frames may be returned and ignored.