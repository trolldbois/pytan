
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
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
2015-08-06 14:44:19,488 DEBUG    pytan.handler.QuestionPoller: ID 86248: id resolved to 86248
2015-08-06 14:44:19,488 DEBUG    pytan.handler.QuestionPoller: ID 86248: expiration resolved to 2015-08-06T14:54:19
2015-08-06 14:44:19,488 DEBUG    pytan.handler.QuestionPoller: ID 86248: query_text resolved to Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] from all machines
2015-08-06 14:44:19,488 DEBUG    pytan.handler.QuestionPoller: ID 86248: id resolved to 86248
2015-08-06 14:44:19,488 DEBUG    pytan.handler.QuestionPoller: ID 86248: Object Info resolved to Question ID: 86248, Query: Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] from all machines
2015-08-06 14:44:19,492 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:44:19,492 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:00:00.004695, Left till expiry: 0:09:59.507026, Loop Count: 1
2015-08-06 14:44:19,493 INFO     pytan.handler.QuestionPoller: ID 86248: Progress Changed 0% (0 of 2)
2015-08-06 14:44:24,503 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:44:24,503 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:00:05.015635, Left till expiry: 0:09:54.496086, Loop Count: 2
2015-08-06 14:44:29,511 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:44:29,511 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:00:10.023700, Left till expiry: 0:09:49.488020, Loop Count: 3
2015-08-06 14:44:34,521 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:44:34,521 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:00:15.033003, Left till expiry: 0:09:44.478717, Loop Count: 4
2015-08-06 14:44:39,527 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:44:39,527 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:00:20.039646, Left till expiry: 0:09:39.472074, Loop Count: 5
2015-08-06 14:44:44,534 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:44:44,534 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:00:25.046470, Left till expiry: 0:09:34.465250, Loop Count: 6
2015-08-06 14:44:49,544 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:44:49,544 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:00:30.056104, Left till expiry: 0:09:29.455616, Loop Count: 7
2015-08-06 14:44:54,554 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:44:54,554 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:00:35.066362, Left till expiry: 0:09:24.445359, Loop Count: 8
2015-08-06 14:44:59,561 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:44:59,561 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:00:40.073425, Left till expiry: 0:09:19.438295, Loop Count: 9
2015-08-06 14:45:04,568 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:45:04,568 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:00:45.080428, Left till expiry: 0:09:14.431292, Loop Count: 10
2015-08-06 14:45:09,575 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:45:09,575 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:00:50.087251, Left till expiry: 0:09:09.424469, Loop Count: 11
2015-08-06 14:45:14,584 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:45:14,584 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:00:55.096669, Left till expiry: 0:09:04.415051, Loop Count: 12
2015-08-06 14:45:19,593 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:45:19,594 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:01:00.105757, Left till expiry: 0:08:59.405964, Loop Count: 13
2015-08-06 14:45:24,601 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:45:24,601 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:01:05.112871, Left till expiry: 0:08:54.398849, Loop Count: 14
2015-08-06 14:45:29,611 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:45:29,611 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:01:10.123142, Left till expiry: 0:08:49.388579, Loop Count: 15
2015-08-06 14:45:34,616 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:45:34,616 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:01:15.128426, Left till expiry: 0:08:44.383295, Loop Count: 16
2015-08-06 14:45:39,621 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:45:39,621 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:01:20.133469, Left till expiry: 0:08:39.378251, Loop Count: 17
2015-08-06 14:45:44,629 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:45:44,629 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:01:25.141401, Left till expiry: 0:08:34.370319, Loop Count: 18
2015-08-06 14:45:49,640 DEBUG    pytan.handler.QuestionPoller: ID 86248: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 844
2015-08-06 14:45:49,640 DEBUG    pytan.handler.QuestionPoller: ID 86248: Timing: Started: 2015-08-06 14:44:19.488282, Expiration: 2015-08-06 14:54:19, Override Timeout: None, Elapsed Time: 0:01:30.152555, Left till expiry: 0:08:29.359165, Loop Count: 19
2015-08-06 14:45:49,640 INFO     pytan.handler.QuestionPoller: ID 86248: Progress Changed 100% (2 of 2)
2015-08-06 14:45:49,640 INFO     pytan.handler.QuestionPoller: ID 86248: Reached Threshold of 99% (2 of 2)

Type of response:  <type 'dict'>

Pretty print of response:
{'poller_object': <pytan.pollers.QuestionPoller object at 0x10fc5f290>,
 'poller_success': True,
 'question_object': <taniumpy.object_types.question.Question object at 0x10fc5f090>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10fc74090>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] from all machines

CSV Results of response: 
"Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*]"
C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2674319\ServicePack\1033_enu_lp\x64\setup\sqlsupport_msi\windows\winsxs\5z1v718o.6n8
C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2958429\ServicePack\1033_enu_lp\x64\setup\sqlsupport_msi\windows\winsxs\92rg91xw.1p4
C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2958429\ServicePack\1033_enu_lp\x64\setup\sqlsupport_msi\windows\winsxs\policies\u1sw1o0k.9hi
C:\Program Files\VMware\VMware Tools\plugins\vmsvc
C:\Program Files\Common Files\Microsoft Shared\VS7Debug
C:\Program Files\Tanium\Tanium Server\Apache24\manual\style
C:\Program Files\Tanium\Tanium Server\ApacheBackup2015-05-15-15-44-27\manual\images
C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2674319\ServicePack\1033_enu_lp\x64\setup\sqlsupport_msi\windows\winsxs\vlv6b2rp.6fi
C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20150306_224415\resources
C:\Program Files\Tanium\Tanium Server\Apache24\htdocs\console\history
C:\Program Files\Windows Portable Devices
C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2977326\GDR\1033_enu_lp\x64\setup\sqlsupport_msi\pfiles\sqlservr\110\keyfile
C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2674319\ServicePack\1033_enu_lp\x64\setup\sql_engine_core_inst_loc_msi
C:\Program Files\Common Files\VMware\Drivers\vmci\sockets\include
..trimmed for brevity..

'''
