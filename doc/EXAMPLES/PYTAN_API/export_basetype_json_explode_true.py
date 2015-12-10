#!/usr/bin/env python
"""
Export a BaseType from getting objects as JSON with true for explode_json_string_values
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
kwargs["export_format"] = u'json'
kwargs["explode_json_string_values"] = True

# setup the arguments for handler.get()
get_kwargs = {
    'name': [
        "Computer Name", "IP Route Details", "IP Address",
        'Folder Contents',
    ],
    'objtype': 'sensor',
}

# get the objects that will provide the basetype that we want to export
print "...CALLING: handler.get() with args: {}".format(get_kwargs)
response = handler.get(**get_kwargs)

# store the basetype object as the obj we want to export
kwargs['obj'] = response

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
...CALLING: handler.get() with args: {'objtype': 'sensor', 'name': ['Computer Name', 'IP Route Details', 'IP Address', 'Folder Contents']}
...CALLING: handler.export_obj() with args {'export_format': u'json', 'explode_json_string_values': True, 'obj': <taniumpy.object_types.sensor_list.SensorList object at 0x106a9c2d0>}
...OUTPUT: print the export_str returned from export_obj():
{
  "_type": "sensors", 
  "sensor": [
    {
      "_type": "sensor", 
      "category": "Reserved", 
      "description": "The assigned name of the client machine.\nExample: workstation-1.company.com", 
      "exclude_from_parse_flag": 0, 
      "hash": 3409330187, 
      "hidden_flag": 0, 
      "id": 3, 
      "ignore_case_flag": 1, 
      "max_age_seconds": 86400, 
      "name": "Computer Name", 
      "queries": {
..trimmed for brevity..

'''

'''STDERR from running this:

'''
