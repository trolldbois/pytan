#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Build the bin/ scripts'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '0.8.0'

import os
import sys
import glob

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

template_dir = os.path.join(my_dir, 'TEMPLATES')
output_bin = os.path.join(parent_dir, 'bin')
output_winbin = os.path.join(parent_dir, 'winbin')

print "## Generating bin/get_object scripts"
go_f = os.path.join(template_dir, 'get_object_template.py')
go_s = open(go_f).read()

for i in constants.GET_OBJ_MAP:
    i_f = os.path.join(output_bin, 'get_{}.py'.format(i))
    i_h = open(i_f, 'w')
    i_h.write(go_s.replace('OBJECTNAME', i))
    i_h.close()
    os.chmod(i_f, 0755)
    print "Generated {} from {}".format(i_f, go_f)

print "## Generating bin/delete_object scripts"
do_f = os.path.join(template_dir, 'delete_object_template.py')
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

print "## Generating bin/create_from_json scripts"
cjo_f = os.path.join(template_dir, 'create_object_from_json_template.py')
cjo_s = open(cjo_f).read()

for i in constants.GET_OBJ_MAP:
    if not constants.GET_OBJ_MAP[i]['create_json']:
        continue
    i_f = os.path.join(output_bin, 'create_{}_from_json.py'.format(i))
    i_h = open(i_f, 'w')
    i_h.write(cjo_s.replace('OBJECTNAME', i))
    i_h.close()
    os.chmod(i_f, 0755)
    print "Generated {} from {}".format(i_f, cjo_f)


print "## Generating winbin/ scripts"
wb_f = os.path.join(template_dir, 'TEMPLATE.bat')
wb_s = open(wb_f).read()
wbi_f = os.path.join(template_dir, 'IA_TEMPLATE.bat')
wbi_s = open(wbi_f).read()

for i in glob.glob(os.path.join(output_bin, '*.py')):
    bin_basename = os.path.basename(i)
    bin_filename, bin_ext = os.path.splitext(bin_basename)
    bin_contents = open(i).read()
    if '-i' in bin_contents.splitlines()[0]:
        bin_template_f = wbi_f
        bin_template = wbi_s
    else:
        bin_template_f = wb_f
        bin_template = wb_s
    i_f = os.path.join(output_winbin, bin_filename + '.bat')
    i_h = open(i_f, 'w')
    i_h.write(bin_template)
    i_h.close()
    os.chmod(i_f, 0755)
    print "Generated {} from {}".format(i_f, bin_template_f)
