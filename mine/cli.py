#!/usr/bin/env python

"""Command-line interface."""

import sys
import argparse

from . import CLI, VERSION, DESCRIPTION
from . import common
from .data import Data
from .services import get_path
from .manager import get_manager

import yorm


log = common.logger(__name__)


def main(args=None):
    """Process command-line arguments and run the program."""
    # Shared options
    debug = argparse.ArgumentParser(add_help=False)
    debug.add_argument('-V', '--version', action='version', version=VERSION)
    group = debug.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='count', default=0,
                       help="enable verbose logging")
    group.add_argument('-q', '--quiet', action='store_const', const=-1,
                       dest='verbose', help="only display errors and prompts")
    shared = {'formatter_class': common.HelpFormatter,
              'parents': [debug]}

    # Build main parser
    parser = argparse.ArgumentParser(prog=CLI, description=DESCRIPTION,
                                     **shared)
    parser.add_argument('-f', '--file', help="custom settings file path")

    # Parse arguments
    args = parser.parse_args(args=args)

    # Configure logging
    common.configure_logging(args.verbose)

    # Run the program
    try:
        log.debug("running main command...")
        success = run(path=args.file)
    except KeyboardInterrupt:
        msg = "command cancelled"
        if common.verbosity == common.MAX_VERBOSITY:
            log.exception(msg)
        else:
            log.debug(msg)
        success = False
    if success:
        log.debug("command succeeded")
    else:
        log.debug("command failed")
        sys.exit(1)


def run(path=None):
    """Run the program."""
    manager = get_manager()
    path = path or get_path()

    # TODO: convert to `yorm.load()` when available
    data = Data()
    yorm.store(data, path)

    config = data.config
    status = data.status

    log.info("identifying current computer...")
    computer = config.computers.get_current()
    log.info("current computer: %s", computer)
    # TODO: remove this fix when YORM stops overwriting attributes: https://github.com/jacebrowning/yorm/issues/47
    data.config = config

    launch_next(config, status, computer, manager)
    update_status(config, status, computer, manager)

    # TODO: remove this fix when YORM stores on nested attributes: https://github.com/jacebrowning/yorm/issues/42
    data.yorm_mapper.store(data)  # pylint: disable=E1101

    return True


# TODO: consider moving this logic to `data`
def launch_next(config, status, computer, manager):
    """Launch applications that have been queued."""
    log.info("launching queued applications...")
    for status in status.applications:
        if status.next:
            application = config.applications.get(status.application)
            log.info("%s queued for: %s", application, status.next)
            if status.next == computer:
                if not manager.is_running(application):
                    manager.start(application)
                status.next = None
            elif manager.is_running(application):
                manager.stop(application)


# TODO: consider moving this logic to `data`
def update_status(config, status, computer, manager):
    """Update and store each application's status."""
    log.info("recording application status...")
    for application in config.applications:
        if manager.is_running(application):
            latest = status.get_latest(application)
            if computer != latest:
                if status.is_running(application, computer):
                    # case 1: application just launched remotely
                    log.info("%s launched on: %s", application, latest)
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


def show_running(application, computer):
    """Display the new state of a running application."""
    print("{} is now running on {}".format(application, computer))


def show_started(application, computer):
    """Display the new state of a started application."""
    print("{} is now started on {}".format(application, computer))


def show_stopped(application, computer):
    """Display the new state of a stopped application."""
    print("{} is now stopped on {}".format(application, computer))


if __name__ == '__main__':  # pragma: no cover (manual test)
    main()
