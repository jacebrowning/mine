"""Data structures for computer information."""

import socket
import uuid

import log
import yorm

from ._bases import NameMixin


@yorm.attr(name=yorm.types.String)
@yorm.attr(hostname=yorm.types.String)
@yorm.attr(address=yorm.types.String)
class Computer(NameMixin, yorm.types.AttributeDictionary):
    """A dictionary of identifying computer information."""

    def __init__(self, name=None, hostname=None, address=None):
        super().__init__()
        self.name = name
        self.address = address or self.get_address()
        self.hostname = hostname or self.get_hostname()

    @staticmethod
    def get_address(node=None):
        """Get this computer's MAC address."""
        if node is None:
            node = uuid.getnode()
        return ":".join(("%012X" % node)[i : i + 2] for i in range(0, 12, 2))

    @staticmethod
    def get_hostname():
        """Get this computer's hostname."""
        return socket.gethostname()


@yorm.attr(all=Computer)
class Computers(yorm.types.SortedList):
    """A list of computers."""

    @property
    def names(self):
        """Get a list of all computers' labels."""
        return [c.name for c in self]

    def get(self, name):
        """Get the computer with the given name."""
        computer = self.find(name)
        assert computer, name
        return computer

    def find(self, name):
        """Find the computer with the given name, else None."""
        log.debug("Finding computer for '%s'...", name)
        for computer in self:
            if computer == name:
                return computer
        return None

    def match(self, partial):
        """Find a computer with a similar name."""
        log.debug("Finding computer similar to '%s'...", partial)
        for computer in self:
            if partial.lower() in computer.name.lower():
                return computer
        return None

    def get_current(self):
        """Get the current computer's information."""
        this = Computer(None)

        # Search for a matching address
        for other in self:
            if this.address == other.address:
                other.hostname = this.hostname
                return other

        # Else, search for a matching hostname
        for other in self:
            if this.hostname == other.hostname:
                other.address = this.address
                return other

        # Else, this is a new computer
        this.name = self.generate_name(this)
        assert this.name != "localhost"
        log.debug("New computer: %s", this)
        self.append(this)
        return this

    def generate_name(self, computer):
        """Generate a new label for a computer."""
        name = computer.hostname.lower().split(".")[0]
        copy = 1
        while name in self.names:
            copy += 1
            name2 = "{}-{}".format(name, copy)
            if name2 not in self.names:
                name = name2
        return name
