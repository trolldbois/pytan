#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Create a group object from command line arguments'''
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

examples = [
    {
        'name': 'Print the help for filters',
        'cmd': 'create_group.py $API_INFO --filters-help',
        'tests': 'notexitcode',
    },
    {
        'name': 'Print the help for options',
        'cmd': 'create_group.py $API_INFO --options-help',
        'tests': 'notexitcode',
    },
    {
        'name': 'Create a new group',
        'cmd': (
            'create_group.py $API_INFO --name "All Windows Computers CMDLINE TEST GROUP" '
            '-f "Operating System, that contains:Windows" '
            '-f "IP Address, that not equals:10.10.10.10" '
            '-o "and" -o "ignore_case"'
        ),
        'notes': [
            'Create a group named All Windows Computers CMDLINE TEST GROUP',
            'Supply a filter that limits the group members to machines that match '
            '.*Windows.* for the Operating System sensor',
            'Supply a filter that limits the group members to machines that do not equal '
            '10.10.10.10 for the IP Address sensor',
            'Supply two options, one to AND the filters supplied, and another '
            'to ignore the case while matching the filters',
        ],
        'tests': 'exitcode',
    },
    {
        'name': 'Delete the recently created group',
        'cmd': (
            'delete_group.py $API_INFO --name "All Windows Computers CMDLINE TEST GROUP" '
        ),
        'notes': [
            'Delete the group named All Windows Computers CMDLINE TEST GROUP',
        ],
        'tests': 'exitcode',
    },
]


def process_handler_args(parser, all_args):
    handler_grp_names = ['Handler Authentication', 'Handler Options']
    handler_opts = utils.get_grp_opts(parser, handler_grp_names)
    handler_args = {k: all_args.pop(k) for k in handler_opts}

    h = pytan.Handler(**handler_args)
    print str(h)
    return h


if __name__ == "__main__":

    utils.version_check(__version__)
    parser = utils.setup_parser(__doc__, True)
    arggroup = parser.add_argument_group('Create Group Options')

    arggroup.add_argument(
        '-n',
        '--name',
        required=True,
        action='store',
        dest='name',
        default=None,
        help='Name of group to create',
    )

    arggroup.add_argument(
        '-f',
        '--filter',
        required=False,
        action='append',
        dest='filters',
        default=[],
        help='Filters to use for group, supply --filters-help to see filter help',
    )

    arggroup.add_argument(
        '-o',
        '--option',
        required=False,
        action='append',
        dest='filter_options',
        default=[],
        help='Filter options to use for group, supply --options-help to see options'
        ' help',
    )

    arggroup.add_argument(
        '--filters-help',
        required=False,
        action='store_true',
        default=False,
        dest='filters_help',
        help='Get the full help for filters strings',
    )

    arggroup.add_argument(
        '--options-help',
        required=False,
        action='store_true',
        default=False,
        dest='options_help',
        help='Get the full help for options strings',
    )

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
        group_obj = handler.create_group(
            groupname=args.name,
            filters=args.filters,
            filter_options=args.filter_options,
            filters_help=args.filters_help,
            options_help=args.options_help,
        )
        m = "New group {!r} created with ID {!r}, filter text: {!r}".format
        print(m(group_obj.name, group_obj.id, group_obj.text))
    except Exception as e:
        print e
        sys.exit(99)
