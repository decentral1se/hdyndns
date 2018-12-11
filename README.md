# hdyndns

A GNU/Linux Python 3.5+ [Dynamic DNS] client for your homebrew server.

[Dynamic DNS]: https://en.wikipedia.org/wiki/Dynamic_DNS

It's lightweight, with no external dependencies and is simple to configure.

See below for documentation about motivation, usage and configuration options.

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

The following examples were run on a [Debian system] using the [Gandi DNS provider].

[Debian system]: https://www.debian.org/
[Gandi DNS provider]: #supported-dns-providers

Make sure you have the necessary system prerequisites with:

```bash
$ sudo apt update
$ sudo apt install -y python3 python3-dev python3-pip
```

And then install `hdyndns` with:

```bash
$ sudo useradd -m hdyndns
$ sudo -u hdyndns pip3 install --user hdyndns
```

If you have an DNS A record for `mysite.com` and subdomains `foo.mysite.com`
and `bar.mysite.come` that looks like the following:

```
@   1800 IN A 86.91.199.200
foo 1800 IN A 86.91.199.200
bar 1800 IN A 86.91.199.200
```

Then create a configuration file at `/home/hdyndns/.hdyndns/hdyndns.ini`:

```config
[mysite.com]
provider = gandi
api_secret = mySuperSecretApiPassword
subdomains = foo,bar
```

This configuration makes sure to keep `mysite.com` and the subdomains up to
date.

Finally, add it your root crontab (`sudo crontab -e`) to run it every 15 minutes:

```bash
*/15 * * * * runuser -l hdyndns -c '$HOME/.local/bin/hdyndns' &>/dev/null
```

Regarding the `&>/dev/null` part, see [issue #1](https://git.coop/decentral1se/hdyndns/issues/1).

## Known Limitations

* Different IP addresses for subdomains are currently not supported.

Please open [an issue] if you want to collaborate on removing these limitations.

[an issue]: https://git.coop/decentral1se/hdyndns/issues

## Supported DNS Providers

* [Gandi](https://www.gandi.net/en)

Any DNS provider can be supported if they provide some programmatic way to
update their DNS records (for example, if they have a public API). If your
current DNS provider is not listed above, please [raise an issue]. If you'd
like to add it yourself, take a look at [hdyndns/providers.py]. All
contributions welcome!

[raise an issue]: https://git.coop/decentral1se/hdyndns/issues
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

## How To Help

You'll need to install [pipenv] for development.

[pipenv]: https://pipenv.readthedocs.io/en/latest/

You can follow these steps to get a working local installation:

```bash
$ pipenv install --dev  # install the dependencies
$ pipenv run pip install -e .  # install the local hdyndns
$ pipenv run hdyndns --help  # check that the local hdynds is working
$ pipenv run tox -e py37  # run the tests on python 3.7 (run `tox -l` to see pythons)
```
