#!/usr/bin/env python -i
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '3.0.0'

import os
import sys
sys.dont_write_bytecode = True
my_filepath = os.path.abspath(sys.argv[0])
my_file = os.path.basename(my_filepath)
my_name = os.path.splitext(my_file)[0]
my_dir = os.path.dirname(my_filepath)
parent_dir = os.path.dirname(my_dir)
path_adds = [parent_dir]
[sys.path.insert(0, aa) for aa in path_adds if aa not in sys.path]

import pytan  # noqa
i = "pytan.shell.{}".format(my_name)
__import__(i)
module = eval(i)
worker = module.Worker()

if __name__ == "__main__":
    version_check = worker.version_check(__version__)
    console = worker.interactive_check()
    check = worker.check()
    setup = worker.setup()
    args = worker.parse_args()
    handler = worker.get_handler()
    result = worker.get_result()
    exec(worker.get_exec())


# from pytan.utils import taniumpy
# from pytan.utils import constants
# from pytan import utils  # noqa


"""

s1 = "Computer Name"
s2 = "Action Statuses"

result = get_sensors()
assert(len(result) == 530)

search = [{'value': s1, 'field': "name"}, {'value': s2, 'field': "name"}]
result = get_sensors(search=search)
assert(len(result) == 2)

search = s1
result = get_sensors(search=search)
assert(len(result) == 1)

search = [s1, s2]
result = get_sensors(search=search)
assert(len(result) == 2)

search = {"value": s1}
result = get_sensors(search=search)
assert(len(result) == 1)

search = {"value": s1, "operator": "EQUALS"}
result = get_sensors(search=search)
assert(len(result) == 1)

search = {"value": s1, "operator": "EQUAL"}
result = get_sensors(search=search)
assert(len(result) == 1)

search = {"value": "Name", "operator": "in"}
result = get_sensors(search=search)
assert(len(result) == 18)

search = {"value": ".*Name.*", "operator": "re"}
result = get_sensors(search=search)
assert(len(result) == 18)

search = 'x'
result = get_sensors(search=search)
assert(len(result) == 0)

search = [['x']]
try:
    result = get_sensors(search=search)
except Exception as e:
    print "this should fail: ", e

search = {"dievalue": s1}
try:
    result = get_sensors(search=search)
except Exception as e:
    print "this should fail: ", e

search = {"value": s1, 'field': 'die'}
try:
    result = get_sensors(search=search)
except Exception as e:
    print "this should fail: ", e

search = {"value": s1, "field": "name", "operator": "die"}
try:
    result = get_sensors(search=search)
except Exception as e:
    print "this should fail: ", e

search = {"value": s1, "field": "name", "not_flag": "die"}
try:
    result = get_sensors(search=search)
except Exception as e:
    print "this should fail: ", e

search = {"value": s1, "field": "name", "field_type": "die"}
try:
    result = get_sensors(search=search)
except Exception as e:
    print "this should fail: ", e

search = {"value": True}
try:
    result = get_sensors(search=search)
except Exception as e:
    print "this should fail: ", e

result = get_actions()
assert(len(result) == 6)

result = get_actions(search='6')
assert(len(result) == 1)

result = get_actions(search='Distribute Application Management Tools')
assert(len(result) == 2)

result = get_packages()
assert(len(result) == 50)

result = get_packages(search='1')
assert(len(result) == 1)

result = get_packages(search=['Update Java 64-bit - Kill / Reboot', '2'])
assert(len(result) == 2)
"""
