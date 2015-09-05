#!/usr/bin/env python
"""
Export a ResultSet from asking a question as CSV with true for header_add_sensor
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
kwargs["export_format"] = u'csv'
kwargs["header_add_sensor"] = True

# setup the arguments for handler.ask()
ask_kwargs = {
    'qtype': 'manual',
    'sensors': [
        "Computer Name", "IP Route Details", "IP Address",
        'Folder Name Search with RegEx Match{dirname=Program Files,regex=.*Shared.*}',
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
...OUTPUT: handler string: PyTan v2.1.0 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
...CALLING: handler.ask() with args {'sensors': ['Computer Name', 'IP Route Details', 'IP Address', 'Folder Name Search with RegEx Match{dirname=Program Files,regex=.*Shared.*}'], 'qtype': 'manual'}
2015-09-05 05:40:41,153 INFO     pytan.pollers.QuestionPoller: ID 11637: Reached Threshold of 99% (2 of 2)
...CALLING: handler.export_obj() with args {'export_format': u'csv', 'obj': <taniumpy.object_types.result_set.ResultSet object at 0x1106af190>, 'header_add_sensor': True}
...OUTPUT: print the export_str returned from export_obj():
Computer Name: Computer Name,"Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*]: Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*]",IP Address: IP Address,IP Route Details: Destination,IP Route Details: Flags,IP Route Details: Gateway,IP Route Details: Interface,IP Route Details: Mask,IP Route Details: Metric
Casus-Belli.local,Windows Only,"2604:2000:1200:60de:dd68:f4b6:d5ee:e562
172.16.31.1
fe80::82e6:50ff:fe1d:1dca
172.16.152.1
10.0.1.8
2604:2000:1200:60de:82e6:50ff:fe1d:1dca","default
10.0.1.8/32
10.0.1/24
172.16.31/24
172.16.152/24
10.0.1.254
169.254
10.0.1.1/32","UGSc
UCS
..trimmed for brevity..

'''

'''STDERR from running this:

'''
