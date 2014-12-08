Create Package From Json Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Create Package From Json Help](#user-content-create-package-from-json-help)
  * [Export package id 1 as JSON](#user-content-export-package-id-1-as-json)
  * [Change name or url_regex in the JSON](#user-content-change-name-or-url_regex-in-the-json)
  * [Create a new package from the modified JSON file](#user-content-create-a-new-package-from-the-modified-json-file)

---------------------------

# Create Package From Json Help

  * Create a package object from a json file

```bash
create_package_from_json.py -h
```

```
usage: create_package_from_json.py [-h] -u USERNAME -p PASSWORD --host HOST
                                   [--port PORT] [-l LOGLEVEL] -j JSON_FILE

Create a package object from a json file

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

Create Package from JSON Options:
  -j JSON_FILE, --json JSON_FILE
                        JSON file to use for creating the object (default: )
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


# Export package id 1 as JSON

  * Get the first package object
  * Save the results to a JSON file

```bash
get_package.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --id 1 --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json" json
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
Found items:  PackageSpecList, len: 1
Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json' written with 1928 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json exists, content:

```
{
  "_type": "package_specs", 
  "package_spec": [
    {
      "_type": "package_spec", 
      "available_time": "2014-12-08T19:21:15", 
      "command": "cmd /c cscript //T:900 java-installer.vbs /KillAppsUsingJava:Yes /RebootIfNeeded:Yes /MaxWaitTimeInSeconds:300", 
      "command_timeout": 900, 
      "creation_time": "2014-12-08T19:20:46", 
      "deleted_flag": 0, 
...trimmed for brevity...
```



[TOC](#user-content-toc)


# Change name or url_regex in the JSON

  * Add CMDLINE TEST to name or url_regex in the JSON file

```bash
perl -p -i -e 's/^(      "(name|url_regex)": ".*)"/$1 CMDLINE TEST 7899"/gm' /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json && cat /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json
```

```
{
  "_type": "package_specs", 
  "package_spec": [
    {
      "_type": "package_spec", 
      "available_time": "2014-12-08T19:21:15", 
      "command": "cmd /c cscript //T:900 java-installer.vbs /KillAppsUsingJava:Yes /RebootIfNeeded:Yes /MaxWaitTimeInSeconds:300", 
      "command_timeout": 900, 
      "creation_time": "2014-12-08T19:20:46", 
      "deleted_flag": 0, 
      "display_name": "Update Java 64-bit - Kill / Reboot", 
      "expire_seconds": 1500, 
      "files": {
        "_type": "package_files", 
        "file": [
          {
            "_type": "file", 
            "bytes_downloaded": 17509, 
            "bytes_total": 17509, 
            "cache_status": "CACHED", 
            "download_seconds": 0, 
            "download_start_time": "2014-12-08T19:20:54", 
            "hash": "30bf532c4c1c5bb9599487712f88ff42190ccd2678192f7e61b160e6592cfbfe", 
            "id": 1, 
            "last_download_progress_time": "2014-12-08T19:21:05", 
            "name": "java-installer.vbs", 
            "size": 17509, 
            "source": "https://content.tanium.com/files/initialcontent/bundles/2014-11-05_12-56-07-8513/update_java_64-bit_-_kill_-_reboot/java-installer.vbs", 
            "status": 200
          }
        ]
      }, 
      "hidden_flag": 0, 
      "id": 1, 
      "last_modified_by": "Jim Olsen", 
      "last_update": "2014-12-08T19:20:46", 
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
      "modification_time": "2014-12-08T19:20:46", 
      "name": "Update Java 64-bit - Kill / Reboot CMDLINE TEST 7899", 
      "source_id": 0, 
      "verify_group_id": 0
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


# Create a new package from the modified JSON file

```bash
create_package_from_json.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 -j "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json"
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
Created item: PackageSpec, name: 'Update Java 64-bit - Kill / Reboot CMDLINE TEST 7899', ID: 97
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Mon Dec  8 14:59:47 2014 EST, Contact info: **Jim Olsen <jim.olsen@tanium.com>**