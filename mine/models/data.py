"""Data structures that combine all program data."""

from dataclasses import dataclass, field

import crayons
import log

from ..manager import BaseManager
from .config import ProgramConfig
from .status import ProgramStatus


@dataclass
class Data:
    """Primary wrapper for all settings."""

    config: ProgramConfig = field(default_factory=ProgramConfig)
    status: ProgramStatus = field(default_factory=ProgramStatus)

    def __post_init__(self):
        self._last_counter = self.status.counter

    def __repr__(self):
        return "settings"

    @property
    def modified(self):
        changed = self.status.counter != self._last_counter
        self._last_counter = self.status.counter
        return changed

    @staticmethod
    def prune_status(config: ProgramConfig, status: ProgramStatus):
        """Remove undefined applications and computers."""
        log.info("Cleaning up applications and computers...")
        for appstatus in status.applications.copy():
            if not config.find_application(appstatus.application):
                status.applications.remove(appstatus)
                log.info("Removed application: %s", appstatus)
            else:
                for computerstate in appstatus.computers.copy():
                    if not config.find_computer(computerstate.computer):
                        appstatus.computers.remove(computerstate)
                        log.info("Removed computer: %s", computerstate)

    @staticmethod
    def queue_all_applications(config: ProgramConfig, status: ProgramStatus, computer):
        """Queue applications for launch."""
        log.info("Queuing applications for launch...")
        for application in config.applications:
            if application.auto_queue:
                log.debug("Queuing %s on %s...", application, computer)
                status.queue(application, computer)

    @staticmethod
    def launch_queued_applications(
        config: ProgramConfig, status: ProgramStatus, computer, manager: BaseManager
    ):
        """Launch applications that have been queued."""
        log.info("Launching queued applications...")
        for app_status in status.applications:
            if app_status.next:
                application = config.get_application(app_status.application)
                print(crayons.yellow(f"{application} is queued for {app_status.next}"))
                if app_status.next == computer:
                    latest = status.get_latest(application)
                    if latest in (computer, None) or application.no_wait:
                        if not manager.is_running(application):
                            manager.start(application)
                        app_status.next = None
                    else:
                        print(
                            crayons.yellow(
                                f"{application} is still running on {latest}"
                            )
                        )
                elif manager.is_running(application):
                    manager.stop(application)

    @staticmethod
    def close_all_applications(config: ProgramConfig, manager: BaseManager):
        """Close all applications running on this computer."""
        log.info("Closing all applications on this computer...")
        for application in config.applications:
            manager.stop(application)

    @staticmethod
    def update_status(
        config: ProgramConfig, status: ProgramStatus, computer, manager: BaseManager
    ):
        """Update each application's status."""
        log.info("Recording application status...")
        for application in config.applications:
            latest = status.get_latest(application)
            if manager.is_running(application):
                if computer != latest:
                    if status.is_running(application, computer):
                        # case 1: application just launched remotely
                        manager.stop(application)
                        status.stop(application, computer)
                        print(
                            crayons.green(f"{application} is now running on {latest}")
                        )
                        print(
                            crayons.red(f"{application} is now stopped on {computer}")
                        )
                    else:
                        # case 2: application just launched locally
                        status.start(application, computer)
                        print(
                            crayons.green(f"{application} is now running on {computer}")
                        )
                else:
                    # case 3: application already running locally
                    print(crayons.cyan(f"{application} is running on {computer}"))
            else:
                if status.is_running(application, computer):
                    # case 4: application just closed locally
                    status.stop(application, computer)
                    print(crayons.red(f"{application} is now stopped on {computer}"))
                elif latest:
                    # case 5: application already closed locally
                    print(crayons.magenta(f"{application} is running on {latest}"))
                else:
                    # case 6: application is not running
                    print(crayons.white(f"{application} is not running"))
