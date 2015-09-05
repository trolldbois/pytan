#!/usr/bin/env python
"""
Ask a saved question by referencing the name of a saved question in a string and use Server Side Export when performing a GetResultData
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
kwargs["sse"] = True
kwargs["qtype"] = u'saved'
kwargs["name"] = u'Installed Applications'

print "...CALLING: handler.ask with args: {}".format(kwargs)
response = handler.ask(**kwargs)

print "...OUTPUT: Type of response: ", type(response)

print "...OUTPUT: Pretty print of response:"
print pprint.pformat(response)

print "...OUTPUT: Equivalent Question if it were to be asked in the Tanium Console: "
print response['question_object'].query_text

if response['question_results']:
    # call the export_obj() method to convert response to CSV and store it in out
    export_kwargs = {}
    export_kwargs['obj'] = response['question_results']
    export_kwargs['export_format'] = 'csv'

    print "...CALLING: handler.export_obj() with args {}".format(export_kwargs)
    out = handler.export_obj(**export_kwargs)

    # trim the output if it is more than 15 lines long
    if len(out.splitlines()) > 15:
        out = out.splitlines()[0:15]
        out.append('..trimmed for brevity..')
        out = '\n'.join(out)

    print "...OUTPUT: CSV Results of response: "
    print out

'''STDOUT from running this:
...CALLING: pytan.handler() with args: {'username': 'Administrator', 'record_all_requests': True, 'loglevel': 1, 'debugformat': False, 'host': '10.0.1.240', 'password': 'Tanium2015!', 'port': '443'}
...OUTPUT: handler string: PyTan v2.1.0 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
...CALLING: handler.ask with args: {'sse': True, 'qtype': u'saved', 'name': u'Installed Applications'}
2015-09-05 05:48:47,019 INFO     pytan.pollers.SSEPoller: ID '1/494747304836.xml': Server Side Export Completed: 'Completed. 391 rows written.'
...OUTPUT: Type of response:  <type 'dict'>
...OUTPUT: Pretty print of response:
{'poller_object': None,
 'poller_success': None,
 'question_object': <taniumpy.object_types.question.Question object at 0x10d8fdb10>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x116522310>,
 'saved_question_object': <taniumpy.object_types.saved_question.SavedQuestion object at 0x112503e50>}
...OUTPUT: Equivalent Question if it were to be asked in the Tanium Console: 
Get Installed Applications from all machines
...CALLING: handler.export_obj() with args {'export_format': 'csv', 'obj': <taniumpy.object_types.result_set.ResultSet object at 0x116522310>}
...OUTPUT: CSV Results of response: 
Installed Applications,Installed Applications,Installed Applications,Installed Applications
Image Capture Extension,Image Capture Extension,Image Capture Extension,Image Capture Extension
Dictation,Dictation,Dictation,Dictation
Wish,Wish,Wish,Wish
Uninstall AnyConnect,Uninstall AnyConnect,Uninstall AnyConnect,Uninstall AnyConnect
Time Machine,Time Machine,Time Machine,Time Machine
7-Zip 9.20 (x64 edition),7-Zip 9.20 (x64 edition),7-Zip 9.20 (x64 edition),7-Zip 9.20 (x64 edition)
AppleGraphicsWarning,AppleGraphicsWarning,AppleGraphicsWarning,AppleGraphicsWarning
soagent,soagent,soagent,soagent
Feedback Assistant,Feedback Assistant,Feedback Assistant,Feedback Assistant
AinuIM,AinuIM,AinuIM,AinuIM
vpndownloader,vpndownloader,vpndownloader,vpndownloader
Pass Viewer,Pass Viewer,Pass Viewer,Pass Viewer
ARDAgent,ARDAgent,ARDAgent,ARDAgent
PressAndHold,PressAndHold,PressAndHold,PressAndHold
..trimmed for brevity..

'''

'''STDERR from running this:

'''
