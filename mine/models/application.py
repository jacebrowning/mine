"""Data structures for application information."""

from dataclasses import dataclass, field
from typing import Optional

from ._bases import NameMixin


@dataclass
class Versions:
    """Dictionary of OS-specific application filenames."""

    mac: Optional[str] = None
    windows: Optional[str] = None
    linux: Optional[str] = None


@dataclass
class Properties:
    """Dictionary of application management settings."""

    auto_queue: bool = False
    single_instance: bool = False


@dataclass
class Application(NameMixin):
    """Dictionary of application information."""

    name: str
    properties: Properties = field(default_factory=Properties)
    versions: Versions = field(default_factory=Versions)

    @property
    def auto_queue(self):
        return self.properties.auto_queue

    @property
    def no_wait(self):
        return not self.properties.single_instance
