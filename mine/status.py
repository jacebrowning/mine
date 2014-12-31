"""Data structures for application/computer status."""

from . import common

import yorm

log = common.logger(__name__)


@yorm.map_attr(started=yorm.standard.Integer)
@yorm.map_attr(stopped=yorm.standard.Integer)
class Timestamps(yorm.container.Dictionary):

    """A dictionary of last start and stop times."""

    def __init__(self, started=0, stopped=0):
        self.started = started
        self.stopped = stopped

    def __repr__(self):
        return "<timestamp {}>".format(self.latest)

    def __eq__(self, other):
        return self.latest == other.latest

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.latest < other.latest

    @property
    def latest(self):
        """Get the latest timestamp."""
        return max((self.started, self.stopped))

    @property
    def active(self):
        """Determine if the timestamps indicate current activity."""
        if not self.started:
            return False
        elif not self.stopped:
            return True
        else:
            return self.started > self.stopped


@yorm.map_attr(computer=yorm.standard.String)
@yorm.map_attr(timestamps=Timestamps)
class State(yorm.container.Dictionary):

    """A dictionary of computer state."""

    def __init__(self, label):
        super().__init__()
        self.computer = label
        self.timestamps = Timestamps()

    def __str__(self):
        return str(self.computer)

    def __lt__(self, other):
        return self.timestamps < other.timestamps


@yorm.map_attr(all=State)
class States(yorm.container.List):

    """A list of computer states for an application."""


@yorm.map_attr(application=yorm.standard.String)
@yorm.map_attr(computers=States)
class Status(yorm.container.Dictionary):

    """A dictionary of computers using an application."""

    def __init__(self, label):
        self.application = label
        self.computers = States()


@yorm.map_attr(all=Status)
class Statuses(yorm.container.List):

    """A list of application statuses."""
