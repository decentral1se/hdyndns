#!/usr/bin/env python3

import logging
from os import environ

try:
    import pkg_resources
except ImportError:
    pass


try:
    __version__ = pkg_resources.get_distribution('hdyndns').version
except Exception:
    __version__ = 'unknown'

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(environ.get('HDYNDNS_LOGLEVEL', 'DEBUG'))
