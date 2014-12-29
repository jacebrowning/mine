"""Classes to manage application state."""

import abc
import platform

# TODO: delete this after implementing `BaseManager`
# pylint: disable=R0903


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

    def is_running(self, application):
        return False

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
