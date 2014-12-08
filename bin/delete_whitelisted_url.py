#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Delete a whitelisted_url object'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '1.0.1'

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
        'name': 'Delete whitelisted_url',
        'cmd': 'delete_whitelisted_url.py $API_INFO --id 123456',
        'notes': ['This example does not actually run'],
        'norun': 'true',
        'tests': '',
    }
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
    parser = utils.setup_delete_object_argparser('whitelisted_url', __doc__)
    args = parser.parse_args()
    all_args = args.__dict__

    handler = process_handler_args(parser, all_args)

    try:
        response = utils.process_delete_object_args(
            parser, handler, 'whitelisted_url', all_args
        )
    except Exception as e:
        print e
        sys.exit(99)
