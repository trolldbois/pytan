#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Get server info'''
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
args = parser.parse_args()
handler_args = args.__dict__

handler = Handler(**handler_args)
print str(handler)

print utils.jsonify(handler.server_info)
