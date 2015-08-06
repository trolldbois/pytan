#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Get client and save as report format'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '2.0.0'


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

examples = [
    {
        'name': 'Export all client as JSON',
        'cmd': 'get_client.py $API_INFO --all --file "$TMP/out.json" json',
        'notes': ['Get all client objects', 'Save the results to a JSON file'],
        'precleanup': 'rm -f $TMP/out.json',
        'file_exist': '$TMP/out.json',
        'tests': 'exitcode, file_exist',
    },
    {
        'name': 'Export all client as CSV',
        'cmd': 'get_client.py $API_INFO --all --file "$TMP/out.csv" csv',
        'notes': ['Get all client objects', 'Save the results to a csv file'],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist',
    },
    {
        'name': 'Export all client as xml',
        'cmd': 'get_client.py $API_INFO --all --file "$TMP/out.xml" xml',
        'notes': ['Get all client objects', 'Save the results to a xml file'],
        'precleanup': 'rm -f $TMP/out.xml',
        'file_exist': '$TMP/out.xml',
        'tests': 'exitcode, file_exist',
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
    parser = utils.setup_get_object_argparser('client', __doc__)
    parser = utils.add_get_object_report_argparser(parser)
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
        response = utils.process_get_object_args(
            parser, handler, 'client', all_args
        )
        report_file, result = handler.export_to_report_file(response, **all_args)
    except Exception as e:
        print e
        sys.exit(99)

    m = "Report file {!r} written with {} bytes".format
    print(m(report_file, len(result)))
