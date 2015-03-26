
"""
Export a ResultSet from asking a question using a bad export_format
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

# setup the export_obj kwargs for later
export_kwargs = {}
export_kwargs["export_format"] = u'bad'

# ask the question that will provide the resultset that we want to use
ask_kwargs = {
    'qtype': 'manual_human',
    'sensors': [
        "Computer Name"
    ],
}
response = handler.ask(**ask_kwargs)
export_kwargs['obj'] = response['question_results']

# export the object to a string
# this should throw an exception: pytan.utils.HandlerError
import traceback

try:
    handler.export_obj(**export_kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)



'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
2015-03-26 12:03:14,502 INFO     question_progress: Results 0% (Get Computer Name from all machines)
2015-03-26 12:03:19,517 INFO     question_progress: Results 50% (Get Computer Name from all machines)
2015-03-26 12:03:24,533 INFO     question_progress: Results 50% (Get Computer Name from all machines)
2015-03-26 12:03:29,545 INFO     question_progress: Results 100% (Get Computer Name from all machines)
Traceback (most recent call last):
  File "<string>", line 64, in <module>
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1429, in export_obj
    raise HandlerError(err)
HandlerError: u'bad' not a supported export format for ResultSet, must be one of: json, csv

'''
