#!/usr/bin/env python

"""Package for mine."""

import sys

__project__ = 'mine'
__version__ = '0.0.0'

CLI = 'mine'
VERSION = __project__ + '-' + __version__
DESCRIPTION = "Manages running applications across multiple computers."

PYTHON_VERSION = 3, 3

if not sys.version_info >= PYTHON_VERSION:  # pragma: no cover (manual test)
    exit("Python {}.{}+ is required.".format(*PYTHON_VERSION))
