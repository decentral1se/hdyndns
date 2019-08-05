#!/usr/bin/env python3

"""DynDNS provider logic."""

from json import dumps
from sys import exit
from typing import List

from hdyndns import logger
from hdyndns.requests import get, put
from hdyndns.settings import EXIT_CODE_1_BAD


class GandiDynDNS:
    """The Gandis DNS provider DynDNS handler."""

    def __init__(self, section, *args, **kwargs):
        """Object initialisation."""
        self.api = 'https://dns.api.gandi.net/api/v5'
        self.api_secret = section['api_secret']
        self.domain = section._name
        self.subdomains = self.parse_subdomains(section)
        self.ip_provider = {
            '4': 'https://api.ipify.org?format=json',
            '6': 'https://api6.ipify.org/?format=json',
        }
        self.dns_type = {'4': 'A', '6': 'AAAA'}
        self.ip_versions = section.get('ip_versions', '4').split(',')
        self.ttl = section.get('ttl', '1800')
        self.section = section

    def parse_subdomains(self, section):
        """Parse subdomains if present."""
        subdomains = section.get('subdomains', None)
        if subdomains is not None:
            return subdomains.split(',')
        return []

    def get_dynamic_ip(self, ip_version) -> str:
        """Retrieve the dynamic IP address."""
        response = get(self.ip_provider[ip_version])

        message = 'Discovered dynamic IP of {} for {}'
        logger.info(message.format(response['ip'], self.domain))

        return response['ip']

    def get_zone_uuid(self) -> List[str]:
        """Get the DNS zone UUID."""
        url = '{}/domains/{}'.format(self.api, self.domain)
        headers = {'X-Api-Key': self.api_secret}
        response = get(url, headers=headers)

        try:
            zone_uuid = response['zone_uuid']

            message = 'Discovered Gandi zone UUID of {} for {}'
            logger.info(message.format(zone_uuid, self.domain))

            return zone_uuid
        except KeyError as exception:
            message = 'Missing {} from {}'
            logger.critical(message.format(str(exception), dumps(response)))
            exit(EXIT_CODE_1_BAD)

    def validate_subdomain_entries(self, response):
        """Validate that user specified subdomain entries exist."""
        entries = set([entry['rrset_name'] for entry in response])
        entries_match = all((subd in entries for subd in self.subdomains))
        if not entries_match:
            message = 'Missing subdomain DNS record from {} under {}'
            subdomains = ','.join(self.subdomains)
            logger.critical(message.format(subdomains, self.domain))
            exit(EXIT_CODE_1_BAD)

    def get_dns_ip(self, zone_uuid: str, dns_type: str) -> str:
        """Get the DNS A (or AAAA for ipv6) @ record."""

        url = '{}/zones/{}/records'.format(self.api, zone_uuid)
        headers = {'X-Api-Key': self.api_secret}
        response = get(url, headers=headers)

        tld_a_record = [
            entry
            for entry in response
            if entry['rrset_type'] == dns_type and entry['rrset_name'] == '@'
        ]

        ip_record = ''
        if len(tld_a_record) > 0:
            ip_record = tld_a_record[0]['rrset_values'][0]

        self.validate_subdomain_entries(response)

        message = 'Discovered IP address of {} for {} DNS {} @ record'
        logger.info(message.format(ip_record, self.domain, dns_type))

        return ip_record

    def update_dns(self):
        """Update the DNS records."""
        zone_uuid = self.get_zone_uuid()
        for ip_v in self.ip_versions:
            dns_ip = self.get_dns_ip(zone_uuid, self.dns_type[ip_v])
            dynamic_ip = self.get_dynamic_ip(ip_v)

            if dns_ip == dynamic_ip:
                message = 'DNS {} record and Dynamic IP for {} match'
                logger.info(message.format(self.dns_type[ip_v], self.domain))
                return

            headers = {
                'X-Api-Key': self.api_secret,
                'Content-type': 'application/json',
            }

            for name in ['@'] + self.subdomains:
                url = '{}/zones/{}/records/{}/{}'.format(
                    self.api, zone_uuid, name, self.dns_type[ip_v]
                )
                payload = {
                    'rrset_name': name,
                    'rrset_values': [dynamic_ip],
                    'rrset_ttl': self.ttl,
                }
                put(url, payload, headers=headers)
                logger.info(
                    'Updated {} entry with IP {}'.format(name, dynamic_ip)
                )
