"""Unit tests for the `services` module."""

import pytest
from unittest.mock import patch, Mock

import os

from mine import services

from mine.test.conftest import FILES


def test_find_dropbox(tmpdir):
    """Verify a settings file can be found in Dropbox."""
    tmpdir.chdir()
    _touch('Dropbox', '.mine.yml')

    path = services.get_path(tmpdir.strpath)

    assert os.path.isfile(path)


def test_find_dropbox_personal(tmpdir):
    """Verify a settings file can be found in Dropbox (Personal)."""
    tmpdir.chdir()
    _touch('Dropbox (Personal)', '.mine.yml')

    path = services.get_path(tmpdir.strpath)

    assert os.path.isfile(path)


@patch('mine.services.DEPTH', 2)
def test_find_depth(tmpdir):
    """Verify a settings file is not found below the maximum depth."""
    tmpdir.chdir()
    _touch('Dropbox', 'a', 'b', '.mine.yml')

    with pytest.raises(OSError):
        services.get_path(tmpdir.strpath)


@patch('os.path.isdir', Mock(return_value=False))
def test_find_no_home():
    """Verify an error occurs when no home directory is found."""
    with pytest.raises(EnvironmentError):
        services.get_path()


def test_find_no_share():
    """Verify an error occurs when no service directory is found."""
    with pytest.raises(EnvironmentError):
        services.get_path(FILES)


def _touch(*parts):
    """Create an empty file at the given path."""
    path = os.path.join(*parts)
    dirpath = os.path.dirname(path)
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    open(path, 'w').close()
