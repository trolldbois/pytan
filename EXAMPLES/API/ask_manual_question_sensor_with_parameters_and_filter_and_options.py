
"""
Ask a manual question using human strings by referencing the name of a single sensor that takes parameters, but supplying only two of the four parameters that are used by the sensor.

Also supply a sensor filter that limits the column data that is shown to values that match the regex '.*Shared.*', and a sensor filter option that re-fetches any cached data that is older than 3600 seconds.

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
PORT = "443"

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
kwargs["sensors"] = u'Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*}, that regex match:.*Shared.*, opt:max_data_age:3600'
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
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
2015-08-07 19:43:16,405 DEBUG    pytan.handler.QuestionPoller: ID 1294: id resolved to 1294
2015-08-07 19:43:16,405 DEBUG    pytan.handler.QuestionPoller: ID 1294: expiration resolved to 2015-08-07T19:53:16
2015-08-07 19:43:16,405 DEBUG    pytan.handler.QuestionPoller: ID 1294: query_text resolved to Get Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*] containing "Shared" from all machines
2015-08-07 19:43:16,405 DEBUG    pytan.handler.QuestionPoller: ID 1294: id resolved to 1294
2015-08-07 19:43:16,405 DEBUG    pytan.handler.QuestionPoller: ID 1294: Object Info resolved to Question ID: 1294, Query: Get Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*] containing "Shared" from all machines
2015-08-07 19:43:16,408 DEBUG    pytan.handler.QuestionPoller: ID 1294: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:43:16,408 DEBUG    pytan.handler.QuestionPoller: ID 1294: Timing: Started: 2015-08-07 19:43:16.405735, Expiration: 2015-08-07 19:53:16, Override Timeout: None, Elapsed Time: 0:00:00.002844, Left till expiry: 0:09:59.591424, Loop Count: 1
2015-08-07 19:43:16,408 INFO     pytan.handler.QuestionPoller: ID 1294: Progress Changed 0% (0 of 2)
2015-08-07 19:43:21,414 DEBUG    pytan.handler.QuestionPoller: ID 1294: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:43:21,414 DEBUG    pytan.handler.QuestionPoller: ID 1294: Timing: Started: 2015-08-07 19:43:16.405735, Expiration: 2015-08-07 19:53:16, Override Timeout: None, Elapsed Time: 0:00:05.008819, Left till expiry: 0:09:54.585449, Loop Count: 2
2015-08-07 19:43:26,420 DEBUG    pytan.handler.QuestionPoller: ID 1294: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:43:26,420 DEBUG    pytan.handler.QuestionPoller: ID 1294: Timing: Started: 2015-08-07 19:43:16.405735, Expiration: 2015-08-07 19:53:16, Override Timeout: None, Elapsed Time: 0:00:10.014489, Left till expiry: 0:09:49.579779, Loop Count: 3
2015-08-07 19:43:31,424 DEBUG    pytan.handler.QuestionPoller: ID 1294: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:43:31,424 DEBUG    pytan.handler.QuestionPoller: ID 1294: Timing: Started: 2015-08-07 19:43:16.405735, Expiration: 2015-08-07 19:53:16, Override Timeout: None, Elapsed Time: 0:00:15.018711, Left till expiry: 0:09:44.575556, Loop Count: 4
2015-08-07 19:43:36,428 DEBUG    pytan.handler.QuestionPoller: ID 1294: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 74
2015-08-07 19:43:36,428 DEBUG    pytan.handler.QuestionPoller: ID 1294: Timing: Started: 2015-08-07 19:43:16.405735, Expiration: 2015-08-07 19:53:16, Override Timeout: None, Elapsed Time: 0:00:20.022489, Left till expiry: 0:09:39.571779, Loop Count: 5
2015-08-07 19:43:36,428 INFO     pytan.handler.QuestionPoller: ID 1294: Progress Changed 50% (1 of 2)
2015-08-07 19:43:41,432 DEBUG    pytan.handler.QuestionPoller: ID 1294: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 74
2015-08-07 19:43:41,432 DEBUG    pytan.handler.QuestionPoller: ID 1294: Timing: Started: 2015-08-07 19:43:16.405735, Expiration: 2015-08-07 19:53:16, Override Timeout: None, Elapsed Time: 0:00:25.027214, Left till expiry: 0:09:34.567054, Loop Count: 6
2015-08-07 19:43:46,441 DEBUG    pytan.handler.QuestionPoller: ID 1294: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 74
2015-08-07 19:43:46,442 DEBUG    pytan.handler.QuestionPoller: ID 1294: Timing: Started: 2015-08-07 19:43:16.405735, Expiration: 2015-08-07 19:53:16, Override Timeout: None, Elapsed Time: 0:00:30.036345, Left till expiry: 0:09:29.557923, Loop Count: 7
2015-08-07 19:43:51,449 DEBUG    pytan.handler.QuestionPoller: ID 1294: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 75
2015-08-07 19:43:51,449 DEBUG    pytan.handler.QuestionPoller: ID 1294: Timing: Started: 2015-08-07 19:43:16.405735, Expiration: 2015-08-07 19:53:16, Override Timeout: None, Elapsed Time: 0:00:35.044025, Left till expiry: 0:09:24.550243, Loop Count: 8
2015-08-07 19:43:51,449 INFO     pytan.handler.QuestionPoller: ID 1294: Progress Changed 100% (2 of 2)
2015-08-07 19:43:51,449 INFO     pytan.handler.QuestionPoller: ID 1294: Reached Threshold of 99% (2 of 2)

Type of response:  <type 'dict'>

Pretty print of response:
{'poller_object': <pytan.pollers.QuestionPoller object at 0x10a615f10>,
 'poller_success': True,
 'question_object': <taniumpy.object_types.question.Question object at 0x10a5f57d0>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10a5b9a10>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*] containing "Shared" from all machines

CSV Results of response: 
"Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*]"
[no results]
C:\Program Files\Common Files\Microsoft Shared\VS7Debug
C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
C:\Program Files\Common Files\Microsoft Shared\ink\ru-RU
C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\keypad
C:\Program Files\Common Files\Microsoft Shared\ink
C:\Program Files\Common Files\Microsoft Shared\ink\sv-SE
C:\Program Files\Common Files\Microsoft Shared\ink\uk-UA
C:\Program Files\Common Files\Microsoft Shared\ink\sl-SI
C:\Program Files\Common Files\Microsoft Shared\ink\hu-HU
C:\Program Files\Common Files\Microsoft Shared\ink\zh-TW
C:\Program Files\Common Files\Microsoft Shared\ink\zh-CN
C:\Program Files\Common Files\Microsoft Shared\ink\fi-FI
C:\Program Files\Common Files\Microsoft Shared
..trimmed for brevity..

'''
