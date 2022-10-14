from collections import OrderedDict

import pytest
import requests
from assertpy import assert_that
from requests.models import PreparedRequest

from test.BaseTest import BaseTest


class TestApi(BaseTest):

    def test_devices_response(self):
        devices_list = self.get_list_of_devices()
        devices_names_list = list()
        for item in devices_list:
            devices_names_list.append(item.name)

        assert_that(devices_list, "collected not all existed devices").is_length(5)
        assert_that(devices_names_list).contains("Engine", "Power", "Transmission", "Brake", "Control")

    @pytest.mark.parametrize('device_address', ['4A', '65', '80', '3F', '40'])
    @pytest.mark.parametrize('device_duty1', [0, 1, 50, 100])
    @pytest.mark.parametrize('device_freq1', [1, 2, 5, 10, 20, 50, 100, 200, 500])
    def test_patch_request(self, device_address, device_duty1, device_freq1):
        patch_request = PreparedRequest()
        params = OrderedDict(
            address=device_address,
            duty1=device_duty1,
            freq1=device_freq1
        )
        patch_request.prepare_url(self.BASE_URL + self.DEVICES, params)
        patch_response = requests.patch(patch_request.url)

        assert_that(patch_response.status_code, 'Patch response status code is not 200.').is_equal_to(200)

        item = self.get_device_by_address(device_address)

        assert_that(item, f"Device with address {device_address} was not in list.").is_not_none()
        assert_that(item.pin_1_pwm_d, "Device duty1 not changed.").is_equal_to(device_duty1)
        assert_that(item.pin_1_pwm_f, "Device freq1 not changed.").is_equal_to(device_freq1)

    @pytest.mark.parametrize('device_address', ['4A', '65', '80', '3F', '40'])
    @pytest.mark.parametrize('device_duty1', [-1, 101])
    @pytest.mark.parametrize('device_freq1', [0, 400, -100])
    def test_patch_with_incorrect_params(self, device_address, device_duty1, device_freq1):
        device_before = self.get_device_by_name("Engine")
        patch_request = PreparedRequest()
        params = OrderedDict(
            address=device_address,
            duty1=device_duty1,
            freq1=device_freq1
        )
        patch_request.prepare_url(self.BASE_URL + self.DEVICES, params)
        patch_response = requests.patch(patch_request.url)

        # from my point of view, response status code should be 403 bad request
        assert_that(patch_response.status_code,
                    f'Patch response is not 400. Response status code {patch_response.status_code}')\
            .is_equal_to(200)

        device_after = self.get_device_by_address(device_address)
        assert_that(device_after.pin_1_pwm_f).is_equal_to(device_before.pin_1_pwm_f)
        assert_that(device_after.pin_1_pwm_d).is_equal_to(device_before.pin_1_pwm_d)

    @pytest.mark.parametrize('device_address', ['4A', '65', '80', '3F', '40'])
    @pytest.mark.parametrize('report_id', ['100', '200', '300', '400'])
    def test_report_request(self, device_address, report_id):
        request_params = {'address': device_address, 'repId': report_id}
        report_response = requests.get(self.BASE_URL + self.REPORT, params=request_params)

        assert_that(report_response.status_code, 'Report response status code is not 200 OK.').is_equal_to(200)
        assert_that(report_response.content).is_not_empty()
