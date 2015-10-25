# -*- coding: utf-8 -*-
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pushover
from models import Person

engine = create_engine(os.environ['DATABASE_URL'])
session = sessionmaker(bind=engine)()


if __name__ == '__main__':
    for person in session.query(Person).all():
        for login in person.logins:
            if person.should_send_report():
                records = login.bot.fetch()
                pushover.send_report(person, records)
