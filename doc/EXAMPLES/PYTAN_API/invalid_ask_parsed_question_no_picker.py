#!/usr/bin/env python
"""
Ask a parsed question without supplying a picker
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
kwargs["question_text"] = u'Computer Name'
kwargs["qtype"] = u'parsed'

print "...CALLING: handler.ask() with args: {}".format(kwargs)
try:
    handler.ask(**kwargs)
except Exception as e:
    print "...EXCEPTION: {}".format(e)
    # this should throw an exception of type: pytan.exceptions.PickerError
    # uncomment to see full exception
    # traceback.print_exc(file=sys.stdout)
'''STDOUT from running this:
...CALLING: pytan.handler() with args: {'username': 'Administrator', 'record_all_requests': True, 'loglevel': 1, 'debugformat': False, 'host': '10.0.1.240', 'password': 'Tanium2015!', 'port': '443'}
...OUTPUT: handler string: PyTan v2.1.4 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
...CALLING: handler.ask() with args: {'question_text': u'Computer Name', 'qtype': u'parsed'}
2015-09-14 20:16:26,042 CRITICAL pytan.handler: You must supply an index as picker=$index to choose one of the parse responses -- re-run ask_parsed with picker set to one of these indexes!!
2015-09-14 20:16:26,043 CRITICAL pytan.handler: Index 1, Score: 6156, Query: 'Get Computer Name from all machines'
2015-09-14 20:16:26,043 CRITICAL pytan.handler: Index 2, Score: 1088, Query: 'Get Computer ID from all machines'
2015-09-14 20:16:26,043 CRITICAL pytan.handler: Index 3, Score: 769, Query: 'Get BIOS Name from all machines'
2015-09-14 20:16:26,043 CRITICAL pytan.handler: Index 4, Score: 544, Query: 'Get Domain Name from all machines'
2015-09-14 20:16:26,043 CRITICAL pytan.handler: Index 5, Score: 384, Query: 'Get AD Computer Groups from all machines'
2015-09-14 20:16:26,043 CRITICAL pytan.handler: Index 6, Score: 228, Query: 'Get Motherboard Name from all machines'
2015-09-14 20:16:26,043 CRITICAL pytan.handler: Index 7, Score: 192, Query: 'Get Computer Serial Number from all machines'
2015-09-14 20:16:26,043 CRITICAL pytan.handler: Index 8, Score: 192, Query: 'Get Primary Owner Name from all machines'
2015-09-14 20:16:26,043 CRITICAL pytan.handler: Index 9, Score: 192, Query: 'Get Tanium Server Name from all machines'
2015-09-14 20:16:26,043 CRITICAL pytan.handler: Index 10, Score: 136, Query: 'Get Network Adapter Name from all machines'
2015-09-14 20:16:26,043 CRITICAL pytan.handler: Index 11, Score: 114, Query: 'Get AD Distinguished Name from all machines'
...EXCEPTION: You must supply an index as picker=$index to choose one of the parse responses -- re-run ask_parsed with picker set to one of these indexes!!

'''

'''STDERR from running this:

'''
