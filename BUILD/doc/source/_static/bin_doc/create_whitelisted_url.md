Create Whitelisted Url Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Help for Create Whitelisted Url](#user-content-help-for-create-whitelisted-url)
  * [Create a whitelisted URL](#user-content-create-a-whitelisted-url)

---------------------------

# Help for Create Whitelisted Url

  * Print the help for create_whitelisted_url.py
  * All scripts in bin/ will supply help if -h is on the command line
  * If passing in a parameter with a space or a special character, you need to surround it with quotes properly. On Windows this means double quotes. On Linux/Mac, this means single or double quotes, depending on what kind of character escaping you need.
  * If running this script on Linux or Mac, use the python scripts directly as the bin/create_whitelisted_url.py
  * If running this script on Windows, use the batch script in the winbin/create_whitelisted_url.bat so that python is called correctly.

```bash
create_whitelisted_url.py -h
```

```
usage: create_whitelisted_url.py [-h] [-u USERNAME] [-p PASSWORD]
                                 [--session_id SESSION_ID] [--host HOST]
                                 [--port PORT] [-l LOGLEVEL] [--debugformat]
                                 [--debug_method_locals]
                                 [--record_all_requests]
                                 [--stats_loop_enabled] [--http_auth_retry]
                                 [--http_retry_count HTTP_RETRY_COUNT]
                                 [--pytan_user_config PYTAN_USER_CONFIG]
                                 [--force_server_version FORCE_SERVER_VERSION]
                                 --url URL [--regex] [-d DOWNLOAD_SECONDS]
                                 [-prop PROPERTIES PROPERTIES]

Create a Whitelisted URL object from command line arguments

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

Create Whitelisted URL Options:
  --url URL             Text of new Whitelisted URL (default: None)
  --regex               Whitelisted URL is a regex pattern (default: False)
  -d DOWNLOAD_SECONDS, --download DOWNLOAD_SECONDS
                        Download Whitelisted URL every N seconds (default:
                        86400)
  -prop PROPERTIES PROPERTIES, --property PROPERTIES PROPERTIES
                        Property name and value to assign to Whitelisted URL
                        (default: [])
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Create a whitelisted URL

  * Create a whitelisted_url for https://testing.com
  * Set the new URL as a regex pattern
  * Set thew new URL to be re-downloaded every 3600 seconds
  * Create a property named property name with the value property value on the new URL

```bash
bin/create_whitelisted_url.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --url "https://testing.com/9115" --regex --download 3600 --property "property name" "property value"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
New Whitelisted URL 'regex:https://testing.com/9115' created with ID 49
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v2.1.0`, date: Fri Oct  2 16:06:31 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**