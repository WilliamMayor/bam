#!/usr/bin/env bash
set -eo pipefail
shopt -s nullglob

Xvfb $DISPLAY -ac &> /dev/null &

python fetch.py
