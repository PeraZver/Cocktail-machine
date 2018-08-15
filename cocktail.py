
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
hx.reset()
#hx.tare()

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

def ShowAdd(personCtr):
    """ Display the add depending on number of persons detected. """
    if (personCtr):
        print (str(personCtr) + " persons detected!")
        #display the add
        label = "{} persons detected".format(personCtr)
        reklama_file = 'girl.jpg' if personCtr > 1 else 'wine.jpg'
        reklama = cv2.imread(reklama_file)
        cv2.namedWindow('reklama', cv2.WINDOW_NORMAL)
        
        screen_res = 1024, 760
        scale_width = screen_res[0] / reklama.shape[1]
        scale_height = screen_res[1] / reklama.shape[0]
        scale = min(scale_width, scale_height)
        window_width = int(reklama.shape[1] * scale)
        window_height = int(reklama.shape[0] * scale)
        cv2.resizeWindow('reklama', window_width, window_height)
        
        cv2.putText(reklama, label, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 5, [255,255,255], 2)
        # cv2.imshow('reklama',reklama)
        
# loop over the frames from the video stream
while True:
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
		ShowAdd(personCtr)


	# show the output frame
	#~ cv2.imshow("Frame", frame)
	#key = cv2.waitKey(1) & 0xFF
	
	# if the `q` key was pressed, break from the loop
	#if key == ord("q"):
	#    break
	
	# update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
