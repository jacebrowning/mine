"""pytest configuration."""

import os
import pytest

ENV = 'TEST_INTEGRATION'  # environment variable to enable integration tests
REASON = "'{0}' variable not set".format(ENV)

ROOT = os.path.dirname(__file__)
FILES = os.path.join(ROOT, 'files')


def pytest_runtest_setup(item):
    """pytest setup."""
    if 'integration' in item.keywords and not os.getenv(ENV):
        pytest.skip(REASON)
