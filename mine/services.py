"""Functions to interact with sharing services."""

import os
import re

import log

from .models.application import Application, Versions

ROOTS = (r"C:\Users", r"/Users", r"/home")
SERVICES = ("Dropbox", "Dropbox (Personal)")
CONFIG = "mine.yml"
CONFLICT_BASE = r"{} \(.+'s conflicted copy \d+-\d+-\d+.*\).*"
CONFLICT_ANY = CONFLICT_BASE.format(".+")
CONFLICT_CONFIG = CONFLICT_BASE.format("mine")
DEPTH = 3  # number of levels to search for the settings file
APPLICATION = Application(
    "Dropbox",
    versions=Versions(mac="Dropbox.app", windows="Dropbox.exe", linux="dropbox"),
)


def find_root(top=None):
    """Get the root of the shared directory."""
    top = top or os.path.expanduser("~")

    log.debug("Looking for sharing service in '%s'...", top)
    for directory in os.listdir(top):
        if directory in SERVICES:
            path = os.path.join(top, directory)
            log.debug("Found sharing service: %s", path)
            return path

    msg = "No sharing service found"
    if os.getenv("CI"):
        log.warning(msg)
        return top

    raise EnvironmentError(msg)


def find_config_path(top=None, root=None):
    """Get the path to the settings file."""
    log.info("Looking for settings file...")
    top = top or os.path.expanduser("~")
    root = root or find_root(top=top)

    log.debug("Looking for '%s' in '%s'...", CONFIG, root)
    for dirpath, dirnames, _ in os.walk(root):
        depth = dirpath.count(os.path.sep) - root.count(os.path.sep)
        if depth >= DEPTH:
            del dirnames[:]
            continue
        path = os.path.join(dirpath, CONFIG)
        if os.path.isfile(path) and not os.path.isfile(os.path.join(path, "setup.py")):
            log.info("Found settings file: %s", path)
            return path

    raise EnvironmentError("No '{}' file found".format(CONFIG))


def delete_conflicts(root=None, config_only=False, force=False) -> int:
    """Delete all files with conflicted filenames."""
    root = root or find_root()

    log.info("%s conflicted files...", "Deleting" if force else "Displaying")
    pattern = CONFLICT_CONFIG if config_only else CONFLICT_ANY
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
        print(f"\nRun again with '--force' to delete these {count} conflict(s)")
        return 0

    return count
