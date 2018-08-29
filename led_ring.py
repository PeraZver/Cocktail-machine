from neopixel import *
import time

class LED_RING:
	# LED strip configuration:
	LED_COUNT      = 16      # Number of LED pixels.
	LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
	#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
	LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
	LED_DMA        = 1      # DMA channel to use for generating signal (try 10)
	LED_BRIGHTNESS = 127    # Set to 0 for darkest and 255 for brightest
	LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
	LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
	
	def __init__(self):
		self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN,
			self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
		self.strip.begin()
		
	def colorWipe(self, color=Color(10, 0, 0), wait_ms=1):
		"""Wipe color across display a pixel at a time."""
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, color)
			self.strip.show()
			time.sleep(wait_ms/1000.0)

	def tail(self, tail_length=2, color=Color(127,127,127), wait_ms=50):
		"""Buffering animation."""
		for i in range(self.strip.numPixels() - tail_length/2):
			for j in range(self.strip.numPixels()):
				if (j in range(i, i + tail_length + 1)):
					self.strip.setPixelColor(j, color)
				else:
					self.strip.setPixelColor(j, 0) 	    					
			self.strip.show()
			time.sleep(wait_ms/1000.0)  
			
	def breathe(self, min_light=50, max_light=150, wait_ms=5):
		"""WTF ne radis """
		self.colorWipe()
		for i in range(min_light, max_light, 1):
			self.strip.setBrightness(i)
			self.strip.show()
			time.sleep(wait_ms/1000.0)
			
		for i in range(max_light, min_light, -1):
			self.strip.setBrightness(i)
			self.strip.show()
			time.sleep(wait_ms/1000.0)
	
	def cleanup(self):
		self.colorWipe(0)

