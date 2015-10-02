Ask Parsed Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Help for Ask Parsed](#user-content-help-for-ask-parsed)
  * [Ask a parsed question example 1](#user-content-ask-a-parsed-question-example-1)
  * [Ask a parsed question example 2](#user-content-ask-a-parsed-question-example-2)
  * [Ask a parsed question example 3](#user-content-ask-a-parsed-question-example-3)
  * [Ask a parsed question example 4](#user-content-ask-a-parsed-question-example-4)

---------------------------

# Help for Ask Parsed

  * Print the help for ask_parsed.py
  * All scripts in bin/ will supply help if -h is on the command line
  * If passing in a parameter with a space or a special character, you need to surround it with quotes properly. On Windows this means double quotes. On Linux/Mac, this means single or double quotes, depending on what kind of character escaping you need.
  * If running this script on Linux or Mac, use the python scripts directly as the bin/ask_parsed.py
  * If running this script on Windows, use the batch script in the winbin/ask_parsed.bat so that python is called correctly.

```bash
ask_parsed.py -h
```

```
usage: ask_parsed.py [-h] [-u USERNAME] [-p PASSWORD]
                     [--session_id SESSION_ID] [--host HOST] [--port PORT]
                     [-l LOGLEVEL] [--debugformat] [--debug_method_locals]
                     [--record_all_requests] [--stats_loop_enabled]
                     [--http_auth_retry] [--http_retry_count HTTP_RETRY_COUNT]
                     [--pytan_user_config PYTAN_USER_CONFIG]
                     [--force_server_version FORCE_SERVER_VERSION] -q
                     QUESTION_TEXT [--picker PICKER]
                     [--no-results | --results] [--file REPORT_FILE]
                     [--dir REPORT_DIR] [--enable_sse | --disable_sse]
                     [--sse_format {csv,xml,xml_obj,cef}] [--leading LEADING]
                     [--trailing TRAILING] [--export_format {csv,xml,json}]
                     [--sort HEADER_SORT | --no-sort | --auto_sort]
                     [--add-sensor | --no-add-sensor]
                     [--add-type | --no-add-type]
                     [--expand-columns | --no-columns]

Ask a parsed question and save the results as a report format

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

Parsed Question Options:
  -q QUESTION_TEXT, --question_text QUESTION_TEXT
                        The question text you want the server to parse into a
                        list of parsed results (default: )
  --picker PICKER       The index number of the parsed results that correlates
                        to the actual question you wish to run -- you can get
                        this by running this once without it to print out a
                        list of indexes (default: None)
  --no-results          Do not get the results after asking the quesiton
                        action
  --results             Get the results after asking the quesiton (default)
                        (default: True)

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


# Ask a parsed question example 1

  * Ask a simple question in english with just one sensor
  * Since --picker is not provided, this will exit with an error and print all of the results that the english form was parsed into, prepended with an index. This should be re-run with --picker INDEX_NUMBER, as seen in the rest of these examples.

```bash
bin/ask_parsed.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 -q "get computer name"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
++ Asking parsed question:
{
  "get_results": true, 
  "picker": null, 
  "question_text": "get computer name"
}
2015-10-02 20:05:49,235 CRITICAL pytan.handler: You must supply an index as picker=$index to choose one of the parse responses -- re-run ask_parsed with picker set to one of these indexes!!
2015-10-02 20:05:49,235 CRITICAL pytan.handler: Index 1, Score: 6823, Query: 'Get Computer Name from all machines'
2015-10-02 20:05:49,235 CRITICAL pytan.handler: Index 2, Score: 1292, Query: 'Get Computer ID from all machines'
2015-10-02 20:05:49,235 CRITICAL pytan.handler: Index 3, Score: 646, Query: 'Get Computer ID containing "name" from all machines'
2015-10-02 20:05:49,235 CRITICAL pytan.handler: Index 4, Score: 457, Query: 'Get AD Computer Groups from all machines'
2015-10-02 20:05:49,235 CRITICAL pytan.handler: Index 5, Score: 323, Query: 'Get BIOS Name from all machines'
2015-10-02 20:05:49,235 CRITICAL pytan.handler: Index 6, Score: 228, Query: 'Get Computer Serial Number from all machines'
2015-10-02 20:05:49,235 CRITICAL pytan.handler: Index 7, Score: 228, Query: 'Get Domain Name from all machines'


Error occurred: You must supply an index as picker=$index to choose one of the parse responses -- re-run ask_parsed with picker set to one of these indexes!!
```

```STDERR
Traceback (most recent call last):
  File "/Users/jolsen/gh/pytan/lib/pytan/binsupport.py", line 2585, in process_ask_parsed_args
    response = handler.ask(qtype='parsed', **obj_grp_args)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 388, in ask
    result = method(**clean_kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 828, in ask_parsed
    raise pytan.exceptions.PickerError(pw())
PickerError: You must supply an index as picker=$index to choose one of the parse responses -- re-run ask_parsed with picker set to one of these indexes!!
```

  * Validation Test: notexitcode
    * Valid: **True**
    * Messages: Exit Code is not 0



[TOC](#user-content-toc)


# Ask a parsed question example 2

  * Ask a simple question in english with just one sensor
  * Pick the first match that the english form gets parsed into
  * Save the results to a CSV file

```bash
bin/ask_parsed.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 -q "get computer name" --picker 1 --file "/tmp/out.csv"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
++ Asking parsed question:
{
  "get_results": true, 
  "picker": 1, 
  "question_text": "get computer name"
}
2015-10-02 20:05:54,708 INFO     pytan.pollers.QuestionPoller: ID 16103: Reached Threshold of 99% (3 of 3)
++ Asked Question 'Get Computer Name from all machines' ID: 16103
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


# Ask a parsed question example 3

  * Ask a more complex question in english with two sensors
  * Pick the first match that the english form gets parsed into
  * Save the results to a CSV file

```bash
bin/ask_parsed.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 -q "get computer name and ip route details" --picker 1 --file "/tmp/out.csv"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
++ Asking parsed question:
{
  "get_results": true, 
  "picker": 1, 
  "question_text": "get computer name and ip route details"
}
2015-10-02 20:06:00,223 INFO     pytan.pollers.QuestionPoller: ID 16104: Reached Threshold of 99% (3 of 3)
++ Asked Question 'Get Computer Name and IP Route Details from all machines' ID: 16104
++ Report file '/tmp/out.csv' written with 678 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/out.csv exists, content:

```
Computer Name,Destination,Flags,Gateway,Interface,Mask,Metric
c1u14-virtual-machine.(none),"0.0.0.0
10.0.1.0","UG
U","10.0.1.1
0.0.0.0","eth0
eth0","0.0.0.0
255.255.255.0","0
1"
WIN-6U71ED4M23D,"10.0.1.11
127.0.0.1
...trimmed for brevity...
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Ask a parsed question example 4

  * Ask a more complex question in english with two sensors
  * Pick the first match that the english form gets parsed into
  * Do not wait for results, just ask the question and return right away. In this use case, you would want to use get_results.py to get the results for this question later.

```bash
bin/ask_parsed.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 -q "get computer name and ip route details" --picker 1 --no-results
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
++ Asking parsed question:
{
  "get_results": false, 
  "picker": 1, 
  "question_text": "get computer name and ip route details"
}
++ Asked Question 'Get Computer Name and IP Route Details from all machines' ID: 16105
++ No action results returned, run get_results.py to get the results
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v2.1.0`, date: Fri Oct  2 16:06:00 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**