"""Data structures for computer information."""

import os
import platform
import re
import socket
import subprocess
import uuid
from dataclasses import dataclass

from .. import __version__


@dataclass
class Computer:
    """A dictionary of identifying computer information."""

    name: str
    serial: str = ""
    address: str = ""
    hostname: str = ""
    mine: str = "v" + __version__

    def __post_init__(self):
        self.address = self.address or self.get_address()
        self.hostname = self.hostname or self.get_hostname()
        self.serial = self.serial or self.get_serial()
        assert ":" in self.address, f"Invalid address: {self.address!r}"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return str(self).lower() == str(other).lower()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return str(self).lower() < str(other).lower()

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

    @staticmethod
    def get_serial():
        if os.name == "nt":
            cmd = "vol C:"
            output = os.popen(cmd).read()
            return re.findall("Volume Serial Number is (.+)", output)[0]

        if platform.system() == "Darwin":
            args = ["/usr/sbin/ioreg", "-l"]
            try:
                output = subprocess.check_output(args).decode("utf-8", "ignore")
                serial_number_match = re.search(
                    '"IOPlatformSerialNumber" = "(.*?)"', output
                )
                if serial_number_match:
                    return serial_number_match.group(1)
            except UnicodeDecodeError:
                return None

        cmd = "/sbin/udevadm info --query=property --name=sda"
        output = os.popen(cmd).read()
        serial_numbers = re.findall("ID_SERIAL=(.+)", output)
        if serial_numbers:
            return serial_numbers[0]
        return None
