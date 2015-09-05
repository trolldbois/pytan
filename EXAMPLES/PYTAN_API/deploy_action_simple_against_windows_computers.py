#!/usr/bin/env python
"""
Deploy an action against only windows computers using human strings. This requires passing in an action filter
"""
# import the basic python packages we need
import os
import sys
import tempfile
import pprint
import traceback

# disable python from generating a .pyc file
sys.dont_write_bytecode = True

# change me to the path of pytan if this script is not running from EXAMPLES/PYTAN_API
pytan_loc = "~/gh/pytan"
pytan_static_path = os.path.join(os.path.expanduser(pytan_loc), 'lib')

# Determine our script name, script dir
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)

# try to automatically determine the pytan lib directory by assuming it is in '../../lib/'
parent_dir = os.path.dirname(my_dir)
pytan_root_dir = os.path.dirname(parent_dir)
lib_dir = os.path.join(pytan_root_dir, 'lib')

# add pytan_loc and lib_dir to the PYTHONPATH variable
path_adds = [lib_dir, pytan_static_path]
[sys.path.append(aa) for aa in path_adds if aa not in sys.path]

# import pytan
import pytan

# create a dictionary of arguments for the pytan handler
handler_args = {}

# establish our connection info for the Tanium Server
handler_args['username'] = "Administrator"
handler_args['password'] = "Tanium2015!"
handler_args['host'] = "10.0.1.240"
handler_args['port'] = "443"  # optional

# optional, level 0 is no output except warnings/errors
# level 1 through 12 are more and more verbose
handler_args['loglevel'] = 1

# optional, use a debug format for the logging output (uses two lines per log entry)
handler_args['debugformat'] = False

# optional, this saves all response objects to handler.session.ALL_REQUESTS_RESPONSES
# very useful for capturing the full exchange of XML requests and responses
handler_args['record_all_requests'] = True

# instantiate a handler using all of the arguments in the handler_args dictionary
print "...CALLING: pytan.handler() with args: {}".format(handler_args)
handler = pytan.Handler(**handler_args)

# print out the handler string
print "...OUTPUT: handler string: {}".format(handler)

# setup the arguments for the handler() class
kwargs = {}
kwargs["run"] = True
kwargs["action_filters"] = u'Operating System, that contains:Windows'
kwargs["package"] = u'Distribute Tanium Standard Utilities'

print "...CALLING: handler.deploy_action with args: {}".format(kwargs)
response = handler.deploy_action(**kwargs)

print "...OUTPUT: Type of response: ", type(response)

print "...OUTPUT: Pretty print of response:"
print pprint.pformat(response)

print "...OUTPUT: Print of action object: "
print response['action_object']

# if results were returned (i.e. get_results=True was one of the kwargs passed in):
if response['action_results']:
    # call the export_obj() method to convert response to CSV and store it in out
    export_kwargs = {}
    export_kwargs['obj'] = response['action_results']
    export_kwargs['export_format'] = 'csv'
    print "...CALLING: handler.export_obj() with args {}".format(export_kwargs)
    out = handler.export_obj(**export_kwargs)

    # trim the output if it is more than 15 lines long
    if len(out.splitlines()) > 15:
        out = out.splitlines()[0:15]
        out.append('..trimmed for brevity..')
        out = '\n'.join(out)

    print "...OUTPUT: CSV Results of response: "
    print out

'''STDOUT from running this:
...CALLING: pytan.handler() with args: {'username': 'Administrator', 'record_all_requests': True, 'loglevel': 1, 'debugformat': False, 'host': '10.0.1.240', 'password': 'Tanium2015!', 'port': '443'}
...OUTPUT: handler string: PyTan v2.1.0 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
...CALLING: handler.deploy_action with args: {'action_filters': u'Operating System, that contains:Windows', 'run': True, 'package': u'Distribute Tanium Standard Utilities'}
2015-09-05 05:29:50,224 INFO     pytan.pollers.QuestionPoller: ID 11616: Reached Threshold of 99% (2 of 2)
2015-09-05 05:30:05,464 INFO     pytan.pollers.ActionPoller: ID 617: Reached Threshold for Seen Count of 100% (1 of 1)
2015-09-05 05:30:10,514 INFO     pytan.pollers.ActionPoller: ID 617: Reached Threshold for Finished Count of 100% (1 of 1)
...OUTPUT: Type of response:  <type 'dict'>
...OUTPUT: Pretty print of response:
{'action_info': <taniumpy.object_types.result_info.ResultInfo object at 0x1122151d0>,
 'action_object': <taniumpy.object_types.action.Action object at 0x113644c10>,
 'action_result_map': {'failed': {'617:Expired.': [],
                                  '617:Failed.': [],
                                  '617:NotSucceeded.': [],
                                  '617:Stopped.': [],
                                  'total': 0},
                       'finished': {'617:Completed.': ['TPT1-0.localdomain'],
                                    '617:Expired.': [],
                                    '617:Failed.': [],
                                    '617:NotSucceeded.': [],
                                    '617:Stopped.': [],
                                    '617:Succeeded.': [],
                                    '617:Verified.': [],
                                    'total': 1},
                       'running': {'617:Copying.': [],
                                   '617:Downloading.': ['TPT1-0.localdomain'],
                                   '617:PendingVerification.': [],
                                   '617:Running.': [],
                                   '617:Waiting.': [],
                                   'total': 1},
                       'success': {'617:Completed.': ['TPT1-0.localdomain'],
                                   '617:Verified.': [],
                                   'total': 1},
                       'unknown': {'total': 0}},
 'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x124e279d0>,
 'group_object': <taniumpy.object_types.group.Group object at 0x110b9f750>,
 'package_object': <taniumpy.object_types.package_spec.PackageSpec object at 0x110b8dd50>,
 'poller_object': <pytan.pollers.ActionPoller object at 0x112215190>,
 'poller_success': True,
 'saved_action_object': <taniumpy.object_types.saved_action.SavedAction object at 0x110b8d590>}
...OUTPUT: Print of action object: 
Action, name: 'API Deploy Distribute Tanium Standard Utilities', id: 617
...CALLING: handler.export_obj() with args {'export_format': 'csv', 'obj': <taniumpy.object_types.result_set.ResultSet object at 0x124e279d0>}
...OUTPUT: CSV Results of response: 
Action Statuses,Computer Name
617:Completed.,TPT1-0.localdomain


'''

'''STDERR from running this:

'''
