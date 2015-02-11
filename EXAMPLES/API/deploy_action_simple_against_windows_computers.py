
"""
Deploy an action against only windows computers using human strings. This requires passing in an action filter
"""
# Path to lib directory which contains pytan package
PYTAN_LIB_PATH = '../lib'

# connection info for Tanium Server
USERNAME = "Tanium User"
PASSWORD = "T@n!um"
HOST = "172.16.31.128"
PORT = "444"

# Logging conrols
LOGLEVEL = 2
DEBUGFORMAT = False

import sys, tempfile
sys.path.append(PYTAN_LIB_PATH)

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
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
2015-02-11 12:05:19,277 INFO     question_progress: Results 0% (Get Online = "True" from all machines where Operating System contains "Windows")
2015-02-11 12:05:24,302 INFO     question_progress: Results 0% (Get Online = "True" from all machines where Operating System contains "Windows")
2015-02-11 12:05:29,319 INFO     question_progress: Results 100% (Get Online = "True" from all machines where Operating System contains "Windows")
2015-02-11 12:05:29,385 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:30,414 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:31,488 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:32,515 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:33,546 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:34,576 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:35,602 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:36,627 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:37,657 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:38,687 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:39,715 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:40,742 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:41,771 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:42,797 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:43,829 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:44,856 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:45,885 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:46,912 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:47,938 INFO     action_progress: Action Results Passed: 100% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:47,962 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:48,990 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:50,019 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:51,046 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:52,074 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:53,101 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:54,128 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:55,158 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:56,186 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:57,213 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:58,249 INFO     action_progress: Action Results Completed: 100% (API Deploy Distribute Tanium Standard Utilities)
2015-02-11 12:05:58,249 INFO     action_progress: API Deploy Distribute Tanium Standard Utilities Result Counts:
	Running Count: 0
	Success Count: 1
	Failed Count: 0
	Unknown Count: 0
	Finished Count: 1
	Total Count: 1
	Finished Count must equal: 1

Type of response:  <type 'dict'>

Pretty print of response:
{'action_object': <taniumpy.object_types.action.Action object at 0x107b4ba50>,
 'action_progress_human': 'API Deploy Distribute Tanium Standard Utilities Result Counts:\n\tRunning Count: 0\n\tSuccess Count: 1\n\tFailed Count: 0\n\tUnknown Count: 0\n\tFinished Count: 1\n\tTotal Count: 1\n\tFinished Count must equal: 1',
 'action_progress_map': {'Completed.': ['jtanium1.localdomain']},
 'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x107ae7890>,
 'pre_action_question_results': {'question_object': <taniumpy.object_types.question.Question object at 0x1059f8710>,
                                 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x1059fb110>}}

Print of action object: 
Action, name: 'API Deploy Distribute Tanium Standard Utilities'

CSV Results of response: 
Action Statuses,Computer Name
1371:Completed.,jtanium1.localdomain


'''
