
"""
Deploy an action using an empty package string.
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
kwargs["run"] = True
kwargs["package"] = u''


# call the handler with the deploy_action_human method, passing in kwargs for arguments
# this should throw an exception: pytan.utils.HumanParserError
import traceback
try:
    handler.deploy_action_human(**kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)



'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
Traceback (most recent call last):
  File "<string>", line 40, in <module>
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1166, in deploy_action_human
    package_def = utils.dehumanize_package(package)
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 1334, in dehumanize_package
    raise HumanParserError(err(package))
HumanParserError: u'' must be a string supplied as 'package'

'''
