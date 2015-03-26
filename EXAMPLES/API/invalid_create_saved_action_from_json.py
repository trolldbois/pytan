
"""
Create a saved action from json (not supported!)
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

# setup the arguments for getting an object to export as json file
get_kwargs = {}
get_kwargs["objtype"] = u'saved_action'
get_kwargs["name"] = u'Distribute Tanium Standard Utilities'

# get objects to use as an export to JSON file
orig_objs = handler.get(**get_kwargs)

# export orig_objs to a json file
json_file, results = handler.export_to_report_file(
    obj=orig_objs,
    export_format='json',
    report_dir=tempfile.gettempdir(),
)

# call the handler with the create_from_json method, passing in kwargs for arguments
# this should throw an exception: pytan.utils.HandlerError
import traceback

# create the object from the exported JSON file
create_kwargs = {'objtype': u'saved_action', 'json_file': json_file}
try:
    response = handler.create_from_json(**create_kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)



'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
2015-03-26 11:49:20,140 INFO     handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/SavedActionList_2015_03_26-11_49_20-EDT.json' written with 1008 bytes
Traceback (most recent call last):
  File "<string>", line 67, in <module>
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 484, in create_from_json
    raise HandlerError(m(objtype, json_createable))
HandlerError: saved_action is not a json createable object! Supported objects: user, whitelisted_url, saved_question, group, package, question, action, sensor

'''
