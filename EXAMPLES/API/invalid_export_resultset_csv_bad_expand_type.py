
"""
Export a ResultSet from asking a question using a bad expand_grouped_columns
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
export_kwargs["expand_grouped_columns"] = u'bad'

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
2015-08-06 15:14:24,093 DEBUG    pytan.handler.QuestionPoller: ID 86298: id resolved to 86298
2015-08-06 15:14:24,093 DEBUG    pytan.handler.QuestionPoller: ID 86298: expiration resolved to 2015-08-06T15:24:24
2015-08-06 15:14:24,093 DEBUG    pytan.handler.QuestionPoller: ID 86298: query_text resolved to Get Computer Name from all machines
2015-08-06 15:14:24,093 DEBUG    pytan.handler.QuestionPoller: ID 86298: id resolved to 86298
2015-08-06 15:14:24,093 DEBUG    pytan.handler.QuestionPoller: ID 86298: Object Info resolved to Question ID: 86298, Query: Get Computer Name from all machines
2015-08-06 15:14:24,098 DEBUG    pytan.handler.QuestionPoller: ID 86298: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:14:24,098 DEBUG    pytan.handler.QuestionPoller: ID 86298: Timing: Started: 2015-08-06 15:14:24.093265, Expiration: 2015-08-06 15:24:24, Override Timeout: None, Elapsed Time: 0:00:00.004880, Left till expiry: 0:09:59.901857, Loop Count: 1
2015-08-06 15:14:24,098 INFO     pytan.handler.QuestionPoller: ID 86298: Progress Changed 0% (0 of 2)
2015-08-06 15:14:29,107 DEBUG    pytan.handler.QuestionPoller: ID 86298: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 15:14:29,107 DEBUG    pytan.handler.QuestionPoller: ID 86298: Timing: Started: 2015-08-06 15:14:24.093265, Expiration: 2015-08-06 15:24:24, Override Timeout: None, Elapsed Time: 0:00:05.014103, Left till expiry: 0:09:54.892637, Loop Count: 2
2015-08-06 15:14:34,118 DEBUG    pytan.handler.QuestionPoller: ID 86298: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
2015-08-06 15:14:34,118 DEBUG    pytan.handler.QuestionPoller: ID 86298: Timing: Started: 2015-08-06 15:14:24.093265, Expiration: 2015-08-06 15:24:24, Override Timeout: None, Elapsed Time: 0:00:10.025100, Left till expiry: 0:09:49.881637, Loop Count: 3
2015-08-06 15:14:34,118 INFO     pytan.handler.QuestionPoller: ID 86298: Progress Changed 100% (2 of 2)
2015-08-06 15:14:34,118 INFO     pytan.handler.QuestionPoller: ID 86298: Reached Threshold of 99% (2 of 2)
Traceback (most recent call last):
  File "<string>", line 65, in <module>
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2710, in wrap
    ret = f(*args, **kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1085, in export_obj
    pytan.utils.check_dictkey(**check_args)
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2696, in check_dictkey
    raise pytan.exceptions.HandlerError(err(key, valid_types, k_type))
HandlerError: 'expand_grouped_columns' must be one of [<type 'bool'>], you supplied <type 'unicode'>!

'''
