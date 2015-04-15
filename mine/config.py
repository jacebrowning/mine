"""Data structures for all settings."""

import yorm

from . import common
from .application import Applications
from .computer import Computers

log = common.logger(__name__)


@yorm.attr(applications=Applications)
@yorm.attr(computers=Computers)
class ProgramConfig(yorm.converters.AttributeDictionary):

    """A dictionary of program configuration settings."""

    def __init__(self):
        super().__init__()
        self.applications = Applications()
        self.computers = Computers()
