import json
import os
import time

import board
import microcontroller
import socketpool
import wifi

from circuitpython_logger import Config, DataBuilder
from circuitpython_logger.data_builder import map_entry
from circuitpython_logger.device.ntp import Ntp
from circuitpython_logger.device.pixel import Pixel
from circuitpython_logger.i2c import Sensors
from circuitpython_logger.mqtt import MQTTClient


def create_watchdog():
    from microcontroller import watchdog as w
    from watchdog import WatchDogMode
    w.timeout = 30
    w.mode = WatchDogMode.RESET
    return w


def wifi_connect(wifi):
    print("connect to WLAN")
    try:
        wifi.radio.connect(
            os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD")
        )
        print(f"IP address: {wifi.radio.ipv4_address}")
    except Exception as e:
        print("wifi_connect() failed:", e)


def mqtt_connect(mqtt):
    print("connect to MQTT")
    try:
        mqtt.connect()
    except Exception as e:
        print("mqtt reconnect failed:", e)


try:
    w = create_watchdog()

    period = 15
    pixel = Pixel(period, period / 5.0)

    pixel.wlan()
    start_time = time.monotonic_ns()

    wifi_connect(wifi)

    pool = socketpool.SocketPool(wifi.radio)

    pixel.ntp()
    print("fetch network time")
    ntp = Ntp(pool)
    ntp.update_time()

    config = Config()

    pixel.mqtt()
    print("Create MQTT client")
    try:
        mqtt = MQTTClient(pool, config)
    except Exception as e:
        print("mqtt setup failed:", e)
        microcontroller.reset()
    mqtt_connect(mqtt)

    pixel.sensors()
    print("setup I2C sensors")
    try:
        i2c_bus = board.STEMMA_I2C()
    except Exception as e:
        print("i2c setup failed:", e)
    sensors = Sensors(config, i2c_bus)

    print("start measurement")
    time_sync_period = 60 * 60
    last_time_sync = time.monotonic()
    last_time = 0
    last_second = 0

    data_builder = DataBuilder()
    end_time = time.monotonic_ns()
    data_builder.add("boot", "time", "ms", (end_time - start_time) / 1e6)
    topic, data = map_entry(config.mqtt_prefix, data_builder.data[0])
    mqtt.publish(topic, json.dumps(data))

    ignore_count = 1

    while True:
        wifi_connected = wifi.radio.connected
        mqtt_connected = mqtt.mqtt_client.is_connected()

        if wifi_connected and mqtt_connected:
            w.feed()
        else:
            pixel.wlan()
            if not wifi_connected:
                wifi_connect(wifi)
            if not mqtt_connected:
                mqtt_connect(mqtt)

        monotonic_time = time.monotonic()
        seconds_difference = monotonic_time - last_time
        if seconds_difference >= period:
            pixel.scan()
            sensors.scan_devices()

            pixel.measure()
            timestamp = time.time()

            data_builder = DataBuilder()
            api_info = wifi.radio.ap_info
            data_builder.add("wifi", "rssi", None, api_info.rssi)
            data_builder.add("wifi", "channel", None, api_info.channel)
            data_builder.add("cpu", "system", "°C", microcontroller.cpu.temperature)
            data = sensors.measure(data_builder)

            if ignore_count == 0:
                pixel.mqtt()
                for entry in data:
                    topic, data = map_entry(config.mqtt_prefix, entry)
                    mqtt.publish(topic, json.dumps(data))
            else:
                print(f"skipping {ignore_count}")
                ignore_count -= 1

            print()
            last_time = monotonic_time
            pixel.done()
        else:
            current_second = time.time()
            if current_second - last_second > 0:
                value = int(seconds_difference)
                pixel.progress(value)
                data = sensors.measure()
                if len(data) == 0:
                    print("WARNING: no measurements")
                last_second = current_second

        if monotonic_time - last_time_sync > time_sync_period:
            last_time_sync = monotonic_time
            ntp.update_time()

        time.sleep(0.25)
except KeyboardInterrupt:
    raise
except:
    import supervisor

    supervisor.reload()
