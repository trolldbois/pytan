import os
import code
import atexit
try:
    import readline
except ImportError:
    import pyreadline as readline
import rlcompleter  # noqa


# TODO figure out pyreadline later
class HistoryConsole(code.InteractiveConsole):
    """Class that provides an interactive python console with full auto complete, history, and
    history file support.

    Examples
    --------
        >>> HistoryConsole()
    """
    def __init__(self, locals=None, filename="<console>",
                 histfile=os.path.expanduser("~/.console-history"), **kwargs):
        code.InteractiveConsole.__init__(self, locals, filename)

        self.atexit = atexit
        self.readline = readline

        # setup autocomplete
        rldoc = getattr(readline, '__doc__', '') or ''
        if 'libedit' in rldoc:
            self.readline.parse_and_bind("bind ^I rl_complete")
            self.readline.parse_and_bind("bind ^R em-inc-search-prev")

        self.readline.parse_and_bind("tab: complete")

        # setup a method to write the history file on exit
        if hasattr(self.readline, "write_history_file"):
            self.atexit.register(self.write_history, histfile)

        # read the history file now
        if hasattr(self.readline, "read_history_file"):
            try:
                self.readline.read_history_file(histfile)
            except IOError:
                # the file doesn't exist/can't be accessed
                pass

    def write_history(self, histfile):
        if hasattr(self.readline, "write_history_file"):
            self.readline.write_history_file(histfile) # noqa
