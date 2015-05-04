import datetime

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from bots import NationwideBot

Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    pushover_key = Column(String)
    report_frequency = Column(String)

    def should_send_report(self):
        today = datetime.date.today()
        today = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'][today.weekday()]
        return today in self.report_frequency

    def should_send_alert(self, record):
        for alert in self.alerts:
            should_send = all([
                alert.account_name == record.account_name,
                alert.balance >= record.balance])
            if should_send:
                return True
        return False


class Login(Base):
    __tablename__ = 'login'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship('Person', backref=backref('logins'))

    __mapper_args__ = {
        'polymorphic_identity': 'login',
        'polymorphic_on': type
    }


class NationwideLogin(Login):
    __tablename__ = 'nationwide'
    id = Column(Integer, ForeignKey('login.id'), primary_key=True)
    customer_number = Column(String)
    pass_number = Column(String)
    memorable_data = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'nationwide'
    }

    @property
    def bot(self):
        return NationwideBot(self)


class Alert(Base):
    __tablename__ = 'alert'
    id = Column(Integer, primary_key=True)
    account_name = Column(String)
    balance = Column(Integer)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship('Person', backref=backref('alerts'))


def create_all():
    engine = create_engine('sqlite:///accounts.db')
    Base.metadata.create_all(engine)
