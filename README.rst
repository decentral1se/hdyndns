.. _header:

*******
hdyndns
*******

.. image:: https://img.shields.io/badge/license-GPL-brightgreen.svg
   :target: LICENSE
   :alt: Repository license

.. image:: https://badge.fury.io/py/hdyndns.svg
   :target: https://badge.fury.io/py/hdyndns
   :alt: PyPI package

.. image:: https://travis-ci.com/decentral1se/hdyndns.svg?branch=master
   :target: https://travis-ci.com/decentral1se/hdyndns
   :alt: Travis CI result

.. image:: https://readthedocs.org/projects/hdyndns/badge/?version=latest
   :target: https://hdyndns.readthedocs.io/en/latest/
   :alt: Documentation status

.. image:: https://img.shields.io/badge/support-maintainers-brightgreen.svg
   :target: https://decentral1.se
   :alt: Support badge

.. _introduction:

A GNU/Linux Python 3.5+ DynDNS client for your homebrew server
--------------------------------------------------------------

Please note, you should probably use the more complete and useful `lexicon`_.

.. _lexicon: https://github.com/analogj/lexicon

When to use hdyndns
-------------------

From `Access Your Home Network From Anywhere With Dynamic DNS`_:

.. _Access Your Home Network From Anywhere With Dynamic DNS: https://www.howtogeek.com/66438/how-to-easily-access-your-home-network-from-anywhere-with-ddns/

    A Local Update Client

    If your router doesn’t support DDNS services, you will need a local client to
    run on a frequently used computer somewhere on your home network. This
    lightweight little application will check what your IP address is and then
    phone home to the DDNS provider to update your DDNS record. It’s less ideal
    than a router-based solution–if the computer isn’t on when your IP address
    changes, then the record doesn’t get updated–but it’s certainly better than
    manually editing your DDNS entry.

This tool is the 'Local Update Client' component of the Dynamic DNS hombrew setup.

Why use hdyndns
---------------

* Lightweight pure python implementation with no external dependencies.
* Simple 'ini style' configuration.
* Avoid writing potentially hard to maintain dynamic DNS bash scripts.
* Small code base, easy to understand, maintain and extend and is cross platform.
* Will be maintained going forward and is being used in existing homebrew setups.

.. _documentation:

Documentation
*************

* https://hdyndns.readthedocs.io/

Mirroring
*********

* `hack.decentral1.se/decentral1se/hdyndns`_
* `github.com/decentral1se/hdyndns`_
* `git.coop/decentral1se/hdyndns`_

.. _hack.decentral1.se/decentral1se/hdyndns: https://hack.decentral1.se/decentral1se/hdyndns
.. _github.com/decentral1se/hdyndns: https://github.com/decentral1se/hdyndns
.. _git.coop/decentral1se/hdyndns: https://git.coop/decentral1se/hdyndns
