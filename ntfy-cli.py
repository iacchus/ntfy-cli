#!/usr/bin/env python

import argparse
import os
import sys

import click
import requests

from requests.auth import HTTPBasicAuth

# https://github.com/iacchus/ntfy-cli
# https://docs.ntfy.sh/publish/
# https://requests.readthedocs.io/en/latest/user/authentication/
# https://docs.python.org/3/library/argparse.html
# https://click.palletsprojects.com/en/stable/
# https://click.palletsprojects.com/en/stable/quickstart/

NTFY_FROM_STDIN = os.environ.get('NTFY_FROM_STDIN')
NTFY_SERVER = os.environ.get('NTFY_SERVER')
NTFY_TOPIC = os.environ.get('NTFY_TOPIC')
#  NTFY_DEFAULT_TOPIC_URL = f"{NTFY_SERVER}/{NTFY_TOPIC}"
NTFY_URL = f"{NTFY_SERVER}/{NTFY_TOPIC}"
NTFY_TOKEN = os.environ.get('NTFY_TOKEN') or ""

ICON_IMAGE_URL = "https://public.kassius.org/python-logo.png"
MESSAGE_TITLE = "Sent via ntfy-cli.py"
MESSAGE_BODY = sys.stdin if NTFY_FROM_STDIN else 'testing\nnotification'

HEADERS = {
        "X-Title": MESSAGE_TITLE,
        "X-Icon": ICON_IMAGE_URL,
        "X-Priority": "urgent",
        "X-Tags": "+1, richtig"
        }

argument_parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]),
        description='Send ntfy notification',
        epilog="This is the epilog\ngh:iacchus/ntfy-cli"
        )

argument_parser.add_argument("title")
argument_parser.add_argument("message")
argument_parser.add_argument("--markdown", action="store_true")
args = argument_parser.parse_args()
print(args, args.message)

#  print(NTFY_SERVER, NTFY_TOKEN, NTFY_TOPIC, NTFY_URL)

#  basic_creds = HTTPBasicAuth("", NTFY_TOKEN)

r = requests.post(url=NTFY_URL,
                  auth=('', NTFY_TOKEN),
                  data=MESSAGE_BODY,
                  headers=HEADERS)

print(r.text)
