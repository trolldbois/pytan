
"""
Export a ResultSet from asking a question as CSV with false for expand_grouped_columns
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
export_kwargs["expand_grouped_columns"] = False

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
2015-08-06 14:58:11,791 DEBUG    pytan.handler.QuestionPoller: ID 86276: id resolved to 86276
2015-08-06 14:58:11,792 DEBUG    pytan.handler.QuestionPoller: ID 86276: expiration resolved to 2015-08-06T15:08:11
2015-08-06 14:58:11,792 DEBUG    pytan.handler.QuestionPoller: ID 86276: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 14:58:11,792 DEBUG    pytan.handler.QuestionPoller: ID 86276: id resolved to 86276
2015-08-06 14:58:11,792 DEBUG    pytan.handler.QuestionPoller: ID 86276: Object Info resolved to Question ID: 86276, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 14:58:11,797 DEBUG    pytan.handler.QuestionPoller: ID 86276: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:58:11,797 DEBUG    pytan.handler.QuestionPoller: ID 86276: Timing: Started: 2015-08-06 14:58:11.792215, Expiration: 2015-08-06 15:08:11, Override Timeout: None, Elapsed Time: 0:00:00.004865, Left till expiry: 0:09:59.202922, Loop Count: 1
2015-08-06 14:58:11,797 INFO     pytan.handler.QuestionPoller: ID 86276: Progress Changed 0% (0 of 2)
2015-08-06 14:58:16,802 DEBUG    pytan.handler.QuestionPoller: ID 86276: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:58:16,802 DEBUG    pytan.handler.QuestionPoller: ID 86276: Timing: Started: 2015-08-06 14:58:11.792215, Expiration: 2015-08-06 15:08:11, Override Timeout: None, Elapsed Time: 0:00:05.010000, Left till expiry: 0:09:54.197787, Loop Count: 2
2015-08-06 14:58:21,808 DEBUG    pytan.handler.QuestionPoller: ID 86276: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:58:21,808 DEBUG    pytan.handler.QuestionPoller: ID 86276: Timing: Started: 2015-08-06 14:58:11.792215, Expiration: 2015-08-06 15:08:11, Override Timeout: None, Elapsed Time: 0:00:10.016583, Left till expiry: 0:09:49.191204, Loop Count: 3
2015-08-06 14:58:26,816 DEBUG    pytan.handler.QuestionPoller: ID 86276: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:58:26,816 DEBUG    pytan.handler.QuestionPoller: ID 86276: Timing: Started: 2015-08-06 14:58:11.792215, Expiration: 2015-08-06 15:08:11, Override Timeout: None, Elapsed Time: 0:00:15.024291, Left till expiry: 0:09:44.183496, Loop Count: 4
2015-08-06 14:58:31,824 DEBUG    pytan.handler.QuestionPoller: ID 86276: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
2015-08-06 14:58:31,824 DEBUG    pytan.handler.QuestionPoller: ID 86276: Timing: Started: 2015-08-06 14:58:11.792215, Expiration: 2015-08-06 15:08:11, Override Timeout: None, Elapsed Time: 0:00:20.032629, Left till expiry: 0:09:39.175158, Loop Count: 5
2015-08-06 14:58:31,824 INFO     pytan.handler.QuestionPoller: ID 86276: Progress Changed 50% (1 of 2)
2015-08-06 14:58:36,834 DEBUG    pytan.handler.QuestionPoller: ID 86276: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
2015-08-06 14:58:36,834 DEBUG    pytan.handler.QuestionPoller: ID 86276: Timing: Started: 2015-08-06 14:58:11.792215, Expiration: 2015-08-06 15:08:11, Override Timeout: None, Elapsed Time: 0:00:25.042069, Left till expiry: 0:09:34.165718, Loop Count: 6
2015-08-06 14:58:36,834 INFO     pytan.handler.QuestionPoller: ID 86276: Progress Changed 100% (2 of 2)
2015-08-06 14:58:36,834 INFO     pytan.handler.QuestionPoller: ID 86276: Reached Threshold of 99% (2 of 2)

print the export_str returned from export_obj():
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
2015-08-06 14:56:11,294 DEBUG    pytan.handler.QuestionPoller: ID 86273: id resolved to 86273
2015-08-06 14:56:11,294 DEBUG    pytan.handler.QuestionPoller: ID 86273: expiration resolved to 2015-08-06T15:06:11
2015-08-06 14:56:11,294 DEBUG    pytan.handler.QuestionPoller: ID 86273: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 14:56:11,294 DEBUG    pytan.handler.QuestionPoller: ID 86273: id resolved to 86273
2015-08-06 14:56:11,294 DEBUG    pytan.handler.QuestionPoller: ID 86273: Object Info resolved to Question ID: 86273, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 14:56:11,299 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:56:11,300 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:00:00.005629, Left till expiry: 0:09:59.699962, Loop Count: 1
2015-08-06 14:56:11,300 INFO     pytan.handler.QuestionPoller: ID 86273: Progress Changed 0% (0 of 2)
2015-08-06 14:56:16,308 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:56:16,308 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:00:05.013748, Left till expiry: 0:09:54.691843, Loop Count: 2
2015-08-06 14:56:21,315 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:56:21,315 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:00:10.021539, Left till expiry: 0:09:49.684051, Loop Count: 3
2015-08-06 14:56:26,321 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:56:26,321 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:00:15.026771, Left till expiry: 0:09:44.678819, Loop Count: 4
..trimmed for brevity..

'''
