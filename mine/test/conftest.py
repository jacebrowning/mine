"""Unit test configuration file."""
# pylint:disable=E1101

import os
import pytest
import platform
import yorm

ENV = 'TEST_INTEGRATION'  # environment variable to enable integration tests
REASON = "'{0}' variable not set".format(ENV)

ROOT = os.path.dirname(__file__)
FILES = os.path.join(ROOT, 'files')


def pytest_configure(config):
    """Disable verbose output when running tests."""
    terminal = config.pluginmanager.getplugin('terminal')
    base = terminal.TerminalReporter

    class QuietReporter(base):
        """A py.test reporting that only shows dots when running tests."""

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.verbosity = 0
            self.showlongtestinfo = False
            self.showfspath = False

    terminal.TerminalReporter = QuietReporter


def pytest_runtest_setup(item):
    """pytest setup."""
    if 'integration' in item.keywords:
        if not os.getenv(ENV):
            pytest.skip(REASON)
        else:
            yorm.settings.fake = False
    else:
        yorm.settings.fake = True

    if 'linux_only' in item.keywords and platform.system() != 'Linux':
        pytest.skip("test can only be run on Linux")
    if 'mac_only' in item.keywords and platform.system() != 'Darwin':
        pytest.skip("test can only be run on OS X")
    if 'windows_only' in item.keywords and platform.system() != 'Windows':
        pytest.skip("test can only be run on Windows")

    if os.getenv('TEST_IDE') and 'not_ide' in item.keywords:
        pytest.skip("test cannot be run from an IDE")


@pytest.fixture
def path(tmpdir):
    """Figure to create a temporary settings file path."""
    tmpdir.chdir()
    return tmpdir.join('custom.ext').strpath
