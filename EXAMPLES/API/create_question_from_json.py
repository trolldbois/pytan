
"""
Export a question object to a JSON file, then create a new question object from the exported JSON file. Questions can not be deleted, so do not delete it. This will, in effect, 're-ask' a question.
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
attr_name = ""
attr_add = ""

# delete object before creating it?
delete = False

# setup the arguments for getting an object to export as json file
get_kwargs = {}
get_kwargs["objtype"] = u'question'
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
            del_kwargs['objtype'] = u'question'
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
create_kwargs = {'objtype': u'question', 'json_file': json_file}
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
2015-08-07 19:46:14,608 INFO     pytan.handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/QuestionList_2015_08_07-15_46_14-EDT.json' written with 2468 bytes
2015-08-07 19:46:14,640 INFO     pytan.handler: New Question, id: 1305 (ID: 1305) created successfully!

Type of response:  <class 'taniumpy.object_types.question_list.QuestionList'>

print of response:
QuestionList, len: 1

print the object returned in JSON format:
{
  "_type": "questions", 
  "question": [
    {
      "_type": "question", 
      "action_tracking_flag": 0, 
      "context_group": {
        "_type": "group", 
        "id": 0
      }, 
      "expiration": "2015-08-07T19:56:14", 
      "expire_seconds": 0, 
      "force_computer_id_flag": 1, 
      "hidden_flag": 0, 
      "id": 1305, 
      "management_rights_group": {
        "_type": "group", 
        "id": 0
      }, 
      "query_text": "Get Action Statuses matching \"Nil\" from all machines", 
      "saved_question": {
        "_type": "saved_question", 
        "id": 0
      }, 
      "selects": {
        "_type": "selects", 
        "select": [
          {
            "_type": "select", 
            "filter": {
              "_type": "filter", 
              "all_times_flag": 0, 
              "all_values_flag": 1, 
              "delimiter_index": 0, 
              "end_time": "2001-01-01T00:00:00", 
              "ignore_case_flag": 1, 
              "max_age_seconds": 0, 
              "not_flag": 0, 
              "operator": "RegexMatch", 
              "start_time": "2001-01-01T00:00:00", 
              "substring_flag": 0, 
              "substring_length": 0, 
              "substring_start": 0, 
              "utf8_flag": 0, 
              "value": "Nil", 
              "value_type": "String"
            }, 
            "sensor": {
              "_type": "sensor", 
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
              "string_count": 238, 
              "value_type": "String"
            }
          }
        ]
      }, 
      "skip_lock_flag": 0, 
      "user": {
        "_type": "user", 
        "id": 2, 
        "name": "Tanium User"
      }
    }
  ]
}

'''
