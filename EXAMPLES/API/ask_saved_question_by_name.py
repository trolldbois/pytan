
"""
Ask a saved question by referencing the name of a saved question in a string.
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
kwargs["qtype"] = u'saved'
kwargs["name"] = u'Installed Applications'

# call the handler with the ask method, passing in kwargs for arguments
response = handler.ask(**kwargs)
import pprint, io

print ""
print "Type of response: ", type(response)

print ""
print "Pretty print of response:"
print pprint.pformat(response)

print ""
print "Equivalent Question if it were to be asked in the Tanium Console: "
print response['question_object'].query_text

# create an IO stream to store CSV results to
out = io.BytesIO()

# call the write_csv() method to convert response to CSV and store it in out
response['question_results'].write_csv(out, response['question_results'])

print ""
print "CSV Results of response: "
out = out.getvalue()
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\n'.join(out)
print out


'''Output from running this:
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!

Type of response:  <type 'dict'>

Pretty print of response:
{'poller_object': None,
 'poller_success': None,
 'question_object': <taniumpy.object_types.question.Question object at 0x10a80a150>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10a810c10>,
 'saved_question_object': <taniumpy.object_types.saved_question.SavedQuestion object at 0x10a810a50>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Installed Applications from all machines

CSV Results of response: 
Name,Silent Uninstall String,Uninstallable,Version
Image Capture Extension,nothing,Not Uninstallable,10.2
Dictation,nothing,Not Uninstallable,1.6.1
Wish,nothing,Not Uninstallable,8.5.9
Uninstall AnyConnect,nothing,Not Uninstallable,3.1.08009
Time Machine,nothing,Not Uninstallable,1.3
AppleGraphicsWarning,nothing,Not Uninstallable,2.3.0
soagent,nothing,Not Uninstallable,7.0
Feedback Assistant,nothing,Not Uninstallable,4.1.3
AinuIM,nothing,Not Uninstallable,1.0
vpndownloader,nothing,Not Uninstallable,3.1.08009
Pass Viewer,nothing,Not Uninstallable,1.0
ARDAgent,nothing,Not Uninstallable,3.8.4
OBEXAgent,nothing,Not Uninstallable,4.3.5
PressAndHold,nothing,Not Uninstallable,1.2
..trimmed for brevity..

'''
