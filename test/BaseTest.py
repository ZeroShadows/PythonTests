from abc import ABC

import requests

from model.api.Device import Device


class BaseTest(ABC):
    BASE_URL = "http://localhost:5585"
    DEVICES = "/devices"
    REPORT = "/report"

    def get_list_of_devices(self) -> list:
        response = requests.get(self.BASE_URL + self.DEVICES).json()
        devices_list = list()
        for device in response:
            devices_list.append(Device.from_dict(device))

        return devices_list

    def get_device_by_name(self, device_name) -> Device:
        device_list = self.get_list_of_devices()
        item = None
        for device in device_list:
            if device.name == device_name:
                item = device
        return item

    def get_device_by_address(self, device_address) -> Device:
        device_list = self.get_list_of_devices()
        item = None
        for device in device_list:
            if device.address == device_address:
                item = device
        return item
