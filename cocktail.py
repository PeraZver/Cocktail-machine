
# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711

####################################
# Setting up scale

def cleanAndExit():
    print ("Cleaning...")
    GPIO.cleanup()
    print ("Bye!")
    sys.exit()

hx = HX711(5, 6)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(99.43)

###################################
# Setting up SSD detector

prototxt = "MobileNetSSD_deploy.prototxt.txt"
model = "MobileNetSSD_deploy.caffemodel"

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# initialize the camera and grab a reference to the raw camera capture
print("[INFO] starting video stream...")
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
fps = FPS().start()

# detection pause and counter
person_detected = -5
personCtr = 0

def MakeACocktail(personCtr):
	""" Make a cocktail depending on number of persons detected. """
	if (personCtr):
		print (str(personCtr) + " persons detected!")
		print ("Giving you 3 sec to put a glass in the machine")
		time.sleep(3)
		# Reset the scale
		hx.reset()
		hx.tare()
		start_time = time.time()
		while (hx.get_weight(5) < 100 and (time.time() - start_time) < 5):
			print ("Weight: ", hx.get_weight(5), " g")
		hx.power_down()
	
# loop over the frames from the video stream
while True:
	try:
		# grab the frame from the threaded video stream and resize it
		frame = vs.read()
		frame = imutils.resize(frame, width=400)

		#if person is not detected proceed with detection algorithm
		if ((time.time()- person_detected) > 5):

			print("Going to detection mode")
			# grab the frame dimensions and convert it to a blob
			(h, w) = frame.shape[:2]
			blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
				0.007843, (300, 300), 127.5)
			
			# pass the blob through the network and obtain the detections and
			# predictions
			net.setInput(blob)
			detections = net.forward()
			print("Detected "+str(detections.shape[2])+" objects")
			# find people with more than 75% confidence
			personIdx = np.where(detections[0,0,:,1] == CLASSES.index("person")) # check how many detections are people
			print("Detected " + str(personIdx[0].size)+" persons")
			personConfidence = detections[0,0,personIdx[0],2] # find their confidences
			print("Confidence: " + str(personConfidence))
			personCtr = np.where(personConfidence > 0.75)[0].size	# return how many confidences are higher than 80%
			print("pretty sure about " + str(personCtr) + " people")
			person_detected = time.time() if personCtr > 0 else 0
			# Make a cocktail
			MakeACocktail(personCtr)


		# show the output frame
		#~ cv2.imshow("Frame", frame)
		#key = cv2.waitKey(1) & 0xFF
		
		# if the `q` key was pressed, break from the loop
		#if key == ord("q"):
		#    break
		
		# update the FPS counter
		fps.update()

	except (KeyboardInterrupt, SystemExit):
		cleanAndExit()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
