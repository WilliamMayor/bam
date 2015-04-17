# -*- coding: utf-8 -*-
import os

import requests


def send_alert(record):
    requests.post('https://api.pushover.net/1/messages.json', data={
        'token': os.environ['PUSHOVER_API_TOKEN'],
        'user': os.environ['PUSHOVER_USER_KEY'],
        'message': u'%s has a balance of £%.2f' % (
            record.name, record.pence/100.0),
        'title': 'BAM: Alert'
    })


def send_report(records):
    requests.post('https://api.pushover.net/1/messages.json', data={
        'token': os.environ['PUSHOVER_API_TOKEN'],
        'user': os.environ['PUSHOVER_USER_KEY'],
        'message': '\n'.join([
            u'%s: £%.2f' % (r.name, r.pence/100.0) for r in records]),
        'title': 'BAM: Report'
    })
