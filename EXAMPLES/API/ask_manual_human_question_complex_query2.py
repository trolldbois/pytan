
"""
This is another complex query that gets the Computer Name and Last Logged in User and Installed Applications that contains Google Search or Google Chrome and limits the rows that are displayed to computers that contain the Installed Applications of Google Search AND Google Chrome
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
kwargs["question_filters"] = [u'Installed Applications, that contains Google Search',
 u'Installed Applications, that contains Google Chrome']
kwargs["sensors"] = [u'Computer Name',
 u'Last Logged In User',
 u'Installed Applications, that contains Google Search',
 u'Installed Applications, that contains Google Chrome']
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
print out.getvalue()



'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
2014-12-07 01:08:15,186 INFO     question_progress: Results 0% (Get Computer Name and Last Logged In User and Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome" from all machines where Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome")
2014-12-07 01:08:20,216 INFO     question_progress: Results 100% (Get Computer Name and Last Logged In User and Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome" from all machines where Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome")

Type of response:  <type 'dict'>

Pretty print of response:
{'question_object': <taniumpy.object_types.question.Question object at 0x102303890>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x1022e4750>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Computer Name and Last Logged In User and Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome" from all machines where Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome"

CSV Results of response: 
Computer Name,Last Logged In User,Name,Name,Silent Uninstall String,Silent Uninstall String,Uninstallable,Uninstallable,Version,Version
Casus-Belli.local,[no results],Google Search,Google Search,nothing,nothing,Not Uninstallable,Not Uninstallable,37.0.2062.120,37.0.2062.120


'''
