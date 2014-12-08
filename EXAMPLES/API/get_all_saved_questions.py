
"""
Get all saved questions
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
kwargs["objtype"] = u'saved_question'

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

Type of response:  <class 'taniumpy.object_types.saved_question_list.SavedQuestionList'>

print of response:
SavedQuestionList, len: 173

length of response (number of objects returned): 
173

print the first object returned in JSON format:
{
  "_type": "saved_question", 
  "action_tracking_flag": 0, 
  "archive_enabled_flag": 0, 
  "archive_owner": {
    "_type": "user", 
    "id": 1, 
    "name": "Jim Olsen"
  }, 
  "cache_row_id": 0, 
  "expire_seconds": 600, 
  "hidden_flag": 0, 
  "id": 1, 
  "issue_seconds": 120, 
  "issue_seconds_never_flag": 0, 
  "keep_seconds": 3600, 
  "mod_time": "2014-12-06T18:01:04", 
  "mod_user": {
    "_type": "user", 
    "name": "Jim Olsen"
  }, 
  "most_recent_question_id": 987, 
  "name": "Run Unmanaged Asset Scan on All Machines", 
  "packages": {
    "_type": "package_specs", 
    "package_spec": []
  }, 
  "public_flag": 1, 
  "query_text": "Get Is Windows from all machines", 
  "question": {
    "_type": "question", 
    "id": 987
  }, 
  "row_count_flag": 1, 
  "sort_column": 0, 
  "user": {
    "_type": "user", 
    "id": 1, 
    "name": "Jim Olsen"
  }
}

'''
