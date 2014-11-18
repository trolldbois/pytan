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

import pytan
from pytan.console_support import *
from pytan import cmdline_parser

pytan.utils.version_check(__version__)
parent_parser = cmdline_parser.setup_parser(__doc__)
parser = cmdline_parser.CustomParser(
    description=__doc__,
    parents=[parent_parser],
)
args = parser.parse_args()
handler_args = args.__dict__

handler = pytan.Handler(**handler_args)
# reporter = Reporter()

if handler_args['loglevel'] >= 10:
    pytan.utils.set_all_loglevels()

print ("%s -- now available as 'handler'!" % handler)
# print ("%s -- now available as 'reporter'!" % reporter)

# ask saved question:
r = handler.ask('saved', name='Manually Created Complex Saved Question')
sensors = [x.sensor for x in r.asker.question.question.selects]
with open('die.csv', 'w') as fd:
    r.write_csv(fd, r)

with open('die_sensors.csv', 'w') as fd:
    r.write_csv(fd, r, header_add_sensor=True, sensors=sensors)


with open('die_sensors_type.csv', 'w') as fd:
    r.write_csv(fd, r, header_add_sensor=True, sensors=sensors, header_add_type=True)

header_sort = ['Tanium Zone Server Version']

with open('die_sensors_type_sort.csv', 'w') as fd:
    r.write_csv(fd, r, header_add_sensor=True, sensors=sensors, header_add_type=True, header_sort=header_sort, expand_grouped_columns=True)

# # write sensor objects out:
# r = handler.get_all('sensor')
# if hasattr(r, '_list_properties'):
#     report_on = getattr(r, r._list_properties.keys()[0])
# else:
#     report_on = r

# with open('die.csv', 'w') as fd:
#     r.write_csv(fd, report_on, explode_json_string_values=True)
