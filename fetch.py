# -*- coding: utf-8 -*-
import os
import datetime
import subprocess

from sqlalchemy import create_engine, event, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import pushover

engine = create_engine('sqlite:///accounts.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Record(Base):
    __tablename__ = 'record'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    when = Column(DateTime, default=datetime.datetime.now())
    pence = Column(Integer)

    def __repr__(self):
        return "<Record(name='%s', when='%s', amount='£%.2f')>" % (
            self.name, self.when.isoformat(), self.pence / 100.0)


class Alert(Base):
    __tablename__ = 'alert'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    lessthan = Column(Integer)


@event.listens_for(Record, 'after_insert')
def send_alerts(mapper, connection, target):
    alerts = session.query(Alert).filter(Alert.name == target.name).all()
    for a in alerts:
        if a.lessthan > target.pence:
            pushover.send_alert(target)


class Credential(object):

    def __enter__(self):
        self.driver = webdriver.Firefox()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.close()
        pass

    def fetch(self):
        with self as s:
            s._fetch()


class Nationwide(Credential, Base):
    __tablename__ = 'nationwide'
    id = Column(Integer, primary_key=True)
    customer_number = Column(String)
    pass_number = Column(String)
    memorable_data = Column(String)

    url = 'https://onlinebanking.nationwide.co.uk/AccessManagement/Login'

    def answer_digit(self, name):
        elem = self.driver.find_element_by_name(name)
        label = self.driver.find_element_by_xpath(
            '//label[@for="%s"]' % elem.get_attribute('id'))
        index = int(label.text[:-len('st digit')]) - 1
        elem.send_keys(self.pass_number[index])

    def _fetch(self):
        self.driver.get(self.url)
        elem = self.driver.find_element_by_name('CustomerNumber')
        elem.send_keys(self.customer_number)
        elem.send_keys(Keys.RETURN)
        elem = self.driver.find_element_by_name(
            'SubmittedMemorableInformation')
        elem.send_keys(self.memorable_data)
        self.answer_digit('SubmittedPassnumber1')
        self.answer_digit('SubmittedPassnumber2')
        self.answer_digit('SubmittedPassnumber3')
        self.driver.find_element_by_id('Continue').click()
        account_rows = self.driver.find_elements_by_css_selector(
            'tr.account-row:not(.ghost-account-row)')
        records = []
        for account_row in account_rows:
            r = Record()
            records.append(r)
            r.name = account_row.find_element_by_css_selector(
                'b.acDesc').text
            balance = account_row.find_element_by_css_selector(
                '.bal-details strong').text[1:]
            balance = float(balance.replace(',', ''))
            r.pence = int(100 * balance)
            session.add(r)
        session.commit()
        pushover.send_report(records)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    with open(os.devnull, "w") as dev_null:
        p = subprocess.Popen(
            ['Xvfb', ':99',  '-ac'], stdout=dev_null, stderr=dev_null)
        for bank in [Nationwide]:
            for login in session.query(bank).all():
                login.fetch()
        p.kill()
