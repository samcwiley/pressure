import time
from bmp280 import BMP280
from smbus import SMBus
from gpiozero import Button, LED
import csv
import statistics
import numpy as np

#LED to gpio 19 (pin 35), button to gpio 26 (pin 37)
bus = SMBus(1)
bmp280 = BMP280(i2c_dev = bus)
button = Button(26)
led = LED(19)
time.sleep(1)
tare = bmp280.get_pressure()
cf = 1/2.491 #2.491 hPa in 1 inch water column

x = 0
print("waiting")
while bmp280.get_pressure() < 1000 and not button.is_pressed:
	x = x+1
	if x == 10:
		led.on()
	if x == 20:
		led.off()
		x = 0
	time.sleep(0.01)

file = open('pressureData.csv', 'w')
writer = csv.writer(file)
led.on()
time.sleep(1)
data = np.array()
x = 0
while not button.is_pressed:
	pressure = bmp280.get_pressure()
	writer.writerow([x,pressure])
	if x%10 == 0:
		print(pressure)
		data.append(pressure)
	time.sleep(0.01)
	x = x+1

print("Stopped")
file.close()

print("Average Pressure: ", data.min(), " in. H2O")
print("Max Pressure: ", max(data), " in. H2O")
print("Min Pressure: ", min(data), " in. H2O")
