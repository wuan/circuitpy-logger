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

ntp_server = os.getenv("NTP_SERVER")
kwargs = {}
if ntp_server:
    print(f"using NTP Server: {ntp_server}")
    kwargs = {"server": ntp_server}

ntp = adafruit_ntp.NTP(pool, tz_offset=0, **kwargs)

rtc.RTC().datetime = ntp.datetime

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

i2c_bus = board.STEMMA_I2C()
config = Config()
sensors = Sensors(config, i2c_bus)

mqtt = MQTTClient(pool, config)
mqtt.connect()

period = 15
last_time = 0
last_second = 0

from microcontroller import watchdog as w
from watchdog import WatchDogMode

w.timeout = 10
w.mode = WatchDogMode.RAISE


def map_entry(entry):
    timestamp = entry["time"]
    value = entry["fields"]["value"]
    tags = entry["tags"]
    measurement_type = tags["type"]
    unit = tags["unit"]
    sensor = tags["sensor"]
    topic = f"{config.mqtt_prefix}/{measurement_type}"
    print(f"{topic}: {value} {unit} ({sensor})")
    return (topic, {
        "time": timestamp,
        "value": value,
        "unit": unit,
        "sensor": sensor,
        "calculated": tags["calculated"]
    })


while True:
    monotonic_time = time.monotonic()
    seconds_difference = monotonic_time - last_time
    if seconds_difference >= period:
        pixel.fill((0, period, period))
        sensors.scan_devices()

        pixel.fill((0, 0, period))
        timestamp = time.time()
        data = sensors.measure()
        for entry in data:
            topic, data = map_entry(entry)
            mqtt.publish(topic, json.dumps(data))

        print()
        last_time = monotonic_time

        pixel.fill((0, period, 0))
    else:
        current_second = time.time()
        if current_second - last_second > 0:
            value = int(seconds_difference)
            pixel.fill((value, period - value, 0))
            sensors.measure()
            last_second = current_second
    time.sleep(0.1)
    w.feed()
