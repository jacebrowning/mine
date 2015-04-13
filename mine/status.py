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


@yorm.attr(computer=yorm.converters.String)
@yorm.attr(timestamp=Timestamp)
class State(yorm.converters.AttributeDictionary):

    """A dictionary of computer state."""

    def __init__(self, name):
        super().__init__()
        self.computer = name
        self.timestamp = Timestamp()

    def __str__(self):
        return str(self.computer)

    def __lt__(self, other):
        return str(self.computer).lower() < str(other.computer).lower()


@yorm.attr(all=State)
class StateList(yorm.converters.SortedList):

    """A list of computer states for an application."""


@yorm.attr(application=yorm.converters.String)
@yorm.attr(computers=StateList)
@yorm.attr(next=yorm.converters.NoneString)
class Status(yorm.converters.AttributeDictionary):

    """A dictionary of computers using an application."""

    def __init__(self, name):
        super().__init__()
        self.application = name
        self.computers = StateList()
        self.next = None

    def __str__(self):
        return str(self.application)

    def __lt__(self, other):
        return str(self.application).lower() < str(other.application).lower()


@yorm.attr(all=Status)
class StatusList(yorm.converters.SortedList):

    """A list of application statuses."""


@yorm.attr(applications=StatusList)
@yorm.attr(counter=yorm.converters.Integer)
class ProgramStatus(yorm.converters.AttributeDictionary):

    """A dictionary of current program status."""

    def __init__(self):
        super().__init__()
        self.applications = StatusList()
        self.counter = 0

    def find(self, application):
        """Return the application status for an application."""
        for app_status in self.applications:
            if app_status.application == application.name:
                break
        else:
            app_status = Status(application.name)
            self.applications.append(app_status)
        return app_status

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

        # Status not found, assume the application is not running
        return False

    def queue(self, application, computer):
        """Record an application as queued for launch on a computer."""
        status = self.find(application)
        status.next = computer.name

    @log_starting
    def start(self, application, computer):
        """Record an application as running on a computer."""
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

        # Status not found, add the application/computer as started
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
        """Record an application as no longer running on a computer."""
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

        # Status not found, add the application/computer as stopped
        self.counter += 1
        state = State(computer.name)
        state.timestamp.stopped = self.counter
        if status is None:
            status = Status(application.name)
            status.computers.append(state)
            self.applications.append(status)
        else:
            status.computers.append(state)
