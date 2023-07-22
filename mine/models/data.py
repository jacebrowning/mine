"""Data structures that combine all program data."""


import crayons
import log
from datafiles import datafile, field

from ..manager import Manager
from .computer import Computer
from .config import ProgramConfig
from .status import ProgramStatus


@datafile("{self.path}", defaults=True)
class Data:
    """Primary wrapper for all settings."""

    path: str
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

    def prune_status(self, *, reset_counter=False):
        """Remove undefined applications and computers."""
        log.info("Cleaning up applications and computers...")
        for status in self.status.applications.copy():
            if not self.config.find_application(status.application):
                self.status.applications.remove(status)
                log.info("Removed application: %s", status)
            else:
                for state in status.computers.copy():
                    if not self.config.find_computer(state.computer):
                        status.computers.remove(state)
                        log.info("Removed computer: %s", state)
        if reset_counter:
            self.status.counter = 0
            for status in self.status.applications:
                for computer in status.computers:
                    computer.timestamp.started = 0
                    computer.timestamp.stopped = 0

    def queue_all_applications(self, computer: Computer):
        """Queue applications for launch."""
        log.info("Queuing applications for launch...")
        for application in self.config.applications:
            if application.auto_queue:
                log.debug("Queuing %s on %s...", application, computer)
                self.status.queue(application, computer)

    def launch_queued_applications(self, computer: Computer, manager: Manager):
        """Launch applications that have been queued."""
        log.info("Launching queued applications...")
        for status in self.status.applications:
            if status.next:
                application = self.config.get_application(status.application)
                print(crayons.yellow(f"{application} is queued for {status.next}"))
                if status.next == computer:
                    latest = self.status.get_latest(application)
                    if latest in (computer, None) or application.no_wait:
                        if not manager.is_running(application):
                            manager.start(application)
                        status.next = None
                    else:
                        print(
                            crayons.yellow(
                                f"{application} is still running on {latest}"
                            )
                        )
                elif manager.is_running(application):
                    manager.stop(application)

    def close_all_applications(self, manager: Manager):
        """Close all applications running on this computer."""
        log.info("Closing all applications on this computer...")
        for application in self.config.applications:
            manager.stop(application)

    def update_status(self, computer: Computer, manager: Manager):
        """Update each application's status."""
        log.info("Recording application status...")
        for application in self.config.applications:
            latest = self.status.get_latest(application)
            if manager.is_running(application):
                if computer != latest:
                    if self.status.is_running(application, computer):
                        # case 1: application just launched remotely
                        manager.stop(application)
                        self.status.stop(application, computer)
                        print(
                            crayons.green(f"{application} is now running on {latest}")
                        )
                        print(
                            crayons.red(f"{application} is now stopped on {computer}")
                        )
                    else:
                        # case 2: application just launched locally
                        self.status.start(application, computer)
                        print(
                            crayons.green(f"{application} is now running on {computer}")
                        )
                else:
                    # case 3: application already running locally
                    print(crayons.cyan(f"{application} is running on {computer}"))
            else:
                if self.status.is_running(application, computer):
                    # case 4: application just closed locally
                    self.status.stop(application, computer)
                    print(crayons.red(f"{application} is now stopped on {computer}"))
                elif latest:
                    # case 5: application already closed locally
                    print(crayons.magenta(f"{application} is running on {latest}"))
                else:
                    # case 6: application is not running
                    print(crayons.white(f"{application} is not running"))
