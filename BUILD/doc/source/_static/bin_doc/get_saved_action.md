Get Saved Action Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Get Saved Action Help](#user-content-get-saved-action-help)
  * [Export all saved_action as JSON](#user-content-export-all-saved_action-as-json)
  * [Export all saved_action as CSV](#user-content-export-all-saved_action-as-csv)
  * [Export all saved_action as xml](#user-content-export-all-saved_action-as-xml)

---------------------------

# Get Saved Action Help

  * Get saved_action and save as report format

```bash
get_saved_action.py -h
```

```
usage: get_saved_action.py [-h] [-u USERNAME] [-p PASSWORD] [--host HOST]
                           [--port PORT] [-l LOGLEVEL] [--all] [--id ID]
                           [--name NAME] [--file REPORT_FILE]
                           [--dir REPORT_DIR]
                           {csv,json,xml} ...

Get saved_action and save as report format

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

Get Saved action Options:
  --all                 Get all saved_actions (default: False)
  --id ID               id of saved_action to get (default: [])
  --name NAME           name of saved_action to get (default: [])

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

usage: get_saved_action.py csv [-h]
                               [--sort HEADER_SORT | --no-sort | --auto_sort]
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

usage: get_saved_action.py json [-h] [--explode-json | --no-explode-json]
                                [--no-include_type | --include_type]

JSON Export Options

optional arguments:
  -h, --help         show this help message and exit
  --explode-json     Explode any embedded JSON into their own columns
  --no-explode-json  Do not explode any embedded JSON into their own columns
                     (default)
  --no-include_type  Do not include SOAP type in JSON output
  --include_type     Include SOAP type in JSON output (default)

usage: get_saved_action.py xml [-h] [--no-minimal | --minimal]

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


# Export all saved_action as JSON

  * Get all saved_action objects
  * Save the results to a JSON file

```bash
get_saved_action.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --all --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json" json
```

```
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
Found items:  SavedActionList, len: 4
Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json' written with 7168 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json exists



[TOC](#user-content-toc)


# Export all saved_action as CSV

  * Get all saved_action objects
  * Save the results to a csv file

```bash
get_saved_action.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --all --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv" csv
```

```
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
Found items:  SavedActionList, len: 4
Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv' written with 2208 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv exists



[TOC](#user-content-toc)


# Export all saved_action as xml

  * Get all saved_action objects
  * Save the results to a xml file

```bash
get_saved_action.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --all --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.xml" xml
```

```
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
Found items:  SavedActionList, len: 4
Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.xml' written with 10881 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.xml exists



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Fri Aug  7 15:34:22 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**