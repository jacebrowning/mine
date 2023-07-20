"""Common exceptions, classes, and functions."""

import argparse
import logging

from . import settings

MAX_VERBOSITY = 4

verbosity = 0


class HelpFormatter(argparse.HelpFormatter):
    """Command-line help text formatter with wider help text."""

    def __init__(self, *args, **kwargs):
        kwargs["max_help_position"] = 40
        super().__init__(*args, **kwargs)


class WarningFormatter(logging.Formatter):
    """Logging formatter that displays verbose formatting for WARNING+."""

    def __init__(self, default_format, verbose_format, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_format = default_format
        self.verbose_format = verbose_format

    def format(self, record):
        """Python 3 hack to change the formatting style dynamically."""
        # pylint: disable=protected-access
        if record.levelno > logging.INFO:
            self._style._fmt = self.verbose_format
        else:
            self._style._fmt = self.default_format
        return super().format(record)


def configure_logging(count=0):
    """Configure logging using the provided verbosity count."""
    assert MAX_VERBOSITY == 4

    if count == -1:
        level = settings.QUIET_LOGGING_LEVEL
        default_format = settings.DEFAULT_LOGGING_FORMAT
        verbose_format = settings.LEVELED_LOGGING_FORMAT
    elif count == 0:
        level = settings.DEFAULT_LOGGING_LEVEL
        default_format = settings.DEFAULT_LOGGING_FORMAT
        verbose_format = settings.LEVELED_LOGGING_FORMAT
    elif count == 1:
        level = settings.VERBOSE_LOGGING_LEVEL
        default_format = settings.VERBOSE_LOGGING_FORMAT
        verbose_format = settings.VERBOSE_LOGGING_FORMAT
    elif count == 2:
        level = settings.VERBOSE2_LOGGING_LEVEL
        default_format = settings.VERBOSE_LOGGING_FORMAT
        verbose_format = settings.VERBOSE_LOGGING_FORMAT
    elif count == 3:
        level = settings.VERBOSE2_LOGGING_LEVEL
        default_format = settings.VERBOSE2_LOGGING_FORMAT
        verbose_format = settings.VERBOSE2_LOGGING_FORMAT
    else:
        level = settings.VERBOSE2_LOGGING_LEVEL - 1
        default_format = settings.VERBOSE2_LOGGING_FORMAT
        verbose_format = settings.VERBOSE2_LOGGING_FORMAT

    # Set a custom formatter
    logging.basicConfig(level=level)
    logging.captureWarnings(True)
    formatter = WarningFormatter(
        default_format, verbose_format, datefmt=settings.LOGGING_DATEFMT
    )
    logging.root.handlers[0].setFormatter(formatter)
    logging.getLogger("datafiles").setLevel(
        max(level, settings.DATAFILES_LOGGING_LEVEL)
    )

    # Warn about excessive verbosity
    global verbosity
    if count > MAX_VERBOSITY:
        msg = "Maximum verbosity level is {}".format(MAX_VERBOSITY)
        logging.warning(msg)
        verbosity = MAX_VERBOSITY
    else:
        verbosity = count
