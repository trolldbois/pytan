#!/usr/bin/env python
"""
Get a package by name
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
kwargs["objtype"] = u'package'
kwargs["name"] = u'Distribute Tanium Standard Utilities'

print "...CALLING: handler.get with args: {}".format(kwargs)
response = handler.get(**kwargs)

print "...OUTPUT: Type of response: ", type(response)

print "...OUTPUT: print of response:"
print response

# call the export_obj() method to convert response to JSON and store it in out
export_kwargs = {}
export_kwargs['obj'] = response
export_kwargs['export_format'] = 'json'

print "...CALLING: handler.export_obj() with args {}".format(export_kwargs)
out = handler.export_obj(**export_kwargs)

# trim the output if it is more than 15 lines long
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\n'.join(out)

print "...OUTPUT: print the objects returned in JSON format:"
print out

'''STDOUT from running this:
...CALLING: pytan.handler() with args: {'username': 'Administrator', 'record_all_requests': True, 'loglevel': 1, 'debugformat': False, 'host': '10.0.1.240', 'password': 'Tanium2015!', 'port': '443'}
...OUTPUT: handler string: PyTan v2.1.4 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
...CALLING: handler.get with args: {'objtype': u'package', 'name': u'Distribute Tanium Standard Utilities'}
...OUTPUT: Type of response:  <class 'taniumpy.object_types.package_spec_list.PackageSpecList'>
...OUTPUT: print of response:
PackageSpecList, len: 1
...CALLING: handler.export_obj() with args {'export_format': 'json', 'obj': <taniumpy.object_types.package_spec_list.PackageSpecList object at 0x108fa0550>}
...OUTPUT: print the objects returned in JSON format:
{
  "_type": "package_specs", 
  "package_spec": [
    {
      "_type": "package_spec", 
      "available_time": "2015-09-14T13:40:54", 
      "command": "cmd /c cscript install-standard-utils.vbs \"Tools\\StdUtils\"", 
      "command_timeout": 2700, 
      "creation_time": "2001-01-01T00:00:00", 
      "deleted_flag": 0, 
      "display_name": "Distribute Tanium Standard Utilities", 
      "expire_seconds": 3300, 
      "files": {
        "_type": "package_files", 
        "file": [
..trimmed for brevity..

'''

'''STDERR from running this:

'''
