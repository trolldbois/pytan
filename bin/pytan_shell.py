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
from pytan import constants

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

for k in constants.GET_OBJ_MAP:
    r = handler.get_all(k)
    print 'all: ', k, r
    if len(r) == 0:
        raise Exception("{} is 0 !!!".format(len(r)))
    if 'id' not in constants.GET_OBJ_MAP[k]['search']:
        continue
    try:
        r = handler.get(k, id=999999)
    except Exception as e:
        print "single get bad id=99999: {}".format(k), str(e).replace('\n', '')

    r = handler.get(k, id=1)
    print 'single id=1: ', k, r
    if len(r) != 1:
        raise Exception("{} != 1 !!!".format(len(r)))
    r = handler.get(k, id=[1, 2])
    print 'multi id=[1,2]: ', k, r
    if len(r) != 2:
        raise Exception("{} != 2 !!!".format(len(r)))

k = 'sensor'
r = handler.get(k, id=[1, 2], name=['Computer Name', 'Operating System'])
print 'many multi id=[1,2] name=Computer Name, Operating System: ', k, r
if len(r) != 4:
    raise Exception("{} != 4 !!!".format(len(r)))



# # Example scenario:
# r = handler.ask_manual_question(
#     sensors=[
#         "Computer Name",
#         "Folder Name Search with RegEx Match[Program Files,.*,No,No], "
#         "that is .*, opt:max_data_age:3600",
#     ],
#     question_filters=[
#         "Operating System, that contains Windows",
#         "Operating System, that does not contain Windows",
#     ],
#     question_options=["ignore_case", "or"],
# )
# print r
# print r.request
