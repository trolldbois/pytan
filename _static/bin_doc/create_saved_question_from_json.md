Create Saved Question From Json Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Create Saved Question From Json Help](#user-content-create-saved-question-from-json-help)
  * [Export saved_question id 1 as JSON](#user-content-export-saved_question-id-1-as-json)
  * [Change name or url_regex in the JSON](#user-content-change-name-or-url_regex-in-the-json)
  * [Create a new saved_question from the modified JSON file](#user-content-create-a-new-saved_question-from-the-modified-json-file)

---------------------------

# Create Saved Question From Json Help

  * Create a saved_question object from a json file

```bash
create_saved_question_from_json.py -h
```

```
usage: create_saved_question_from_json.py [-h] -u USERNAME -p PASSWORD --host
                                          HOST [--port PORT] [-l LOGLEVEL] -j
                                          JSON_FILE

Create a saved_question object from a json file

optional arguments:
  -h, --help            show this help message and exit

Handler Authentication:
  -u USERNAME, --username USERNAME
                        Name of user (default: None)
  -p PASSWORD, --password PASSWORD
                        Password of user (default: None)
  --host HOST           Hostname/ip of SOAP Server (default: None)
  --port PORT           Port to use when connecting to SOAP Server (default:
                        444)

Handler Options:
  -l LOGLEVEL, --loglevel LOGLEVEL
                        Logging level to use, increase for more verbosity
                        (default: 0)

Create Saved question from JSON Options:
  -j JSON_FILE, --json JSON_FILE
                        JSON file to use for creating the object (default: )
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


# Export saved_question id 1 as JSON

  * Get the first saved_question object
  * Save the results to a JSON file

```bash
get_saved_question.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --id 1 --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json" json
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
Found items:  SavedQuestionList, len: 1
Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json' written with 4592 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json exists, content:

```
{
  "_type": "saved_questions", 
  "saved_question": [
    {
      "_type": "saved_question", 
      "action_tracking_flag": 0, 
      "archive_enabled_flag": 0, 
      "archive_owner": {
        "_type": "user", 
        "id": 1, 
...trimmed for brevity...
```



[TOC](#user-content-toc)


# Change name or url_regex in the JSON

  * Add CMDLINE TEST to name or url_regex in the JSON file

```bash
perl -p -i -e 's/^(      "(name|url_regex)": ".*)"/$1 CMDLINE TEST 6321"/gm' /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json && cat /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json
```

```
{
  "_type": "saved_questions", 
  "saved_question": [
    {
      "_type": "saved_question", 
      "action_tracking_flag": 0, 
      "archive_enabled_flag": 0, 
      "archive_owner": {
        "_type": "user", 
        "id": 1, 
        "name": "Jim Olsen"
      }, 
      "expire_seconds": 600, 
      "hidden_flag": 0, 
      "id": 1, 
      "issue_seconds": 120, 
      "issue_seconds_never_flag": 0, 
      "keep_seconds": 3600, 
      "mod_time": "2014-12-06T18:01:04", 
      "mod_user": {
        "_type": "user", 
        "name": "Jim Olsen"
      }, 
      "most_recent_question_id": 2931, 
      "name": "Run Unmanaged Asset Scan on All Machines CMDLINE TEST 6321", 
      "packages": {
        "_type": "package_specs", 
        "package_spec": []
      }, 
      "public_flag": 1, 
      "query_text": "Get Is Windows from all machines", 
      "question": {
        "_type": "question", 
        "action_tracking_flag": 0, 
        "expiration": "2014-12-08T17:38:57", 
        "expire_seconds": 0, 
        "force_computer_id_flag": 0, 
        "hidden_flag": 0, 
        "id": 2931, 
        "management_rights_group": {
          "_type": "group", 
          "id": 0
        }, 
        "query_text": "Get Is Windows from all machines", 
        "saved_question": {
          "_type": "saved_question", 
          "id": 1
        }, 
        "selects": {
          "_type": "selects", 
          "select": [
            {
              "_type": "select", 
              "filter": {
                "_type": "filter", 
                "all_times_flag": 0, 
                "all_values_flag": 0, 
                "delimiter_index": 0, 
                "end_time": "2001-01-01T00:00:00", 
                "ignore_case_flag": 1, 
                "max_age_seconds": 0, 
                "not_flag": 0, 
                "operator": "Less", 
                "start_time": "2001-01-01T00:00:00", 
                "substring_flag": 0, 
                "substring_length": 0, 
                "substring_start": 0, 
                "utf8_flag": 0, 
                "value_type": "String"
              }, 
              "sensor": {
                "_type": "sensor", 
                "category": "Operating System", 
                "creation_time": "2014-12-06T18:00:21", 
                "delimiter": ",", 
                "description": "Returns whether the machine runs Windows.  True if so, False if not.\nExample: True", 
                "exclude_from_parse_flag": 0, 
                "hash": 2721439124, 
                "hidden_flag": 0, 
                "id": 35, 
                "ignore_case_flag": 1, 
                "last_modified_by": "Jim Olsen", 
                "max_age_seconds": 86400, 
                "metadata": {
                  "_type": "metadata", 
                  "item": [
                    {
                      "_type": "item", 
                      "admin_flag": 0, 
                      "name": "defined", 
                      "value": "Tanium"
                    }
                  ]
                }, 
                "modification_time": "2014-12-06T18:00:21", 
                "name": "Is Windows", 
                "queries": {
                  "_type": "queries", 
                  "query": [
                    {
                      "_type": "query", 
                      "platform": "Windows", 
                      "script": "&#039;========================================\n&#039; Is Windows\n&#039;========================================\n\nWscript.echo &quot;True&quot;", 
                      "script_type": "VBScript"
                    }, 
                    {
                      "_type": "query", 
                      "platform": "Linux", 
                      "script": "#!/bin/bash\necho False\n", 
                      "script_type": "UnixShell"
                    }, 
                    {
                      "_type": "query", 
                      "platform": "Mac", 
                      "script": "#!/bin/bash\necho False\n", 
                      "script_type": "UnixShell"
                    }
                  ]
                }, 
                "source_id": 0, 
                "string_count": 3, 
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
      }, 
      "row_count_flag": 1, 
      "sort_column": 0, 
      "user": {
        "_type": "user", 
        "id": 1, 
        "name": "Jim Olsen"
      }
    }
  ]
}
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json exists



[TOC](#user-content-toc)


# Create a new saved_question from the modified JSON file

```bash
create_saved_question_from_json.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 -j "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json"
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
Created item: SavedQuestion, name: 'Run Unmanaged Asset Scan on All Machines CMDLINE TEST 6321', ID: 213
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Mon Dec  8 12:32:42 2014 EST, Contact info: **Jim Olsen <jim.olsen@tanium.com>**