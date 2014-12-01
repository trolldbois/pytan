#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Stop a deploy action ID'''
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
parser = utils.setup_stop_action_argparser(__doc__)

args = parser.parse_args()
all_args = args.__dict__

handler = process_handler_args(parser, all_args)

d_opts = ['id']
d_args = {k: all_args.pop(k) for k in d_opts}

print "++ Stopping action: {}".format(d_args)
action_stop = handler.stop_action(**d_args)
print "++ Action stopped successfully, id of action stop:", action_stop.id
