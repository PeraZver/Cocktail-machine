#!/usr/bin/env python
import sys
from imutils.video import VideoStream
import imutils
import tensorflow as tf
import numpy as np
import time
import cv2

from model import OpenNsfwModel, InputType
# from image_utils import create_tensorflow_image_loader
from image_utils import create_yahoo_image_loader

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
print("[INFO] starting video stream ...")
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# tensor flow loader options
IMAGE_LOADER_TENSORFLOW = "tensorflow"
IMAGE_LOADER_YAHOO = "yahoo"
MODEL = "open_nsfw-weights.npy"
INPUT_TYPE = "tensor"

image_loader = IMAGE_LOADER_YAHOO

print("[INFO] loading model ...")
now = time.time() 
model = OpenNsfwModel()

start_time = time.time()
total_time = 0

sess = tf.Session()
input_type = InputType[INPUT_TYPE.upper()]
model.build(weights_path=MODEL, input_type=input_type)

fn_load_image = None

if input_type == InputType.TENSOR:
	if image_loader == IMAGE_LOADER_TENSORFLOW:
		fn_load_image = create_tensorflow_image_loader(sess)
	else:
		fn_load_image = create_yahoo_image_loader()
elif input_type == InputType.BASE64_JPEG:
	import base64
	fn_load_image = lambda filename: np.array([base64.urlsafe_b64encode(open(filename, "rb").read())])

sess.run(tf.global_variables_initializer())
print("[INFO] Time of  model upload: {:.2} s".format(time.time() - start_time))

def CV_Detect():

	frame = vs.read()
	
	image = fn_load_image(frame) # send the frame to the image loader and run the prediction. 
	predictions = sess.run(model.predictions, feed_dict={model.input: image})

	print ("NSFW coefficient: {:.2}".format(predictions[0][1]))
	if predictions[0][1] > 0.8:
		print("I see your boobies! :D")
		return True
		
def CV_Cleanup():
	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()
