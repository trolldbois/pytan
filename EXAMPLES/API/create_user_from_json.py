
"""
Export a user object to a JSON file, adding ' API TEST' to the name of the user before exporting the JSON file and deleting any pre-existing user with the same (new) name, then create a new user object from the exported JSON file
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

# set the attribute name and value we want to add to the original object (if any)
attr_name = "name"
attr_add = " API TEST"

# delete object before creating it?
delete = True

# setup the arguments for getting an object to export as json file
get_kwargs = {}
get_kwargs["objtype"] = u'user'
get_kwargs["id"] = 1


# get objects to use as an export to JSON file
orig_objs = handler.get(**get_kwargs)

# if attr_name and attr_add exists, modify the orig_objs to add attr_add to the attribute
# attr_name
if attr_name:
    for x in orig_objs:
        new_attr = getattr(x, attr_name)
        new_attr += attr_add
        setattr(x, attr_name, new_attr)
        if delete:
            # delete the object in case it already exists
            del_kwargs = {}
            del_kwargs[attr_name] = new_attr
            del_kwargs['objtype'] = u'user'
            try:
                handler.delete(**del_kwargs)
            except Exception as e:
                print e

# export orig_objs to a json file
json_file, results = handler.export_to_report_file(
    obj=orig_objs,
    export_format='json',
    report_dir=tempfile.gettempdir(),
)

# create the object from the exported JSON file
create_kwargs = {'objtype': u'user', 'json_file': json_file}
response = handler.create_from_json(**create_kwargs)


print ""
print "Type of response: ", type(response)

print ""
print "print of response:"
print response

print ""
print "print the object returned in JSON format:"
print response.to_json(response)


'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
2014-12-08 16:28:44,799 INFO     handler: Deleted "User, name: 'Jim Olsen API TEST'"
2014-12-08 16:28:44,800 INFO     handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/UserList_2014_12_08-16_28_44-EST.json' written with 831 bytes
2014-12-08 16:28:44,816 INFO     handler: New User, name: 'Jim Olsen API TEST' (ID: 17) created successfully!

Type of response:  <class 'taniumpy.object_types.user_list.UserList'>

print of response:
UserList, len: 1

print the object returned in JSON format:
{
  "_type": "users", 
  "user": [
    {
      "_type": "user", 
      "deleted_flag": 0, 
      "group_id": 0, 
      "id": 17, 
      "last_login": "2001-01-01T00:00:00", 
      "name": "Jim Olsen API TEST", 
      "permissions": {
        "_type": "permissions", 
        "permission": "admin"
      }, 
      "roles": {
        "_type": "roles", 
        "role": [
          {
            "_type": "role", 
            "description": "Administrators can perform all functions in the system, including creating other users, viewing the System Status, changing Global Settings, and creating Computer Groups.", 
            "id": 1, 
            "name": "Administrator", 
            "permissions": {
              "_type": "permissions", 
              "permission": "admin"
            }
          }
        ]
      }
    }
  ]
}

'''
