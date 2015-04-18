# -*- coding: utf-8 -*-
import os

import requests


def send_alert(person, record):
    requests.post('https://api.pushover.net/1/messages.json', data={
        'token': os.environ['PUSHOVER_API_TOKEN'],
        'user': person.pushover_key,
        'message': u'%s has a balance of £%.2f' % (
            record.name, record.balance/100.0),
        'title': 'BAM: Alert'
    })


def send_report(person, records):
    requests.post('https://api.pushover.net/1/messages.json', data={
        'token': os.environ['PUSHOVER_API_TOKEN'],
        'user': person.pushover_key,
        'message': '\n'.join([
            u'%s: £%.2f' % (r.name, r.balance/100.0) for r in records]),
        'title': 'BAM: Report'
    })
