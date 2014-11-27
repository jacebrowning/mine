"""Data structures for application/computer status."""
# pylint: disable=R0903

from . import common

import yorm

log = common.logger(__name__)


@yorm.map_attr(started=common.NoneInteger)
@yorm.map_attr(stopped=common.NoneInteger)
class Timestamps(common.AttributeDictionary):

    """A dictionary of last start and stop times."""

    def __init__(self):
        self.started = None
        self.stopped = None


@yorm.map_attr(computer=yorm.standard.String)
@yorm.map_attr(timestamps=Timestamps)
class State(common.AttributeDictionary):

    """A dictionary of computer state."""

    def __init__(self, label):
        self.computer = label
        self.timestamps = Timestamps()


@yorm.map_attr(all=State)
class States(yorm.container.List):

    """A list of computer states for an application."""


@yorm.map_attr(application=yorm.standard.String)
@yorm.map_attr(computers=States)
class Status(common.AttributeDictionary):

    """A dictionary of computers using an application."""

    def __init__(self, label):
        self.application = label
        self.computers = States()


@yorm.map_attr(all=Status)
class Statuses(yorm.container.List):

    """A list of application statuses."""
