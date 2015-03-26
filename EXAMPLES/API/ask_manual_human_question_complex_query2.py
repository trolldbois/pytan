
"""
This is another complex query that gets the Computer Name and Last Logged in User and Installed Applications that contains Google Search or Google Chrome and limits the rows that are displayed to computers that contain the Installed Applications of Google Search AND Google Chrome
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
kwargs["question_filters"] = [u'Installed Applications, that contains:Google Search',
 u'Installed Applications, that contains:Google Chrome']
kwargs["sensors"] = [u'Computer Name',
 u'Last Logged In User',
 u'Installed Applications, that contains:Google Search',
 u'Installed Applications, that contains:Google Chrome']
kwargs["question_options"] = [u'ignore_case', u'and']
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
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
2015-03-26 11:45:08,635 INFO     question_progress: Results 0% (Get Computer Name and Last Logged In User and Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome" from all machines where Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome")
2015-03-26 11:45:13,672 INFO     question_progress: Results 0% (Get Computer Name and Last Logged In User and Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome" from all machines where Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome")
2015-03-26 11:45:18,723 INFO     question_progress: Results 100% (Get Computer Name and Last Logged In User and Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome" from all machines where Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome")

Type of response:  <type 'dict'>

Pretty print of response:
{'question_object': <taniumpy.object_types.question.Question object at 0x10767b610>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x1076184d0>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Computer Name and Last Logged In User and Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome" from all machines where Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome"

CSV Results of response: 
Computer Name,Last Logged In User,Name,Name,Silent Uninstall String,Silent Uninstall String,Uninstallable,Uninstallable,Version,Version
Casus-Belli.local,N/A on Mac,Google Search,Google Search,nothing,nothing,Not Uninstallable,Not Uninstallable,37.0.2062.120,37.0.2062.120


'''
