"""Unit tests for the `status` module."""
# pylint: disable=R0201,W0201,W0613

from unittest.mock import Mock

from mine.status import ProgramStatus
from mine.application import Application


class TestProgramStatusEmpty:

    """Unit tests for the program status class with an empty list."""

    def setup_method(self, method):
        """Create an empty program status for all tests."""
        self.status = ProgramStatus()
        self.application = Application('my-application')
        self.computer = Mock()

    def test_get_latest(self):
        """Verify None is returned when there is no latest computer."""
        assert None == self.status.get_latest(self.application)

    def test_is_running(self):
        """Verify no app is running when the list is empty."""
        assert False == self.status.is_running(self.application, self.computer)

    def test_start(self):
        """Verify starting an application adds it to the list."""
        self.status.start(self.application, self.computer)
        names = [status.application for status in self.status.applications]
        assert self.application.name in names

    def test_stop(self):
        """Verify stopping an application adds it to the list."""
        self.status.stop(self.application, self.computer)
        names = [status.application for status in self.status.applications]
        assert self.application.name in names
