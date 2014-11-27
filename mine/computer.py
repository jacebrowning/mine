"""Data structures for computer information."""
# pylint: disable=R0903

from . import common

import yorm

log = common.logger(__name__)


@yorm.map_attr(internal=common.NoneString)
@yorm.map_attr(external=common.NoneString)
class Address(common.AttributeDictionary):

    """A dictionary of IP addresses."""

    def __init__(self):
        self.internal = None
        self.external = None


@yorm.map_attr(label=yorm.standard.String)
@yorm.map_attr(hostname=yorm.standard.String)
@yorm.map_attr(address=Address)
class Computer(common.AttributeDictionary):

    """A dictionary of identifying computer information."""

    def __init__(self, label):
        self.label = label
        self.hostname = ""
        self.address = Address()


@yorm.map_attr(all=Computer)
class Computers(yorm.container.List):

    """A list of computers."""
