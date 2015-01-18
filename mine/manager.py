"""Classes to manage application state."""

import os
import abc
import platform
import functools

import psutil

from . import common

log = common.logger(__name__)

# TODO: delete this after implementing `BaseManager`
# https://github.com/jacebrowning/mine/issues/8
# https://github.com/jacebrowning/mine/issues/9
# pylint: disable=R0903,W0223,E0110


def log_running(func):
    """Decorator for methods that return application status."""
    @functools.wraps(func)
    def wrapped(self, application):
        """Wrapped method to log if an application is running."""
        log.debug("determining if %s is running...", application)
        running = func(self, application)
        if running is None:
            status = "untracked"
        elif running:
            status = "running"
        else:
            status = "not running"
        log.info("%s: %s", status, application)
        return running
    return wrapped


def log_stopping(func):
    """Decorator for methods that stop an application."""
    @functools.wraps(func)
    def wrapped(self, application):
        """Wrapped method to log that an application is being stopped."""
        log.info("stopping %s...", application)
        result = func(self, application)
        log.info("not running: %s", application)
        return result
    return wrapped


class BaseManager(metaclass=abc.ABCMeta):  # pragma: no cover (abstract)

    """Base application manager."""

    NAME = FRIENDLY = None

    def __str__(self):
        return self.FRIENDLY

    @abc.abstractmethod
    def is_running(self, application):
        """Determine if an application is currently running."""
        raise NotImplementedError

# TODO: add this method when a feature calls for it
# https://github.com/jacebrowning/mine/issues/5
#     @abc.abstractclassmethod
#     def start(self, application):
#         """Start an application on the current computer."""
#         raise NotImplementedError

    @abc.abstractmethod
    def stop(self, application):
        """Stop an application on the current computer."""
        raise NotImplementedError


class LinuxManager(BaseManager):  # pragma: no cover (manual)

    """Application manager for Linux."""

    NAME = 'Linux'
    FRIENDLY = NAME

    def is_running(self, application):
        name = application.versions.linux
        if not name:
            return None
        process = self._get_process(name)
        return process is not None

    def stop(self, application):
        name = application.versions.linux
        process = self._get_process(name)
        if process.is_running():
            process.terminate()

    @staticmethod
    def _get_process(name):
        """Get a process whose name matches."""
        for process in psutil.process_iter():
            try:
                if name == process.name():
                    path = process.exe()
                    if process.status() == psutil.STATUS_ZOMBIE:
                        log.debug("skipped zombie process: %s", path)
                    else:
                        log.debug("found matching process: %s", path)
                        return process
            except psutil.AccessDenied:
                pass  # the process is likely owned by root


class MacManager(BaseManager):  # pragma: no cover (manual)

    """Application manager for OS X."""

    NAME = 'Darwin'
    FRIENDLY = 'Mac'

    @log_running
    def is_running(self, application):
        name = application.versions.mac
        if not name:
            return None
        process = self._get_process(name)
        return process is not None

    @log_stopping
    def stop(self, application):
        name = application.versions.mac
        process = self._get_process(name)
        if process.is_running():
            process.terminate()

    @staticmethod
    def _get_process(name):
        """Get a process whose executable path contains an app name."""
        for process in psutil.process_iter():
            try:
                path = process.exe()
                if name in path.split(os.sep):
                    if process.status() == psutil.STATUS_ZOMBIE:
                        log.debug("skipped zombie process: %s", path)
                    else:
                        log.debug("found matching process: %s", path)
                        return process
            except psutil.AccessDenied:
                pass  # the process is likely owned by root


class WindowsManager(BaseManager):  # pragma: no cover (manual)

    """Application manager for Windows."""

    NAME = 'Windows'
    FRIENDLY = NAME

    def is_running(self, application):
        pass

    def stop(self, application):
        pass


def get_manager(name=None):
    """Return an application manager for the current operating system."""
    log.info("detecting the current system...")
    name = name or platform.system()
    if name == WindowsManager.NAME:
        manager = WindowsManager()
    elif name == MacManager.NAME:
        manager = MacManager()
    else:
        assert name == LinuxManager.NAME
        manager = LinuxManager()

    log.info("current system: %s", manager)
    return manager
