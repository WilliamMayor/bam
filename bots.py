from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import pushover


class Record(object):

    def __init__(self, account_name, balance):
        self.account_name = account_name
        self.balance = balance


class Bot(object):

    def __enter__(self):
        self.driver = webdriver.Firefox()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.close()
        pass

    def fetch(self):
        with self as s:
            return s._fetch()


class NationwideBot(Bot):
    url = 'https://onlinebanking.nationwide.co.uk/AccessManagement/Login'

    def __init__(self, login):
        self.login = login

    def answer_pass_number_digit(self, name):
        elem = self.driver.find_element_by_name(name)
        label = self.driver.find_element_by_xpath(
            '//label[@for="%s"]' % elem.get_attribute('id'))
        index = int(label.text[:-len('st digit')]) - 1
        elem.send_keys(self.login.pass_number[index])

    def answer_customer_number(self):
        elem = self.driver.find_element_by_name('CustomerNumber')
        elem.send_keys(self.login.customer_number)
        elem.send_keys(Keys.RETURN)

    def answer_memorable_data(self):
        elem = self.driver.find_element_by_name(
            'SubmittedMemorableInformation')
        elem.send_keys(self.login.memorable_data)

    def find_records(self):
        account_rows = self.driver.find_elements_by_css_selector(
            'tr.account-row:not(.ghost-account-row)')
        records = []
        for account_row in account_rows:
            name = account_row.find_element_by_css_selector(
                'b.acDesc').text
            balance = account_row.find_element_by_css_selector(
                '.bal-details strong').text
            balance = balance.replace(',', '')
            balance = balance.replace('£', '')
            pence = int(100 * float(balance))
            records.append(Record(name, pence))
        return records

    def _fetch(self):
        try:
            self.driver.get(self.url)
            self.driver.save_screenshot('nationwide-0.png')
            self.answer_customer_number()
            self.driver.save_screenshot('nationwide-1.png')
            self.driver.find_element_by_id('logInWithMemDataLink').click()
            self.driver.save_screenshot('nationwide-2.png')
            self.answer_memorable_data()
            self.answer_pass_number_digit('SubmittedPassnumber1')
            self.answer_pass_number_digit('SubmittedPassnumber2')
            self.answer_pass_number_digit('SubmittedPassnumber3')
            self.driver.save_screenshot('nationwide-3.png')
            self.driver.find_element_by_id('Continue').click()
            self.driver.save_screenshot('nationwide-4.png')
            return self.find_records()
        except:
            self.driver.save_screenshot('nationwide-error.png')
            pushover.send_message(
                self.login.person,
                title='Error', message='Error collecting Nationwide data')
            raise
