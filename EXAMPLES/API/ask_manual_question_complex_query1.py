
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
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
2015-08-06 14:49:13,745 DEBUG    pytan.handler.QuestionPoller: ID 86262: id resolved to 86262
2015-08-06 14:49:13,745 DEBUG    pytan.handler.QuestionPoller: ID 86262: expiration resolved to 2015-08-06T14:59:13
2015-08-06 14:49:13,745 DEBUG    pytan.handler.QuestionPoller: ID 86262: query_text resolved to Get Computer Name and Folder Name Search with RegEx Match[test, No, Program Files, No, , Microsoft.*] contains "Shared" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows"
2015-08-06 14:49:13,745 DEBUG    pytan.handler.QuestionPoller: ID 86262: id resolved to 86262
2015-08-06 14:49:13,745 DEBUG    pytan.handler.QuestionPoller: ID 86262: Object Info resolved to Question ID: 86262, Query: Get Computer Name and Folder Name Search with RegEx Match[test, No, Program Files, No, , Microsoft.*] contains "Shared" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows"
2015-08-06 14:49:13,750 DEBUG    pytan.handler.QuestionPoller: ID 86262: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:49:13,750 DEBUG    pytan.handler.QuestionPoller: ID 86262: Timing: Started: 2015-08-06 14:49:13.745310, Expiration: 2015-08-06 14:59:13, Override Timeout: None, Elapsed Time: 0:00:00.004934, Left till expiry: 0:09:59.249759, Loop Count: 1
2015-08-06 14:49:13,750 INFO     pytan.handler.QuestionPoller: ID 86262: Progress Changed 0% (0 of 2)
2015-08-06 14:49:18,758 DEBUG    pytan.handler.QuestionPoller: ID 86262: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:49:18,758 DEBUG    pytan.handler.QuestionPoller: ID 86262: Timing: Started: 2015-08-06 14:49:13.745310, Expiration: 2015-08-06 14:59:13, Override Timeout: None, Elapsed Time: 0:00:05.013298, Left till expiry: 0:09:54.241395, Loop Count: 2
2015-08-06 14:49:23,768 DEBUG    pytan.handler.QuestionPoller: ID 86262: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:49:23,768 DEBUG    pytan.handler.QuestionPoller: ID 86262: Timing: Started: 2015-08-06 14:49:13.745310, Expiration: 2015-08-06 14:59:13, Override Timeout: None, Elapsed Time: 0:00:10.023316, Left till expiry: 0:09:49.231377, Loop Count: 3
2015-08-06 14:49:28,773 DEBUG    pytan.handler.QuestionPoller: ID 86262: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:49:28,773 DEBUG    pytan.handler.QuestionPoller: ID 86262: Timing: Started: 2015-08-06 14:49:13.745310, Expiration: 2015-08-06 14:59:13, Override Timeout: None, Elapsed Time: 0:00:15.028001, Left till expiry: 0:09:44.226691, Loop Count: 4
2015-08-06 14:49:33,783 DEBUG    pytan.handler.QuestionPoller: ID 86262: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:49:33,783 DEBUG    pytan.handler.QuestionPoller: ID 86262: Timing: Started: 2015-08-06 14:49:13.745310, Expiration: 2015-08-06 14:59:13, Override Timeout: None, Elapsed Time: 0:00:20.038117, Left till expiry: 0:09:39.216576, Loop Count: 5
2015-08-06 14:49:38,793 DEBUG    pytan.handler.QuestionPoller: ID 86262: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
2015-08-06 14:49:38,793 DEBUG    pytan.handler.QuestionPoller: ID 86262: Timing: Started: 2015-08-06 14:49:13.745310, Expiration: 2015-08-06 14:59:13, Override Timeout: None, Elapsed Time: 0:00:25.048604, Left till expiry: 0:09:34.206088, Loop Count: 6
2015-08-06 14:49:38,793 INFO     pytan.handler.QuestionPoller: ID 86262: Progress Changed 50% (1 of 2)
2015-08-06 14:49:43,800 DEBUG    pytan.handler.QuestionPoller: ID 86262: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
2015-08-06 14:49:43,801 DEBUG    pytan.handler.QuestionPoller: ID 86262: Timing: Started: 2015-08-06 14:49:13.745310, Expiration: 2015-08-06 14:59:13, Override Timeout: None, Elapsed Time: 0:00:30.055755, Left till expiry: 0:09:29.198937, Loop Count: 7
2015-08-06 14:49:43,801 INFO     pytan.handler.QuestionPoller: ID 86262: Progress Changed 100% (2 of 2)
2015-08-06 14:49:43,801 INFO     pytan.handler.QuestionPoller: ID 86262: Reached Threshold of 99% (2 of 2)

Type of response:  <type 'dict'>

Pretty print of response:
{'poller_object': <pytan.pollers.QuestionPoller object at 0x1113c2c90>,
 'poller_success': True,
 'question_object': <taniumpy.object_types.question.Question object at 0x111365f10>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x1113c2850>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Computer Name and Folder Name Search with RegEx Match[test, No, Program Files, No, , Microsoft.*] contains "Shared" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows"

CSV Results of response: 
Computer Name,"Folder Name Search with RegEx Match[test, No, Program Files, No, , Microsoft.*]"
Casus-Belli.local,[no results]
jtanium1.localdomain,"C:\Program Files\Common Files\Microsoft Shared\VS7Debug
C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
C:\Program Files\Common Files\Microsoft Shared\ink\ru-RU
C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\keypad
C:\Program Files\Common Files\Microsoft Shared\ink
C:\Program Files\Common Files\Microsoft Shared\ink\sv-SE
C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2977326\GDR\1033_enu_lp\x64\setup\sqlsupport_msi\pfiles32\sqlservr\110\shared
C:\Program Files\Common Files\Microsoft Shared\ink\uk-UA
C:\Program Files\Common Files\Microsoft Shared\ink\sl-SI
C:\Program Files\Common Files\Microsoft Shared\ink\hu-HU
C:\Program Files\Common Files\Microsoft Shared\ink\zh-TW
C:\Program Files\Common Files\Microsoft Shared\ink\zh-CN
C:\Program Files\Common Files\Microsoft Shared\ink\fi-FI
..trimmed for brevity..

'''
