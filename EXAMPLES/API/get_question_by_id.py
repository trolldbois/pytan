
"""
Get a question by id
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
kwargs["objtype"] = u'question'
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

Type of response:  <class 'taniumpy.object_types.question_list.QuestionList'>

print of response:
QuestionList, len: 1

length of response (number of objects returned): 
1

print the first object returned in JSON format:
{
  "_type": "question", 
  "action_tracking_flag": 0, 
  "context_group": {
    "_type": "group", 
    "id": 0
  }, 
  "expiration": "2014-12-08T19:30:12", 
  "expire_seconds": 0, 
  "force_computer_id_flag": 1, 
  "hidden_flag": 0, 
  "id": 1, 
  "management_rights_group": {
    "_type": "group", 
    "id": 0
  }, 
  "query_text": "Get Action Statuses matches \"Nil\" from all machines", 
  "saved_question": {
    "_type": "saved_question", 
    "id": 0
  }, 
  "selects": {
    "_type": "selects", 
    "select": [
      {
        "_type": "select", 
        "filter": {
          "_type": "filter", 
          "all_times_flag": 0, 
          "all_values_flag": 1, 
          "delimiter_index": 0, 
          "end_time": "2001-01-01T00:00:00", 
          "ignore_case_flag": 1, 
          "max_age_seconds": 0, 
          "not_flag": 0, 
          "operator": "RegexMatch", 
          "start_time": "2001-01-01T00:00:00", 
          "substring_flag": 0, 
          "substring_length": 0, 
          "substring_start": 0, 
          "utf8_flag": 0, 
          "value": "Nil", 
          "value_type": "String"
        }, 
        "sensor": {
          "_type": "sensor", 
          "category": "Reserved", 
          "description": "The recorded state of each action a client has taken recently in the form of id:status.\nExample: 1:Completed", 
          "exclude_from_parse_flag": 1, 
          "hash": 1792443391, 
          "hidden_flag": 0, 
          "id": 1, 
          "ignore_case_flag": 1, 
          "max_age_seconds": 3600, 
          "name": "Action Statuses", 
          "queries": {
            "_type": "queries", 
            "query": [
              {
                "_type": "query", 
                "platform": "Windows", 
                "script": "Reserved", 
                "script_type": "WMIQuery"
              }
            ]
          }, 
          "source_id": 0, 
          "string_count": 3524, 
          "value_type": "String"
        }
      }
    ]
  }, 
  "skip_lock_flag": 0, 
  "user": {
    "_type": "user", 
    "id": 1, 
    "name": "Jim Olsen"
  }
}

'''
