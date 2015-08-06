
"""
Ask a question using a sensor that does not exist
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
kwargs["sensors"] = u'Dweedle Dee and Dum'
kwargs["qtype"] = u'manual'


# call the handler with the ask method, passing in kwargs for arguments
# this should throw an exception: pytan.exceptions.HandlerError
import traceback
try:
    handler.ask(**kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)



'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
Traceback (most recent call last):
  File "<string>", line 55, in <module>
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 131, in ask
    result = getattr(self, q_obj_map['handler'])(**kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 306, in ask_manual
    **kwargs
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2710, in wrap
    ret = f(*args, **kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1880, in _ask_manual
    sensor_defs = self._get_sensor_defs(sensor_defs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1419, in _get_sensor_defs
    d['sensor_obj'] = self.get('sensor', **def_search)[0]
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2710, in wrap
    ret = f(*args, **kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1251, in get
    return self._get_multi(obj_map, **kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1364, in _get_multi
    found = self._find(api_obj_multi, **kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2710, in wrap
    ret = f(*args, **kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1328, in _find
    raise pytan.exceptions.HandlerError(err(search_str))
HandlerError: No results found searching for Sensor, name: u'Dweedle Dee and Dum'!!

'''
