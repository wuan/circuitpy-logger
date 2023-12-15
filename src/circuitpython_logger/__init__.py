import os


class Config:

    @property
    def mqtt_host(self):
        return os.getenv("MQTT_HOST")

    @property
    def mqtt_port(self):
        return os.getenv("MQTT_PORT","1883")
