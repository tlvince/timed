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
