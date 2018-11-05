#!/usr/bin/env python3

"""Configuration module."""

from configparser import ConfigParser
from os import makedirs
from os.path import exists
from subprocess import check_output
from sys import exit
from typing import Any, Union

from hdyndns import logger
from hdyndns.settings import EXIT_CODE_1_BAD, SUPPORTED_DNS_PROVIDERS


def get_user() -> str:
    """Determine who the current user is."""
    try:
        return check_output('whoami', timeout=0.5).decode('utf-8').strip()
    except OSError as exception:
        message = 'Canot determine user. Raised {}'.format(str(exception))
        logger.critical(message)
        exit(EXIT_CODE_1_BAD)


def create_home(user: str,
                root: Union[str, None] = None) -> None:
    """Create the home configuration folder."""
    home_path = '{root}/{user}/.hdyndns'.format(
        root=root if root else '/home',
        user=user,
    )
    if not exists(home_path):
        makedirs(home_path)


def read_config(user: str,
                root: Union[str, None] = None) -> Any:
    """Read the INI configuration file."""
    cfg_path = '{root}/{user}/.hdyndns/hdyndns.ini'.format(
        root=root if root else '/home',
        user=user,
    )

    config = ConfigParser()

    if not config.read(cfg_path):
        message = 'Missing configuration from {}'.format(cfg_path)
        logger.critical(message)
        exit(EXIT_CODE_1_BAD)

    return config


def validate_dns_providers(config, sections) -> None:
    """Validate the DNS providers are actually supported."""
    for section in sections:
        try:
            provider = config[section]['provider']
            if provider not in SUPPORTED_DNS_PROVIDERS:
                message = 'Unsupported DNS provider {}'.format(provider)
                logger.critical(message)
                exit(EXIT_CODE_1_BAD)
        except KeyError:
            message = 'No provider in {} config section'.format(section)
            logger.critical(message)
            exit(EXIT_CODE_1_BAD)


def validate_api_secrets(config, sections) -> None:
    """Validate the DNS providers are actually supported."""
    for section in sections:
        try:
            config[section]['api_secret']
        except KeyError:
            message = 'No api_secret in {} config section'.format(section)
            logger.critical(message)
            exit(EXIT_CODE_1_BAD)
