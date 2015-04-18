# -*- coding: utf-8 -*-
import os

import requests


def send_message(person, title, message):
    requests.post('https://api.pushover.net/1/messages.json', data={
        'token': os.environ['PUSHOVER_API_TOKEN'],
        'user': person.pushover_key,
        'title': 'BAM: %s' % title,
        'message': message})


def send_alert(person, record):
    send_message(
        person,
        title='Alert',
        message=u'%s has a balance of £%.2f' % (
            record.account_name, record.balance/100.0))


def send_report(person, records):
    send_message(
        person,
        title='Report',
        message='\n'.join([
            u'%s: £%.2f' % (r.account_name, r.balance/100.0)
            for r in records]))
