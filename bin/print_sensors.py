#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Prints sensor information to stdout'''
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
from pytan import Reporter
from pytan import cmdline_parser

utils.version_check(__version__)
parent_parser = cmdline_parser.setup_parser(__doc__)
parser = cmdline_parser.CustomParser(
    description=__doc__,
    parents=[parent_parser],
)
output_group = parser.add_argument_group('Output Options')
output_group.add_argument(
    '--category',
    required=False,
    default=[],
    action='append',
    dest='CATEGORIES',
    help='Only show sensors in given category',
)
output_group.add_argument(
    '--platform',
    required=False,
    default=[],
    action='append',
    dest='PLATFORMS',
    help='Only show sensors for given platform',
)
output_group.add_argument(
    '--sensor_regex',
    required=False,
    default=[],
    action='append',
    dest='SENSOR_REGEXES',
    help='Only show sensors whose name matches a regex',
)
output_group.add_argument(
    '--hide_params',
    required=False,
    default=False,
    action='store_true',
    dest='HIDE_PARAMS',
    help='Do not show parameters in output',
)
output_group.add_argument(
    '--params_only',
    required=False,
    default=False,
    action='store_true',
    dest='PARAMS_ONLY',
    help='Only show sensors with parameters',
)
output_group.add_argument(
    '--json',
    required=False,
    default=False,
    action='store_true',
    dest='JSON_SENSOR',
    help='Show a json dump of the sensor information',
)

script_group = parser.add_argument_group('Get Sensor Options')
script_group.add_argument(
    '--query',
    required=True,
    action='append',
    dest='query',
    help='Object to get - can prepend with id:, name:, or hash: '
    '- name: will be prepended by default, use "all" to get all objects',
)
args = parser.parse_args()
handler_args = args.__dict__

# put our query args into their own dict and remove them from handler_args
qgrp_names = ['Get Sensor Options']
qgrp_opts = cmdline_parser.get_grp_opts(parser, qgrp_names)
qgrp_args = {k: handler_args.pop(k) for k in qgrp_opts}

# put our transform args into their own dict and remove them from handler_args
tgrp_names = ['Output Options']
tgrp_opts = cmdline_parser.get_grp_opts(parser, tgrp_names)
tgrp_args = {k: handler_args.pop(k) for k in tgrp_opts if k in handler_args}

objtype = 'sensor'

handler = Handler(**handler_args)
print str(handler)

response = utils.get_object_case(handler, objtype, qgrp_args)

reporter = Reporter()
human_out = reporter.humanize_result_object(response, **tgrp_args)
print human_out
