from __future__ import annotations

import logging

import sentry_sdk
from decouple import config as environment
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration


class SentryClient:

    def set_logging_config(self):
        # All of this is already happening by default!
        sentry_logging = LoggingIntegration(
            level=logging.INFO,        # Capture info and above as breadcrumbs
            event_level=logging.ERROR,  # Send errors as events
        )

        return sentry_logging

    def initialize_monitor(self):
        if environment('SENTRY_DSN') and environment('ENVIRONMENT') != 'local':
            sentry_sdk.init(
                dsn=environment('SENTRY_DSN'),
                environment=environment('ENVIRONMENT'),
                integrations=[
                    self.set_logging_config(),
                    FlaskIntegration(),
                ],
                # integrations=[FlaskIntegration()],
                auto_session_tracking=True,
                debug=True,
                # Set traces_sample_rate to 1.0 to capture 100%
                # of transactions for performance monitoring.
                # We recommend adjusting this value in production,
                traces_sample_rate=environment('SENTRY_SAMPLE_RATE'),
                # traces_sample_rate=1.0
            )
