
"""
Create a whitelisted url
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
delete_kwargs["objtype"] = 'whitelisted_url'
delete_kwargs["url_regex"] = 'regex:http://test.com/.*API_Test.*URL'


# setup the arguments for the handler method
kwargs = {}
kwargs["url"] = u'http://test.com/.*API_Test.*URL'
kwargs["regex"] = True
kwargs["properties"] = [[u'property1', u'value1']]
kwargs["download_seconds"] = 3600

# delete the object in case it already exists
try:
    handler.delete(**delete_kwargs)
except Exception as e:
    print e

# call the handler with the create_whitelisted_url method, passing in kwargs for arguments
response = handler.create_whitelisted_url(**kwargs)


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
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
No results found searching for whitelisted_url with {'url_regex': 'regex:http://test.com/.*API_Test.*URL'}!!
2015-08-06 14:56:10,045 INFO     pytan.handler: New Whitelisted URL 'regex:http://test.com/.*API_Test.*URL' created with ID 3069

Type of response:  <class 'taniumpy.object_types.white_listed_url.WhiteListedUrl'>

print of response:
WhiteListedUrl, id: 3069

print the object returned in JSON format:
{
  "_type": "white_listed_url", 
  "download_seconds": 3600, 
  "id": 3069, 
  "metadata": {
    "_type": "metadata", 
    "item": [
      {
        "_type": "item", 
        "admin_flag": 0, 
        "name": "TConsole.WhitelistedURL.property1", 
        "value": "value1"
      }
    ]
  }, 
  "url_regex": "regex:http://test.com/.*API_Test.*URL"
}
2015-08-06 14:56:10,279 INFO     pytan.handler: Deleted 'WhiteListedUrl, id: 3069'

'''
