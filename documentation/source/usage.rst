*****
Usage
*****

The following examples were run on a `Debian system`_ using the Gandi DNS provider.

See the :ref:`supported-providers` section for more on supported DNS providers.

.. _Debian system: https://www.debian.org/

Make sure you have the necessary system prerequisites with:

.. code-block:: bash

    $ sudo apt update
    $ sudo apt install -y python3 python3-dev python3-pip

And then install ``hdyndns`` with:

.. code-block:: bash

    $ sudo useradd -m hdyndns
    $ sudo -u hdyndns pip3 install --user hdyndns

If you have an DNS A record for ``mysite.com`` and subdomains
``foo.mysite.com`` and ``bar.mysite.com`` that looks like the following:

.. code-block:: bash

    @   1800 IN A 86.91.199.200
    foo 1800 IN A 86.91.199.200
    bar 1800 IN A 86.91.199.200

Then create a configuration file at ``/home/hdyndns/.hdyndns/hdyndns.ini``:

.. code-block:: ini

    [mysite.com]
    provider = gandi
    api_secret = mySuperSecretApiPassword
    subdomains = foo,bar

Finally, add it your root crontab (``sudo crontab -e``) to run it every 15 minutes:

.. code-block:: bash

    */15 * * * * runuser -l hdyndns -c '$HOME/.local/bin/hdyndns' &>/dev/null

Regarding the ``&>/dev/null`` part, see `issue #8`_.

.. _issue #8: https://github.com/decentral1se/hdyndns/issues/8
