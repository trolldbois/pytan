#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Provides the ability to find all sensors that reference a given set of strings in their scripts, and all saved actions that reference those same sensors'''
__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '2.1.6'

# change me to the location of PyTan!
pytan_loc = '~/gh/pytan'

# modify me for the list of string matches
match_strings = [
    "ldap://",
]

import os
import sys

sys.dont_write_bytecode = True
sys.path.append(os.path.join(os.path.expanduser(pytan_loc), 'lib'))

my_file = os.path.abspath(sys.argv[0])
my_name = os.path.splitext(os.path.basename(my_file))[0]
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]
[sys.path.append(aa) for aa in path_adds if aa not in sys.path]

import pytan
import pytan.binsupport

if __name__ == "__main__":
    pytan.binsupport.version_check(reqver=__version__)

    setupmethod = getattr(pytan.binsupport, 'setup_pytan_shell_argparser')
    responsemethod = getattr(pytan.binsupport, 'process_pytan_shell_args')

    parser = setupmethod(doc=__doc__)
    args = parser.parse_args()

    handler = pytan.binsupport.process_handler_args(parser=parser, args=args)
    response = responsemethod(parser=parser, handler=handler, args=args)

    all_sensors = handler.get_all('sensor', include_hidden_flag=1)
    matched_sensors = [
        x
        for x in all_sensors
        for y in x.queries
        for z in match_strings
        if z.lower() in y.script.lower()
    ]

    m = "Found {} sensors that reference any of these strings: {}".format
    print m(len(matched_sensors), ', '.join(match_strings))

    for x in matched_sensors:
        m = "Matched Sensor -- ID: {}, Name: {}".format
        print m(x.id, x.name)

    all_saved_actions = handler.get_all('saved_action', include_hidden_flag=1)
