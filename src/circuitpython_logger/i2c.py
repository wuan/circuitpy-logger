import time

from board import I2C

from . import DataBuilder, Config
from .calc import TemperatureCalc, PressureCalc
from .measurements import Measurements
from .sensor.bh1750_sensor import BH1750Sensor
from .sensor.bme680_sensor import BME680Sensor
from .sensor.bmp3xx_sensor import BMP3xxSensor
from .sensor.mmc56x3_sensor import MMC56x3Sensor
from .sensor.scd4x_sensor import SCD4xSensor
from .sensor.sgp40_sensor import SGP40Sensor
from .sensor.sht4x_sensor import Sht4xSensor
from .sensor.veml7700_sensor import VEML7700Sensor


def scan(i2c_bus: I2C):
    lock_attempts = 0
    while not i2c_bus.try_lock():
        lock_attempts += 1

    if lock_attempts > 1:
        print(f"scan() attempts: {lock_attempts}")

    devices = i2c_bus.scan()

    i2c_bus.unlock()

    return devices


class Sensors:
    sensor_map = {
        SCD4xSensor.name: lambda i2c_bus, _: SCD4xSensor(i2c_bus),
        SGP40Sensor.name: lambda i2c_bus, _: SGP40Sensor(i2c_bus),
        Sht4xSensor.name: lambda i2c_bus, _: Sht4xSensor(i2c_bus, TemperatureCalc()),
        BMP3xxSensor.name: lambda i2c_bus, config: BMP3xxSensor(i2c_bus, config, PressureCalc()),
        BME680Sensor.name: lambda i2c_bus, config: BME680Sensor(i2c_bus, config, TemperatureCalc(), PressureCalc()),
        MMC56x3Sensor.name: lambda i2c_bus, _: MMC56x3Sensor(i2c_bus),
        VEML7700Sensor.name: lambda i2c_bus, _: VEML7700Sensor(i2c_bus),
        BH1750Sensor.name: lambda i2c_bus, _: BH1750Sensor(i2c_bus),
    }

    def __init__(self, config: Config, i2c_bus: I2C):
        self.config = config
        self.i2c_bus = i2c_bus
        self.sensors = []

        self.device_map = {
            16: VEML7700Sensor.name,
            35: BH1750Sensor.name,
            48: MMC56x3Sensor.name,
            68: Sht4xSensor.name,
            89: SGP40Sensor.name,
            98: SCD4xSensor.name,
            119: BMP3xxSensor.name,
        }
        device_map = config.device_map
        if device_map:
            self.device_map.update(device_map)

        self.scan_devices()

    def scan_devices(self):
        sensors_in_use = {sensor.name for sensor in self.sensors}

        device_addresses = scan(self.i2c_bus)
        sensors_found = {self.device_map[device_address] for device_address in device_addresses if
                         device_address in self.device_map}
        unknown_sensors_found = {str(device_address) for device_address in device_addresses if
                                 device_address not in self.device_map}
        if unknown_sensors_found:
            print("Could not find sensors for addresses:", ", ".join(unknown_sensors_found))

        if sensors_in_use != sensors_found:

            sensors = [sensor for sensor in self.sensors if sensor.name in sensors_found]
            for sensor_name in sensors_found.difference(sensors_in_use):
                if sensor_name in self.sensor_map:
                    sensor = self.sensor_map[sensor_name]
                    sensors.append(sensor(self.i2c_bus, self.config))

            sensors.sort(key=lambda sensor: sensor.priority)

            print("updated sensors:")
            for sensor in sensors:
                print("  ", sensor.name, sensor.priority)

            self.sensors = sensors

    def measure(self, data_builder = None):
        if data_builder is None:
            data_builder = DataBuilder()
        measurements = Measurements()

        for sensor in self.sensors:
            start_time = time.monotonic_ns()
            sensor.measure(data_builder, measurements)
            end_time = time.monotonic_ns()
            data_builder.add(sensor.name, "time", "ms", (end_time - start_time) / 1e6)

        return data_builder.data
