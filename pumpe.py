import RPi.GPIO as GPIO
#from gpiozero import LED

class Pumpa: 
	drink_amounts = {
		'Rum': 100,
		'Coke': 200,
		'Lime': 50,
		'Gin' : 100,
		'Tonic' : 200 }		
	
	def __init__(self, pin, drink):
		self.pin = pin
		self.drink = drink
		
		self.amount = self.drink_amounts[self.drink]
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin, GPIO.OUT)
	
	def turnon(self):
		GPIO.output(self.pin, True)
	
	def turnoff(self):
		GPIO.output(self.pin, False)
		
		
		