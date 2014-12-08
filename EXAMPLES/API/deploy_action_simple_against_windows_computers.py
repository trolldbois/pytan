
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
kwargs["action_filters"] = u'Operating System, that contains Windows'
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
2014-12-07 01:09:29,611 INFO     question_progress: Results 0% (Get Online = "True" from all machines where Operating System contains "Windows")
2014-12-07 01:09:34,626 INFO     question_progress: Results 0% (Get Online = "True" from all machines where Operating System contains "Windows")
2014-12-07 01:09:39,647 INFO     question_progress: Results 100% (Get Online = "True" from all machines where Operating System contains "Windows")
2014-12-07 01:09:39,744 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:40,774 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:41,804 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:42,835 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:43,869 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:44,897 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:45,925 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:46,955 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:47,982 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:49,010 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:50,036 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:51,065 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:52,105 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:53,134 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:54,274 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:55,345 INFO     action_progress: Action Results Passed: 100% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:55,375 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:56,405 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:57,431 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:58,458 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:09:59,485 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:10:00,515 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:10:01,552 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:10:02,581 INFO     action_progress: Action Results Completed: 100% (API Deploy Distribute Tanium Standard Utilities)
2014-12-07 01:10:02,581 INFO     action_progress: API Deploy Distribute Tanium Standard Utilities Result Counts:
	Running Count: 0
	Success Count: 1
	Failed Count: 0
	Unknown Count: 0
	Finished Count: 1
	Total Count: 1
	Finished Count must equal: 1

Type of response:  <type 'dict'>

Pretty print of response:
{'action_object': <taniumpy.object_types.action.Action object at 0x102286810>,
 'action_progress_human': 'API Deploy Distribute Tanium Standard Utilities Result Counts:\n\tRunning Count: 0\n\tSuccess Count: 1\n\tFailed Count: 0\n\tUnknown Count: 0\n\tFinished Count: 1\n\tTotal Count: 1\n\tFinished Count must equal: 1',
 'action_progress_map': {'Completed.': ['jtanium1.localdomain']},
 'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x102047a10>,
 'pre_action_question_results': {'question_object': <taniumpy.object_types.question.Question object at 0x102339410>,
                                 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10228efd0>}}

Print of action object: 
Action, name: 'API Deploy Distribute Tanium Standard Utilities'

CSV Results of response: 
Action Statuses,Computer Name
73:Completed.,jtanium1.localdomain


'''
