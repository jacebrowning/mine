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


class BaseManager(metaclass=abc.ABCMeta):

    """Base application manager."""

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

    @abc.abstractclassmethod
    def stop(self, application):
        """Stop an application on the current computer."""
        raise NotImplementedError


class LinuxManager(BaseManager):

    """Application manager for Linux."""


class MacManager(BaseManager):

    """Application manager for OS X."""

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
                    return process
            except psutil.AccessDenied:
                pass  # the process is likely owned by root


class WindowsManager(BaseManager):

    """Application manager for Windows."""


def get_manager():
    """Return an application manager for the current operating system."""
    name = platform.system()
    if name == 'Windows':
        return WindowsManager()
    elif name == 'Darwin':
        return MacManager()
    else:
        assert name == 'Linux'
        return LinuxManager()
