#!/usr/bin/env python

"""Sends data to the input of a local TTY.

Requires root privileges.
"""

from __future__ import print_function
import sys
import os
import fcntl
import termios
import argparse


class RootRequired(Exception):

    """Our standard exception."""

    pass


def delay(data, i):
    """Override this function to insert a delay."""
    pass


def send(data, tty):
    """Send each char of data to tty, being intelligent about newlines."""
    if len(data):
        # Handle trailing newline
        if data[-1][-1] != '\n':
            data += '\n'
        send_raw(data, tty)


def send_raw(data, tty):
    """Send each char of data to tty."""
    if(os.getuid() != 0):
        raise RootRequired('Only root can send input to other TTYs.')
    for i, c in enumerate(data):
        # Must not insert delays in the middle of escape sequences
        if chr(27) not in data:
            delay(data, i)
        fcntl.ioctl(tty, termios.TIOCSTI, c)


def cli():
    """Used by to console_scripts entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument('tty', type=argparse.FileType('w'),
                        help='display a square of a given number')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-n', action='store_true',
                       help='Do not force a trailing newline character.')
    group.add_argument('--stdin', action='store_true',
                       help='Read input from stdin.')
    args, data = parser.parse_known_args()

    # Prepare data
    if args.stdin:
        data = sys.stdin.read()
    else:
        data = ' '.join(data)

    # Send data
    try:
        if args.n:
            send_raw(data, args.tty)
        else:
            send(data, args.tty)
    except RootRequired, e:
        sys.exit(print('ERROR:', e, file=sys.stderr))


if __name__ == '__main__':
    cli()
