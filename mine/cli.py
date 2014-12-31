#!/usr/bin/env python

"""Command-line interface."""

import sys
import argparse

from . import CLI, VERSION, DESCRIPTION
from . import common
from .settings import DEFAULT_PATH
from .config import Settings  # TODO: consider renaming to data.Data
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

    # Parse arguments
    args = parser.parse_args(args=args)

    # Configure logging
    common.configure_logging(args.verbose)

    # Run the program
    try:
        success = run()
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


def run(path=DEFAULT_PATH):  # pragma: no cover (not implemented)
    """Run the program."""
    manager = get_manager()

    # TODO: convert to `yorm.load()` when available
    settings = Settings()
    yorm.store(settings, path)

    configuration = settings.configuration
    status = settings.status

    log.info("identifying current computer...")
    computer = configuration.computers.get_current()
    log.info("current computer: %s", computer)
    # TODO: remove this line when fixed: https://github.com/jacebrowning/yorm/issues/47
    settings.configuration = configuration

    # TODO: add print() for status and replace pass
    for application in configuration.applications:
        if manager.is_running(application):
            latest = status.get_latest(application)
            if latest:
                if computer != latest:
                    if status.is_running(application, computer):
                        log.info("%s launched on: %s", application, latest)
                        manager.stop(application)
                        status.stop(application, computer)
                        show_running(application, latest)
                        show_stopped(application, computer)
                    else:
                        status.start(application, computer)
                        show_running(application, computer)
                else:
                    pass
            else:
                status.start(application, computer)
                show_running(application, computer)
        else:
            if status.is_running(application, computer):
                status.stop(application, computer)
                show_stopped(application, computer)
            else:
                pass

    # TODO: remove this line when YORM stores on nested attributes
    settings.yorm_mapper.store(settings)  # pylint: disable=E1101

    return True


def show_running(application, computer):
    """Display the new state of a running application."""
    print("{} is now running on {}".format(application, computer))


def show_stopped(application, computer):
    """Display the new state of a stopped application."""
    print("{} is now stopped on {}".format(application, computer))


if __name__ == '__main__':  # pragma: no cover (manual test)
    main()
