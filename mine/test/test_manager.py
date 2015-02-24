"""Unit tests for the `manager` module."""
# pylint: disable=R0201

import pytest

from mine.manager import get_manager, LinuxManager, MacManager, WindowsManager
from mine.application import Application


class TestLinuxManager:

    """Unit tests for the Linux manager class."""

    manager = get_manager('Linux')

    def test_init(self):
        """Verify the OS is detected correctly."""
        assert isinstance(self.manager, LinuxManager)

    def test_is_running_false(self):
        """Verify a process can be detected as not running."""
        pytest.skip("TODO: implement test")
        application = Application('fake-program-for-mine')
        application.versions.linux = 'fake_program_for_mine.sh'
        assert False is self.manager.is_running(application)

    @pytest.mark.linux_only
    def test_is_running_true(self):
        """Verify a process can be detected as running."""
        pytest.skip("TODO: implement test")

    def test_is_running_none(self):
        """Verify a process can be detected as untracked."""
        application = Application('fake-program-for-mine')
        assert None is self.manager.is_running(application)


class TestMacManager:

    """Unit tests for the Mac manager class."""

    manager = get_manager('Darwin')

    def test_init(self):
        """Verify the OS is detected correctly."""
        assert isinstance(self.manager, MacManager)

    def test_is_running_false(self):
        """Verify a process can be detected as not running."""
        application = Application('fake-program-for-mine')
        application.versions.mac = 'FakeProgramForMine.app'
        assert False is self.manager.is_running(application)

    @pytest.mark.mac_only
    def test_is_running_true(self):
        """Verify a process can be detected as running."""
        application = Application('finder')
        application.versions.mac = 'Finder.app'
        assert True is self.manager.is_running(application)

    def test_is_running_none(self):
        """Verify a process can be detected as untracked."""
        application = Application('fake-program-for-mine')
        assert None is self.manager.is_running(application)

    @pytest.mark.mac_only
    @pytest.mark.not_ide
    @pytest.mark.integration
    def test_stop_start(self):
        """Verify a process can be stopped and started."""
        application = Application('mail')
        application.versions.mac = 'Mail.app'
        self.manager.stop(application)
        assert not self.manager.is_running(application)
        self.manager.start(application)
        assert self.manager.is_running(application)


class TestWindowsManager:

    """Unit tests for the Windows manager class."""

    manager = get_manager('Windows')

    def test_init(self):
        """Verify the OS is detected correctly."""
        assert isinstance(self.manager, WindowsManager)

    def test_is_running_false(self):
        """Verify a process can be detected as not running."""
        pytest.skip("TODO: implement test")
        application = Application('fake-program-for-mine')
        application.versions.windows = 'FakeProgramForMine.exe'
        assert False is self.manager.is_running(application)

    @pytest.mark.windows_only
    def test_is_running_true(self):
        """Verify a process can be detected as running."""
        pytest.skip("TODO: implement test")
        application = Application('explorer')
        application.versions.windows = 'explorer.exe'
        assert True is self.manager.is_running(application)

    def test_is_running_none(self):
        """Verify a process can be detected as untracked."""
        application = Application('fake-program-for-mine')
        assert None is self.manager.is_running(application)
