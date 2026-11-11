# pylint: disable=redefined-outer-name

import logging
import os
from unittest.mock import Mock, patch

import pytest

from mine import cli, common
from mine.models import Application


@pytest.fixture
def tmp_path(tmpdir):
    return tmpdir.join("custom.yml").strpath


class TestMain:
    """Unit tests for the `main` function."""

    @patch("mine.cli.run", Mock(return_value=True))
    def test_run(self):
        """Verify the CLI can be run."""
        cli.main([])

    @patch("mine.cli.run", Mock(return_value=False))
    def test_run_fail(self):
        """Verify the CLI can detect errors."""
        with pytest.raises(SystemExit):
            cli.main([])

    def test_help(self):
        """Verify the CLI help text can be displayed."""
        with pytest.raises(SystemExit):
            cli.main(["--help"])

    @patch("mine.cli.run", Mock(side_effect=KeyboardInterrupt))
    def test_interrupt(self):
        """Verify the CLI can be interrupted."""
        with pytest.raises(SystemExit):
            cli.main([])

    @patch("mine.cli.log")
    @patch("mine.cli.run", Mock(side_effect=KeyboardInterrupt))
    def test_interrupt_verbose(self, mock_log):
        """Verify the CLI can be interrupted (verbose output)."""
        with pytest.raises(SystemExit):
            cli.main(["-vvvv"])
        assert mock_log.exception.call_count == 1

    @patch("mine.daemon.application", None)
    def test_path(self, tmp_path):
        """Verify a custom setting file path can be used."""
        cli.main(["--file", tmp_path])

        assert os.path.isfile(tmp_path)

    @patch("mine.cli.run")
    def test_daemon(self, mock_run):
        cli.main(["--daemon"])
        mock_run.assert_called_once_with(path=None, delay=300)

    @patch("mine.cli.run")
    def test_daemon_with_specific_delay(self, mock_run):
        cli.main(["--daemon", "42"])
        mock_run.assert_called_once_with(path=None, delay=42)

    @patch("mine.daemon.application", Application("?"))
    def test_warning_when_daemon_is_not_running(self, tmp_path):
        with pytest.raises(SystemExit):
            cli.main(["--file", tmp_path])


class TestSwitch:
    """Unit tests for the `switch` function."""

    @patch("mine.cli.run")
    def test_switch(self, mock_run):
        """Verify a the current computer can be queued."""
        cli.main(["switch"])
        mock_run.assert_called_once_with(path=None, delay=None, switch=True)

    @patch("mine.cli.run")
    def test_switch_specific(self, mock_run):
        """Verify a specific computer can be queued."""
        cli.main(["switch", "foobar"])
        mock_run.assert_called_once_with(path=None, delay=None, switch="foobar")


class TestClean:
    @patch("mine.cli.run")
    def test_clean(self, mock_run):
        cli.main(["clean"])
        mock_run.assert_called_once_with(
            path=None, delay=None, delete=True, force=False, reset=False, stop=False
        )

    @patch("mine.cli.run")
    def test_clean_with_force(self, mock_run):
        cli.main(["clean", "--force"])
        mock_run.assert_called_once_with(
            path=None, delay=None, delete=True, force=True, reset=False, stop=False
        )

    @patch("mine.cli.run")
    def test_clean_with_stop(self, mock_run):
        cli.main(["clean", "--stop"])
        mock_run.assert_called_once_with(
            path=None, delay=None, delete=True, force=False, reset=False, stop=True
        )


class TestEdit:
    @patch("mine.cli.run")
    def test_edit(self, mock_run):
        cli.main(["edit"])
        mock_run.assert_called_once_with(path=None, delay=None, edit=True)


class TestCleanRun:
    """Integration tests for `run` with the `delete` path."""

    @patch("mine.services.find_root")
    def test_clean_without_conflicts_succeeds(self, mock_root, tmpdir_factory):
        """`mine clean` on a clean tree must succeed (exit 0)."""
        root = tmpdir_factory.mktemp("clean")
        mock_root.return_value = str(root)
        path = str(root.join("mine.yml"))
        assert cli.run(path, delete=True, cleanup=False) is True

    @patch("mine.services.find_root")
    def test_clean_with_force_and_nothing_to_delete_succeeds(
        self, mock_root, tmpdir_factory
    ):
        """`mine clean --force` with no conflicts must succeed (exit 0)."""
        root = tmpdir_factory.mktemp("clean-force")
        mock_root.return_value = str(root)
        path = str(root.join("mine.yml"))
        assert cli.run(path, delete=True, force=True, cleanup=False) is True

    @patch("mine.services.find_root")
    def test_clean_with_force_deletes_and_succeeds(
        self, mock_root, tmpdir_factory
    ):
        """`mine clean --force` deletes conflicts and succeeds (exit 0)."""
        root = tmpdir_factory.mktemp("clean-delete")
        mock_root.return_value = str(root)
        conflict = root.join("0 (Jace's conflicted copy 2015-03-11).fake")
        conflict.write("")
        path = str(root.join("mine.yml"))
        assert cli.run(path, delete=True, force=True, cleanup=False) is True
        assert not os.path.exists(str(conflict))


def _mock_run(*args, **kwargs):
    """Placeholder logic for logging tests."""
    logging.debug(args)
    logging.debug(kwargs)
    logging.warning("warning")
    logging.error("error")
    return True


@patch("mine.cli.run", _mock_run)
class TestLogging:
    """Integration tests for the Doorstop CLI logging."""

    arg_verbosity = [
        ("", 0),
        ("-v", 1),
        ("-vv", 2),
        ("-vvv", 3),
        ("-vvvv", 4),
        ("-vvvvv", 4),
        ("-q", -1),
    ]

    @pytest.mark.parametrize("arg,verbosity", arg_verbosity)
    def test_verbose(self, arg, verbosity):
        """Verify verbose level can be set."""
        cli.main([arg] if arg else [])
        assert verbosity == common.verbosity
