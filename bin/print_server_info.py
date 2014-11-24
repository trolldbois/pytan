#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Get server info'''
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

utils.version_check(__version__)
parent_parser = utils.setup_parser(__doc__)
parser = utils.CustomParser(
    description=__doc__,
    parents=[parent_parser],
)
parser.add_argument(
    '--json',
    required=False,
    default=False,
    action='store_true',
    dest='json',
    help='Show a json dump of the server information',
)

args = parser.parse_args()
handler_args = args.__dict__

handler = pytan.Handler(**handler_args)


def print_obj(d, indent=0):
    for k, v in d.iteritems():
        if utils.is_dict(v):
            print "{}{}: \n".format('  ' * indent, k),
            print_obj(v, indent + 1)
        elif utils.is_list(v):
            print "{}{}: ".format('  ' * indent, k)
            for a in v:
                print_obj(a, indent + 1)
        else:
            print "{}{}: {}".format('  ' * indent, k, v)


if args.json:
    print utils.jsonify(handler.session.server_info)
else:
    print str(handler)
    print_obj(handler.session.server_info)
