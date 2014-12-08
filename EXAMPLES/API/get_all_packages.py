
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
print response.to_json(response[0])


'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258

Type of response:  <class 'taniumpy.object_types.package_spec_list.PackageSpecList'>

print of response:
PackageSpecList, len: 89

length of response (number of objects returned): 
89

print the first object returned in JSON format:
{
  "_type": "package_spec", 
  "available_time": "2014-12-06T18:01:03", 
  "cache_row_id": 0, 
  "command": "cmd /c cscript //T:900 java-installer.vbs /KillAppsUsingJava:Yes /RebootIfNeeded:Yes /MaxWaitTimeInSeconds:300", 
  "command_timeout": 900, 
  "creation_time": "2014-12-06T18:00:27", 
  "deleted_flag": 0, 
  "display_name": "Update Java 64-bit - Kill / Reboot", 
  "expire_seconds": 1500, 
  "files": {
    "_type": "package_files", 
    "file": [
      {
        "_type": "file", 
        "bytes_downloaded": 17509, 
        "bytes_total": 17509, 
        "cache_status": "CACHED", 
        "download_seconds": 0, 
        "download_start_time": "2014-12-06T18:00:31", 
        "hash": "30bf532c4c1c5bb9599487712f88ff42190ccd2678192f7e61b160e6592cfbfe", 
        "id": 1, 
        "last_download_progress_time": "2014-12-06T18:00:53", 
        "name": "java-installer.vbs", 
        "size": 17509, 
        "source": "https://content.tanium.com/files/initialcontent/bundles/2014-11-05_12-56-07-8513/update_java_64-bit_-_kill_-_reboot/java-installer.vbs", 
        "status": 200
      }
    ]
  }, 
  "hidden_flag": 0, 
  "id": 1, 
  "last_modified_by": "Jim Olsen", 
  "last_update": "2014-12-06T18:00:27", 
  "metadata": {
    "_type": "metadata", 
    "item": [
      {
        "_type": "item", 
        "admin_flag": 0, 
        "name": "defined", 
        "value": "Tanium"
      }, 
      {
        "_type": "item", 
        "admin_flag": 0, 
        "name": "category", 
        "value": "Tanium"
      }
    ]
  }, 
  "modification_time": "2014-12-06T18:00:27", 
  "name": "Update Java 64-bit - Kill / Reboot", 
  "source_id": 0, 
  "verify_group_id": 0
}

'''
