"""Data structures for computer information."""

import os
import platform
import re
import socket
import subprocess
import uuid

import yorm

from ._bases import NameMixin


@yorm.attr(name=yorm.types.String)
@yorm.attr(hostname=yorm.types.String)
@yorm.attr(address=yorm.types.String)
@yorm.attr(serial=yorm.types.String)
class Computer(NameMixin, yorm.types.AttributeDictionary):
    """A dictionary of identifying computer information."""

    def __init__(self, name=None, hostname=None, address=None, serial=None):
        super().__init__()
        self.name = name
        self.address = address or self.get_address()
        self.hostname = hostname or self.get_hostname()
        self.serial = serial or self.get_serial()

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


@yorm.attr(all=Computer)
class Computers(yorm.types.SortedList):
    """A list of computers."""
