"""Integration tests configuration file."""

import os

from mine.tests.conftest import pytest_configure, pytest_runtest_setup  # pylint: disable=unused-import

ROOT = os.path.dirname(__file__)
FILES = os.path.join(ROOT, 'files')
