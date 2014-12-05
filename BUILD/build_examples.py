#!/usr/bin/env python -i
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''generates all of the examples for doc from the test/ddt JSON files'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '1.0.0'

import os
import sys
import json

sys.dont_write_bytecode = True
my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

# import pytan
from pytan import utils

utils.version_check(__version__)

test_dir = os.path.join(parent_dir, 'test')
ddt_dir = os.path.join(test_dir, 'ddt')

get_object_ddt = os.path.join(ddt_dir, 'ddt_valid_get_object.json')
question_object_ddt = os.path.join(ddt_dir, 'ddt_valid_questions.json')
api_info_py = os.path.join(test_dir, 'API_INFO.py')


def read_file(f):
    with open(get_object_ddt) as fh:
        out = fh.read()
    return out


def json_read(f):
    return json.loads(read_file(f))


question_objects = json_read(question_object_ddt)
get_objects = json_read(get_object_ddt)
api_info = read_file(api_info_py)
