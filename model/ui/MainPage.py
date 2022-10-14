from selenium.webdriver.common.by import By

from model.ui.BasePage import BasePage


class MainPage(BasePage):
    TABLE_HEADER = (By.XPATH, '//*[@class="ant-table-thead"]//th')
    TABLE_ROWS = (By.XPATH, '//*[@class="ant-table-tbody"]/tr')

    def get_table_header(self):
        return self.find_elements(self.TABLE_HEADER)

    def get_table_content(self):
        table_content = self.__get_table_rows()
        return self.__get_table_content_as_dict(table_content)

    def get_button_by_device_address(self, device_address, button_name):
        row = self.__get_row_by_device_address(self.__get_table_rows(), device_address)
        button_cell = None
        cells = row.find_elements(By.TAG_NAME, 'td')
        for cell in cells:
            if cell.text == button_name:
                button_cell = cell

        button = button_cell.find_element(By.TAG_NAME, 'button')

        if button is None:
            raise Exception(f'Button with name {button_name} was not found in row with address: {device_address}')

        return button

    def __get_table_rows(self):
        return self.find_elements(self.TABLE_ROWS)

    @staticmethod
    def __get_row_by_device_address(table_content, device_address):
        row = None
        for item in table_content:
            if item.get_attribute('data-row-key') == device_address:
                row = item
        if row is None:
            raise Exception(f'row with device address {device_address} not found.')
        else:
            return row

    @staticmethod
    def __get_table_content_as_dict(table_content):
        table_cells = dict()
        for row in table_content:
            cells = row.find_presence_of_elements(By.TAG_NAME, 'td')
            table_cells[row.get_attribute('data-row-key')] = [cell_text.text for cell_text in cells]
        return table_cells
