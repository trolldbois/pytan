
"""
Export a ResultSet from asking a question using a bad export_format
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
export_kwargs["export_format"] = u'bad'

# ask the question that will provide the resultset that we want to use
ask_kwargs = {
    'qtype': 'manual',
    'sensors': [
        "Computer Name"
    ],
}
response = handler.ask(**ask_kwargs)
export_kwargs['obj'] = response['question_results']

# export the object to a string
# this should throw an exception: pytan.exceptions.HandlerError
import traceback

try:
    handler.export_obj(**export_kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)



'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
2015-08-06 15:14:44,863 DEBUG    pytan.handler.QuestionPoller: ID 86300: id resolved to 86300
2015-08-06 15:14:44,863 DEBUG    pytan.handler.QuestionPoller: ID 86300: expiration resolved to 2015-08-06T15:24:45
2015-08-06 15:14:44,863 DEBUG    pytan.handler.QuestionPoller: ID 86300: query_text resolved to Get Computer Name from all machines
2015-08-06 15:14:44,863 DEBUG    pytan.handler.QuestionPoller: ID 86300: id resolved to 86300
2015-08-06 15:14:44,863 DEBUG    pytan.handler.QuestionPoller: ID 86300: Object Info resolved to Question ID: 86300, Query: Get Computer Name from all machines
2015-08-06 15:14:44,868 DEBUG    pytan.handler.QuestionPoller: ID 86300: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:14:44,868 DEBUG    pytan.handler.QuestionPoller: ID 86300: Timing: Started: 2015-08-06 15:14:44.863586, Expiration: 2015-08-06 15:24:45, Override Timeout: None, Elapsed Time: 0:00:00.004970, Left till expiry: 0:10:00.131447, Loop Count: 1
2015-08-06 15:14:44,868 INFO     pytan.handler.QuestionPoller: ID 86300: Progress Changed 0% (0 of 2)
2015-08-06 15:14:49,881 DEBUG    pytan.handler.QuestionPoller: ID 86300: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:14:49,881 DEBUG    pytan.handler.QuestionPoller: ID 86300: Timing: Started: 2015-08-06 15:14:44.863586, Expiration: 2015-08-06 15:24:45, Override Timeout: None, Elapsed Time: 0:00:05.017735, Left till expiry: 0:09:55.118683, Loop Count: 2
2015-08-06 15:14:54,892 DEBUG    pytan.handler.QuestionPoller: ID 86300: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
2015-08-06 15:14:54,892 DEBUG    pytan.handler.QuestionPoller: ID 86300: Timing: Started: 2015-08-06 15:14:44.863586, Expiration: 2015-08-06 15:24:45, Override Timeout: None, Elapsed Time: 0:00:10.028580, Left till expiry: 0:09:50.107837, Loop Count: 3
2015-08-06 15:14:54,892 INFO     pytan.handler.QuestionPoller: ID 86300: Progress Changed 100% (2 of 2)
2015-08-06 15:14:54,892 INFO     pytan.handler.QuestionPoller: ID 86300: Reached Threshold of 99% (2 of 2)
Traceback (most recent call last):
  File "<string>", line 64, in <module>
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2710, in wrap
    ret = f(*args, **kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1079, in export_obj
    raise pytan.exceptions.HandlerError(err)
HandlerError: u'bad' not a supported export format for ResultSet, must be one of: json, csv

'''
