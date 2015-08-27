"""Functions to interact with sharing services."""

import os
import re
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
CONFIG = 'mine.yml'
CONFLICT_BASE = r"{} \(.+'s conflicted copy \d+-\d+-\d+.*\).*"
CONFLICT_ANY = CONFLICT_BASE.format(".+")
CONFLICT_CONFIG = CONFLICT_BASE.format("mine")
DEPTH = 3  # number of levels to search for the settings file

log = common.logger(__name__)


def find_root(top=None):
    """Get the root of the shared directory."""
    top = top or _default_top()

    log.debug("looking for sharing service in '%s'...", top)
    for directory in os.listdir(top):
        if directory in SERVICES:
            path = os.path.join(top, directory)
            log.debug("found sharing service: %s", path)
            return path

    msg = "no sharing service found"
    if os.getenv('CI'):
        log.warning(msg)
        return top
    else:
        raise EnvironmentError(msg)


def find_config_path(top=None, root=None):
    """Get the path to the settings file."""
    log.info("looking for settings file...")
    top = top or _default_top()
    root = root or find_root(top=top)

    log.debug("looking for '%s' in '%s'...", CONFIG, root)
    for dirpath, dirnames, _, in os.walk(root):
        depth = dirpath.count(os.path.sep) - root.count(os.path.sep)
        if depth >= DEPTH:
            del dirnames[:]
            continue
        path = os.path.join(dirpath, CONFIG)
        if os.path.isfile(path) and \
                not os.path.isfile(os.path.join(path, 'setup.py')):
            log.info("found settings file: %s", path)
            return path

    raise EnvironmentError("no '{}' file found".format(CONFIG))


def _default_top():
    """Get the default search path."""
    username = getpass.getuser()
    log.debug("looking for home directory...")
    for root in ROOTS:
        dirpath = os.path.join(root, username)
        if os.path.isdir(dirpath):  # pragma: no cover - manual test
            log.debug("found home directory: %s", dirpath)
            return dirpath

    raise EnvironmentError("no home directory found for '{}'".format(username))


def delete_conflicts(root=None, config_only=False, force=False):
    """Delete all files with conflicted filenames."""
    root = root or find_root()

    log.info("%s conflicted files...", 'deleting' if force else 'displaying')
    pattern = CONFLICT_CONFIG if config_only else CONFLICT_ANY
    log.debug("pattern: %r", pattern)
    regex = re.compile(pattern)
    count = 0
    for dirname, _, filenames in os.walk(root):
        for filename in filenames:
            if regex.match(filename):
                count += 1
                path = os.path.join(dirname, filename)
                if force:
                    os.remove(path)
                print(path)

    if count and not force:
        print()
        print("run again with '--force' to delete these "
              "{} conflict(s)".format(count))
        return False
    else:
        return True
