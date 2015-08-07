
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
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
2015-08-07 19:42:06,009 DEBUG    pytan.handler.QuestionPoller: ID 1288: id resolved to 1288
2015-08-07 19:42:06,010 DEBUG    pytan.handler.QuestionPoller: ID 1288: expiration resolved to 2015-08-07T19:52:06
2015-08-07 19:42:06,010 DEBUG    pytan.handler.QuestionPoller: ID 1288: query_text resolved to Get Folder Name Search with RegEx Match[, , No, No] from all machines
2015-08-07 19:42:06,010 DEBUG    pytan.handler.QuestionPoller: ID 1288: id resolved to 1288
2015-08-07 19:42:06,010 DEBUG    pytan.handler.QuestionPoller: ID 1288: Object Info resolved to Question ID: 1288, Query: Get Folder Name Search with RegEx Match[, , No, No] from all machines
2015-08-07 19:42:06,013 DEBUG    pytan.handler.QuestionPoller: ID 1288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:42:06,013 DEBUG    pytan.handler.QuestionPoller: ID 1288: Timing: Started: 2015-08-07 19:42:06.010216, Expiration: 2015-08-07 19:52:06, Override Timeout: None, Elapsed Time: 0:00:00.003035, Left till expiry: 0:09:59.986751, Loop Count: 1
2015-08-07 19:42:06,013 INFO     pytan.handler.QuestionPoller: ID 1288: Progress Changed 0% (0 of 2)
2015-08-07 19:42:11,021 DEBUG    pytan.handler.QuestionPoller: ID 1288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:42:11,021 DEBUG    pytan.handler.QuestionPoller: ID 1288: Timing: Started: 2015-08-07 19:42:06.010216, Expiration: 2015-08-07 19:52:06, Override Timeout: None, Elapsed Time: 0:00:05.011720, Left till expiry: 0:09:54.978067, Loop Count: 2
2015-08-07 19:42:16,025 DEBUG    pytan.handler.QuestionPoller: ID 1288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:42:16,025 DEBUG    pytan.handler.QuestionPoller: ID 1288: Timing: Started: 2015-08-07 19:42:06.010216, Expiration: 2015-08-07 19:52:06, Override Timeout: None, Elapsed Time: 0:00:10.014927, Left till expiry: 0:09:49.974860, Loop Count: 3
2015-08-07 19:42:21,032 DEBUG    pytan.handler.QuestionPoller: ID 1288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:42:21,032 DEBUG    pytan.handler.QuestionPoller: ID 1288: Timing: Started: 2015-08-07 19:42:06.010216, Expiration: 2015-08-07 19:52:06, Override Timeout: None, Elapsed Time: 0:00:15.022585, Left till expiry: 0:09:44.967202, Loop Count: 4
2015-08-07 19:42:26,037 DEBUG    pytan.handler.QuestionPoller: ID 1288: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 1001
2015-08-07 19:42:26,037 DEBUG    pytan.handler.QuestionPoller: ID 1288: Timing: Started: 2015-08-07 19:42:06.010216, Expiration: 2015-08-07 19:52:06, Override Timeout: None, Elapsed Time: 0:00:20.027742, Left till expiry: 0:09:39.962045, Loop Count: 5
2015-08-07 19:42:26,038 INFO     pytan.handler.QuestionPoller: ID 1288: Progress Changed 100% (2 of 2)
2015-08-07 19:42:26,038 INFO     pytan.handler.QuestionPoller: ID 1288: Reached Threshold of 99% (2 of 2)

Type of response:  <type 'dict'>

Pretty print of response:
{'poller_object': <pytan.pollers.QuestionPoller object at 0x10a6147d0>,
 'poller_success': True,
 'question_object': <taniumpy.object_types.question.Question object at 0x10a613790>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10a5f5190>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Folder Name Search with RegEx Match[, , No, No] from all machines

CSV Results of response: 
Count,"Folder Name Search with RegEx Match[, , No, No]"
24705,[too many results]
1,C:\Windows\winsxs\amd64_microsoft-windows-s..structure.resources_31bf3856ad364e35_6.1.7600.16385_en-us_faf46e6f502e00e8
1,C:\Windows\winsxs\x86_microsoft-windows-e..-host-authenticator_31bf3856ad364e35_6.1.7601.17514_none_a7c68343f07f776f
1,C:\Windows\winsxs\amd64_microsoft-windows-ocspsvc_31bf3856ad364e35_6.1.7601.22807_none_3bfeae7293092e4b
1,C:\Windows\winsxs\amd64_microsoft-windows-c..ityclient.resources_31bf3856ad364e35_6.1.7601.22865_en-us_c339d6d6cfb99c39
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\System.Xml
1,C:\Windows\winsxs\amd64_microsoft-windows-winsetupui_31bf3856ad364e35_6.1.7601.18804_none_bd3cf1bbdc424e8d
1,C:\Windows\winsxs\amd64_microsoft-windows-scripting.resources_31bf3856ad364e35_6.1.7600.16385_en-us_e72192b67124ad43
1,C:\Windows\winsxs\x86_microsoft-windows-mlang.resources_31bf3856ad364e35_6.1.7600.16385_ru-ru_cf3a10abc52740f6
1,C:\Windows\winsxs\x86_microsoft-windows-minkernelapinamespace_31bf3856ad364e35_6.1.7601.21728_none_0d3c29cef3342a85
1,C:\Users\Jim Olsen\AppData\Local\Google
1,C:\Windows\winsxs\x86_microsoft-windows-e..nt-client.resources_31bf3856ad364e35_6.1.7600.16385_en-us_e5c3d3ec6ff64de3
1,C:\Windows\winsxs\amd64_microsoft-windows-d..e-eashared-kjshared_31bf3856ad364e35_6.1.7600.16385_none_99b74194b7347cab
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\RadLangSvc
..trimmed for brevity..

'''
