from os.path import join
from tempfile import TemporaryDirectory

import pytest

from hdyndns.config import (
    create_home, get_user, read_config, validate_api_secrets,
    validate_dns_providers
)


def test_handles_missing_config(caplog):
    with TemporaryDirectory() as temp_dir:
        user = get_user()
        create_home(user, root=temp_dir)
        with pytest.raises(SystemExit):
            read_config(user, root=temp_dir)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'CRITICAL'
    assert 'Missing configuration' in caplog.records[0].message


def test_reads_config_correctly():
    with TemporaryDirectory() as temp_dir:
        user = get_user()
        create_home(user, root=temp_dir)

        cfg_path = join(temp_dir, user, '.hdyndns', 'hdyndns.ini')
        with open(cfg_path, 'w+') as handle:
            handle.write('[foo.bar]\nprovider=baz')
        config = read_config(user, root=temp_dir)

        assert config is not []
        assert config.sections() == ['foo.bar']
        assert config['foo.bar']['provider'] == 'baz'


def test_bails_out_not_supported_provider(caplog):
    with TemporaryDirectory() as temp_dir:
        user = get_user()
        create_home(user, root=temp_dir)

        cfg_path = join(temp_dir, user, '.hdyndns', 'hdyndns.ini')
        with open(cfg_path, 'w+') as handle:
            handle.write('[bar.foo]\nprovider=baz')

        config = read_config(user, root=temp_dir)
        with pytest.raises(SystemExit):
            sections = filter(lambda s: s != 'DEFAULT', config.keys())
            validate_dns_providers(config, sections)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'CRITICAL'
    assert 'Unsupported' in caplog.records[0].message


def test_bails_out_missing_provider(caplog):
    with TemporaryDirectory() as temp_dir:
        user = get_user()
        create_home(user, root=temp_dir)

        cfg_path = join(temp_dir, user, '.hdyndns', 'hdyndns.ini')
        with open(cfg_path, 'w+') as handle:
            handle.write('[bar.foo]\nsomething=else')

        config = read_config(user, root=temp_dir)
        with pytest.raises(SystemExit):
            sections = filter(lambda s: s != 'DEFAULT', config.keys())
            validate_dns_providers(config, sections)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'CRITICAL'
    assert 'No provider' in caplog.records[0].message


def test_bails_out_missing_api_secret(caplog):
    with TemporaryDirectory() as temp_dir:
        user = get_user()
        create_home(user, root=temp_dir)

        cfg_path = join(temp_dir, user, '.hdyndns', 'hdyndns.ini')
        with open(cfg_path, 'w+') as handle:
            handle.write('[bar.foo]\nprovider=gandi')

        config = read_config(user, root=temp_dir)
        with pytest.raises(SystemExit):
            sections = filter(lambda s: s != 'DEFAULT', config.keys())
            validate_api_secrets(config, sections)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'CRITICAL'
    assert 'No api_secret' in caplog.records[0].message
