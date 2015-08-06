
"""
Export a ResultSet from asking a question as CSV with false for header_add_sensor
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
export_kwargs["header_add_sensor"] = False

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
2015-08-06 15:13:02,694 DEBUG    pytan.handler.QuestionPoller: ID 86292: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:13:02,694 DEBUG    pytan.handler.QuestionPoller: ID 86292: Timing: Started: 2015-08-06 15:12:42.640787, Expiration: 2015-08-06 15:22:42, Override Timeout: None, Elapsed Time: 0:00:20.054123, Left till expiry: 0:09:39.305092, Loop Count: 5
2015-08-06 15:13:07,707 DEBUG    pytan.handler.QuestionPoller: ID 86292: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:13:07,707 DEBUG    pytan.handler.QuestionPoller: ID 86292: Timing: Started: 2015-08-06 15:12:42.640787, Expiration: 2015-08-06 15:22:42, Override Timeout: None, Elapsed Time: 0:00:25.066558, Left till expiry: 0:09:34.292657, Loop Count: 6
2015-08-06 15:13:12,718 DEBUG    pytan.handler.QuestionPoller: ID 86292: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:13:12,718 DEBUG    pytan.handler.QuestionPoller: ID 86292: Timing: Started: 2015-08-06 15:12:42.640787, Expiration: 2015-08-06 15:22:42, Override Timeout: None, Elapsed Time: 0:00:30.078041, Left till expiry: 0:09:29.281174, Loop Count: 7
2015-08-06 15:13:17,725 DEBUG    pytan.handler.QuestionPoller: ID 86292: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:13:17,725 DEBUG    pytan.handler.QuestionPoller: ID 86292: Timing: Started: 2015-08-06 15:12:42.640787, Expiration: 2015-08-06 15:22:42, Override Timeout: None, Elapsed Time: 0:00:35.084832, Left till expiry: 0:09:24.274383, Loop Count: 8
2015-08-06 15:13:22,736 DEBUG    pytan.handler.QuestionPoller: ID 86292: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:13:22,736 DEBUG    pytan.handler.QuestionPoller: ID 86292: Timing: Started: 2015-08-06 15:12:42.640787, Expiration: 2015-08-06 15:22:42, Override Timeout: None, Elapsed Time: 0:00:40.095914, Left till expiry: 0:09:19.263303, Loop Count: 9
2015-08-06 15:13:27,749 DEBUG    pytan.handler.QuestionPoller: ID 86292: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:13:27,749 DEBUG    pytan.handler.QuestionPoller: ID 86292: Timing: Started: 2015-08-06 15:12:42.640787, Expiration: 2015-08-06 15:22:42, Override Timeout: None, Elapsed Time: 0:00:45.109134, Left till expiry: 0:09:14.250082, Loop Count: 10
2015-08-06 15:13:32,760 DEBUG    pytan.handler.QuestionPoller: ID 86292: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:13:32,760 DEBUG    pytan.handler.QuestionPoller: ID 86292: Timing: Started: 2015-08-06 15:12:42.640787, Expiration: 2015-08-06 15:22:42, Override Timeout: None, Elapsed Time: 0:00:50.120137, Left till expiry: 0:09:09.239078, Loop Count: 11
2015-08-06 15:13:37,774 DEBUG    pytan.handler.QuestionPoller: ID 86292: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
2015-08-06 15:13:37,774 DEBUG    pytan.handler.QuestionPoller: ID 86292: Timing: Started: 2015-08-06 15:12:42.640787, Expiration: 2015-08-06 15:22:42, Override Timeout: None, Elapsed Time: 0:00:55.133597, Left till expiry: 0:09:04.225619, Loop Count: 12
2015-08-06 15:13:37,774 INFO     pytan.handler.QuestionPoller: ID 86292: Progress Changed 100% (2 of 2)
2015-08-06 15:13:37,774 INFO     pytan.handler.QuestionPoller: ID 86292: Reached Threshold of 99% (2 of 2)

print the export_str returned from export_obj():
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
2015-08-06 15:11:06,894 DEBUG    pytan.handler.QuestionPoller: ID 86290: id resolved to 86290
2015-08-06 15:11:06,894 DEBUG    pytan.handler.QuestionPoller: ID 86290: expiration resolved to 2015-08-06T15:21:06
2015-08-06 15:11:06,894 DEBUG    pytan.handler.QuestionPoller: ID 86290: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 15:11:06,894 DEBUG    pytan.handler.QuestionPoller: ID 86290: id resolved to 86290
2015-08-06 15:11:06,894 DEBUG    pytan.handler.QuestionPoller: ID 86290: Object Info resolved to Question ID: 86290, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 15:11:06,898 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:11:06,898 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:00:00.004455, Left till expiry: 0:09:59.101312, Loop Count: 1
2015-08-06 15:11:06,898 INFO     pytan.handler.QuestionPoller: ID 86290: Progress Changed 0% (0 of 2)
2015-08-06 15:11:11,908 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:11:11,908 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:00:05.014495, Left till expiry: 0:09:54.091273, Loop Count: 2
2015-08-06 15:11:16,919 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:11:16,919 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:00:10.025055, Left till expiry: 0:09:49.080713, Loop Count: 3
2015-08-06 15:11:21,929 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:11:21,929 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:00:15.035633, Left till expiry: 0:09:44.070135, Loop Count: 4
..trimmed for brevity..

'''
