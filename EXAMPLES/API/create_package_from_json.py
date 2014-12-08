
"""
Export a package object to a JSON file, adding ' API TEST' to the name of the package before exporting the JSON file and deleting any pre-existing package with the same (new) name, then create a new package object from the exported JSON file
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
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
2014-12-08 15:17:04,751 INFO     handler: Deleted 'PackageSpec, id: 92'
2014-12-08 15:17:04,751 INFO     handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/PackageSpecList_2014_12_08-15_17_04-EST.json' written with 2599 bytes
2014-12-08 15:17:04,775 INFO     handler: New PackageSpec, name: 'Custom Tagging - Add Tags API TEST' (ID: 101) created successfully!

Type of response:  <class 'taniumpy.object_types.package_spec_list.PackageSpecList'>

print of response:
PackageSpecList, len: 1

print the object returned in JSON format:
{
  "_type": "package_specs", 
  "package_spec": [
    {
      "_type": "package_spec", 
      "available_time": "1900-01-01T00:00:00", 
      "command": "cmd /c cscript //T:60 add-tags.vbs \"$1\"", 
      "command_timeout": 60, 
      "creation_time": "2014-12-08T20:17:04", 
      "deleted_flag": 0, 
      "display_name": "Custom Tagging - Add Tags", 
      "expire_seconds": 660, 
      "files": {
        "_type": "package_files", 
        "file": [
          {
            "_type": "file", 
            "bytes_downloaded": 1972, 
            "bytes_total": 1972, 
            "cache_status": "CACHED", 
            "download_seconds": 0, 
            "download_start_time": "2014-12-08T19:23:55", 
            "hash": "55aa6c54d82282ad2d41390e49f7b9939c582e14fa5cfca1b7b7fb9264261182", 
            "id": 71, 
            "last_download_progress_time": "2014-12-08T19:24:06", 
            "name": "add-tags.vbs", 
            "size": 1972, 
            "source": "https://content.tanium.com/files/initialcontent/bundles/2014-11-05_12-56-07-8513/custom_tagging_-_add_tags/add-tags.vbs", 
            "status": 200
          }
        ]
      }, 
      "hidden_flag": 0, 
      "id": 101, 
      "last_modified_by": "Tanium User", 
      "last_update": "2014-12-08T20:17:04", 
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
      "modification_time": "2014-12-08T20:17:04", 
      "name": "Custom Tagging - Add Tags API TEST", 
      "parameter_definition": "{\"parameters\":[{\"restrict\":null,\"validationExpressions\":[{\"helpString\":\"You must enter a value\",\"flags\":\"\",\"expression\":\"\\\\S\",\"parameterType\":\"com.tanium.models::ValidationExpression\",\"model\":\"com.tanium.models::ValidationExpression\"}],\"helpString\":\"Enter tags space-delimited.\",\"promptText\":\"e.g. PCI DMZ Decomm\",\"defaultValue\":\"\",\"value\":\"\",\"label\":\"Add tags (space-delimited)\",\"maxChars\":0,\"key\":\"$1\",\"parameterType\":\"com.tanium.components.parameters::TextInputParameter\",\"model\":\"com.tanium.components.parameters::TextInputParameter\"}],\"parameterType\":\"com.tanium.components.parameters::ParametersArray\",\"model\":\"com.tanium.components.parameters::ParametersArray\"}", 
      "source_id": 0, 
      "verify_group_id": 0
    }
  ]
}

'''
