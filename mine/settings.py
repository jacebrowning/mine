"""Program defaults."""

import os
import logging

# Logging settings
DEFAULT_LOGGING_FORMAT = "%(message)s"
LEVELED_LOGGING_FORMAT = "%(levelname)s: %(message)s"
VERBOSE_LOGGING_FORMAT = "[%(levelname)-8s] %(message)s"
VERBOSE2_LOGGING_FORMAT = "[%(levelname)-8s] (%(name)s @%(lineno)4d) %(message)s"  # pylint: disable=C0301
QUIET_LOGGING_LEVEL = logging.WARNING
DEFAULT_LOGGING_LEVEL = logging.WARNING
VERBOSE_LOGGING_LEVEL = logging.INFO
VERBOSE2_LOGGING_LEVEL = logging.DEBUG

# Path settings
DEFAULT_PATH = os.path.expanduser(os.path.join('~', 'Drive', '.mine.yml'))
