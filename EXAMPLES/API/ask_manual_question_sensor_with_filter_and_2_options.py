
"""
Ask a manual question using human strings by referencing the name of a single sensor.

Also supply a sensor filter that limits the column data that is shown to values that contain Windows (which is short hand for regex match against .*Windows.*).

Also supply filter options that re-fetches any cached data that is older than 3600 seconds and treats the values as type string.

No question filters or question options supplied.
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
kwargs["sensors"] = u'Operating System, that contains:Windows, opt:max_data_age:3600, opt:value_type:string'
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
2015-08-06 14:48:17,696 DEBUG    pytan.handler.QuestionPoller: ID 86258: id resolved to 86258
2015-08-06 14:48:17,696 DEBUG    pytan.handler.QuestionPoller: ID 86258: expiration resolved to 2015-08-06T14:58:17
2015-08-06 14:48:17,696 DEBUG    pytan.handler.QuestionPoller: ID 86258: query_text resolved to Get Operating System contains "Windows" from all machines
2015-08-06 14:48:17,696 DEBUG    pytan.handler.QuestionPoller: ID 86258: id resolved to 86258
2015-08-06 14:48:17,696 DEBUG    pytan.handler.QuestionPoller: ID 86258: Object Info resolved to Question ID: 86258, Query: Get Operating System contains "Windows" from all machines
2015-08-06 14:48:17,701 DEBUG    pytan.handler.QuestionPoller: ID 86258: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:48:17,701 DEBUG    pytan.handler.QuestionPoller: ID 86258: Timing: Started: 2015-08-06 14:48:17.696639, Expiration: 2015-08-06 14:58:17, Override Timeout: None, Elapsed Time: 0:00:00.004815, Left till expiry: 0:09:59.298548, Loop Count: 1
2015-08-06 14:48:17,701 INFO     pytan.handler.QuestionPoller: ID 86258: Progress Changed 0% (0 of 2)
2015-08-06 14:48:22,708 DEBUG    pytan.handler.QuestionPoller: ID 86258: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
2015-08-06 14:48:22,708 DEBUG    pytan.handler.QuestionPoller: ID 86258: Timing: Started: 2015-08-06 14:48:17.696639, Expiration: 2015-08-06 14:58:17, Override Timeout: None, Elapsed Time: 0:00:05.011611, Left till expiry: 0:09:54.291752, Loop Count: 2
2015-08-06 14:48:22,708 INFO     pytan.handler.QuestionPoller: ID 86258: Progress Changed 50% (1 of 2)
2015-08-06 14:48:27,715 DEBUG    pytan.handler.QuestionPoller: ID 86258: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
2015-08-06 14:48:27,715 DEBUG    pytan.handler.QuestionPoller: ID 86258: Timing: Started: 2015-08-06 14:48:17.696639, Expiration: 2015-08-06 14:58:17, Override Timeout: None, Elapsed Time: 0:00:10.018807, Left till expiry: 0:09:49.284556, Loop Count: 3
2015-08-06 14:48:27,715 INFO     pytan.handler.QuestionPoller: ID 86258: Progress Changed 100% (2 of 2)
2015-08-06 14:48:27,715 INFO     pytan.handler.QuestionPoller: ID 86258: Reached Threshold of 99% (2 of 2)

Type of response:  <type 'dict'>

Pretty print of response:
{'poller_object': <pytan.pollers.QuestionPoller object at 0x10fc65a10>,
 'poller_success': True,
 'question_object': <taniumpy.object_types.question.Question object at 0x10fc65ad0>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10fc3ead0>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Operating System contains "Windows" from all machines

CSV Results of response: 
Operating System
[no results]
Windows Server 2008 R2 Standard


'''
