import time
import board
import neopixel
import os
import wifi
import time
import rtc
import socketpool
import adafruit_ntp
import board
import adafruit_sht4x

wifi.radio.connect(
    os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD")
)
print(f"My IP address: {wifi.radio.ipv4_address}")

pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=0)

rtc.RTC().datetime = ntp.datetime

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

i2c = board.STEMMA_I2C()

sht = adafruit_sht4x.SHT4x(i2c)
print("Found SHT4x with serial number", hex(sht.serial_number))

sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
# Can also set the mode to enable heater
# sht.mode = adafruit_sht4x.Mode.LOWHEAT_100MS
print("Current mode is: ", adafruit_sht4x.Mode.string[sht.mode])

while True:
    print(time.time())
    pixel.fill((5, 0, 0))
    time.sleep(0.5)
    pixel.fill((0, 5, 0))
    time.sleep(0.5)
    pixel.fill((0, 0, 5))
    time.sleep(0.5)
    pixel.fill((0, 0, 0))
    time.sleep(0.5)

    temperature, relative_humidity = sht.measurements
    print("Temperature: %0.1f C" % temperature)
    print("Humidity: %0.1f %%" % relative_humidity)
    print("")
    time.sleep(1)
