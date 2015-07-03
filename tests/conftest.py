"""Integration test configuration file."""

import os

from mine.test.conftest import pytest_configure, pytest_runtest_setup

ROOT = os.path.dirname(__file__)
FILES = os.path.join(ROOT, 'files')
