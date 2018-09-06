import time
from neopixel import *
from led_ring import LED_RING

led = LED_RING()

# Main program logic follows:
if __name__ == '__main__':
    try:
        while True:
			f = open("status.txt", 'r')
			msg = f.readline()
			if (msg == 'Detected\0'):
				led.breathe()
			elif (msg == 'Wait\0'):
				led.breathe_wait()
			else:
				led.tail(tail_length=5)
			f.close()
			#time.sleep(1)

    except KeyboardInterrupt:
        led.cleanup()
        f.close()
