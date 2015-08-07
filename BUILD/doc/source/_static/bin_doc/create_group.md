Create Group Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Create Group Help](#user-content-create-group-help)
  * [Print the help for filters](#user-content-print-the-help-for-filters)
  * [Print the help for options](#user-content-print-the-help-for-options)
  * [Create a new group](#user-content-create-a-new-group)
  * [Delete the recently created group](#user-content-delete-the-recently-created-group)

---------------------------

# Create Group Help

  * Create a group object from command line arguments

```bash
create_group.py -h
```

```
usage: create_group.py [-h] [-u USERNAME] [-p PASSWORD] [--host HOST]
                       [--port PORT] [-l LOGLEVEL] -n NAME [-f FILTERS]
                       [-o FILTER_OPTIONS] [--filters-help] [--options-help]

Create a group object from command line arguments

optional arguments:
  -h, --help            show this help message and exit

Handler Authentication:
  -u USERNAME, --username USERNAME
                        Name of user (default: None)
  -p PASSWORD, --password PASSWORD
                        Password of user (default: None)
  --host HOST           Hostname/ip of SOAP Server (default: None)
  --port PORT           Port to use when connecting to SOAP Server (default:
                        443)

Handler Options:
  -l LOGLEVEL, --loglevel LOGLEVEL
                        Logging level to use, increase for more verbosity
                        (default: 0)

Create Group Options:
  -n NAME, --name NAME  Name of group to create (default: None)
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



[TOC](#user-content-toc)


# Print the help for filters

```bash
create_group.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --filters-help
```

```
usage: create_group.py [-h] [-u USERNAME] [-p PASSWORD] [--host HOST]
                       [--port PORT] [-l LOGLEVEL] -n NAME [-f FILTERS]
                       [-o FILTER_OPTIONS] [--filters-help] [--options-help]

Create a group object from command line arguments

optional arguments:
  -h, --help            show this help message and exit

Handler Authentication:
  -u USERNAME, --username USERNAME
                        Name of user (default: None)
  -p PASSWORD, --password PASSWORD
                        Password of user (default: None)
  --host HOST           Hostname/ip of SOAP Server (default: None)
  --port PORT           Port to use when connecting to SOAP Server (default:
                        443)

Handler Options:
  -l LOGLEVEL, --loglevel LOGLEVEL
                        Logging level to use, increase for more verbosity
                        (default: 0)

Create Group Options:
  -n NAME, --name NAME  Name of group to create (default: None)
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
create_group.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --options-help
```

```
usage: create_group.py [-h] [-u USERNAME] [-p PASSWORD] [--host HOST]
                       [--port PORT] [-l LOGLEVEL] -n NAME [-f FILTERS]
                       [-o FILTER_OPTIONS] [--filters-help] [--options-help]

Create a group object from command line arguments

optional arguments:
  -h, --help            show this help message and exit

Handler Authentication:
  -u USERNAME, --username USERNAME
                        Name of user (default: None)
  -p PASSWORD, --password PASSWORD
                        Password of user (default: None)
  --host HOST           Hostname/ip of SOAP Server (default: None)
  --port PORT           Port to use when connecting to SOAP Server (default:
                        443)

Handler Options:
  -l LOGLEVEL, --loglevel LOGLEVEL
                        Logging level to use, increase for more verbosity
                        (default: 0)

Create Group Options:
  -n NAME, --name NAME  Name of group to create (default: None)
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


# Create a new group

  * Create a group named All Windows Computers CMDLINE TEST GROUP
  * Supply a filter that limits the group members to machines that match .*Windows.* for the Operating System sensor
  * Supply a filter that limits the group members to machines that do not equal 10.10.10.10 for the IP Address sensor
  * Supply two options, one to AND the filters supplied, and another to ignore the case while matching the filters

```bash
create_group.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --name "All Windows Computers CMDLINE TEST GROUP" -f "Operating System, that contains:Windows" -f "IP Address, that not equals:10.10.10.10" -o "and" -o "ignore_case"
```

```
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
New group 'All Windows Computers CMDLINE TEST GROUP' created with ID 184, filter text: ' ( Operating System containing "Windows" and any IP Address != "10.10.10.10" )'
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


# Delete the recently created group

  * Delete the group named All Windows Computers CMDLINE TEST GROUP

```bash
delete_group.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --name "All Windows Computers CMDLINE TEST GROUP"
```

```
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
Deleted item:  Group, id: 184
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Fri Aug  7 15:27:34 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**