
"""
Ask a manual question using human strings by referencing the name of a single sensor that takes parameters, but supplying only two of the four parameters that are used by the sensor.

Also supply a sensor filter that limits the column data that is shown to values that match the regex '.*Shared.*', and a sensor filter option that re-fetches any cached data that is older than 3600 seconds.

No question filters or question options supplied.
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
kwargs["sensors"] = u'Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*}, that regex match:.*Shared.*, opt:max_data_age:3600'
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
2014-12-08 15:12:44,501 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines)
2014-12-08 15:12:49,518 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines)
2014-12-08 15:12:54,537 INFO     question_progress: Results 17% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines)
2014-12-08 15:12:59,553 INFO     question_progress: Results 17% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines)
2014-12-08 15:13:04,570 INFO     question_progress: Results 67% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines)
2014-12-08 15:13:09,588 INFO     question_progress: Results 100% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines)

Type of response:  <type 'dict'>

Pretty print of response:
{'question_object': <taniumpy.object_types.question.Question object at 0x10e03dad0>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10e1b2210>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines

CSV Results of response: 
Count,"Folder Name Search with RegEx Match[No, Program Files, No, ]"
4,[no results]
1,C:\Program Files\Common Files\Microsoft Shared\VS7Debug
2,C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
2,C:\Program Files\Common Files\Microsoft Shared\ink\ru-RU
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\keypad
2,C:\Program Files\Common Files\Microsoft Shared\ink
2,C:\Program Files\Common Files\Microsoft Shared\ink\sv-SE
2,C:\Program Files\Common Files\Microsoft Shared\ink\uk-UA
2,C:\Program Files\Common Files\Microsoft Shared\ink\sl-SI
2,C:\Program Files\Common Files\Microsoft Shared\ink\hu-HU
2,C:\Program Files\Common Files\Microsoft Shared\ink\zh-TW
2,C:\Program Files\Common Files\Microsoft Shared\ink\zh-CN
2,C:\Program Files\Common Files\Microsoft Shared\ink\fi-FI
2,C:\Program Files\Common Files\Microsoft Shared
2,C:\Program Files\Common Files\Microsoft Shared\ink\da-DK
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\oskmenu
2,C:\Program Files\Common Files\Microsoft Shared\ink\ko-KR
2,C:\Program Files\Common Files\Microsoft Shared\ink\it-IT
2,C:\Program Files\Common Files\Microsoft Shared\Triedit
1,C:\Program Files\Microsoft SQL Server\110\Shared
2,C:\Program Files\Common Files\Microsoft Shared\ink\he-IL
2,C:\Program Files\Common Files\Microsoft Shared\ink\ro-RO
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\oskpred
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\numbers
2,C:\Program Files\Common Files\Microsoft Shared\ink\nb-NO
2,C:\Program Files\Common Files\Microsoft Shared\ink\lv-LV
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\auxpad
2,C:\Program Files\Common Files\Microsoft Shared\TextConv
2,C:\Program Files\Common Files\Microsoft Shared\MSInfo\en-US
2,C:\Program Files\Common Files\Microsoft Shared\ink\nl-NL
1,C:\Program Files\Microsoft SQL Server\90\Shared\Resources\1033
2,C:\Program Files\Common Files\Microsoft Shared\ink\fr-FR
2,C:\Program Files\Common Files\Microsoft Shared\ink\tr-TR
2,C:\Program Files\Common Files\Microsoft Shared\VC
1,C:\Program Files\Common Files\Microsoft Shared\WF
1,C:\Program Files\Microsoft SQL Server\110\Shared\en
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\symbols
2,C:\Program Files\Common Files\Microsoft Shared\ink\lt-LT
2,C:\Program Files\Common Files\Microsoft Shared\ink\et-EE
2,C:\Program Files\Common Files\Microsoft Shared\ink\cs-CZ
1,C:\Program Files\Microsoft SQL Server\110\Shared\VS2008
2,C:\Program Files\Common Files\Microsoft Shared\ink\en-US
2,C:\Program Files\Common Files\Microsoft Shared\ink\bg-BG
1,C:\Program Files\Microsoft SQL Server\100\Shared
2,C:\Program Files\Common Files\Microsoft Shared\ink\es-ES
2,C:\Program Files\Common Files\Microsoft Shared\MSInfo
1,C:\Program Files\Microsoft SQL Server\110\Shared\RsFxInstall
1,C:\Program Files\Common Files\Microsoft Shared\WF\amd64
2,C:\Program Files\Common Files\Microsoft Shared\ink\de-DE
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\main
1,C:\Program Files\Microsoft SQL Server\90\Shared\Resources
2,C:\Program Files\Common Files\Microsoft Shared\ink\sr-Latn-CS
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\osknumpad
1,C:\Program Files\Microsoft SQL Server\110\Shared\Resources\1033
1,C:\Program Files\Common Files\Microsoft Shared\MSEnv
1,C:\Program Files\Microsoft SQL Server\110\Shared\VS2008\1033
2,C:\Program Files\Common Files\Microsoft Shared\ink\pt-BR
2,C:\Program Files\Common Files\Microsoft Shared\ink\pt-PT
2,C:\Program Files\Common Files\Microsoft Shared\ink\el-GR
1,C:\Program Files\Microsoft SQL Server\110\Shared\Resources
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\web
2,C:\Program Files\Common Files\Microsoft Shared\ink\ja-JP
2,C:\Program Files\Common Files\Microsoft Shared\ink\sk-SK
2,C:\Program Files\Common Files\Microsoft Shared\ink\hr-HR
2,C:\Program Files\Common Files\Microsoft Shared\VGX
2,C:\Program Files\Common Files\Microsoft Shared\Triedit\en-US
2,C:\Program Files\Common Files\Microsoft Shared\TextConv\en-US
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions
2,C:\Program Files\Common Files\Microsoft Shared\ink\th-TH
1,C:\Program Files\Common Files\Microsoft Shared\SQL Debugging
1,C:\Program Files\Microsoft SQL Server\90\Shared
2,C:\Program Files\Common Files\Microsoft Shared\ink\pl-PL
2,C:\Program Files\Common Files\Microsoft Shared\Stationery
1,C:\Program Files\Common Files\Microsoft Shared\VS7Debug\1033
1,C:\Program Files\Microsoft SQL Server\110\Shared\ErrorDumps


'''
