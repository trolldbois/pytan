#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Deploy an action and save the results as a report format'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '0.8.0'

import os
import sys

sys.dont_write_bytecode = True
my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
path_adds = [parent_dir]

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
parser = utils.setup_deploy_action_argparser(__doc__)

args = parser.parse_args()
all_args = args.__dict__

handler = process_handler_args(parser, all_args)

d_opts = [
    'package', 'action_filters', 'action_options', 'run', 'report_dir',
    'start_seconds_from_now', 'expire_seconds', 'get_results',
]

d_args = {k: all_args.pop(k) for k in d_opts}

print "++ Deploying action:\n{}".format(utils.jsonify(d_args))
ret = handler.deploy_action_human(**d_args)

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
    report_file, result = handler.export_to_report_file(
        obj=ret['action_results'],
        export_format='csv',
        prefix='deploy_action_',
        **all_args
    )
    m = "++ Deploy results written to {!r} with {} bytes".format
    print(m(report_file, len(result)))
else:
    print (
        "++ No action results returned, run get_results.py to get the results"
    )
