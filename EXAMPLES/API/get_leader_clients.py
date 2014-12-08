
"""
Get all clients that are Leader status
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
kwargs["objtype"] = u'client'
kwargs["status"] = u'Leader'

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

Type of response:  <class 'taniumpy.object_types.system_status_list.SystemStatusList'>

print of response:
SystemStatusList, len: 1

length of response (number of objects returned): 
1

print the first object returned in JSON format:
{
  "_type": "client_status", 
  "cache_row_id": 2, 
  "computer_id": "3508795802", 
  "full_version": "6.0.314.1190", 
  "host_name": "WIN-A12SC6N6T7Q", 
  "ipaddress_client": "172.16.31.145", 
  "ipaddress_server": "172.16.31.145", 
  "last_registration": "2014-12-08T21:26:21", 
  "port_number": 17472, 
  "protocol_version": 314, 
  "receive_state": "Previous Only", 
  "send_state": "Backward Only", 
  "status": "Leader"
}

'''
