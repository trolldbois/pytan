#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''This is used to ask a parsed question
STILL A WIP
Last validated to work with:
- SoapWrap 0.1
- Python 2.7.3
'''
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
import tanwrap

tanwrap.version_check(__version__)
parent_parser = customparser.setup_parser(__doc__)
parser = customparser.CustomParser(
    description=__doc__,
    parents=[parent_parser],
)
parser.add_argument(
    '--question',
    required=True,
    action='store',
    dest='question',
    help='Question to ask',
)

parser.add_argument(
    '--picker',
    required=False,
    action='store',
    default=None,
    dest='picker',
    help='Which parsed query to pick, only needed if parsed queries do not '
    'match lower cased input query - supply -1 to force a list of query '
    'matches',
)

args = parser.parse_args()
swargs = args.__dict__
qkeys = ['picker', 'question']
qargs = {k: swargs.pop(k) for k in qkeys}
sw = tanwrap.SoapWrap(**swargs)
print sw
response = sw.ask_parsed_question(**qargs)
# need file arg, and dir arg
# response.write_csv_file()
