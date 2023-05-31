# -*- coding: utf-8 -*-
"""Playwrightのデバイスのリストを取得するモジュール。

使い方:
    ```import util_device
    util_device.download_devices()
    device = util_device.random_device(os_name='Android') # os_name: 'iPhone', 'Desktop'
    specs = util_device.generate_device_specs() # Generate random RAM/Hardware Concurrency.
    ```
    


Todo:
    - download_devices
    
    

"""

import csv
import os
import random
import pysnooper
import json
from pprint import pprint
import requests

DEVICES_JSON_PATH = "devices.json"

def get_device_list(filepath=DEVICES_JSON_PATH):
    """JSON ファイルを読み込んで Python オブジェクトとして返します。"""
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), filepath))
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)
    
def filter_dict_list(dict_list, key):
    return list(filter(lambda x: key in x, dict_list))

def download_devices(filepath=DEVICES_JSON_PATH):
    """
    Downloads a list of proxies and saves it to a file named 'http.txt'.
    """
    response = requests.get('https://raw.githubusercontent.com/microsoft/playwright/main/packages/playwright-core/src/server/deviceDescriptorsSource.json')

    with open(filepath, 'wb') as f:
        f.write(response.content)


def random_device(os_name='Android'):
    # os_name: 'iPhone', 'Desktop'
    device_list = get_device_list()
    devices = [x for x,v in device_list.items() if os_name in v['userAgent']]
    return random.choice(devices)


def generate_device_specs():
    """
    Generate random RAM/Hardware Concurrency.

    Returns:
        Tuple[int, int]: A tuple containing a random RAM and hardware
        concurrency.
    """
    random_ram = random.choice([1, 2, 4, 8, 16, 32, 64])
    max_hw_concurrency = random_ram * 2 if random_ram < 64 else 64
    random_hw_concurrency = random.choice([1, 2, 4, max_hw_concurrency])
    return (random_ram, random_hw_concurrency)

if __name__ == '__main__':
    device_list = get_device_list()
    # download_devices(filepath='devices.json')
    import pdb;pdb.set_trace()
    