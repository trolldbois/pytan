Ask Parsed Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Help for Ask Parsed](#user-content-help-for-ask-parsed)

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
                     [-l LOGLEVEL] [--debugformat] [--record_all_requests]
                     [--stats_loop_enabled] [--http_auth_retry]
                     [--http_retry_count HTTP_RETRY_COUNT] -q QUESTION_TEXT
                     [--picker PICKER] [--no-results | --results]
                     [--file REPORT_FILE] [--dir REPORT_DIR]
                     [--enable_sse | --disable_sse]
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


###### generated by: `build_bin_doc v2.1.0`, date: Thu Sep  3 21:50:05 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**