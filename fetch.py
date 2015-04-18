# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pushover
from models import Person

engine = create_engine('sqlite:///accounts.db')
session = sessionmaker(bind=engine)()


if __name__ == '__main__':
    for person in session.query(Person).all():
        for login in person.logins:
            records = login.bot.fetch()
            for record in records:
                if person.should_send_alert(record):
                    pushover.send_alert(person, record)
            if person.should_send_report():
                pushover.send_report(person, records)
