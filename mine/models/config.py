"""Data structures for all settings."""


from dataclasses import dataclass, field
from typing import List

import log

from .application import Application
from .computer import Computer


@dataclass
class ProgramConfig:
    """Dictionary of program configuration settings."""

    computers: List[Computer] = field(default_factory=list)
    applications: List[Application] = field(default_factory=list)

    @property
    def computer_names(self):
        """Get a list of all computers' labels."""
        return [c.name for c in self.computers]

    def get_computer(self, name):
        """Get the computer with the given name."""
        computer = self.find_computer(name)
        assert computer, name
        return computer

    def find_computer(self, name):
        """Find the computer with the given name, else None."""
        log.debug("Finding computer for '%s'...", name)
        for computer in self.computers:
            if computer == name:
                return computer
        return None

    def match_computer(self, partial):
        """Find a computer with a similar name."""
        log.debug("Finding computer similar to '%s'...", partial)
        for computer in self.computers:
            if partial.lower() in computer.name.lower():
                return computer
        return None

    def get_current_computer(self):
        """Get the current computer's information."""
        this = Computer(None)

        # Search for a matching address
        for other in self.computers:
            if this.address == other.address:
                other.hostname = this.hostname
                return other

        # Else, search for a matching hostname
        for other in self.computers:
            if this.hostname == other.hostname:
                other.address = this.address
                return other

        # Else, this is a new computer
        this.name = self.generate_computer_name(this)
        assert this.name != 'localhost'
        log.debug("New computer: %s", this)
        self.computers.append(this)
        return this

    def generate_computer_name(self, computer):
        """Generate a new label for a computer."""
        name = computer.hostname.lower().split('.')[0]
        copy = 1
        while name in self.computer_names:
            copy += 1
            name2 = "{}-{}".format(name, copy)
            if name2 not in self.computer_names:
                name = name2
        return name

    def get_application(self, name):
        """Get the application with the given name."""
        application = self.find_application(name)
        assert application, name
        return application

    def find_application(self, name):
        """Find the application with the given name, else None."""
        log.debug("Finding application for '%s'...", name)
        for application in self.applications:
            if application == name:
                return application
        return None
