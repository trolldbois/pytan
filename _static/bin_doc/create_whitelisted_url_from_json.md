Create Whitelisted Url From Json Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Create Whitelisted Url From Json Help](#user-content-create-whitelisted-url-from-json-help)
  * [Export whitelisted_url id 1 as JSON](#user-content-export-whitelisted_url-id-1-as-json)
  * [Change name or url_regex in the JSON](#user-content-change-name-or-url_regex-in-the-json)
  * [Create a new whitelisted_url from the modified JSON file](#user-content-create-a-new-whitelisted_url-from-the-modified-json-file)

---------------------------

# Create Whitelisted Url From Json Help

  * Create a whitelisted_url object from a json file

```bash
create_whitelisted_url_from_json.py -h
```

```
usage: create_whitelisted_url_from_json.py [-h] -u USERNAME -p PASSWORD --host
                                           HOST [--port PORT] [-l LOGLEVEL] -j
                                           JSON_FILE

Create a whitelisted_url object from a json file

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

Create Whitelisted url from JSON Options:
  -j JSON_FILE, --json JSON_FILE
                        JSON file to use for creating the object (default: )
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


# Export whitelisted_url id 1 as JSON

  * Get the first whitelisted_url object
  * Save the results to a JSON file

```bash
get_whitelisted_url.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --id 1 --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json" json
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
Found items:  WhiteListedUrlList, len: 11
Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json' written with 2459 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json exists, content:

```
{
  "_type": "white_listed_urls", 
  "white_listed_url": [
    {
      "_type": "white_listed_url", 
      "download_seconds": 86400, 
      "id": 1, 
      "url_regex": "test1"
    }, 
    {
...trimmed for brevity...
```



[TOC](#user-content-toc)


# Change name or url_regex in the JSON

  * Add CMDLINE TEST to name or url_regex in the JSON file

```bash
perl -p -i -e 's/^(      "(name|url_regex)": ".*)"/$1 CMDLINE TEST 4893"/gm' /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json && cat /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json
```

```
{
  "_type": "white_listed_urls", 
  "white_listed_url": [
    {
      "_type": "white_listed_url", 
      "download_seconds": 86400, 
      "id": 1, 
      "url_regex": "test1 CMDLINE TEST 4893"
    }, 
    {
      "_type": "white_listed_url", 
      "download_seconds": 86400, 
      "id": 2, 
      "url_regex": "test2 CMDLINE TEST 4893"
    }, 
    {
      "_type": "white_listed_url", 
      "download_seconds": 86400, 
      "id": 3, 
      "url_regex": "test3 CMDLINE TEST 4893"
    }, 
    {
      "_type": "white_listed_url", 
      "download_seconds": 86400, 
      "id": 7, 
      "url_regex": "test1 API TEST CMDLINE TEST 4893"
    }, 
    {
      "_type": "white_listed_url", 
      "download_seconds": 3600, 
      "id": 8, 
      "metadata": {
        "_type": "metadata", 
        "item": [
          {
            "_type": "item", 
            "admin_flag": 0, 
            "name": "TConsole.WhitelistedURL.property name", 
            "value": "property value"
          }
        ]
      }, 
      "url_regex": "regex:https://testing.com/9741 CMDLINE TEST 4893"
    }, 
    {
      "_type": "white_listed_url", 
      "download_seconds": 86400, 
      "id": 9, 
      "url_regex": "test1 CMDLINE TEST 3257 CMDLINE TEST 4893"
    }, 
    {
      "_type": "white_listed_url", 
      "download_seconds": 86400, 
      "id": 10, 
      "url_regex": "test2 CMDLINE TEST 3257 CMDLINE TEST 4893"
    }, 
    {
      "_type": "white_listed_url", 
      "download_seconds": 86400, 
      "id": 11, 
      "url_regex": "test3 CMDLINE TEST 3257 CMDLINE TEST 4893"
    }, 
    {
      "_type": "white_listed_url", 
      "download_seconds": 86400, 
      "id": 12, 
      "url_regex": "test1 API TEST CMDLINE TEST 3257 CMDLINE TEST 4893"
    }, 
    {
      "_type": "white_listed_url", 
      "download_seconds": 3600, 
      "id": 13, 
      "metadata": {
        "_type": "metadata", 
        "item": [
          {
            "_type": "item", 
            "admin_flag": 0, 
            "name": "TConsole.WhitelistedURL.property name", 
            "value": "property value"
          }
        ]
      }, 
      "url_regex": "regex:https://testing.com/9741 CMDLINE TEST 3257 CMDLINE TEST 4893"
    }, 
    {
      "_type": "white_listed_url", 
      "download_seconds": 3600, 
      "id": 14, 
      "metadata": {
        "_type": "metadata", 
        "item": [
          {
            "_type": "item", 
            "admin_flag": 0, 
            "name": "TConsole.WhitelistedURL.property name", 
            "value": "property value"
          }
        ]
      }, 
      "url_regex": "regex:https://testing.com/298 CMDLINE TEST 4893"
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


# Create a new whitelisted_url from the modified JSON file

```bash
create_whitelisted_url_from_json.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 -j "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json"
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
Created item: WhiteListedUrl, id: 15, ID: 15
Created item: WhiteListedUrl, id: 16, ID: 16
Created item: WhiteListedUrl, id: 17, ID: 17
Created item: WhiteListedUrl, id: 18, ID: 18
Created item: WhiteListedUrl, id: 19, ID: 19
Created item: WhiteListedUrl, id: 20, ID: 20
Created item: WhiteListedUrl, id: 21, ID: 21
Created item: WhiteListedUrl, id: 22, ID: 22
Created item: WhiteListedUrl, id: 23, ID: 23
Created item: WhiteListedUrl, id: 24, ID: 24
Created item: WhiteListedUrl, id: 25, ID: 25
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Mon Dec  8 14:59:52 2014 EST, Contact info: **Jim Olsen <jim.olsen@tanium.com>**