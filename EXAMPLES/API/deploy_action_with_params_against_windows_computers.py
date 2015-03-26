
"""
Deploy an action with parameters against only windows computers using human strings.

This will use the Package 'Custom Tagging - Add Tags' and supply two parameters. The second parameter will be ignored because the package in question only requires one parameter.
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
kwargs["package"] = u'Custom Tagging - Add Tags{$1=tag_should_be_added,$2=tag_should_be_ignore}'

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
2015-03-26 11:48:36,436 INFO     question_progress: Results 0% (Get Online = "True" from all machines where Operating System contains "Windows")
2015-03-26 11:48:41,456 INFO     question_progress: Results 50% (Get Online = "True" from all machines where Operating System contains "Windows")
2015-03-26 11:48:46,478 INFO     question_progress: Results 100% (Get Online = "True" from all machines where Operating System contains "Windows")
2015-03-26 11:48:46,628 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2015-03-26 11:48:47,667 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2015-03-26 11:48:48,712 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2015-03-26 11:48:49,747 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2015-03-26 11:48:50,784 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2015-03-26 11:48:51,830 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2015-03-26 11:48:52,867 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2015-03-26 11:48:53,907 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2015-03-26 11:48:54,946 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2015-03-26 11:48:55,985 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2015-03-26 11:48:57,023 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2015-03-26 11:48:58,064 INFO     action_progress: Action Results Passed: 100% (API Deploy Custom Tagging - Add Tags)
2015-03-26 11:48:58,099 INFO     action_progress: Action Results Completed: 100% (API Deploy Custom Tagging - Add Tags)
2015-03-26 11:48:58,100 INFO     action_progress: API Deploy Custom Tagging - Add Tags Result Counts:
	Running Count: 0
	Success Count: 1
	Failed Count: 0
	Unknown Count: 0
	Finished Count: 1
	Total Count: 1
	Finished Count must equal: 1

Type of response:  <type 'dict'>

Pretty print of response:
{'action_object': <taniumpy.object_types.action.Action object at 0x10756c410>,
 'action_progress_human': 'API Deploy Custom Tagging - Add Tags Result Counts:\n\tRunning Count: 0\n\tSuccess Count: 1\n\tFailed Count: 0\n\tUnknown Count: 0\n\tFinished Count: 1\n\tTotal Count: 1\n\tFinished Count must equal: 1',
 'action_progress_map': {'Completed.': ['jtanium1.localdomain']},
 'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x107563bd0>,
 'pre_action_question_results': {'question_object': <taniumpy.object_types.question.Question object at 0x107817710>,
                                 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10855d290>}}

Print of action object: 
Action, name: 'API Deploy Custom Tagging - Add Tags'

CSV Results of response: 
Action Statuses,Computer Name
21079:Completed.,jtanium1.localdomain


'''
