
"""
Ask a manual question using human strings by referencing the name of multiple sensors and providing a selector that tells pytan explicitly that we are providing a name of a sensor.

No sensor filters, sensor parameters, sensor filter options, question filters, or question options supplied.
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
kwargs["sensors"] = [u'name:Computer Name', u'name:Installed Applications']
kwargs["qtype"] = u'manual'

# call the handler with the ask method, passing in kwargs for arguments
response = handler.ask(**kwargs)
import pprint, io

print ""
print "Type of response: ", type(response)

print ""
print "Pretty print of response:"
print pprint.pformat(response)

print ""
print "Equivalent Question if it were to be asked in the Tanium Console: "
print response['question_object'].query_text

# create an IO stream to store CSV results to
out = io.BytesIO()

# call the write_csv() method to convert response to CSV and store it in out
response['question_results'].write_csv(out, response['question_results'])

print ""
print "CSV Results of response: "
out = out.getvalue()
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\n'.join(out)
print out


'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
2015-08-06 14:44:04,334 DEBUG    pytan.handler.QuestionPoller: ID 86247: id resolved to 86247
2015-08-06 14:44:04,334 DEBUG    pytan.handler.QuestionPoller: ID 86247: expiration resolved to 2015-08-06T14:54:04
2015-08-06 14:44:04,334 DEBUG    pytan.handler.QuestionPoller: ID 86247: query_text resolved to Get Computer Name and Installed Applications from all machines
2015-08-06 14:44:04,334 DEBUG    pytan.handler.QuestionPoller: ID 86247: id resolved to 86247
2015-08-06 14:44:04,334 DEBUG    pytan.handler.QuestionPoller: ID 86247: Object Info resolved to Question ID: 86247, Query: Get Computer Name and Installed Applications from all machines
2015-08-06 14:44:04,339 DEBUG    pytan.handler.QuestionPoller: ID 86247: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:44:04,339 DEBUG    pytan.handler.QuestionPoller: ID 86247: Timing: Started: 2015-08-06 14:44:04.334425, Expiration: 2015-08-06 14:54:04, Override Timeout: None, Elapsed Time: 0:00:00.004821, Left till expiry: 0:09:59.660756, Loop Count: 1
2015-08-06 14:44:04,339 INFO     pytan.handler.QuestionPoller: ID 86247: Progress Changed 0% (0 of 2)
2015-08-06 14:44:09,345 DEBUG    pytan.handler.QuestionPoller: ID 86247: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:44:09,345 DEBUG    pytan.handler.QuestionPoller: ID 86247: Timing: Started: 2015-08-06 14:44:04.334425, Expiration: 2015-08-06 14:54:04, Override Timeout: None, Elapsed Time: 0:00:05.011116, Left till expiry: 0:09:54.654461, Loop Count: 2
2015-08-06 14:44:14,352 DEBUG    pytan.handler.QuestionPoller: ID 86247: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:44:14,352 DEBUG    pytan.handler.QuestionPoller: ID 86247: Timing: Started: 2015-08-06 14:44:04.334425, Expiration: 2015-08-06 14:54:04, Override Timeout: None, Elapsed Time: 0:00:10.018210, Left till expiry: 0:09:49.647367, Loop Count: 3
2015-08-06 14:44:19,360 DEBUG    pytan.handler.QuestionPoller: ID 86247: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
2015-08-06 14:44:19,360 DEBUG    pytan.handler.QuestionPoller: ID 86247: Timing: Started: 2015-08-06 14:44:04.334425, Expiration: 2015-08-06 14:54:04, Override Timeout: None, Elapsed Time: 0:00:15.026133, Left till expiry: 0:09:44.639444, Loop Count: 4
2015-08-06 14:44:19,360 INFO     pytan.handler.QuestionPoller: ID 86247: Progress Changed 100% (2 of 2)
2015-08-06 14:44:19,360 INFO     pytan.handler.QuestionPoller: ID 86247: Reached Threshold of 99% (2 of 2)

Type of response:  <type 'dict'>

Pretty print of response:
{'poller_object': <pytan.pollers.QuestionPoller object at 0x10fc3ed10>,
 'poller_success': True,
 'question_object': <taniumpy.object_types.question.Question object at 0x10fc5f290>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10f83d410>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Computer Name and Installed Applications from all machines

CSV Results of response: 
Computer Name,Name,Silent Uninstall String,Uninstallable,Version
Casus-Belli.local,"Image Capture Extension
Dictation
Wish
Uninstall AnyConnect
Time Machine
AppleGraphicsWarning
soagent
Feedback Assistant
AinuIM
vpndownloader
Pass Viewer
ARDAgent
OBEXAgent
PressAndHold
..trimmed for brevity..

'''
