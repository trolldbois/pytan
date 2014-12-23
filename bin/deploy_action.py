#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Deploy an action and save the results as a report format'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '1.0.1'

import os
import sys
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
        'name': 'Print the help for package',
        'cmd': 'deploy_action.py $API_INFO --package-help',
        'tests': 'notexitcode',
    },
    {
        'name': 'Print the help for filters',
        'cmd': 'deploy_action.py $API_INFO --filters-help',
        'tests': 'notexitcode',
    },
    {
        'name': 'Print the help for options',
        'cmd': 'deploy_action.py $API_INFO --options-help',
        'tests': 'notexitcode',
    },
    {
        'name': 'Deploy an action example 1',
        'cmd': (
            'deploy_action.py $API_INFO --package "Distribute Tanium Standard Utilities" '
            '--file "$TMP/out.csv"'
        ),
        'notes': [
            'Deploys an action using the package Distribute Tanium Standard Utilities',
            'Since --run was not supplied, the results of the question for the filters '
            'of this action will be written to a CSV file for verification, and the deploy '
            'action will NOT be run'
        ],
        'precleanup': 'rm -f $TMP/VERIFY_BEFORE_DEPLOY_ACTION_out.csv',
        'file_exist': '$TMP/VERIFY_BEFORE_DEPLOY_ACTION_out.csv',
        'tests': 'notexitcode, file_exist_contents',
    },
    {
        'name': 'Deploy an action example 2',
        'cmd': (
            'deploy_action.py $API_INFO --package "Distribute Tanium Standard Utilities" '
            '--run --file "$TMP/out.csv"'
        ),
        'notes': ['Deploys an action using the package Distribute Tanium Standard Utilities'],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Deploy an action example 3',
        'cmd': (
            'deploy_action.py $API_INFO '
            '--package "Custom Tagging - Add Tags{\\$1=new_tag}" '
            '--filter "Operating System, that contains:Windows" '
            '--run --file "$TMP/out.csv"'
        ),
        'notes': [
            'Deploys an action using the package "Custom Tagging - Add Tags", passing in a '
            'parameter for the tag to be added',
            'Uses a filter to only deploy the action agains machines that match .*Windows.* '
            'for the Operating System sensor',
        ],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
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
    parser = utils.setup_deploy_action_argparser(__doc__)

    args = parser.parse_args()
    all_args = args.__dict__

    handler = process_handler_args(parser, all_args)

    d_opts = [
        'package', 'action_filters', 'action_options', 'run', 'report_file', 'report_dir',
        'start_seconds_from_now', 'expire_seconds', 'get_results',
        'package_help', 'filters_help', 'options_help',
    ]
    report_dir = all_args.get('report_dir', '')
    report_file = all_args.get('report_file', '')
    if not report_file:
        prefix = 'deploy_action_'
    else:
        prefix = ''

    d_args = {k: all_args.pop(k) for k in d_opts}

    print "++ Deploying action:\n{}".format(utils.jsonify(d_args))
    try:
        ret = handler.deploy_action_human(**d_args)
    except Exception as e:
        print e
        sys.exit(99)

    print "++ Deployed Action {!r} ID: {!r}".format(
        ret['action_object'].name, ret['action_object'].id
    )
    print "++ Command used in Action: {!r}".format(
        ret['action_object'].package_spec.command
    )

    if ret['action_progress_human']:
        print "++ Deploy action progress check results:"
        print ret['action_progress_human']

    if ret['action_results']:
        try:
            report_file, result = handler.export_to_report_file(
                report_dir=report_dir,
                report_file=report_file,
                obj=ret['action_results'],
                export_format='csv',
                prefix=prefix,
                **all_args
            )
            m = "++ Deploy results written to {!r} with {} bytes".format
            print(m(report_file, len(result)))
        except Exception as e:
            print e
            sys.exit(99)
    else:
        print (
            "++ No action results returned, run get_results.py to get the results"
        )
