Create Action From Json Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Create Action From Json Help](#user-content-create-action-from-json-help)
  * [Export action id 1 as JSON](#user-content-export-action-id-1-as-json)
  * [Change name or url_regex in the JSON](#user-content-change-name-or-url_regex-in-the-json)
  * [Create a new action from the modified JSON file](#user-content-create-a-new-action-from-the-modified-json-file)

---------------------------

# Create Action From Json Help

  * Create a action object from a json file

```bash
create_action_from_json.py -h
```

```
usage: create_action_from_json.py [-h] [-u USERNAME] [-p PASSWORD]
                                  [--host HOST] [--port PORT] [-l LOGLEVEL] -j
                                  JSON_FILE

Create a action object from a json file

optional arguments:
  -h, --help            show this help message and exit

Handler Authentication:
  -u USERNAME, --username USERNAME
                        Name of user (default: None)
  -p PASSWORD, --password PASSWORD
                        Password of user (default: None)
  --host HOST           Hostname/ip of SOAP Server (default: None)
  --port PORT           Port to use when connecting to SOAP Server (default:
                        443)

Handler Options:
  -l LOGLEVEL, --loglevel LOGLEVEL
                        Logging level to use, increase for more verbosity
                        (default: 0)

Create Action from JSON Options:
  -j JSON_FILE, --json JSON_FILE
                        JSON file to use for creating the object (default: )
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


# Export action id 1 as JSON

  * Get the first action object
  * Save the results to a JSON file

```bash
get_action.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --id 1 --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json" json
```

```
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
Found items:  ActionList, len: 1
Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json' written with 1294 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json exists, content:

```
{
  "_type": "actions", 
  "action": [
    {
      "_type": "action", 
      "action_group": {
        "_type": "group", 
        "id": 0, 
        "name": "Default"
      }, 
...trimmed for brevity...
```



[TOC](#user-content-toc)


# Change name or url_regex in the JSON

  * Add CMDLINE TEST to name or url_regex in the JSON file

```bash
perl -p -i -e 's/^(      "(name|url_regex)": ".*)"/$1 CMDLINE TEST 6556"/gm' /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json && cat /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json
```

```
{
  "_type": "actions", 
  "action": [
    {
      "_type": "action", 
      "action_group": {
        "_type": "group", 
        "id": 0, 
        "name": "Default"
      }, 
      "approver": {
        "_type": "user", 
        "id": 1, 
        "name": "Jim Olsen"
      }, 
      "comment": "Distribute Tanium Standard Utilities", 
      "creation_time": "2015-08-07T13:22:26", 
      "distribute_seconds": 3200, 
      "expire_seconds": 3300, 
      "history_saved_question": {
        "_type": "saved_question", 
        "id": 102
      }, 
      "id": 1, 
      "name": "Distribute Tanium Standard Utilities CMDLINE TEST 6556", 
      "package_spec": {
        "_type": "package_spec", 
        "command": "cmd /c cscript install-standard-utils.vbs \"Tools\\StdUtils\"", 
        "id": 20, 
        "name": "Distribute Tanium Standard Utilities"
      }, 
      "saved_action": {
        "_type": "saved_action", 
        "id": 1
      }, 
      "skip_lock_flag": 0, 
      "status": "Pending", 
      "stopped_flag": 0, 
      "target_group": {
        "_type": "group", 
        "id": 37, 
        "name": "Default"
      }, 
      "user": {
        "_type": "user", 
        "group_id": 0, 
        "id": 1, 
        "last_login": "2015-08-07T13:21:59", 
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


# Create a new action from the modified JSON file

```bash
create_action_from_json.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 -j "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json"
```

```
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
Created item: Action, name: 'Distribute Tanium Standard Utilities CMDLINE TEST 6556', id: 53, ID: 53
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Fri Aug  7 15:27:33 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**