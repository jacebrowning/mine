"""Data structures for application/computer status."""

import functools
from dataclasses import dataclass, field

import log

from .application import Application
from .computer import Computer
from .timestamp import Timestamp


def log_running(func):
    @functools.wraps(func)
    def wrapped(self, application, computer):
        running = func(self, application, computer)
        log.debug(
            "%s marked as %s on: %s",
            application,
            "started" if running else "stopped",
            computer,
        )
        return running

    return wrapped


def log_starting(func):
    @functools.wraps(func)
    def wrapped(self, application, computer):
        log.debug("Marking %s as started on %s...", application, computer)
        result = func(self, application, computer)
        log.debug("%s marked as started on: %s", application, computer)
        return result

    return wrapped


def log_stopping(func):
    @functools.wraps(func)
    def wrapped(self, application, computer):
        log.debug("Marking %s as stopped on %s...", application, computer)
        result = func(self, application, computer)
        log.debug("%s marked as stopped on: %s", application, computer)
        return result

    return wrapped


@dataclass
class State:
    """Dictionary of computer state."""

    computer: str
    timestamp: Timestamp = field(default_factory=Timestamp)

    def __str__(self):
        return str(self.computer)

    def __lt__(self, other):
        return str(self.computer).lower() < str(other.computer).lower()


@dataclass
class Status:
    """Dictionary of computers using an application."""

    application: str
    computers: list[State] = field(default_factory=list)
    next: str | None = None

    def __str__(self):
        return str(self.application)

    def __lt__(self, other):
        return str(self.application).lower() < str(other.application).lower()


@dataclass
class ProgramStatus:
    """Dictionary of current program status."""

    counter: int = 0
    applications: list[Status] = field(default_factory=list)

    def find(self, application: Application):
        """Return the application status for an application."""
        for status in self.applications:
            if status.application == application.name:
                break
        else:
            status = Status(application.name)
            self.applications.append(status)
        return status

    def get_latest(self, application: Application) -> str | None:
        """Get the last computer's name logged as running an application."""
        for status in self.applications:
            if status.application == application.name:
                states = [s for s in status.computers if s.timestamp.active]
                if states:
                    states.sort(key=lambda s: s.timestamp, reverse=True)
                    log.debug(
                        "%s marked as started on: %s",
                        application,
                        ", ".join(str(s) for s in states),
                    )
                    return states[0].computer

        log.debug(f"{application} marked as started on: nothing")
        return None

    @log_running
    def is_running(self, application: Application, computer: Computer):
        """Determine if an application is logged as running on a computer."""
        for status in self.applications:
            if status.application == application.name:
                for state in status.computers:
                    if state.computer == computer.name:
                        return state.timestamp.active

        # Status not found, assume the application is not running
        return False

    def queue(self, application: Application, computer: Computer):
        """Record an application as queued for launch on a computer."""
        status = self.find(application)
        status.next = computer.name

    @log_starting
    def start(self, application: Application, computer: Computer):
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
            status = None  # type: ignore

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
    def stop(self, application: Application, computer: Computer):
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
            status = None  # type: ignore

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
