#!/usr/bin/env python3
import json
import os.path
import pathlib
import shutil
from collections import deque

base_path = os.path.expanduser("~/Downloads/")
base_name = "adafruit-circuitpython-bundle"
release_name = "20231210"
circuitpython_version = "8.x"

target_path = "/Volumes/CIRCUITPY"

if __name__ == "__main__":

    with open(os.path.join(base_path, f"{base_name}-{release_name}.json"), "r") as config_file:
        data = json.loads(config_file.read())

    pypi_dependencies = [
        "adafruit-circuitpython-requests",
        "adafruit-circuitpython-minimqtt",
        "adafruit-circuitpython-ntp",
        "adafruit-circuitpython-adafruitio",
        "adafruit-circuitpython-scd4x",
        "adafruit-circuitpython-sgp40",
        "adafruit-circuitpython-sht4x",
        "adafruit-circuitpython-bmp3xx",
        "adafruit-circuitpython-bme680",
        "adafruit-circuitpython-neopixel",
    ]

    pypi_map = {value["pypi_name"]: key for key, value in data.items()}

    dependency_queue = deque([pypi_map[pypi_dependency] for pypi_dependency in pypi_dependencies])
    dependencies = set()
    while True:
        if not dependency_queue:
            break
        dependency = dependency_queue.pop()

        dependency_data = data[dependency]
        data_dependencies = dependency_data["dependencies"]
        print(f"{dependency}: {dependency_data}")

        dependency_queue += data_dependencies
        dependencies.add(dependency)

    print(dependencies)

    bundle_base_path = os.path.join(base_path, f"{base_name}-{circuitpython_version}-mpy-{release_name}")
    for dependency in dependencies:
        if dependency in data:
            entry = data[dependency]
            file_name = entry["path"] + ".mpy"
            module_base_path = os.path.join(bundle_base_path, entry["path"])
            if os.path.exists(module_base_path + ".mpy"):
                print(f"copy {dependency} module")
                shutil.copyfile(module_base_path + ".mpy", os.path.join(target_path, file_name))
            else:
                module_target_path = os.path.join(target_path, entry["path"])
                shutil.rmtree(module_target_path, ignore_errors=True)
                shutil.copytree(module_base_path, module_target_path)

    src_path = pathlib.Path(__file__).parent.resolve() / "src"
    shutil.copyfile(src_path / "code.py", os.path.join(target_path, "code.py"))
    shutil.rmtree(os.path.join(target_path, "circuitpython_logger"), ignore_errors=True)
    shutil.copytree(src_path / "circuitpython_logger", os.path.join(target_path, "circuitpython_logger"))

