import adafruit_minimqtt.adafruit_minimqtt as MQTT
from socketpool import SocketPool

from . import Config


def connect(mqtt_client, userdata, flags, rc):
    print(f"Connected to MQTT Broker. flags {flags}, RC: {rc}")


def disconnect(mqtt_client, userdata, rc):
    # This method is called when the mqtt_client disconnects
    # from the broker.
    print("Disconnected from MQTT Broker!")


def subscribe(mqtt_client, userdata, topic, granted_qos):
    # This method is called when the mqtt_client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


def unsubscribe(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client unsubscribes from a feed.
    print("Unsubscribed from {0} with PID {1}".format(topic, pid))


def publish(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client publishes data to a feed.
    print("Published to {0} with PID {1}".format(topic, pid))


def message(client, topic, message):
    print("New message on topic {0}: {1}".format(topic, message))


class MQTTClient:

    def __init__(self, pool: SocketPool, config: Config):
        self.mqtt_client = MQTT.MQTT(
            broker=config.mqtt_host,
            port=config.mqtt_port,
            client_id=config.location_name,
            socket_pool=pool,
            is_ssl=False,
        )

        # Connect callback handlers to mqtt_client
        self.mqtt_client.on_connect = connect
        self.mqtt_client.on_disconnect = disconnect
        self.mqtt_client.on_subscribe = subscribe
        self.mqtt_client.on_unsubscribe = unsubscribe
        self.mqtt_client.on_message = message

        # self.io = IO_MQTT(mqtt_client)

    def publish(self, topic: str, message: str):
        try:
            self.mqtt_client.publish(topic, message, qos=1, retain=False)
        except OSError as e:
            print("Exception:", type(e), e)
            try:
                reconnect = self.mqtt_client.reconnect(False)
                print(f"Reconnecting to MQTT: {reconnect}")
            except:
                pass
        except MQTT.MMQTTException as e:
            print("Exception:", type(e), e)


    def connect(self):
        self.mqtt_client.connect()
