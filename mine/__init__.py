#!/usr/bin/env python

"""Package for mine."""

import sys

__project__ = 'mine'
__version__ = '0.1.1'

CLI = 'mine'
VERSION = __project__ + '-' + __version__
DESCRIPTION = "For applications that haven't learned to share."

PYTHON_VERSION = 3, 3

if not sys.version_info >= PYTHON_VERSION:  # pragma: no cover (manual test)
    exit("Python {}.{}+ is required.".format(*PYTHON_VERSION))
