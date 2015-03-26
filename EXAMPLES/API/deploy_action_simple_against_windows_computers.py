
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

# call the handler with the deploy_action_human method, passing in kwargs for arguments
response = handler.deploy_action_human(**kwargs)
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
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
2015-03-26 11:48:04,109 INFO     question_progress: Results 0% (Get Online = "True" from all machines where Operating System contains "Windows")
2015-03-26 11:48:09,130 INFO     question_progress: Results 100% (Get Online = "True" from all machines where Operating System contains "Windows")
2015-03-26 11:48:09,233 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:10,272 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:11,310 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:12,348 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:13,396 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:14,439 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:15,482 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:16,525 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:17,562 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:18,613 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:19,657 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:20,695 INFO     action_progress: Action Results Passed: 100% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:20,733 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:21,772 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:22,807 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:23,849 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:24,887 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:25,927 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:26,965 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:28,004 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:29,042 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:30,077 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:31,105 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:32,140 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:33,178 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:34,216 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:35,252 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:36,290 INFO     action_progress: Action Results Completed: 100% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:36,290 INFO     action_progress: API Deploy Distribute Tanium Standard Utilities Result Counts:
	Running Count: 0
	Success Count: 1
	Failed Count: 0
	Unknown Count: 0
	Finished Count: 1
	Total Count: 1
	Finished Count must equal: 1

Type of response:  <type 'dict'>

Pretty print of response:
{'action_object': <taniumpy.object_types.action.Action object at 0x108567450>,
 'action_progress_human': 'API Deploy Distribute Tanium Standard Utilities Result Counts:\n\tRunning Count: 0\n\tSuccess Count: 1\n\tFailed Count: 0\n\tUnknown Count: 0\n\tFinished Count: 1\n\tTotal Count: 1\n\tFinished Count must equal: 1',
 'action_progress_map': {'Completed.': ['jtanium1.localdomain']},
 'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x1077fa950>,
 'pre_action_question_results': {'question_object': <taniumpy.object_types.question.Question object at 0x107608d10>,
                                 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x107808550>}}

Print of action object: 
Action, name: 'API Deploy Distribute Tanium Standard Utilities'

CSV Results of response: 
Action Statuses,Computer Name
21078:Completed.,jtanium1.localdomain


'''
