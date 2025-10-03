# circuitpy-logger

A sensor data logger for various I2C sensor devices for CircuitPython using MQTT.

## Supported sensors

* SHT4x Temperature / Humidity
* BME680 Temperature / Humidity / Pressure
* BMP3xx Pressure
* SCD4x CO2
* SGP40 VOC index (air quality)
* Light sensor (BH1750, VEML7700)
* Magnetometer MMC56x3

more to come ...

## Compatibility

| CircuitPy version | Bundle release |
|-------------------|----------------|
| 8.x               | 20240423       |
| 9.x (9.2.6)       | 20250224       |

The installer `install.py` is configured to download and install the bundle release for CircuitPython 9.x by default. Current bundle releases can be found [here](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases).

## Color coding

| Step                  | Color        |
|-----------------------|--------------|
| WLAN connect          | yellow       |
| NTP update            | magenta      |
| MQTT connect / update | white        |
| Sensor detection      | cyan         |
| Sensor readout        | blue         | 
| Operation             | green -> red |

## Example config

```
WIFI_SSID = "SSDF"
WIFI_PASSWORD = "XZCXCZXC"
MQTT_HOST="mqtt"
MQTT_PREFIX="sensors/test"
ELEVATION="530"
```

By default the following sensors are mapped to their default I2C addresses:

| I2C address | sensor name |
|-------------|-------------|
| 16          | VEML7700    |
| 35          | BH1750      |
| 48          | MMC56x3     |
| 68          | SHT4x       |
| 89          | SGP40       |
| 98          | SCD4x       |
| 119         | BMP3xx      |

As the address to sensor mapping might not be unique there can be an override through the configuration:

```
DEVICE_MAP="119=BME680"
```

mapping the real address to one of the supported sensor names: `SHT4x`, `SGP40`, `SCD4x`, `BMP3xx`, `BME680`, ...

## Installation

Run `./install.py` which will copy all relevant dependencies and the sources to `/Volumes/CIRCUITPY` when connecting a CircuitPython device.