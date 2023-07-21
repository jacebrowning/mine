"""Classes to manage application state."""

import abc
import functools
import glob
import os
import platform
import time

import log
import psutil


def log_running(func):
    @functools.wraps(func)
    def wrapped(self, application):
        log.debug(f"Determining if {application} is running...")
        running = func(self, application)
        if running is None:
            status = "Application is untracked"
        elif running:
            status = "Application running on this computer"
        else:
            status = "Application not running on this computer"
        log.info(f"{status}: {application}")
        return running

    return wrapped


def log_starting(func):
    @functools.wraps(func)
    def wrapped(self, application):
        log.info("Starting %s...", application)
        result = func(self, application)
        log.info("Running: %s", application)
        return result

    return wrapped


def log_stopping(func):
    @functools.wraps(func)
    def wrapped(self, application):
        log.info("Stopping %s...", application)
        result = func(self, application)
        log.info("Not running: %s", application)
        return result

    return wrapped


class Manager(metaclass=abc.ABCMeta):  # pragma: no cover (abstract)
    """Base application manager."""

    NAME = FRIENDLY = ""

    IGNORED_APPLICATION_NAMES: list[str] = []

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

    @classmethod
    def _get_process(cls, name: str):
        """Get a process whose executable path contains an app name."""
        log.debug("Searching for exe path containing '%s'...", name)

        for process in psutil.process_iter():
            if process.status() == psutil.STATUS_ZOMBIE:
                log.debug("Skipped zombie process: %s", process)
                continue

            try:
                command = " ".join(process.cmdline()).lower()
                parts = []
                for arg in process.cmdline():
                    parts.extend([p.lower() for p in arg.split(os.sep)])
            except psutil.AccessDenied:
                continue  # the process is likely owned by root

            if name.lower() not in parts:
                continue

            if process.pid == os.getpid():
                log.debug("Skipped current process: %s", command)
                continue

            log.debug("Found matching process: %s", command)
            for ignored in cls.IGNORED_APPLICATION_NAMES:
                if ignored.lower() in parts:
                    log.debug("But skipped due to ignored name")
                    break
            else:
                return process

        return None


class LinuxManager(Manager):  # pragma: no cover (manual)
    """Application manager for Linux."""

    NAME = "Linux"
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
        while True:
            process = self._get_process(name)
            if process and process.is_running():
                process.terminate()
                process.wait()
            else:
                break


class MacManager(Manager):  # pragma: no cover (manual)
    """Application manager for macOS."""

    NAME = "Darwin"
    FRIENDLY = "macOS"

    IGNORED_APPLICATION_NAMES = [
        "com.apple.mail.spotlightindexextension",
        "com.apple.notes.spotlightindexextension",
        "com.apple.podcasts.spotlightindexextension",
        "garcon.appex",
        "iTunesHelper.app",
        "mailcachedelete",
        "mailshortcutsextension",
        "musiccacheextension",
        "podcastswidget",
        "slack helper.app",
    ]

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
        path = None
        for base in (
            ".",
            "/Applications",
            "/Applications/*",
            "/System/Applications",
            "~/Applications",
        ):
            pattern = os.path.expanduser(os.path.join(base, name))
            log.debug("Glob pattern: %s", pattern)
            paths = glob.glob(pattern)
            if paths:
                path = paths[0]
                log.debug("Match: %s", path)
                break
        else:
            assert path, "Not found: {}".format(application)
        return self._start_app(path)

    @log_stopping
    def stop(self, application):
        name = application.versions.mac
        while True:
            process = self._get_process(name)
            if process and process.is_running():
                process.terminate()
                process.wait()
            else:
                break

    @staticmethod
    def _start_app(path):
        """Start an application from it's .app directory."""
        assert os.path.exists(path), path
        process = psutil.Popen(["open", path])
        time.sleep(1)
        return process


class WindowsManager(Manager):  # pragma: no cover (manual)
    """Application manager for Windows."""

    NAME = "Windows"
    FRIENDLY = NAME

    def is_running(self, application):
        pass

    def start(self, application):
        pass

    def stop(self, application):
        pass


def get_manager(name=None) -> Manager:
    """Return an application manager for the current operating system."""
    log.info("Detecting the operating system...")
    name = name or platform.system()
    manager = {  # type: ignore
        WindowsManager.NAME: WindowsManager,
        MacManager.NAME: MacManager,
        LinuxManager.NAME: LinuxManager,
    }[name]()
    log.info("Identified operating system: %s", manager)
    return manager
