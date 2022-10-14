from selenium.webdriver.common.by import By
from time import sleep

from model.ui.BasePage import BasePage


class DiagnosticsPage(BasePage):
    DROPDOWN = (By.CSS_SELECTOR, '.ant-select')
    DROPDOWN_VALUES = (By.XPATH, '//*[@class="rc-virtual-list-holder-inner"]/div')
    LOAD_REPORT_BUTTON = (By.CSS_SELECTOR, '.ant-btn.ant-btn-primary')
    REPORT = (By.XPATH, '//*[@class="ant-typography"]/pre')
    VALUE_IN_DROPDOWN_FIELD = (By.XPATH, '//*[@class="ant-select-selection-item"]')

    def load_report_by_id(self, report_id):
        self.__click_on_dropdown()
        self.__find_id_in_dropdown_and_click_it(report_id)
        sleep(1)
        self.__click_on_load_report_button()
        return self.__get_report_text()

    def __click_on_dropdown(self):
        self.find_element(self.DROPDOWN).click()

    def __find_id_in_dropdown_and_click_it(self, report_id):
        ids_in_drop_down = self.find_elements_visible(self.DROPDOWN_VALUES)
        for item in ids_in_drop_down:
            if item.text == report_id:
                if item.is_displayed():
                    item.click()
                else:
                    self.find_element(self.DROPDOWN).click()
                    item.click()

    def __click_on_load_report_button(self):
        self.find_element(self.LOAD_REPORT_BUTTON).click()

    def __get_report_text(self):
        return self.find_element(self.REPORT).text

