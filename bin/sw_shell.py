#!/usr/bin/env python -i
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''This is used to get an interactive console with SoapWrap available as sw

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
import SoapUtil
import SoapWrap
from console_support import *

SoapUtil.version_check(__version__)
parent_parser = customparser.setup_parser(__doc__)
parser = customparser.CustomParser(
    description=__doc__,
    parents=[parent_parser],
)

args = parser.parse_args()
swargs = args.__dict__
sw = SoapWrap.SoapWrap(**swargs)
st = SoapWrap.SoapTransform()
if swargs['loglevel'] >= 10:
    SoapUtil.set_all_loglevels()

print ("%s -- now available as 'sw'!" % sw)
print ("%s -- now available as 'st'!" % st)
