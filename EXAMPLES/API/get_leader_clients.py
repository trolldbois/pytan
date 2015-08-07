
"""
Get all clients that are Leader status
"""

import os
import sys
sys.dont_write_bytecode = True

# Determine our script name, script dir
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)

# determine the pytan lib dir and add it to the path
parent_dir = os.path.dirname(my_dir)
pytan_root_dir = os.path.dirname(parent_dir)
lib_dir = os.path.join(pytan_root_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)


# connection info for Tanium Server
USERNAME = "Tanium User"
PASSWORD = "T@n!um"
HOST = "172.16.31.128"
PORT = "443"

# Logging conrols
LOGLEVEL = 2
DEBUGFORMAT = False

import tempfile

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
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!

Type of response:  <class 'taniumpy.object_types.system_status_list.SystemStatusList'>

print of response:
SystemStatusList, len: 1

length of response (number of objects returned): 
1

print the first object returned in JSON format:
{
  "_type": "client_status", 
  "cache_row_id": 1, 
  "computer_id": "3741604154", 
  "full_version": "6.0.314.1195", 
  "host_name": "JTANIUM1.localdomain", 
  "ipaddress_client": "172.16.31.128", 
  "ipaddress_server": "172.16.31.128", 
  "last_registration": "2015-08-07T19:45:00", 
  "port_number": 17473, 
  "protocol_version": 314, 
  "public_key_valid": 1, 
  "receive_state": "Previous Only", 
  "send_state": "Backward Only", 
  "status": "Leader"
..trimmed for brevity..

'''
