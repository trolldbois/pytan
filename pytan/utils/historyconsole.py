import os
import code
import atexit
import logging
import platform

mylog = logging.getLogger(__name__)

if platform.system().lower() == 'windows':
    from .externalwin import readline
else:
    import readline

import rlcompleter  # noqa


class HistoryConsole(code.InteractiveConsole):
    """Class that provides an interactive python console with full auto complete, history, and history file support.

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
        else:
            m = "readline module {} has no write_history_file(), methods: {}"
            mylog.debug(m.format(self.readline, dir(self.readline)))

        # read the history file now
        if hasattr(self.readline, "read_history_file"):
            try:
                self.readline.read_history_file(histfile)
            except IOError:
                # the file doesn't exist/can't be accessed
                pass
            except Exception as e:
                m = "Unable to read history file '{}', exception: '{}'"
                self.mylog.debug(m.format(histfile, e))
        else:
            m = "readline module {} has no read_history_file(), methods: {}"
            mylog.debug(m.format(self.readline, dir(self.readline)))

    def write_history(self, histfile):
        if hasattr(self.readline, "write_history_file"):
            try:
                self.readline.write_history_file(histfile) # noqa
            except Exception as e:
                m = "Unable to write history file '{}', exception: '{}'"
                mylog.debug(m.format(histfile, e))
        else:
            m = "readline module {} has no write_history_file(), methods: {}"
            mylog.debug(m.format(self.readline, dir(self.readline)))
