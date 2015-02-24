"""Unit tests for the `status` module."""
# pylint: disable=R0201,W0201,W0613

import pytest
from unittest.mock import Mock

from mine.status import State, Status, ProgramStatus
from mine.application import Application


class TestState:

    """Unit tests for the computer state class."""

    state1 = State('computer1')
    state2 = State('computer2')
    state2.timestamp.started = 42
    state3 = State('Computer2')
    state4 = State('Computer2')

    str_state = [
        ("computer1", state1),
        ("computer2", state2),
        ("Computer2", state3),
    ]

    @pytest.mark.parametrize("string,state", str_state)
    def test_str(self, string, state):
        """Verify states can be converted to strings."""
        assert string == str(state)

    def test_eq(self):
        """Verify states can be equated."""
        assert self.state3 == self.state4
        assert self.state2 != self.state3
        assert self.state1 != self.state2

    def test_lt(self):
        """Verify states can be sorted."""
        assert self.state1 < self.state2
        assert self.state3 > self.state1


class TestStatus:

    """Unit tests for the application status class."""

    status1 = Status('app1')
    status2 = Status('app2')
    status3 = Status('App2')
    status4 = Status('App2')

    str_status = [
        ("app1", status1),
        ("app2", status2),
        ("App2", status3),
    ]

    @pytest.mark.parametrize("string,status", str_status)
    def test_str(self, string, status):
        """Verify statuss can be converted to strings."""
        assert string == str(status)

    def test_eq(self):
        """Verify statuss can be equated."""
        assert self.status3 == self.status4
        assert self.status2 != self.status3
        assert self.status1 != self.status2

    def test_lt(self):
        """Verify statuss can be sorted."""
        assert self.status1 < self.status2
        assert self.status3 > self.status1


class TestProgramStatus:

    """Unit tests for the program status class."""

    def setup_method(self, method):
        """Create an empty program status for all tests."""
        self.status = ProgramStatus()
        self.application = Application('my-application')
        self.computer = Mock()
        self.computer.name = 'local'
        self.computer2 = Mock()
        self.computer2.name = 'remote'
        self.computer3 = Mock()
        self.computer3.name = 'remote2'

    def test_get_latest(self):
        """Verify the latest computer can be determined."""
        self.status.start(self.application, self.computer)
        self.status.start(self.application, self.computer2)
        self.status.stop(self.application, self.computer3)
        assert self.computer2.name == self.status.get_latest(self.application)
        assert 3 == self.status.counter

    def test_get_latest_empty(self):
        """Verify None is returned when there is no latest computer."""
        assert None is self.status.get_latest(self.application)
        assert 0 == self.status.counter

    def test_is_running_empty(self):
        """Verify no app is running when the list is empty."""
        assert False is self.status.is_running(self.application, self.computer)
        assert 0 == self.status.counter

    def test_queue(self):
        """Verify queuing an application sets the next computer."""
        self.status.queue(self.application, self.computer)
        app_status = self.status.find(self.application)
        assert self.computer.name == app_status.next

    def test_start(self):
        """Verify starting an application adds it to the list."""
        self.status.start(self.application, self.computer)
        names = [status.application for status in self.status.applications]
        assert self.application.name in names
        assert 1 == self.status.counter

    def test_stop(self):
        """Verify stopping an application adds it to the list."""
        self.status.stop(self.application, self.computer)
        names = [status.application for status in self.status.applications]
        assert self.application.name in names
        assert 1 == self.status.counter

    def test_start_again(self):
        """Verify starting a known application increments the counter."""
        self.status.start(self.application, self.computer)
        self.status.start(self.application, self.computer)
        self.status.start(self.application, self.computer2)
        assert self.status.is_running(self.application, self.computer)
        assert self.status.is_running(self.application, self.computer2)
        assert 3 == self.status.counter

    def test_stop_again(self):
        """Verify stopping a known application increments the counter."""
        self.status.stop(self.application, self.computer)
        self.status.stop(self.application, self.computer)
        self.status.stop(self.application, self.computer2)
        assert not self.status.is_running(self.application, self.computer)
        assert not self.status.is_running(self.application, self.computer2)
        assert 3 == self.status.counter
