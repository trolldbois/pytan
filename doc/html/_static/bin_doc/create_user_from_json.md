Create User From Json Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Create User From Json Help](#user-content-create-user-from-json-help)
  * [Export user id 1 as JSON](#user-content-export-user-id-1-as-json)
  * [Change name or url_regex in the JSON](#user-content-change-name-or-url_regex-in-the-json)
  * [Create a new user from the modified JSON file](#user-content-create-a-new-user-from-the-modified-json-file)

---------------------------

# Create User From Json Help

  * Create a user object from a json file

```bash
create_user_from_json.py -h
```

```
usage: create_user_from_json.py [-h] [-u USERNAME] [-p PASSWORD] [--host HOST]
                                [--port PORT] [-l LOGLEVEL] -j JSON_FILE

Create a user object from a json file

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

Create User from JSON Options:
  -j JSON_FILE, --json JSON_FILE
                        JSON file to use for creating the object (default: )
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


# Export user id 1 as JSON

  * Get the first user object
  * Save the results to a JSON file

```bash
get_user.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --id 1 --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json" json
```

```
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
Found items:  UserList, len: 1
Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json' written with 1601 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json exists, content:

```
{
  "_type": "users", 
  "user": [
    {
      "_type": "user", 
      "deleted_flag": 0, 
      "group_id": 0, 
      "id": 1, 
      "last_login": "2015-08-07T13:21:59", 
      "local_admin_flag": -1, 
...trimmed for brevity...
```



[TOC](#user-content-toc)


# Change name or url_regex in the JSON

  * Add CMDLINE TEST to name or url_regex in the JSON file

```bash
perl -p -i -e 's/^(      "(name|url_regex)": ".*)"/$1 CMDLINE TEST 8052"/gm' /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json && cat /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json
```

```
{
  "_type": "users", 
  "user": [
    {
      "_type": "user", 
      "deleted_flag": 0, 
      "group_id": 0, 
      "id": 1, 
      "last_login": "2015-08-07T13:21:59", 
      "local_admin_flag": -1, 
      "name": "Jim Olsen CMDLINE TEST 8052", 
      "permissions": {
        "_type": "permissions", 
        "permission": [
          "admin", 
          "sensor_read", 
          "sensor_write", 
          "question_read", 
          "question_write", 
          "action_read", 
          "action_write", 
          "action_approval", 
          "notification_write", 
          "clients_read", 
          "question_log_read", 
          "content_admin"
        ]
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
              "permission": [
                "admin", 
                "sensor_read", 
                "sensor_write", 
                "question_read", 
                "question_write", 
                "action_read", 
                "action_write", 
                "action_approval", 
                "notification_write", 
                "clients_read", 
                "question_log_read", 
                "content_admin"
              ]
            }
          }
        ]
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


# Create a new user from the modified JSON file

```bash
create_user_from_json.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 -j "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json"
```

```
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
Created item: User, name: 'Jim Olsen CMDLINE TEST 8052', id: 14, ID: 14
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Fri Aug  7 15:27:41 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**