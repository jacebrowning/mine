"""Package for mine."""

import sys

__project__ = 'mine'
__version__ = '0.5'

CLI = 'mine'
VERSION = "{0} v{1}".format(__project__, __version__)
DESCRIPTION = "Share application state across computers using Dropbox."

PYTHON_VERSION = 3, 3

if sys.version_info < PYTHON_VERSION:  # pragma: no cover (manual test)
    exit("Python {}.{}+ is required.".format(*PYTHON_VERSION))
