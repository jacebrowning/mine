"""Data structures for all settings."""

import yorm

from .application import Applications
from .computer import Computers


@yorm.attr(computers=Computers)
@yorm.attr(applications=Applications)
class ProgramConfig(yorm.types.AttributeDictionary):
    """Dictionary of program configuration settings."""

    def __init__(self, applications=None, computers=None):
        super().__init__()
        self.applications = applications or Applications()
        self.computers = computers or Computers()
