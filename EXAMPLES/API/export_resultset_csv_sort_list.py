
"""
Export a ResultSet from asking a question as CSV with Computer Name and IP Address for the header_sort
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

# setup the export_obj kwargs for later
export_kwargs = {}
export_kwargs["export_format"] = u'csv'
export_kwargs["header_sort"] = [u'Computer Name', u'IP Address']

# ask the question that will provide the resultset that we want to use
ask_kwargs = {
    'qtype': 'manual',
    'sensors': [
        "Computer Name", "IP Route Details", "IP Address",
        'Folder Name Search with RegEx Match{dirname=Program Files,regex=.*Shared.*}',
    ],
}
response = handler.ask(**ask_kwargs)

# export the object to a string
# (we could just as easily export to a file using export_to_report_file)
export_kwargs['obj'] = response['question_results']
export_str = handler.export_obj(**export_kwargs)


print ""
print "print the export_str returned from export_obj():"
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\n'.join(out)

print out


'''Output from running this:
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
2015-08-07 19:52:51,388 DEBUG    pytan.handler.QuestionPoller: ID 1316: id resolved to 1316
2015-08-07 19:52:51,388 DEBUG    pytan.handler.QuestionPoller: ID 1316: expiration resolved to 2015-08-07T20:02:51
2015-08-07 19:52:51,388 DEBUG    pytan.handler.QuestionPoller: ID 1316: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
2015-08-07 19:52:51,388 DEBUG    pytan.handler.QuestionPoller: ID 1316: id resolved to 1316
2015-08-07 19:52:51,388 DEBUG    pytan.handler.QuestionPoller: ID 1316: Object Info resolved to Question ID: 1316, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
2015-08-07 19:52:51,392 DEBUG    pytan.handler.QuestionPoller: ID 1316: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:52:51,392 DEBUG    pytan.handler.QuestionPoller: ID 1316: Timing: Started: 2015-08-07 19:52:51.388838, Expiration: 2015-08-07 20:02:51, Override Timeout: None, Elapsed Time: 0:00:00.003893, Left till expiry: 0:09:59.607272, Loop Count: 1
2015-08-07 19:52:51,392 INFO     pytan.handler.QuestionPoller: ID 1316: Progress Changed 0% (0 of 2)
2015-08-07 19:52:56,396 DEBUG    pytan.handler.QuestionPoller: ID 1316: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:52:56,396 DEBUG    pytan.handler.QuestionPoller: ID 1316: Timing: Started: 2015-08-07 19:52:51.388838, Expiration: 2015-08-07 20:02:51, Override Timeout: None, Elapsed Time: 0:00:05.007914, Left till expiry: 0:09:54.603251, Loop Count: 2
2015-08-07 19:53:01,404 DEBUG    pytan.handler.QuestionPoller: ID 1316: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:53:01,404 DEBUG    pytan.handler.QuestionPoller: ID 1316: Timing: Started: 2015-08-07 19:52:51.388838, Expiration: 2015-08-07 20:02:51, Override Timeout: None, Elapsed Time: 0:00:10.015872, Left till expiry: 0:09:49.595292, Loop Count: 3
2015-08-07 19:53:06,413 DEBUG    pytan.handler.QuestionPoller: ID 1316: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
2015-08-07 19:53:06,413 DEBUG    pytan.handler.QuestionPoller: ID 1316: Timing: Started: 2015-08-07 19:52:51.388838, Expiration: 2015-08-07 20:02:51, Override Timeout: None, Elapsed Time: 0:00:15.024914, Left till expiry: 0:09:44.586250, Loop Count: 4
2015-08-07 19:53:06,413 INFO     pytan.handler.QuestionPoller: ID 1316: Progress Changed 50% (1 of 2)
2015-08-07 19:53:11,418 DEBUG    pytan.handler.QuestionPoller: ID 1316: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
2015-08-07 19:53:11,419 DEBUG    pytan.handler.QuestionPoller: ID 1316: Timing: Started: 2015-08-07 19:52:51.388838, Expiration: 2015-08-07 20:02:51, Override Timeout: None, Elapsed Time: 0:00:20.030239, Left till expiry: 0:09:39.580926, Loop Count: 5
2015-08-07 19:53:11,419 INFO     pytan.handler.QuestionPoller: ID 1316: Progress Changed 100% (2 of 2)
2015-08-07 19:53:11,419 INFO     pytan.handler.QuestionPoller: ID 1316: Reached Threshold of 99% (2 of 2)

print the export_str returned from export_obj():
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
2015-08-07 19:52:21,243 DEBUG    pytan.handler.QuestionPoller: ID 1315: id resolved to 1315
2015-08-07 19:52:21,243 DEBUG    pytan.handler.QuestionPoller: ID 1315: expiration resolved to 2015-08-07T20:02:21
2015-08-07 19:52:21,243 DEBUG    pytan.handler.QuestionPoller: ID 1315: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
2015-08-07 19:52:21,243 DEBUG    pytan.handler.QuestionPoller: ID 1315: id resolved to 1315
2015-08-07 19:52:21,243 DEBUG    pytan.handler.QuestionPoller: ID 1315: Object Info resolved to Question ID: 1315, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
2015-08-07 19:52:21,246 DEBUG    pytan.handler.QuestionPoller: ID 1315: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:52:21,246 DEBUG    pytan.handler.QuestionPoller: ID 1315: Timing: Started: 2015-08-07 19:52:21.243267, Expiration: 2015-08-07 20:02:21, Override Timeout: None, Elapsed Time: 0:00:00.003479, Left till expiry: 0:09:59.753257, Loop Count: 1
2015-08-07 19:52:21,246 INFO     pytan.handler.QuestionPoller: ID 1315: Progress Changed 0% (0 of 2)
2015-08-07 19:52:26,251 DEBUG    pytan.handler.QuestionPoller: ID 1315: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:52:26,251 DEBUG    pytan.handler.QuestionPoller: ID 1315: Timing: Started: 2015-08-07 19:52:21.243267, Expiration: 2015-08-07 20:02:21, Override Timeout: None, Elapsed Time: 0:00:05.007825, Left till expiry: 0:09:54.748911, Loop Count: 2
2015-08-07 19:52:31,255 DEBUG    pytan.handler.QuestionPoller: ID 1315: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:52:31,255 DEBUG    pytan.handler.QuestionPoller: ID 1315: Timing: Started: 2015-08-07 19:52:21.243267, Expiration: 2015-08-07 20:02:21, Override Timeout: None, Elapsed Time: 0:00:10.012556, Left till expiry: 0:09:49.744181, Loop Count: 3
2015-08-07 19:52:36,264 DEBUG    pytan.handler.QuestionPoller: ID 1315: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
2015-08-07 19:52:36,264 DEBUG    pytan.handler.QuestionPoller: ID 1315: Timing: Started: 2015-08-07 19:52:21.243267, Expiration: 2015-08-07 20:02:21, Override Timeout: None, Elapsed Time: 0:00:15.020856, Left till expiry: 0:09:44.735880, Loop Count: 4
..trimmed for brevity..

'''
