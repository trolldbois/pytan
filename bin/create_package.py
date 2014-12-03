#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Create a package object from command line arguments'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '1.0.0'

import os
import sys
sys.dont_write_bytecode = True
my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

import pytan
from pytan import utils


def process_handler_args(parser, all_args):
    handler_grp_names = ['Handler Authentication', 'Handler Options']
    handler_opts = utils.get_grp_opts(parser, handler_grp_names)
    handler_args = {k: all_args.pop(k) for k in handler_opts}

    h = pytan.Handler(**handler_args)
    print str(h)
    return h


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
    ', supply --filter-help to see filter help',
)

arggroup.add_argument(
    '-vo',
    '--verify-option',
    required=False,
    action='append',
    dest='verify_filter_options',
    default=[],
    help='Options to use for the verify filters, supply --option-help to see '
    'options help',
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
handler = process_handler_args(parser, all_args)

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
)

m = "New package {!r} created with ID {!r}, command: {!r}".format
print(m(package_obj.name, package_obj.id, package_obj.command))
