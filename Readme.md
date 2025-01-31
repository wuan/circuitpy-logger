# circuitpy-logger

A sensor data logger for various I2C sensor devices for CircuitPython using MQTT.

## Supported sensors

* SHT4x Temperature / Humidity
* BME680 Temperature / Humidity / Pressure
* BMP3xx Pressure
* SCD4x CO2
* SGP40 VOC index (air quality)

more to come ...

## Compatibility

| CircuitPy version | Bundle release |
|-------------------|----------------|
| 8.x               | 20240423       |
| 9.x (9.2.4)       | 20250123       |

The installer `install.py` is configured to download and install the bundle release for CircuitPython 9.x by default.

## Color coding

| Step                  | Color       |
|-----------------------|-------------|
| WLAN connect          | yellow      |
| NTP update            | magenta     |
| MQTT connect / update | white       |
| Sensor detection      | cyan        |
| Sensor readout        | blue        | 
| Operation             | green - red |

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
| 68          | SHT4x       |
| 89          | SGP40       |
| 98          | SCD4x       |
| 119         | BMP3xx      |

As the address to sensor mapping might not be unique there can be an override through the configuration:

```
DEVICE_MAP="119=BME680"
```

mapping the real address to one of the supported sensor names: `SHT4x`, `SGP40`, `SCD4x`, `BMP3xx`, `BME680`.

## Installation

1. Download
   * dependency map `adafruit-circuitpython-bundle-YYYYMMDD.json`
   * module file archive `adafruit-circuitpython-bundle-8.x-mpy-YYYYMMDD.zip` 

   from https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases to the main folder.
2. Extract the module file archive in place.
3. Update the release name variable in `install.py`
4. run `./install.py` which will copy all relevant dependencies and the sources to `/Volumes/CIRCUITPY`