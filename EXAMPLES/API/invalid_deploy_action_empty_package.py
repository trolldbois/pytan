
"""
Deploy an action using an empty package string.
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

# setup the arguments for the handler method
kwargs = {}
kwargs['report_dir'] = tempfile.gettempdir()
kwargs["run"] = True
kwargs["package"] = u''


# call the handler with the deploy_action method, passing in kwargs for arguments
# this should throw an exception: pytan.exceptions.HumanParserError
import traceback
try:
    handler.deploy_action(**kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)



'''Output from running this:
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
Traceback (most recent call last):
  File "<string>", line 56, in <module>
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 398, in deploy_action
    package_def = pytan.utils.dehumanize_package(package)
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 1508, in dehumanize_package
    raise pytan.exceptions.HumanParserError(err(package))
HumanParserError: u'' must be a string supplied as 'package'

'''
