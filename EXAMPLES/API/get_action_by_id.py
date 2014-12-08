
"""
Get an action by id
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
kwargs["objtype"] = u'action'
kwargs["id"] = 1

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
print response.to_json(response[0])


'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258

Type of response:  <class 'taniumpy.object_types.action_list.ActionList'>

print of response:
ActionList, len: 1

length of response (number of objects returned): 
1

print the first object returned in JSON format:
{
  "_type": "action", 
  "action_group": {
    "_type": "group", 
    "id": 0, 
    "name": "Default"
  }, 
  "comment": "Scans for unmanaged assets on the network.", 
  "creation_time": "2014-12-08T19:22:33", 
  "distribute_seconds": 600, 
  "expire_seconds": 1800, 
  "history_saved_question": {
    "_type": "saved_question", 
    "id": 173
  }, 
  "id": 1, 
  "name": "Unmanaged Asset Tracking - Run Scan", 
  "package_spec": {
    "_type": "package_spec", 
    "command": "cmd /c start /B cscript //T:3600 ..\\..\\Tools\\run-ua-scan.vbs /RANDOM_WAIT_TIME_IN_SECONDS:240", 
    "id": 6, 
    "name": "Run Unmanaged Asset Scanner"
  }, 
  "saved_action": {
    "_type": "saved_action", 
    "id": 1
  }, 
  "skip_lock_flag": 0, 
  "status": "Pending", 
  "stopped_flag": 0, 
  "target_group": {
    "_type": "group", 
    "id": 65, 
    "name": "Default"
  }, 
  "user": {
    "_type": "user", 
    "group_id": 0, 
    "id": 1, 
    "last_login": "2014-12-08T19:28:09", 
    "name": "Jim Olsen"
  }
}

'''
