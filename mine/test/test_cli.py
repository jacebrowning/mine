"""Unit tests for the 'cli' module."""
# pylint: disable=R0201

import pytest
from unittest.mock import Mock, patch
import logging

from mine import cli
from mine import common


class TestMain:

    """Unit tests for the `main` function."""

    @patch('mine.cli.run', Mock(return_value=True))
    def test_run(self):
        """Verify the CLI can be run."""
        cli.main([])

    @patch('mine.cli.run', Mock(return_value=False))
    def test_run_fail(self):
        """Verify the CLI can detect errors."""
        with pytest.raises(SystemExit):
            cli.main([])

    def test_help(self):
        """Verify the CLI help text can be displayed."""
        with pytest.raises(SystemExit):
            cli.main(['--help'])

    @patch('mine.cli.run', Mock(side_effect=KeyboardInterrupt))
    def test_interrupt(self):
        """Verify the CLI can be interrupted."""
        with pytest.raises(SystemExit):
            cli.main([])


def mock_run(*args, **kwargs):
    """Placeholder logic for logging tests."""
    logging.debug(args)
    logging.debug(kwargs)
    logging.warning("warning")
    logging.error("error")
    return True


@patch('mine.cli.run', mock_run)
class TestLogging:

    """Integration tests for the Doorstop CLI logging."""

    arg_verbosity = [
        ('', 0),
        ('-v', 1),
        ('-vv', 2),
        ('-vvv', 3),
        ('-vvvv', 4),
        ('-vvvvv', 4),
        ('-q', -1),
    ]

    @pytest.mark.parametrize("arg,verbosity", arg_verbosity)
    def test_verbose(self, arg, verbosity):
        """Verify verbose level can be set."""
        cli.main([arg] if arg else [])
        assert verbosity == common.verbosity