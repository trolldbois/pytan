
"""
Get all packages
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

# call the handler with the get_all method, passing in kwargs for arguments
response = handler.get_all(**kwargs)

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
PackageSpecList, len: 92

length of response (number of objects returned): 
92

print the first object returned in JSON format:
{
  "_type": "package_spec", 
  "available_time": "2014-12-08T19:21:15", 
  "cache_row_id": 0, 
  "command": "cmd /c cscript //T:900 java-installer.vbs /KillAppsUsingJava:Yes /RebootIfNeeded:Yes /MaxWaitTimeInSeconds:300", 
  "command_timeout": 900, 
  "creation_time": "2014-12-08T19:20:46", 
  "deleted_flag": 0, 
  "display_name": "Update Java 64-bit - Kill / Reboot", 
  "expire_seconds": 1500, 
  "files": {
    "_type": "package_files", 
    "file": [
      {
        "_type": "file", 
..trimmed for brevity..

'''
