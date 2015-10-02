Ask Saved Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Help for Ask Saved](#user-content-help-for-ask-saved)
  * [Ask a saved question](#user-content-ask-a-saved-question)
  * [Ask a saved question and refresh the data available before fetching the data](#user-content-ask-a-saved-question-and-refresh-the-data-available-before-fetching-the-data)

---------------------------

# Help for Ask Saved

  * Print the help for ask_saved.py
  * All scripts in bin/ will supply help if -h is on the command line
  * If passing in a parameter with a space or a special character, you need to surround it with quotes properly. On Windows this means double quotes. On Linux/Mac, this means single or double quotes, depending on what kind of character escaping you need.
  * If running this script on Linux or Mac, use the python scripts directly as the bin/ask_saved.py
  * If running this script on Windows, use the batch script in the winbin/ask_saved.bat so that python is called correctly.

```bash
ask_saved.py -h
```

```
usage: ask_saved.py [-h] [-u USERNAME] [-p PASSWORD] [--session_id SESSION_ID]
                    [--host HOST] [--port PORT] [-l LOGLEVEL] [--debugformat]
                    [--debug_method_locals] [--record_all_requests]
                    [--stats_loop_enabled] [--http_auth_retry]
                    [--http_retry_count HTTP_RETRY_COUNT]
                    [--pytan_user_config PYTAN_USER_CONFIG]
                    [--force_server_version FORCE_SERVER_VERSION]
                    [--no-refresh_data | --refresh_data]
                    [--id ID | --name NAME] [--file REPORT_FILE]
                    [--dir REPORT_DIR] [--enable_sse | --disable_sse]
                    [--sse_format {csv,xml,xml_obj,cef}] [--leading LEADING]
                    [--trailing TRAILING] [--export_format {csv,xml,json}]
                    [--sort HEADER_SORT | --no-sort | --auto_sort]
                    [--add-sensor | --no-add-sensor]
                    [--add-type | --no-add-type]
                    [--expand-columns | --no-columns]

Ask a saved question and save the results as a report format

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

Saved Question Selectors:
  --no-refresh_data     Do not refresh the data available for a saved question
                        (default)
  --refresh_data        Refresh the data available for a saved question
  --id ID               id of saved_question to ask (default: None)
  --name NAME           name of saved_question to ask (default: None)

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


# Ask a saved question

```bash
bin/ask_saved.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --name "Installed Applications" --file "/tmp/out.csv"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
++ Asking saved question: {
  "name": "Installed Applications", 
  "refresh_data": false
}
++ Saved Question 'Get Installed Applications from all machines' ID: 16093
Report file '/tmp/out.csv' written with 63722 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/out.csv exists, content:

```
Count,Name,Silent Uninstall String,Uninstallable,Version
756,[too many results],[too many results],[too many results],[too many results]
1,libminiupnpc8,nothing,Not Uninstallable,1.6-3ubuntu2.14.04.1
1,iso-codes,nothing,Not Uninstallable,3.52-1
1,libexttextcat-2.0-0,nothing,Not Uninstallable,3.4.3-1ubuntu1
1,growisofs,nothing,Not Uninstallable,7.1-10build1
1,libxml2:i386,nothing,Not Uninstallable,2.9.1+dfsg1-3ubuntu4.4
1,libsm6:i386,nothing,Not Uninstallable,2:1.2.1-2
1,findutils,nothing,Not Uninstallable,4.4.2-7
1,libgcr-base-3-1:i386,nothing,Not Uninstallable,3.10.1-1
...trimmed for brevity...
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Ask a saved question and refresh the data available before fetching the data

```bash
bin/ask_saved.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --name "Installed Applications" --file "/tmp/out.csv" --refresh_data
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
++ Asking saved question: {
  "name": "Installed Applications", 
  "refresh_data": true
}
2015-10-02 20:06:12,406 INFO     pytan.pollers.QuestionPoller: ID 16106: Reached Threshold of 99% (3 of 3)
++ Saved Question 'Get number of machines' ID: 16106
Report file '/tmp/out.csv' written with 63988 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/out.csv exists, content:

```
Count,Name,Silent Uninstall String,Uninstallable,Version
756,[too many results],[too many results],[too many results],[too many results]
1,libminiupnpc8,nothing,Not Uninstallable,1.6-3ubuntu2.14.04.1
1,iso-codes,nothing,Not Uninstallable,3.52-1
1,libexttextcat-2.0-0,nothing,Not Uninstallable,3.4.3-1ubuntu1
1,growisofs,nothing,Not Uninstallable,7.1-10build1
1,libxml2:i386,nothing,Not Uninstallable,2.9.1+dfsg1-3ubuntu4.4
1,libsm6:i386,nothing,Not Uninstallable,2:1.2.1-2
1,findutils,nothing,Not Uninstallable,4.4.2-7
1,libgcr-base-3-1:i386,nothing,Not Uninstallable,3.10.1-1
...trimmed for brevity...
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v2.1.0`, date: Fri Oct  2 16:06:12 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**