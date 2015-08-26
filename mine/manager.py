"""Classes to manage application state."""

import os
import abc
import time
import glob
import platform
import functools
import subprocess

import psutil

from . import common

log = common.logger(__name__)

# TODO: delete this after implementing `BaseManager`
# https://github.com/jacebrowning/mine/issues/8
# https://github.com/jacebrowning/mine/issues/9
# pylint: disable=R0903,W0223,E0110


# TODO: enable coverage when a Linux test is implemented
def log_running(func):  # pragma: no cover (manual)
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


# TODO: enable coverage when a Linux test is implemented
def log_starting(func):  # pragma: no cover (manual)
    """Decorator for methods that start an application."""
    @functools.wraps(func)
    def wrapped(self, application):
        """Wrapped method to log that an application is being started."""
        log.info("starting %s...", application)
        result = func(self, application)
        log.info("running: %s", application)
        return result
    return wrapped


# TODO: enable coverage when a Linux test is implemented
def log_stopping(func):  # pragma: no cover (manual)
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

    @abc.abstractmethod
    def start(self, application):
        """Start an application on the current computer."""
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self, application):
        """Stop an application on the current computer."""
        raise NotImplementedError

    @abc.abstractmethod
    def launch(self, path):
        """Open a file for editing."""
        raise NotImplementedError

    @staticmethod
    def _get_process(name):
        """Get a process whose executable path contains an app name."""
        log.debug("searching for exe path containing '%s'...", name)

        for process in psutil.process_iter():
            try:
                command = ' '.join(process.cmdline()).lower()
                parts = []
                for arg in process.cmdline():
                    parts.extend([p.lower() for p in arg.split(os.sep)])

                if name.lower() in parts:
                    if process.pid == os.getpid():
                        log.debug("skipped current process: %s", command)
                    elif process.status() == psutil.STATUS_ZOMBIE:
                        log.debug("skipped zombie process: %s", command)
                    else:
                        log.debug("found matching process: %s", command)
                        return process

            except psutil.AccessDenied:
                pass  # the process is likely owned by root

        return None


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

    def start(self, application):
        pass

    def stop(self, application):
        name = application.versions.linux
        process = self._get_process(name)
        if process.is_running():
            process.terminate()

    def launch(self, path):
        log.info("opening %s...", path)
        return subprocess.call(['xdg-open', path]) == 0


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

    @log_starting
    def start(self, application):
        name = application.versions.mac
        if os.path.exists(name):
            path = name
        else:
            path = os.path.join('/Applications', name)
            if not os.path.exists(path):
                pattern = os.path.join("/Applications/*", name)
                log.debug("glob pattern: %s", pattern)
                paths = glob.glob(pattern)
                for path in paths:
                    log.debug("match: %s", path)
                assert paths, "not found: {}".format(application)
                path = paths[0]
        self._start_app(path)

    @log_stopping
    def stop(self, application):
        name = application.versions.mac
        process = self._get_process(name)
        if process and process.is_running():
            process.terminate()
            time.sleep(0.1)

    @staticmethod
    def _start_app(path):
        """Start an application from it's .app directory."""
        assert os.path.exists(path), path
        process = psutil.Popen(['open', path])
        time.sleep(0.1)
        return process

    def launch(self, path):
        log.info("opening %s...", path)
        return subprocess.call(['open', path]) == 0


class WindowsManager(BaseManager):  # pragma: no cover (manual)

    """Application manager for Windows."""

    NAME = 'Windows'
    FRIENDLY = NAME

    def is_running(self, application):
        pass

    def start(self, application):
        pass

    def stop(self, application):
        pass

    def launch(self, path):
        log.info("starting %s...", path)
        os.startfile(path)  # pylint: disable=no-member
        return True


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
