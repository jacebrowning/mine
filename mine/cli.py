#!/usr/bin/env python

"""Command-line interface."""

import sys
import argparse

from . import common
from . import CLI, VERSION, DESCRIPTION


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
        log.debug("command cancelled")
        success = False
    if success:
        log.debug("command succeeded")
    else:
        log.debug("command failed")
        sys.exit(1)


def run():  # pragma: no cover (not implemented)
    """Run the program."""
    return False


if __name__ == '__main__':  # pragma: no cover (manual test)
    main()
