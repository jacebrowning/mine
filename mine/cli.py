#!/usr/bin/env python

"""Command-line interface."""

import argparse
import sys
import time

import datafiles
import log
from startfile import startfile

from . import CLI, DESCRIPTION, VERSION, common, daemon, services
from .manager import get_manager
from .models import Data


def main(args=None):
    """Process command-line arguments and run the program."""

    # Shared options
    debug = argparse.ArgumentParser(add_help=False)
    debug.add_argument("-V", "--version", action="version", version=VERSION)
    group = debug.add_mutually_exclusive_group()
    group.add_argument(
        "-v", "--verbose", action="count", default=0, help="enable verbose logging"
    )
    group.add_argument(
        "-q",
        "--quiet",
        action="store_const",
        const=-1,
        dest="verbose",
        help="only display errors and prompts",
    )

    # Build main parser
    parser = argparse.ArgumentParser(
        prog=CLI,
        description=DESCRIPTION,
        formatter_class=common.HelpFormatter,
        parents=[debug],
    )
    parser.add_argument(
        "-d",
        "--daemon",
        metavar="DELAY",
        nargs="?",
        const=300,
        type=int,
        help="run continuously with delay [seconds]",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="custom settings file path",
    )
    subs = parser.add_subparsers(help="", dest="command", metavar="<command>")

    # Build switch parser
    info = "start applications on another computer"
    sub = subs.add_parser(
        "switch",
        description=info.capitalize() + ".",
        help=info,
        formatter_class=common.HelpFormatter,
        parents=[debug],
    )
    sub.add_argument(
        "name",
        nargs="?",
        help="computer to queue for launch (default: current)",
    )

    # Build close parser
    info = "close applications on this computer"
    sub = subs.add_parser(
        "close",
        description=info.capitalize() + ".",
        help=info,
        formatter_class=common.HelpFormatter,
        parents=[debug],
    )

    # Build edit parser
    info = "launch the settings file for editing"
    sub = subs.add_parser(
        "edit",
        description=info.capitalize() + ".",
        help=info,
        formatter_class=common.HelpFormatter,
        parents=[debug],
    )

    # Build clean parser
    info = "display and delete conflicted files"
    sub = subs.add_parser(
        "clean",
        description=info.capitalize() + ".",
        help=info,
        formatter_class=common.HelpFormatter,
        parents=[debug],
    )
    sub.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="actually delete the conflicted files",
    )
    sub.add_argument(
        "-r",
        "--reset",
        action="store_true",
        help="reset the internal status counter",
    )
    sub.add_argument(
        "-s",
        "--stop",
        action="store_true",
        help="stop the background daemon process",
    )

    # Parse arguments
    args = parser.parse_args(args=args)
    kwargs = {"delay": args.daemon}
    if args.command == "switch":
        kwargs["switch"] = args.name if args.name else True
    elif args.command == "close":
        kwargs["switch"] = False
    elif args.command == "edit":
        kwargs["edit"] = True
    elif args.command == "clean":
        kwargs["delete"] = True
        kwargs["force"] = args.force
        kwargs["reset"] = args.reset
        kwargs["stop"] = args.stop

    # Configure logging
    common.configure_logging(args.verbose)

    # Run the program
    try:
        log.debug("Running main command...")
        success = run(path=args.file, **kwargs)
    except KeyboardInterrupt:
        msg = "command canceled"
        if common.verbosity == common.MAX_VERBOSITY:
            log.exception(msg)
        else:
            log.debug(msg)
        success = False
    if success:
        log.debug("Command succeeded")
    else:
        log.debug("Command failed")
        sys.exit(1)


def run(
    path=None,
    cleanup=True,
    delay=None,
    switch=None,
    edit=False,
    delete=False,
    force=False,
    reset=False,
    stop=False,
):
    """Run the program.

    :param path: custom settings file path
    :param cleanup: remove unused items from the config
    :param delay: number of seconds to delay before repeating

    :param switch: computer name to queue for launch

    :param edit: launch the configuration file for editing

    :param delete: attempt to delete conflicted files
    :param force: actually delete conflicted files
    :param reset: reset the internal status counter
    :param stop: stop the background daemon process

    """
    manager = get_manager()
    if not manager.is_running(services.APPLICATION):
        manager.start(services.APPLICATION)

    root = services.find_root()
    path = path or services.find_config_path(root=root)
    data = Data(path)

    log.info("Identifying current computer...")
    with datafiles.frozen(data):
        computer = data.config.get_current_computer()
    log.info("Current computer: %s", computer)

    if stop:
        daemon.stop(manager)
    if reset:
        with datafiles.frozen(data):
            data.prune_status(reset_counter=True)
    if edit:
        return startfile(path)
    if delete:
        return services.delete_conflicts(root, force=force)

    if switch is True:
        switch = computer
    elif switch is False:
        data.close_all_applications(manager)
    elif switch:
        switch = data.config.match_computer(switch)

    if switch:
        if switch != computer:
            data.close_all_applications(manager)
        data.queue_all_applications(switch)

    while True:
        if services.delete_conflicts(root, config_only=True, force=True):
            log.info("Delaying 10 seconds for changes to delete...")
            time.sleep(10)
        with datafiles.frozen(data):
            data.launch_queued_applications(computer, manager)
            data.update_status(computer, manager)

        if delay is None or delay <= 0:
            break

        if data.modified:
            log.info("Delaying 10 seconds for changes to upload...")
            time.sleep(10)

        elapsed = 0
        log.info(f"Waiting up to {delay} seconds for changes...")
        while elapsed < delay:
            time.sleep(5)
            elapsed += 5
            if data.modified:
                log.info(f"Status changed after {elapsed} seconds")
                log.info("Delaying 10 seconds for changes to download...")
                time.sleep(10)
                break
        else:
            log.info(f"No status change after {elapsed} seconds")

    if cleanup:
        with datafiles.frozen(data):
            data.prune_status()

    if delay is None:
        return daemon.restart(manager)

    return True


if __name__ == "__main__":
    main()
