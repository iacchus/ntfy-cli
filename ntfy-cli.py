#!/usr/bin/env python

import argparse
import base64
import os
import pathlib
import sys

import click

import requests
from requests.auth import HTTPBasicAuth

# https://github.com/iacchus/ntfy-cli
# https://docs.ntfy.sh/publish/
# https://docs.ntfy.sh/publish/#attachments
# https://docs.python.org/3.13/library/urllib.request.html#module-urllib.request
# https://docs.python.org/3/howto/urllib2.html
# https://www.geeksforgeeks.org/python-urllib-module/
# https://realpython.com/urllib-request/#post-requests-with-urllibrequest
# https://requests.readthedocs.io/en/latest/user/authentication/
# https://docs.python.org/3/library/argparse.html
# https://docs.python.org/3.13/howto/argparse.html
# https://click.palletsprojects.com/en/stable/
# https://click.palletsprojects.com/en/stable/quickstart/
# https://stackoverflow.com/a/48593823/371160
# https://docs.python.org/3/library/mimetypes.html

# for posting binary files with PUT:
# https://stackoverflow.com/a/8706029/371160

# let's prepend all environment variables with our namespace ("NTFY_", by now)
#  NTFY_FROM_STDIN = os.environ.get('NTFY_FROM_STDIN')
NTFY_SERVER = os.environ.get('NTFY_SERVER')
NTFY_TOPIC = os.environ.get('NTFY_TOPIC')
#  NTFY_DEFAULT_TOPIC_URL = f"{NTFY_SERVER}/{NTFY_TOPIC}"
NTFY_URL = f"{NTFY_SERVER}/{NTFY_TOPIC}"
NTFY_TOKEN = os.environ.get('NTFY_TOKEN') or ""

ICON_IMAGE_URL = "https://public.kassius.org/python-logo.png"

DEFAULT_MESSAGE_TITLE = "Sent via ntfy-cli.py"
DEFAULT_MESSAGE_BODY = 'testing\nnotification'
#  DEFAULT_MESSAGE_BODY = sys.stdin if NTFY_FROM_STDIN else 'testing\nnotification'

PRIORITIES = {"urgent", "high", "default", "low", "min"}

argument_parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]),
        description='Send ntfy notification',
        epilog="https://github.com/iacchus/ntfy-cli"
        )

#  argument_parser.add_argument("title")
#  argument_parser.add_argument("message")
#  argument_parser.add_argument("-t", "--title", default=DEFAULT_MESSAGE_TITLE)
argument_parser.add_argument("-t", "--title",
                             default=os.environ.get('NTFY_MESSAGE_TITLE') or
                             DEFAULT_MESSAGE_TITLE)
argument_parser.add_argument("-m", "--message",
                             default=os.environ.get('NTFY_MESSAGE_BODY') or
                             DEFAULT_MESSAGE_BODY)
argument_parser.add_argument("-p", "--priority", default="default",
                             choices=PRIORITIES)
argument_parser.add_argument("-x", "--tags", "--tag", action="extend", nargs="+",
                             type=str)
argument_parser.add_argument("-d", "--delay", default=None)
argument_parser.add_argument("-c", "--click", default=None)
#  argument_parser.add_argument("-k", "--markdown", action="store_true")
argument_parser.add_argument("-k", "--markdown", action="store_const", const="yes")
argument_parser.add_argument("-f", "--file", help="Attach a local file")
argument_parser.add_argument("-a", "--attach",
                             help="Attach a file from an URL", default=None)
args = argument_parser.parse_args()
print(args)

auth_string = f":{NTFY_TOKEN}"
auth_string_bytes = auth_string.encode("ascii")
auth_string_base64 = base64.b64encode(auth_string_bytes).decode("utf-8")
auth_header_basic = f"Basic {auth_string_base64}"
auth_header_bearer = f"Bearer {NTFY_TOKEN}"
# https://docs.ntfy.sh/publish/#query-param
auth_header_query_param_key = "auth"
auth_header_query_param_value = \
        base64.b64encode(auth_header_basic.encode("ascii")).decode("utf-8")

MESSAGE_BODY = args.message or DEFAULT_MESSAGE_BODY
#  print(auth_string, auth_string_bytes, auth_string_base64)

HEADERS = {
        "X-Title": args.title or DEFAULT_MESSAGE_TITLE,
        "X-Icon": ICON_IMAGE_URL,
        "X-Priority": "urgent",
        #  "X-Tags": "+1, richtig",
        "X-Tags": ", ".join(args.tags if args.tags else []),
        "X-Markdown": args.markdown or "no",
        "X-Delay": args.delay or None,
        "X-Click": args.click or None,
        "X-Attach": args.attach,
        #  "Authorization": f"Bearer {NTFY_TOKEN}",
        "Authorization": f"Basic {auth_string_base64}",
        }

print(HEADERS)
#  print(NTFY_SERVER, NTFY_TOKEN, NTFY_TOPIC, NTFY_URL)

#  basic_creds = HTTPBasicAuth("", NTFY_TOKEN)

#  make_post_request(url=NTFY_URL, unencoded_data={"X-Message": "okayy"}, headers=HEADERS)
r = requests.post(url=NTFY_URL,
#                    auth=('', NTFY_TOKEN),
                  data=MESSAGE_BODY,
#                    data=DEFAULT_MESSAGE_BODY,
                  headers=HEADERS)

#  print(r.text)
