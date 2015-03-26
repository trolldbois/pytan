
"""
Ask a manual question using human strings by referencing the name of multiple sensors, one that takes parameters, but supplying only two of the four parameters that are used by the sensor (and letting pytan automatically determine the appropriate default value for those parameters which require a value and none was supplied), and one that does not take parameters.

No sensor filters, question filters, or question options supplied.
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
kwargs["sensors"] = [u'Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*}',
 u'Computer Name']
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
2015-03-26 11:41:00,959 INFO     question_progress: Results 0% (Get Computer Name from all machines)
2015-03-26 11:41:05,976 INFO     question_progress: Results 0% (Get Computer Name from all machines)
2015-03-26 11:41:10,992 INFO     question_progress: Results 0% (Get Computer Name from all machines)
2015-03-26 11:41:16,155 INFO     question_progress: Results 50% (Get Computer Name from all machines)
2015-03-26 11:41:21,169 INFO     question_progress: Results 100% (Get Computer Name from all machines)

Type of response:  <type 'dict'>

Pretty print of response:
{'question_object': <taniumpy.object_types.question.Question object at 0x1075b8c10>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x107623550>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Computer Name from all machines

CSV Results of response: 
Computer Name,"Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*]"
Casus-Belli.local,Windows Only
jtanium1.localdomain,"C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2674319\ServicePack\1033_enu_lp\x64\setup\sqlsupport_msi\windows\winsxs\5z1v718o.6n8
C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2958429\ServicePack\1033_enu_lp\x64\setup\sqlsupport_msi\windows\winsxs\92rg91xw.1p4
C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2958429\ServicePack\1033_enu_lp\x64\setup\sqlsupport_msi\windows\winsxs\policies\u1sw1o0k.9hi
C:\Program Files\VMware\VMware Tools\plugins\vmsvc
C:\Program Files\Common Files\Microsoft Shared\VS7Debug
C:\Program Files\Tanium\Tanium Server\Apache24\manual\style
C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2674319\ServicePack\1033_enu_lp\x64\setup\sqlsupport_msi\windows\winsxs\vlv6b2rp.6fi
C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20150306_224415\resources
C:\Program Files\Tanium\Tanium Server\Apache24\htdocs\console\history
C:\Program Files\Windows Portable Devices
C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2977326\GDR\1033_enu_lp\x64\setup\sqlsupport_msi\pfiles\sqlservr\110\keyfile
C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2674319\ServicePack\1033_enu_lp\x64\setup\sql_engine_core_inst_loc_msi
C:\Program Files\Common Files\VMware\Drivers\vmci\sockets\include
..trimmed for brevity..

'''
