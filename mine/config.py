"""Data structures for all settings."""

import logging

import yorm

from .application import Applications
from .computer import Computers


log = logging.getLogger(__name__)


@yorm.attr(applications=Applications)
@yorm.attr(computers=Computers)
class ProgramConfig(yorm.converters.AttributeDictionary):
    """Dictionary of program configuration settings."""

    def __init__(self):
        super().__init__()
        self.applications = Applications()
        self.computers = Computers()
