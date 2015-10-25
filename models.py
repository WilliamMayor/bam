import datetime

from sqlalchemy import Column, Integer, String, ForeignKey
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
