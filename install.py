#!/usr/bin/env python3
import json
import os.path
import pathlib
import shutil
from collections import deque

base_path = "./"
base_name = "adafruit-circuitpython-bundle"
t release_date = "20240423"
circuitpython_version = "8.x"
# release_date = "20241128"
# circuitpython_version = "9.x"

#
# curl -s https://api.github.com/repos/adafruit/Adafruit_CircuitPython_Bundle/releases/latest | grep browser_download_url | cut -d '"' -f 4
#

import zipfile
import requests

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


# Download the file from a given URL
def download_file(url, local_path):
    """Download a file from a URL to a local path."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(local_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        print(f"Failed to download file: status code {response.status_code}")
        
def download_url(release_date: str, file_name: str):
    return f"https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/{release_date}/{file_name}"


target_path = "/Volumes/CIRCUITPY"

if __name__ == "__main__":

    bundle_catalog = f"{base_name}-{release_date}.json"
    if not os.path.exists(bundle_catalog):
       download_file(download_url(release_date, bundle_catalog), bundle_catalog)

    bundle_folder = f"{base_name}-{circuitpython_version}-mpy-{release_date}"
    bundle_archive = f"{bundle_folder}.zip"
    if not os.path.exists(bundle_folder):
        download_file(download_url(release_date, bundle_archive), bundle_archive)
        with zipfile.ZipFile(bundle_archive, 'r') as zip_ref:
            zip_ref.extractall(".")
    

    with open(os.path.join(base_path, bundle_catalog), "r") as catalog_file:
        catalog_data = json.loads(catalog_file.read())

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

    pypi_map = {value["pypi_name"]: key for key, value in catalog_data.items()}

    dependency_queue = deque([pypi_map[pypi_dependency] for pypi_dependency in pypi_dependencies])
    dependencies = set()
    while True:
        if not dependency_queue:
            break
        dependency = dependency_queue.pop()

        dependency_data = catalog_data[dependency]
        data_dependencies = dependency_data["dependencies"]
        print(f"{dependency}: {dependency_data}")

        dependency_queue += data_dependencies
        dependencies.add(dependency)

    print(dependencies)

    log.info("cleaning up existing files")

    main_code = os.path.join(target_path, "code.py")
    if os.path.exists(main_code):
        os.remove(main_code)
    shutil.rmtree(os.path.join(target_path, "lib"), ignore_errors=True)


    os.makedirs(os.path.join(target_path, "lib"), exist_ok=True)
    bundle_base_path = os.path.join(base_path, f"{base_name}-{circuitpython_version}-mpy-{release_date}")
    for dependency in dependencies:
        if dependency in catalog_data:
            entry = catalog_data[dependency]
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
    shutil.rmtree(os.path.join(target_path, "lib", "circuitpython_logger"), ignore_errors=True)
    shutil.copytree(src_path / "circuitpython_logger", os.path.join(target_path, "lib", "circuitpython_logger"))
    shutil.copyfile(src_path / "code.py", main_code)

