Tsat Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Help for Tsat](#user-content-help-for-tsat)

---------------------------

# Help for Tsat

  * Print the help for tsat.py
  * All scripts in bin/ will supply help if -h is on the command line
  * If passing in a parameter with a space or a special character, you need to surround it with quotes properly. On Windows this means double quotes. On Linux/Mac, this means single or double quotes, depending on what kind of character escaping you need.
  * If running this script on Linux or Mac, use the python scripts directly as the bin/tsat.py
  * If running this script on Windows, use the batch script in the winbin/tsat.bat so that python is called correctly.

```bash
tsat.py -h
```

```
usage: tsat.py [-h] [-u USERNAME] [-p PASSWORD] [--session_id SESSION_ID]
               [--host HOST] [--port PORT] [-l LOGLEVEL] [--debugformat]
               [--debug_method_locals] [--record_all_requests]
               [--stats_loop_enabled] [--http_auth_retry]
               [--http_retry_count HTTP_RETRY_COUNT]
               [--pytan_user_config PYTAN_USER_CONFIG]
               [--force_server_version FORCE_SERVER_VERSION]
               [--platform PLATFORMS] [--category CATEGORIES]
               [--output_dir REPORT_DIR] [--sleep SLEEP]
               [--pct PCT_COMPLETE_THRESHOLD] [--timeout TIMEOUT]
               [-f QUESTION_FILTERS] [-o QUESTION_OPTIONS] [--sensors-help]
               [--filters-help] [--options-help]

Tanium Sensor Analysis Tool: asks a question for every sensor and saves theresults as CSV reports

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

TSAT Options:
  --platform PLATFORMS  Only ask questions for sensors on a given platform
                        (default: [])
  --category CATEGORIES
                        Only ask questions for sensors in a given category
                        (default: [])
  --output_dir REPORT_DIR
                        Directory to save output to (default: /Users/jolsen/gh
                        /pytan/TSAT_OUTPUT/2015_10_02-16_09_39-EDT)
  --sleep SLEEP         Number of seconds to wait between asking questions
                        (default: 1)
  --pct PCT_COMPLETE_THRESHOLD
                        Percent to consider questions complete (default: 99.0)
  --timeout TIMEOUT     How many seconds to wait before a question times out
                        (default: 300)
  -f QUESTION_FILTERS, --filter QUESTION_FILTERS
                        Whole question filter; pass --filters-help to get a
                        full description (default: [])
  -o QUESTION_OPTIONS, --option QUESTION_OPTIONS
                        Whole question option; pass --options-help to get a
                        full description (default: [])
  --sensors-help        Get the full help for sensor strings (default: False)
  --filters-help        Get the full help for filters strings (default: False)
  --options-help        Get the full help for options strings (default: False)
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v2.1.0`, date: Fri Oct  2 16:09:39 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**