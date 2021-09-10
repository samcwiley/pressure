import time
from bmp280 import BMP280
from smbus import SMBus
from gpiozero import Button, LED
import csv
import numpy as np
import statistics

#start OLED init
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

RST = None
DC = 23
SPI_PORT = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = -2
top = padding
bottom = height-padding
x = 0
font = ImageFont.load_default()
#end OLED init

#-----------_WIRING------------

#LED (green) to gpio 19 (pin 35),
# button (blue) to gpio 26 (pin 37)
#Ground (black) to pin 39
#VCC/power (red) to 3V3 pin(1)
#SDA (white) to GPIO 2 (pin 3)
#SCL (yellow) to GPIO 3 (pin 5)


bus = SMBus(1)
bmp280 = BMP280(i2c_dev = bus)
button = Button(26)
led = LED(19)
data = []
cf = 1/2.491 #1 inch water per 2.491 hPa
threshold = 1000 #ambient hPa ~ 900

tare = bmp280.get_pressure()
print("{:.2f}".format(tare) + "hPa")
print("{:.2f}".format(tare*cf) + "in H2O")


#----------------- Splash Screen--------------
print("Splash screen")
for i in range(20):
	draw.rectangle((0,0,width,height), outline = 0, fill=0)
	draw.text((x, top), 	"Piping Precision", font=font, fill=255)
	draw.text((x, top + 8),	"Version 4", font=font, fill=255)
	draw.text((x, top + 16),"Wiley & Miller", font=font, fill=255)
	
	disp.image(image)
	disp.display()
	time.sleep(.1)
print ("splash ended")

#---------------Waiting Loop----------------
print("waiting loop begin")

draw.rectangle((0,0,width,height), outline = 0, fill=0)
draw.text((x, top), 	"Begin playing to", font=font, fill=255)
draw.text((x, top + 8),	"Start session", font=font, fill=255)	
disp.image(image)
disp.display()

i = 0 
while bmp280.get_pressure() < threshold and not button.is_pressed:
	i = i+1
	if i == 5:
		led.on()
	if i == 10:
		led.off()
		i = 0
#	draw.rectangle((0,0,width,height), outline = 0, fill=0)
#	draw.text((x, top), 	"Begin playing to", font=font, fill=255)
#	draw.text((x, top + 8),	"Start session", font=font, fill=255)
	
#	disp.image(image)
#	disp.display()
	time.sleep(.1)
print("waiting loop end")

#init
file = open('pressureData.csv', 'w')
writer = csv.writer(file)
led.on()
#time.sleep(1)

draw.rectangle((0,0,width,height), outline = 0, fill=0)
draw.text((x, top), 	"Current Pressure:", font=font, fill=255)
#	draw.text((x, top + 8),	"Start session", font=font, fill=255)
disp.image(image)
disp.display()


#----------- MAIN LOOP -------------#
i = 0
while not button.is_pressed:
	pressure = (bmp280.get_pressure()-tare)*cf
	writer.writerow([i,pressure])
	if i%10 == 0:
		print(pressure)
		data.append(pressure)
		
		draw.rectangle((x, top + 8, width, top + 16), outline = 0, fill = 0)
		draw.text((x, top + 8), "{:.2f}".format(pressure + i), font=font, fill=255)
		disp.image(image)
		disp.display()
#	time.sleep(0.01)
	i = i+1





#data = [(j-tare)*cf for j in data]
print("Stopped")
file.close()

avgP = statistics.mean(data)
minP = min(data)
maxP = max(data)

avgPdisp = "{:.2f}".format(avgP)
minPdisp = "{:.2f}".format(minP)
maxPdisp = "{:.2f}".format(maxP)

print("Average pressure: ", avgPdisp, " in. H2O")
print("Max pressure: ", maxPdisp, " in. H2O")
print("Min pressure: ", minPdisp, " in. H2O")

while True:
	draw.rectangle((0,0,width,height), outline = 0, fill=0)
	draw.text((x, top), 	"Average: " + avgPdisp, font=font, fill=255)
	draw.text((x, top + 8),	"Min: " + minPdisp, font=font, fill=255)
	draw.text((x, top + 16),"Max: " + maxPdisp, font=font, fill=255)
	
	disp.image(image)
	disp.display()
	time.sleep(.1)

