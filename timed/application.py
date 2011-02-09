#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Main logic and argument handling for timed."""

import sys
import os.path
import argparse

from timed.timed import Timed

def buildArguments():
    """Return an argparse object with the known arguments."""
    parser = argparse.ArgumentParser(description="A command-line time tracker.")
    parser.add_argument("-v", "--version", action="version",
        version="%(prog)s v0.13", help="show version information and exit")
    subparser = parser.add_subparsers(title="sub-commands")

    status = subparser.add_parser("status", help="print current status")
    status.set_defaults(func=Timed.status)
    status.add_argument("-q", "--quiet", action="store_true",
        help="print only the current active project")

    start = subparser.add_parser("start", help="start tracking for [project]")
    start.add_argument("project", help="the project name")
    start.set_defaults(func=Timed.start)

    stop = subparser.add_parser("stop", help="stop tracking for the current project")
    stop.set_defaults(func=Timed.stop)

    summary = subparser.add_parser("summary",
        help="print a summary of hours for all projects")
    summary.set_defaults(func=Timed.summary)

    return parser

def parseArguments(parser):
    """Parse the command-line arguments."""

    # XXX: argparse does not support optional subparsers
    # See: http://bugs.python.org/issue9253
    if len(sys.argv) == 1:
        # Default to "status" if no arguments given
        sys.argv.append("status")

    args = parser.parse_args()
    return args.func

def main():
    """Start execution of timed."""
    log_file = os.path.expanduser('~/.timed')
    time_format = "%H:%M on %d %b %Y"

    args = parseArguments(buildArguments())

    if not os.path.exists(log_file):
        open(log_file, 'w').close()  

    timed = Timed(log_file, time_format)
    args(timed)

if __name__ == "__main__":
    main()
