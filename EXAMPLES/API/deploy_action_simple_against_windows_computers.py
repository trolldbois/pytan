
"""
Deploy an action against only windows computers using human strings. This requires passing in an action filter
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
PORT = "444"

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
kwargs["run"] = True
kwargs["action_filters"] = u'Operating System, that contains:Windows'
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
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
2015-08-06 14:52:20,806 DEBUG    pytan.handler.ActionPoller: ID 36369: id resolved to 36369
2015-08-06 14:52:20,806 DEBUG    pytan.handler.ActionPoller: ID 36369: package_spec resolved to PackageSpec, name: 'Distribute Tanium Standard Utilities', id: 20
2015-08-06 14:52:20,813 DEBUG    pytan.handler.ActionPoller: ID 36369: target_group resolved to Group, name: 'Default', id: 27374
2015-08-06 14:52:20,831 DEBUG    pytan.handler.ActionPoller: ID 36369: Result Map resolved to {'failed': {'36369:NotSucceeded.': [], '36369:Stopped.': [], 'total': 0, '36369:Expired.': [], '36369:Failed.': []}, 'finished': {'36369:Failed.': [], '36369:NotSucceeded.': [], '36369:Expired.': [], '36369:Completed.': [], '36369:Stopped.': [], '36369:Verified.': [], 'total': 0, '36369:Succeeded.': []}, 'running': {'36369:Waiting.': [], '36369:Running.': [], '36369:Downloading.': [], '36369:Copying.': [], 'total': 0, '36369:PendingVerification.': []}, 'success': {'36369:Verified.': [], 'total': 0, '36369:Completed.': []}, 'unknown': {'total': 0}}
2015-08-06 14:52:20,831 DEBUG    pytan.handler.ActionPoller: ID 36369: expiration_time resolved to 2015-08-06T16:32:21
2015-08-06 14:52:20,831 DEBUG    pytan.handler.ActionPoller: ID 36369: status resolved to Active
2015-08-06 14:52:20,831 DEBUG    pytan.handler.ActionPoller: ID 36369: stopped_flag resolved to 0
2015-08-06 14:52:20,831 DEBUG    pytan.handler.ActionPoller: ID 36369: Object Info resolved to ID 36369: Package: 'Distribute Tanium Standard Utilities', Target: ' Operating System contains "Windows"', Verify: False, Stopped: False, Status: Active
2015-08-06 14:52:20,831 DEBUG    pytan.handler.ActionPoller: ID 36369: Adding Question to derive passed count
2015-08-06 14:52:21,077 DEBUG    pytan.handler.QuestionPoller: ID 86267: id resolved to 86267
2015-08-06 14:52:21,078 DEBUG    pytan.handler.QuestionPoller: ID 86267: expiration resolved to 2015-08-06T15:02:21
2015-08-06 14:52:21,078 DEBUG    pytan.handler.QuestionPoller: ID 86267: query_text resolved to Get number of machines where Operating System contains "Windows"
2015-08-06 14:52:21,078 DEBUG    pytan.handler.QuestionPoller: ID 86267: id resolved to 86267
2015-08-06 14:52:21,078 DEBUG    pytan.handler.QuestionPoller: ID 86267: Object Info resolved to Question ID: 86267, Query: Get number of machines where Operating System contains "Windows"
2015-08-06 14:52:21,083 DEBUG    pytan.handler.QuestionPoller: ID 86267: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:52:21,083 DEBUG    pytan.handler.QuestionPoller: ID 86267: Timing: Started: 2015-08-06 14:52:21.078205, Expiration: 2015-08-06 15:02:21, Override Timeout: None, Elapsed Time: 0:00:00.004905, Left till expiry: 0:09:59.916893, Loop Count: 1
2015-08-06 14:52:21,083 INFO     pytan.handler.QuestionPoller: ID 86267: Progress Changed 0% (0 of 2)
2015-08-06 14:52:26,090 DEBUG    pytan.handler.QuestionPoller: ID 86267: Progress: Tested: 2, Passed: 1, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 0
2015-08-06 14:52:26,090 DEBUG    pytan.handler.QuestionPoller: ID 86267: Timing: Started: 2015-08-06 14:52:21.078205, Expiration: 2015-08-06 15:02:21, Override Timeout: None, Elapsed Time: 0:00:05.012353, Left till expiry: 0:09:54.909445, Loop Count: 2
2015-08-06 14:52:26,090 INFO     pytan.handler.QuestionPoller: ID 86267: Progress Changed 100% (2 of 2)
2015-08-06 14:52:26,090 INFO     pytan.handler.QuestionPoller: ID 86267: Reached Threshold of 99% (2 of 2)
2015-08-06 14:52:26,090 DEBUG    pytan.handler.ActionPoller: ID 36369: Passed Count resolved to 1
2015-08-06 14:52:26,226 DEBUG    pytan.handler.ActionPoller: ID 36369: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:52:26,226 DEBUG    pytan.handler.ActionPoller: ID 36369: Timing: Started: 2015-08-06 14:52:20.831609, Expiration: 2015-08-06 16:32:21, Override Timeout: None, Elapsed Time: 0:00:05.394624, Left till expiry: 1:39:54.773769, Loop Count: 1
2015-08-06 14:52:26,226 INFO     pytan.handler.ActionPoller: ID 36369: Progress Changed for Seen Count 0% (0 of 1)
2015-08-06 14:52:31,517 DEBUG    pytan.handler.ActionPoller: ID 36369: Progress: Seen Action: 1, Expected Seen: 1, Percent: 100%
2015-08-06 14:52:31,517 DEBUG    pytan.handler.ActionPoller: ID 36369: Timing: Started: 2015-08-06 14:52:20.831609, Expiration: 2015-08-06 16:32:21, Override Timeout: None, Elapsed Time: 0:00:10.685562, Left till expiry: 1:39:49.482831, Loop Count: 2
2015-08-06 14:52:31,517 INFO     pytan.handler.ActionPoller: ID 36369: Progress Changed for Seen Count 100% (1 of 1)
2015-08-06 14:52:31,517 INFO     pytan.handler.ActionPoller: ID 36369: Reached Threshold for Seen Count of 100% (1 of 1)
2015-08-06 14:52:31,531 DEBUG    pytan.handler.ActionPoller: ID 36369: failed: 0, finished: 0, running: 1, success: 0, unknown: 0, Done Key: success, Passed Count: 1
2015-08-06 14:52:31,531 DEBUG    pytan.handler.ActionPoller: ID 36369: Timing: Started: 2015-08-06 14:52:20.831609, Expiration: 2015-08-06 16:32:21, Override Timeout: None, Elapsed Time: 0:00:10.699486, Left till expiry: 1:39:49.468907, Loop Count: 1
2015-08-06 14:52:31,531 INFO     pytan.handler.ActionPoller: ID 36369: Progress Changed for Finished Count 0% (0 of 1)
2015-08-06 14:52:36,556 DEBUG    pytan.handler.ActionPoller: ID 36369: failed: 0, finished: 0, running: 1, success: 0, unknown: 0, Done Key: success, Passed Count: 1
2015-08-06 14:52:36,556 DEBUG    pytan.handler.ActionPoller: ID 36369: Timing: Started: 2015-08-06 14:52:20.831609, Expiration: 2015-08-06 16:32:21, Override Timeout: None, Elapsed Time: 0:00:15.725172, Left till expiry: 1:39:44.443221, Loop Count: 2
2015-08-06 14:52:41,574 DEBUG    pytan.handler.ActionPoller: ID 36369: failed: 0, finished: 1, running: 1, success: 1, unknown: 0, Done Key: success, Passed Count: 1
2015-08-06 14:52:41,574 DEBUG    pytan.handler.ActionPoller: ID 36369: Timing: Started: 2015-08-06 14:52:20.831609, Expiration: 2015-08-06 16:32:21, Override Timeout: None, Elapsed Time: 0:00:20.743171, Left till expiry: 1:39:39.425223, Loop Count: 3
2015-08-06 14:52:41,574 INFO     pytan.handler.ActionPoller: ID 36369: Progress Changed for Finished Count 100% (1 of 1)
2015-08-06 14:52:41,574 INFO     pytan.handler.ActionPoller: ID 36369: Reached Threshold for Finished Count of 100% (1 of 1)

Type of response:  <type 'dict'>

Pretty print of response:
{'action_info': <taniumpy.object_types.result_info.ResultInfo object at 0x122cdd050>,
 'action_object': <taniumpy.object_types.action.Action object at 0x1115fbb10>,
 'action_result_map': {'failed': {'36369:Expired.': [],
                                  '36369:Failed.': [],
                                  '36369:NotSucceeded.': [],
                                  '36369:Stopped.': [],
                                  'total': 0},
                       'finished': {'36369:Completed.': ['jtanium1.localdomain'],
                                    '36369:Expired.': [],
                                    '36369:Failed.': [],
                                    '36369:NotSucceeded.': [],
                                    '36369:Stopped.': [],
                                    '36369:Succeeded.': [],
                                    '36369:Verified.': [],
                                    'total': 1},
                       'running': {'36369:Copying.': [],
                                   '36369:Downloading.': ['jtanium1.localdomain'],
                                   '36369:PendingVerification.': [],
                                   '36369:Running.': [],
                                   '36369:Waiting.': [],
                                   'total': 1},
                       'success': {'36369:Completed.': ['jtanium1.localdomain'],
                                   '36369:Verified.': [],
                                   'total': 1},
                       'unknown': {'total': 0}},
 'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x122cdd210>,
 'group_object': <taniumpy.object_types.group.Group object at 0x122cdd790>,
 'package_object': <taniumpy.object_types.package_spec.PackageSpec object at 0x122cddf50>,
 'poller_object': <pytan.pollers.ActionPoller object at 0x122cdd510>,
 'poller_success': True,
 'saved_action_object': None}

Print of action object: 
Action, name: 'API Deploy Distribute Tanium Standard Utilities', id: 36369

CSV Results of response: 
Action Statuses,Computer Name
36369:Completed.,jtanium1.localdomain


'''
