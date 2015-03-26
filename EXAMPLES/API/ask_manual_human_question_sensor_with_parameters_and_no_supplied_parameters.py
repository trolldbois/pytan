
"""
Ask a manual question using human strings by referencing the name of a single sensor that takes parameters, but not supplying any parameters (and letting pytan automatically determine the appropriate default value for those parameters which require a value).

No sensor filters, sensor parameters, sensor filter options, question filters, or question options supplied.
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
kwargs["sensors"] = u'Folder Name Search with RegEx Match'
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
2015-03-26 11:41:21,293 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2015-03-26 11:41:26,311 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2015-03-26 11:41:31,325 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2015-03-26 11:41:36,344 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2015-03-26 11:41:41,362 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2015-03-26 11:41:46,376 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2015-03-26 11:41:51,393 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2015-03-26 11:41:56,410 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2015-03-26 11:42:01,427 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2015-03-26 11:42:06,442 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2015-03-26 11:42:11,461 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2015-03-26 11:42:16,479 INFO     question_progress: Results 50% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2015-03-26 11:42:21,503 INFO     question_progress: Results 50% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2015-03-26 11:42:26,523 INFO     question_progress: Results 50% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2015-03-26 11:42:31,545 INFO     question_progress: Results 50% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2015-03-26 11:42:36,564 INFO     question_progress: Results 100% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)

Type of response:  <type 'dict'>

Pretty print of response:
{'question_object': <taniumpy.object_types.question.Question object at 0x1075b8210>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x107817210>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Folder Name Search with RegEx Match[No, , No, ] from all machines

CSV Results of response: 
Count,"Folder Name Search with RegEx Match[No, , No, ]"
24707,[too many results]
1,C:\Windows\winsxs\amd64_microsoft-windows-s..structure.resources_31bf3856ad364e35_6.1.7600.16385_en-us_faf46e6f502e00e8
1,C:\Windows\winsxs\x86_microsoft-windows-e..-host-authenticator_31bf3856ad364e35_6.1.7601.17514_none_a7c68343f07f776f
1,C:\Windows\winsxs\amd64_microsoft-windows-ocspsvc_31bf3856ad364e35_6.1.7601.22807_none_3bfeae7293092e4b
1,C:\Windows\winsxs\amd64_microsoft-windows-c..ityclient.resources_31bf3856ad364e35_6.1.7601.22865_en-us_c339d6d6cfb99c39
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2674319\ServicePack\1033_enu_lp\x64\setup\sqlsupport_msi\windows\winsxs\5z1v718o.6n8
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\System.Xml
1,C:\Windows\winsxs\amd64_microsoft-windows-scripting.resources_31bf3856ad364e35_6.1.7600.16385_en-us_e72192b67124ad43
1,C:\Windows\winsxs\x86_microsoft-windows-mlang.resources_31bf3856ad364e35_6.1.7600.16385_ru-ru_cf3a10abc52740f6
1,C:\Windows\winsxs\amd64_microsoft-windows-ie-internetexplorer_31bf3856ad364e35_11.2.9600.17041_none_11e6f4b92ee9bf19
1,C:\Windows\Installer\$PatchCache$\Managed\1F1FFB6230C555C4C9C7DF5688A9AF07
1,C:\Program Files (x86)\Windows Defender
1,C:\Users\Jim Olsen\AppData\Local\Google
1,C:\Windows\winsxs\x86_microsoft-windows-e..nt-client.resources_31bf3856ad364e35_6.1.7600.16385_en-us_e5c3d3ec6ff64de3
..trimmed for brevity..

'''
