from time import sleep

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from model.ui.BasePage import BasePage


class MonitoringPage(BasePage):
    CARDS = (By.XPATH, '//*[@class="ant-card"]')
    DROPDOWN_VALUES = (By.XPATH, '//*[@class="rc-virtual-list-holder-inner"]/div')
    CARD_NAME = 'ant-card-head-title'
    CARD_INPUT = '.ant-input'
    SAVE_BUTTON = '.ant-btn-primary'
    HZ_DROPDOWN = '.ant-select-selector'
    PIN_VALUES_ON_CARD = 'ant-typography'

    def get_displayed_cards(self):
        return self.find_elements(self.CARDS)

    def get_card_by_header_name(self, card_header):
        displayed_cards = self.get_displayed_cards()
        card_by_name = None
        for card in displayed_cards:
            card_name = card.find_element(By.CLASS_NAME, self.CARD_NAME)
            if card_name.text == card_header:
                card_by_name = card

        if card_by_name is None:
            raise Exception(f'Card with name {card_header} not found.')

        return card_by_name

    def put_values_to_duty_and_frequency_and_save(self, card, duty_value, freq_value):
        self.__put_duty_value(card, duty_value)
        self.__select_value_from_card_dropdown(card, freq_value)
        self.__press_save_button(card)

    def get_pin_values_from_card(self, card):
        sleep(5)
        values_on_card = card.find_elements(By.CLASS_NAME, self.PIN_VALUES_ON_CARD)
        return [value.text for value in values_on_card]

    def __put_duty_value(self, card, value):
        duty_field = card.find_element(By.CSS_SELECTOR, self.CARD_INPUT)
        for i in range(len(duty_field.get_attribute('value'))):
            duty_field.send_keys(Keys.BACKSPACE)
        duty_field.send_keys(value)

    def __select_value_from_card_dropdown(self, card, value):
        dropdown_list = card.find_element(By.CSS_SELECTOR, self.HZ_DROPDOWN).click()
        dropdown_options = self.find_elements(self.DROPDOWN_VALUES)
        for item in dropdown_options:
            if item.get_attribute('label') == value:
                if item.is_displayed():
                    item.click()
                else:
                    dropdown_list.click()
                    item.click()

    def __press_save_button(self, card):
        card.find_element(By.CSS_SELECTOR, self.SAVE_BUTTON).click()
