#!/usr/bin/env python

import os
import argparse

import click
import requests

from requests.auth import HTTPBasicAuth

# https://docs.ntfy.sh/publish/

NTFY_SERVER = os.environ.get('NTFY_SERVER')
NTFY_TOPIC = os.environ.get('NTFY_TOPIC')
#  NTFY_DEFAULT_TOPIC_URL = f"{NTFY_SERVER}/{NTFY_TOPIC}"
NTFY_URL = f"{NTFY_SERVER}/{NTFY_TOPIC}"
NTFY_TOKEN = os.environ.get('NTFY_TOKEN') or ""

ICON_IMAGE_URL = "https://public.kassius.org/python-logo.png"

HEADERS = {
        "X-Icon": ICON_IMAGE_URL,
        "X-Priority": "urgent",
        }
#  print(NTFY_SERVER, NTFY_TOKEN, NTFY_TOPIC, NTFY_URL)

#  basic_creds = HTTPBasicAuth("", NTFY_TOKEN)

r = requests.post(url=NTFY_URL,
                  auth=('', NTFY_TOKEN),
                  data='testing\nnotification',
                  headers=HEADERS)

print(r.text)
