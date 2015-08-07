
"""
Ask a manual question using human strings by referencing the name of a two sensors sensor.

Supply 3 parameters for the second sensor, one of which is not a valid parameter (and will be ignored).

Supply one option to the second sensor.

Supply two question filters that limit the rows returned in the result to computers that match the sensor Operating System that contains Windows and does not contain Windows.

Supply two question options that 'or' the two question filters and ignore the case of any values while matching the question filters.
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
kwargs["question_filters"] = [u'Operating System, that contains:Windows',
 u'Operating System, that does not contain:Windows']
kwargs["sensors"] = [u'Computer Name',
 u'Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*, invalidparam=test}, that regex match:.*Shared.*, opt:max_data_age:3600']
kwargs["question_options"] = [u'ignore_case', u'or']
kwargs["qtype"] = u'manual'

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
2015-08-07 19:44:01,651 DEBUG    pytan.handler.QuestionPoller: ID 1296: id resolved to 1296
2015-08-07 19:44:01,651 DEBUG    pytan.handler.QuestionPoller: ID 1296: expiration resolved to 2015-08-07T19:54:01
2015-08-07 19:44:01,651 DEBUG    pytan.handler.QuestionPoller: ID 1296: query_text resolved to Get Computer Name and Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*, test] containing "Shared" from all machines with ( Operating System containing "Windows" or any Operating System not containing "Windows" )
2015-08-07 19:44:01,651 DEBUG    pytan.handler.QuestionPoller: ID 1296: id resolved to 1296
2015-08-07 19:44:01,651 DEBUG    pytan.handler.QuestionPoller: ID 1296: Object Info resolved to Question ID: 1296, Query: Get Computer Name and Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*, test] containing "Shared" from all machines with ( Operating System containing "Windows" or any Operating System not containing "Windows" )
2015-08-07 19:44:01,655 DEBUG    pytan.handler.QuestionPoller: ID 1296: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:44:01,655 DEBUG    pytan.handler.QuestionPoller: ID 1296: Timing: Started: 2015-08-07 19:44:01.651938, Expiration: 2015-08-07 19:54:01, Override Timeout: None, Elapsed Time: 0:00:00.003335, Left till expiry: 0:09:59.344729, Loop Count: 1
2015-08-07 19:44:01,655 INFO     pytan.handler.QuestionPoller: ID 1296: Progress Changed 0% (0 of 2)
2015-08-07 19:44:06,659 DEBUG    pytan.handler.QuestionPoller: ID 1296: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:44:06,659 DEBUG    pytan.handler.QuestionPoller: ID 1296: Timing: Started: 2015-08-07 19:44:01.651938, Expiration: 2015-08-07 19:54:01, Override Timeout: None, Elapsed Time: 0:00:05.007902, Left till expiry: 0:09:54.340163, Loop Count: 2
2015-08-07 19:44:11,666 DEBUG    pytan.handler.QuestionPoller: ID 1296: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:44:11,667 DEBUG    pytan.handler.QuestionPoller: ID 1296: Timing: Started: 2015-08-07 19:44:01.651938, Expiration: 2015-08-07 19:54:01, Override Timeout: None, Elapsed Time: 0:00:10.015067, Left till expiry: 0:09:49.332998, Loop Count: 3
2015-08-07 19:44:16,670 DEBUG    pytan.handler.QuestionPoller: ID 1296: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-07 19:44:16,670 DEBUG    pytan.handler.QuestionPoller: ID 1296: Timing: Started: 2015-08-07 19:44:01.651938, Expiration: 2015-08-07 19:54:01, Override Timeout: None, Elapsed Time: 0:00:15.019009, Left till expiry: 0:09:44.329056, Loop Count: 4
2015-08-07 19:44:21,677 DEBUG    pytan.handler.QuestionPoller: ID 1296: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
2015-08-07 19:44:21,677 DEBUG    pytan.handler.QuestionPoller: ID 1296: Timing: Started: 2015-08-07 19:44:01.651938, Expiration: 2015-08-07 19:54:01, Override Timeout: None, Elapsed Time: 0:00:20.025509, Left till expiry: 0:09:39.322557, Loop Count: 5
2015-08-07 19:44:21,677 INFO     pytan.handler.QuestionPoller: ID 1296: Progress Changed 50% (1 of 2)
2015-08-07 19:44:26,687 DEBUG    pytan.handler.QuestionPoller: ID 1296: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
2015-08-07 19:44:26,687 DEBUG    pytan.handler.QuestionPoller: ID 1296: Timing: Started: 2015-08-07 19:44:01.651938, Expiration: 2015-08-07 19:54:01, Override Timeout: None, Elapsed Time: 0:00:25.035246, Left till expiry: 0:09:34.312819, Loop Count: 6
2015-08-07 19:44:31,691 DEBUG    pytan.handler.QuestionPoller: ID 1296: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
2015-08-07 19:44:31,692 DEBUG    pytan.handler.QuestionPoller: ID 1296: Timing: Started: 2015-08-07 19:44:01.651938, Expiration: 2015-08-07 19:54:01, Override Timeout: None, Elapsed Time: 0:00:30.040068, Left till expiry: 0:09:29.307997, Loop Count: 7
2015-08-07 19:44:31,692 INFO     pytan.handler.QuestionPoller: ID 1296: Progress Changed 100% (2 of 2)
2015-08-07 19:44:31,692 INFO     pytan.handler.QuestionPoller: ID 1296: Reached Threshold of 99% (2 of 2)

Type of response:  <type 'dict'>

Pretty print of response:
{'poller_object': <pytan.pollers.QuestionPoller object at 0x10a5c9690>,
 'poller_success': True,
 'question_object': <taniumpy.object_types.question.Question object at 0x10a5e1610>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10a615510>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Computer Name and Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*, test] containing "Shared" from all machines with ( Operating System containing "Windows" or any Operating System not containing "Windows" )

CSV Results of response: 
Computer Name,"Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*, test]"
Casus-Belli.local,[no results]
JTANIUM1.localdomain,"C:\Program Files\Common Files\Microsoft Shared\VS7Debug
C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
C:\Program Files\Common Files\Microsoft Shared\ink\ru-RU
C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\keypad
C:\Program Files\Common Files\Microsoft Shared\ink
C:\Program Files\Common Files\Microsoft Shared\ink\sv-SE
C:\Program Files\Common Files\Microsoft Shared\ink\uk-UA
C:\Program Files\Common Files\Microsoft Shared\ink\sl-SI
C:\Program Files\Common Files\Microsoft Shared\ink\hu-HU
C:\Program Files\Common Files\Microsoft Shared\ink\zh-TW
C:\Program Files\Common Files\Microsoft Shared\ink\zh-CN
C:\Program Files\Common Files\Microsoft Shared\ink\fi-FI
C:\Program Files\Common Files\Microsoft Shared
..trimmed for brevity..

'''
