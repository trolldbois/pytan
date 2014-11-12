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

# session = api.Session('172.16.31.128', 444)
# session.authenticate('Tanium User', 'T@n!um')

# for x in dir(pytan.api):
#     try:
#         t = getattr(pytan.api, x)()
#     except:
#         print "UNABLE TO INSTANTIATE pytan.api.", x
#         continue
#     try:
#         r = handler.session.find(t)
#         print "RETURN FROM 'findall' on %s == %s len:%s" % (x, r, len(str(r)))
#     except Exception as e:
#         print "EXCEPTION FROM 'findall' on: ", x, e

#     try:
#         t.id = 1
#     except:
#         continue
#     try:
#         r = handler.session.find(t)
#         print "RETURN FROM 'findsingle' on %s == %s len:%s" % (x, r, len(str(r)))
#     except Exception as e:
#         print "EXCEPTION FROM 'findsingle' on: ", x, e
#         continue
