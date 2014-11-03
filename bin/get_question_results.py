#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Get results for a question ID and save the results as a report format'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '0.1'

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

import customparser
import SoapWrap
import SoapUtil

SoapUtil.version_check(__version__)
parent_parser = customparser.setup_parser(__doc__)
parser = customparser.CustomParser(
    description=__doc__,
    parents=[parent_parser],
)
parser.add_argument(
    '--query',
    required=True,
    action='store',
    dest='query',
    help='Question to get results for - can prepend with id:, '
    '- id: will be prepended by default',
)

parser = customparser.setup_transform_parser(parser)
parser = customparser.setup_transform_resultxml_parser(parser)
parser = customparser.setup_transform_sort_parser(parser)

args = parser.parse_args()
swargs = args.__dict__

# put our query args into their own dict and remove them from swargs
qkeys = ['query']
qargs = {k: swargs.pop(k) for k in qkeys}

# put our transform args into their own dict and remove them from swargs
f_grpnames = [
    'Report Options',
    'Question Report Options',
    'Report Sort Options',
]
fgrps = [a for a in parser._action_groups if a.title in f_grpnames]
fargs = [a.dest for b in fgrps for a in b._group_actions]
fargs = {k: swargs.pop(k) for k in fargs if k in swargs}

sw = SoapWrap.SoapWrap(**swargs)
print str(sw)
print "++ Getting question results: ", SoapUtil.json.dumps(qargs)
response = sw.get_question_results(**qargs)
print "++ Received Response: ", str(response)
print "++ Creating Report: ", SoapUtil.json.dumps(fargs)
report_file = sw.st.write_response(response, **fargs)
print "++ Report created: ", report_file
