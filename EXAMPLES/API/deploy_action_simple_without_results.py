
"""
Deploy an action against all computers using human strings, but do not get the completed results of the job -- return right away with the deploy action object.
"""

import os
import sys
sys.dont_write_bytecode = True

# Determine our script name, script dir
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)

# determine the pytan lib dir and add it to the path
parent_dir = os.path.dirname(my_dir)
pytan_root_dir = os.path.dirname(parent_dir)
lib_dir = os.path.join(pytan_root_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)


# connection info for Tanium Server
USERNAME = "Tanium User"
PASSWORD = "T@n!um"
HOST = "172.16.31.128"
PORT = "443"

# Logging conrols
LOGLEVEL = 2
DEBUGFORMAT = False

import tempfile

import pytan
handler = pytan.Handler(
    username=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    loglevel=LOGLEVEL,
    debugformat=DEBUGFORMAT,
)

print handler

# setup the arguments for the handler method
kwargs = {}
kwargs["get_results"] = False
kwargs["run"] = True
kwargs["package"] = u'Distribute Tanium Standard Utilities'

# call the handler with the deploy_action method, passing in kwargs for arguments
response = handler.deploy_action(**kwargs)
import pprint, io

print ""
print "Type of response: ", type(response)

print ""
print "Pretty print of response:"
print pprint.pformat(response)

print ""
print "Print of action object: "
print response['action_object']

# create an IO stream to store CSV results to
out = io.BytesIO()

# if results were returned (i.e. get_results=True was one of the kwargs passed in):
if response['action_results']:
    # call the write_csv() method to convert response to CSV and store it in out
    response['action_results'].write_csv(out, response['action_results'])

    print ""
    print "CSV Results of response: "
    print out.getvalue()



'''Output from running this:
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
2015-08-07 19:45:28,497 DEBUG    pytan.handler.ActionPoller: ID 57: id resolved to 57
2015-08-07 19:45:28,497 DEBUG    pytan.handler.ActionPoller: ID 57: package_spec resolved to PackageSpec, name: 'Distribute Tanium Standard Utilities', id: 20
2015-08-07 19:45:28,503 DEBUG    pytan.handler.ActionPoller: ID 57: target_group resolved to Group, name: 'Default'
2015-08-07 19:45:28,504 DEBUG    pytan.handler.ActionPoller: ID 57: Result Map resolved to {'failed': {'total': 0, '57:Expired.': [], '57:Failed.': [], '57:NotSucceeded.': [], '57:Stopped.': []}, 'finished': {'57:Verified.': [], '57:NotSucceeded.': [], '57:Stopped.': [], '57:Completed.': [], '57:Expired.': [], '57:Failed.': [], '57:Succeeded.': [], 'total': 0}, 'running': {'57:Downloading.': [], '57:Copying.': [], '57:PendingVerification.': [], '57:Running.': [], '57:Waiting.': [], 'total': 0}, 'success': {'57:Completed.': [], 'total': 0, '57:Verified.': []}, 'unknown': {'total': 0}}
2015-08-07 19:45:28,504 DEBUG    pytan.handler.ActionPoller: ID 57: expiration_time resolved to 2015-08-07T20:40:30
2015-08-07 19:45:28,504 DEBUG    pytan.handler.ActionPoller: ID 57: status resolved to Open
2015-08-07 19:45:28,504 DEBUG    pytan.handler.ActionPoller: ID 57: stopped_flag resolved to 0
2015-08-07 19:45:28,504 DEBUG    pytan.handler.ActionPoller: ID 57: Object Info resolved to ID 57: Package: 'Distribute Tanium Standard Utilities', Target: 'None', Verify: False, Stopped: False, Status: Open

Type of response:  <type 'dict'>

Pretty print of response:
{'action_info': <taniumpy.object_types.result_info.ResultInfo object at 0x10be950d0>,
 'action_object': <taniumpy.object_types.action.Action object at 0x10bf70fd0>,
 'action_result_map': None,
 'action_results': None,
 'group_object': None,
 'package_object': <taniumpy.object_types.package_spec.PackageSpec object at 0x11aae6050>,
 'poller_object': <pytan.pollers.ActionPoller object at 0x11aae6090>,
 'poller_success': None,
 'saved_action_object': <taniumpy.object_types.saved_action.SavedAction object at 0x10c063a50>}

Print of action object: 
Action, name: 'API Deploy Distribute Tanium Standard Utilities', id: 57

'''
