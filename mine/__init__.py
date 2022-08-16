"""Package for mine."""

from pkg_resources import get_distribution


CLI = "mine"
VERSION = "mine v{}".format(get_distribution("mine").version)
DESCRIPTION = "Share application state across computers using Dropbox."
