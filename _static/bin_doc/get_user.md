Get User Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Get User Help](#user-content-get-user-help)
  * [Export all user as JSON](#user-content-export-all-user-as-json)
  * [Export all user as CSV](#user-content-export-all-user-as-csv)
  * [Export all user as xml](#user-content-export-all-user-as-xml)

---------------------------

# Get User Help

  * Get user and save as report format

```bash
get_user.py -h
```

```
usage: get_user.py [-h] -u USERNAME -p PASSWORD --host HOST [--port PORT]
                   [-l LOGLEVEL] [--all] [--id ID] [--file REPORT_FILE]
                   [--dir REPORT_DIR]
                   {csv,json,xml} ...

Get user and save as report format

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

Get User Options:
  --all                 Get all users (default: False)
  --id ID               id of user to get (default: [])

Report File Options:
  --file REPORT_FILE    File to save report to (will be automatically
                        generated if not supplied) (default: None)
  --dir REPORT_DIR      Directory to save report to (current directory will be
                        used if not supplied) (default: None)

Export Formats:
  {csv,json,xml}        Export Format choices
    csv                 Produce a CSV report, supply "csv -h" to see CSV
                        options
    json                Produce a JSON report, supply "json -h" to see JSON
                        options
    xml                 Produce a XML report, supply "xml -h" to see XML
                        options

usage: get_user.py csv [-h] [--sort HEADER_SORT | --no-sort | --auto_sort]
                       [--no-explode-json | --explode-json]

CSV Export Options

optional arguments:
  -h, --help          show this help message and exit
  --sort HEADER_SORT  Sort headers by given names (default: [])
  --no-sort           Do not sort the headers at all
  --auto_sort         Sort the headers with a basic alphanumeric sort
                      (default)
  --no-explode-json   Do not explode any embedded JSON into their own columns
  --explode-json      Explode any embedded JSON into their own columns
                      (default)

usage: get_user.py json [-h] [--explode-json | --no-explode-json]
                        [--no-include_type | --include_type]

CSV Export Options

optional arguments:
  -h, --help         show this help message and exit
  --explode-json     Explode any embedded JSON into their own columns
  --no-explode-json  Do not explode any embedded JSON into their own columns
                     (default)
  --no-include_type  Do not include SOAP type in JSON output
  --include_type     Include SOAP type in JSON output (default)

usage: get_user.py xml [-h] [--no-minimal | --minimal]

XML Export Options

optional arguments:
  -h, --help    show this help message and exit
  --no-minimal  Produce the full XML representation, including empty
                attributes
  --minimal     Only include attributes that are not empty (default)
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


# Export all user as JSON

  * Get all user objects
  * Save the results to a JSON file

```bash
get_user.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --all --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json" json
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
Found items:  UserList, len: 5
Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json' written with 4006 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json exists



[TOC](#user-content-toc)


# Export all user as CSV

  * Get all user objects
  * Save the results to a csv file

```bash
get_user.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --all --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv" csv
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
Found items:  UserList, len: 5
Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv' written with 1398 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv exists



[TOC](#user-content-toc)


# Export all user as xml

  * Get all user objects
  * Save the results to a xml file

```bash
get_user.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --all --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.xml" xml
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
Found items:  UserList, len: 5
Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.xml' written with 2973 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.xml exists



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Mon Dec  8 15:02:31 2014 EST, Contact info: **Jim Olsen <jim.olsen@tanium.com>**