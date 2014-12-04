"""Data structures for computer information."""

import socket
from contextlib import closing

import yorm
import ipgetter

from . import common

log = common.logger(__name__)


@yorm.map_attr(internal=common.NoneString)
@yorm.map_attr(external=common.NoneString)
class Address(common.AttributeDictionary):

    """A dictionary of IP addresses."""

    def __init__(self, external=None, internal=None):
        self.external = external or self.get_external()
        self.internal = internal or self.get_internal()

    @staticmethod
    def get_external():
        """Get this computer's external IP address."""
        return ipgetter.myip()

    @staticmethod
    def get_internal():
        """Get this computer's (first) internal IP address."""
        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]


@yorm.map_attr(label=yorm.standard.String)
@yorm.map_attr(hostname=yorm.standard.String)
@yorm.map_attr(address=Address)
class Computer(common.AttributeDictionary):

    """A dictionary of identifying computer information."""

    def __init__(self, label, hostname=None, external=None, internal=None):
        self.label = label
        self.hostname = hostname or self.get_hostname()
        self.address = Address(external=external, internal=internal)

    @staticmethod
    def get_hostname():
        """Get this computer's hostname."""
        return socket.gethostname()


@yorm.map_attr(all=Computer)
class Computers(yorm.container.List):

    """A list of computers."""
