"""Data structures for all settings."""

from dataclasses import dataclass, field

import log

from .application import Application
from .computer import Computer


@dataclass
class ProgramConfig:
    """Dictionary of program configuration settings."""

    computers: list[Computer] = field(default_factory=list)
    applications: list[Application] = field(default_factory=list)

    @property
    def computer_names(self):
        """Get a list of all computers' labels."""
        return [c.name for c in self.computers]

    def get_computer(self, name: str):
        """Get the computer with the given name."""
        computer = self.find_computer(name)
        assert computer, name
        return computer

    def find_computer(self, name: str):
        """Find the computer with the given name, else None."""
        log.debug("Finding computer for '%s'...", name)
        for computer in self.computers:
            if computer == name:
                return computer
        return None

    def match_computer(self, partial: str):
        """Find a computer with a similar name."""
        log.debug("Finding computer similar to '%s'...", partial)
        matches = []
        for computer in self.computers:
            if partial.lower() in computer.name.lower():
                matches.append(computer)
        if matches:
            return min(matches, key=lambda computer: len(computer.name))
        return None

    def get_current_computer(self, default_name: str = ""):
        """Get the current computer's information."""
        this = Computer("?")
        log.debug(f"Comparing information with {this!r}...")

        # Search for a matching serial
        for other in self.computers:
            if this.serial and this.serial == other.serial:
                log.debug(f"Matched via serial: {other!r}")
                other.hostname = this.hostname
                other.mine = this.mine
                return other

        # Else, search for a matching hostname
        for other in self.computers:
            if this.hostname == other.hostname:
                log.debug(f"Matched via hostname: {other!r}")
                other.address = this.address
                other.serial = other.serial or this.serial
                other.mine = this.mine
                return other

        # Else, search for a matching address
        for other in self.computers:
            if this.address == other.address:
                log.debug(f"Matched via address: {other!r}")
                other.hostname = this.hostname
                other.serial = other.serial or this.serial
                other.mine = this.mine
                return other

        # Else, this is a new computer
        this.name = default_name or self.generate_computer_name(this)
        assert this.name != "localhost"
        log.debug(f"Detected new computer: {this!r}")
        self.computers.append(this)
        return this

    def generate_computer_name(self, computer: Computer):
        """Generate a new label for a computer."""
        name = computer.hostname.lower().split(".")[0]
        copy = 1
        while name in self.computer_names:
            copy += 1
            name2 = "{}-{}".format(name, copy)
            if name2 not in self.computer_names:
                name = name2
        return name

    def get_application(self, name: str):
        """Get the application with the given name."""
        application = self.find_application(name)
        assert application, name
        return application

    def find_application(self, name: str):
        """Find the application with the given name, else None."""
        log.debug(f"Finding application for {name!r}...")
        for application in self.applications:
            if application == name:
                return application
        return None
