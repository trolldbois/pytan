#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Get results from a deploy action, saved question, or question'''
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

examples = [
    {
        'name': 'Ask a question',
        'cmd': (
            'ask_manual_question.py $API_INFO --no-results --sensor "Computer Name" csv | tee $TMP/ask.out'
        ),
        'notes': ['Ask a question without getting the results, save stdout to ask.out'],
        'precleanup': 'rm -f $TMP/ask.out',
        'file_exist': '$TMP/ask.out',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Wait 30 seconds',
        'cmd': (
            'sleep 15'
        ),
        'notes': ['Wait 30 seconds for data for the previously asked question to be available'],
        'tests': 'exitcode',
    },
    {
        'name': 'Get the results for a question',
        'cmd': (
            'get_results.py $API_INFO -o "question" --id `cat $TMP/ask.out | grep ID| cut -d: -f2 | tr -d " "` --file "$TMP/out.csv" csv'
        ),
        'notes': ['Get the results for the question ID asked previously ', 'Save the results to a CSV file'],
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
    parser = utils.setup_get_result_argparser(__doc__)
    parser = utils.add_ask_report_argparser(parser)

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

    try:
        if args.object_type == 'saved_question':
            obj = handler.get('saved_question', id=args.object_id)[0]
        elif args.object_type == 'question':
            obj = handler.get('question', id=args.object_id)[0]
        elif args.object_type == 'action':
            obj = handler.get('action', id=args.object_id)[0]

    except Exception as e:
        print e
        sys.exit(99)

    m = "++ Found object: {}".format
    print(m(obj))

    try:
        results_obj = handler.get_result_data(obj)
        if results_obj.rows:
            m = "++ Found results for object: {}".format
            print(m(results_obj))

            report_file, result = handler.export_to_report_file(
                obj=results_obj,
                **all_args)
            m = "++ Report file {!r} written with {} bytes".format
            print(m(report_file, len(result)))

        else:
            m = "++ No rows returned for results: {}".format
            print(m(results_obj))
    except Exception as e:
        print e
        sys.exit(99)
