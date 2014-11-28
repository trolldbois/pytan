#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Get results from a deploy action, saved question, or question'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '0.8.0'

import os
import sys

sys.dont_write_bytecode = True
my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
path_adds = [parent_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

import pytan
from pytan import utils


def process_handler_args(parser, all_args):
    handler_grp_names = ['Handler Authentication', 'Handler Options']
    handler_opts = utils.get_grp_opts(parser, handler_grp_names)
    handler_args = {k: all_args.pop(k) for k in handler_opts}

    h = pytan.Handler(**handler_args)
    print str(h)
    return h

utils.version_check(__version__)
parser = utils.setup_get_result_argparser(__doc__)
parser = utils.add_ask_report_argparser(parser)

args = parser.parse_args()
all_args = args.__dict__

handler = process_handler_args(parser, all_args)

if args.object_type == 'saved_question':
    obj = handler.get('saved_question', id=args.object_id)[0]
elif args.object_type == 'question':
    obj = handler.get('question', id=args.object_id)[0]
elif args.object_type == 'action':
    obj = handler.get('action', id=args.object_id)[0]

m = "++ Found object: {}".format
print(m(obj))

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
