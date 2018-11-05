# import the necessary packages
import time
import sys
from hx711 import HX711
from pumpe import Pumpa
import RPi.GPIO as GPIO
#from CV_stuff import *
from DLIB_stuff import *
#from NSFW_stuff import *

####################################
# Setting up scale

hx = HX711(5, 6)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(949.4)

###################################
# Setting up pumps

p1 = Pumpa(16, 'Rum')
p2 = Pumpa(20, 'Coke')
p3 = Pumpa(21, 'Lime')
pumps = [p1, p2, p3]

for pump in pumps:   # make sure all are turned off!!!
	pump.turnoff()

###################################
# Interface to RGB LED Ring
statusfile = "status.txt"

def MakeACocktail(personCtr):
	""" Make a cocktail depending on number of persons detected. """
	TIMEOUT = 100		#if cocktail isn't done in this time, break the operation
	COCKTAIL_SIZE_MAX = 300
	SLEEP_TIME = 10
	
	if (personCtr):
		f = open(statusfile, 'w')
		f.write('Detected\0')
		f.close()
		print ("[INFO] Giving you 3 sec to put a glass in the machine ...")
		hx.reset()
		time.sleep(3)
		cocktail_amount = 0
		
		# Turn on the pumps
		for pump in pumps:
			# Reset the scale
			
			hx.tare()
			current_amount, tot_amount = 0, 0
			start_time = time.time()
			pump.turnon()
	
			print ("[INFO] Sipping %s. Required %d ml." % (pump.drink, pump.amount))
		
			while (  (current_amount < pump.amount) and 
				( tot_amount < COCKTAIL_SIZE_MAX) and
				( (time.time() - start_time) < TIMEOUT )  ):
			
				current_amount = hx.get_weight(5)
				tot_amount = current_amount + cocktail_amount
				cocktail_percent = int(tot_amount/(p1.amount + p2.amount + p3.amount)*100)
		
				print ("[INFO] %s : %.1f ml. Total: %.1f ml. Cocktail %d %% done."  
					% (pump.drink, current_amount, tot_amount, cocktail_percent))
				
				f = open(statusfile, 'w')
				f.write('Percentage\n%d\0' % cocktail_percent)
				#f.write("%d" % cocktail_percent)
				#f.write("\0")
				f.close()	
				
	
			pump.turnoff()	
			cocktail_amount += current_amount	
			
		hx.power_down()
		
		f = open(statusfile, 'w')
		f.write('Wait\0')
		f.close()	
		
		print("Hold on a minute, alcoholic!")	
		time.sleep(SLEEP_TIME)
		print("Wait done. Going to detection mode.")

	f = open(statusfile, 'w')
	f.write('Idle\0')
	f.close()
		
# loop over the frames from the video stream
while True:
	try:
		
		# Make a cocktail
		MakeACocktail(CV_Detect())



	except (KeyboardInterrupt, SystemExit, RuntimeError, TypeError, NameError):
		raise
		print ("Cleaning...")
		for pump in pumps:
			pump.turnoff()
		GPIO.cleanup()
		f = open(statusfile, 'w')
		f.write('Wait\0')
		f.close()		
		CV_Cleanup()
		hx.power_down()
		print ("Bye!")
		sys.exit()



