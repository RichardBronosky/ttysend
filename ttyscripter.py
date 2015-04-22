#!/usr/bin/env python

"""A UI for ttysender.

Useful for giving live demo presentations.
"""

import urwid
import os
import signal
import sys
import tempfile
from time import sleep
from random import randint
import argparse
import ttysend


def get_commands(data):
    """Read file and split on detected separator."""
    # Split on either double or single spaced lines.
    if data.find('\n\n') == -1:
        data = data.split('\n')
    else:
        data = data.split('\n\n')
    if len(data[-1]) == 0:
        del(data[-1])
    # Strip the trailing newline
    return map(lambda x: x.strip('\n'), data)


def get_tty():
    """Return device path for current tty."""
    return os.ttyname(sys.stdout.fileno())


def store_tty():
    """Write tty device path to temp file."""
    with open(os.path.join(tempfile.gettempdir(), 'ttyscripter.tty'),
              'w') as fd:
        fd.write(get_tty())


def retrieve_tty():
    """Read tty device path from temp file."""
    with open(os.path.join(tempfile.gettempdir(), 'ttyscripter.tty')) as fd:
        return fd.read()


def menu(title, entries):
    """Return a ListBox of SimpleFocusListWalker Buttons."""
    body = [urwid.Text(('banner', title), align='center'), urwid.Divider()]

    for i, c in enumerate(entries):
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.append(urwid.AttrMap(button,
                    {None: ('odd', 'even')[i % 2]},
                    focus_map='higlighted'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def mark_menu_item(menu):
    """Change palette entry to the corresponding 'used' value."""
    obj = menu.body[menu.body.focus]
    key = obj.attr_map.keys()[0]
    is_even = obj.attr_map[key].find('even') > -1
    obj.set_attr_map({key: ('used_odd', 'used_even')[is_even]})


def advance_menu(menu):
    """Select the next item or add and empty items at the end if needed."""
    try:
        menu.focus_position += 1
    # The error indicates you are focused on the last postion.
    except IndexError:
        # Create and select an empty button.
        # This button has no event handler, so this shouldn't be called again.
        menu.body.append(urwid.Button(''))
        menu.focus_position += 1


def item_chosen(button, choice):
    """Respond to button clicks and enter or space presses."""
    # from pudb import set_trace; set_trace()
    mark_menu_item(cli.main_menu)
    advance_menu(cli.main_menu)
    send_wrapper(choice, cli.tty)


def exit_program(*args):
    """Exit the main loop cleanly.

    Accept but ignore args so this can be uses as an urwid event handler.
    """
    cli.tty.close()
    raise urwid.ExitMainLoop()


def send_wrapper(choice, tty):
    """Chose the right display method."""
    if hasattr(cli, 'args') and cli.args.n:
        ttysend.send_raw(choice.replace('\\n', '\n'), tty)
    else:
        ttysend.send(choice, tty)


def delay(data, i):
    """Delay output to simulate natural typing."""
    # Long pause bewteen words
    if data[i-1] == ' ':
        sleep(float(12)/100)
    # Random pause mid word
    sleep(float(randint(5, 16))/100)


def cli():
    """Used by to console_scripts entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', type=argparse.FileType('r'),
                        help='Read commands from <filename>')
    parser.add_argument('-d', action='store_true',
                        help='Delay output to simulate natural typing')
    parser.add_argument('-n', action='store_true',
                        help='Newlines are sent in place of \\n')
    group1 = parser.add_mutually_exclusive_group(required=True)
    group1.add_argument('--tty', type=argparse.FileType('w'),
                        metavar='device_path',
                        help='TTY to use as output destination')
    group1.add_argument('-s', action='store_true',
                        help='Store current tty device path for use with -t')
    group1.add_argument('-t', action='store_true',
                        help='Use the stored tty device as the '
                        'output destination')
    cli.args = parser.parse_args()

    if cli.args.tty:
        cli.tty = cli.args.tty
    elif cli.args.t:
        cli.tty = open(retrieve_tty(), 'w')
    elif cli.args.s:
        sys.exit(store_tty())

    if cli.args.d:
        ttysend.delay = delay

    if not cli.args.filename:
        parser.error('<filename> is required when not using -s.')

    commands = cli.args.filename.read()

    cli.main_menu = menu(u'Commands', get_commands(commands))
    main = urwid.Padding(cli.main_menu, left=2, right=2)
    palette = [
        ('higlighted', 'black', 'dark red'),
        ('odd', 'light gray', 'black'),
        ('used_odd', 'light cyan', 'black'),
        ('even', 'light gray', 'dark gray'),
        ('used_even', 'light cyan', 'dark gray'), ]
    signal.signal(signal.SIGINT, exit_program)
    urwid.MainLoop(main, palette).run()


if __name__ == '__main__':
    cli()
