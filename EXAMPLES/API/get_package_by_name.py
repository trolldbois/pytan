
"""
Get a package by name
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
kwargs["objtype"] = u'package'
kwargs["name"] = u'Distribute Patch Tools'

# call the handler with the get method, passing in kwargs for arguments
response = handler.get(**kwargs)

print ""
print "Type of response: ", type(response)

print ""
print "print of response:"
print response

print ""
print "length of response (number of objects returned): "
print len(response)

print ""
print "print the first object returned in JSON format:"
out = response.to_json(response[0])
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\n'.join(out)

print out



'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258

Type of response:  <class 'taniumpy.object_types.package_spec_list.PackageSpecList'>

print of response:
PackageSpecList, len: 1

length of response (number of objects returned): 
1

print the first object returned in JSON format:
{
  "_type": "package_spec", 
  "available_time": "2015-01-05T20:26:33", 
  "command": "cmd /c cscript //T:1800 copy-to-tanium-dir.vbs \"Tools\"", 
  "command_timeout": 1800, 
  "creation_time": "2015-01-05T20:22:32", 
  "deleted_flag": 0, 
  "display_name": "Distribute Patch Tools", 
  "expire_seconds": 2400, 
  "files": {
    "_type": "package_files", 
    "file": [
      {
        "_type": "file", 
        "bytes_downloaded": 3041, 
..trimmed for brevity..

'''
