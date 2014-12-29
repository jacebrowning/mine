"""Unit tests for the `config` module."""
# pylint: disable=R0201,W0201,W0613

from mine.config import ProgramStatus
from mine.application import Application


class TestProgramStatusEmpty:

    """Unit tests for the program status class with an empty list."""

    def setup_method(self, method):
        self.status = ProgramStatus()
        self.application = Application('my-app')
        self.computer = None

    def test_get_latest(self):
        """Verify None is returned when there is no latest computer."""
        assert None == self.status.get_latest(self.application)

    def test_is_running(self):
        """Verify no app is running when the list is empty."""
        assert False == self.status.is_running(self.application, self.computer)

    def test_start(self):
        """Verify starting an application adds it to the list."""
        self.status.start(self.application, self.computer)
        labels = [status.application for status in self.status.applications]
        assert self.application.label in labels

    def test_stop(self):
        """Verify stopping an application adds it to the list."""
        self.status.stop(self.application, self.computer)
        labels = [status.application for status in self.status.applications]
        assert self.application.label in labels
