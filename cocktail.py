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
hx.set_reference_unit(-99.71)

###################################
# Setting up pumps

p1 = Pumpa(21, 'Rum')
p2 = Pumpa(20, 'Coke')
p3 = Pumpa(16, 'Lime')
pumps = [p1, p2, p3]
for pump in pumps:   # make sure all are turned off!!!
	pump.turnoff()

###################################
# Interface to RGB LED Ring
statusfile = "status.txt"

def MakeACocktail(personCtr):
	""" Make a cocktail depending on number of persons detected. """
	TIMEOUT = 100 		#if cocktail isn't done in this time, break the operation
	COCKTAIL_SIZE_MAX = 300
	f = open(statusfile, 'w')
	
	if (personCtr):
		f.write('Detected\0')
		f.close()
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
	
			print ("[INFO] Sipping %s. Required %d ml." % (pump.drink, pump.amount))
		
			while (  (current_amount < pump.amount) and 
				( (current_amount + cocktail_amount) < COCKTAIL_SIZE_MAX) and
				(  (time.time() - start_time) < TIMEOUT  )  ):
			
				current_amount = hx.get_weight(5)
				tot_amount = (current_amount + cocktail_amount)
		
				print ("[INFO] %s : %.1f ml. Total: %.1f ml. Cocktail %d %% done."  
					% (pump.drink, current_amount, tot_amount, int(tot_amount/(p1.amount + p2.amount + p3.amount)*100)))
	
			pump.turnoff()	
			cocktail_amount += current_amount	
			
		hx.power_down()
	
	else:
		f.write('\0')
		f.close()
		
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


	except (KeyboardInterrupt, SystemExit, RuntimeError, TypeError, NameError):
		print ("Cleaning...")
		for pump in pumps:
			pump.turnoff()
		GPIO.cleanup()
		CV_Cleanup()
		hx.power_down()
		print ("Bye!")
		sys.exit()



