from typing import List

from board import I2C


def scan(i2c_bus: I2C) -> List[int]:
    locked = i2c_bus.try_lock()

    if locked:
        devices = i2c_bus.scan()
        i2c_bus.unlock()
    else:
        devices = []

    return devices
