#!/usr/bin/env python
"""
Export a ResultSet from asking a question as CSV with true for header_add_sensor, true for header_add_type, true for header_sort, and true for expand_grouped_columns
"""
# import the basic python packages we need
import os
import sys
import tempfile
import pprint
import traceback

# disable python from generating a .pyc file
sys.dont_write_bytecode = True

# change me to the path of pytan if this script is not running from EXAMPLES/PYTAN_API
pytan_loc = "~/gh/pytan"
pytan_static_path = os.path.join(os.path.expanduser(pytan_loc), 'lib')

# Determine our script name, script dir
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)

# try to automatically determine the pytan lib directory by assuming it is in '../../lib/'
parent_dir = os.path.dirname(my_dir)
pytan_root_dir = os.path.dirname(parent_dir)
lib_dir = os.path.join(pytan_root_dir, 'lib')

# add pytan_loc and lib_dir to the PYTHONPATH variable
path_adds = [lib_dir, pytan_static_path]
[sys.path.append(aa) for aa in path_adds if aa not in sys.path]

# import pytan
import pytan

# create a dictionary of arguments for the pytan handler
handler_args = {}

# establish our connection info for the Tanium Server
handler_args['username'] = "Administrator"
handler_args['password'] = "Tanium2015!"
handler_args['host'] = "10.0.1.240"
handler_args['port'] = "443"  # optional

# optional, level 0 is no output except warnings/errors
# level 1 through 12 are more and more verbose
handler_args['loglevel'] = 1

# optional, use a debug format for the logging output (uses two lines per log entry)
handler_args['debugformat'] = False

# optional, this saves all response objects to handler.session.ALL_REQUESTS_RESPONSES
# very useful for capturing the full exchange of XML requests and responses
handler_args['record_all_requests'] = True

# instantiate a handler using all of the arguments in the handler_args dictionary
print "...CALLING: pytan.handler() with args: {}".format(handler_args)
handler = pytan.Handler(**handler_args)

# print out the handler string
print "...OUTPUT: handler string: {}".format(handler)

# setup the arguments for the handler() class
kwargs = {}
kwargs["header_sort"] = True
kwargs["export_format"] = u'csv'
kwargs["header_add_type"] = True
kwargs["expand_grouped_columns"] = True
kwargs["header_add_sensor"] = True

# setup the arguments for handler.ask()
ask_kwargs = {
    'qtype': 'manual',
    'sensors': [
        "Computer Name", "IP Route Details", "IP Address",
        'Folder Contents{folderPath=C:\Program Files}',
    ],
}

# ask the question that will provide the resultset that we want to use
print "...CALLING: handler.ask() with args {}".format(ask_kwargs)
response = handler.ask(**ask_kwargs)

# store the resultset object as the obj we want to export into kwargs
kwargs['obj'] = response['question_results']

# export the object to a string
# (we could just as easily export to a file using export_to_report_file)
print "...CALLING: handler.export_obj() with args {}".format(kwargs)
out = handler.export_obj(**kwargs)

# trim the output if it is more than 15 lines long
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\n'.join(out)

print "...OUTPUT: print the export_str returned from export_obj():"
print out

'''STDOUT from running this:
...CALLING: pytan.handler() with args: {'username': 'Administrator', 'record_all_requests': True, 'loglevel': 1, 'debugformat': False, 'host': '10.0.1.240', 'password': 'Tanium2015!', 'port': '443'}
...OUTPUT: handler string: PyTan v2.1.4 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
...CALLING: handler.ask() with args {'sensors': ['Computer Name', 'IP Route Details', 'IP Address', 'Folder Contents{folderPath=C:\\Program Files}'], 'qtype': 'manual'}
2015-09-14 20:01:59,031 INFO     pytan.pollers.QuestionPoller: ID 771: Reached Threshold of 99% (3 of 3)
...CALLING: handler.export_obj() with args {'header_add_sensor': True, 'obj': <taniumpy.object_types.result_set.ResultSet object at 0x1068522d0>, 'export_format': u'csv', 'expand_grouped_columns': True, 'header_sort': True, 'header_add_type': True}
...OUTPUT: print the export_str returned from export_obj():
Computer Name: Computer Name (String),Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),IP Address: IP Address (IPAddress),IP Route Details: Destination (IPAddress),IP Route Details: Flags (String),IP Route Details: Gateway (IPAddress),IP Route Details: Interface (String),IP Route Details: Mask (String),IP Route Details: Metric (NumericInteger)
c1u14-virtual-machine.(none),N/A on Linux,10.0.1.12,0.0.0.0,UG,10.0.1.1,eth0,0.0.0.0,0
c1u14-virtual-machine.(none),N/A on Linux,10.0.1.12,10.0.1.0,U,0.0.0.0,eth0,255.255.255.0,1
TPT1.pytanlab.com,Folder : Microsoft Visual Studio 10.0,10.0.1.240,UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String)
TPT1.pytanlab.com,desktop.ini,10.0.1.240,UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String)
TPT1.pytanlab.com,Folder : Windows NT,10.0.1.240,UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String)
TPT1.pytanlab.com,Folder : Microsoft Help Viewer,10.0.1.240,UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String)
TPT1.pytanlab.com,Folder : Reference Assemblies,10.0.1.240,UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String)
TPT1.pytanlab.com,Folder : Common Files,10.0.1.240,UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String)
TPT1.pytanlab.com,Folder : Tanium,10.0.1.240,UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String)
TPT1.pytanlab.com,Folder : Microsoft.NET,10.0.1.240,UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String)
TPT1.pytanlab.com,Folder : OpenSSH,10.0.1.240,UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String)
TPT1.pytanlab.com,Folder : VMware,10.0.1.240,UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String)
TPT1.pytanlab.com,Folder : Internet Explorer,10.0.1.240,UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String)
TPT1.pytanlab.com,Folder : Uninstall Information,10.0.1.240,UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String),UNRELATED TO Folder Contents[C:\Program Files]: Folder Contents[C:\Program Files] (String)
..trimmed for brevity..

'''

'''STDERR from running this:

'''
