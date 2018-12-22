"""Unit test configuration file."""

import os
import platform

import log
import pytest


ENV = 'TEST_INTEGRATION'  # environment variable to enable integration tests
REASON = "'{0}' variable not set".format(ENV)

ROOT = os.path.dirname(__file__)
FILES = os.path.join(ROOT, 'files')


def pytest_configure(config):
    """Disable verbose output when running tests."""
    log.init(
        level=log.DEBUG, format="[%(levelname)-8s] (%(name)s @%(lineno)4d) %(message)s"
    )
    log.silence('yorm', allow_warning=True)

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
    if 'linux_only' in item.keywords and platform.system() != 'Linux':
        pytest.skip("test can only be run on Linux")
    if 'mac_only' in item.keywords and platform.system() != 'Darwin':
        pytest.skip("test can only be run on OS X")
    if 'windows_only' in item.keywords and platform.system() != 'Windows':
        pytest.skip("test can only be run on Windows")
