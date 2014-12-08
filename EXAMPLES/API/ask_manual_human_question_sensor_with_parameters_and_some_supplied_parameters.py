
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
print out.getvalue()



'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
2014-12-08 15:06:02,320 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 15:06:07,338 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 15:06:12,356 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 15:06:17,374 INFO     question_progress: Results 50% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 15:06:22,392 INFO     question_progress: Results 50% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 15:06:27,409 INFO     question_progress: Results 100% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)

Type of response:  <type 'dict'>

Pretty print of response:
{'question_object': <taniumpy.object_types.question.Question object at 0x10e805690>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10e622690>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines

CSV Results of response: 
Count,"Folder Name Search with RegEx Match[No, Program Files, No, ]"
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\cgi-bin
2,C:\Program Files\VMware\VMware Tools\plugins\vmsvc
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1040_ITA_LP\x64\1040\help
1,C:\Program Files\Common Files\Microsoft Shared\VS7Debug
1,C:\Program Files\Tanium\Tanium Server\Apache24\manual\style
1,C:\Program Files\Tanium\Tanium Server\Apache24\htdocs\console\history
2,C:\Program Files\Common Files\VMware\Drivers\vmci\sockets\include
2,C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
1,C:\Program Files\Tanium\Tanium Server\plugins\console\Dashboards
1,C:\Program Files\Tanium\Tanium Server\CertificateBackup2014-11-17-11-17-33
2,C:\Program Files\Common Files\SpeechEngines\Microsoft
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\modules
2,C:\Program Files\Common Files\Microsoft Shared\ink\ru-RU
1,C:\Program Files\Microsoft SQL Server\110\DTS\ForEachEnumerators\en
1,C:\Program Files\Tanium\Tanium Server\Apache24\htdocs\php\Auth
1,C:\Program Files\MSBuild\Microsoft\Windows Workflow Foundation\v3.0
1,C:\Program Files\MSBuild\Microsoft\Windows Workflow Foundation\v3.5
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\2052_CHS_LP\x64
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\keypad
1,C:\Program Files\Tanium\Tanium Server\plugins\console\InstallPlugin
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112831\resources
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Bin
1,C:\Program Files\Microsoft SQL Server\110\DTS\ForEachEnumerators
1,C:\Program Files\Tanium\Tanium Server\Apache24\conf
1,C:\Program Files\MSBuild\Microsoft
1,C:\Program Files\Microsoft SQL Server\110\DTS\UpgradeMappings
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\htdocs\php\Auth
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\style\css
2,C:\Program Files\Common Files\Microsoft Shared\ink
2,C:\Program Files\Common Files\Microsoft Shared\ink\sv-SE
2,C:\Program Files\VMware\VMware Tools\messages
1,C:\Program Files\Microsoft SQL Server\110\DTS\ForEachEnumerators\Resources
2,C:\Program Files\Common Files\Microsoft Shared\ink\uk-UA
1,C:\Program Files\Microsoft SQL Server\110\DTS\Binn\Resources\1033
1,C:\Program Files\Tanium\Tanium Server\Apache24\manual\platform
1,C:\Program Files\Microsoft SQL Server\110\KeyFile
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\3082
1,C:\Program Files\Tanium\Tanium Server\CertificateBackup2014-09-16-20-44-23
1,C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap\Release\x64\1033
1,C:\Program Files\Microsoft.NET\ADOMD.NET
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1028_CHT_LP\x64\1028\help
2,C:\Program Files\Common Files\Microsoft Shared\ink\sl-SI
1,C:\Program Files\Tanium\Tanium Server\plugins\console\UserGroups
2,C:\Program Files\Common Files\Microsoft Shared\ink\hu-HU
2,C:\Program Files\Common Files\System\en-US
2,C:\Program Files\Common Files\Microsoft Shared\ink\zh-TW
2,C:\Program Files\Common Files\Microsoft Shared\ink\zh-CN
2,C:\Program Files\Common Files\VMware\Drivers\video_wddm
2,C:\Program Files\Common Files\Microsoft Shared\ink\fi-FI
2,C:\Program Files\Common Files\Microsoft Shared
1,C:\Program Files\Microsoft SQL Server\110\SDK\Include
2,C:\Program Files\Common Files\Microsoft Shared\ink\da-DK
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\icons\small
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33
1,C:\Program Files\Microsoft Visual Studio 10.0\Common7\IDE\PrivateAssemblies
1,C:\Program Files\Microsoft SQL Server\80
1,C:\Program Files\Microsoft SQL Server\90
2,C:\Program Files\Windows Mail
2,C:\Program Files\Common Files\VMware\Drivers\vmci\sockets\bin\win64
2,C:\Program Files\Common Files\VMware\Drivers\vmci\sockets\bin\win32
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\oskmenu
1,C:\Program Files\Microsoft SQL Server\110\DTS\LogProviders
1,C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap\Release\Resources\1033
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1049_RUS_LP\x64\1049
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112604\Datastore_GlobalRules
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\images
1,C:\Program Files\Microsoft SQL Server\110\SDK
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1036_FRA_LP\x64
2,C:\Program Files\Windows NT\Accessories
1,C:\Program Files\Tanium\Tanium Server\content_public_keys
2,C:\Program Files\Windows NT\TableTextService\en-US
1,C:\Program Files\Tanium\Tanium Server\plugins\console\Manifest
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\bin
1,C:\Program Files\Tanium\Tanium Server\Apache24\logs
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1033_ENU_LP
1,C:\Program Files\Tanium\Tanium Server\plugins\content
1,C:\Program Files\Reference Assemblies\Microsoft\Framework
1,C:\Program Files\Microsoft SQL Server\110\DTS\Connections\en
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\icons\small
2,C:\Program Files\Common Files\VMware\Drivers\Virtual Printer\TPOG3\amd64
1,C:\Program Files\Microsoft Visual Studio 10.0\Common7\IDE\PrivateAssemblies\1033
2,C:\Program Files\Common Files\Microsoft Shared\ink\ko-KR
1,C:\Program Files\Tanium\Tanium Server\Apache24\manual\ssl
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1042_KOR_LP\x64
1,C:\Program Files\Tanium\Tanium Server\Apache24\manual\style\css
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\misc
1,C:\Program Files\Microsoft SQL Server\110\SDK\Lib\x64
1,C:\Program Files\Microsoft SQL Server\110\SDK\Lib\x86
1,C:\Program Files\Tanium\Tanium Server\plugins\console\lib
2,C:\Program Files\Common Files\Microsoft Shared\ink\it-IT
1,C:\Program Files\Microsoft.NET
1,C:\Program Files\Microsoft SQL Server\110\DTS\DataDumps
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\conf
1,C:\Program Files\Internet Explorer\images
2,C:\Program Files\Windows NT
1,C:\Program Files\Microsoft SQL Server\110\COM\Resources\1033
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\JOBS
1,C:\Program Files\Tanium\Tanium Server\Apache24\htdocs
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1041_JPN_LP
1,C:\Program Files\Tanium\Tanium Server\php55\extras
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1031_DEU_LP\x64\1031\help
1,C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap
2,C:\Program Files\Common Files\SpeechEngines\Microsoft\TTS20
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23
2,C:\Program Files\Common Files\Microsoft Shared\Triedit
1,C:\Program Files\Microsoft.NET\ADOMD.NET\110
1,C:\Program Files\Microsoft SQL Server\110\Shared
1,C:\Program Files\Microsoft SQL Server\110\Tools\Binn
1,C:\Program Files\Microsoft Help Viewer
1,C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap\Release\x64\Patch
1,C:\Program Files\Tanium\Tanium Server\Apache24\bin\iconv
2,C:\Program Files\Common Files\VMware\Drivers\memctl
1,C:\Program Files\Tanium\Tanium Server\plugins\console
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\conf\original
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\htdocs\php
1,C:\Program Files\Microsoft SQL Server\90\License Terms
1,C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap\Release\Resources
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\pt
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\ru
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\lib
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\it
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\ko
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\ja
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\es
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\de
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\fr
2,C:\Program Files\Common Files\Microsoft Shared\ink\he-IL
2,C:\Program Files\Common Files\Microsoft Shared\ink\ro-RO
2,C:\Program Files\Common Files\VMware\Drivers\pvscsi
1,C:\Program Files\Microsoft Visual Studio 10.0\Common7\Packages
1,C:\Program Files\Microsoft Visual Studio 10.0\Common7
2,C:\Program Files\Common Files\Services
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\oskpred
1,C:\Program Files\Microsoft SQL Server\110\SDK\Lib
1,C:\Program Files\Microsoft SQL Server\110\DTS\PipelineComponents\Resources\1033
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\misc
1,C:\Program Files\Tanium\Tanium Server\Apache24\manual\misc
2,C:\Program Files\Common Files\SpeechEngines\Microsoft\TTS20\en-US
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\modules
1,C:\Program Files\Microsoft SQL Server\110\DTS\Connections
1,C:\Program Files\Tanium\Tanium Server\Downloads\URLCache
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1046_PTB_LP
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\rewrite
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\images
2,C:\Program Files\Common Files\VMware\Drivers\vmci\device
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\rewrite
2,C:\Program Files\Common Files
1,C:\Program Files\Tanium\Tanium Server\Apache24\manual
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\platform
1,C:\Program Files\Tanium\Tanium Server\Apache24\conf\extra
2,C:\Program Files\Common Files\VMware\Drivers\vmci
2,C:\Program Files\Common Files\System\msadc\en-US
2,C:\Program Files\Common Files\System
2,C:\Program Files\Windows NT\Accessories\en-US
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1036_FRA_LP\x64\1036
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources
1,C:\Program Files\Tanium\Tanium Server\plugins\console\RegistrySetting
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1046_PTB_LP\x64\1046
1,C:\Program Files\Tanium\Tanium Server\Apache24\manual\rewrite
2,C:\Program Files\VMware\VMware Tools
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\numbers
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1049_RUS_LP\x64
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Log
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\lib
2,C:\Program Files\Windows NT\TableTextService
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1055
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1053
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1049
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1041
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1040
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1043
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1042
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1045
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1044
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1046
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1038
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1035
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1036
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1030
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1031
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1032
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1033
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1029
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1028
1,C:\Program Files\Tanium\Tanium Server\Apache24\htdocs\console
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1042_KOR_LP\x64\1042
1,C:\Program Files\Tanium\Tanium Server\Apache24\error
2,C:\Program Files\Common Files\Microsoft Shared\ink\nb-NO
1,C:\Program Files\Tanium\Tanium Server\Apache24\manual\mod
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1041_JPN_LP\x64
2,C:\Program Files\Common Files\Microsoft Shared\ink\lv-LV
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1033_ENU_LP\x64\1033
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\conf\original\extra
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\auxpad
2,C:\Program Files\Common Files\Microsoft Shared\TextConv
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\developer
2,C:\Program Files\Common Files\Microsoft Shared\MSInfo\en-US
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\3082_ESN_LP\x64\3082
2,C:\Program Files\Common Files\Microsoft Shared\ink\nl-NL
1,C:\Program Files\Tanium
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\howto
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\include
1,C:\Program Files\Reference Assemblies\Microsoft\Framework\v3.5\RedistList
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112532\Datastore_LandingPage
1,C:\Program Files\Microsoft SQL Server\100\KeyFile\1033
1,C:\Program Files\Microsoft SQL Server\110\Tools\Binn\Resources\1033
1,C:\Program Files\Tanium\Tanium Server\Downloads\Cache
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\style\latex
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\3082_ESN_LP
1,C:\Program Files\Tanium\Tanium Server\php55\dev
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\bin\iconv
2,C:\Program Files\VMware\VMware Tools\messages\zh_CN
1,C:\Program Files\Tanium\Tanium Server\Apache24\manual\vhosts
2,C:\Program Files\Common Files\VMware\Drivers\vmci\sockets
1,C:\Program Files\Microsoft SQL Server\90\Shared\Resources\1033
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\conf
2,C:\Program Files\Common Files\VMware
2,C:\Program Files\Common Files\System\msadc
1,C:\Program Files\Microsoft SQL Server\110\Tools
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\htdocs\php
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1040_ITA_LP
2,C:\Program Files\Common Files\Microsoft Shared\ink\fr-FR
2,C:\Program Files\Common Files\VMware\Drivers\vss
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\bin
2,C:\Program Files\Common Files\Microsoft Shared\ink\tr-TR
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\programs
2,C:\Program Files\Common Files\Microsoft Shared\VC
1,C:\Program Files\Tanium\Tanium Server\php55\ext
1,C:\Program Files\Common Files\Microsoft Shared\WF
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\ssl
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\htdocs
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\htdocs\console
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Templates
1,C:\Program Files\Tanium\Tanium Server\plugins
1,C:\Program Files\Tanium\Tanium Server\Apache24\icons\small
1,C:\Program Files\Microsoft SQL Server\110\Shared\en
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\htdocs\php\Auth
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\error\include
1,C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap\Release\x64\Help
1,C:\Program Files\Microsoft Help Viewer\v1.0\Microsoft Help Viewer 1.1
4,Windows Only
1,C:\Program Files\Microsoft SQL Server\110\Tools\Binn\ManagementStudio
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\symbols
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1036_FRA_LP\x64\1036\help
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual
2,C:\Program Files\Common Files\System\Ole DB\en-US
1,C:\Program Files\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\Extensions
1,C:\Program Files\Microsoft SQL Server\80\Tools\Binn
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\2052_CHS_LP
2,C:\Program Files\Common Files\Microsoft Shared\ink\lt-LT
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\htdocs
1,C:\Program Files\Microsoft SQL Server\100\KeyFile
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\style
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Install
2,C:\Program Files\Common Files\Microsoft Shared\ink\et-EE
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1028_CHT_LP
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1040_ITA_LP\x64\1040
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1028_CHT_LP\x64
2,C:\Program Files\Common Files\VMware\Drivers\Virtual Printer\TPOGPS
2,C:\Program Files\Common Files\Microsoft Shared\ink\cs-CZ
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\2052_CHS_LP\x64\2052\help
2,C:\Program Files\VMware
1,C:\Program Files\Microsoft SQL Server\110\Shared\VS2008
1,C:\Program Files\Microsoft Visual Studio 10.0\Common7\Packages\Debugger
2,C:\Program Files\Common Files\VMware\Drivers\mouse
2,C:\Program Files\Common Files\VMware\Drivers\vmci\sockets\bin
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\bin\iconv
2,C:\Program Files\Common Files\Microsoft Shared\ink\en-US
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Backup
1,C:\Program Files\Tanium\Tanium Server\VB
1,C:\Program Files\Microsoft SQL Server\110\DTS\ForEachEnumerators\Resources\1033
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\vhosts
2,C:\Program Files\Common Files\Microsoft Shared\ink\bg-BG
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\ssl
1,C:\Program Files\Tanium\Tanium Server\Apache24\bin
2,C:\Program Files\Common Files\System\Ole DB
1,C:\Program Files\Tanium\Tanium Server\Apache24\manual\faq
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS
2,C:\Program Files\Common Files\VMware\Drivers\audio
1,C:\Program Files\Microsoft SQL Server\110\DTS\Binn\Resources
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1041_JPN_LP\x64\1041
1,C:\Program Files\Reference Assemblies\Microsoft\Framework\v3.0\RedistList
1,C:\Program Files\Tanium\Tanium Server\Downloads
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1049_RUS_LP\x64\1049\help
1,C:\Program Files\Microsoft Visual Studio 10.0\Common7\Packages\Debugger\x86
1,C:\Program Files\Microsoft Visual Studio 10.0\Common7\Packages\Debugger\X64
1,C:\Program Files\MSBuild\Microsoft\Windows Workflow Foundation
1,C:\Program Files\Microsoft SQL Server\100\Shared
2,C:\Program Files\Internet Explorer\SIGNUP
2,C:\Program Files\Common Files\Microsoft Shared\ink\es-ES
1,C:\Program Files\Tanium\Tanium Server\Support
1,C:\Program Files\Microsoft SQL Server\110\DTS\Binn
2,C:\Program Files\Common Files\Microsoft Shared\MSInfo
1,C:\Program Files\Reference Assemblies
1,C:\Program Files\Microsoft SQL Server\110\Shared\RsFxInstall
1,C:\Program Files\Microsoft Help Viewer\v1.0\CatalogInfo
1,C:\Program Files\Microsoft SQL Server\110\DTS\MappingFiles
1,C:\Program Files\Microsoft SQL Server\110\DTS\PipelineComponents\Resources
1,C:\Program Files\Common Files\Microsoft Shared\WF\amd64
1,C:\Program Files\Tanium\Tanium Server\plugins\console\SigVerifier
1,C:\Program Files\Tanium\Tanium Server\plugins\console\DashboardGroups
1,C:\Program Files\Microsoft SQL Server\80\Tools
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Template Data
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\icons
2,C:\Program Files\Common Files\Microsoft Shared\ink\de-DE
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1031_DEU_LP\x64\1031
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1042_KOR_LP
1,C:\Program Files\Microsoft Visual Studio 10.0\Common7\IDE
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1033_ENU_LP\x64\1033\help
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\main
1,C:\Program Files\Microsoft Help Viewer\v1.0\StopWords
1,C:\Program Files\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\Extensions\Application
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\repldata
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\zh-CHT
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\zh-CHS
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\vhosts
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1042_KOR_LP\x64\1042\help
1,C:\Program Files\Microsoft SQL Server\110\DTS\Tasks\en
2,C:\Program Files\Common Files\SpeechEngines
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\logs
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\mod
2,C:\Program Files\VMware\VMware Tools\Drivers\hgfs
1,C:\Program Files\Tanium\Tanium Server\Apache24\conf\original
2,C:\Program Files\Uninstall Information
1,C:\Program Files\Reference Assemblies\Microsoft\Framework\v3.5
1,C:\Program Files\Reference Assemblies\Microsoft\Framework\v3.0
1,C:\Program Files\Microsoft Visual Studio 10.0\Common7\IDE\Xml
1,C:\Program Files\Microsoft SQL Server\110\DTS\PipelineComponents
1,C:\Program Files\Microsoft SQL Server\90\Shared\Resources
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1046_PTB_LP\x64\1046\help
1,C:\Program Files\Tanium\Tanium Server\Apache24\include
1,C:\Program Files\Tanium\Tanium Server\plugins\console\GroupFiliters
2,C:\Program Files\VMware\VMware Tools\Drivers
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1041_JPN_LP\x64\1041\help
1,C:\Program Files\Tanium\Tanium Server\Downloads\tmp
1,C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap\Release
1,C:\Program Files\Tanium\Tanium Server\Apache24\conf\original\extra
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\style\scripts
2,C:\Program Files\Common Files\Microsoft Shared\ink\sr-Latn-CS
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\osknumpad
1,C:\Program Files\Microsoft SQL Server\110\License Terms
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1031_DEU_LP\x64
2,C:\Program Files\Common Files\VMware\Drivers\vmxnet
1,C:\Program Files\Tanium\Tanium Server\Strings
1,C:\Program Files\MSBuild
1,C:\Program Files\Microsoft SQL Server\110\COM\Resources
2,C:\Program Files\Common Files\VMware\Drivers\Virtual Printer\TPOGPS\amd64
1,C:\Program Files\Microsoft SQL Server\80\COM
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\htdocs\console\history
1,C:\Program Files\Tanium\Tanium Server\Apache24\manual\howto
1,C:\Program Files\Microsoft SQL Server\110\Shared\Resources\1033
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\conf\extra
1,C:\Program Files\Common Files\Microsoft Shared\MSEnv
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\2052_CHS_LP\x64\2052
2,C:\Program Files\Common Files\VMware\Drivers\Virtual Printer
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\htdocs\console\history
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1028_CHT_LP\x64\1028
1,C:\Program Files\Microsoft SQL Server\110\Shared\VS2008\1033
2,C:\Program Files\Common Files\Microsoft Shared\ink\pt-BR
2,C:\Program Files\Common Files\Microsoft Shared\ink\pt-PT
2,C:\Program Files\Common Files\System\ado
1,C:\Program Files\Microsoft SQL Server\110\KeyFile\1033
1,C:\Program Files\Tanium\Tanium Server\SOAPUpload
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\2052
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112604\resources
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\DATA
1,C:\Program Files\Tanium\Tanium Server\php55\extras\ssl
2,C:\Program Files\Common Files\Microsoft Shared\ink\el-GR
2,C:\Program Files\VMware\VMware Tools\win32
2,C:\Program Files\VMware\VMware Tools\win64
1,C:\Program Files\Microsoft SQL Server\110\Shared\Resources
2,C:\Program Files\Internet Explorer
1,C:\Program Files\Tanium\Tanium Server\Apache24\icons
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1033_ENU_LP\x64
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1031_DEU_LP
1,C:\Program Files\Tanium\Tanium Server\Apache24\manual\programs
2,C:\Program Files\Common Files\VMware\Drivers\vmxnet3
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1049_RUS_LP
2,C:\Program Files\VMware\VMware Tools\Drivers\hgfs\wow64
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log
1,C:\Program Files\Microsoft SQL Server\90\License Terms\1033
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\logs
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\faq
1,C:\Program Files\Tanium\Tanium Server\Suppot_patch1
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\web
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\cgi-bin
1,C:\Program Files\Tanium\Tanium Server\Apache24\manual\developer
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\1036
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\1033
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\1031
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\1028
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\1049
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\1046
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\1042
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\1041
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\1040
1,C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap\Release\x64
1,C:\Program Files\Tanium\Tanium Server\Apache24\manual\style\latex
1,C:\Program Files\Tanium\Tanium Server
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\htdocs\console
1,C:\Program Files\Tanium\Tanium Server\http
2,C:\Program Files\Common Files\Microsoft Shared\ink\ja-JP
1,C:\Program Files\Microsoft SQL Server\110\DTS\Packages
2,C:\Program Files\Common Files\Microsoft Shared\ink\sk-SK
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\style\css
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\conf\original
1,C:\Program Files\Tanium\Tanium Server\Apache24\htdocs\php
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\howto
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\style\latex
2,C:\Program Files\Common Files\Microsoft Shared\ink\hr-HR
2,C:\Program Files\Common Files\VMware\Drivers
1,C:\Program Files\Tanium\Tanium Server\Apache24\lib
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112532
1,C:\Program Files\Microsoft Help Viewer\v1.0
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\conf\extra
1,C:\Program Files\Tanium\Tanium Server\Apache24
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\style\scripts
2,C:\Program Files\Common Files\Microsoft Shared\VGX
1,C:\Program Files\Microsoft SQL Server\110\DTS\ProviderDescriptors
1,C:\Program Files\Microsoft SQL Server\110\COM\en
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\faq
1,C:\Program Files\Tanium\Tanium Server\Apache24\manual\style\scripts
2,C:\Program Files\Common Files\Microsoft Shared\Triedit\en-US
1,C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap\Release\x64\Help\1033
1,C:\Program Files\Microsoft SQL Server\110\COM
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1046_PTB_LP\x64
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112831\Datastore_GlobalRules
2,C:\Program Files\Common Files\Microsoft Shared\TextConv\en-US
2,C:\Program Files\VMware\VMware Tools\plugins
1,C:\Program Files\Microsoft SQL Server\110\DTS
1,C:\Program Files\Tanium\Tanium Server\plugins\console\SavedQuestions
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\error\include
2,C:\Program Files\Common Files\System\ado\en-US
1,C:\Program Files\Tanium\Tanium Server\Apache24\cgi-bin
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112604
2,C:\Program Files\VMware\VMware Tools\plugins\vmusr
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112831\Datastore
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\DllTmp64
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\DllTmp32
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\programs
1,C:\Program Files\Microsoft SQL Server\110\Tools\Binn\Resources
1,C:\Program Files\Tanium\Tanium Server\php55
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\style
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1040_ITA_LP\x64
1,C:\Program Files\Reference Assemblies\Microsoft
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\include
1,C:\Program Files\Tanium\Tanium Server\Apache24\manual\images
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions
1,C:\Program Files\Microsoft SQL Server\110\SDK\Assemblies\en
1,C:\Program Files\Tanium\Tanium Server\Logs
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\mod
2,C:\Program Files\Common Files\VMware\Drivers\Virtual Printer\TPOG3
1,C:\Program Files\Microsoft SQL Server\110
1,C:\Program Files\Microsoft SQL Server\100
1,C:\Program Files\Tanium\Tanium Server\Apache24\modules
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\platform
1,C:\Program Files\Microsoft Visual Studio 10.0
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\3082
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112831
2,C:\Program Files\VMware\VMware Tools\plugins\common
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112804
2,C:\Program Files\Common Files\Microsoft Shared\ink\th-TH
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\icons
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112831\Datastore_ComponentUpdate
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\error
1,C:\Program Files\Microsoft SQL Server
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\error
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\3082_ESN_LP\x64
1,C:\Program Files\Common Files\Microsoft Shared\SQL Debugging
1,C:\Program Files\Tanium\Tanium Server\Apache24\error\include
1,C:\Program Files\Microsoft SQL Server\110\SDK\Assemblies
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\Patch
1,C:\Program Files\Microsoft Help Viewer\v1.0\en
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\3082_ESN_LP\x64\3082\help
1,C:\Program Files\Microsoft SQL Server\90\Shared
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\2052
1,C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\2070
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\conf\original\extra
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\developer
2,C:\Program Files\Common Files\Microsoft Shared\ink\pl-PL
2,C:\Program Files\Common Files\SpeechEngines\Microsoft\TTS20\en-US\enu-dsk
2,C:\Program Files\Common Files\Microsoft Shared\Stationery
1,C:\Program Files\Common Files\Microsoft Shared\VS7Debug\1033
1,C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap\Bin
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources
1,C:\Program Files\Microsoft SQL Server\110\Shared\ErrorDumps
2,C:\Program Files\Internet Explorer\en-US
2,C:\Program Files\VMware\VMware Tools\messages\it
2,C:\Program Files\VMware\VMware Tools\messages\ja
2,C:\Program Files\VMware\VMware Tools\messages\ko
2,C:\Program Files\VMware\VMware Tools\messages\de
2,C:\Program Files\VMware\VMware Tools\messages\es
2,C:\Program Files\VMware\VMware Tools\messages\fr
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1036_FRA_LP
1,C:\Program Files\Microsoft SQL Server\110\DTS\Tasks


'''
