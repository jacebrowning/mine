"""Classes to manage application state."""

import abc
import platform
import functools

from . import common

log = common.logger(__name__)

# TODO: delete this after implementing `BaseManager`
# pylint: disable=R0903


def log_running(func):
    """Decorator for methods that return application status."""
    @functools.wraps(func)
    def wrapped(self, application, *args, **kwargs):
        """Wrapped method to log if an application is running."""
        running = func(self, application, *args, **kwargs)
        log.info("%s is%s running", application, "" if running else " not")
        return running
    return wrapped


def log_stopping(func):
    """Decorator for methods that stop an application."""
    @functools.wraps(func)
    def wrapped(self, application, *args, **kwargs):
        """Wrapped method to log that an application is being stopped."""
        log.info("stopping %s...", application)
        return func(self, application, *args, **kwargs)
    return wrapped



class BaseManager(metaclass=abc.ABCMeta):

    """Base application manager."""

    @abc.abstractmethod
    def is_running(self, application):
        """Determine if an application is currently running."""
        raise NotImplementedError

# TODO: add this method when a feature calls for it
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
        return False

    @log_stopping
    def stop(self, application):
        pass


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
