#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Ask a manual question and save the results as a report format'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '0.1'

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

from pytan import utils
from pytan import Handler
from pytan import cmdline_parser

utils.version_check(__version__)
parent_parser = cmdline_parser.setup_parser(__doc__)
parser = cmdline_parser.CustomParser(
    description=__doc__,
    parents=[parent_parser],
)

parser = cmdline_parser.setup_report_parser(parser)
parser = cmdline_parser.setup_question_report_parser(parser)
parser = cmdline_parser.setup_report_sort_parser(parser)
ask_question_group = parser.add_argument_group('Ask Manual Question Options')
ask_question_group.add_argument(
    '--sensor',
    required=True,
    action='append',
    dest='sensors',
    help='Sensors to use in manual question - can prepend with id:, name:, '
    ' or hash: - name: will be prepended by default',
)
args = parser.parse_args()
handler_args = args.__dict__

# put our query args into their own dict and remove them from handler_args
qgrp_names = ['Ask Manual Question Options']
qgrp_opts = cmdline_parser.get_grp_opts(parser, qgrp_names)
qgrp_args = {k: handler_args.pop(k) for k in qgrp_opts}

# put our transform args into their own dict and remove them from handler_args
tgrp_names = [
    'Report Options',
    'Question Report Options',
    'Report Sort Options',
]
tgrp_opts = cmdline_parser.get_grp_opts(parser, tgrp_names)
tgrp_args = {k: handler_args.pop(k) for k in tgrp_opts if k in handler_args}

handler = Handler(**handler_args)
print str(handler)

print "++ Asking manual question: ", utils.json.dumps(qgrp_args)
response = handler.ask_manual_question(**qgrp_args)
print "++ Received Response: ", str(response)

utils.write_object(handler, response, tgrp_args)
