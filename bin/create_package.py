#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Create a package object from command line arguments'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '1.0.3'

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
        'cmd': 'create_package.py $API_INFO --filters-help',
        'tests': 'notexitcode',
    },
    {
        'name': 'Print the help for options',
        'cmd': 'create_package.py $API_INFO --options-help',
        'tests': 'notexitcode',
    },
    {
        'name': 'Create a new package',
        'cmd': (
            'create_package.py $API_INFO '
            '--name "1234 CMDLINE TEST package" '
            '--display-name "1234 CMDLINE TEST package display name" '
            '--command "testing.vbs \\$1 \\$2 \\$3 \\$4 \\$5 \\$6 \\$7 \\$8" '
            '--expire-seconds 1500 '
            '--file-url "3600::testing.vbs||https://testing.com/testing.vbs" '
            '--file-url "https://testing.com/another_testing.vbs" '
            '--parameters-file "{}/doc/example_of_all_package_parameters.json" '
            '--verify-expire-seconds 3600 '
            '--verify-filter "Custom Tags, that contains:tag" '
            '--verify-option "ignore_case" '
            '--command-timeout 600 '
        ).format(parent_dir),
        'notes': [
            'Create a package named 1234 CMDLINE TEST package',
            'Set the display name in the console for the new '
            'package to 1234 CMDLINE TEST package display name',
            'When this package is deployed, run the command testing.vbs and expect 8 arguments',
            'When this package is deployed as part of an action, default the action to expire '
            'after 3600 seconds',
            'Add a file to this package that will be redownloaded every 3600 seconds, named '
            'testing.vbs in Tanium, and downloaded from testing.com/testing.vbs',
            'Add another file to this package that will be downloaded once, '
            'extract the file name from the URL, and downloaded from '
            'testing.com/another_testing.vbs',
            'Add all the parameters defined in doc/example_of_all_package_parameters.json',
            'Expire the verification filter after 3600 seconds',
            'Expire the command if it takes longer than 600 seconds to run',
            'Supply a verification filter that will be used when this package is deployed as part '
            'of an action',
            'Supply an option for the verification filter that ignores case',
        ],
        'tests': 'exitcode',
    },
    {
        'name': 'Delete the recently created package',
        'cmd': (
            'delete_package.py $API_INFO --name "1234 CMDLINE TEST package" '
        ),
        'notes': [
            'Delete the package named 1234 CMDLINE TEST package',
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
    arggroup = parser.add_argument_group('Create Package Options')

    arggroup.add_argument(
        '-n',
        '--name',
        required=True,
        action='store',
        dest='name',
        default=None,
        help='Name of package to create',
    )

    arggroup.add_argument(
        '-c',
        '--command',
        required=True,
        action='store',
        dest='command',
        default='',
        help='Command to execute with package',
    )

    arggroup.add_argument(
        '-d',
        '--display-name',
        required=False,
        action='store',
        dest='display_name',
        default='',
        help='Display name of package',
    )

    arggroup.add_argument(
        '--command-timeout',
        required=False,
        action='store',
        dest='command_timeout_seconds',
        type=int,
        default=600,
        help='Command for this package timeout in N seconds',
    )

    arggroup.add_argument(
        '--expire-seconds',
        required=False,
        action='store',
        dest='expire_seconds',
        type=int,
        default=600,
        help='Expire actions created for this package in N seconds',
    )

    arggroup.add_argument(
        '-f',
        '--file-url',
        required=False,
        action='store',
        dest='file_urls',
        default=[],
        help='URL of file to include with package, can specify any of the '
        'following: "$url", or "$download_seconds::$url", or "$filename||$url",'
        ' or "$filename||$download_seconds::$url"',
    )

    arggroup.add_argument(
        '--parameters-file',
        required=False,
        action='store',
        dest='parameters_json_file',
        default='',
        help='JSON file describing parameters for this package, see '
        'doc/example_of_all_package_parameters.json for an example',
    )
    arggroup.add_argument(
        '-vf',
        '--verify-filter',
        required=False,
        action='append',
        dest='verify_filters',
        default=[],
        help='Filters to use for verifying the package after it is deployed, '
        ', supply --filters-help to see filter help',
    )

    arggroup.add_argument(
        '-vo',
        '--verify-option',
        required=False,
        action='append',
        dest='verify_filter_options',
        default=[],
        help='Options to use for the verify filters, supply --options-help to see '
        'options help',
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

    arggroup.add_argument(
        '--verify-expire-seconds',
        required=False,
        action='store',
        dest='verify_expire_seconds',
        type=int,
        default=600,
        help='Expire the verify filters used by this package in N seconds',
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
        package_obj = handler.create_package(
            name=args.name,
            command=args.command,
            display_name=args.display_name,
            file_urls=args.file_urls,
            command_timeout_seconds=args.command_timeout_seconds,
            expire_seconds=args.expire_seconds,
            parameters_json_file=args.parameters_json_file,
            verify_filters=args.verify_filters,
            verify_filter_options=args.verify_filter_options,
            verify_expire_seconds=args.verify_expire_seconds,
            filters_help=args.filters_help,
            options_help=args.options_help,
        )

        m = "New package {!r} created with ID {!r}, command: {!r}".format
        print(m(package_obj.name, package_obj.id, package_obj.command))
    except Exception as e:
        print e
        sys.exit(99)
