"""Data structures for computer information."""

import socket
from contextlib import closing

import yorm
import ipgetter

from . import common

log = common.logger(__name__)


@yorm.map_attr(internal=common.NoneString)
@yorm.map_attr(external=common.NoneString)
class Address(yorm.container.Dictionary):

    """A dictionary of IP addresses."""

    def __init__(self, external=None, internal=None):
        super().__init__()
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
class Computer(yorm.container.Dictionary):

    """A dictionary of identifying computer information."""

    current = False

    def __init__(self, label, hostname=None, external=None, internal=None):
        super().__init__()
        self.label = label
        self.hostname = hostname or self.get_hostname()
        self.address = Address(external=external, internal=internal)

    def __str__(self):
        if self.current:
            return "this computer ({})".format(self.label)
        else:
            return str(self.label)

    @staticmethod
    def get_hostname():
        """Get this computer's hostname."""
        return socket.gethostname()


@yorm.map_attr(all=Computer)
class Computers(yorm.container.List):

    """A list of computers."""

    @property
    def labels(self):
        """Get a list of all computers' labels."""
        return [c.label for c in self]

    @property
    def hostnames(self):
        """Get a list of all computers' hostnames."""
        return [c.hostname for c in self]

    def get_current(self):
        """Get the current computer's information."""
        this = Computer(None)

        # Search for (1) any matching hostname and...
        for other in self:
            if this.hostname == other.hostname:

                # (2) a matching external AND internal addresses
                if all((this.address.external == other.address.external,
                        this.address.internal == other.address.internal)):
                    return other

                # (2) a matching external OR internal addresses
                elif any((this.address.external == other.address.external,
                          this.address.internal == other.address.internal)):
                    other.address.external = this.address.external
                    other.address.internal = this.address.internal
                    return other

                # (2) only one matching hostname
                elif self.hostnames.count(this.hostname) == 1:
                    other.address.external = this.address.external
                    other.address.internal = this.address.internal
                    return other

        # Or, search for...
        for other in self:

            # a matching external AND internal addresses
            if all((this.address.external == other.address.external,
                    this.address.internal == other.address.internal)):
                other.hostname = this.hostname
                return other

        # Or, this is a new computer
        this.label = self.generate_label(this)
        self.append(this)
        return this

    def generate_label(self, computer):
        """Generate a new label for a computer."""
        label = computer.hostname.lower().split('.')[0]
        copy = 1
        while label in self.labels:
            copy += 1
            label2 = "{}-{}".format(label, copy)
            if label2 not in self.labels:
                label = label2
        return label
