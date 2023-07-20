"""Unit test configuration file."""

import os
import platform

import log
import pytest

ENV = "TEST_INTEGRATION"  # environment variable to enable integration tests
REASON = "'{0}' variable not set".format(ENV)

ROOT = os.path.dirname(__file__)
FILES = os.path.join(ROOT, "files")


def pytest_configure(config):
    """Disable verbose output when running tests."""
    log.init(
        level=log.DEBUG, format="[%(levelname)-8s] (%(name)s @%(lineno)4d) %(message)s"
    )
    log.silence("datafiles", allow_warning=True)

    terminal = config.pluginmanager.getplugin("terminal")
    terminal.TerminalReporter.showfspath = False


def pytest_runtest_setup(item):
    if "linux_only" in item.keywords and platform.system() != "Linux":
        pytest.skip("Test can only be run on Linux")
    if "mac_only" in item.keywords and platform.system() != "Darwin":
        pytest.skip("Test can only be run on macOS")
    if "windows_only" in item.keywords and platform.system() != "Windows":
        pytest.skip("Test can only be run on Windows")
