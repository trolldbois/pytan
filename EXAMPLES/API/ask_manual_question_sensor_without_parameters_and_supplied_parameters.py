
"""
Ask a manual question using human strings by referencing the name of a single sensor that does NOT take parameters, but supplying parameters anyways (which will be ignored since the sensor does not take parameters).

No sensor filters, sensor filter options, question filters, or question options supplied.
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
kwargs["sensors"] = u'Computer Name{fake=Dweedle}'
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
2015-08-06 14:46:21,641 DEBUG    pytan.handler.QuestionPoller: ID 86252: id resolved to 86252
2015-08-06 14:46:21,641 DEBUG    pytan.handler.QuestionPoller: ID 86252: expiration resolved to 2015-08-06T14:56:21
2015-08-06 14:46:21,641 DEBUG    pytan.handler.QuestionPoller: ID 86252: query_text resolved to Get Computer Name[Dweedle] from all machines
2015-08-06 14:46:21,641 DEBUG    pytan.handler.QuestionPoller: ID 86252: id resolved to 86252
2015-08-06 14:46:21,642 DEBUG    pytan.handler.QuestionPoller: ID 86252: Object Info resolved to Question ID: 86252, Query: Get Computer Name[Dweedle] from all machines
2015-08-06 14:46:21,646 DEBUG    pytan.handler.QuestionPoller: ID 86252: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:46:21,646 DEBUG    pytan.handler.QuestionPoller: ID 86252: Timing: Started: 2015-08-06 14:46:21.642041, Expiration: 2015-08-06 14:56:21, Override Timeout: None, Elapsed Time: 0:00:00.004885, Left till expiry: 0:09:59.353077, Loop Count: 1
2015-08-06 14:46:21,647 INFO     pytan.handler.QuestionPoller: ID 86252: Progress Changed 0% (0 of 2)
2015-08-06 14:46:26,657 DEBUG    pytan.handler.QuestionPoller: ID 86252: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:46:26,657 DEBUG    pytan.handler.QuestionPoller: ID 86252: Timing: Started: 2015-08-06 14:46:21.642041, Expiration: 2015-08-06 14:56:21, Override Timeout: None, Elapsed Time: 0:00:05.015544, Left till expiry: 0:09:54.342417, Loop Count: 2
2015-08-06 14:46:31,668 DEBUG    pytan.handler.QuestionPoller: ID 86252: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
2015-08-06 14:46:31,668 DEBUG    pytan.handler.QuestionPoller: ID 86252: Timing: Started: 2015-08-06 14:46:21.642041, Expiration: 2015-08-06 14:56:21, Override Timeout: None, Elapsed Time: 0:00:10.026653, Left till expiry: 0:09:49.331309, Loop Count: 3
2015-08-06 14:46:31,668 INFO     pytan.handler.QuestionPoller: ID 86252: Progress Changed 50% (1 of 2)
2015-08-06 14:46:36,679 DEBUG    pytan.handler.QuestionPoller: ID 86252: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
2015-08-06 14:46:36,679 DEBUG    pytan.handler.QuestionPoller: ID 86252: Timing: Started: 2015-08-06 14:46:21.642041, Expiration: 2015-08-06 14:56:21, Override Timeout: None, Elapsed Time: 0:00:15.037733, Left till expiry: 0:09:44.320229, Loop Count: 4
2015-08-06 14:46:41,689 DEBUG    pytan.handler.QuestionPoller: ID 86252: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
2015-08-06 14:46:41,689 DEBUG    pytan.handler.QuestionPoller: ID 86252: Timing: Started: 2015-08-06 14:46:21.642041, Expiration: 2015-08-06 14:56:21, Override Timeout: None, Elapsed Time: 0:00:20.047084, Left till expiry: 0:09:39.310877, Loop Count: 5
2015-08-06 14:46:46,695 DEBUG    pytan.handler.QuestionPoller: ID 86252: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
2015-08-06 14:46:46,696 DEBUG    pytan.handler.QuestionPoller: ID 86252: Timing: Started: 2015-08-06 14:46:21.642041, Expiration: 2015-08-06 14:56:21, Override Timeout: None, Elapsed Time: 0:00:25.053966, Left till expiry: 0:09:34.303996, Loop Count: 6
2015-08-06 14:46:46,696 INFO     pytan.handler.QuestionPoller: ID 86252: Progress Changed 100% (2 of 2)
2015-08-06 14:46:46,696 INFO     pytan.handler.QuestionPoller: ID 86252: Reached Threshold of 99% (2 of 2)

Type of response:  <type 'dict'>

Pretty print of response:
{'poller_object': <pytan.pollers.QuestionPoller object at 0x10fc74950>,
 'poller_success': True,
 'question_object': <taniumpy.object_types.question.Question object at 0x10fc74c10>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10fc65450>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Computer Name[Dweedle] from all machines

CSV Results of response: 
Computer Name[Dweedle]
[no results]
JTANIUM1


'''
