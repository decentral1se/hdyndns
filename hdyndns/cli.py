#!/usr/bin/env python3

"""Command line entry point."""

from hdyndns import logger
from hdyndns.config import (
    create_home,
    get_user,
    read_config,
    validate_api_secrets,
    validate_dns_providers,
)
from hdyndns.providers import GandiDynDNS
from hdyndns.settings import EXIT_CODE_0_OK, EXIT_CODE_1_BAD


def cli_entrypoint() -> None:
    """The command line entrypoint."""
    user = get_user()
    create_home(user)

    config = read_config(user)
    sections = [section for section in config.keys() if section != 'DEFAULT']

    validate_dns_providers(config, sections)
    validate_api_secrets(config, sections)

    for section in sections:
        if 'gandi' == config[section]['provider']:
            logger.info('Processing {} with provider Gandi'.format(section))
            GandiDynDNS(config[section]).update_dns()
            exit(EXIT_CODE_0_OK)
        else:
            logger.critical('No supported provider found')
            exit(EXIT_CODE_1_BAD)
