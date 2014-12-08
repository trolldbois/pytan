
"""
Export a BaseType from getting objects using a bad export_format
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

# setup the export_obj kwargs for later
export_kwargs = {}
export_kwargs["export_format"] = u'bad'

# get the objects that will provide the basetype that we want to use
get_kwargs = {
    'name': [
        "Computer Name", "IP Route Details", "IP Address",
        'Folder Name Search with RegEx Match',
    ],
    'objtype': 'sensor',
}
response = handler.get(**get_kwargs)
export_kwargs['obj'] = response

# export the object to a string
# this should throw an exception: pytan.utils.HandlerError
import traceback

try:
    handler.export_obj(**export_kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)



'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
Traceback (most recent call last):
  File "<string>", line 49, in <module>
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1396, in export_obj
    raise HandlerError(err)
HandlerError: u'bad' not a supported export format for SensorList, must be one of: xml, json, csv

'''
