"""Data structures for all settings."""

import yorm

from . import common
from .application import Applications
from .computer import Computers
from .status import Statuses


@yorm.map_attr(applications=Applications)
@yorm.map_attr(computers=Computers)
class ProgramConfiguration(common.AttributeDictionary):

    """A dictionary of configuration settings."""

    def __init__(self):
        self.applications = Applications()
        self.computers = Computers()


@yorm.map_attr(applications=Statuses)
@yorm.map_attr(counter=yorm.standard.Integer)
class ProgramStatus(common.AttributeDictionary):

    """A dictionary of configuration settings."""

    def __init__(self):
        self.applications = Applications()
        self.counter = 0


@yorm.map_attr(configuration=ProgramConfiguration)
@yorm.map_attr(status=ProgramStatus)
class Settings:

    """Primary wrapper for all settings."""

    def __init__(self):
        self.configuration = ProgramConfiguration()
        self.status = ProgramStatus()
