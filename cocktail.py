# import the necessary packages
import time
import sys
from hx711 import HX711
from pumpe import Pumpa
import RPi.GPIO as GPIO
from CV_stuff import *

####################################
# Setting up scale

hx = HX711(5, 6)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(99.85)

###################################
# Setting up pumps

p1 = Pumpa(21, 'Rum')
p2 = Pumpa(20, 'Coke')
p3 = Pumpa(16, 'Lime')
pumps = [p1, p2, p3]
for pump in pumps:   # make sure all are turned off!!!
	pump.turnoff()


def MakeACocktail(personCtr):
	""" Make a cocktail depending on number of persons detected. """
	TIMEOUT = 15 		#if cocktail isn't done in this time, break the operation
	COCKTAIL_SIZE = 300
	
	if (not personCtr):
		print (str(personCtr) + " persons detected!")
		print ("[INFO] Giving you 3 sec to put a glass in the machine ...")
		time.sleep(3)
		cocktail_amount = 0
		
		# Turn on the pumps
		for pump in pumps:
			# Reset the scale
			hx.reset()
			hx.tare()
			current_amount = 0
			start_time = time.time()
			pump.turnon()
			print ("[INFO] Sipping " + pump.drink)
			while (  (current_amount < pump.amount) and (  (time.time() - start_time) < TIMEOUT  )  ):
				current_amount = hx.get_weight(5)
				print ("[INFO] Weight: "+str(current_amount)+" g. Total weight: "
					+str(current_amount + cocktail_amount) + " g.")
	
			pump.turnoff()	
			cocktail_amount += current_amount	
			
		hx.power_down()
		
# loop over the frames from the video stream
while True:
	try:
		
		# Make a cocktail
		MakeACocktail(CV_Detect())


		# show the output frame
		#~ cv2.imshow("Frame", frame)
		#key = cv2.waitKey(1) & 0xFF
		
		# if the `q` key was pressed, break from the loop
		#if key == ord("q"):
		#    break
		
		# update the FPS counter


	except (KeyboardInterrupt, SystemExit):
		print ("Cleaning...")
		GPIO.cleanup()
		CV_Cleanup()
		hx.power_down()
		print ("Bye!")
		sys.exit()



