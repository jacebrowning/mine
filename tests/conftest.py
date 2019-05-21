"""Integration tests configuration file."""

import os

from mine.tests.conftest import (  # pylint: disable=unused-import
    pytest_configure,
    pytest_runtest_setup,
)


ROOT = os.path.dirname(__file__)
FILES = os.path.join(ROOT, 'files')
