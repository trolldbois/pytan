"""Interactive python console with full auto complete, history, and history file support."""
from __future__ import absolute_import, division, print_function, unicode_literals

import code
import os


class HistoryConsole(code.InteractiveConsole):
    """Interactive python console with full auto complete, history, and history file support.

    Examples
    --------
        >>> HistoryConsole()
    """

    HISTFILE = "~/.console-history"
    FILENAME = "<console>"

    def __init__(self, locals=None, **kwargs):
        """Interactive python console with full auto complete, history, and history file support."""
        import atexit
        import readline
        import rlcompleter  # noqa

        self.FILENAME = kwargs.get("filename", self.FILENAME)
        self.HISTFILE = os.path.expanduser(kwargs.get("histfile", self.HISTFILE))
        code.InteractiveConsole.__init__(self, locals, self.FILENAME)

        self.atexit = atexit
        self.readline = readline

        # setup autocomplete
        rldoc = getattr(readline, "__doc__", "") or ""
        if "libedit" in rldoc:
            self.readline.parse_and_bind("bind ^I rl_complete")
            self.readline.parse_and_bind("bind ^R em-inc-search-prev")

        self.readline.parse_and_bind("tab: complete")

        # setup a method to write the history file on exit
        if hasattr(self.readline, "write_history_file"):
            self.atexit.register(self.write_history, self.HISTFILE)

        # read the history file now
        if hasattr(self.readline, "read_history_file"):
            try:
                self.readline.read_history_file(self.HISTFILE)
            except IOError:
                # the file doesn't exist/can't be accessed
                pass

    def write_history(self, histfile):
        """Write the history file."""
        if hasattr(self.readline, "write_history_file"):
            self.readline.write_history_file(histfile)
