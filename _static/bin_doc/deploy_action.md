Deploy Action Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Deploy Action Help](#user-content-deploy-action-help)
  * [Print the help for package](#user-content-print-the-help-for-package)
  * [Print the help for filters](#user-content-print-the-help-for-filters)
  * [Print the help for options](#user-content-print-the-help-for-options)
  * [Deploy an action example 1](#user-content-deploy-an-action-example-1)
  * [Deploy an action example 2](#user-content-deploy-an-action-example-2)
  * [Deploy an action example 3](#user-content-deploy-an-action-example-3)

---------------------------

# Deploy Action Help

  * Deploy an action and save the results as a report format

```bash
deploy_action.py -h
```

```
usage: deploy_action.py [-h] -u USERNAME -p PASSWORD --host HOST [--port PORT]
                        [-l LOGLEVEL] [--run] [--no-results | --results]
                        [-k PACKAGE] [-f ACTION_FILTERS] [-o ACTION_OPTIONS]
                        [--start_seconds_from_now START_SECONDS_FROM_NOW]
                        [--expire_seconds EXPIRE_SECONDS] [--package-help]
                        [--filters-help] [--options-help] [--file REPORT_FILE]
                        [--dir REPORT_DIR]

Deploy an action and save the results as a report format

optional arguments:
  -h, --help            show this help message and exit

Handler Authentication:
  -u USERNAME, --username USERNAME
                        Name of user (default: None)
  -p PASSWORD, --password PASSWORD
                        Password of user (default: None)
  --host HOST           Hostname/ip of SOAP Server (default: None)
  --port PORT           Port to use when connecting to SOAP Server (default:
                        444)

Handler Options:
  -l LOGLEVEL, --loglevel LOGLEVEL
                        Logging level to use, increase for more verbosity
                        (default: 0)

Deploy Action Options:
  --run                 Run the deploy action, if not supplied the deploy
                        action will only ask the question that matches
                        --filter and save the results to csv file for
                        verification (default: False)
  --no-results          Do not get the results after starting the deploy
                        action
  --results             Get the results after starting the deploy action
                        (default) (default: True)
  -k PACKAGE, --package PACKAGE
                        Package to deploy action with, optionally describe
                        parameters, pass --package-help to get a full
                        description (default: )
  -f ACTION_FILTERS, --filter ACTION_FILTERS
                        Filter to deploy action against; pass --filters-helpto
                        get a full description (default: [])
  -o ACTION_OPTIONS, --option ACTION_OPTIONS
                        Options for deploy action filter; pass --options-help
                        to get a full description (default: [])
  --start_seconds_from_now START_SECONDS_FROM_NOW
                        Start the action N seconds from now (default: 1)
  --expire_seconds EXPIRE_SECONDS
                        Expire the action N seconds after it starts, if not
                        supplied the packages own expire_seconds will be used
                        (default: None)
  --package-help        Get the full help for package string (default: False)
  --filters-help        Get the full help for filters strings (default: False)
  --options-help        Get the full help for options strings (default: False)

Report File Options:
  --file REPORT_FILE    File to save report to (will be automatically
                        generated if not supplied) (default: None)
  --dir REPORT_DIR      Directory to save report to (current directory will be
                        used if not supplied) (default: None)
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


# Print the help for package

```bash
deploy_action.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --package-help
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Deploying action:
{
  "action_filters": [], 
  "action_options": [], 
  "expire_seconds": null, 
  "filters_help": false, 
  "get_results": true, 
  "options_help": false, 
  "package": "", 
  "package_help": true, 
  "report_dir": null, 
  "report_file": null, 
  "run": false, 
  "start_seconds_from_now": 1
}

Package Help
============

Supplying package defines what package will be deployed as part of the
action.

A package string is a human string that describes, at a minimum, a
package. It can also optionally define a selector for the package,
and/or parameters for the package. A package must be provided as a string.

Examples for package
---------------------------------

Supplying a package:

    'Distribute Tanium Standard Utilities'

Supplying a package by id:

    'id:1'

Supplying a package by hash:

    'hash:123456789'

Supplying a package by name:

    'name:Distribute Tanium Standard Utilities'

Package Parameters
------------------

Supplying parameters to a package can control the arguments
that are supplied to a package, if that package takes any arguments.

Package parameters must be surrounded with curly braces '{}',
and must have a key and value specified that is separated by
an equals '='. Multiple parameters must be seperated by
a comma ','. The key should match up to a valid parameter key
for the package in question.

If a parameter is supplied and the package doesn't have a
corresponding key name, it will be ignored. If the package has
parameters and a parameter is NOT supplied then an exception
will be raised, printing out the JSON of the missing paramater
for the package in question.

Examples for package with parameters
------------------------------------

Supplying a package with a single parameter '$1':

    'Package With Params{$1=value1}'

Supplying a package with two parameters, '$1' and '$2':

    'Package With Params{$1=value1,$2=value2}'
```

  * Validation Test: notexitcode
    * Valid: **True**
    * Messages: Exit Code is not 0



[TOC](#user-content-toc)


# Print the help for filters

```bash
deploy_action.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --filters-help
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Deploying action:
{
  "action_filters": [], 
  "action_options": [], 
  "expire_seconds": null, 
  "filters_help": true, 
  "get_results": true, 
  "options_help": false, 
  "package": "", 
  "package_help": false, 
  "report_dir": null, 
  "report_file": null, 
  "run": false, 
  "start_seconds_from_now": 1
}

Filters Help
============

Filters are used generously throughout pytan. When used as part of a
sensor string, they control what data is shown for the columns that
the sensor returns. When filters are used for whole question filters,
they control what rows will be returned. They are used by Groups to
define group membership, deploy actions to determine which machines
should have the action deployed to it, and more.

A filter string is a human string that describes, a sensor followed
by ', that FILTER:VALUE', where FILTER is a valid filter string,
and VALUE is the string that you want FILTER to match on.

Valid Filters
-------------

    '<'                      
        Help: Filter for less than VALUE
        Example: "Sensor1, that <:VALUE"

    'less'                   
        Help: Filter for less than VALUE
        Example: "Sensor1, that less:VALUE"

    'lt'                     
        Help: Filter for less than VALUE
        Example: "Sensor1, that lt:VALUE"

    'less than'              
        Help: Filter for less than VALUE
        Example: "Sensor1, that less than:VALUE"

    '!<'                     
        Help: Filter for not less than VALUE
        Example: "Sensor1, that !<:VALUE"

    'notless'                
        Help: Filter for not less than VALUE
        Example: "Sensor1, that notless:VALUE"

    'not less'               
        Help: Filter for not less than VALUE
        Example: "Sensor1, that not less:VALUE"

    'not less than'          
        Help: Filter for not less than VALUE
        Example: "Sensor1, that not less than:VALUE"

    '<='                     
        Help: Filter for less than or equal to VALUE
        Example: "Sensor1, that <=:VALUE"

    'less equal'             
        Help: Filter for less than or equal to VALUE
        Example: "Sensor1, that less equal:VALUE"

    'lessequal'              
        Help: Filter for less than or equal to VALUE
        Example: "Sensor1, that lessequal:VALUE"

    'le'                     
        Help: Filter for less than or equal to VALUE
        Example: "Sensor1, that le:VALUE"

    '!<='                    
        Help: Filter for not less than or equal to VALUE
        Example: "Sensor1, that !<=:VALUE"

    'not less equal'         
        Help: Filter for not less than or equal to VALUE
        Example: "Sensor1, that not less equal:VALUE"

    'not lessequal'          
        Help: Filter for not less than or equal to VALUE
        Example: "Sensor1, that not lessequal:VALUE"

    '>'                      
        Help: Filter for greater than VALUE
        Example: "Sensor1, that >:VALUE"

    'greater'                
        Help: Filter for greater than VALUE
        Example: "Sensor1, that greater:VALUE"

    'gt'                     
        Help: Filter for greater than VALUE
        Example: "Sensor1, that gt:VALUE"

    'greater than'           
        Help: Filter for greater than VALUE
        Example: "Sensor1, that greater than:VALUE"

    '!>'                     
        Help: Filter for not greater than VALUE
        Example: "Sensor1, that !>:VALUE"

    'not greater'            
        Help: Filter for not greater than VALUE
        Example: "Sensor1, that not greater:VALUE"

    'notgreater'             
        Help: Filter for not greater than VALUE
        Example: "Sensor1, that notgreater:VALUE"

    'not greater than'       
        Help: Filter for not greater than VALUE
        Example: "Sensor1, that not greater than:VALUE"

    '=>'                     
        Help: Filter for greater than or equal to VALUE
        Example: "Sensor1, that =>:VALUE"

    'greater equal'          
        Help: Filter for greater than or equal to VALUE
        Example: "Sensor1, that greater equal:VALUE"

    'greaterequal'           
        Help: Filter for greater than or equal to VALUE
        Example: "Sensor1, that greaterequal:VALUE"

    'ge'                     
        Help: Filter for greater than or equal to VALUE
        Example: "Sensor1, that ge:VALUE"

    '!=>'                    
        Help: Filter for not greater than VALUE
        Example: "Sensor1, that !=>:VALUE"

    'not greater equal'      
        Help: Filter for not greater than VALUE
        Example: "Sensor1, that not greater equal:VALUE"

    'notgreaterequal'        
        Help: Filter for not greater than VALUE
        Example: "Sensor1, that notgreaterequal:VALUE"

    '='                      
        Help: Filter for equals to VALUE
        Example: "Sensor1, that =:VALUE"

    'equal'                  
        Help: Filter for equals to VALUE
        Example: "Sensor1, that equal:VALUE"

    'equals'                 
        Help: Filter for equals to VALUE
        Example: "Sensor1, that equals:VALUE"

    'eq'                     
        Help: Filter for equals to VALUE
        Example: "Sensor1, that eq:VALUE"

    '!='                     
        Help: Filter for not equals to VALUE
        Example: "Sensor1, that !=:VALUE"

    'not equal'              
        Help: Filter for not equals to VALUE
        Example: "Sensor1, that not equal:VALUE"

    'notequal'               
        Help: Filter for not equals to VALUE
        Example: "Sensor1, that notequal:VALUE"

    'not equals'             
        Help: Filter for not equals to VALUE
        Example: "Sensor1, that not equals:VALUE"

    'notequals'              
        Help: Filter for not equals to VALUE
        Example: "Sensor1, that notequals:VALUE"

    'ne'                     
        Help: Filter for not equals to VALUE
        Example: "Sensor1, that ne:VALUE"

    'contains'               
        Help: Filter for contains VALUE (adds .* before and after VALUE)
        Example: "Sensor1, that contains:VALUE"

    'does not contain'       
        Help: Filter for does not contain VALUE (adds .* before and after VALUE)
        Example: "Sensor1, that does not contain:VALUE"

    'doesnotcontain'         
        Help: Filter for does not contain VALUE (adds .* before and after VALUE)
        Example: "Sensor1, that doesnotcontain:VALUE"

    'not contains'           
        Help: Filter for does not contain VALUE (adds .* before and after VALUE)
        Example: "Sensor1, that not contains:VALUE"

    'notcontains'            
        Help: Filter for does not contain VALUE (adds .* before and after VALUE)
        Example: "Sensor1, that notcontains:VALUE"

    'starts with'            
        Help: Filter for starts with VALUE (adds .* after VALUE)
        Example: "Sensor1, that starts with:VALUE"

    'startswith'             
        Help: Filter for starts with VALUE (adds .* after VALUE)
        Example: "Sensor1, that startswith:VALUE"

    'does not start with'    
        Help: Filter for does not start with VALUE (adds .* after VALUE)
        Example: "Sensor1, that does not start with:VALUE"

    'doesnotstartwith'       
        Help: Filter for does not start with VALUE (adds .* after VALUE)
        Example: "Sensor1, that doesnotstartwith:VALUE"

    'not starts with'        
        Help: Filter for does not start with VALUE (adds .* after VALUE)
        Example: "Sensor1, that not starts with:VALUE"

    'notstartswith'          
        Help: Filter for does not start with VALUE (adds .* after VALUE)
        Example: "Sensor1, that notstartswith:VALUE"

    'ends with'              
        Help: Filter for ends with VALUE (adds .* before VALUE)
        Example: "Sensor1, that ends with:VALUE"

    'endswith'               
        Help: Filter for ends with VALUE (adds .* before VALUE)
        Example: "Sensor1, that endswith:VALUE"

    'does not end with'      
        Help: Filter for does bit end with VALUE (adds .* before VALUE)
        Example: "Sensor1, that does not end with:VALUE"

    'doesnotendwith'         
        Help: Filter for does bit end with VALUE (adds .* before VALUE)
        Example: "Sensor1, that doesnotendwith:VALUE"

    'not ends with'          
        Help: Filter for does bit end with VALUE (adds .* before VALUE)
        Example: "Sensor1, that not ends with:VALUE"

    'notstartswith'          
        Help: Filter for does bit end with VALUE (adds .* before VALUE)
        Example: "Sensor1, that notstartswith:VALUE"

    'is not'                 
        Help: Filter for non regular expression match for VALUE
        Example: "Sensor1, that is not:VALUE"

    'not regex'              
        Help: Filter for non regular expression match for VALUE
        Example: "Sensor1, that not regex:VALUE"

    'notregex'               
        Help: Filter for non regular expression match for VALUE
        Example: "Sensor1, that notregex:VALUE"

    'not regex match'        
        Help: Filter for non regular expression match for VALUE
        Example: "Sensor1, that not regex match:VALUE"

    'notregexmatch'          
        Help: Filter for non regular expression match for VALUE
        Example: "Sensor1, that notregexmatch:VALUE"

    'nre'                    
        Help: Filter for non regular expression match for VALUE
        Example: "Sensor1, that nre:VALUE"

    'is'                     
        Help: Filter for regular expression match for VALUE
        Example: "Sensor1, that is:VALUE"

    'regex'                  
        Help: Filter for regular expression match for VALUE
        Example: "Sensor1, that regex:VALUE"

    'regex match'            
        Help: Filter for regular expression match for VALUE
        Example: "Sensor1, that regex match:VALUE"

    'regexmatch'             
        Help: Filter for regular expression match for VALUE
        Example: "Sensor1, that regexmatch:VALUE"

    're'                     
        Help: Filter for regular expression match for VALUE
        Example: "Sensor1, that re:VALUE"
```

  * Validation Test: notexitcode
    * Valid: **True**
    * Messages: Exit Code is not 0



[TOC](#user-content-toc)


# Print the help for options

```bash
deploy_action.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --options-help
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Deploying action:
{
  "action_filters": [], 
  "action_options": [], 
  "expire_seconds": null, 
  "filters_help": false, 
  "get_results": true, 
  "options_help": true, 
  "package": "", 
  "package_help": false, 
  "report_dir": null, 
  "report_file": null, 
  "run": false, 
  "start_seconds_from_now": 1
}

Options Help
============

Options are used for controlling how filters act. When options are
used as part of a sensor string, they change how the filters
supplied as part of that sensor operate. When options are used for
whole question options, they change how all of the question filters
operate.

When options are supplied for a sensor string, they must be
supplied as ', opt:OPTION' or ', opt:OPTION:VALUE' for options
that require a value.

When options are supplied for question options, they must be
supplied as 'OPTION' or 'OPTION:VALUE' for options that require
a value.

Options can be used on 'filter' or 'group', where 'group' pertains
to group filters or question filters. All 'filter' options are also
applicable to 'group' for question options.

Valid Options
-------------

    'ignore_case'            
        Help: Make the filter do a case insensitive match
        Usable on: filter
        Example for sensor: "Sensor1, opt:ignore_case"
        Example for question: "ignore_case"

    'match_case'             
        Help: Make the filter do a case sensitive match
        Usable on: filter
        Example for sensor: "Sensor1, opt:match_case"
        Example for question: "match_case"

    'match_any_value'        
        Help: Make the filter match any value
        Usable on: filter
        Example for sensor: "Sensor1, opt:match_any_value"
        Example for question: "match_any_value"

    'match_all_values'       
        Help: Make the filter match all values
        Usable on: filter
        Example for sensor: "Sensor1, opt:match_all_values"
        Example for question: "match_all_values"

    'max_data_age'           
        Help: Re-fetch cached values older than N seconds
        Usable on: filter
        VALUE description and type: seconds, <type 'int'>
        Example for sensor: "Sensor1, opt:max_data_age:seconds"
        Example for question: "max_data_age:seconds"

    'value_type'             
        Help: Make the filter consider the value type as VALUE_TYPE
        Usable on: filter
        VALUE description and type: value_type, <type 'str'>
        Example for sensor: "Sensor1, opt:value_type:value_type"
        Example for question: "value_type:value_type"

    'and'                    
        Help: Use 'and' for all of the filters supplied
        Usable on: group
        Example for sensor: "Sensor1, opt:and"
        Example for question: "and"

    'or'                     
        Help: Use 'or' for all of the filters supplied
        Usable on: group
        Example for sensor: "Sensor1, opt:or"
        Example for question: "or"
```

  * Validation Test: notexitcode
    * Valid: **True**
    * Messages: Exit Code is not 0



[TOC](#user-content-toc)


# Deploy an action example 1

  * Deploys an action using the package Distribute Tanium Standard Utilities
  * Since --run was not supplied, the results of the question for the filters of this action will be written to a CSV file for verification, and the deploy action will NOT be run

```bash
deploy_action.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --package "Distribute Tanium Standard Utilities" --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv"
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Deploying action:
{
  "action_filters": [], 
  "action_options": [], 
  "expire_seconds": null, 
  "filters_help": false, 
  "get_results": true, 
  "options_help": false, 
  "package": "Distribute Tanium Standard Utilities", 
  "package_help": false, 
  "report_dir": null, 
  "report_file": "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv", 
  "run": false, 
  "start_seconds_from_now": 1
}
2014-12-08 14:59:54,534 INFO     question_progress: Results 0% (Get Computer Name and Online = "True" from all machines)
2014-12-08 14:59:59,551 INFO     question_progress: Results 50% (Get Computer Name and Online = "True" from all machines)
2014-12-08 15:00:04,571 INFO     question_progress: Results 100% (Get Computer Name and Online = "True" from all machines)
'Run' is not True!!
View and verify the contents of /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/VERIFY_BEFORE_DEPLOY_ACTION_out.csv (length: 159 bytes)
Re-run this deploy action with run=True after verifying
```

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/VERIFY_BEFORE_DEPLOY_ACTION_out.csv exists, content:

```
Computer Name,Online
Casus-Belli.local,True
jtanium1.localdomain,True
ubuntu.(none),True
localhost.(none),True
Jims-Mac.local,True
WIN-A12SC6N6T7Q,True
```

  * Validation Test: notexitcode
    * Valid: **True**
    * Messages: Exit Code is not 0



[TOC](#user-content-toc)


# Deploy an action example 2

  * Deploys an action using the package Distribute Tanium Standard Utilities

```bash
deploy_action.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --package "Distribute Tanium Standard Utilities" --run --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv"
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Deploying action:
{
  "action_filters": [], 
  "action_options": [], 
  "expire_seconds": null, 
  "filters_help": false, 
  "get_results": true, 
  "options_help": false, 
  "package": "Distribute Tanium Standard Utilities", 
  "package_help": false, 
  "report_dir": null, 
  "report_file": "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv", 
  "run": true, 
  "start_seconds_from_now": 1
}
2014-12-08 15:00:04,777 INFO     question_progress: Results 0% (Get Online = "True" from all machines)
2014-12-08 15:00:09,793 INFO     question_progress: Results 0% (Get Online = "True" from all machines)
2014-12-08 15:00:14,809 INFO     question_progress: Results 100% (Get Online = "True" from all machines)
2014-12-08 15:00:14,873 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:15,903 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:16,930 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:17,961 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:18,991 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:20,026 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:21,056 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:22,085 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:23,114 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:24,143 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:25,171 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:26,216 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:27,246 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:28,275 INFO     action_progress: Action Results Passed: 67% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:29,304 INFO     action_progress: Action Results Passed: 67% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:30,330 INFO     action_progress: Action Results Passed: 67% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:31,358 INFO     action_progress: Action Results Passed: 67% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:32,387 INFO     action_progress: Action Results Passed: 67% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:33,415 INFO     action_progress: Action Results Passed: 83% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:34,443 INFO     action_progress: Action Results Passed: 100% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:34,472 INFO     action_progress: Action Results Completed: 100% (API Deploy Distribute Tanium Standard Utilities)
2014-12-08 15:00:34,472 INFO     action_progress: API Deploy Distribute Tanium Standard Utilities Result Counts:
	Running Count: 0
	Success Count: 6
	Failed Count: 0
	Unknown Count: 0
	Finished Count: 6
	Total Count: 6
	Finished Count must equal: 6
++ Deployed Action 'API Deploy Distribute Tanium Standard Utilities' ID: 26
++ Command used in Action: 'cmd /c cscript install-standard-utils.vbs "Tools\\StdUtils"'
++ Deploy action progress check results:
API Deploy Distribute Tanium Standard Utilities Result Counts:
	Running Count: 0
	Success Count: 6
	Failed Count: 0
	Unknown Count: 0
	Finished Count: 6
	Total Count: 6
	Finished Count must equal: 6
++ Deploy results written to '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv' with 222 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv exists, content:

```
Action Statuses,Computer Name
26:Completed.,Casus-Belli.local
26:Completed.,jtanium1.localdomain
26:Completed.,ubuntu.(none)
26:Completed.,localhost.(none)
26:Completed.,Jims-Mac.local
26:Completed.,WIN-A12SC6N6T7Q
```



[TOC](#user-content-toc)


# Deploy an action example 3

  * Deploys an action using the package "Custom Tagging - Add Tags", passing in a parameter for the tag to be added
  * Uses a filter to only deploy the action agains machines that match .*Windows.* for the Operating System sensor

```bash
deploy_action.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --package "Custom Tagging - Add Tags{\$1=new_tag}" --filter "Operating System, that contains:Windows" --run --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv"
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Deploying action:
{
  "action_filters": [
    "Operating System, that contains:Windows"
  ], 
  "action_options": [], 
  "expire_seconds": null, 
  "filters_help": false, 
  "get_results": true, 
  "options_help": false, 
  "package": "Custom Tagging - Add Tags{$1=new_tag}", 
  "package_help": false, 
  "report_dir": null, 
  "report_file": "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv", 
  "run": true, 
  "start_seconds_from_now": 1
}
2014-12-08 15:00:34,691 INFO     question_progress: Results 0% (Get Online = "True" from all machines where Operating System contains "Windows")
2014-12-08 15:00:39,709 INFO     question_progress: Results 50% (Get Online = "True" from all machines where Operating System contains "Windows")
2014-12-08 15:00:44,726 INFO     question_progress: Results 100% (Get Online = "True" from all machines where Operating System contains "Windows")
2014-12-08 15:00:44,802 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:00:45,829 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:00:46,859 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:00:47,892 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:00:48,920 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:00:49,947 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:00:50,974 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:00:52,008 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:00:53,108 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:00:54,135 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:00:55,165 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:00:56,194 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:00:57,222 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:00:58,247 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:00:59,276 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:00,306 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:01,335 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:02,360 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:03,388 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:04,421 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:05,450 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:06,475 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:07,506 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:08,532 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:09,559 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:10,586 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:11,616 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:12,653 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:13,698 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:14,726 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:15,753 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:16,779 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:17,806 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:18,835 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:19,864 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:20,898 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:21,931 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:22,962 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:23,992 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:25,022 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:26,051 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:27,087 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:28,114 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:29,142 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:30,171 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:31,197 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:32,225 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:33,253 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:34,282 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:35,310 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:36,339 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:37,368 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:38,402 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:39,428 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:40,456 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:41,485 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:42,514 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:43,540 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:44,570 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:45,597 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:46,623 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:47,654 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:48,691 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:49,718 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:50,751 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:51,782 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:52,814 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:53,844 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:54,874 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:55,902 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:56,929 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:57,957 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:01:58,984 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:00,014 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:01,044 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:02,072 INFO     action_progress: Action Results Passed: 50% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:03,102 INFO     action_progress: Action Results Passed: 50% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:04,129 INFO     action_progress: Action Results Passed: 50% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:05,157 INFO     action_progress: Action Results Passed: 50% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:06,190 INFO     action_progress: Action Results Passed: 50% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:07,219 INFO     action_progress: Action Results Passed: 50% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:08,246 INFO     action_progress: Action Results Passed: 50% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:09,280 INFO     action_progress: Action Results Passed: 50% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:10,307 INFO     action_progress: Action Results Passed: 50% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:11,334 INFO     action_progress: Action Results Passed: 50% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:12,367 INFO     action_progress: Action Results Passed: 50% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:13,399 INFO     action_progress: Action Results Passed: 50% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:14,429 INFO     action_progress: Action Results Passed: 50% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:15,459 INFO     action_progress: Action Results Passed: 50% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:16,490 INFO     action_progress: Action Results Passed: 50% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:17,517 INFO     action_progress: Action Results Passed: 100% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:17,542 INFO     action_progress: Action Results Completed: 100% (API Deploy Custom Tagging - Add Tags)
2014-12-08 15:02:17,542 INFO     action_progress: API Deploy Custom Tagging - Add Tags Result Counts:
	Running Count: 0
	Success Count: 2
	Failed Count: 0
	Unknown Count: 0
	Finished Count: 2
	Total Count: 2
	Finished Count must equal: 2
++ Deployed Action 'API Deploy Custom Tagging - Add Tags' ID: 27
++ Command used in Action: 'cmd /c cscript //T:60 add-tags.vbs "new%5ftag"'
++ Deploy action progress check results:
API Deploy Custom Tagging - Add Tags Result Counts:
	Running Count: 0
	Success Count: 2
	Failed Count: 0
	Unknown Count: 0
	Finished Count: 2
	Total Count: 2
	Finished Count must equal: 2
++ Deploy results written to '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv' with 98 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv exists, content:

```
Action Statuses,Computer Name
27:Completed.,jtanium1.localdomain
27:Completed.,WIN-A12SC6N6T7Q
```



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Mon Dec  8 15:02:17 2014 EST, Contact info: **Jim Olsen <jim.olsen@tanium.com>**