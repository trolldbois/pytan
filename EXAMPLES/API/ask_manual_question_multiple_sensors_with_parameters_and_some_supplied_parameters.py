
"""
Ask a manual question using human strings by referencing the name of multiple sensors, one that takes parameters, but supplying only two of the four parameters that are used by the sensor (and letting pytan automatically determine the appropriate default value for those parameters which require a value and none was supplied), and one that does not take parameters.

No sensor filters, question filters, or question options supplied.
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
kwargs["sensors"] = [u'Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*}',
 u'Computer Name']
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
2015-08-07 19:40:30,754 DEBUG    pytan.handler.QuestionPoller: ID 1284: id resolved to 1284
2015-08-07 19:40:30,754 DEBUG    pytan.handler.QuestionPoller: ID 1284: expiration resolved to 2015-08-07T19:50:30
2015-08-07 19:40:30,754 DEBUG    pytan.handler.QuestionPoller: ID 1284: query_text resolved to Get Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*] and Computer Name from all machines
2015-08-07 19:40:30,754 DEBUG    pytan.handler.QuestionPoller: ID 1284: id resolved to 1284
2015-08-07 19:40:30,754 DEBUG    pytan.handler.QuestionPoller: ID 1284: Object Info resolved to Question ID: 1284, Query: Get Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*] and Computer Name from all machines
2015-08-07 19:40:30,757 DEBUG    pytan.handler.QuestionPoller: ID 1284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:40:30,757 DEBUG    pytan.handler.QuestionPoller: ID 1284: Timing: Started: 2015-08-07 19:40:30.754560, Expiration: 2015-08-07 19:50:30, Override Timeout: None, Elapsed Time: 0:00:00.002925, Left till expiry: 0:09:59.242518, Loop Count: 1
2015-08-07 19:40:30,757 INFO     pytan.handler.QuestionPoller: ID 1284: Progress Changed 0% (0 of 2)
2015-08-07 19:40:35,761 DEBUG    pytan.handler.QuestionPoller: ID 1284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:40:35,761 DEBUG    pytan.handler.QuestionPoller: ID 1284: Timing: Started: 2015-08-07 19:40:30.754560, Expiration: 2015-08-07 19:50:30, Override Timeout: None, Elapsed Time: 0:00:05.007403, Left till expiry: 0:09:54.238040, Loop Count: 2
2015-08-07 19:40:40,766 DEBUG    pytan.handler.QuestionPoller: ID 1284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:40:40,766 DEBUG    pytan.handler.QuestionPoller: ID 1284: Timing: Started: 2015-08-07 19:40:30.754560, Expiration: 2015-08-07 19:50:30, Override Timeout: None, Elapsed Time: 0:00:10.011661, Left till expiry: 0:09:49.233783, Loop Count: 3
2015-08-07 19:40:45,773 DEBUG    pytan.handler.QuestionPoller: ID 1284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:40:45,773 DEBUG    pytan.handler.QuestionPoller: ID 1284: Timing: Started: 2015-08-07 19:40:30.754560, Expiration: 2015-08-07 19:50:30, Override Timeout: None, Elapsed Time: 0:00:15.018672, Left till expiry: 0:09:44.226770, Loop Count: 4
2015-08-07 19:40:50,777 DEBUG    pytan.handler.QuestionPoller: ID 1284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:40:50,777 DEBUG    pytan.handler.QuestionPoller: ID 1284: Timing: Started: 2015-08-07 19:40:30.754560, Expiration: 2015-08-07 19:50:30, Override Timeout: None, Elapsed Time: 0:00:20.022850, Left till expiry: 0:09:39.222593, Loop Count: 5
2015-08-07 19:40:55,782 DEBUG    pytan.handler.QuestionPoller: ID 1284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:40:55,782 DEBUG    pytan.handler.QuestionPoller: ID 1284: Timing: Started: 2015-08-07 19:40:30.754560, Expiration: 2015-08-07 19:50:30, Override Timeout: None, Elapsed Time: 0:00:25.027993, Left till expiry: 0:09:34.217450, Loop Count: 6
2015-08-07 19:41:00,790 DEBUG    pytan.handler.QuestionPoller: ID 1284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:41:00,790 DEBUG    pytan.handler.QuestionPoller: ID 1284: Timing: Started: 2015-08-07 19:40:30.754560, Expiration: 2015-08-07 19:50:30, Override Timeout: None, Elapsed Time: 0:00:30.036024, Left till expiry: 0:09:29.209419, Loop Count: 7
2015-08-07 19:41:05,798 DEBUG    pytan.handler.QuestionPoller: ID 1284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:41:05,798 DEBUG    pytan.handler.QuestionPoller: ID 1284: Timing: Started: 2015-08-07 19:40:30.754560, Expiration: 2015-08-07 19:50:30, Override Timeout: None, Elapsed Time: 0:00:35.044097, Left till expiry: 0:09:24.201346, Loop Count: 8
2015-08-07 19:41:10,805 DEBUG    pytan.handler.QuestionPoller: ID 1284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:41:10,805 DEBUG    pytan.handler.QuestionPoller: ID 1284: Timing: Started: 2015-08-07 19:40:30.754560, Expiration: 2015-08-07 19:50:30, Override Timeout: None, Elapsed Time: 0:00:40.050634, Left till expiry: 0:09:19.194810, Loop Count: 9
2015-08-07 19:41:15,809 DEBUG    pytan.handler.QuestionPoller: ID 1284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:41:15,809 DEBUG    pytan.handler.QuestionPoller: ID 1284: Timing: Started: 2015-08-07 19:40:30.754560, Expiration: 2015-08-07 19:50:30, Override Timeout: None, Elapsed Time: 0:00:45.054617, Left till expiry: 0:09:14.190826, Loop Count: 10
2015-08-07 19:41:20,813 DEBUG    pytan.handler.QuestionPoller: ID 1284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:41:20,813 DEBUG    pytan.handler.QuestionPoller: ID 1284: Timing: Started: 2015-08-07 19:40:30.754560, Expiration: 2015-08-07 19:50:30, Override Timeout: None, Elapsed Time: 0:00:50.058554, Left till expiry: 0:09:09.186891, Loop Count: 11
2015-08-07 19:41:25,817 DEBUG    pytan.handler.QuestionPoller: ID 1284: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
2015-08-07 19:41:25,817 DEBUG    pytan.handler.QuestionPoller: ID 1284: Timing: Started: 2015-08-07 19:40:30.754560, Expiration: 2015-08-07 19:50:30, Override Timeout: None, Elapsed Time: 0:00:55.063175, Left till expiry: 0:09:04.182268, Loop Count: 12
2015-08-07 19:41:25,817 INFO     pytan.handler.QuestionPoller: ID 1284: Progress Changed 100% (2 of 2)
2015-08-07 19:41:25,817 INFO     pytan.handler.QuestionPoller: ID 1284: Reached Threshold of 99% (2 of 2)

Type of response:  <type 'dict'>

Pretty print of response:
{'poller_object': <pytan.pollers.QuestionPoller object at 0x10a614b50>,
 'poller_success': True,
 'question_object': <taniumpy.object_types.question.Question object at 0x10a5f51d0>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10a614f10>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*] and Computer Name from all machines

CSV Results of response: 
Computer Name,"Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*]"
Casus-Belli.local,Windows Only
JTANIUM1.localdomain,"C:\Program Files\VMware\VMware Tools\plugins\vmsvc
C:\Program Files\Common Files\Microsoft Shared\VS7Debug
C:\Program Files\Tanium\Tanium Server\http\taniumjs\sensor-query\src
C:\Program Files\Microsoft SQL Server\110\LocalDB\Binn\Resources\1033
C:\Program Files\Tanium\Tanium Server\http\tux\spin\src
C:\Program Files\Tanium\Tanium Server\http\taniumjs\archived-question\src
C:\Program Files\Tanium\Tanium Module Server\plugins\content
C:\Program Files\Tanium\Tanium Server\http\libraries\kendoui\styles\Moonlight
C:\Program Files\Common Files\VMware\Drivers\vmci\sockets\include
C:\Program Files\Tanium\Tanium Server\http\taniumjs\plugin
C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
C:\Program Files\Tanium\Tanium Server\plugins\console\WorkbenchesManager
C:\Program Files\Tanium\Tanium Module Server\logs
..trimmed for brevity..

'''
