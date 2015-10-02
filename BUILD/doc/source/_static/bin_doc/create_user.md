Create User Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Help for Create User](#user-content-help-for-create-user)
  * [Example 1: Delete the user we want to create to ensure it does not pre-exist](#user-content-example-1:-delete-the-user-we-want-to-create-to-ensure-it-does-not-pre-exist)
  * [Example 1: Create a new user](#user-content-example-1:-create-a-new-user)
  * [Example 1: Delete the recently created user](#user-content-example-1:-delete-the-recently-created-user)
  * [Example 2: Delete the user we want to create to ensure it does not pre-exist](#user-content-example-2:-delete-the-user-we-want-to-create-to-ensure-it-does-not-pre-exist)
  * [Example 2: Create a new user with a group specificied](#user-content-example-2:-create-a-new-user-with-a-group-specificied)
  * [Example 2: Delete the recently created user](#user-content-example-2:-delete-the-recently-created-user)

---------------------------

# Help for Create User

  * Print the help for create_user.py
  * All scripts in bin/ will supply help if -h is on the command line
  * If passing in a parameter with a space or a special character, you need to surround it with quotes properly. On Windows this means double quotes. On Linux/Mac, this means single or double quotes, depending on what kind of character escaping you need.
  * If running this script on Linux or Mac, use the python scripts directly as the bin/create_user.py
  * If running this script on Windows, use the batch script in the winbin/create_user.bat so that python is called correctly.

```bash
create_user.py -h
```

```
usage: create_user.py [-h] [-u USERNAME] [-p PASSWORD]
                      [--session_id SESSION_ID] [--host HOST] [--port PORT]
                      [-l LOGLEVEL] [--debugformat] [--debug_method_locals]
                      [--record_all_requests] [--stats_loop_enabled]
                      [--http_auth_retry]
                      [--http_retry_count HTTP_RETRY_COUNT]
                      [--pytan_user_config PYTAN_USER_CONFIG]
                      [--force_server_version FORCE_SERVER_VERSION] -n NAME
                      [-rn ROLENAME] [-ri ROLEID] [-g GROUP]
                      [-prop PROPERTIES PROPERTIES]

Create a user object from command line arguments

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

Create User Options:
  -n NAME, --name NAME  Name of user to create (default: None)
  -rn ROLENAME, --rolename ROLENAME
                        Name of role to assign to new user (default: [])
  -ri ROLEID, --roleid ROLEID
                        ID of role to assign to new user (default: [])
  -g GROUP, --group GROUP
                        Name of group to assign to user (default: )
  -prop PROPERTIES PROPERTIES, --property PROPERTIES PROPERTIES
                        Property name and value to assign to user (default:
                        [])
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Example 1: Delete the user we want to create to ensure it does not pre-exist

  * Delete the user named "CMDLINE TEST user"
  * This may or may not fail -- thats fine!

```bash
bin/delete_user.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --name "CMDLINE TEST user"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301


Error occurred: No results found searching for user with {'id': [], 'name': ['CMDLINE TEST user']}!!
```

```STDERR
Traceback (most recent call last):
  File "/Users/jolsen/gh/pytan/lib/pytan/binsupport.py", line 2082, in process_delete_object_args
    response = handler.delete(**obj_grp_args)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1923, in delete
    objs_to_del = self.get(objtype=objtype, pytan_help=h, **clean_kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 2264, in get
    raise pytan.exceptions.HandlerError(err(objtype, err_args))
HandlerError: No results found searching for user with {'id': [], 'name': ['CMDLINE TEST user']}!!
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Example 1: Create a new user

  * Create a user named CMDLINE TEST user
  * Assign the Administrator role to the new user
  * Create a property named property name with the value property value on the new user

```bash
bin/create_user.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --name "CMDLINE TEST user" --rolename "Administrator" --property "property name" "property value"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
New user 'CMDLINE TEST user' created with ID 57, roles: 'Administrator', group id: 0
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Example 1: Delete the recently created user

  * Delete the user by name

```bash
bin/delete_user.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --name "CMDLINE TEST user"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
Deleted item:  User, name: 'CMDLINE TEST user', id: 57
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Example 2: Delete the user we want to create to ensure it does not pre-exist

  * Delete the user named "CMDLINE TEST user"
  * This may or may not fail -- thats fine!

```bash
bin/delete_user.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --name "CMDLINE TEST user"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301


Error occurred: No results found searching for user with {'id': [], 'name': ['CMDLINE TEST user']}!!
```

```STDERR
Traceback (most recent call last):
  File "/Users/jolsen/gh/pytan/lib/pytan/binsupport.py", line 2082, in process_delete_object_args
    response = handler.delete(**obj_grp_args)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1923, in delete
    objs_to_del = self.get(objtype=objtype, pytan_help=h, **clean_kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 2264, in get
    raise pytan.exceptions.HandlerError(err(objtype, err_args))
HandlerError: No results found searching for user with {'id': [], 'name': ['CMDLINE TEST user']}!!
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Example 2: Create a new user with a group specificied

  * Create a user named CMDLINE TEST user and allow it only access to users in the "All Computers" group name
  * Assign the Administrator role to the new user
  * Create a property named property name with the value property value on the new user

```bash
bin/create_user.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --name "CMDLINE TEST user" --rolename "Administrator" --property "property name" "property value" -g "All Computers"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
New user 'CMDLINE TEST user' created with ID 58, roles: 'Administrator', group id: 62
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Example 2: Delete the recently created user

  * Delete the user by name

```bash
bin/delete_user.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --name "CMDLINE TEST user"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
Deleted item:  User, name: 'CMDLINE TEST user', id: 58
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v2.1.0`, date: Fri Oct  2 16:06:28 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**