#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Exports an action, its source package, and its temp package to json format for troubleshooting'''
__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '2.1.6'

# change me to the location of PyTan!
pytan_loc = '~/gh/pytan'

import os
import sys
import traceback

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

    parser = pytan.binsupport.setup_parent_parser(doc=__doc__)
    arggroup_name = 'Export Action Objects Options'
    get_object_group = parser.add_argument_group(arggroup_name)
    get_object_group.add_argument(
        '--id',
        required=True,
        action='append',
        default=[],
        dest='id',
        help='id of action to export objects for',
    )

    args = parser.parse_args()

    handler = pytan.binsupport.process_handler_args(parser=parser, args=args)

    try:
        action = handler.get('action', id=args.id)[0]
    except Exception as e:
        traceback.print_exc()
        print "\n\nError occurred: {}".format(e)
        sys.exit(100)

    e = handler.export_to_report_file(action, 'json')
    print "Found action: {}, exported to: {}".format(action, e[0])

    try:
        action_pkg = handler.get('package', id=action.package_spec.id, include_hidden_flag=1)[0]
    except Exception as e:
        traceback.print_exc()
        print "\n\nError occurred: {}".format(e)
        sys.exit(100)

    e = handler.export_to_report_file(action_pkg, 'json')
    print "Found package for action: {}, exported to: {}".format(action_pkg, e[0])
