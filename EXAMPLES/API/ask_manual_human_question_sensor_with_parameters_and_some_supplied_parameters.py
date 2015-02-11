
"""
Ask a manual question using human strings by referencing the name of a single sensor that takes parameters, but supplying only two of the four parameters that are used by the sensor (and letting pytan automatically determine the appropriate default value for those parameters which require a value and none was supplied).

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
kwargs["sensors"] = u'Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*}'
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
2015-02-11 11:59:37,165 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 11:59:42,179 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 11:59:47,194 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 11:59:52,211 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 11:59:57,225 INFO     question_progress: Results 100% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)

Type of response:  <type 'dict'>

Pretty print of response:
{'question_object': <taniumpy.object_types.question.Question object at 0x105a1f510>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x105b4af10>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines

CSV Results of response: 
"Folder Name Search with RegEx Match[No, Program Files, No, ]"
C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\cgi-bin
C:\Program Files\VMware\VMware Tools\plugins\vmsvc
C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1040_ITA_LP\x64\1040\help
C:\Program Files\Common Files\Microsoft Shared\VS7Debug
C:\Program Files\Tanium\Tanium Server\Apache24\manual\style
C:\Program Files\Tanium\Tanium Server\Apache24\htdocs\console\history
C:\Program Files\Common Files\VMware\Drivers\vmci\sockets\include
C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
C:\Program Files\Tanium\Tanium Server\plugins\console\Dashboards
C:\Program Files\Tanium\Tanium Server\CertificateBackup2014-11-17-11-17-33
C:\Program Files\Common Files\SpeechEngines\Microsoft
C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\modules
C:\Program Files\Common Files\Microsoft Shared\ink\ru-RU
C:\Program Files\Microsoft SQL Server\110\DTS\ForEachEnumerators\en
..trimmed for brevity..

'''
