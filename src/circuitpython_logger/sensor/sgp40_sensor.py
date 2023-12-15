# -*- coding: utf8 -*-

import adafruit_sgp40
import busio

from ..data_builder import DataBuilder
from ..measurements import Measurements


class SGP40Sensor:
    name = "SGP40"
    priority = 3

    def __init__(self, i2c_bus: busio.I2C):
        self.driver = adafruit_sgp40.SGP40(i2c_bus)

    def measure(self, data_builder: DataBuilder, measurements: Measurements) -> None:
        voc_index = None
        if measurements.temperature is not None and measurements.relative_humidity is not None:
            raw_gas = self.driver.measure_raw(
                temperature=measurements.temperature, relative_humidity=measurements.relative_humidity
            )
            voc_index = self.driver.measure_index(
                temperature=measurements.temperature, relative_humidity=measurements.relative_humidity)
        else:
            raw_gas = self.driver.raw

        data_builder.add(self.name, "raw gas", "", float(raw_gas))
        if voc_index is not None:
            data_builder.add(self.name, "VOC index", "", float(voc_index))
