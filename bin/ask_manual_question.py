#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Ask a manual question and save the results as a report format'''
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
parser = utils.setup_ask_manual_argparser(__doc__)
parser = utils.add_ask_report_argparser(parser)

args = parser.parse_args()
all_args = args.__dict__

handler = process_handler_args(parser, all_args)

q_opts = ['sensors', 'question_filters', 'question_options']
q_args = {k: all_args.pop(k) for k in q_opts}

print "++ Asking manual question: {}".format(q_args)
response = handler.ask(qtype='manual_human', **q_args)
print "++ Received Response: ", str(response)

report_file, result = handler.export_to_report_file(response, **all_args)
m = "Report file {!r} written with {} bytes".format
print(m(report_file, len(result)))
