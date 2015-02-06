#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Create a OBJECTNAME object from a json file'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '1.0.2'


import os
import sys
import getpass
sys.dont_write_bytecode = True
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

import pytan
from pytan import utils

from random import randint

examples = [
    {
        'name': 'Export OBJECTNAME id 1 as JSON',
        'cmd': 'get_OBJECTNAME.py $API_INFO --id 1 --file "$TMP/out.json" json',
        'notes': ['Get the first OBJECTNAME object', 'Save the results to a JSON file'],
        'precleanup': 'rm -f $TMP/out.json',
        'file_exist': '$TMP/out.json',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Change name or url_regex in the JSON',
        'cmd': (
            """perl -p -i -e 's/^(      "(name|url_regex)": ".*)"/$1 CMDLINE TEST {}"/gm'"""
            """ $TMP/out.json && cat $TMP/out.json""".format(randint(1, 9999))
        ),
        'notes': ['Add CMDLINE TEST to name or url_regex in the JSON file'],
        'file_exist': '$TMP/out.json',
        'tests': 'exitcode, file_exist',
    },
    {
        'name': 'Create a new OBJECTNAME from the modified JSON file',
        'cmd': 'create_OBJECTNAME_from_json.py $API_INFO -j "$TMP/out.json"',
        'precleanup': 'rm -f $TMP/create.out',
        'tests': 'exitcode',
    },

]


def process_handler_args(parser, all_args):
    handler_grp_names = ['Handler Authentication', 'Handler Options']
    handler_opts = utils.get_grp_opts(parser, handler_grp_names)
    handler_args = {k: all_args.pop(k) for k in handler_opts}

    try:
        h = pytan.Handler(**handler_args)
        print str(h)
    except Exception as e:
        print e
        sys.exit(99)
    return h


if __name__ == "__main__":
    utils.version_check(__version__)
    parser = utils.setup_create_json_object_argparser('OBJECTNAME', __doc__)
    args = parser.parse_args()
    all_args = args.__dict__

    if not args.username:
        username = raw_input('Tanium Username: ')
        all_args['username'] = username.strip()

    if not args.password:
        password = getpass.getpass('Tanium Password: ')
        all_args['password'] = password.strip()

    if not args.host:
        host = raw_input('Tanium Host: ')
        all_args['host'] = host.strip()

    handler = process_handler_args(parser, all_args)

    try:
        response = utils.process_create_json_object_args(
            parser, handler, 'OBJECTNAME', all_args
        )
    except Exception as e:
        print e
        sys.exit(99)
