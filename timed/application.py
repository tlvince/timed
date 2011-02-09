#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Main logic and argument handling for timed."""

import os.path
import argparse

def buildArguments():
    """Construct an argparse object."""
    parser = argparse.ArgumentParser(description="A command-line time tracker.")
    parser.add_argument("-v", "--version", action="version", version="0.13",
        help="show version information and exit")
    parser.add_argument("-q", "--quiet", action="store_true",
        help="print only the current active project")

    subparser = parser.add_subparsers(title="sub-commands")
    subparser.add_parser("status", help="print current status")
    start = subparser.add_parser("start", help="start tracking for [project]")
    start.add_argument("project", help="the project name")
    subparser.add_parser("stop", help="stop tracking for the current project")
    subparser.add_parser("summary",
        help="print a summary of hours for all projects")

    return parser

def parseArguments(parser):
    """Parse the command-line arguments."""
    parsed = parser.parse_args()
    return parsed

def main():
    """Start execution of timed."""
    log_file = os.path.expanduser('~/.timed')
    args = parseArguments(buildArguments())
    if not os.path.exists(log_file):
        open(log_file, 'w').close()  

if __name__ == "__main__":
    main()
