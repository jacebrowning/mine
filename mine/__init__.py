"""Package for mine."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("mine")
except PackageNotFoundError:
    __version__ = "(local)"

del PackageNotFoundError
del version

CLI = "mine"
VERSION = f"mine v{__version__}"
DESCRIPTION = "Share application state across computers using Dropbox."
