
"""
Ask a manual question using human strings by referencing the name of multiple sensors in a list.

No sensor filters, sensor parameters, sensor filter options, question filters, or question options supplied.
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
kwargs["sensors"] = [u'Computer Name', u'Installed Applications']
kwargs["qtype"] = u'manual_human'

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
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
2015-02-11 11:59:11,806 INFO     question_progress: Results 0% (Get Computer Name and Installed Applications from all machines)
2015-02-11 11:59:16,825 INFO     question_progress: Results 0% (Get Computer Name and Installed Applications from all machines)
2015-02-11 11:59:21,844 INFO     question_progress: Results 0% (Get Computer Name and Installed Applications from all machines)
2015-02-11 11:59:26,863 INFO     question_progress: Results 100% (Get Computer Name and Installed Applications from all machines)

Type of response:  <type 'dict'>

Pretty print of response:
{'question_object': <taniumpy.object_types.question.Question object at 0x1059d78d0>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x105a1f250>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Computer Name and Installed Applications from all machines

CSV Results of response: 
Computer Name,Name,Silent Uninstall String,Uninstallable,Version
Casus-Belli.local,"Google Search
Microsoft Chart Converter
Spotify
Wish
BluetoothUIServer
Time Machine
AppleGraphicsWarning
soagent
AinuIM
ARDAgent
Microsoft Clip Gallery
Pass Viewer
PressAndHold
PluginIM
..trimmed for brevity..

'''
