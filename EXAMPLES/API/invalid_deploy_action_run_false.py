
"""
Deploy an action without run=True, which will only run the pre-deploy action question that matches action_filters, export the results to a file, and raise a RunFalse exception
"""
# Path to lib directory which contains pytan package
PYTAN_LIB_PATH = '../lib'

# connection info for Tanium Server
USERNAME = "Tanium User"
PASSWORD = "T@n!um"
HOST = "172.16.31.128"
PORT = "444"

# Logging conrols
LOGLEVEL = 2
DEBUGFORMAT = False

import sys, tempfile
sys.path.append(PYTAN_LIB_PATH)

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


# call the handler with the deploy_action_human method, passing in kwargs for arguments
# this should throw an exception: pytan.utils.RunFalse
import traceback
try:
    handler.deploy_action_human(**kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)



'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
2015-02-11 12:06:19,976 INFO     question_progress: Results 0% (Get Computer Name and Online = "True" from all machines)
2015-02-11 12:06:24,991 INFO     question_progress: Results 100% (Get Computer Name and Online = "True" from all machines)
2015-02-11 12:06:25,005 INFO     handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/VERIFY_BEFORE_DEPLOY_ACTION_ResultSet_2015_02_11-12_06_25-EST.csv' written with 73 bytes
Traceback (most recent call last):
  File "<string>", line 39, in <module>
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1176, in deploy_action_human
    **kwargs
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1017, in deploy_action
    raise RunFalse(m(report_path, len(result)))
RunFalse: 'Run' is not True!!
View and verify the contents of /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/VERIFY_BEFORE_DEPLOY_ACTION_ResultSet_2015_02_11-12_06_25-EST.csv (length: 73 bytes)
Re-run this deploy action with run=True after verifying

'''
