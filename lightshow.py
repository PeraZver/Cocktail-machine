import time
from neopixel import *
from led_ring import LED_RING

led = LED_RING()

# Main program logic follows:
if __name__ == '__main__':
    try:
        while True:
			f = open("status.txt", 'r')
			if (f.readline() == 'Detected\0'):
				led.breathe()
			else:
				led.tail(tail_length=1)
			f.close()

    except KeyboardInterrupt:
        led.cleanup()
        f.close()
