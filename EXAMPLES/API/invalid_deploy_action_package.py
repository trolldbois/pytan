
"""
Deploy an action using a non-existing package.
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
kwargs["run"] = True
kwargs["package"] = u'Invalid Package'


# call the handler with the deploy_action method, passing in kwargs for arguments
# this should throw an exception: pytan.exceptions.HandlerError
import traceback
try:
    handler.deploy_action(**kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)



'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
Traceback (most recent call last):
  File "<string>", line 56, in <module>
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 405, in deploy_action
    **kwargs
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2710, in wrap
    ret = f(*args, **kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1612, in _deploy_action
    package_def = self._get_package_def(package_def)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1431, in _get_package_def
    d['package_obj'] = self.get('package', **def_search)[0]
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2710, in wrap
    ret = f(*args, **kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1256, in get
    return self._get_single(obj_map, **kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1391, in _get_single
    for x in self._single_find(obj_map, k, v, **kwargs):
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1401, in _single_find
    obj_ret = self._find(api_obj_single, **kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2710, in wrap
    ret = f(*args, **kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1328, in _find
    raise pytan.exceptions.HandlerError(err(search_str))
HandlerError: No results found searching for PackageSpec, name: u'Invalid Package'!!

'''
