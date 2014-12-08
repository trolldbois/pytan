
"""
Ask a question using an invalid option.
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
kwargs["sensors"] = u'Operating system, opt:bad'
kwargs["qtype"] = u'manual_human'


# call the handler with the ask method, passing in kwargs for arguments
# this should throw an exception: pytan.utils.HumanParserError
import traceback
try:
    handler.ask(**kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)



'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
Traceback (most recent call last):
  File "<string>", line 39, in <module>
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 127, in ask
    result = getattr(self, q_obj_map['handler'])(**kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 380, in ask_manual_human
    sensor_defs = utils.dehumanize_sensors(sensors)
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 1234, in dehumanize_sensors
    s, parsed_options = extract_options(s)
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 1472, in extract_options
    parsed_options = map_options(parsed_options, ['filter'])
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 1502, in map_options
    raise HumanParserError(err(option))
HumanParserError: Option u'bad' is not a valid option!

'''
