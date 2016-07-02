import datetime

from bots import NationwideBot


class Person:

    def __init__(self, name, pushover_key, report_frequency, logins):
        self.name = name
        self.pushover_key = pushover_key
        self.report_frequency = report_frequency
        self.logins = logins

    def should_send_report(self):
        today = datetime.date.today()
        today = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'][today.weekday()]
        return today in self.report_frequency


class NationwideLogin:

    def __init__(self, customer_number, pass_number, memorable_data):
        self.customer_number = customer_number
        self.pass_number = pass_number
        self.memorable_data = memorable_data

    @property
    def bot(self):
        return NationwideBot(self)
