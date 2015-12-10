Create Package Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Help for Create Package](#user-content-help-for-create-package)
  * [Create a new package](#user-content-create-a-new-package)
  * [Delete the recently created package](#user-content-delete-the-recently-created-package)

---------------------------

# Help for Create Package

  * Print the help for create_package.py
  * All scripts in bin/ will supply help if -h is on the command line
  * If passing in a parameter with a space or a special character, you need to surround it with quotes properly. On Windows this means double quotes. On Linux/Mac, this means single or double quotes, depending on what kind of character escaping you need.
  * If running this script on Linux or Mac, use the python scripts directly as the bin/create_package.py
  * If running this script on Windows, use the batch script in the winbin/create_package.bat so that python is called correctly.

```bash
create_package.py -h
```

```
usage: create_package.py [-h] [-u USERNAME] [-p PASSWORD]
                         [--session_id SESSION_ID] [--host HOST] [--port PORT]
                         [-l LOGLEVEL] [--debugformat] [--debug_method_locals]
                         [--record_all_requests] [--stats_loop_enabled]
                         [--http_auth_retry]
                         [--http_retry_count HTTP_RETRY_COUNT]
                         [--pytan_user_config PYTAN_USER_CONFIG]
                         [--force_server_version FORCE_SERVER_VERSION] -n NAME
                         -c COMMAND [-d DISPLAY_NAME]
                         [--command-timeout COMMAND_TIMEOUT_SECONDS]
                         [--expire-seconds EXPIRE_SECONDS] [-f FILE_URLS]
                         [--parameters-file PARAMETERS_JSON_FILE]
                         [-vf VERIFY_FILTERS] [-vo VERIFY_FILTER_OPTIONS]
                         [--filters-help] [--options-help]
                         [--verify-expire-seconds VERIFY_EXPIRE_SECONDS]

Create a package object from command line arguments

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

Create Package Options:
  -n NAME, --name NAME  Name of package to create (default: None)
  -c COMMAND, --command COMMAND
                        Command to execute with package (default: )
  -d DISPLAY_NAME, --display-name DISPLAY_NAME
                        Display name of package (default: )
  --command-timeout COMMAND_TIMEOUT_SECONDS
                        Command for this package timeout in N seconds
                        (default: 600)
  --expire-seconds EXPIRE_SECONDS
                        Expire actions created for this package in N seconds
                        (default: 600)
  -f FILE_URLS, --file-url FILE_URLS
                        URL of file to include with package, can specify any
                        of the following: "$url", or
                        "$download_seconds::$url", or "$filename||$url", or
                        "$filename||$download_seconds::$url" (default: [])
  --parameters-file PARAMETERS_JSON_FILE
                        JSON file describing parameters for this package, see
                        doc/example_of_all_package_parameters.json for an
                        example (default: )
  -vf VERIFY_FILTERS, --verify-filter VERIFY_FILTERS
                        Filters to use for verifying the package after it is
                        deployed, , supply --filters-help to see filter help
                        (default: [])
  -vo VERIFY_FILTER_OPTIONS, --verify-option VERIFY_FILTER_OPTIONS
                        Options to use for the verify filters, supply
                        --options-help to see options help (default: [])
  --filters-help        Get the full help for filters strings (default: False)
  --options-help        Get the full help for options strings (default: False)
  --verify-expire-seconds VERIFY_EXPIRE_SECONDS
                        Expire the verify filters used by this package in N
                        seconds (default: 600)
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Create a new package

  * Create a package named 1234 CMDLINE TEST package
  * Set the display name in the console for the new package to 1234 CMDLINE TEST package display name
    * Supply an option for the verification filter that ignores case
  * When this package is deployed, run the command testing.vbs and expect 8 arguments
  * When this package is deployed as part of an action, default the action to expire after 3600 seconds
  * Add a file to this package that will be redownloaded every 3600 seconds, named testing.vbs in Tanium, and downloaded from testing.com/testing.vbs
  * Add another file to this package that will be downloaded once, extract the file name from the URL, and downloaded from testing.com/another_testing.vbs
  * Add all the parameters defined in doc/example_of_all_package_parameters.json
  * Expire the verification filter after 3600 seconds
  * Expire the command if it takes longer than 600 seconds to run
  * Supply a verification filter that will be used when this package is deployed as part of an action

```bash
bin/create_package.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --name "1234 CMDLINE TEST package" --display-name "1234 CMDLINE TEST package display name" --command "testing.vbs \$1 \$2 \$3 \$4 \$5 \$6 \$7 \$8" --expire-seconds 1500 --file-url "3600::testing.vbs||https://testing.com/testing.vbs" --file-url "https://testing.com/another_testing.vbs" --parameters-file "doc/example_of_all_package_parameters.json" --verify-expire-seconds 3600 --verify-filter "Custom Tags, that contains:tag" --verify-option "ignore_case" --command-timeout 600
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
New package '1234 CMDLINE TEST package' created with ID 125, command: 'testing.vbs $1 $2 $3 $4 $5 $6 $7 $8'
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Delete the recently created package

  * Delete the package named 1234 CMDLINE TEST package

```bash
bin/delete_package.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --name "1234 CMDLINE TEST package"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
Deleted item:  PackageSpec, id: 125
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v2.1.0`, date: Fri Oct  2 16:06:19 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**