# hdyndns

A GNU/Linux Python 3.5+ DynDNS client for your homebrew server.

## When To Use It

From [Access Your Home Network From Anywhere With Dynamic DNS]:

[Access Your Home Network From Anywhere With Dynamic DNS]: https://www.howtogeek.com/66438/how-to-easily-access-your-home-network-from-anywhere-with-ddns/

> A Local Update Client
>
> If your router doesn’t support DDNS services, you will need a local client to
> run on a frequently used computer somewhere on your home network. This
> lightweight little application will check what your IP address is and then
> phone home to the DDNS provider to update your DDNS record. It’s less ideal
> than a router-based solution–if the computer isn’t on when your IP address
> changes, then the record doesn’t get updated–but it’s certainly better than
> manually editing your DDNS entry.

This tool is the 'Local Update Client' component of the Dynamic DNS hombrew setup.

## How To Use It

The following examples were run on a [Debian system].

[Debian system]: https://www.debian.org/

```bash
$ sudo apt update && sudo apt install -y python3 python3-dev python3-pip
$ sudo useradd -m hdyndns
$ sudo -u hdyndns pip3 install --user hdyndns
```

If you have DNS records for `baz.com` and subdomains that looks like:

```
@   1800 IN A 86.91.199.200
foo 1800 IN A 86.91.199.200
bar 1800 IN A 86.91.199.200
```

Then create a configuration file at `/home/hdyndns/.hdyndns/hdyndns.ini`:

```config
[baz.com]
provider = gandi
api_secret = passw0rd
subdomains = foo,bar
```

This configuration makes sure to keep `baz.com` and the subdomains
`foo.baz.com`, `bar.baz.com` entries up to date.

Finally, add it your crontab to run every 5 minutes:

```bash
*/5 * * * * su - hdyndns -c '/home/hdyndns/.local/bin/hdyndns' &>/dev/null
```

We configure the logging level to only output messages when it fails.

## Known Limitations

* Different IP addresses for subdomains are currently not supported.

## Supported Providers

* [Gandi](https://www.gandi.net/en)

Any DNS provider can be supported if they provide some programmatic way to
update their DNS records. If your current DNS provider is not listed above,
please contact the package maintainer (see `setup.py` for more details). If
you'd like to add it yourself, take a look at [hdyndns/providers.py]. All
contributions welcome!

[hdyndns/providers.py]: hdyndns/providers.py

## Configuration Options

### provider

The DNS provider.

### api_secret

The API secret for the DNS provider.

### subdomains

Optional comma separated list of subdomains to also update DNS entries for.

### ttl

The DNS [time to live] counter in secods. Default is `1800`.

[time to live]: https://en.wikipedia.org/wiki/Time_to_live

## How to Hack It

We use [pipenv], [pytest] and [tox] for development.

[pipenv]: https://pipenv.readthedocs.io/en/latest/
[pytest]: https://docs.pytest.org/en/latest/
[tox]: https://tox.readthedocs.io/en/latest/


```bash
$ pipenv install --dev
$ pipenv run pip install -e .
$ pipenv run hdyndns --help
$ pipenv run tox -e py37
```
