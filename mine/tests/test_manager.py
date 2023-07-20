import pytest

from mine.manager import LinuxManager, MacManager, WindowsManager, get_manager
from mine.models import Application


class TestLinuxManager:
    """Unit tests for the Linux manager class."""

    manager = get_manager("Linux")

    def test_init(self):
        """Verify the OS is detected correctly."""
        assert isinstance(self.manager, LinuxManager)

    @pytest.mark.linux_only
    def test_is_running_false(self):
        """Verify a process can be detected as not running."""
        application = Application("Fake Application")
        application.versions.linux = "fake_application.sh"
        assert False is self.manager.is_running(application)

    @pytest.mark.linux_only
    def test_is_running_true(self):
        """Verify a process can be detected as running."""
        application = Application("init")
        application.versions.linux = "init"
        assert True is self.manager.is_running(application)

    def test_is_running_none(self):
        """Verify a process can be detected as untracked."""
        application = Application("Fake Application")
        assert None is self.manager.is_running(application)


class TestMacManager:
    """Unit tests for the Mac manager class."""

    manager = get_manager("Darwin")

    def test_init(self):
        """Verify the OS is detected correctly."""
        assert isinstance(self.manager, MacManager)

    def test_is_running_false(self):
        """Verify a process can be detected as not running."""
        application = Application("Fake Application")
        application.versions.mac = "FakeApplication.app"
        assert False is self.manager.is_running(application)

    @pytest.mark.mac_only
    def test_is_running_true(self):
        """Verify a process can be detected as running."""
        application = Application("Finder")
        application.versions.mac = "Finder.app"
        assert True is self.manager.is_running(application)

    def test_is_running_none(self):
        """Verify a process can be detected as untracked."""
        application = Application("Fake Application")
        assert None is self.manager.is_running(application)

    @pytest.mark.mac_only
    def test_stop(self):
        """Verify a process can be stopped."""
        application = Application("mail")
        application.versions.mac = "Mail.app"
        self.manager.stop(application)
        assert not self.manager.is_running(application)


class TestWindowsManager:
    """Unit tests for the Windows manager class."""

    manager = get_manager("Windows")

    def test_init(self):
        """Verify the OS is detected correctly."""
        assert isinstance(self.manager, WindowsManager)

    @pytest.mark.windows_only
    def test_is_running_false(self):
        """Verify a process can be detected as not running."""
        application = Application("Fake Application")
        application.versions.windows = "FakeApplication.exe"
        assert False is self.manager.is_running(application)

    @pytest.mark.windows_only
    def test_is_running_true(self):
        """Verify a process can be detected as running."""
        application = Application("Explorer")
        application.versions.windows = "explorer.exe"
        assert True is self.manager.is_running(application)

    def test_is_running_none(self):
        """Verify a process can be detected as untracked."""
        application = Application("Fake Application")
        assert None is self.manager.is_running(application)
