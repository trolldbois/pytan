#!/usr/bin/env python -i
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Provides an interactive console with pytan available as handler'''
__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '2.1.5'

import os
import sys
sys.dont_write_bytecode = True

# change me to the location of PyTan!
pytan_loc = '~/gh/pytan'
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

# List your sensors here that are exact name matches for sensors that should not be deleted
KEEP_LIST = [
    'Folder Exists',
]

# List your sensor categories that are exact matches for sensor categories that should not be deleted
KEEP_CATEGORIES = [
    'Reserved',
]

# Set this to True to actually delete, set to False to just report on what would be deleted
ACTUALLY_DELETE = False

if __name__ == "__main__":
    pytan.binsupport.version_check(reqver=__version__)

    setupmethod = getattr(pytan.binsupport, 'setup_pytan_shell_argparser')
    parser = setupmethod(doc=__doc__)
    args = parser.parse_args()

    handler = pytan.binsupport.process_handler_args(parser=parser, args=args)

    all_sensors = handler.get_all('sensor', include_hidden_flag=1)
    print "-- {} sensors in total".format(len(all_sensors))

    to_be_deleted = [
        x for x in all_sensors
        if x.name not in KEEP_LIST
        and x.category not in KEEP_CATEGORIES
    ]
    print "-- {} sensors to be deleted".format(len(to_be_deleted))

    for s in to_be_deleted:
        print "!! Sensor ID {s.id!r}, name: {s.name!r} to be deleted!".format(s=s)
        if ACTUALLY_DELETE:
            handler.session.delete(s)
            print "-- Sensor ID {s.id!r}, name: {s.name!r} deleted!".format(s=s)
