"""Data structures for all settings."""

import log
import yorm

from .application import Applications
from .computer import Computer, Computers


@yorm.attr(computers=Computers)
@yorm.attr(applications=Applications)
class ProgramConfig(yorm.types.AttributeDictionary):
    """Dictionary of program configuration settings."""

    def __init__(self, applications=None, computers=None):
        super().__init__()
        self.applications = applications or Applications()
        self.computers = computers or Computers()

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

    def get_current_computer(self):
        """Get the current computer's information."""
        this = Computer(None)
        log.debug(f"Matching: {this.hostname=} {this.address=} {this.serial=}")

        # Search for a matching hostname
        for other in self.computers:
            if this.hostname == other.hostname:
                log.debug(f"Matched via hostname: {other}")
                other.address = this.address
                if this.serial:
                    other.serial = this.serial
                return other

        # Else, search for a matching serial
        for other in self.computers:
            if this.serial and this.serial == other.serial:
                log.debug(f"Matched via serial: {other}")
                other.hostname = this.hostname
                return other

        # Else, search for a matching address
        for other in self.computers:
            if this.address == other.address:
                log.debug(f"Matched via address: {other}")
                other.hostname = this.hostname
                if this.serial:
                    other.serial = this.serial
                return other

        # Else, this is a new computer
        this.name = self.generate_name(this)
        assert this.name != "localhost"
        log.debug("New computer: %s", this)
        self.computers.append(this)
        return this

    def generate_name(self, computer: Computer):
        """Generate a new label for a computer."""
        name = computer.hostname.lower().split(".")[0]
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
