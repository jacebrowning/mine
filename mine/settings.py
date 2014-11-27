"""Data structures for all settings."""
# pylint: disable=R0903

import yorm

from . import common
from .application import Applications
from .computer import Computers
from .status import Statuses


@yorm.map_attr(applications=Applications)
@yorm.map_attr(computers=Computers)
class Configuration(common.AttributeDictionary):

    """A dictionary of configuration settings."""

    def __init__(self):
        self.applications = Applications()
        self.computers = Computers()


@yorm.map_attr(configuration=Configuration)
@yorm.map_attr(status=Statuses)
class Settings:

    """Primary wrapper for all settings."""

    def __init__(self):
        self.configuration = Configuration()
        self.status = Statuses()
