from gpiozero import Button, LED
from time import sleep

#ground pin 39
#Button 26 is GPIO pin 37
#LED 19 is pin 35
button = Button(26)
led = LED(19)

while True:
	if button.is_pressed:
		led.on()
	else:
		led.off()

