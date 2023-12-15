from . import Config


class MqttClient:

    def __init__(self, pool: SocketPool, config: Config):
        mqtt_client = MQTT.MQTT(
            broker=config.mqtt_host,
            port=config.mqtt_port,
            socket_pool=pool,
            is_ssl=False,
        )

        io = IO_MQTT(mqtt_client)