import logging

import yorm

logger = logging.getLogger


class NoneString(yorm.standard.String):

    """Converter for the `str` type with `None` as default."""

    DEFAULT = None


class NoneInteger(yorm.standard.Integer):

    """Converter for the `int` type with `None` as default."""

    DEFAULT = None


class dict2(dict):

    """A `dict` with keys available as attributes."""

    def __init__(self, *args, **kwargs):
        super(dict2, self).__init__(*args, **kwargs)
        self.__dict__ = self


class AttributeDictionary(yorm.container.Dictionary):

    """Base class for an attribute dictionary of attribute converters."""

    TYPE = dict2
