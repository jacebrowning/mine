"""Data structures that combine all program data."""


from .config import ProgramConfig
from .status import ProgramStatus


import yorm

from . import common


log = common.logger(__name__)


@yorm.map_attr(config=ProgramConfig)
@yorm.map_attr(status=ProgramStatus)
class Data:

    """Primary wrapper for all settings."""

    def __init__(self):
        self.config = ProgramConfig()
        self.status = ProgramStatus()

    def __repr__(self):
        return "settings"
