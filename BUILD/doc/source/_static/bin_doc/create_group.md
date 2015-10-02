Create Group Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Help for Create Group](#user-content-help-for-create-group)
  * [Delete the group we want to create to ensure it does not pre-exist](#user-content-delete-the-group-we-want-to-create-to-ensure-it-does-not-pre-exist)
  * [Create a new group](#user-content-create-a-new-group)
  * [Delete the recently created group](#user-content-delete-the-recently-created-group)
  * [Print the help for filters](#user-content-print-the-help-for-filters)
  * [Print the help for options](#user-content-print-the-help-for-options)

---------------------------

# Help for Create Group

  * Print the help for create_group.py
  * All scripts in bin/ will supply help if -h is on the command line
  * If passing in a parameter with a space or a special character, you need to surround it with quotes properly. On Windows this means double quotes. On Linux/Mac, this means single or double quotes, depending on what kind of character escaping you need.
  * If running this script on Linux or Mac, use the python scripts directly as the bin/create_group.py
  * If running this script on Windows, use the batch script in the winbin/create_group.bat so that python is called correctly.

```bash
create_group.py -h
```

```
usage: create_group.py [-h] [-u USERNAME] [-p PASSWORD]
                       [--session_id SESSION_ID] [--host HOST] [--port PORT]
                       [-l LOGLEVEL] [--debugformat] [--debug_method_locals]
                       [--record_all_requests] [--stats_loop_enabled]
                       [--http_auth_retry]
                       [--http_retry_count HTTP_RETRY_COUNT]
                       [--pytan_user_config PYTAN_USER_CONFIG]
                       [--force_server_version FORCE_SERVER_VERSION] -n
                       GROUPNAME [-f FILTERS] [-o FILTER_OPTIONS]
                       [--filters-help] [--options-help]

Create a group object from command line arguments

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

Create Group Options:
  -n GROUPNAME, --name GROUPNAME
                        Name of group to create (default: None)
  -f FILTERS, --filter FILTERS
                        Filters to use for group, supply --filters-help to see
                        filter help (default: [])
  -o FILTER_OPTIONS, --option FILTER_OPTIONS
                        Filter options to use for group, supply --options-help
                        to see options help (default: [])
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


# Delete the group we want to create to ensure it does not pre-exist

  * Delete the group named All Windows Computers CMDLINE TEST GROUP
  * This may or may not fail -- thats fine!

```bash
bin/delete_group.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --name "All Windows Computers CMDLINE TEST GROUP"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301


Error occurred: No results found searching for Group, name: 'All Windows Computers CMDLINE TEST GROUP' (error: Response command GroupNotFound does not match request command GetObject)!!
```

```STDERR
Traceback (most recent call last):
  File "/Users/jolsen/gh/pytan/lib/pytan/binsupport.py", line 2082, in process_delete_object_args
    response = handler.delete(**obj_grp_args)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1923, in delete
    objs_to_del = self.get(objtype=objtype, pytan_help=h, **clean_kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 2277, in get
    return self._get_multi(obj_map=obj_map, **clean_kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 2461, in _get_multi
    found = self._find(obj=api_obj_multi, **clean_kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 2406, in _find
    raise pytan.exceptions.HandlerError(err(search_str, e))
HandlerError: No results found searching for Group, name: 'All Windows Computers CMDLINE TEST GROUP' (error: Response command GroupNotFound does not match request command GetObject)!!
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Create a new group

  * Create a group named All Windows Computers CMDLINE TEST GROUP
  * Supply a filter that limits the group members to machines that match .*Windows.* for the Operating System sensor
  * Supply a filter that limits the group members to machines that do not equal 10.10.10.10 for the IP Address sensor
  * Supply two options, one to AND the filters supplied, and another to ignore the case while matching the filters

```bash
bin/create_group.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --name "All Windows Computers CMDLINE TEST GROUP" -f "Operating System, that contains:Windows" -f "IP Address, that not equals:10.10.10.10" -o "and" -o "ignore_case"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
New group 'All Windows Computers CMDLINE TEST GROUP' created with ID 502, filter text: ' ( Operating System containing "Windows" and any IP Address != "10.10.10.10" )'
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Delete the recently created group

  * Delete the group named All Windows Computers CMDLINE TEST GROUP

```bash
bin/delete_group.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --name "All Windows Computers CMDLINE TEST GROUP"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
Deleted item:  Group, id: 502
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Print the help for filters

```bash
bin/create_group.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --filters-help
```

```
usage: create_group.py [-h] [-u USERNAME] [-p PASSWORD]
                       [--session_id SESSION_ID] [--host HOST] [--port PORT]
                       [-l LOGLEVEL] [--debugformat] [--debug_method_locals]
                       [--record_all_requests] [--stats_loop_enabled]
                       [--http_auth_retry]
                       [--http_retry_count HTTP_RETRY_COUNT]
                       [--pytan_user_config PYTAN_USER_CONFIG]
                       [--force_server_version FORCE_SERVER_VERSION] -n
                       GROUPNAME [-f FILTERS] [-o FILTER_OPTIONS]
                       [--filters-help] [--options-help]

Create a group object from command line arguments

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

Create Group Options:
  -n GROUPNAME, --name GROUPNAME
                        Name of group to create (default: None)
  -f FILTERS, --filter FILTERS
                        Filters to use for group, supply --filters-help to see
                        filter help (default: [])
  -o FILTER_OPTIONS, --option FILTER_OPTIONS
                        Filter options to use for group, supply --options-help
                        to see options help (default: [])
  --filters-help        Get the full help for filters strings (default: False)
  --options-help        Get the full help for options strings (default: False)
ERROR:create_group:argument -n/--name is required
```

  * Validation Test: notexitcode
    * Valid: **True**
    * Messages: Exit Code is not 0



[TOC](#user-content-toc)


# Print the help for options

```bash
bin/create_group.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --options-help
```

```
usage: create_group.py [-h] [-u USERNAME] [-p PASSWORD]
                       [--session_id SESSION_ID] [--host HOST] [--port PORT]
                       [-l LOGLEVEL] [--debugformat] [--debug_method_locals]
                       [--record_all_requests] [--stats_loop_enabled]
                       [--http_auth_retry]
                       [--http_retry_count HTTP_RETRY_COUNT]
                       [--pytan_user_config PYTAN_USER_CONFIG]
                       [--force_server_version FORCE_SERVER_VERSION] -n
                       GROUPNAME [-f FILTERS] [-o FILTER_OPTIONS]
                       [--filters-help] [--options-help]

Create a group object from command line arguments

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

Create Group Options:
  -n GROUPNAME, --name GROUPNAME
                        Name of group to create (default: None)
  -f FILTERS, --filter FILTERS
                        Filters to use for group, supply --filters-help to see
                        filter help (default: [])
  -o FILTER_OPTIONS, --option FILTER_OPTIONS
                        Filter options to use for group, supply --options-help
                        to see options help (default: [])
  --filters-help        Get the full help for filters strings (default: False)
  --options-help        Get the full help for options strings (default: False)
ERROR:create_group:argument -n/--name is required
```

  * Validation Test: notexitcode
    * Valid: **True**
    * Messages: Exit Code is not 0



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v2.1.0`, date: Fri Oct  2 16:06:16 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**