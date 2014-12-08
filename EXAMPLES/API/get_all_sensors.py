
"""
Get all sensors
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
kwargs["objtype"] = u'sensor'

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

Type of response:  <class 'taniumpy.object_types.sensor_list.SensorList'>

print of response:
SensorList, len: 477

length of response (number of objects returned): 
477

print the first object returned in JSON format:
{
  "_type": "sensor", 
  "cache_row_id": 0, 
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

'''
