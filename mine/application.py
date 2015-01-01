"""Data structures for application information."""

from . import common

import yorm

log = common.logger(__name__)


@yorm.map_attr(mac=common.NoneString)
@yorm.map_attr(windows=common.NoneString)
@yorm.map_attr(linux=common.NoneString)
class Versions(yorm.container.Dictionary):

    """A dictionary of OS-specific application filenames."""

    def __init__(self):
        super().__init__()
        self.mac = None
        self.windows = None
        self.linux = None


@yorm.map_attr(label=yorm.standard.String)
@yorm.map_attr(versions=Versions)
class Application(yorm.container.Dictionary):

    """A dictionary of application information."""

    def __init__(self, label):
        super().__init__()
        self.label = label
        self.versions = Versions()

    def __str__(self):
        return str(self.label)


@yorm.map_attr(all=Application)
class ApplicationList(yorm.container.List):

    """A list of monitored applications."""
