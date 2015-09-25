#!/usr/bin/env python

"""Command-line interface."""

import sys
import time
import argparse

from . import CLI, VERSION, DESCRIPTION
from . import common
from . import services
from .data import Data
from .application import Application
from .manager import get_manager

import yorm


log = common.logger(__name__)
daemon = Application(CLI, filename=CLI)


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
    parser.add_argument('-d', '--daemon', metavar='DELAY', nargs='?', const=60,
                        type=int, help="run continuously with delay [seconds]")
    parser.add_argument('-f', '--file', help="custom settings file path")
    subs = parser.add_subparsers(help="", dest='command', metavar="<command>")

    # Build switch parser
    info = "start applications on another computer"
    sub = subs.add_parser('switch', description=info.capitalize() + '.',
                          help=info, **shared)
    sub.add_argument('name', nargs='?',
                     help="computer to queue for launch (default: current)")

    # Build clean parser
    info = "display and delete conflicted files"
    sub = subs.add_parser('clean', description=info.capitalize() + '.',
                          help=info, **shared)
    sub.add_argument('-f', '--force', action='store_true',
                     help="actually delete the conflicted files")

    # Build edit parser
    info = "launch the settings file for editing"
    sub = subs.add_parser('edit', description=info.capitalize() + '.',
                          help=info, **shared)

    # Parse arguments
    args = parser.parse_args(args=args)
    kwargs = {'delay': args.daemon}
    if args.command == 'switch':
        kwargs['switch'] = args.name if args.name else True
    elif args.command == 'clean':
        kwargs['delete'] = True
        kwargs['force'] = args.force
    elif args.command == 'edit':
        kwargs['edit'] = True

    # Configure logging
    common.configure_logging(args.verbose)

    # Run the program
    try:
        log.debug("running main command...")
        success = run(path=args.file, **kwargs)
    except KeyboardInterrupt:
        msg = "command canceled"
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


def run(path=None, cleanup=True, delay=None,
        switch=None,
        edit=False,
        delete=False, force=False):
    """Run the program.

    :param path: custom settings file path
    :param cleanup: remove unused items from the config
    :param delay: number of seconds to delay before repeating

    :param switch: computer name to queue for launch

    :param edit: launch the configuration file for editing

    :param delete: attempt to delete conflicted files
    :param force: actually delete conflicted files

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
        data.clean(config, status)
    if edit:
        return manager.launch(path)
    if delete:
        return services.delete_conflicts(root, force=force)

    if switch is True:
        switch = computer
    elif switch:
        switch = config.computers.match(switch)
    if switch:
        data.queue(config, status, switch)

    while True:
        data.launch(config, status, computer, manager)
        data.update(config, status, computer, manager)

        if delay is None:
            break

        log.info("delaying for %s seconds...", delay)
        time.sleep(delay)
        services.delete_conflicts(root, config_only=True, force=True)

    if daemon and not manager.is_running(daemon):
        msg = ("daemon is not running, start it with: " + "\n" +
               "nohup %s --daemon --verbose >> /tmp/mine.log 2>&1 &")
        log.warning(msg, CLI)
        return False

    return True


if __name__ == '__main__':  # pragma: no cover (manual test)
    main()
