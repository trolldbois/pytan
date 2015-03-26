
"""
Create a group called All Windows Computers API Test
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
PORT = "444"

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

# setup the arguments for the delete method (to remove the package in case it exists)
delete_kwargs = {}
delete_kwargs["objtype"] = 'group'
delete_kwargs["name"] = 'All Windows Computers API Test'


# setup the arguments for the handler method
kwargs = {}
kwargs["groupname"] = u'All Windows Computers API Test'
kwargs["filters"] = [u'Operating System, that contains:Windows']
kwargs["filter_options"] = [u'and']

# delete the object in case it already exists
try:
    handler.delete(**delete_kwargs)
except Exception as e:
    print e

# call the handler with the create_group method, passing in kwargs for arguments
response = handler.create_group(**kwargs)


print ""
print "Type of response: ", type(response)

print ""
print "print of response:"
print response

print ""
print "print the object returned in JSON format:"
print response.to_json(response)

# delete the object, we are done with it now
try:
    handler.delete(**delete_kwargs)
except Exception as e:
    print e



'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
No results found searching for Group, name: 'All Windows Computers API Test'!!
2015-03-26 11:49:19,021 INFO     handler: New group 'All Windows Computers API Test' created with ID 19223, filter text: ' Operating System contains "Windows"'

Type of response:  <class 'taniumpy.object_types.group.Group'>

print of response:
Group, name: 'All Windows Computers API Test'

print the object returned in JSON format:
{
  "_type": "group", 
  "and_flag": 1, 
  "deleted_flag": 0, 
  "filters": {
    "_type": "filters", 
    "filter": [
      {
        "_type": "filter", 
        "all_times_flag": 0, 
        "all_values_flag": 0, 
        "delimiter_index": 0, 
        "ignore_case_flag": 1, 
        "max_age_seconds": 0, 
        "not_flag": 0, 
        "operator": "RegexMatch", 
        "sensor": {
          "_type": "sensor", 
          "hash": 45421433
        }, 
        "substring_flag": 0, 
        "substring_length": 0, 
        "substring_start": 0, 
        "utf8_flag": 0, 
        "value": ".*Windows.*", 
        "value_type": "String"
      }
    ]
  }, 
  "id": 19223, 
  "name": "All Windows Computers API Test", 
  "not_flag": 0, 
  "sub_groups": {
    "_type": "groups", 
    "group": []
  }, 
  "text": " Operating System contains \"Windows\"", 
  "type": 0
}
2015-03-26 11:49:19,044 INFO     handler: Deleted 'Group, id: 19223'

'''
