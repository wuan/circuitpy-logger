# circuitpy-logger

A sensor data logger for various I2C sensor devices for CircuitPython using MQTT.

## Supported sensors

* SHT4x Temperature / Humidity
* BME680 Temperature / Humidity / Pressure
* Pressure Sensors (BMP3xx, DPS310)
* SCD4x CO2
* SGP40 VOC index (air quality)
* Light sensors (BH1750, VEML7700, TSL2591)
* Magnetometer MMC56x3
* Air quality (PM2.5)

more to come ...

## Compatibility

| CircuitPy version | Bundle release |
|-------------------|----------------|
| 8.x               | 20240423       |
| 9.x (9.2.6)       | 20251003       |
| 10.x (10.0.1)     | 20251010       |

The installer `install.py` is configured to download and install the bundle release for CircuitPython 10.x by default. Current bundle releases can be found [here](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases).

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
MQTT_HOST = "mqtt"
MQTT_PREFIX = "sensors/test"
ELEVATION = q"530"
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
DEVICE_MAP = "119=BME680"
```

mapping the real address to one of the supported sensor names: `SHT4x`, `SGP40`, `SCD4x`, `BMP3xx`, `BME680`, ...

## Installation

Connect a Circuitpython device so that `/Volumes/CIRCUITPY` is mounted.

### Update Circuitpython

Press and hold BOOT button and press reset to get into bootloader mode.

Run

```
esptool write-flash -e 0 ~/Downloads/adafruit-circuitpython-adafruit_qtpy_esp32s2-en_US-10.0.3.bin
```

### Update dependencies

```aiignore
circup install -r requirements_cpy.txt
```

### Install software

Run `./install.py` which will copy the sources
