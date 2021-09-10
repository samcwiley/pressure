from gpiozero import Button, LED
from time import sleep

button1 = Button(2)
button2 = Button(4)
led = LED(19)

#check pinout for pins corresponding to GPIO 2,4,19

button.wait_for_press()
led.on()
print('button pressed')
sleep(3)
print('LED off')
led.off()
