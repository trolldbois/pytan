#!/usr/bin/env python -i
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''get an interactive console with pytan available as handler'''
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
from pytan.console_support import *

utils.version_check(__version__)
parent_parser = cmdline_parser.setup_parser(__doc__)
parser = cmdline_parser.CustomParser(
    description=__doc__,
    parents=[parent_parser],
)
args = parser.parse_args()
handler_args = args.__dict__

handler = Handler(**handler_args)
reporter = Reporter()

if handler_args['loglevel'] >= 10:
    utils.set_all_loglevels()

print ("%s -- now available as 'handler'!" % handler)
print ("%s -- now available as 'reporter'!" % reporter)

sensors = [
    # will fail because "does not meet" is not a valid operator
    # 'Computer name, that does not meet little',

    # will fail because "IP Sensor" is not a valid sensor
    # 'IP Sensor, that ipaddress = 127.0.0.1',

    # will fail because multiple parameters ([][])
    # 'Folder Name Search with RegEx Match[Program Files,.*,No,No][]',

    # will fail because Computer Name does not take params
    # 'Computer Name[Dweedle]',

    # will print help and exit
    # 'Operating system, that help'
    # 'Operating system, opt:help'

    # all will work...
    # 'Computer Name',
    # 'Operating System, that contains Windows, opt:match_all_values',
    'Operating System, that string contains Windows',
    # "Folder Name Search with RegEx Match, that is .*",
    # "Folder Name Search with RegEx Match[Program Files,.*,No,No], that is .*", opt,
]

'''
        sensor filter options:
        opt:ignore_case, opt:match_case, opt:match_any_value, opt:match_all_values, opt:max_data_age:1 hour

-                <ignore_case_flag>1</ignore_case_flag> IGNORE CASE
+                <ignore_case_flag>0</ignore_case_flag> MATCH CASE

-                <all_values_flag>0</all_values_flag> Match any value
+                <all_values_flag>1</all_values_flag> Match all values
-                <all_times_flag>0</all_times_flag>  Match any value
+                <all_times_flag>1</all_times_flag>  Match all values
-                <max_age_seconds>0</max_age_seconds> max data age
+                <max_age_seconds>950400</max_age_seconds> max data age

next to do add build objects dict support for filters and options
'''
r = handler.ask_manual_question(sensors)
