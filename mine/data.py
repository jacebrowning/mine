"""Data structures that combine all program data."""

import yorm

from . import common
from .config import ProgramConfig
from .status import ProgramStatus


log = common.logger(__name__)


@yorm.attr(config=ProgramConfig)
@yorm.attr(status=ProgramStatus)
class Data:

    """Primary wrapper for all settings."""

    def __init__(self):
        self.config = ProgramConfig()
        self.status = ProgramStatus()

    def __repr__(self):
        return "settings"

    @staticmethod
    def clean(config, status):
        """Remove undefined applications and computers."""
        log.info("cleaning up applications and computers...")
        for appstatus in status.applications.copy():
            if not config.applications.find(appstatus.application):
                status.applications.remove(appstatus)
                log.info("removed application: %s", appstatus)
            else:
                for computerstate in appstatus.computers.copy():
                    if not config.computers.find(computerstate.computer):
                        appstatus.computers.remove(computerstate)
                        log.info("removed computer: %s", computerstate)

    @staticmethod
    def queue(config, status, computer):
        """Queue applications for launch."""
        log.info("queuing applications for launch...")
        for application in config.applications:
            if application.queued:
                log.debug("queuing %s on %s...", application, computer)
                status.queue(application, computer)
            else:
                log.debug("skipping %s (not queued)...", application)

    @staticmethod
    def launch(config, status, computer, manager):
        """Launch applications that have been queued."""
        log.info("launching queued applications...")
        for app_status in status.applications:
            if app_status.next:
                application = config.applications.get(app_status.application)
                show_queued(application, app_status.next)
                if app_status.next == computer:
                    latest = status.get_latest(application)
                    if latest in (computer, None):
                        if not manager.is_running(application):
                            manager.start(application)
                        app_status.next = None
                    else:
                        show_waiting(application, latest)
                elif manager.is_running(application):
                    manager.stop(application)

    @staticmethod
    def update(config, status, computer, manager):
        """Update each application's status."""
        log.info("recording application status...")
        for application in config.applications:
            if manager.is_running(application):
                latest = status.get_latest(application)
                if computer != latest:
                    if status.is_running(application, computer):
                        # case 1: application just launched remotely
                        manager.stop(application)
                        status.stop(application, computer)
                        show_running(application, latest)
                        show_stopped(application, computer)
                    else:
                        # case 2: application just launched locally
                        status.start(application, computer)
                        show_running(application, computer)
                else:
                    # case 3: application already running locally
                    pass
            else:
                if status.is_running(application, computer):
                    # case 4: application just closed locally
                    status.stop(application, computer)
                    show_stopped(application, computer)
                else:
                    # case 5: application already closed locally
                    pass


def show_queued(application, computer):
    """Display the state of a queued application."""
    print("{} is queued for {}".format(application, computer))


def show_waiting(application, computer):
    """Display the old state of a running application."""
    print("{} is still running on {}".format(application, computer))


def show_running(application, computer):
    """Display the new state of a running application."""
    print("{} is now running on {}".format(application, computer))


def show_started(application, computer):
    """Display the new state of a started application."""
    print("{} is now started on {}".format(application, computer))


def show_stopped(application, computer):
    """Display the new state of a stopped application."""
    print("{} is now stopped on {}".format(application, computer))
