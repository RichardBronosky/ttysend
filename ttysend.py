from __future__ import print_function
import sys
import os
import fcntl
import termios
import argparse


class RootRequired(Exception):

    """Our standard exception."""

    pass


def send(data, tty):
    """Send each char of data to tty."""
    if(os.getuid() != 0):
        raise RootRequired('Only root can send input to other TTYs.')
    for c in data:
        fcntl.ioctl(tty, termios.TIOCSTI, c)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tty', type=argparse.FileType('w'),
                        help='display a square of a given number')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-n', action='store_true',
                       help='Do not print the trailing newline character.')
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
        send(data, args.tty)
    except RootRequired, e:
        sys.exit(print('ERROR:', e, file=sys.stderr))

    # Handle trailing newline
    if data[-1][-1] != '\n' and not args.n:
        send('\n', args.tty)
