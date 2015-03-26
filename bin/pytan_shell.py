#!/usr/bin/env python -i
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''get an interactive console with pytan available as handler'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '1.0.4'

examples = []

import os
import sys
import getpass
sys.dont_write_bytecode = True
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

import pytan
from pytan import utils
from pytan import constants  # noqa

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
            self.rldoc = rlcompleter.__doc__
        except:
            pass
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


def process_handler_args(parser, all_args):
    handler_grp_names = ['Handler Authentication', 'Handler Options']
    handler_opts = utils.get_grp_opts(parser, handler_grp_names)
    handler_args = {k: all_args.pop(k) for k in handler_opts}

    try:
        h = pytan.Handler(**handler_args)
        print str(h)
    except Exception as e:
        print e
        sys.exit(99)
    return h


def dictify_resultset(rs):
    return [dictify_resultset_row(x) for x in rs.rows]


def dictify_resultset_row(rs_row):
    d = dict(zip(
        [x.display_name for x in rs_row.columns],
        [join_list(x, ', ') for x in rs_row.vals]
    ))
    return d


def join_list(l, j='\n'):
    if None in l:
        l = ""
    if type(l) == list:
        l = j.join(l)
    return l


def remove_count(rd):
    for r in rd:
        try:
            r.pop('Count')
        except:
            pass
    return rd


def get_question_data(i):
    return dictify_resultset(handler.get_result_data(handler.get('question', id=i)[0]))


def get_action_data(i):
    return dictify_resultset(handler.get_result_data(handler.get('action', id=i)[0]))


def chew_question_data(i, renew=False):
    if renew:
        return get_question_data(i['question_object'].id)
    else:
        return dictify_resultset(i['question_results'])


def create_get_pkg(handler, pkg_name, pkg_opts):
    try:
        p = handler.get('package', name=pkg_name)[0]
        m = 'Found package {}, skipped creation'.format
    except:
        p = handler.create_package(name=pkg_name, **pkg_opts)
        m = 'Created package {}'.format
    print m(pkg_name)
    return p

if __name__ == "__main__":

    console = HistoryConsole()

    utils.version_check(__version__)
    parent_parser = utils.setup_parser(__doc__)
    parser = utils.CustomArgParse(
        description=__doc__,
        parents=[parent_parser],
    )
    args = parser.parse_args()
    all_args = args.__dict__
    if not args.username:
        username = raw_input('Tanium Username: ')
        all_args['username'] = username.strip()

    if not args.password:
        password = getpass.getpass('Tanium Password: ')
        all_args['password'] = password.strip()

    if not args.host:
        host = raw_input('Tanium Host: ')
        all_args['host'] = host.strip()

    handler = process_handler_args(parser, all_args)

    if handler.loglevel >= 10:
        utils.set_all_loglevels()
