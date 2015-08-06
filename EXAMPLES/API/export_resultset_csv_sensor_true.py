
"""
Export a ResultSet from asking a question as CSV with true for header_add_sensor
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

# setup the export_obj kwargs for later
export_kwargs = {}
export_kwargs["export_format"] = u'csv'
export_kwargs["header_add_sensor"] = True

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
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
2015-08-06 15:13:38,096 DEBUG    pytan.handler.QuestionPoller: ID 86294: id resolved to 86294
2015-08-06 15:13:38,096 DEBUG    pytan.handler.QuestionPoller: ID 86294: expiration resolved to 2015-08-06T15:23:38
2015-08-06 15:13:38,096 DEBUG    pytan.handler.QuestionPoller: ID 86294: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 15:13:38,096 DEBUG    pytan.handler.QuestionPoller: ID 86294: id resolved to 86294
2015-08-06 15:13:38,096 DEBUG    pytan.handler.QuestionPoller: ID 86294: Object Info resolved to Question ID: 86294, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 15:13:38,101 DEBUG    pytan.handler.QuestionPoller: ID 86294: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:13:38,101 DEBUG    pytan.handler.QuestionPoller: ID 86294: Timing: Started: 2015-08-06 15:13:38.096863, Expiration: 2015-08-06 15:23:38, Override Timeout: None, Elapsed Time: 0:00:00.004952, Left till expiry: 0:09:59.898187, Loop Count: 1
2015-08-06 15:13:38,101 INFO     pytan.handler.QuestionPoller: ID 86294: Progress Changed 0% (0 of 2)
2015-08-06 15:13:43,111 DEBUG    pytan.handler.QuestionPoller: ID 86294: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:13:43,111 DEBUG    pytan.handler.QuestionPoller: ID 86294: Timing: Started: 2015-08-06 15:13:38.096863, Expiration: 2015-08-06 15:23:38, Override Timeout: None, Elapsed Time: 0:00:05.015012, Left till expiry: 0:09:54.888127, Loop Count: 2
2015-08-06 15:13:48,117 DEBUG    pytan.handler.QuestionPoller: ID 86294: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:13:48,117 DEBUG    pytan.handler.QuestionPoller: ID 86294: Timing: Started: 2015-08-06 15:13:38.096863, Expiration: 2015-08-06 15:23:38, Override Timeout: None, Elapsed Time: 0:00:10.020569, Left till expiry: 0:09:49.882570, Loop Count: 3
2015-08-06 15:13:53,127 DEBUG    pytan.handler.QuestionPoller: ID 86294: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:13:53,127 DEBUG    pytan.handler.QuestionPoller: ID 86294: Timing: Started: 2015-08-06 15:13:38.096863, Expiration: 2015-08-06 15:23:38, Override Timeout: None, Elapsed Time: 0:00:15.030793, Left till expiry: 0:09:44.872346, Loop Count: 4
2015-08-06 15:13:58,138 DEBUG    pytan.handler.QuestionPoller: ID 86294: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:13:58,138 DEBUG    pytan.handler.QuestionPoller: ID 86294: Timing: Started: 2015-08-06 15:13:38.096863, Expiration: 2015-08-06 15:23:38, Override Timeout: None, Elapsed Time: 0:00:20.041543, Left till expiry: 0:09:39.861596, Loop Count: 5
2015-08-06 15:14:03,151 DEBUG    pytan.handler.QuestionPoller: ID 86294: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
2015-08-06 15:14:03,151 DEBUG    pytan.handler.QuestionPoller: ID 86294: Timing: Started: 2015-08-06 15:13:38.096863, Expiration: 2015-08-06 15:23:38, Override Timeout: None, Elapsed Time: 0:00:25.054239, Left till expiry: 0:09:34.848901, Loop Count: 6
2015-08-06 15:14:03,151 INFO     pytan.handler.QuestionPoller: ID 86294: Progress Changed 100% (2 of 2)
2015-08-06 15:14:03,151 INFO     pytan.handler.QuestionPoller: ID 86294: Reached Threshold of 99% (2 of 2)

print the export_str returned from export_obj():
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
2015-08-06 15:12:42,640 DEBUG    pytan.handler.QuestionPoller: ID 86292: id resolved to 86292
2015-08-06 15:12:42,640 DEBUG    pytan.handler.QuestionPoller: ID 86292: expiration resolved to 2015-08-06T15:22:42
2015-08-06 15:12:42,640 DEBUG    pytan.handler.QuestionPoller: ID 86292: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 15:12:42,640 DEBUG    pytan.handler.QuestionPoller: ID 86292: id resolved to 86292
2015-08-06 15:12:42,640 DEBUG    pytan.handler.QuestionPoller: ID 86292: Object Info resolved to Question ID: 86292, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 15:12:42,645 DEBUG    pytan.handler.QuestionPoller: ID 86292: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:12:42,645 DEBUG    pytan.handler.QuestionPoller: ID 86292: Timing: Started: 2015-08-06 15:12:42.640787, Expiration: 2015-08-06 15:22:42, Override Timeout: None, Elapsed Time: 0:00:00.004914, Left till expiry: 0:09:59.354301, Loop Count: 1
2015-08-06 15:12:42,645 INFO     pytan.handler.QuestionPoller: ID 86292: Progress Changed 0% (0 of 2)
2015-08-06 15:12:47,658 DEBUG    pytan.handler.QuestionPoller: ID 86292: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:12:47,658 DEBUG    pytan.handler.QuestionPoller: ID 86292: Timing: Started: 2015-08-06 15:12:42.640787, Expiration: 2015-08-06 15:22:42, Override Timeout: None, Elapsed Time: 0:00:05.017741, Left till expiry: 0:09:54.341474, Loop Count: 2
2015-08-06 15:12:52,671 DEBUG    pytan.handler.QuestionPoller: ID 86292: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:12:52,671 DEBUG    pytan.handler.QuestionPoller: ID 86292: Timing: Started: 2015-08-06 15:12:42.640787, Expiration: 2015-08-06 15:22:42, Override Timeout: None, Elapsed Time: 0:00:10.031150, Left till expiry: 0:09:49.328065, Loop Count: 3
2015-08-06 15:12:57,685 DEBUG    pytan.handler.QuestionPoller: ID 86292: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:12:57,685 DEBUG    pytan.handler.QuestionPoller: ID 86292: Timing: Started: 2015-08-06 15:12:42.640787, Expiration: 2015-08-06 15:22:42, Override Timeout: None, Elapsed Time: 0:00:15.044509, Left till expiry: 0:09:44.314706, Loop Count: 4
..trimmed for brevity..

'''
