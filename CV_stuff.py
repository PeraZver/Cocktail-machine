# This package deals with computer vision part.

from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2

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

# detection pause and counter
person_detected = -5
personCtr = 0


def CV_Detect():
	global person_detected
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
		print("Detected %d objects." % detections.shape[2])
		# find people with more than 75% confidence
		personIdx = np.where(detections[0,0,:,1] == CLASSES.index("person")) # check how many detections are people
		print("Detected %d persons." % personIdx[0].size)
		personConfidence = detections[0,0,personIdx[0],2] # find their confidences
		#print("Confidence: %.2f %%" % max(personConfidence))
		personCtr = np.where(personConfidence > 0.75)[0].size	# return how many confidences are higher than 80%
		print("Pretty sure about %d people" % personCtr)
		person_detected = time.time() if personCtr > 0 else 0
		
	return (personCtr)

def CV_Cleanup():
	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()
