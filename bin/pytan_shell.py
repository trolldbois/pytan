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
import taniumpy # noqa
import taniumpy as api # noqa
from pytan import utils
from pytan import constants  # noqa

# adds readline, autocomplete, history to python interactive console
import atexit
import os
import sys
import pprint
import code
from datetime import datetime
import logging
import time
logging.Formatter.converter = time.gmtime

try:
    import readline
    import rlcompleter
except:
    pass

sys.dont_write_bytecode = True


def timing(c):
    t_start = datetime.now()
    r = eval(c)
    t_end = datetime.now()
    t_elapsed = t_end - t_start

    m = "Timing info for {} -- START: {}, END: {}, ELAPSED: {}, RESPONSE LEN: {}".format
    logging.info(m(c, t_start, t_end, t_elapsed, len(r)))
    return (c, r, t_start, t_end, t_elapsed)


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
    my_args = dict(all_args)
    handler_grp_names = ['Handler Authentication', 'Handler Options']
    handler_opts = utils.get_grp_opts(parser, handler_grp_names)
    handler_args = {k: my_args.pop(k) for k in handler_opts}

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


def get_rdattr(rd, a):
    try:
        k = getattr(rd, a)
    except:
        k = None
    if type(k) in [list, tuple]:
        k = len(k)
    return k


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
    session = handler.session
    self = handler

    if handler.loglevel >= 20:
        utils.set_all_loglevels()

    v = "Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*}"
    while True:
        start = datetime.utcnow()
        q_obj = handler.ask_manual_human(sensors=v, get_results=False)['question_object']
        # asker = taniumpy.QuestionAsker(self.session, q_obj, timeout=1)
        # try:
        # asker.run({'ProgressChanged': utils.question_progress})
        # logging.info("question ran normally, going to next one..")
        # except Exception as e:
        # logging.info("QUESTION RAN BUT HIT EXCEPTION: {}".format(e))
        q_obj_expiry = datetime.strptime(q_obj.expiration, '%Y-%m-%dT%H:%M:%S')
        expired = False
        while not expired:
            time.sleep(2)
            rd = session.getResultData(q_obj)

            now = datetime.utcnow()
            left_till_expiry = q_obj_expiry - now
            q_expired = now >= q_obj_expiry
            elapsed = now - start

            try:
                rd_ex = handler.export_obj(rd, 'csv')
                rd_ex_len = len(rd_ex)
            except:
                rd_ex = None
                rd_ex_len = 0

            mr_tested = get_rdattr(rd, 'mr_tested')
            estimated_total = get_rdattr(rd, 'estimated_total')

            logging.info((
                "ID: {}, rd len: {}, start: {}, now: {}, expires: {}, elapsed: {}, left_till_expiry: {}"
            ).format(
                q_obj.id,
                rd_ex_len,
                start,
                now,
                q_obj_expiry,
                elapsed,
                left_till_expiry
            ))

            rd_attrs = sorted(rd.__dict__)
            rd_attrs = ", ".join(["{}: {}".format(a, get_rdattr(rd, a)) for a in rd_attrs])
            logging.info(rd_attrs)
            si = session.get_server_info()
            diags = si['Diagnostics']
            perf = [x for x in diags if 'System Performance Info' in x.keys()][0]
            perf = dict([(key, d[key]) for d in perf.values()[0] for key in d])
            perf_str = ", ".join(["{}: {}".format(a, b) for a, b in perf.items()])
            logging.info(perf_str)

            if q_expired:
                expired = True
                logging.warning("question expired!!!")
                if not rd_ex_len > 0:
                    rd = session.getResultData(q_obj)
                    print si
                    print session.request_body
                    print session.response_body
                    introspect(rd)
                    raise Exception("no result data exported!!")

            if not estimated_total:
                raise Exception("estimated total is {}!!".format(estimated_total))

            if mr_tested >= estimated_total:
                logging.warning("QUESTION PASSED/FINISHED IN {}".format(elapsed))
                break
