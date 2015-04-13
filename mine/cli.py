#!/usr/bin/env python

"""Command-line interface."""

import sys
import argparse

from . import CLI, VERSION, DESCRIPTION
from . import common
from . import services
from .data import Data
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
    subs = parser.add_subparsers(help="", dest='command', metavar="<command>")

    # Build switch parser
    info = "start applications on another computer"
    sub = subs.add_parser('switch', description=info.capitalize() + '.',
                          help=info, **shared)
    sub.add_argument('name', nargs='?',
                     help="computer to queue for launch (default: current)")

    # Build clean parser
    info = "clean up configuration and remove conflicted files"
    sub = subs.add_parser('clean', description=info.capitalize() + '.',
                          help=info, **shared)
    sub.add_argument('-f', '--force', action='store_true',
                     help="actually delete the conflicted files")

    # Parse arguments
    args = parser.parse_args(args=args)
    kwargs = {'switch': None}
    if args.command == 'switch':
        kwargs['switch'] = args.name if args.name else True
    elif args.command == 'clean':
        kwargs['delete'] = True
        kwargs['force'] = args.force

    # Configure logging
    common.configure_logging(args.verbose)

    # Run the program
    try:
        log.debug("running main command...")
        success = run(path=args.file, **kwargs)
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


def run(path=None, cleanup=True, delete=False, force=False, switch=None):
    """Run the program.

    :param path: custom settings file path
    :param switch: computer name to queue for launch

    """
    manager = get_manager()
    root = services.find_root()
    path = path or services.find_config_path(root=root)

    data = Data()
    yorm.sync(data, path)

    config = data.config
    status = data.status

    log.info("identifying current computer...")
    computer = config.computers.get_current()
    log.info("current computer: %s", computer)

    if cleanup:
        clean(config, status)
    if delete:
        return services.delete_conflicts(root, force=force)

    if switch is True:
        switch = computer
    elif switch:
        switch = config.computers.match(switch)
    if switch:
        queue(config, status, switch)

    launch(config, status, computer, manager)
    update(config, status, computer, manager)

    return True


# TODO: consider moving this logic to `data`
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


# TODO: consider moving this logic to `data`
def queue(config, status, computer):
    """Queue applications for launch."""
    log.info("queuing applications for launch...")
    for application in config.applications:
        if application.queued:
            log.debug("queuing %s on %s...", application, computer)
            status.queue(application, computer)
        else:
            log.debug("skipping %s (not queued)...", application)


# TODO: consider moving this logic to `data`
def launch(config, status, computer, manager):
    """Launch applications that have been queued."""
    log.info("launching queued applications...")
    for app_status in status.applications:
        if app_status.next:
            application = config.applications.get(app_status.application)
            log.info("%s queued for: %s", application, app_status.next)
            if app_status.next == computer:
                latest = status.get_latest(application)
                if latest in (computer, None):
                    if not manager.is_running(application):
                        manager.start(application)
                    app_status.next = None
                else:
                    log.info("%s still running on: %s", application, latest)
            elif manager.is_running(application):
                manager.stop(application)


# TODO: consider moving this logic to `data`
def update(config, status, computer, manager):
    """Update each application's status."""
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
