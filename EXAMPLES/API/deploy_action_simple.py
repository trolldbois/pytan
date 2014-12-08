
"""
Deploy an action against all computers using human strings.
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
2014-12-08 15:14:43,044 INFO     question_progress: Results 0% (Get Online = "True" from all machines)
2014-12-08 15:14:48,061 INFO     question_progress: Results 50% (Get Online = "True" from all machines)
2014-12-08 15:14:53,079 INFO     question_progress: Results 100% (Get Online = "True" from all machines)
2014-12-08 15:14:53,142 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:14:54,168 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:14:55,200 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:14:56,225 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:14:57,254 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:14:58,284 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:14:59,310 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:00,339 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:01,367 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:02,395 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:03,431 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:04,481 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:05,510 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:06,541 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:07,572 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:08,601 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:09,630 INFO     action_progress: Action Results Passed: 17% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:10,661 INFO     action_progress: Action Results Passed: 67% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:11,690 INFO     action_progress: Action Results Passed: 67% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:12,716 INFO     action_progress: Action Results Passed: 67% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:13,745 INFO     action_progress: Action Results Passed: 67% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:14,774 INFO     action_progress: Action Results Passed: 67% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:15,804 INFO     action_progress: Action Results Passed: 67% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:16,830 INFO     action_progress: Action Results Passed: 83% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:17,860 INFO     action_progress: Action Results Passed: 83% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:18,889 INFO     action_progress: Action Results Passed: 100% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:18,916 INFO     action_progress: Action Results Completed: 100% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:15:18,916 INFO     action_progress: API Deploy Distribute Tanium Standard Utilities Result Counts:
	Running Count: 0
	Success Count: 6
	Failed Count: 0
	Unknown Count: 0
	Finished Count: 6
	Total Count: 6
	Finished Count must equal: 6

Type of response:  <type 'dict'>

Pretty print of response:
{'action_object': <taniumpy.object_types.action.Action object at 0x10e0f4ed0>,
 'action_progress_human': 'API Deploy Distribute Tanium Standard Utilities Result Counts:\n\tRunning Count: 0\n\tSuccess Count: 6\n\tFailed Count: 0\n\tUnknown Count: 0\n\tFinished Count: 6\n\tTotal Count: 6\n\tFinished Count must equal: 6',
 'action_progress_map': {'Completed.': ['Casus-Belli.local',
                                        'jtanium1.localdomain',
                                        'ubuntu.(none)',
                                        'localhost.(none)',
                                        'Jims-Mac.local',
                                        'WIN-A12SC6N6T7Q']},
 'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x10e634c50>,
 'pre_action_question_results': {'question_object': <taniumpy.object_types.question.Question object at 0x10e664110>,
                                 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10e0f4e50>}}

Print of action object: 
Action, name: 'API Deploy Distribute Tanium Standard Utilities'

CSV Results of response: 
Action Statuses,Computer Name
29:Completed.,Casus-Belli.local
29:Completed.,jtanium1.localdomain
29:Completed.,ubuntu.(none)
29:Completed.,localhost.(none)
29:Completed.,Jims-Mac.local
29:Completed.,WIN-A12SC6N6T7Q


'''
