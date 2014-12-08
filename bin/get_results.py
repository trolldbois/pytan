#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Get results from a deploy action, saved question, or question'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '1.0.1'

examples = []

import os
import sys
sys.dont_write_bytecode = True
my_file = os.path.abspath(__file__)
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
        'name': 'Get the results for a saved question',
        'cmd': (
            'get_results.py $API_INFO -o "saved_question" --id 107 --file "$TMP/out.csv" csv'
        ),
        'notes': ['Get the results for Saved Question ID 107', 'Save the results to a CSV file'],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Get the results for a question',
        'cmd': (
            'get_results.py $API_INFO -o "question" --id 249 --file "$TMP/out.csv" csv'
        ),
        'notes': ['Get the results for Question ID 249', 'Save the results to a CSV file'],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Get the results for a action',
        'cmd': (
            'get_results.py $API_INFO -o "action" --id 24 --file "$TMP/out.csv" csv'
        ),
        'notes': ['Get the results for action ID 24', 'Save the results to a CSV file'],
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
