import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(19,GPIO.OUT)

#GPIO PIN 19 corresponds to pin 35 on raspberry pi zero
#Pin 39- ground, connects to anode of LED
#Cathode of LED goes to resistor (360 ohm here)
#Resistor goes to GPIO 19

for x in range(20):
	print "LED on"
	GPIO.output(19,GPIO.HIGH)
	time.sleep(1)
	print "LED off"
	GPIO.output(19,GPIO.LOW)
	time.sleep(1)
