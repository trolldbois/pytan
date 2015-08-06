
"""
Deploy an action without run=True, which will only run the pre-deploy action question that matches action_filters, export the results to a file, and raise a RunFalse exception
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

# setup the arguments for the handler method
kwargs = {}
kwargs['report_dir'] = tempfile.gettempdir()
kwargs["package"] = u'Distribute Tanium Standard Utilities'


# call the handler with the deploy_action method, passing in kwargs for arguments
# this should throw an exception: pytan.exceptions.RunFalse
import traceback
try:
    handler.deploy_action(**kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)



'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
2015-08-06 14:55:59,337 DEBUG    pytan.handler.QuestionPoller: ID 86271: id resolved to 86271
2015-08-06 14:55:59,337 DEBUG    pytan.handler.QuestionPoller: ID 86271: expiration resolved to 2015-08-06T15:05:59
2015-08-06 14:55:59,337 DEBUG    pytan.handler.QuestionPoller: ID 86271: query_text resolved to Get Computer Name and Online = "True" from all machines
2015-08-06 14:55:59,337 DEBUG    pytan.handler.QuestionPoller: ID 86271: id resolved to 86271
2015-08-06 14:55:59,337 DEBUG    pytan.handler.QuestionPoller: ID 86271: Object Info resolved to Question ID: 86271, Query: Get Computer Name and Online = "True" from all machines
2015-08-06 14:55:59,343 DEBUG    pytan.handler.QuestionPoller: ID 86271: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:55:59,343 DEBUG    pytan.handler.QuestionPoller: ID 86271: Timing: Started: 2015-08-06 14:55:59.337907, Expiration: 2015-08-06 15:05:59, Override Timeout: None, Elapsed Time: 0:00:00.005395, Left till expiry: 0:09:59.656701, Loop Count: 1
2015-08-06 14:55:59,343 INFO     pytan.handler.QuestionPoller: ID 86271: Progress Changed 0% (0 of 2)
2015-08-06 14:56:04,353 DEBUG    pytan.handler.QuestionPoller: ID 86271: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:56:04,353 DEBUG    pytan.handler.QuestionPoller: ID 86271: Timing: Started: 2015-08-06 14:55:59.337907, Expiration: 2015-08-06 15:05:59, Override Timeout: None, Elapsed Time: 0:00:05.015347, Left till expiry: 0:09:54.646748, Loop Count: 2
2015-08-06 14:56:09,358 DEBUG    pytan.handler.QuestionPoller: ID 86271: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
2015-08-06 14:56:09,358 DEBUG    pytan.handler.QuestionPoller: ID 86271: Timing: Started: 2015-08-06 14:55:59.337907, Expiration: 2015-08-06 15:05:59, Override Timeout: None, Elapsed Time: 0:00:10.021029, Left till expiry: 0:09:49.641067, Loop Count: 3
2015-08-06 14:56:09,358 INFO     pytan.handler.QuestionPoller: ID 86271: Progress Changed 100% (2 of 2)
2015-08-06 14:56:09,359 INFO     pytan.handler.QuestionPoller: ID 86271: Reached Threshold of 99% (2 of 2)
2015-08-06 14:56:09,364 INFO     pytan.handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/VERIFY_BEFORE_DEPLOY_ACTION_ResultSet_2015_08_06-10_56_09-EDT.csv' written with 73 bytes
Traceback (most recent call last):
  File "<string>", line 55, in <module>
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 405, in deploy_action
    **kwargs
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2710, in wrap
    ret = f(*args, **kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1663, in _deploy_action
    raise pytan.exceptions.RunFalse(m(report_path, len(result)))
RunFalse: 'Run' is not True!!
View and verify the contents of /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/VERIFY_BEFORE_DEPLOY_ACTION_ResultSet_2015_08_06-10_56_09-EDT.csv (length: 73 bytes)
Re-run this deploy action with run=True after verifying

'''
