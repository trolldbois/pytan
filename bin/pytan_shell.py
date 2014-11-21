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

if handler_args['loglevel'] >= 10:
    pytan.utils.set_all_loglevels()

print ("%s -- now available as 'handler'!" % handler)


'''ask_manual_human example'''

sensors = [
    (
        'Folder Name Search with RegEx Match{dirname=Program Files,regex=.*}'
        ', that is .*, opt:max_data_age:3600, opt:ignore_case, '
        'opt:match_any_value'
    )
]

question_filters = [
    'Operating System, that contains Windows'
]

question_options = [
    'max_data_age:3600', 'ignore_case', 'and',
]

result = handler.ask(
    qtype='manual_human',
    sensors=sensors,
    question_filters=question_filters,
    question_options=question_options,
)


sensor_hashes = [x.hash for x in result.sensors]
column_hashes = [x.what_hash for x in result.columns]
missing_hashes = [
    x for x in column_hashes if x not in sensor_hashes and x > 1
]
missing_sensors = handler.get('sensor', hash=missing_hashes)
sensors = result.sensors + list(missing_sensors)

with open('die_manualq1.csv', 'w') as fd:
    result.write_csv(
        fd,
        result,
        header_add_sensor=True,
        sensors=sensors,
        header_add_type=True,
        expand_grouped_columns=True,
    )


'''ask_manual example'''
sensor_defs = [
    {
        "name": "Computer Name",
    },
    {
        "name": "Folder Name Search with RegEx Match",
        'params': {'dirname': 'Program Files'},
        'filter': {"operator": "RegexMatch", "not_flag": 0, "value": ".*"},
        'options': {
            'max_age_seconds': 3600,
            'ignore_case_flag': 0,
            'value_type': 'string',
        },
    },
]

q_filters = [
    {
        "name": "Operating System",
        "filter": {
            'operator': "RegexMatch",
            'not_flag': 0,
            'value': ".*Windows.*",
        },
    },
]

q_options = {
    'max_age_seconds': 3600,
    'ignore_case_flag': 0,
    'and_flag': 0,
}

result = handler.ask(
    qtype='manual',
    sensor_defs=sensor_defs,
    question_filters=q_filters,
    question_options=q_options,
)

sensor_hashes = [x.hash for x in result.sensors]
column_hashes = [x.what_hash for x in result.columns]
missing_hashes = [
    x for x in column_hashes if x not in sensor_hashes and x > 1
]
missing_sensors = handler.get('sensor', hash=missing_hashes)
sensors = result.sensors + list(missing_sensors)

with open('die_manualq2.csv', 'w') as fd:
    result.write_csv(
        fd,
        result,
        header_add_sensor=True,
        sensors=sensors,
        header_add_type=True,
        expand_grouped_columns=True,
    )
