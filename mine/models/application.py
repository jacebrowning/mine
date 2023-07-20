"""Data structures for application information."""

from dataclasses import dataclass, field


@dataclass
class Versions:
    """Dictionary of OS-specific application filenames."""

    mac: str | None = None
    windows: str | None = None
    linux: str | None = None


@dataclass
class Properties:
    """Dictionary of application management settings."""

    auto_queue: bool = False
    single_instance: bool = False


@dataclass
class Application:
    """Dictionary of application information."""

    name: str
    properties: Properties = field(default_factory=Properties)
    versions: Versions = field(default_factory=Versions)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return str(self).lower() == str(other).lower()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return str(self).lower() < str(other).lower()

    @property
    def auto_queue(self):
        return self.properties.auto_queue

    @property
    def no_wait(self):
        return not self.properties.single_instance
