Get Results Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Help for Get Results](#user-content-help-for-get-results)
  * [Ask a question](#user-content-ask-a-question)
  * [Wait 30 seconds](#user-content-wait-30-seconds)
  * [Get the results for a question](#user-content-get-the-results-for-a-question)
  * [Get the results for a question via a server side export](#user-content-get-the-results-for-a-question-via-a-server-side-export)

---------------------------

# Help for Get Results

  * Print the help for get_results.py
  * All scripts in bin/ will supply help if -h is on the command line
  * If passing in a parameter with a space or a special character, you need to surround it with quotes properly. On Windows this means double quotes. On Linux/Mac, this means single or double quotes, depending on what kind of character escaping you need.
  * If running this script on Linux or Mac, use the python scripts directly as the bin/get_results.py
  * If running this script on Windows, use the batch script in the winbin/get_results.bat so that python is called correctly.

```bash
get_results.py -h
```

```
usage: get_results.py [-h] [-u USERNAME] [-p PASSWORD]
                      [--session_id SESSION_ID] [--host HOST] [--port PORT]
                      [-l LOGLEVEL] [--debugformat] [--debug_method_locals]
                      [--record_all_requests] [--stats_loop_enabled]
                      [--http_auth_retry]
                      [--http_retry_count HTTP_RETRY_COUNT]
                      [--pytan_user_config PYTAN_USER_CONFIG]
                      [--force_server_version FORCE_SERVER_VERSION]
                      [-o {saved_question,question,action}] [-i ID] [-n NAME]
                      [--file REPORT_FILE] [--dir REPORT_DIR]
                      [--enable_sse | --disable_sse]
                      [--sse_format {csv,xml,xml_obj,cef}] [--leading LEADING]
                      [--trailing TRAILING] [--export_format {csv,xml,json}]
                      [--sort HEADER_SORT | --no-sort | --auto_sort]
                      [--add-sensor | --no-add-sensor]
                      [--add-type | --no-add-type]
                      [--expand-columns | --no-columns]

Get results from a deploy action, saved question, or question

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

Get Result Options:
  -o {saved_question,question,action}, --object {saved_question,question,action}
                        Type of object to get results for (default: question)
  -i ID, --id ID        id of object to get results for (default: None)
  -n NAME, --name NAME  name of object to get results for (default: )

Report File Options:
  --file REPORT_FILE    File to save report to (will be automatically
                        generated if not supplied) (default: None)
  --dir REPORT_DIR      Directory to save report to (current directory will be
                        used if not supplied) (default: None)

Export Options:
  --enable_sse          Perform a server side export when getting data
                        (default: True)
  --disable_sse         Perform a normal get result data export when getting
                        data (default: True)
  --sse_format {csv,xml,xml_obj,cef}
                        If sse = True, perform server side export in this
                        format (default: xml_obj)
  --leading LEADING     If sse = True, and sse_format = "cef", prepend each
                        row with this text (default: )
  --trailing TRAILING   If sse = True, and sse_format = "cef", append each row
                        with this text (default: )
  --export_format {csv,xml,json}
                        Export Format to create report file in, only used if
                        sse = False (default: csv)
  --sort HEADER_SORT    For export_format: csv, Sort headers by given names
                        (default: [])
  --no-sort             For export_format: csv, Do not sort the headers at all
  --auto_sort           For export_format: csv, Sort the headers with a basic
                        alphanumeric sort (default)
  --add-sensor          For export_format: csv, Add the sensor names to each
                        header
  --no-add-sensor       For export_format: csv, Do not add the sensor names to
                        each header (default)
  --add-type            For export_format: csv, Add the result type to each
                        header
  --no-add-type         For export_format: csv, Do not add the result type to
                        each header (default)
  --expand-columns      For export_format: csv, Expand multi-line cells into
                        their own rows that have sensor correlated columns in
                        the new rows
  --no-columns          For export_format: csv, Do not add expand multi-line
                        cells into their own rows (default)
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Ask a question

  * Ask a question without getting the results, save stdout to ask.out

```bash
bin/ask_manual.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --no-results --sensor "Computer Name" | tee /tmp/ask.out
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
++ Asking manual question:
{
  "filters_help": false, 
  "get_results": false, 
  "options_help": false, 
  "question_filters": [], 
  "question_options": [], 
  "sensors": [
    "Computer Name"
  ], 
  "sensors_help": false
}
++ Asked Question 'Get Computer Name from all machines' ID: 16112
++ No action results returned, run get_results.py to get the results
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/ask.out exists, content:

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
++ Asking manual question:
{
  "filters_help": false, 
  "get_results": false, 
  "options_help": false, 
  "question_filters": [], 
  "question_options": [], 
  "sensors": [
    "Computer Name"
...trimmed for brevity...
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Wait 30 seconds

  * Wait 30 seconds for data for the previously asked question to be available

```bash
sleep 15
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Get the results for a question

  * Get the results for the question ID asked previously
  * Save the results to a CSV file

```bash
bin/get_results.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 -o "question" --id `cat /tmp/ask.out | grep ID| cut -d: -f2 | tr -d " "` --file "/tmp/out.csv"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
++ Found object: Question, id: 16112
2015-10-02 20:08:25,761 INFO     pytan.pollers.SSEPoller: ID '1/497131669533.xml': Server Side Export Completed: 'Completed. 3 rows written.'
++ Found results for object: ResultSet for ID None, Columns: 2, Total Rows: None, Current Rows: 3, EstTotal: None, Passed: None, MrPassed: None, Tested: None, MrTested: None
++ Report file '/tmp/out.csv' written with 81 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/out.csv exists, content:

```
Computer Name
c1u14-virtual-machine.(none)
WIN-6U71ED4M23D
TPT1.pytanlab.com
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Get the results for a question via a server side export

  * Get the results for the question ID asked previously using a server side export
  * Save the results to a CSV file

```bash
bin/get_results.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 -o "question" --id `cat /tmp/ask.out | grep ID| cut -d: -f2 | tr -d " "` --file "/tmp/out.csv" --enable_sse
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
++ Found object: Question, id: 16112
2015-10-02 20:08:26,194 INFO     pytan.pollers.SSEPoller: ID '1/497131669970.xml': Server Side Export Completed: 'Completed. 3 rows written.'
++ Found results for object: ResultSet for ID None, Columns: 2, Total Rows: None, Current Rows: 3, EstTotal: None, Passed: None, MrPassed: None, Tested: None, MrTested: None
++ Report file '/tmp/out.csv' written with 81 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/out.csv exists, content:

```
Computer Name
c1u14-virtual-machine.(none)
WIN-6U71ED4M23D
TPT1.pytanlab.com
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v2.1.0`, date: Fri Oct  2 16:08:26 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**