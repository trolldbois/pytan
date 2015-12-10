Get Question Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Help for Get Question](#user-content-help-for-get-question)
  * [Export all question objects as JSON](#user-content-export-all-question-objects-as-json)
  * [Export all question objects as CSV](#user-content-export-all-question-objects-as-csv)
  * [Export all question objects as xml](#user-content-export-all-question-objects-as-xml)

---------------------------

# Help for Get Question

  * Print the help for get_question.py
  * All scripts in bin/ will supply help if -h is on the command line
  * If passing in a parameter with a space or a special character, you need to surround it with quotes properly. On Windows this means double quotes. On Linux/Mac, this means single or double quotes, depending on what kind of character escaping you need.
  * If running this script on Linux or Mac, use the python scripts directly as the bin/get_question.py
  * If running this script on Windows, use the batch script in the winbin/get_question.bat so that python is called correctly.

```bash
get_question.py -h
```

```
usage: get_question.py [-h] [-u USERNAME] [-p PASSWORD]
                       [--session_id SESSION_ID] [--host HOST] [--port PORT]
                       [-l LOGLEVEL] [--debugformat] [--debug_method_locals]
                       [--record_all_requests] [--stats_loop_enabled]
                       [--http_auth_retry]
                       [--http_retry_count HTTP_RETRY_COUNT]
                       [--pytan_user_config PYTAN_USER_CONFIG]
                       [--force_server_version FORCE_SERVER_VERSION] [--all]
                       [--id ID] [--file REPORT_FILE] [--dir REPORT_DIR]
                       [--export_format {csv,xml,json}]
                       [--sort HEADER_SORT | --no-sort | --auto_sort]
                       [--no-explode-json | --explode-json]
                       [--no-include_type | --include_type]
                       [--no-minimal | --minimal]

Get an object of type: question and save the object to a report file

optional arguments:
  -h, --help            show this help message and exit

Handler Authentication:
  -u USERNAME, --username USERNAME
                        Name of user (default: None)
  -p PASSWORD, --password PASSWORD
                        Password of user (default: None)
  --session_id SESSION_ID
                        Session ID to authenticate with instead of
                        username/password (default: None)
  --host HOST           Hostname/ip of SOAP Server (default: None)
  --port PORT           Port to use when connecting to SOAP Server (default:
                        443)

Handler Options:
  -l LOGLEVEL, --loglevel LOGLEVEL
                        Logging level to use, increase for more verbosity
                        (default: 0)
  --debugformat         Enable debug format for logging (default: False)
  --debug_method_locals
                        Enable debug logging for each methods local variables
                        (default: False)
  --record_all_requests
                        Record all requests in
                        handler.session.ALL_REQUESTS_RESPONSES (default:
                        False)
  --stats_loop_enabled  Enable the statistics loop (default: False)
  --http_auth_retry     Disable retry on HTTP authentication failures
                        (default: True)
  --http_retry_count HTTP_RETRY_COUNT
                        Retry count for HTTP failures/invalid responses
                        (default: 5)
  --pytan_user_config PYTAN_USER_CONFIG
                        PyTan User Config file to use for PyTan arguments
                        (defaults to: ~/.pytan_config.json) (default: )
  --force_server_version FORCE_SERVER_VERSION
                        Force PyTan to consider the server version as this,
                        instead of relying on the server version derived from
                        the server info page. (default: )

Get Question Options:
  --all                 Get all questions (default: False)
  --id ID               id of question to get (default: [])

Report File Options:
  --file REPORT_FILE    File to save report to (will be automatically
                        generated if not supplied) (default: None)
  --dir REPORT_DIR      Directory to save report to (current directory will be
                        used if not supplied) (default: None)

Export Options:
  --export_format {csv,xml,json}
                        Export Format to create report file in, only used if
                        sse = False (default: csv)
  --sort HEADER_SORT    Only for export_format csv, Sort headers by given
                        names (default: [])
  --no-sort             Only for export_format csv, Do not sort the headers at
                        all
  --auto_sort           Only for export_format csv, Sort the headers with a
                        basic alphanumeric sort (default)
  --no-explode-json     Only for export_format csv or json, Do not explode any
                        embedded JSON into their own columns
  --explode-json        Only for export_format csv or json, Only for
                        export_format csv, Explode any embedded JSON into
                        their own columns (default)
  --no-include_type     Only for export_format json, Do not include SOAP type
                        in JSON output
  --include_type        Only for export_format json, Include SOAP type in JSON
                        output (default)
  --no-minimal          Only for export_format xml, Produce the full XML
                        representation, including empty attributes
  --minimal             Only for export_format xml, Only include attributes
                        that are not empty (default)
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Export all question objects as JSON

  * Get all question objects
  * Save the results to a JSON file

```bash
bin/get_question.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --all --file "/tmp/out.json" --export_format json
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
Found items:  QuestionList, len: 3031
Report file '/tmp/out.json' written with 2446730 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist
    * Valid: **True**
    * Messages: File /tmp/out.json exists

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Export all question objects as CSV

  * Get all question objects
  * Save the results to a csv file

```bash
bin/get_question.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --all --file "/tmp/out.csv"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
Found items:  QuestionList, len: 3031
Report file '/tmp/out.csv' written with 533906 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist
    * Valid: **True**
    * Messages: File /tmp/out.csv exists

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Export all question objects as xml

  * Get all question objects
  * Save the results to a xml file

```bash
bin/get_question.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --all --file "/tmp/out.xml"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
Found items:  QuestionList, len: 3031
Report file '/tmp/out.xml' written with 533906 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist
    * Valid: **True**
    * Messages: File /tmp/out.xml exists

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v2.1.0`, date: Fri Oct  2 16:08:08 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**