"""Data structures for all settings."""


import yorm

from . import common
from .application import ApplicationList
from .computer import ComputerList

log = common.logger(__name__)


@yorm.map_attr(applications=ApplicationList)
@yorm.map_attr(computers=ComputerList)
class ProgramConfig(yorm.extended.AttributeDictionary):

    """A dictionary of program configuration settings."""

    def __init__(self):
        super().__init__()
        self.applications = ApplicationList()
        self.computers = ComputerList()
