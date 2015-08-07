
"""
Ask a manual question using human strings by referencing the name of a single sensor that takes parameters, but supplying only two of the four parameters that are used by the sensor (and letting pytan automatically determine the appropriate default value for those parameters which require a value and none was supplied).

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
kwargs["sensors"] = u'Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*}'
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
2015-08-07 19:38:25,510 DEBUG    pytan.handler.QuestionPoller: ID 1283: id resolved to 1283
2015-08-07 19:38:25,510 DEBUG    pytan.handler.QuestionPoller: ID 1283: expiration resolved to 2015-08-07T19:48:25
2015-08-07 19:38:25,510 DEBUG    pytan.handler.QuestionPoller: ID 1283: query_text resolved to Get Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*] from all machines
2015-08-07 19:38:25,510 DEBUG    pytan.handler.QuestionPoller: ID 1283: id resolved to 1283
2015-08-07 19:38:25,510 DEBUG    pytan.handler.QuestionPoller: ID 1283: Object Info resolved to Question ID: 1283, Query: Get Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*] from all machines
2015-08-07 19:38:25,513 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:38:25,513 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:00:00.002791, Left till expiry: 0:09:59.486424, Loop Count: 1
2015-08-07 19:38:25,513 INFO     pytan.handler.QuestionPoller: ID 1283: Progress Changed 0% (0 of 2)
2015-08-07 19:38:30,521 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:38:30,521 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:00:05.010918, Left till expiry: 0:09:54.478298, Loop Count: 2
2015-08-07 19:38:35,526 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:38:35,526 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:00:10.015483, Left till expiry: 0:09:49.473732, Loop Count: 3
2015-08-07 19:38:40,532 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:38:40,532 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:00:15.021829, Left till expiry: 0:09:44.467387, Loop Count: 4
2015-08-07 19:38:45,536 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:38:45,536 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:00:20.025699, Left till expiry: 0:09:39.463516, Loop Count: 5
2015-08-07 19:38:50,539 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:38:50,539 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:00:25.029142, Left till expiry: 0:09:34.460073, Loop Count: 6
2015-08-07 19:38:55,543 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:38:55,543 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:00:30.032768, Left till expiry: 0:09:29.456448, Loop Count: 7
2015-08-07 19:39:00,547 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:39:00,547 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:00:35.036936, Left till expiry: 0:09:24.452281, Loop Count: 8
2015-08-07 19:39:05,554 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:39:05,554 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:00:40.043300, Left till expiry: 0:09:19.445916, Loop Count: 9
2015-08-07 19:39:10,558 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:39:10,558 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:00:45.047479, Left till expiry: 0:09:14.441737, Loop Count: 10
2015-08-07 19:39:15,561 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:39:15,561 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:00:50.051017, Left till expiry: 0:09:09.438199, Loop Count: 11
2015-08-07 19:39:20,566 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:39:20,566 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:00:55.056020, Left till expiry: 0:09:04.433196, Loop Count: 12
2015-08-07 19:39:25,571 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:39:25,571 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:01:00.060525, Left till expiry: 0:08:59.428690, Loop Count: 13
2015-08-07 19:39:30,577 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:39:30,577 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:01:05.066434, Left till expiry: 0:08:54.422783, Loop Count: 14
2015-08-07 19:39:35,581 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:39:35,581 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:01:10.070382, Left till expiry: 0:08:49.418834, Loop Count: 15
2015-08-07 19:39:40,585 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:39:40,585 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:01:15.074593, Left till expiry: 0:08:44.414623, Loop Count: 16
2015-08-07 19:39:45,588 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:39:45,588 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:01:20.078080, Left till expiry: 0:08:39.411135, Loop Count: 17
2015-08-07 19:39:50,592 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:39:50,592 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:01:25.082184, Left till expiry: 0:08:34.407031, Loop Count: 18
2015-08-07 19:39:55,597 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:39:55,597 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:01:30.086827, Left till expiry: 0:08:29.402389, Loop Count: 19
2015-08-07 19:40:00,603 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:40:00,603 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:01:35.092863, Left till expiry: 0:08:24.396353, Loop Count: 20
2015-08-07 19:40:05,612 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:40:05,613 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:01:40.102208, Left till expiry: 0:08:19.387009, Loop Count: 21
2015-08-07 19:40:10,618 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 532
2015-08-07 19:40:10,618 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:01:45.107920, Left till expiry: 0:08:14.381296, Loop Count: 22
2015-08-07 19:40:10,618 INFO     pytan.handler.QuestionPoller: ID 1283: Progress Changed 50% (1 of 2)
2015-08-07 19:40:15,626 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 532
2015-08-07 19:40:15,626 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:01:50.115984, Left till expiry: 0:08:09.373232, Loop Count: 23
2015-08-07 19:40:20,631 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 532
2015-08-07 19:40:20,631 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:01:55.120942, Left till expiry: 0:08:04.368274, Loop Count: 24
2015-08-07 19:40:25,635 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 532
2015-08-07 19:40:25,635 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:02:00.124707, Left till expiry: 0:07:59.364508, Loop Count: 25
2015-08-07 19:40:30,639 DEBUG    pytan.handler.QuestionPoller: ID 1283: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 533
2015-08-07 19:40:30,639 DEBUG    pytan.handler.QuestionPoller: ID 1283: Timing: Started: 2015-08-07 19:38:25.510787, Expiration: 2015-08-07 19:48:25, Override Timeout: None, Elapsed Time: 0:02:05.128949, Left till expiry: 0:07:54.360267, Loop Count: 26
2015-08-07 19:40:30,639 INFO     pytan.handler.QuestionPoller: ID 1283: Progress Changed 100% (2 of 2)
2015-08-07 19:40:30,639 INFO     pytan.handler.QuestionPoller: ID 1283: Reached Threshold of 99% (2 of 2)

Type of response:  <type 'dict'>

Pretty print of response:
{'poller_object': <pytan.pollers.QuestionPoller object at 0x10a613090>,
 'poller_success': True,
 'question_object': <taniumpy.object_types.question.Question object at 0x10a613cd0>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10a810650>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*] from all machines

CSV Results of response: 
"Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*]"
C:\Program Files\VMware\VMware Tools\plugins\vmsvc
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
C:\Program Files\Common Files\SpeechEngines\Microsoft
..trimmed for brevity..

'''
