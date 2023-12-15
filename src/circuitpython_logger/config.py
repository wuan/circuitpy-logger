import os


class Config:

    @property
    def mqtt_host(self):
        return os.getenv("MQTT_HOST")

    @property
    def mqtt_port(self):
        return os.getenv("MQTT_PORT", "1883")

    @property
    def location_name(self):
        return os.getenv("LOCATION_NAME")

    @property
    def elevation(self):
        return int(os.getenv("ELEVATION", "0"))
