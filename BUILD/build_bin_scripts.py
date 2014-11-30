#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Build the bin/ scripts'''
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

from pytan import utils
from pytan import constants

utils.version_check(__version__)

build_bin = os.path.join(my_dir, 'build_bin')
output_bin = os.path.join(parent_dir, 'bin')

go_f = os.path.join(build_bin, 'get_object_template.py')
go_s = open(go_f).read()

for i in constants.GET_OBJ_MAP:
    i_f = os.path.join(output_bin, 'get_{}.py'.format(i))
    i_h = open(i_f, 'w')
    i_h.write(go_s.replace('OBJECTNAME', i))
    i_h.close()
    os.chmod(i_f, 0755)
    print "Generated {} from {}".format(i_f, go_f)

do_f = os.path.join(build_bin, 'delete_object_template.py')
do_s = open(do_f).read()

for i in constants.GET_OBJ_MAP:
    if not constants.GET_OBJ_MAP[i]['delete']:
        continue
    i_f = os.path.join(output_bin, 'delete_{}.py'.format(i))
    i_h = open(i_f, 'w')
    i_h.write(do_s.replace('OBJECTNAME', i))
    i_h.close()
    os.chmod(i_f, 0755)
    print "Generated {} from {}".format(i_f, do_f)
