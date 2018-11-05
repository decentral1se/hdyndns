from os.path import exists, join
from tempfile import TemporaryDirectory

import pytest

from hdyndns.config import create_home, get_user


def test_can_read_user():
    assert isinstance(get_user(), str)


def test_handles_not_able_to_read_user(mocker, caplog):
    target = 'hdyndns.config.check_output'

    with pytest.raises(SystemExit):
        with mocker.patch(target, side_effect=OSError('foobar')):
            get_user()

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'CRITICAL'
    assert 'foobar' in caplog.records[0].message


def test_creates_home_path():
    with TemporaryDirectory() as temp_dir:
        user = get_user()
        create_home(user, root=temp_dir)
        assert exists(join(temp_dir, user, '.hdyndns'))


def test_does_not_re_create_home_path():
    with TemporaryDirectory() as temp_dir:
        user = get_user()
        create_home(user, root=temp_dir)
        create_home(user, root=temp_dir)
        assert exists(join(temp_dir, user, '.hdyndns'))
