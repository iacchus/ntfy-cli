#!/usr/bin/env python

import os
import argparse

import click
import requests

# https://docs.ntfy.sh/publish/

NTFY_SERVER = os.environ.get('NTFY_SERVER')
NTFY_TOPIC = os.environ.get('NTFY_TOPIC')
#  NTFY_DEFAULT_TOPIC_URL = f"{NTFY_SERVER}/{NTFY_TOPIC}"
NTFY_URL = f"{NTFY_SERVER}/{NTFY_TOPIC}"
NTFY_TOKEN = os.environ.get('NTFY_TOKEN')

requests.post(url=NTFY_URL,
              data='testing\nnotification')
