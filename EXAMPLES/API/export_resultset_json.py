
"""
Export a ResultSet from asking a question as JSON with the default options
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
export_kwargs["export_format"] = u'json'

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
2015-08-06 15:03:14,128 DEBUG    pytan.handler.QuestionPoller: ID 86281: id resolved to 86281
2015-08-06 15:03:14,128 DEBUG    pytan.handler.QuestionPoller: ID 86281: expiration resolved to 2015-08-06T15:13:14
2015-08-06 15:03:14,128 DEBUG    pytan.handler.QuestionPoller: ID 86281: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 15:03:14,128 DEBUG    pytan.handler.QuestionPoller: ID 86281: id resolved to 86281
2015-08-06 15:03:14,128 DEBUG    pytan.handler.QuestionPoller: ID 86281: Object Info resolved to Question ID: 86281, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 15:03:14,133 DEBUG    pytan.handler.QuestionPoller: ID 86281: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:03:14,133 DEBUG    pytan.handler.QuestionPoller: ID 86281: Timing: Started: 2015-08-06 15:03:14.128736, Expiration: 2015-08-06 15:13:14, Override Timeout: None, Elapsed Time: 0:00:00.004741, Left till expiry: 0:09:59.866525, Loop Count: 1
2015-08-06 15:03:14,133 INFO     pytan.handler.QuestionPoller: ID 86281: Progress Changed 0% (0 of 2)
2015-08-06 15:03:19,140 DEBUG    pytan.handler.QuestionPoller: ID 86281: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:03:19,140 DEBUG    pytan.handler.QuestionPoller: ID 86281: Timing: Started: 2015-08-06 15:03:14.128736, Expiration: 2015-08-06 15:13:14, Override Timeout: None, Elapsed Time: 0:00:05.011756, Left till expiry: 0:09:54.859510, Loop Count: 2
2015-08-06 15:03:24,148 DEBUG    pytan.handler.QuestionPoller: ID 86281: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:03:24,148 DEBUG    pytan.handler.QuestionPoller: ID 86281: Timing: Started: 2015-08-06 15:03:14.128736, Expiration: 2015-08-06 15:13:14, Override Timeout: None, Elapsed Time: 0:00:10.019819, Left till expiry: 0:09:49.851447, Loop Count: 3
2015-08-06 15:03:29,155 DEBUG    pytan.handler.QuestionPoller: ID 86281: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:03:29,155 DEBUG    pytan.handler.QuestionPoller: ID 86281: Timing: Started: 2015-08-06 15:03:14.128736, Expiration: 2015-08-06 15:13:14, Override Timeout: None, Elapsed Time: 0:00:15.027080, Left till expiry: 0:09:44.844186, Loop Count: 4
2015-08-06 15:03:34,160 DEBUG    pytan.handler.QuestionPoller: ID 86281: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
2015-08-06 15:03:34,160 DEBUG    pytan.handler.QuestionPoller: ID 86281: Timing: Started: 2015-08-06 15:03:14.128736, Expiration: 2015-08-06 15:13:14, Override Timeout: None, Elapsed Time: 0:00:20.032228, Left till expiry: 0:09:39.839039, Loop Count: 5
2015-08-06 15:03:34,161 INFO     pytan.handler.QuestionPoller: ID 86281: Progress Changed 100% (2 of 2)
2015-08-06 15:03:34,161 INFO     pytan.handler.QuestionPoller: ID 86281: Reached Threshold of 99% (2 of 2)

print the export_str returned from export_obj():
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
..trimmed for brevity..

'''
