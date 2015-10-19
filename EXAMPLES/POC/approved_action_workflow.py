#!/usr/bin/env python -i
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Provides an example workflow for how to deploy actions when require_action_approval == 1'''
__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '2.1.7'

pytan_loc = '~/gh/pytan'

import os
import sys

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

import time
import logging


@pytan.utils.func_timing
def wait_for_new_action(saved_action_id):
    while True:
        # re-fetch the saved action in order to get the updated last_action attribute
        saved_action = handler.get('saved_action', id=saved_action_id)[0]
        # fetch the full object of the last action created by the saved action
        full_action_object = handler.get('action', id=saved_action.last_action.id)[0]
        if full_action_object.status != 'Pending':
            print 'DEBUG: new action created by saved_action: {}'.format(full_action_object)
            return full_action_object
        print 'DEBUG: action is still in Pending status, new action not yet created: {} / {}'.format(full_action_object, full_action_object.status)
        time.sleep(1)


if __name__ == "__main__":
    pytan.binsupport.version_check(reqver=__version__)

    setupmethod = getattr(pytan.binsupport, 'setup_pytan_shell_argparser')
    responsemethod = getattr(pytan.binsupport, 'process_pytan_shell_args')

    parser = setupmethod(doc=__doc__)
    args = parser.parse_args()

    handler = pytan.binsupport.process_handler_args(parser=parser, args=args)
    response = responsemethod(parser=parser, handler=handler, args=args)

    # bump log level up to 2 so we can see poller timing logs
    pytan.utils.set_log_levels(loglevel=2)

    # enable timing logger for func_timing:
    logging.getLogger('pytan.handler.timing').setLevel(getattr(logging, 'DEBUG'))

    # establish a package name with params
    pkg_name = "Custom Tagging - Add Tags{$1=\{test\}}"

    # deploy the action with that package but set get_results to False so that it immediately returns and does not poll the action that is created by the saved action that will always be in Pending status
    deployed_action = handler.deploy_action(package=pkg_name, run=True, get_results=False)

    # get the action_object that was created by the platform on behalf of the saved_action, which should have a status of 'Pending' due to require_action_approval = 1
    pending_action_obj = deployed_action['action_object']

    # prove that the action created by the saved action before approval is "Pending"
    print "DEBUG: action created by platform: {}, status: {}".format(pending_action_obj.id, pending_action_obj.status)

    # get the saved_action_object that was created by the platform
    unapproved_saved_action = deployed_action['saved_action_object']

    # prove that the saved_action created by the platform is not yet approved
    print "DEBUG: saved_action approved_flag before approval: {}".format(unapproved_saved_action.approved_flag)

    # approve the saved action
    saved_action_approval = handler.approve_saved_action(id=unapproved_saved_action.id)

    # prove that the saved_action created by the platform is now approved
    print "DEBUG: saved_action approved_flag after approval: {}".format(saved_action_approval.approved_flag)

    # wait for the saved action to create a new action after approval
    full_running_action_obj = wait_for_new_action(unapproved_saved_action.id)

    # create an Action Poller for the new action
    poller = pytan.pollers.ActionPoller(handler=handler, obj=full_running_action_obj)

    # run the poller
    poller.run()
