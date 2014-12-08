
"""
Get a saved action by name
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
kwargs["objtype"] = u'saved_action'
kwargs["name"] = u'Distribute Tanium Standard Utilities'

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

Type of response:  <class 'taniumpy.object_types.saved_action_list.SavedActionList'>

print of response:
SavedActionList, len: 1

length of response (number of objects returned): 
1

print the first object returned in JSON format:
{
  "_type": "saved_action", 
  "action_group_id": 0, 
  "comment": "Distributes the Hardware Tools used for hardware identification.", 
  "creation_time": "2014-12-06T18:02:04", 
  "distribute_seconds": 0, 
  "end_time": "Never", 
  "expire_seconds": 660, 
  "id": 14, 
  "issue_count": 0, 
  "issue_seconds": 86400, 
  "last_action": {
    "_type": "action", 
    "id": 4294967295, 
    "start_time": "Never"
  }, 
  "name": "Distribute Hardware Tools", 
  "package_spec": {
    "_type": "package_spec", 
    "id": 4294967295
  }, 
  "policy": {
    "_type": "policy", 
    "max_age": 86400, 
    "min_count": 0, 
    "row_filter_group_id": 208, 
    "saved_question_group_id": 0, 
    "saved_question_id": 13
  }, 
  "policy_flag": 1, 
  "status": 0, 
  "user": {
    "_type": "user", 
    "id": 1
  }
}

'''