import json
import os
import time

import adafruit_ntp
import board
import neopixel
import rtc
import socketpool
import wifi

from circuitpython_logger import Config
from circuitpython_logger.i2c import Sensors
from circuitpython_logger.mqtt import MQTTClient

wifi.radio.connect(
    os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD")
)
print(f"My IP address: {wifi.radio.ipv4_address}")

pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=0)

rtc.RTC().datetime = ntp.datetime

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

i2c_bus = board.STEMMA_I2C()
config = Config()
sensors = Sensors(config, i2c_bus)

mqtt = MQTTClient(pool, config)
print("connecting to MQTT server")
mqtt.connect()

period = 10
next_time = 0
while True:
    monotonic_time = time.monotonic()
    if monotonic_time >= next_time:
        pixel.fill((0, 5, 5))
        sensors.scan_devices()

        pixel.fill((0, 0, 5))
        timestamp = time.time()
        data = sensors.measure()
        print("###", timestamp)
        for entry in data:
            timestamp = entry["time"]
            value = entry["fields"]["value"]

            tags = entry["tags"]
            measurement_type = tags["type"]
            unit = tags["unit"]
            topic = f"{config.mqtt_prefix}/{measurement_type}"
            print(f"{topic}: {value} {unit}")

            mqtt.publish(topic, json.dumps({
                "time": timestamp,
                "value": value,
                "unit": unit,
                "calculated": tags["calculated"]
            }))

        print()
        next_time = monotonic_time + period

        pixel.fill((0, 5, 0))
    time.sleep(0.1)
