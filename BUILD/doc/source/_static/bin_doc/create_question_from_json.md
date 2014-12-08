Create Question From Json Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Create Question From Json Help](#user-content-create-question-from-json-help)
  * [Export question id 1 as JSON](#user-content-export-question-id-1-as-json)
  * [Change name or url_regex in the JSON](#user-content-change-name-or-url_regex-in-the-json)
  * [Create a new question from the modified JSON file](#user-content-create-a-new-question-from-the-modified-json-file)

---------------------------

# Create Question From Json Help

  * Create a question object from a json file

```bash
create_question_from_json.py -h
```

```
usage: create_question_from_json.py [-h] -u USERNAME -p PASSWORD --host HOST
                                    [--port PORT] [-l LOGLEVEL] -j JSON_FILE

Create a question object from a json file

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

Create Question from JSON Options:
  -j JSON_FILE, --json JSON_FILE
                        JSON file to use for creating the object (default: )
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


# Export question id 1 as JSON

  * Get the first question object
  * Save the results to a JSON file

```bash
get_question.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --id 1 --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json" json
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
Found items:  QuestionList, len: 1
Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json' written with 2468 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json exists, content:

```
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
...trimmed for brevity...
```



[TOC](#user-content-toc)


# Change name or url_regex in the JSON

  * Add CMDLINE TEST to name or url_regex in the JSON file

```bash
perl -p -i -e 's/^(      "(name|url_regex)": ".*)"/$1 CMDLINE TEST 8534"/gm' /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json && cat /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json
```

```
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
      "expiration": "2014-12-06T18:08:58", 
      "expire_seconds": 0, 
      "force_computer_id_flag": 1, 
      "hidden_flag": 0, 
      "id": 1, 
      "management_rights_group": {
        "_type": "group", 
        "id": 0
      }, 
      "query_text": "Get Action Statuses matches \"Nil\" from all machines", 
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
              "string_count": 3485, 
              "value_type": "String"
            }
          }
        ]
      }, 
      "skip_lock_flag": 0, 
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


# Create a new question from the modified JSON file

```bash
create_question_from_json.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 -j "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json"
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
Created item: Question, id: 2936, ID: 2936
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Mon Dec  8 12:32:41 2014 EST, Contact info: **Jim Olsen <jim.olsen@tanium.com>**