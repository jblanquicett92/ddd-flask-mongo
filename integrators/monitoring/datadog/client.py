from __future__ import annotations

import logging

from ddtrace import config
from ddtrace import patch
from ddtrace import patch_all
from ddtrace import tracer

config.env = 'test'      # the environment the application is in
config.service = 'companies-ms'  # name of your application
config.version = '0.1'  # version of your application

patch_all()

patch(logging=True)

FORMAT = (
    '%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
    '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s '
    'dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
    '- %(message)s'
)
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)
log.level = logging.INFO

# Network socket
tracer.configure(
    dogstatsd_url='localhost:8126/v0.4/traces',
)


@tracer.wrap()
def hello():
    log.info('Hello, World!')


hello()
