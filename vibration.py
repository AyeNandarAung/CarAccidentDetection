
import RPi.GPIO as GPIO
import time
channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN)
def callback(channel):
	if GPIO.input(channel):
		vibration=1
		print (vibration)
	else:
		vibration=0
		print(vibration)
GPIO.add_event_detect(channel,GPIO.BOTH,bouncetime=300)
GPIO.add_event_callback(channel,callback)
while True:
	#GPIO.add_event_callback(channel,callback)

	time.sleep(1)
