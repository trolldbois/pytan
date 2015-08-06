#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Ask a saved question and save the results as a report format'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '2.0.0'

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

examples = [
    {
        'name': 'Ask a saved question',
        'cmd': (
            'ask_saved_question.py $API_INFO '
            '--name "Installed Applications" --file "$TMP/out.csv" csv'
        ),
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
]


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


if __name__ == "__main__":

    utils.version_check(__version__)
    parser = utils.setup_ask_saved_argparser(__doc__)
    parser = utils.add_ask_report_argparser(parser)

    args = parser.parse_args()
    all_args = args.__dict__

    if args.id:
        q_args = {'id': args.id}
    elif args.name:
        q_args = {'name': args.name}
    else:
        parser.error("Must supply --id or --name")

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

    try:
        print "++ Asking saved question: {}".format(args.id or args.name)
        ret = handler.ask(qtype='saved', **q_args)
        print "++ Saved Question {!r} ID: {!r}".format(
            ret['question_object'].query_text, ret['question_object'].id
        )

        report_file, result = handler.export_to_report_file(
            obj=ret['question_results'],
            **all_args
        )
        m = "Report file {!r} written with {} bytes".format
        print(m(report_file, len(result)))
    except Exception as e:
        print e
        sys.exit(99)
