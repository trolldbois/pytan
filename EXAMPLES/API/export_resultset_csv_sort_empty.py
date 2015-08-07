
"""
Export a ResultSet from asking a question as CSV with an empty list for header_sort
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
export_kwargs["header_sort"] = []

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
2015-08-07 19:49:40,850 DEBUG    pytan.handler.QuestionPoller: ID 1312: id resolved to 1312
2015-08-07 19:49:40,850 DEBUG    pytan.handler.QuestionPoller: ID 1312: expiration resolved to 2015-08-07T19:59:41
2015-08-07 19:49:40,850 DEBUG    pytan.handler.QuestionPoller: ID 1312: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
2015-08-07 19:49:40,850 DEBUG    pytan.handler.QuestionPoller: ID 1312: id resolved to 1312
2015-08-07 19:49:40,850 DEBUG    pytan.handler.QuestionPoller: ID 1312: Object Info resolved to Question ID: 1312, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
2015-08-07 19:49:40,853 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:49:40,853 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:00:00.003307, Left till expiry: 0:10:00.146043, Loop Count: 1
2015-08-07 19:49:40,854 INFO     pytan.handler.QuestionPoller: ID 1312: Progress Changed 0% (0 of 2)
2015-08-07 19:49:45,859 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:49:45,859 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:00:05.008874, Left till expiry: 0:09:55.140477, Loop Count: 2
2015-08-07 19:49:50,863 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:49:50,863 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:00:10.013265, Left till expiry: 0:09:50.136086, Loop Count: 3
2015-08-07 19:49:55,870 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:49:55,870 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:00:15.019570, Left till expiry: 0:09:45.129781, Loop Count: 4
2015-08-07 19:50:00,877 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:50:00,877 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:00:20.026916, Left till expiry: 0:09:40.122434, Loop Count: 5
2015-08-07 19:50:05,881 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:50:05,881 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:00:25.031127, Left till expiry: 0:09:35.118224, Loop Count: 6
2015-08-07 19:50:10,886 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:50:10,886 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:00:30.035757, Left till expiry: 0:09:30.113594, Loop Count: 7
2015-08-07 19:50:15,891 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:50:15,891 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:00:35.040818, Left till expiry: 0:09:25.108533, Loop Count: 8
2015-08-07 19:50:20,896 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:50:20,896 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:00:40.045903, Left till expiry: 0:09:20.103448, Loop Count: 9
2015-08-07 19:50:25,901 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:50:25,901 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:00:45.050579, Left till expiry: 0:09:15.098771, Loop Count: 10
2015-08-07 19:50:30,906 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:50:30,906 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:00:50.055629, Left till expiry: 0:09:10.093722, Loop Count: 11
2015-08-07 19:50:35,910 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:50:35,910 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:00:55.059821, Left till expiry: 0:09:05.089530, Loop Count: 12
2015-08-07 19:50:40,915 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:50:40,915 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:01:00.064642, Left till expiry: 0:09:00.084709, Loop Count: 13
2015-08-07 19:50:45,919 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:50:45,919 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:01:05.068912, Left till expiry: 0:08:55.080439, Loop Count: 14
2015-08-07 19:50:50,923 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:50:50,923 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:01:10.073184, Left till expiry: 0:08:50.076167, Loop Count: 15
2015-08-07 19:50:55,928 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:50:55,928 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:01:15.077932, Left till expiry: 0:08:45.071419, Loop Count: 16
2015-08-07 19:51:00,934 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:51:00,935 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:01:20.084418, Left till expiry: 0:08:40.064934, Loop Count: 17
2015-08-07 19:51:05,939 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:51:05,939 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:01:25.088901, Left till expiry: 0:08:35.060449, Loop Count: 18
2015-08-07 19:51:10,947 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
2015-08-07 19:51:10,947 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:01:30.096751, Left till expiry: 0:08:30.052600, Loop Count: 19
2015-08-07 19:51:10,947 INFO     pytan.handler.QuestionPoller: ID 1312: Progress Changed 100% (2 of 2)
2015-08-07 19:51:10,947 INFO     pytan.handler.QuestionPoller: ID 1312: Reached Threshold of 99% (2 of 2)

print the export_str returned from export_obj():
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
2015-08-07 19:49:10,709 DEBUG    pytan.handler.QuestionPoller: ID 1311: id resolved to 1311
2015-08-07 19:49:10,709 DEBUG    pytan.handler.QuestionPoller: ID 1311: expiration resolved to 2015-08-07T19:59:10
2015-08-07 19:49:10,709 DEBUG    pytan.handler.QuestionPoller: ID 1311: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
2015-08-07 19:49:10,709 DEBUG    pytan.handler.QuestionPoller: ID 1311: id resolved to 1311
2015-08-07 19:49:10,709 DEBUG    pytan.handler.QuestionPoller: ID 1311: Object Info resolved to Question ID: 1311, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
2015-08-07 19:49:10,713 DEBUG    pytan.handler.QuestionPoller: ID 1311: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:49:10,713 DEBUG    pytan.handler.QuestionPoller: ID 1311: Timing: Started: 2015-08-07 19:49:10.709830, Expiration: 2015-08-07 19:59:10, Override Timeout: None, Elapsed Time: 0:00:00.003431, Left till expiry: 0:09:59.286741, Loop Count: 1
2015-08-07 19:49:10,713 INFO     pytan.handler.QuestionPoller: ID 1311: Progress Changed 0% (0 of 2)
2015-08-07 19:49:15,721 DEBUG    pytan.handler.QuestionPoller: ID 1311: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:49:15,721 DEBUG    pytan.handler.QuestionPoller: ID 1311: Timing: Started: 2015-08-07 19:49:10.709830, Expiration: 2015-08-07 19:59:10, Override Timeout: None, Elapsed Time: 0:00:05.012026, Left till expiry: 0:09:54.278146, Loop Count: 2
2015-08-07 19:49:20,725 DEBUG    pytan.handler.QuestionPoller: ID 1311: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:49:20,726 DEBUG    pytan.handler.QuestionPoller: ID 1311: Timing: Started: 2015-08-07 19:49:10.709830, Expiration: 2015-08-07 19:59:10, Override Timeout: None, Elapsed Time: 0:00:10.016173, Left till expiry: 0:09:49.274000, Loop Count: 3
2015-08-07 19:49:25,730 DEBUG    pytan.handler.QuestionPoller: ID 1311: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:49:25,730 DEBUG    pytan.handler.QuestionPoller: ID 1311: Timing: Started: 2015-08-07 19:49:10.709830, Expiration: 2015-08-07 19:59:10, Override Timeout: None, Elapsed Time: 0:00:15.021031, Left till expiry: 0:09:44.269141, Loop Count: 4
..trimmed for brevity..

'''
