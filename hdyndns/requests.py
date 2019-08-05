#!/usr/bin/env python3

"""The mandatory urllib helper module."""

from json import dumps, loads
from json.decoder import JSONDecodeError
from socket import timeout
from urllib.error import URLError
from urllib.request import Request, urlopen

from hdyndns import logger
from hdyndns.settings import EXIT_CODE_1_BAD, REQUEST_TIMEOUT


def get(url, headers=None, load_json=True):
    """Run a HTTP GET on some web resource."""
    headers = headers or {}
    try:
        request = Request(url, headers=headers, method='GET')
        response = (
            urlopen(request, timeout=REQUEST_TIMEOUT).read().decode('utf-8')
        )
        if not load_json:
            return response
        try:
            return loads(response)
        except JSONDecodeError:
            message = 'Unable to JSON load {}'.format(response)
            logger.critical(message)
            exit(EXIT_CODE_1_BAD)
    except (URLError, ValueError, timeout) as exception:
        message = 'Unable to GET against {}: {}'.format(url, str(exception))
        logger.critical(message)
        exit(EXIT_CODE_1_BAD)


def put(url, payload, headers=None):
    """Run a HTTP PUT on some web resource."""
    headers = headers or []
    try:
        request = Request(url, headers=headers, method='PUT')
        dumped = dumps(payload).encode('utf-8')
        return (
            urlopen(request, data=dumped, timeout=REQUEST_TIMEOUT)
            .read()
            .decode('utf-8')
        )
    except (URLError, ValueError, timeout) as exception:
        print(exception.file.read())
        message = 'Unable to PUT against {}: {}'.format(url, str(exception))
        logger.critical(message)
        exit(EXIT_CODE_1_BAD)
