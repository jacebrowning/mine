"""Data structures for application information."""

from . import common
from .base import NameMixin

import yorm

log = common.logger(__name__)


@yorm.attr(mac=yorm.converters.NoneString)
@yorm.attr(windows=yorm.converters.NoneString)
@yorm.attr(linux=yorm.converters.NoneString)
class Versions(yorm.converters.AttributeDictionary):

    """A dictionary of OS-specific application filenames."""

    def __init__(self, mac=None, windows=None, linux=None):
        super().__init__()
        self.mac = mac
        self.windows = windows
        self.linux = linux


@yorm.attr(name=yorm.converters.String)
@yorm.attr(queued=yorm.converters.Boolean)
@yorm.attr(versions=Versions)
class Application(NameMixin, yorm.converters.AttributeDictionary):

    """A dictionary of application information."""

    def __init__(self, name, queued=False, filename=None):
        super().__init__()
        self.name = name
        self.queued = queued
        self.versions = Versions(mac=filename, windows=filename, linux=filename)


@yorm.attr(all=Application)
class Applications(yorm.converters.SortedList):

    """A list of monitored applications."""

    def get(self, name):
        """Get the application with the given name."""
        application = self.find(name)
        assert application, name
        return application

    def find(self, name):
        """Find the application with the given name, else None."""
        log.debug("finding application for '%s'...", name)
        for application in self:
            if application == name:
                return application
