import pushover
from config import people


if __name__ == '__main__':
    for person in people:
        for login in person.logins:
            if person.should_send_report():
                records = login.bot.fetch()
                pushover.send_report(person, records)
