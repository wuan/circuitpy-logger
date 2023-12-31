import json
import os
import time

import board
import neopixel
import socketpool
import wifi

from circuitpython_logger import Config, DataBuilder
from circuitpython_logger.data_builder import map_entry
from circuitpython_logger.i2c import Sensors
from circuitpython_logger.mqtt import MQTTClient
from circuitpython_logger.ntp import Ntp

start_time = time.monotonic_ns()

wifi.radio.connect(
    os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD")
)
print(f"My IP address: {wifi.radio.ipv4_address}")

pool = socketpool.SocketPool(wifi.radio)

ntp = Ntp(pool)
ntp.update_time()

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

i2c_bus = board.STEMMA_I2C()
config = Config()
sensors = Sensors(config, i2c_bus)

mqtt = MQTTClient(pool, config)
mqtt.connect()

period = 15
time_sync_period = 60 * 60
last_time_sync = time.monotonic()
last_time = 0
last_second = 0

from microcontroller import watchdog as w
from watchdog import WatchDogMode

w.timeout = 30
w.mode = WatchDogMode.RESET

data_builder = DataBuilder()
end_time = time.monotonic_ns()
data_builder.add("boot", "time", "ms", (end_time - start_time) / 1e6)
topic, data = map_entry(config.mqtt_prefix, data_builder.data[0])
mqtt.publish(topic, json.dumps(data))

while True:
    w.feed()
    monotonic_time = time.monotonic()
    seconds_difference = monotonic_time - last_time
    if seconds_difference >= period:
        pixel.fill((0, period, period))
        sensors.scan_devices()

        pixel.fill((0, 0, period))
        timestamp = time.time()
        data = sensors.measure()
        for entry in data:
            topic, data = map_entry(config.mqtt_prefix, entry)
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

    if monotonic_time - last_time_sync > time_sync_period:
        last_time_sync = monotonic_time
        ntp.update_time()

    time.sleep(0.1)
