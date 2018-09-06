# USAGE
# python video_facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat
# python video_facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat --picamera 1

# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
from imutils.video import FPS
import datetime
import imutils
import time
import dlib
import cv2

shape_predictor_file = "shape_predictor_68_face_landmarks.dat"
 
# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
now = time.time()
detector = dlib.get_frontal_face_detector()
# detector = cv2.CascadeClassifier(args["cascade"])
predictor = dlib.shape_predictor(shape_predictor_file)
print("[INFO] Time to load the model {:.2f} s".format(time.time()-now)) 


# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] camera sensor warming up...")
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)


# loop over the frames from the video stream
def CV_Detect():
	# grab the frame from the threaded video stream, resize it to
	# have a maximum width of 400 pixels, and convert it to
	# grayscale
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect faces in the grayscale frame
	rects = detector(gray, 0)
	return (len(rects))
	
	#if len(rects) > 0:
	#	print("[INFO] Found %d faces!" %(len(rects)))
		#text = "{} face(s) found".format(len(rects))
		#cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
		#	0.5, (0, 0, 255), 2)
		

	# loop over the face detections
	#for rect in rects:
		# compute the bounding box of the face and draw it on the
		# frame
	#	(bX, bY, bW, bH) = face_utils.rect_to_bb(rect)
	#	cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH),
	#		(0, 255, 0), 1)

		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
	#	shape = predictor(gray, rect)
	#	shape = face_utils.shape_to_np(shape)

		# loop over the (x, y)-coordinates for the facial landmarks
		# and draw them on the image
	#	for (x, y) in shape:
	#		cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
	  
	# show the frame
	#cv2.imshow("Frame", frame)
	#key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	#if key == ord("q"):
	#	break
 
def CV_Cleanup():
	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()
