
"""
Ask a manual question using human strings by referencing the name of a two sensors sensor.

Supply 3 parameters for the second sensor, one of which is not a valid parameter (and will be ignored).

Supply one option to the second sensor.

Supply two question filters that limit the rows returned in the result to computers that match the sensor Operating System that contains Windows and does not contain Windows.

Supply two question options that 'or' the two question filters and ignore the case of any values while matching the question filters.
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
kwargs["question_filters"] = [u'Operating System, that contains Windows',
 u'Operating System, that does not contain Windows']
kwargs["sensors"] = [u'Computer Name',
 u'Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*, invalidparam=test}, that regex match .*Shared.*, opt:max_data_age:3600']
kwargs["question_options"] = [u'ignore_case', u'or']
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
2014-12-07 01:07:49,920 INFO     question_progress: Results 0% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] matches "match .*Shared.*" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")
2014-12-07 01:07:54,941 INFO     question_progress: Results 0% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] matches "match .*Shared.*" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")
2014-12-07 01:07:59,961 INFO     question_progress: Results 0% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] matches "match .*Shared.*" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")
2014-12-07 01:08:04,980 INFO     question_progress: Results 50% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] matches "match .*Shared.*" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")
2014-12-07 01:08:10,005 INFO     question_progress: Results 50% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] matches "match .*Shared.*" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")
2014-12-07 01:08:15,026 INFO     question_progress: Results 100% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] matches "match .*Shared.*" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")

Type of response:  <type 'dict'>

Pretty print of response:
{'question_object': <taniumpy.object_types.question.Question object at 0x1020241d0>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x102024390>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] matches "match .*Shared.*" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows"

CSV Results of response: 
Computer Name,"Folder Name Search with RegEx Match[No, Program Files, No, ]"
Casus-Belli.local,[no results]
jtanium1.localdomain,[no results]


'''
