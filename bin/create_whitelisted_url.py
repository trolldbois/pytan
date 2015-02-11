#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Create a Whitelisted URL object from command line arguments'''
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
from random import randint

examples = [
    {
        'name': 'Create a whitelisted URL',
        'cmd': (
            'create_whitelisted_url.py $API_INFO '
            '--url "https://testing.com/{}" '
            '--regex '
            '--download 3600 '
            '--property "property name" "property value"'
        ).format(randint(1, 9999)),
        'notes': [
            'Create a whitelisted_url for https://testing.com',
            'Set the new URL as a regex pattern',
            'Set thew new URL to be re-downloaded every 3600 seconds'
            'Create a property named property name with the value property value on the new URL',
        ],
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
    parser = utils.setup_parser(__doc__, True)
    arggroup = parser.add_argument_group('Create Whitelisted URL Options')

    arggroup.add_argument(
        '--url',
        required=True,
        action='store',
        dest='url',
        default=None,
        help='Text of new Whitelisted URL',
    )

    arggroup.add_argument(
        '--regex',
        required=False,
        action='store_true',
        dest='regex',
        default=False,
        help='Whitelisted URL is a regex pattern',
    )

    arggroup.add_argument(
        '-d',
        '--download',
        required=False,
        action='store',
        dest='download_seconds',
        type=int,
        default=86400,
        help='Download Whitelisted URL every N seconds',
    )

    arggroup.add_argument(
        '-prop',
        '--property',
        required=False,
        action='append',
        dest='properties',
        nargs=2,
        default=[],
        help='Property name and value to assign to Whitelisted URL',
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
        url_obj = handler.create_whitelisted_url(
            url=args.url,
            regex=args.regex,
            download_seconds=args.download_seconds,
            properties=args.properties,
        )

        m = "New Whitelisted URL {!r} created with ID {!r}".format
        print(m(url_obj.url_regex, url_obj.id))
    except Exception as e:
        print e
        sys.exit(99)
