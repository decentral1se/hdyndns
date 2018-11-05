#!/usr/bin/env python3

import logging
from os import environ

logging.basicConfig()

logger = logging.getLogger(__name__)

logger.setLevel(environ.get('HDYNDNS_LOGLEVEL', 'DEBUG'))
