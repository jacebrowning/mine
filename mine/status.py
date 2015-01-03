"""Data structures for application/computer status."""

import functools

from . import common
from .timestamp import Timestamp

import yorm

log = common.logger(__name__)


def log_running(func):
    """Decorator for methods that return application status."""
    @functools.wraps(func)
    def wrapped(self, application, computer):
        """Wrapped method to log if an application is running."""
        running = func(self, application, computer)
        log.debug("%s marked as %s on: %s",
                  application, "started" if running else "stopped", computer)
        return running
    return wrapped


def log_starting(func):
    """Decorator for methods that mark an application as started."""
    @functools.wraps(func)
    def wrapped(self, application, computer):
        """Wrapped method to log that an application is started."""
        log.debug("marking %s as started on %s...", application, computer)
        result = func(self, application, computer)
        log.debug("%s marked as started on: %s", application, computer)
        return result
    return wrapped


def log_stopping(func):
    """Decorator for methods that mark an application as stopped."""
    @functools.wraps(func)
    def wrapped(self, application, computer):
        """Wrapped method to log that an application is stopped."""
        log.debug("marking %s as stopped on %s...", application, computer)
        result = func(self, application, computer)
        log.debug("%s marked as stopped on: %s", application, computer)
        return result
    return wrapped


@yorm.map_attr(computer=yorm.standard.String)
@yorm.map_attr(timestamp=Timestamp)
class State(yorm.extended.AttributeDictionary):

    """A dictionary of computer state."""

    def __init__(self, name):
        super().__init__()
        self.computer = name
        self.timestamp = Timestamp()

    def __str__(self):
        return str(self.computer)

    def __lt__(self, other):
        return self.computer < other.computer


@yorm.map_attr(all=State)
class StateList(yorm.extended.SortedList):

    """A list of computer states for an application."""


@yorm.map_attr(application=yorm.standard.String)
@yorm.map_attr(computers=StateList)
class Status(yorm.extended.AttributeDictionary):

    """A dictionary of computers using an application."""

    def __init__(self, name):
        super().__init__()
        self.application = name
        self.computers = StateList()

    def __lt__(self, other):
        return self.application < other.application


@yorm.map_attr(all=Status)
class StatusList(yorm.extended.SortedList):

    """A list of application statuses."""


@yorm.map_attr(applications=StatusList)
@yorm.map_attr(counter=yorm.standard.Integer)
class ProgramStatus(yorm.extended.AttributeDictionary):

    """A dictionary of current program status."""

    def __init__(self):
        super().__init__()
        self.applications = StatusList()
        self.counter = 0

    def get_latest(self, application):
        """Get the last computer's name logged as running an application."""
        for status in self.applications:
            if status.application == application.name:
                states = [s for s in status.computers if s.timestamp.active]
                if states:
                    states.sort(key=lambda s: s.timestamp, reverse=True)
                    log.debug("%s marked as started on: %s", application,
                              ', '.join(str(s) for s in states))
                    # TODO: consider returning the computer instance?
                    return states[0].computer

        log.debug("marked as started on: nothing")
        return None

    @log_running
    def is_running(self, application, computer):
        """Determine if an application is logged as running on a computer."""
        for status in self.applications:
            if status.application == application.name:
                for state in status.computers:
                    if state.computer == computer.name:
                        return state.timestamp.active
                break
        else:
            status = None

        # TODO: this method probably doesn't need to set a default
        # Status not found so add the application/computer as stopped
        self.counter += 1
        state = State(computer.name)
        state.timestamp.stopped = self.counter
        if status is None:
            status = Status(application.name)
            status.computers.append(state)
            self.applications.append(status)
        else:
            status.computers.append(state)
        return state.timestamp.active

    @log_starting
    def start(self, application, computer):
        """Log an application as running on a computer."""
        for status in self.applications:
            if status.application == application.name:
                for state in status.computers:
                    if state.computer == computer.name:
                        self.counter += 1
                        state.timestamp.started = self.counter
                        return
                break
        else:
            status = None

        # Status not found so add the application/computer as started
        self.counter += 1
        state = State(computer.name)
        state.timestamp.started = self.counter
        if status is None:
            status = Status(application.name)
            status.computers.append(state)
            self.applications.append(status)
        else:
            status.computers.append(state)

    @log_stopping
    def stop(self, application, computer):
        """Log an application as no longer running on a computer."""
        for status in self.applications:
            if status.application == application.name:
                for state in status.computers:
                    if state.computer == computer.name:
                        self.counter += 1
                        state.timestamp.stopped = self.counter
                        return
                break
        else:
            status = None

        # Status not found so add the application/computer as stopped
        self.counter += 1
        state = State(computer.name)
        state.timestamp.stopped = self.counter
        if status is None:
            status = Status(application.name)
            status.computers.append(state)
            self.applications.append(status)
        else:
            status.computers.append(state)
