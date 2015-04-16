# ttysend
---------
Send input to a tty (other than the one you are on)

# Usage
    ## In current tty
    $ python ttysend.py /dev/ttys002 ls -la
    ERROR: Only root can send input to other TTYs.
    $ sudo python ttysend.py /dev/ttys002 ls -la

    # In ttys002
    drwxr-xr-x   12 bruno  staff    408 Apr 16 03:00 .
    drwxrwxr-x  183 bruno  staff   6222 Apr 15 15:44 ..
    drwxr-xr-x   12 bruno  staff    408 Apr 16 03:00 .git
    -rw-r--r--    1 bruno  staff    702 Apr 16 02:59 .gitignore
    -rw-r--r--    1 bruno  staff   1082 Apr 16 02:59 LICENSE
    -rw-r--r--    1 bruno  staff     62 Apr 16 02:59 README.md
    -rw-r--r--    1 bruno  staff   1279 Apr 16 02:56 ttysend.py
