# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert

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
            balance = balance.replace(u'£', '')
            pence = int(100 * float(balance))
            records.append(Record(name, pence))
        return records

    def _fetch(self):
        try:
            self.driver.get(self.url)
            self.driver.save_screenshot(
                '%s-nationwide-0.png' % self.login.person.name)
            self.answer_customer_number()
            self.driver.save_screenshot(
                '%s-nationwide-1.png' % self.login.person.name)
            self.driver.find_element_by_id('logInWithMemDataLink').click()
            self.driver.save_screenshot(
                '%s-nationwide-2.png' % self.login.person.name)
            self.answer_memorable_data()
            self.answer_pass_number_digit('SubmittedPassnumber1')
            self.answer_pass_number_digit('SubmittedPassnumber2')
            self.answer_pass_number_digit('SubmittedPassnumber3')
            self.driver.save_screenshot(
                '%s-nationwide-3.png' % self.login.person.name)
            self.driver.find_element_by_id('Continue').click()
            self.driver.save_screenshot(
                '%s-nationwide-4.png' % self.login.person.name)
            continue_links = self.driver.find_elements_by_link_text(
                'Continue with Internet Banking')
            if continue_links:
                continue_links[0].click()
                self.driver.save_screenshot(
                    '%s-nationwide-5.png' % self.login.person.name)
            records = self.find_records()
            if not records:
                raise Exception('No records found')
            return records
        except:
            self.driver.save_screenshot('nationwide-error.png')
            pushover.send_message(
                self.login.person,
                title='Error', message='Error collecting Nationwide data')
            raise
        finally:
            self.driver.get(('https://onlinebanking.nationwide.co.uk/'
                             'AccessManagement/Logout/Logout'))
            Alert(self.driver).accept()
            self.driver.save_screenshot(
                '%s-nationwide-6.png' % self.login.person.name)
