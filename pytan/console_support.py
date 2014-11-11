# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""
Adds readline support and other handy things to an interactive python
console.
"""
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'

# adds readline, autocomplete, history to python interactive console
import atexit
import os
import sys
import pprint
import code

try:
    import readline
    import rlcompleter
except:
    pass

sys.dont_write_bytecode = True


def debug_list(debuglist):
    for x in debuglist:
        debug_obj(x)


def debug_obj(debugobj):
    pprint.pprint(vars(debugobj))


# Utility function to dump all info about an object
def introspect(obj, depth=0):
    import types
    print "%s%s: %s\n" % (depth * "\t", obj, [
        x for x in dir(obj) if x[:2] != "__"])
    depth += 1
    for x in dir(obj):
        if x[:2] == "__":
            continue
        subobj = getattr(obj, x)
        print "%s%s: %s" % (depth * "\t", x, subobj)
        if isinstance(subobj, types.InstanceType) and dir(subobj) != []:
            introspect(subobj, depth=depth + 1)
            print


class HistoryConsole(code.InteractiveConsole):
    def __init__(self, locals=None, filename="<console>",
                 histfile=os.path.expanduser("~/.console-history")):
        code.InteractiveConsole.__init__(self, locals, filename)
        try:
            self.init_history(histfile)
        except:
            pass

    def init_history(self, histfile):
        if 'libedit' in readline.__doc__:
            # osx style readline
            readline.parse_and_bind("bind ^I rl_complete")
            readline.parse_and_bind("bind ^R em-inc-search-prev")
        else:
            # unix style readline
            readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self.save_history, histfile)

    @staticmethod
    def save_history(histfile):
        readline.write_history_file(histfile)


console = HistoryConsole()
