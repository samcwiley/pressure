import time
from bmp280 import BMP280
from smbus import SMBus

bus = SMBus(1)
bmp280 = BMP280(i2c_dev = bus)

bmp280.sea_level_pressure = 1013.25

while True:
	print("\n Temperature: %0.1f C" % bmp280.get_temperature())
	print("Pressure: %0.1f hPa" % bmp280.get_pressure())
	print("Altitude = %0.2f meters" % bmp280.get_altitude())
	time.sleep(2)
