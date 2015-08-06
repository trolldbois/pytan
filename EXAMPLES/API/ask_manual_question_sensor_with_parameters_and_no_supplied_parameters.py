
"""
Ask a manual question using human strings by referencing the name of a single sensor that takes parameters, but not supplying any parameters (and letting pytan automatically determine the appropriate default value for those parameters which require a value).

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
kwargs["sensors"] = u'Folder Name Search with RegEx Match'
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
2015-08-06 14:46:47,125 DEBUG    pytan.handler.QuestionPoller: ID 86253: id resolved to 86253
2015-08-06 14:46:47,125 DEBUG    pytan.handler.QuestionPoller: ID 86253: expiration resolved to 2015-08-06T14:56:47
2015-08-06 14:46:47,125 DEBUG    pytan.handler.QuestionPoller: ID 86253: query_text resolved to Get Folder Name Search with RegEx Match[No, , No, ] from all machines
2015-08-06 14:46:47,125 DEBUG    pytan.handler.QuestionPoller: ID 86253: id resolved to 86253
2015-08-06 14:46:47,125 DEBUG    pytan.handler.QuestionPoller: ID 86253: Object Info resolved to Question ID: 86253, Query: Get Folder Name Search with RegEx Match[No, , No, ] from all machines
2015-08-06 14:46:47,131 DEBUG    pytan.handler.QuestionPoller: ID 86253: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:46:47,131 DEBUG    pytan.handler.QuestionPoller: ID 86253: Timing: Started: 2015-08-06 14:46:47.125988, Expiration: 2015-08-06 14:56:47, Override Timeout: None, Elapsed Time: 0:00:00.005140, Left till expiry: 0:09:59.868874, Loop Count: 1
2015-08-06 14:46:47,131 INFO     pytan.handler.QuestionPoller: ID 86253: Progress Changed 0% (0 of 2)
2015-08-06 14:46:52,139 DEBUG    pytan.handler.QuestionPoller: ID 86253: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:46:52,139 DEBUG    pytan.handler.QuestionPoller: ID 86253: Timing: Started: 2015-08-06 14:46:47.125988, Expiration: 2015-08-06 14:56:47, Override Timeout: None, Elapsed Time: 0:00:05.013752, Left till expiry: 0:09:54.860262, Loop Count: 2
2015-08-06 14:46:57,146 DEBUG    pytan.handler.QuestionPoller: ID 86253: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:46:57,146 DEBUG    pytan.handler.QuestionPoller: ID 86253: Timing: Started: 2015-08-06 14:46:47.125988, Expiration: 2015-08-06 14:56:47, Override Timeout: None, Elapsed Time: 0:00:10.020160, Left till expiry: 0:09:49.853854, Loop Count: 3
2015-08-06 14:47:02,156 DEBUG    pytan.handler.QuestionPoller: ID 86253: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:47:02,156 DEBUG    pytan.handler.QuestionPoller: ID 86253: Timing: Started: 2015-08-06 14:46:47.125988, Expiration: 2015-08-06 14:56:47, Override Timeout: None, Elapsed Time: 0:00:15.030391, Left till expiry: 0:09:44.843623, Loop Count: 4
2015-08-06 14:47:07,161 DEBUG    pytan.handler.QuestionPoller: ID 86253: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:47:07,161 DEBUG    pytan.handler.QuestionPoller: ID 86253: Timing: Started: 2015-08-06 14:46:47.125988, Expiration: 2015-08-06 14:56:47, Override Timeout: None, Elapsed Time: 0:00:20.035588, Left till expiry: 0:09:39.838427, Loop Count: 5
2015-08-06 14:47:12,168 DEBUG    pytan.handler.QuestionPoller: ID 86253: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:47:12,168 DEBUG    pytan.handler.QuestionPoller: ID 86253: Timing: Started: 2015-08-06 14:46:47.125988, Expiration: 2015-08-06 14:56:47, Override Timeout: None, Elapsed Time: 0:00:25.042624, Left till expiry: 0:09:34.831390, Loop Count: 6
2015-08-06 14:47:17,175 DEBUG    pytan.handler.QuestionPoller: ID 86253: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:47:17,175 DEBUG    pytan.handler.QuestionPoller: ID 86253: Timing: Started: 2015-08-06 14:46:47.125988, Expiration: 2015-08-06 14:56:47, Override Timeout: None, Elapsed Time: 0:00:30.049590, Left till expiry: 0:09:29.824425, Loop Count: 7
2015-08-06 14:47:22,180 DEBUG    pytan.handler.QuestionPoller: ID 86253: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:47:22,180 DEBUG    pytan.handler.QuestionPoller: ID 86253: Timing: Started: 2015-08-06 14:46:47.125988, Expiration: 2015-08-06 14:56:47, Override Timeout: None, Elapsed Time: 0:00:35.054692, Left till expiry: 0:09:24.819322, Loop Count: 8
2015-08-06 14:47:27,187 DEBUG    pytan.handler.QuestionPoller: ID 86253: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:47:27,187 DEBUG    pytan.handler.QuestionPoller: ID 86253: Timing: Started: 2015-08-06 14:46:47.125988, Expiration: 2015-08-06 14:56:47, Override Timeout: None, Elapsed Time: 0:00:40.061717, Left till expiry: 0:09:19.812297, Loop Count: 9
2015-08-06 14:47:32,196 DEBUG    pytan.handler.QuestionPoller: ID 86253: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:47:32,196 DEBUG    pytan.handler.QuestionPoller: ID 86253: Timing: Started: 2015-08-06 14:46:47.125988, Expiration: 2015-08-06 14:56:47, Override Timeout: None, Elapsed Time: 0:00:45.070995, Left till expiry: 0:09:14.803019, Loop Count: 10
2015-08-06 14:47:37,206 DEBUG    pytan.handler.QuestionPoller: ID 86253: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:47:37,206 DEBUG    pytan.handler.QuestionPoller: ID 86253: Timing: Started: 2015-08-06 14:46:47.125988, Expiration: 2015-08-06 14:56:47, Override Timeout: None, Elapsed Time: 0:00:50.080398, Left till expiry: 0:09:09.793616, Loop Count: 11
2015-08-06 14:47:42,216 DEBUG    pytan.handler.QuestionPoller: ID 86253: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
2015-08-06 14:47:42,216 DEBUG    pytan.handler.QuestionPoller: ID 86253: Timing: Started: 2015-08-06 14:46:47.125988, Expiration: 2015-08-06 14:56:47, Override Timeout: None, Elapsed Time: 0:00:55.090311, Left till expiry: 0:09:04.783703, Loop Count: 12
2015-08-06 14:47:42,216 INFO     pytan.handler.QuestionPoller: ID 86253: Progress Changed 50% (1 of 2)
2015-08-06 14:47:47,226 DEBUG    pytan.handler.QuestionPoller: ID 86253: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
2015-08-06 14:47:47,226 DEBUG    pytan.handler.QuestionPoller: ID 86253: Timing: Started: 2015-08-06 14:46:47.125988, Expiration: 2015-08-06 14:56:47, Override Timeout: None, Elapsed Time: 0:01:00.100332, Left till expiry: 0:08:59.773685, Loop Count: 13
2015-08-06 14:47:52,233 DEBUG    pytan.handler.QuestionPoller: ID 86253: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 1001
2015-08-06 14:47:52,233 DEBUG    pytan.handler.QuestionPoller: ID 86253: Timing: Started: 2015-08-06 14:46:47.125988, Expiration: 2015-08-06 14:56:47, Override Timeout: None, Elapsed Time: 0:01:05.107927, Left till expiry: 0:08:54.766088, Loop Count: 14
2015-08-06 14:47:52,233 INFO     pytan.handler.QuestionPoller: ID 86253: Progress Changed 100% (2 of 2)
2015-08-06 14:47:52,234 INFO     pytan.handler.QuestionPoller: ID 86253: Reached Threshold of 99% (2 of 2)

Type of response:  <type 'dict'>

Pretty print of response:
{'poller_object': <pytan.pollers.QuestionPoller object at 0x10fc74950>,
 'poller_success': True,
 'question_object': <taniumpy.object_types.question.Question object at 0x10fc5f0d0>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x1113addd0>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Folder Name Search with RegEx Match[No, , No, ] from all machines

CSV Results of response: 
Count,"Folder Name Search with RegEx Match[No, , No, ]"
24534,[too many results]
1,C:\Windows\winsxs\amd64_microsoft-windows-s..structure.resources_31bf3856ad364e35_6.1.7600.16385_en-us_faf46e6f502e00e8
1,C:\Windows\winsxs\x86_microsoft-windows-e..-host-authenticator_31bf3856ad364e35_6.1.7601.17514_none_a7c68343f07f776f
1,C:\Windows\winsxs\amd64_microsoft-windows-ocspsvc_31bf3856ad364e35_6.1.7601.22807_none_3bfeae7293092e4b
1,C:\Windows\winsxs\amd64_microsoft-windows-c..ityclient.resources_31bf3856ad364e35_6.1.7601.22865_en-us_c339d6d6cfb99c39
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2674319\ServicePack\1033_enu_lp\x64\setup\sqlsupport_msi\windows\winsxs\5z1v718o.6n8
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\System.Xml
1,C:\Windows\winsxs\amd64_microsoft-windows-scripting.resources_31bf3856ad364e35_6.1.7600.16385_en-us_e72192b67124ad43
1,C:\Windows\winsxs\x86_microsoft-windows-mlang.resources_31bf3856ad364e35_6.1.7600.16385_ru-ru_cf3a10abc52740f6
1,C:\Windows\winsxs\amd64_microsoft-windows-ie-internetexplorer_31bf3856ad364e35_11.2.9600.17041_none_11e6f4b92ee9bf19
1,C:\Windows\Installer\$PatchCache$\Managed\1F1FFB6230C555C4C9C7DF5688A9AF07
1,C:\Program Files (x86)\Windows Defender
1,C:\Users\Jim Olsen\AppData\Local\Google
1,C:\Windows\winsxs\x86_microsoft-windows-e..nt-client.resources_31bf3856ad364e35_6.1.7600.16385_en-us_e5c3d3ec6ff64de3
..trimmed for brevity..

'''
