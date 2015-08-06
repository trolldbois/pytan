
"""
Export a ResultSet from asking a question as CSV with true for header_sort
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
export_kwargs["header_sort"] = True

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
2015-08-06 15:03:59,519 DEBUG    pytan.handler.QuestionPoller: ID 86283: id resolved to 86283
2015-08-06 15:03:59,519 DEBUG    pytan.handler.QuestionPoller: ID 86283: expiration resolved to 2015-08-06T15:13:59
2015-08-06 15:03:59,519 DEBUG    pytan.handler.QuestionPoller: ID 86283: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 15:03:59,519 DEBUG    pytan.handler.QuestionPoller: ID 86283: id resolved to 86283
2015-08-06 15:03:59,519 DEBUG    pytan.handler.QuestionPoller: ID 86283: Object Info resolved to Question ID: 86283, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 15:03:59,524 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:03:59,524 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:00:00.004793, Left till expiry: 0:09:59.475810, Loop Count: 1
2015-08-06 15:03:59,524 INFO     pytan.handler.QuestionPoller: ID 86283: Progress Changed 0% (0 of 2)
2015-08-06 15:04:04,529 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:04:04,529 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:00:05.010366, Left till expiry: 0:09:54.470237, Loop Count: 2
2015-08-06 15:04:09,538 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:04:09,538 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:00:10.018850, Left till expiry: 0:09:49.461753, Loop Count: 3
2015-08-06 15:04:14,549 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:04:14,549 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:00:15.030350, Left till expiry: 0:09:44.450253, Loop Count: 4
2015-08-06 15:04:19,557 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:04:19,557 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:00:20.038154, Left till expiry: 0:09:39.442448, Loop Count: 5
2015-08-06 15:04:24,564 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:04:24,564 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:00:25.045234, Left till expiry: 0:09:34.435368, Loop Count: 6
2015-08-06 15:04:29,573 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:04:29,573 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:00:30.054274, Left till expiry: 0:09:29.426328, Loop Count: 7
2015-08-06 15:04:34,578 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:04:34,578 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:00:35.059368, Left till expiry: 0:09:24.421234, Loop Count: 8
2015-08-06 15:04:39,585 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:04:39,585 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:00:40.065770, Left till expiry: 0:09:19.414832, Loop Count: 9
2015-08-06 15:04:44,593 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:04:44,593 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:00:45.073694, Left till expiry: 0:09:14.406908, Loop Count: 10
2015-08-06 15:04:49,601 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:04:49,602 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:00:50.082628, Left till expiry: 0:09:09.397974, Loop Count: 11
2015-08-06 15:04:54,609 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:04:54,609 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:00:55.089850, Left till expiry: 0:09:04.390752, Loop Count: 12
2015-08-06 15:04:59,620 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:04:59,620 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:01:00.100903, Left till expiry: 0:08:59.379699, Loop Count: 13
2015-08-06 15:05:04,628 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:05:04,628 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:01:05.109089, Left till expiry: 0:08:54.371513, Loop Count: 14
2015-08-06 15:05:09,635 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:05:09,635 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:01:10.116243, Left till expiry: 0:08:49.364360, Loop Count: 15
2015-08-06 15:05:14,643 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:05:14,643 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:01:15.124324, Left till expiry: 0:08:44.356278, Loop Count: 16
2015-08-06 15:05:19,651 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:05:19,651 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:01:20.132504, Left till expiry: 0:08:39.348098, Loop Count: 17
2015-08-06 15:05:24,657 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:05:24,657 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:01:25.138251, Left till expiry: 0:08:34.342352, Loop Count: 18
2015-08-06 15:05:29,666 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:05:29,666 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:01:30.147506, Left till expiry: 0:08:29.333096, Loop Count: 19
2015-08-06 15:05:34,671 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:05:34,671 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:01:35.152487, Left till expiry: 0:08:24.328115, Loop Count: 20
2015-08-06 15:05:39,679 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:05:39,679 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:01:40.159922, Left till expiry: 0:08:19.320681, Loop Count: 21
2015-08-06 15:05:44,687 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:05:44,687 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:01:45.168016, Left till expiry: 0:08:14.312586, Loop Count: 22
2015-08-06 15:05:49,692 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:05:49,692 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:01:50.173549, Left till expiry: 0:08:09.307053, Loop Count: 23
2015-08-06 15:05:54,702 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:05:54,702 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:01:55.183004, Left till expiry: 0:08:04.297598, Loop Count: 24
2015-08-06 15:05:59,708 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:05:59,708 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:02:00.188796, Left till expiry: 0:07:59.291806, Loop Count: 25
2015-08-06 15:06:04,718 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:06:04,719 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:02:05.199597, Left till expiry: 0:07:54.281006, Loop Count: 26
2015-08-06 15:06:09,727 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
2015-08-06 15:06:09,727 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:02:10.208061, Left till expiry: 0:07:49.272542, Loop Count: 27
2015-08-06 15:06:09,727 INFO     pytan.handler.QuestionPoller: ID 86283: Progress Changed 50% (1 of 2)
2015-08-06 15:06:14,733 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
2015-08-06 15:06:14,733 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:02:15.214381, Left till expiry: 0:07:44.266222, Loop Count: 28
2015-08-06 15:06:19,741 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
2015-08-06 15:06:19,741 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:02:20.222144, Left till expiry: 0:07:39.258459, Loop Count: 29
2015-08-06 15:06:19,741 INFO     pytan.handler.QuestionPoller: ID 86283: Progress Changed 100% (2 of 2)
2015-08-06 15:06:19,741 INFO     pytan.handler.QuestionPoller: ID 86283: Reached Threshold of 99% (2 of 2)

print the export_str returned from export_obj():
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
2015-08-06 15:03:34,315 DEBUG    pytan.handler.QuestionPoller: ID 86282: id resolved to 86282
2015-08-06 15:03:34,315 DEBUG    pytan.handler.QuestionPoller: ID 86282: expiration resolved to 2015-08-06T15:13:34
2015-08-06 15:03:34,315 DEBUG    pytan.handler.QuestionPoller: ID 86282: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 15:03:34,315 DEBUG    pytan.handler.QuestionPoller: ID 86282: id resolved to 86282
2015-08-06 15:03:34,315 DEBUG    pytan.handler.QuestionPoller: ID 86282: Object Info resolved to Question ID: 86282, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
2015-08-06 15:03:34,320 DEBUG    pytan.handler.QuestionPoller: ID 86282: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:03:34,320 DEBUG    pytan.handler.QuestionPoller: ID 86282: Timing: Started: 2015-08-06 15:03:34.315567, Expiration: 2015-08-06 15:13:34, Override Timeout: None, Elapsed Time: 0:00:00.004867, Left till expiry: 0:09:59.679569, Loop Count: 1
2015-08-06 15:03:34,320 INFO     pytan.handler.QuestionPoller: ID 86282: Progress Changed 0% (0 of 2)
2015-08-06 15:03:39,325 DEBUG    pytan.handler.QuestionPoller: ID 86282: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:03:39,325 DEBUG    pytan.handler.QuestionPoller: ID 86282: Timing: Started: 2015-08-06 15:03:34.315567, Expiration: 2015-08-06 15:13:34, Override Timeout: None, Elapsed Time: 0:00:05.010254, Left till expiry: 0:09:54.674182, Loop Count: 2
2015-08-06 15:03:44,335 DEBUG    pytan.handler.QuestionPoller: ID 86282: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
2015-08-06 15:03:44,335 DEBUG    pytan.handler.QuestionPoller: ID 86282: Timing: Started: 2015-08-06 15:03:34.315567, Expiration: 2015-08-06 15:13:34, Override Timeout: None, Elapsed Time: 0:00:10.019513, Left till expiry: 0:09:49.664923, Loop Count: 3
2015-08-06 15:03:44,335 INFO     pytan.handler.QuestionPoller: ID 86282: Progress Changed 50% (1 of 2)
2015-08-06 15:03:49,342 DEBUG    pytan.handler.QuestionPoller: ID 86282: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
..trimmed for brevity..

'''
