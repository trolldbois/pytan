
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


# call the handler with the deploy_action_human method, passing in kwargs for arguments
# this should throw an exception: pytan.utils.HandlerError
import traceback
try:
    handler.deploy_action_human(**kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)



'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
Traceback (most recent call last):
  File "<string>", line 56, in <module>
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1193, in deploy_action_human
    **kwargs
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 971, in deploy_action
    package_def = self._get_package_def(package_def)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1829, in _get_package_def
    d['package_obj'] = self.get('package', **def_search)[0]
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1605, in get
    return self._get_single(obj_map, **kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1789, in _get_single
    for x in self._single_find(obj_map, k, v, **kwargs):
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1799, in _single_find
    obj_ret = self._find(api_obj_single, **kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1727, in _find
    raise HandlerError(err(search_str))
HandlerError: No results found searching for PackageSpec, name: u'Invalid Package'!!

'''
