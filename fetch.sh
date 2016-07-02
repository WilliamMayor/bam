#!/usr/bin/env bash
set -e

/opt/bin/entry_point.sh &
/usr/bin/python3 /usr/src/app/fetch.py
