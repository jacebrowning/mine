"""Data structures for computer information."""

import socket
import uuid
from dataclasses import dataclass

import log

from ._bases import NameMixin


@dataclass
class Computer(NameMixin):
    """A dictionary of identifying computer information."""

    name: str
    hostname: str = ''
    address: str = ''

    def __post_init__(self):
        self.address = self.address or self.get_address()
        self.hostname = self.hostname or self.get_hostname()

    @staticmethod
    def get_address(node=None):
        """Get this computer's MAC address."""
        if node is None:
            node = uuid.getnode()
        return ':'.join(("%012X" % node)[i : i + 2] for i in range(0, 12, 2))

    @staticmethod
    def get_hostname():
        """Get this computer's hostname."""
        return socket.gethostname()
