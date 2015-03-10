"""Data structures for application information."""

from . import common

import yorm

log = common.logger(__name__)


@yorm.attr(mac=yorm.extended.NoneString)
@yorm.attr(windows=yorm.extended.NoneString)
@yorm.attr(linux=yorm.extended.NoneString)
class Versions(yorm.extended.AttributeDictionary):

    """A dictionary of OS-specific application filenames."""

    def __init__(self):
        super().__init__()
        self.mac = None
        self.windows = None
        self.linux = None


@yorm.attr(name=yorm.standard.String)
@yorm.attr(queued=yorm.standard.Boolean)
@yorm.attr(versions=Versions)
class Application(yorm.extended.AttributeDictionary):

    """A dictionary of application information."""

    def __init__(self, name, queued=False):
        super().__init__()
        self.name = name
        self.queued = queued
        self.versions = Versions()

    def __str__(self):
        return str(self.name)

    def __eq__(self, other):
        return str(self).lower() == str(other).lower()

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return str(self).lower() < str(other).lower()


@yorm.attr(all=Application)
class Applications(yorm.extended.SortedList):

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
