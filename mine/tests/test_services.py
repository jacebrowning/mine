# pylint: disable=redefined-outer-name

import os
from unittest.mock import Mock, patch

import pytest

from mine import services
from mine.tests.conftest import FILES


@pytest.fixture
def tmp_dir(tmpdir):
    cwd = os.getcwd()
    tmpdir.chdir()
    yield str(tmpdir)
    os.chdir(cwd)


def touch(*parts):
    """Create an empty file at the given path."""
    path = os.path.join(*parts)
    dirpath = os.path.dirname(path)
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    open(path, "w", encoding="utf-8").close()


class TestFindRoot:
    @patch("os.listdir", Mock(return_value=[]))
    @patch("os.getenv", Mock(return_value=True))
    def test_ci_workaround_enabled(self):
        root = services.find_root(top="mock/top")
        assert "mock/top" == root

    @patch("os.listdir", Mock(return_value=[]))
    @patch("os.getenv", Mock(return_value=False))
    def test_ci_workaround_disabled(self):
        with pytest.raises(EnvironmentError):
            services.find_root(top="mock/top")


class TestFindConfigPath:
    def test_find_dropbox(self, tmp_dir):
        """Verify a settings file can be found in Dropbox."""
        touch("Dropbox", "mine.yml")

        path = services.find_config_path(tmp_dir)

        assert os.path.isfile(path)

    def test_find_dropbox_personal(self, tmp_dir):
        """Verify a settings file can be found in Dropbox (Personal)."""
        touch("Dropbox (Personal)", "mine.yml")

        path = services.find_config_path(tmp_dir)

        assert os.path.isfile(path)

    @patch("mine.services.DEPTH", 2)
    def test_find_depth(self, tmp_dir):
        """Verify a settings file is not found below the maximum depth."""
        touch("Dropbox", "a", "b", "mine.yml")

        with pytest.raises(OSError):
            services.find_config_path(tmp_dir)

    def test_find_no_share(self):
        """Verify an error occurs when no service directory is found."""
        with pytest.raises(EnvironmentError):
            with patch("os.getenv", Mock(return_value=False)):
                services.find_config_path(FILES)


@patch("os.remove")
class TestDeleteConflicts:
    @staticmethod
    def _create_conflicts(tmp_dir, count=2):
        for index in range(count):
            fmt = "{} (Jace's conflicted copy 2015-03-11).fake"
            filename = fmt.format(index)
            touch(tmp_dir, filename)

        return tmp_dir

    def test_fail_when_leftover_conflicts(self, _, tmpdir):
        root = self._create_conflicts(tmpdir)

        result = services.delete_conflicts(root)

        assert False is result

    def test_pass_when_no_conflicts(self, _, tmpdir):
        root = self._create_conflicts(tmpdir, count=0)

        result = services.delete_conflicts(root)

        assert True is result

    def test_no_deletion_without_force(self, mock_remove, tmpdir):
        root = self._create_conflicts(tmpdir)

        services.delete_conflicts(root, force=False)

        assert 0 == mock_remove.call_count

    def test_deletion_count_is_correct(self, mock_remove, tmpdir):
        root = self._create_conflicts(tmpdir, count=2)

        services.delete_conflicts(root, force=True)

        assert 2 == mock_remove.call_count
