
import abc

import yorm

from . import common
from .application import Applications
from .computer import Computers
from .status import Statuses


@yorm.map_attr(applications=Applications)
@yorm.map_attr(computers=Computers)
class Configuration(common.AttributeDictionary):

    def __init__(self):
        self.applications = []
        self.computers = []


@yorm.map_attr(configuration=Configuration)
@yorm.map_attr(status=Statuses)
class Settings:

    def __init__(self):
        self.configuration = Configuration()
        self.status = Statuses()
