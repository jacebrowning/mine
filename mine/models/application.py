"""Data structures for application information."""

from dataclasses import dataclass
from typing import List, Optional

import log

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

    auto_queue: bool = True
    single_instance: bool = True


@dataclass
class Application(NameMixin):
    """Dictionary of application information."""

    name: str
    properties: Properties = Properties()
    versions: Versions = Versions()

    @property
    def auto_queue(self):
        return self.properties.auto_queue

    @property
    def no_wait(self):
        return not self.properties.single_instance
