
"""
Export a ResultSet from asking a question as CSV with false for header_add_type
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
export_kwargs["header_add_type"] = False

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
2015-08-07 19:53:11,519 DEBUG    pytan.handler.QuestionPoller: ID 1318: id resolved to 1318
2015-08-07 19:53:11,519 DEBUG    pytan.handler.QuestionPoller: ID 1318: expiration resolved to 2015-08-07T20:03:11
2015-08-07 19:53:11,519 DEBUG    pytan.handler.QuestionPoller: ID 1318: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
2015-08-07 19:53:11,519 DEBUG    pytan.handler.QuestionPoller: ID 1318: id resolved to 1318
2015-08-07 19:53:11,519 DEBUG    pytan.handler.QuestionPoller: ID 1318: Object Info resolved to Question ID: 1318, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
2015-08-07 19:53:11,522 DEBUG    pytan.handler.QuestionPoller: ID 1318: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:53:11,522 DEBUG    pytan.handler.QuestionPoller: ID 1318: Timing: Started: 2015-08-07 19:53:11.519348, Expiration: 2015-08-07 20:03:11, Override Timeout: None, Elapsed Time: 0:00:00.002979, Left till expiry: 0:09:59.477675, Loop Count: 1
2015-08-07 19:53:11,522 INFO     pytan.handler.QuestionPoller: ID 1318: Progress Changed 0% (0 of 2)
2015-08-07 19:53:16,530 DEBUG    pytan.handler.QuestionPoller: ID 1318: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:53:16,530 DEBUG    pytan.handler.QuestionPoller: ID 1318: Timing: Started: 2015-08-07 19:53:11.519348, Expiration: 2015-08-07 20:03:11, Override Timeout: None, Elapsed Time: 0:00:05.010954, Left till expiry: 0:09:54.469700, Loop Count: 2
2015-08-07 19:53:21,538 DEBUG    pytan.handler.QuestionPoller: ID 1318: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:53:21,538 DEBUG    pytan.handler.QuestionPoller: ID 1318: Timing: Started: 2015-08-07 19:53:11.519348, Expiration: 2015-08-07 20:03:11, Override Timeout: None, Elapsed Time: 0:00:10.019447, Left till expiry: 0:09:49.461210, Loop Count: 3
2015-08-07 19:53:26,543 DEBUG    pytan.handler.QuestionPoller: ID 1318: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:53:26,543 DEBUG    pytan.handler.QuestionPoller: ID 1318: Timing: Started: 2015-08-07 19:53:11.519348, Expiration: 2015-08-07 20:03:11, Override Timeout: None, Elapsed Time: 0:00:15.023902, Left till expiry: 0:09:44.456753, Loop Count: 4
2015-08-07 19:53:31,548 DEBUG    pytan.handler.QuestionPoller: ID 1318: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:53:31,548 DEBUG    pytan.handler.QuestionPoller: ID 1318: Timing: Started: 2015-08-07 19:53:11.519348, Expiration: 2015-08-07 20:03:11, Override Timeout: None, Elapsed Time: 0:00:20.029090, Left till expiry: 0:09:39.451565, Loop Count: 5
2015-08-07 19:53:36,552 DEBUG    pytan.handler.QuestionPoller: ID 1318: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:53:36,552 DEBUG    pytan.handler.QuestionPoller: ID 1318: Timing: Started: 2015-08-07 19:53:11.519348, Expiration: 2015-08-07 20:03:11, Override Timeout: None, Elapsed Time: 0:00:25.033252, Left till expiry: 0:09:34.447403, Loop Count: 6
2015-08-07 19:53:41,559 DEBUG    pytan.handler.QuestionPoller: ID 1318: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:53:41,559 DEBUG    pytan.handler.QuestionPoller: ID 1318: Timing: Started: 2015-08-07 19:53:11.519348, Expiration: 2015-08-07 20:03:11, Override Timeout: None, Elapsed Time: 0:00:30.039743, Left till expiry: 0:09:29.440912, Loop Count: 7
2015-08-07 19:53:46,566 DEBUG    pytan.handler.QuestionPoller: ID 1318: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:53:46,566 DEBUG    pytan.handler.QuestionPoller: ID 1318: Timing: Started: 2015-08-07 19:53:11.519348, Expiration: 2015-08-07 20:03:11, Override Timeout: None, Elapsed Time: 0:00:35.047230, Left till expiry: 0:09:24.433424, Loop Count: 8
2015-08-07 19:53:51,570 DEBUG    pytan.handler.QuestionPoller: ID 1318: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:53:51,570 DEBUG    pytan.handler.QuestionPoller: ID 1318: Timing: Started: 2015-08-07 19:53:11.519348, Expiration: 2015-08-07 20:03:11, Override Timeout: None, Elapsed Time: 0:00:40.050878, Left till expiry: 0:09:19.429777, Loop Count: 9
2015-08-07 19:53:56,577 DEBUG    pytan.handler.QuestionPoller: ID 1318: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:53:56,577 DEBUG    pytan.handler.QuestionPoller: ID 1318: Timing: Started: 2015-08-07 19:53:11.519348, Expiration: 2015-08-07 20:03:11, Override Timeout: None, Elapsed Time: 0:00:45.058560, Left till expiry: 0:09:14.422095, Loop Count: 10
2015-08-07 19:54:01,583 DEBUG    pytan.handler.QuestionPoller: ID 1318: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:54:01,583 DEBUG    pytan.handler.QuestionPoller: ID 1318: Timing: Started: 2015-08-07 19:53:11.519348, Expiration: 2015-08-07 20:03:11, Override Timeout: None, Elapsed Time: 0:00:50.064562, Left till expiry: 0:09:09.416093, Loop Count: 11
2015-08-07 19:54:06,590 DEBUG    pytan.handler.QuestionPoller: ID 1318: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:54:06,591 DEBUG    pytan.handler.QuestionPoller: ID 1318: Timing: Started: 2015-08-07 19:53:11.519348, Expiration: 2015-08-07 20:03:11, Override Timeout: None, Elapsed Time: 0:00:55.071771, Left till expiry: 0:09:04.408885, Loop Count: 12
2015-08-07 19:54:11,600 DEBUG    pytan.handler.QuestionPoller: ID 1318: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:54:11,600 DEBUG    pytan.handler.QuestionPoller: ID 1318: Timing: Started: 2015-08-07 19:53:11.519348, Expiration: 2015-08-07 20:03:11, Override Timeout: None, Elapsed Time: 0:01:00.081018, Left till expiry: 0:08:59.399640, Loop Count: 13
2015-08-07 19:54:16,608 DEBUG    pytan.handler.QuestionPoller: ID 1318: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:54:16,608 DEBUG    pytan.handler.QuestionPoller: ID 1318: Timing: Started: 2015-08-07 19:53:11.519348, Expiration: 2015-08-07 20:03:11, Override Timeout: None, Elapsed Time: 0:01:05.089357, Left till expiry: 0:08:54.391297, Loop Count: 14
2015-08-07 19:54:21,612 DEBUG    pytan.handler.QuestionPoller: ID 1318: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:54:21,612 DEBUG    pytan.handler.QuestionPoller: ID 1318: Timing: Started: 2015-08-07 19:53:11.519348, Expiration: 2015-08-07 20:03:11, Override Timeout: None, Elapsed Time: 0:01:10.093366, Left till expiry: 0:08:49.387288, Loop Count: 15
2015-08-07 19:54:26,621 DEBUG    pytan.handler.QuestionPoller: ID 1318: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:54:26,621 DEBUG    pytan.handler.QuestionPoller: ID 1318: Timing: Started: 2015-08-07 19:53:11.519348, Expiration: 2015-08-07 20:03:11, Override Timeout: None, Elapsed Time: 0:01:15.102294, Left till expiry: 0:08:44.378360, Loop Count: 16
2015-08-07 19:54:31,629 DEBUG    pytan.handler.QuestionPoller: ID 1318: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:54:31,629 DEBUG    pytan.handler.QuestionPoller: ID 1318: Timing: Started: 2015-08-07 19:53:11.519348, Expiration: 2015-08-07 20:03:11, Override Timeout: None, Elapsed Time: 0:01:20.110500, Left till expiry: 0:08:39.370155, Loop Count: 17
2015-08-07 19:54:36,635 DEBUG    pytan.handler.QuestionPoller: ID 1318: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
2015-08-07 19:54:36,635 DEBUG    pytan.handler.QuestionPoller: ID 1318: Timing: Started: 2015-08-07 19:53:11.519348, Expiration: 2015-08-07 20:03:11, Override Timeout: None, Elapsed Time: 0:01:25.115807, Left till expiry: 0:08:34.364849, Loop Count: 18
2015-08-07 19:54:36,635 INFO     pytan.handler.QuestionPoller: ID 1318: Progress Changed 100% (2 of 2)
2015-08-07 19:54:36,635 INFO     pytan.handler.QuestionPoller: ID 1318: Reached Threshold of 99% (2 of 2)

print the export_str returned from export_obj():
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
..trimmed for brevity..

'''
