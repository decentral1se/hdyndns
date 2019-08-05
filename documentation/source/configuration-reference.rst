***********************
Configuration reference
***********************

* ``provider``: The DNS provider.
* ``api_secret``: The API secret for the DNS provider.
* ``subdomains``: Optional comma separated list of subdomains to also update DNS entries for.
* ``ttl``: The DNS `time to live`_ counter in secods. Default is ``1800``.
* ``ip_versions``: The versions of IP that you wish to use. Default is ``4``.

.. _time to live: https://en.wikipedia.org/wiki/Time_to_live
