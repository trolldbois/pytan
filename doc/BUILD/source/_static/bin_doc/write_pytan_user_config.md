Write PyTan User Config Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Help for Write PyTan User Config](#user-content-help-for-write-pytan-user-config)
  * [Create a PyTan User Config file at the default location](#user-content-create-a-pytan-user-config-file-at-the-default-location)
  * [Test that the PyTan User Config file that was created above at the default location works for another script without having to supply any credentials on the command line](#user-content-test-that-the-pytan-user-config-file-that-was-created-above-at-the-default-location-works-for-another-script-without-having-to-supply-any-credentials-on-the-command-line)
  * [Create a PyTan User Config file at a custom location](#user-content-create-a-pytan-user-config-file-at-a-custom-location)
  * [Test that the PyTan User Config file that was created above at the custom location works for another script without having to supply any credentials on the command line](#user-content-test-that-the-pytan-user-config-file-that-was-created-above-at-the-custom-location-works-for-another-script-without-having-to-supply-any-credentials-on-the-command-line)
  * [Manually create a PyTan User Config file in JSON format with only two parameters](#user-content-manually-create-a-pytan-user-config-file-in-json-format-with-only-two-parameters)

---------------------------

# Help for Write PyTan User Config

  * Print the help for write_pytan_user_config.py
  * All scripts in bin/ will supply help if -h is on the command line
  * If passing in a parameter with a space or a special character, you need to surround it with quotes properly. On Windows this means double quotes. On Linux/Mac, this means single or double quotes, depending on what kind of character escaping you need.
  * If running this script on Linux or Mac, use the python scripts directly as the bin/write_pytan_user_config.py
  * If running this script on Windows, use the batch script in the winbin/write_pytan_user_config.bat so that python is called correctly.

```bash
write_pytan_user_config.py -h
```

```
usage: write_pytan_user_config.py [-h] [-u USERNAME] [-p PASSWORD]
                                  [--session_id SESSION_ID] [--host HOST]
                                  [--port PORT] [-l LOGLEVEL] [--debugformat]
                                  [--debug_method_locals]
                                  [--record_all_requests]
                                  [--stats_loop_enabled] [--http_auth_retry]
                                  [--http_retry_count HTTP_RETRY_COUNT]
                                  [--pytan_user_config PYTAN_USER_CONFIG]
                                  [--force_server_version FORCE_SERVER_VERSION]
                                  [--file FILE]

Creates a PyTan User Config based on the current parameters

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

Write PyTan User Config Options:
  --file FILE           PyTan User Config file to write for PyTan arguments
                        (defaults to: ~/.pytan_config.json) (default: )
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Create a PyTan User Config file at the default location

  * This will take the command line arguments and authenticate with them.
  * Upon successful authentication, a PyTan User Config file will be written in JSON format to ~/.pytan_config.json

```bash
bin/write_pytan_user_config.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
PyTan User config file successfully written: /Users/jolsen/.pytan_config.json
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /Users/jolsen/.pytan_config.json exists, content:

```
{
  "username": "Administrator", 
  "loglevel": 1, 
  "debugformat": false, 
  "session_id": null, 
  "host": "10.0.1.240", 
  "gmt_log": true, 
  "debug_method_locals": false, 
  "password": "::wbWfzuetm4WSZow=::", 
  "port": 443
}```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Test that the PyTan User Config file that was created above at the default location works for another script without having to supply any credentials on the command line

  * The print_sensors script should now successfully authenticate based on the parameters defined in the default location for the PyTan User Config file, and we no longer need to supply the parameters on the command line

```bash
print_sensors.py --name "Installed Applications"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
Found items:  SensorList, len: 1
Filtered out sourced sensors: 1
Filtered out sensors based on user filters: 1

  * Sensor Name: 'Installed Applications', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Applications
  * Description: List of the applications and versions of those applications installed on the client machine. Example: Mozilla Firefox | 16.0.1
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Create a PyTan User Config file at a custom location

  * This will take the command line arguments and authenticate with them.
  * Upon successful authentication, a PyTan User Config file will be written in JSON format to /tmp/custom.sjon

```bash
bin/write_pytan_user_config.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --file /tmp/custom.json
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
PyTan User config file successfully written: /tmp/custom.json
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/custom.json exists, content:

```
{
  "username": "Administrator", 
  "loglevel": 1, 
  "debugformat": false, 
  "session_id": null, 
  "host": "10.0.1.240", 
  "gmt_log": true, 
  "debug_method_locals": false, 
  "password": "::wbWfzuetm4WSZow=::", 
  "port": 443
}```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Test that the PyTan User Config file that was created above at the custom location works for another script without having to supply any credentials on the command line

  * The print_sensors script should now successfully authenticate based on the parameters defined in the custom location for the PyTan User Config

```bash
print_sensors.py --name "Installed Applications" --pytan_user_config /tmp/custom.json
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
Found items:  SensorList, len: 1
Filtered out sourced sensors: 1
Filtered out sensors based on user filters: 1

  * Sensor Name: 'Installed Applications', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Applications
  * Description: List of the applications and versions of those applications installed on the client machine. Example: Mozilla Firefox | 16.0.1
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Manually create a PyTan User Config file in JSON format with only two parameters

  * First we create /tmp/manualcustom.json with just username and password
  * Next we run print_sensors script and supply host on the command line.
  * Note: Command line supplied arguments will always over ride arguments supplied in the PyTan User Config file

 * Content File: /tmp/manualcustom.json

```json
{
    "password": "Tanium2015!", 
    "username": "Administrator"
}
```

```bash
print_sensors.py --name "Installed Applications" --pytan_user_config /tmp/manualcustom.json --host 10.0.1.240
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
Found items:  SensorList, len: 1
Filtered out sourced sensors: 1
Filtered out sensors based on user filters: 1

  * Sensor Name: 'Installed Applications', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Applications
  * Description: List of the applications and versions of those applications installed on the client machine. Example: Mozilla Firefox | 16.0.1
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v2.1.0`, date: Fri Oct  2 16:09:41 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**