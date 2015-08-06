#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Prints sensor information to stdout'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '2.0.0'

import os
import sys
import json
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
        'name': 'Print the server info',
        'cmd': 'print_server_info.py $API_INFO',
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
    parser = utils.setup_get_object_argparser('sensor', __doc__)
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument(
        '--category',
        required=False,
        default=[],
        action='append',
        dest='categories',
        help='Only show sensors in given category',
    )
    output_group.add_argument(
        '--platform',
        required=False,
        default=[],
        action='append',
        dest='platforms',
        help='Only show sensors for given platform',
    )
    output_group.add_argument(
        '--hide_params',
        required=False,
        default=False,
        action='store_true',
        dest='hide_params',
        help='Do not show parameters in output',
    )
    output_group.add_argument(
        '--params_only',
        required=False,
        default=False,
        action='store_true',
        dest='params_only',
        help='Only show sensors with parameters',
    )
    output_group.add_argument(
        '--json',
        required=False,
        default=False,
        action='store_true',
        dest='json',
        help='Show a json dump of the server information',
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

    response = utils.process_get_object_args(
        parser, handler, 'sensor', all_args
    )

    # filter out all sensors that have a source_id (i.e. are created as temp sensors for params)
    response = [x for x in response if not x.source_id]

    if args.json:
        for x in response:
            result = handler.export_obj(x, 'json')
            print "{}:\n{}".format(x, result)
        sys.exit()

    for x in sorted(response, key=lambda x: x.category):
        if args.categories:
            if str(x.category).lower() not in [y.lower() for y in args.categories]:
                continue

        platforms = [
            q.platform for q in x.queries
            if q.script
            and 'THIS IS A STUB' not in q.script
            and 'echo Windows Only' not in q.script
            and 'Not a Windows Sensor' not in q.script
        ]

        if args.platforms:
            match = [
                p for p in platforms
                if p.lower() in [y.lower() for y in args.platforms]
            ]
            if not match:
                continue

        param_def = x.parameter_definition or {}
        if param_def:
            try:
                param_def = json.loads(param_def)
            except:
                print "Error loading JSON parameter definition {}".format(param_def)
                param_def = {}

        params = param_def.get('parameters', [])
        if args.params_only and not params:
            continue

        desc = (x.description or '').replace('\n', ' ').strip()
        print (
            "\n  * Sensor Name: '{0.name}', Platforms: {1}, Category: {0.category}"
        ).format(x, ', '.join(platforms))
        print "  * Description: {}".format(desc)

        if args.hide_params:
            continue

        skip_attrs = [
            'model',
            'parameterType',
            'snapInterval',
            'validationExpressions',
            'key',
        ]

        for param in params:
            print "  * Parameter '{}':".format(param['key'])
            for k, v in sorted(param.iteritems()):
                if k in skip_attrs:
                    continue
                if not v:
                    continue
                print "    - '{}': {}".format(k, v)
