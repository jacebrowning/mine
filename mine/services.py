"""Functions to interact with sharing services."""

import os
import getpass

from . import common

ROOTS = (
    r"C:\Users",
    r"/Users",
    r"/home",
)
SERVICES = (
    'Dropbox',
    'Dropbox (Personal)',
)
FILENAME = '.mine.yml'
DEPTH = 3  # number of levels to search for the settings file

log = common.logger(__name__)


def get_path(top=None, name=None):
    """Return the path to the settings file."""
    log.info("looking for settings file...")
    top = top or _default_top()

    log.debug("looking for sharing service in '%s'...", top)
    for directory in os.listdir(top):
        if directory in SERVICES:
            service = os.path.join(top, directory)
            log.debug("found sharing service: %s", service)
            log.debug("looking for '%s' in '%s'...", FILENAME, service)
            for dirpath, dirnames, _, in os.walk(service):
                depth = dirpath.count(os.path.sep) - service.count(os.path.sep)
                if depth >= DEPTH:
                    del dirnames[:]
                    continue
                path = os.path.join(dirpath, FILENAME)
                if os.path.isfile(path) and \
                        not os.path.isfile(os.path.join(path, 'setup.py')):
                    log.info("found settings file: %s", path)
                    return path

    raise EnvironmentError("no '{}' file found".format(FILENAME))


def _default_top():
    """Return the default search path."""
    username = getpass.getuser()
    log.debug("looking for home directory...")
    for root in ROOTS:
        dirpath = os.path.join(root, username)
        if os.path.isdir(dirpath):  # pragma: no cover - manual test
            log.debug("found home directory: %s", dirpath)
            return dirpath

    raise EnvironmentError("no home directory found for '{}'".format(username))
