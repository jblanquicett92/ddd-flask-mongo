from __future__ import annotations

import logging

import client
from sentry_sdk import capture_message

client_sentry = client.SentryClient()

client_sentry.initialize_monitor()

capture_message('Hello World')  # Will create an event in Sentry.

# raise ValueError()  # Will also create an event in Sentry.

# division_by_zero = 1 / 0

logging.debug('I am ignored')
logging.info('I am a breadcrumb')
logging.error('I am an event', extra=dict(bar=43))
logging.exception('An exception happened')
