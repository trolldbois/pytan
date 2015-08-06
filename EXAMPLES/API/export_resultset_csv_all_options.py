
"""
Export a ResultSet from asking a question as CSV with true for header_add_sensor, true for header_add_type, true for header_sort, and true for expand_grouped_columns
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
export_kwargs["header_sort"] = True
export_kwargs["export_format"] = u'csv'
export_kwargs["header_add_type"] = True
export_kwargs["expand_grouped_columns"] = True
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
2015-08-06 15:02:42,946 DEBUG    pytan.handler.QuestionPoller: ID 86279: id resolved to 86279
2015-08-06 15:02:42,946 DEBUG    pytan.handler.QuestionPoller: ID 86279: expiration resolved to 2015-08-06T15:12:43
2015-08-06 15:02:42,946 DEBUG    pytan.handler.QuestionPoller: ID 86279: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 15:02:42,946 DEBUG    pytan.handler.QuestionPoller: ID 86279: id resolved to 86279
2015-08-06 15:02:42,946 DEBUG    pytan.handler.QuestionPoller: ID 86279: Object Info resolved to Question ID: 86279, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 15:02:42,951 DEBUG    pytan.handler.QuestionPoller: ID 86279: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:02:42,951 DEBUG    pytan.handler.QuestionPoller: ID 86279: Timing: Started: 2015-08-06 15:02:42.946585, Expiration: 2015-08-06 15:12:43, Override Timeout: None, Elapsed Time: 0:00:00.005325, Left till expiry: 0:10:00.048093, Loop Count: 1
2015-08-06 15:02:42,951 INFO     pytan.handler.QuestionPoller: ID 86279: Progress Changed 0% (0 of 2)
2015-08-06 15:02:47,959 DEBUG    pytan.handler.QuestionPoller: ID 86279: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:02:47,959 DEBUG    pytan.handler.QuestionPoller: ID 86279: Timing: Started: 2015-08-06 15:02:42.946585, Expiration: 2015-08-06 15:12:43, Override Timeout: None, Elapsed Time: 0:00:05.013313, Left till expiry: 0:09:55.040105, Loop Count: 2
2015-08-06 15:02:52,969 DEBUG    pytan.handler.QuestionPoller: ID 86279: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:02:52,969 DEBUG    pytan.handler.QuestionPoller: ID 86279: Timing: Started: 2015-08-06 15:02:42.946585, Expiration: 2015-08-06 15:12:43, Override Timeout: None, Elapsed Time: 0:00:10.023090, Left till expiry: 0:09:50.030328, Loop Count: 3
2015-08-06 15:02:57,978 DEBUG    pytan.handler.QuestionPoller: ID 86279: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:02:57,978 DEBUG    pytan.handler.QuestionPoller: ID 86279: Timing: Started: 2015-08-06 15:02:42.946585, Expiration: 2015-08-06 15:12:43, Override Timeout: None, Elapsed Time: 0:00:15.032072, Left till expiry: 0:09:45.021346, Loop Count: 4
2015-08-06 15:03:02,987 DEBUG    pytan.handler.QuestionPoller: ID 86279: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:03:02,987 DEBUG    pytan.handler.QuestionPoller: ID 86279: Timing: Started: 2015-08-06 15:02:42.946585, Expiration: 2015-08-06 15:12:43, Override Timeout: None, Elapsed Time: 0:00:20.040955, Left till expiry: 0:09:40.012464, Loop Count: 5
2015-08-06 15:03:07,995 DEBUG    pytan.handler.QuestionPoller: ID 86279: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:03:07,995 DEBUG    pytan.handler.QuestionPoller: ID 86279: Timing: Started: 2015-08-06 15:02:42.946585, Expiration: 2015-08-06 15:12:43, Override Timeout: None, Elapsed Time: 0:00:25.048582, Left till expiry: 0:09:35.004836, Loop Count: 6
2015-08-06 15:03:13,006 DEBUG    pytan.handler.QuestionPoller: ID 86279: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
2015-08-06 15:03:13,006 DEBUG    pytan.handler.QuestionPoller: ID 86279: Timing: Started: 2015-08-06 15:02:42.946585, Expiration: 2015-08-06 15:12:43, Override Timeout: None, Elapsed Time: 0:00:30.059814, Left till expiry: 0:09:29.993603, Loop Count: 7
2015-08-06 15:03:13,006 INFO     pytan.handler.QuestionPoller: ID 86279: Progress Changed 100% (2 of 2)
2015-08-06 15:03:13,006 INFO     pytan.handler.QuestionPoller: ID 86279: Reached Threshold of 99% (2 of 2)

print the export_str returned from export_obj():
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
2015-08-06 14:58:37,302 DEBUG    pytan.handler.QuestionPoller: ID 86277: id resolved to 86277
2015-08-06 14:58:37,302 DEBUG    pytan.handler.QuestionPoller: ID 86277: expiration resolved to 2015-08-06T15:08:37
2015-08-06 14:58:37,302 DEBUG    pytan.handler.QuestionPoller: ID 86277: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 14:58:37,302 DEBUG    pytan.handler.QuestionPoller: ID 86277: id resolved to 86277
2015-08-06 14:58:37,302 DEBUG    pytan.handler.QuestionPoller: ID 86277: Object Info resolved to Question ID: 86277, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 14:58:37,307 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:58:37,307 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:00:00.004670, Left till expiry: 0:09:59.692356, Loop Count: 1
2015-08-06 14:58:37,307 INFO     pytan.handler.QuestionPoller: ID 86277: Progress Changed 0% (0 of 2)
2015-08-06 14:58:42,316 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:58:42,316 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:00:05.013225, Left till expiry: 0:09:54.683801, Loop Count: 2
2015-08-06 14:58:47,321 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:58:47,321 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:00:10.018281, Left till expiry: 0:09:49.678744, Loop Count: 3
2015-08-06 14:58:52,332 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:58:52,332 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:00:15.029218, Left till expiry: 0:09:44.667808, Loop Count: 4
..trimmed for brevity..

'''
