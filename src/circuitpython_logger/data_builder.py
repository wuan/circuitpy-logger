import time

from . import Config


class DataBuilder:
    def __init__(self, configuration: Config):
        self.location = configuration.location_name
        self.timestamp = time.time()
        self.data = []

    def add(self, sensor: str, measurement_type: str, measurement_unit: str, measurement_value: float,
            is_calculated: bool = False):
        if measurement_value is not None:
            self.data += [self.create(sensor, measurement_type, measurement_unit, measurement_value, is_calculated)]

    def create(self, sensor: str, measurement_type: str, measurement_unit: str, measurement_value: float,
               is_calculated: bool = False):
        return {
            "measurement": "data",
            "tags": {
                "location": self.location,
                "type": measurement_type,
                "unit": measurement_unit,
                "sensor": sensor,
                "calculated": is_calculated
            },
            "time": self.timestamp,
            "fields": {
                "value": measurement_value
            }
        }
