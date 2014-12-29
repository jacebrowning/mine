"""Data structures for all settings."""

import yorm

from . import common
from .application import Applications
from .computer import Computers
from .status import Statuses, Status, State


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

    def is_running(self, application, computer):
        """Determine if an application is logged as running on a computer."""
        for status in self.applications:
            pass
        return False

    def start(self, application, computer):
        """Log an application as running on a computer."""
        for status in self.applications:
            if status.application == application.label:
                for state in status.application.computers:
                    if state.computer == computer.label:
                        status.timestamps.started = self.counter
                        break
                else:
                    state = State(application.label)
                    state.timestamps.started = self.counter
                    status.application.computers.append(state)
                break
        else:
            status = Status(application.label)
            state = State(application.label)
            state.timestamps.started = self.counter
            status.computers.append(state)
            self.applications.append(status)

    def stop(self, application, computer):
        """Log an application as no longer running on a computer."""
        for status in self.applications:
            if status.application == application.label:
                for state in status.application.computers:
                    if state.computer == computer.label:
                        status.timestamps.stopped = self.counter
                        break
                else:
                    state = State(application.label)
                    state.timestamps.stopped = self.counter
                    status.application.computers.append(state)
                break
        else:
            status = Status(application.label)
            state = State(application.label)
            state.timestamps.stopped = self.counter
            status.computers.append(state)
            self.applications.append(status)


@yorm.map_attr(configuration=ProgramConfiguration)
@yorm.map_attr(status=ProgramStatus)
class Settings:

    """Primary wrapper for all settings."""

    def __init__(self):
        self.configuration = ProgramConfiguration()
        self.status = ProgramStatus()
