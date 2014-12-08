
"""
Export a BaseType from getting objects as JSON with true for explode_json_string_values
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

# setup the export_obj kwargs for later
export_kwargs = {}
export_kwargs["export_format"] = u'json'
export_kwargs["explode_json_string_values"] = True

# get the objects that will provide the basetype that we want to use
get_kwargs = {
    'name': [
        "Computer Name", "IP Route Details", "IP Address",
        'Folder Name Search with RegEx Match',
    ],
    'objtype': 'sensor',
}
response = handler.get(**get_kwargs)

# export the object to a string
# (we could just as easily export to a file using export_to_report_file)
export_kwargs['obj'] = response
export_str = handler.export_obj(**export_kwargs)


print ""
print "print the export_str returned from export_obj():"

out = export_str
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\n'.join(out)

print out


'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258

print the export_str returned from export_obj():
{
  "_type": "sensors", 
  "sensor": [
    {
      "_type": "sensor", 
      "category": "Reserved", 
      "description": "The assigned name of the client machine.\nExample: workstation-1.company.com", 
      "exclude_from_parse_flag": 0, 
      "hash": 3409330187, 
      "hidden_flag": 0, 
      "id": 3, 
      "ignore_case_flag": 1, 
      "max_age_seconds": 86400, 
      "name": "Computer Name", 
      "queries": {
..trimmed for brevity..

'''
