#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Get saved_question objects and save the results as a report format'''
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
parser = cmdline_parser.setup_report_sort_parser(parser)
parser = cmdline_parser.setup_get_object_parser(parser)
args = parser.parse_args()
handler_args = args.__dict__

# put our query args into their own dict and remove them from handler_args
qgrp_names = ['Get Object Options']
qgrp_opts = cmdline_parser.get_grp_opts(parser, qgrp_names)
qgrp_args = {k: handler_args.pop(k) for k in qgrp_opts}

# put our transform args into their own dict and remove them from handler_args
tgrp_names = ['Report Options', 'Report Sort Options']
tgrp_opts = cmdline_parser.get_grp_opts(parser, tgrp_names)
tgrp_args = {k: handler_args.pop(k) for k in tgrp_opts if k in handler_args}

objtype = 'saved_question'

handler = Handler(**handler_args)
print str(handler)

response = utils.get_object_case(handler, objtype, qgrp_args)
utils.write_object(handler, response, tgrp_args)
