
"""
Deploy an action against all computers using human strings.
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
2015-03-26 11:45:58,435 INFO     question_progress: Results 0% (Get Online = "True" from all machines)
2015-03-26 11:46:03,455 INFO     question_progress: Results 100% (Get Online = "True" from all machines)
2015-03-26 11:46:03,540 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:04,579 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:05,615 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:06,649 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:07,682 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:08,717 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:09,752 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:10,788 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:11,819 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:12,851 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:13,886 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:14,922 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:15,954 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:16,988 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:18,020 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:19,054 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:20,095 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:21,131 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:22,164 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:23,199 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:24,233 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:25,270 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:26,307 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:27,342 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:28,375 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:29,414 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:30,476 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:31,513 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:32,552 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:33,592 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:34,626 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:35,663 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:36,697 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:37,734 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:38,768 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:39,803 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:40,836 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:41,874 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:42,913 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:43,947 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:44,984 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:46,015 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:47,043 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:48,070 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:49,104 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:50,136 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:51,175 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:52,208 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:53,248 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:54,285 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:55,324 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:56,365 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:57,400 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:58,435 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:46:59,471 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:00,506 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:01,537 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:02,577 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:03,614 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:04,649 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:05,686 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:06,722 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:07,757 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:08,793 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:09,828 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:10,867 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:11,904 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:12,942 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:13,983 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:15,019 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:16,056 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:17,095 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:18,132 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:19,171 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:20,204 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:21,241 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:22,282 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:23,318 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:24,356 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:25,396 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:26,434 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:27,471 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:28,509 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:29,545 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:30,582 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:31,618 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:32,654 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:33,693 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:34,733 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:35,765 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:36,804 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:37,838 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:38,875 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:39,907 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:40,945 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:41,985 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:43,020 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:44,066 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:45,103 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:46,138 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:47,180 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:48,220 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:49,263 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:50,300 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:51,338 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:52,379 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:53,466 INFO     action_progress: Action Results Passed: 100% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:53,499 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:54,539 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:55,581 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:56,621 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:57,666 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:58,702 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:47:59,739 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:00,778 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:01,819 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:02,854 INFO     action_progress: Action Results Completed: 0% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:03,895 INFO     action_progress: Action Results Completed: 100% (API Deploy Distribute Tanium Standard Utilities)
2015-03-26 11:48:03,895 INFO     action_progress: API Deploy Distribute Tanium Standard Utilities Result Counts:
	Running Count: 0
	Success Count: 2
	Failed Count: 0
	Unknown Count: 0
	Finished Count: 2
	Total Count: 2
	Finished Count must equal: 2

Type of response:  <type 'dict'>

Pretty print of response:
{'action_object': <taniumpy.object_types.action.Action object at 0x10856d890>,
 'action_progress_human': 'API Deploy Distribute Tanium Standard Utilities Result Counts:\n\tRunning Count: 0\n\tSuccess Count: 2\n\tFailed Count: 0\n\tUnknown Count: 0\n\tFinished Count: 2\n\tTotal Count: 2\n\tFinished Count must equal: 2',
 'action_progress_map': {'Completed.': ['Casus-Belli.local',
                                        'jtanium1.localdomain']},
 'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x10769cfd0>,
 'pre_action_question_results': {'question_object': <taniumpy.object_types.question.Question object at 0x107618b90>,
                                 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x1075963d0>}}

Print of action object: 
Action, name: 'API Deploy Distribute Tanium Standard Utilities'

CSV Results of response: 
Action Statuses,Computer Name
21076:Completed.,Casus-Belli.local
21076:Completed.,jtanium1.localdomain


'''
