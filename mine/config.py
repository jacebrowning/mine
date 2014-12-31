"""Data structures for all settings."""

import functools

import yorm

from . import common
from .application import Applications
from .computer import Computers
from .status import Statuses, Status, State

log = common.logger(__name__)


def log_running(func):
    """Decorator for methods that return application status."""
    @functools.wraps(func)
    def wrapped(self, application, computer):
        """Wrapped method to log if an application is running."""
        running = func(self, application, computer)
        log.debug("%s was marked as%s running on %s",
                  application, "" if running else " not", computer)
        return running
    return wrapped


def log_stopped(func):
    """Decorator for methods that mark an application as stopped."""
    @functools.wraps(func)
    def wrapped(self, application, computer):
        """Wrapped method to log that an application is stopped."""
        log.info("marking %s as stopped on %s...", application, computer)
        return func(self, application, computer)
    return wrapped


@yorm.map_attr(applications=Applications)
@yorm.map_attr(computers=Computers)
class ProgramConfiguration(yorm.container.Dictionary):

    """A dictionary of configuration settings."""

    def __init__(self):
        self.applications = Applications()
        self.computers = Computers()


@yorm.map_attr(applications=Statuses)
@yorm.map_attr(counter=yorm.standard.Integer)
class ProgramStatus(yorm.container.Dictionary):

    """A dictionary of configuration settings."""

    def __init__(self):
        self.applications = Statuses()
        self.counter = 0

    def get_latest(self, application):
        """Get the last computer logged as running an application."""
        for status in self.applications:
            pass
        return None

    @log_running
    def is_running(self, application, computer):
        """Determine if an application is logged as running on a computer."""
        for status in self.applications:
            if status.application == application.label:
                for state in status.computers:
                    if state.computer == computer.label:
                        return state.timestamps.active
                break
        else:
            status = None

        # Status not found so add the application/computer as stopped
        self.counter += 1
        state = State(computer.label)
        state.timestamps.stopped = self.counter
        if status is None:
            status = Status(application.label)
            status.computers.append(state)
            self.applications.append(status)
        else:
            status.computers.append(state)
        return state.timestamps.active

    def start(self, application, computer):
        """Log an application as running on a computer."""
        for status in self.applications:
            if status.application == application.label:
                for state in status.application.computers:
                    if state.computer == computer.label:
                        self.counter += 1
                        status.timestamps.started = self.counter
                        return
                break
        else:
            status = None

        # Status not found so add the application/computer as started
        self.counter += 1
        state = State(computer.label)
        state.timestamps.started = self.counter
        if status is None:
            status = Status(application.label)
            status.computers.append(state)
            self.applications.append(status)
        else:
            status.computers.append(state)

    @log_stopped
    def stop(self, application, computer):
        """Log an application as no longer running on a computer."""
        for status in self.applications:
            if status.application == application.label:
                for state in status.computers:
                    if state.computer == computer.label:
                        self.counter += 1
                        state.timestamps.stopped = self.counter
                        return
                break
        else:
            status = None

        # Status not found so add the application/computer as stopped
        self.counter += 1
        state = State(computer.label)
        state.timestamps.stopped = self.counter
        if status is None:
            status = Status(application.label)
            status.computers.append(state)
            self.applications.append(status)
        else:
            status.computers.append(state)


@yorm.map_attr(configuration=ProgramConfiguration)
@yorm.map_attr(status=ProgramStatus)
class Settings:

    """Primary wrapper for all settings."""

    def __init__(self):
        self.configuration = ProgramConfiguration()
        self.status = ProgramStatus()

    def __repr__(self):
        return "settings"
