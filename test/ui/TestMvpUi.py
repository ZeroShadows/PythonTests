import pytest
from assertpy import assert_that

from model.ui.DiagnosticsPage import DiagnosticsPage
from model.ui.MainPage import MainPage
from model.ui.MonitoringPage import MonitoringPage
from test.BaseTest import BaseTest


class TestMvpUi(BaseTest):
    MONITORING_BUTTON = 'Monitoring'
    DIAGNOSTICS_BUTTON = 'Diagnostics'

    def test_main_page(self, browser):
        main_page = MainPage(browser)
        main_page.go_to_site()
        table_header = main_page.get_table_header()
        header_names = [header_name.text for header_name in table_header]

        assert_that(header_names).contains('Name', 'Type', 'Address', 'Monitoring', 'Diagnostics')

        table_content = main_page.get_table_content()
        devices_list = self.get_list_of_devices()

        assert_that(len(table_content)).is_length(len(devices_list))
        for device in devices_list:
            assert_that(table_content[device.name]).contains(device.address, device.type)

        for item in table_content.values():
            assert_that(item).contains('Monitoring', 'Diagnostics')

    @pytest.mark.parametrize('device_address', ['4A', '65', '3F', '80'])
    @pytest.mark.parametrize('card_name', ['Pin 2', 'Pin 3'])
    def test_monitoring_page(self, browser, device_address, card_name):
        main_page = MainPage(browser)
        monitoring_page = MonitoringPage(browser)
        main_page.go_to_site()

        monitoring_button = main_page.get_button_by_device_address(device_address, self.MONITORING_BUTTON)
        monitoring_button.click()

        assert_that(monitoring_page.get_displayed_cards()).is_length(3)

        card = monitoring_page.get_card_by_header_name(card_name)
        monitoring_page.put_values_to_duty_and_frequency_and_save(card, '10', '100')
        values_on_card = monitoring_page.get_pin_values_from_card(card)
        assert_that(values_on_card).contains('10%', '100Hz')

    @pytest.mark.parametrize('device_address', ['4A', '65', '3F', '80'])
    @pytest.mark.parametrize('report_id', ['100', '200', '300'])
    def test_diagnostics_page(self, browser, device_address, report_id):
        main_page = MainPage(browser)

        main_page.go_to_site()
        main_page.get_button_by_device_address(device_address, self.DIAGNOSTICS_BUTTON).click()

        diagnostics_page = DiagnosticsPage(browser)
        report = diagnostics_page.load_report_by_id(report_id)

        assert_that(report).is_not_empty()
        assert_that(report).is_not_equal_to("Invalid type of 'repId' value")
