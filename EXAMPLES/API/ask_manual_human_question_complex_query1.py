
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
2015-03-26 11:44:38,245 INFO     question_progress: Results 0% (Get Computer Name and Folder Name Search with RegEx Match[test, No, Program Files, No, , Microsoft.*] contains "Shared" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")
2015-03-26 11:44:43,272 INFO     question_progress: Results 0% (Get Computer Name and Folder Name Search with RegEx Match[test, No, Program Files, No, , Microsoft.*] contains "Shared" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")
2015-03-26 11:44:48,308 INFO     question_progress: Results 0% (Get Computer Name and Folder Name Search with RegEx Match[test, No, Program Files, No, , Microsoft.*] contains "Shared" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")
2015-03-26 11:44:53,341 INFO     question_progress: Results 0% (Get Computer Name and Folder Name Search with RegEx Match[test, No, Program Files, No, , Microsoft.*] contains "Shared" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")
2015-03-26 11:44:58,368 INFO     question_progress: Results 0% (Get Computer Name and Folder Name Search with RegEx Match[test, No, Program Files, No, , Microsoft.*] contains "Shared" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")
2015-03-26 11:45:03,396 INFO     question_progress: Results 0% (Get Computer Name and Folder Name Search with RegEx Match[test, No, Program Files, No, , Microsoft.*] contains "Shared" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")
2015-03-26 11:45:08,419 INFO     question_progress: Results 100% (Get Computer Name and Folder Name Search with RegEx Match[test, No, Program Files, No, , Microsoft.*] contains "Shared" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")

Type of response:  <type 'dict'>

Pretty print of response:
{'question_object': <taniumpy.object_types.question.Question object at 0x107619110>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x1078087d0>}

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
