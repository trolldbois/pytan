
"""
Get a system setting by name
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
kwargs["objtype"] = u'setting'
kwargs["name"] = u'control_address'

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

Type of response:  <class 'taniumpy.object_types.system_settings_list.SystemSettingsList'>

print of response:
SystemSettingsList, len: 1

length of response (number of objects returned): 
1

print the first object returned in JSON format:
{
  "_type": "system_setting", 
  "default_value": "512:17473:127.0.0.1", 
  "hidden_flag": 0, 
  "id": 57, 
  "name": "control_address", 
  "read_only_flag": 0, 
  "setting_type": "Server", 
  "value": "512:17473:127.0.0.1", 
  "value_type": "Text"
}

'''
