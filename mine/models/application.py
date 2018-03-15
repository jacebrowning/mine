"""Data structures for application information."""

import yorm
import log

from ._bases import NameMixin


@yorm.attr(mac=yorm.types.NullableString)
@yorm.attr(windows=yorm.types.NullableString)
@yorm.attr(linux=yorm.types.NullableString)
class Versions(yorm.types.AttributeDictionary):
    """Dictionary of OS-specific application filenames."""


@yorm.attr(auto_queue=yorm.types.Boolean)
@yorm.attr(single_instance=yorm.types.Boolean)
class Properties(yorm.types.AttributeDictionary):
    """Dictionary of application management settings."""


@yorm.attr(name=yorm.types.String)
@yorm.attr(properties=Properties)
@yorm.attr(versions=Versions)
class Application(NameMixin, yorm.types.AttributeDictionary):
    """Dictionary of application information."""

    def __init__(self, name=None, properties=None, versions=None,
                 filename=None):
        super().__init__()
        self.name = name
        self.properties = properties or Properties()
        self.versions = versions or Versions(mac=filename,
                                             windows=filename,
                                             linux=filename)

    @property
    def auto_queue(self):
        return self.properties.auto_queue

    @property
    def no_wait(self):
        return not self.properties.single_instance


@yorm.attr(all=Application)
class Applications(yorm.types.SortedList):
    """List of monitored applications."""

    def get(self, name):
        """Get the application with the given name."""
        application = self.find(name)
        assert application, name
        return application

    def find(self, name):
        """Find the application with the given name, else None."""
        log.debug("Finding application for '%s'...", name)
        for application in self:
            if application == name:
                return application
        return None
