
"""
Export a package object to a JSON file, adding ' API TEST' to the name of the package before exporting the JSON file and deleting any pre-existing package with the same (new) name, then create a new package object from the exported JSON file
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

# set the attribute name and value we want to add to the original object (if any)
attr_name = "name"
attr_add = " API TEST"

# delete object before creating it?
delete = True

# setup the arguments for getting an object to export as json file
get_kwargs = {}
get_kwargs["objtype"] = u'package'
get_kwargs["id"] = 31


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
            del_kwargs['objtype'] = u'package'
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
create_kwargs = {'objtype': u'package', 'json_file': json_file}
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
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
2015-08-07 19:46:14,304 INFO     pytan.handler: Deleted 'PackageSpec, id: 76'
2015-08-07 19:46:14,305 INFO     pytan.handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/PackageSpecList_2015_08_07-15_46_14-EDT.json' written with 2347 bytes
2015-08-07 19:46:14,337 INFO     pytan.handler: New PackageSpec, name: 'Disable Java Auto Update API TEST', id: 83 (ID: 83) created successfully!

Type of response:  <class 'taniumpy.object_types.package_spec_list.PackageSpecList'>

print of response:
PackageSpecList, len: 1

print the object returned in JSON format:
{
  "_type": "package_specs", 
  "package_spec": [
    {
      "_type": "package_spec", 
      "available_time": "2015-08-07T13:22:40", 
      "command": "cmd /c cscript //T:60 disable-java-auto-update.vbs", 
      "command_timeout": 60, 
      "creation_time": "2001-01-01T00:00:00", 
      "deleted_flag": 0, 
      "display_name": "Disable Java Auto Update", 
      "expire_seconds": 660, 
      "files": {
        "_type": "package_files", 
        "file": [
          {
            "_type": "file", 
            "bytes_downloaded": 0, 
            "bytes_total": 0, 
            "cache_status": "CACHED", 
            "download_seconds": 0, 
            "file_status": {
              "_type": "file_status", 
              "status": [
                {
                  "_type": "status", 
                  "bytes_downloaded": 0, 
                  "bytes_total": 0, 
                  "cache_status": "Processing", 
                  "server_id": 1, 
                  "server_name": "JTANIUM1.localdomain:17472", 
                  "status": 0
                }
              ]
            }, 
            "hash": "9e36208ce643c767ad76ef2ad6a69141fbb5a59a607b8eb8065db09e3a153c0d", 
            "id": 43, 
            "name": "disable-java-auto-update.vbs", 
            "size": 11377, 
            "source": "https://content.tanium.com/files/published/InitialContent/2015-06-04_18-59-45_6.5.1.0011-ga516c3c/disable_java_auto_update/disable-java-auto-update.vbs", 
            "status": 0
          }
        ]
      }, 
      "hidden_flag": 0, 
      "id": 83, 
      "last_update": "2001-01-01T00:00:00", 
      "metadata": {
        "_type": "metadata", 
        "item": [
          {
            "_type": "item", 
            "admin_flag": 0, 
            "name": "defined", 
            "value": "Tanium"
          }, 
          {
            "_type": "item", 
            "admin_flag": 0, 
            "name": "category", 
            "value": "Tanium"
          }
        ]
      }, 
      "modification_time": "2001-01-01T00:00:00", 
      "name": "Disable Java Auto Update API TEST", 
      "skip_lock_flag": 0, 
      "source_id": 0, 
      "verify_expire_seconds": 600, 
      "verify_group": {
        "_type": "group", 
        "id": 0
      }, 
      "verify_group_id": 0
    }
  ]
}

'''
