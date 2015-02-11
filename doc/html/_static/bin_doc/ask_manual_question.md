Ask Manual Question Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Ask Manual Question Help](#user-content-ask-manual-question-help)
  * [Print the help for sensors](#user-content-print-the-help-for-sensors)
  * [Print the help for filters](#user-content-print-the-help-for-filters)
  * [Print the help for options](#user-content-print-the-help-for-options)
  * [Ask a question example 1](#user-content-ask-a-question-example-1)
  * [Ask a question example 2](#user-content-ask-a-question-example-2)
  * [Ask a question example 3](#user-content-ask-a-question-example-3)
  * [Ask a question example 4](#user-content-ask-a-question-example-4)
  * [Ask a question example 5](#user-content-ask-a-question-example-5)
  * [Ask a question example 6](#user-content-ask-a-question-example-6)
  * [Ask a question example 7](#user-content-ask-a-question-example-7)

---------------------------

# Ask Manual Question Help

  * Ask a manual question and save the results as a report format

```bash
ask_manual_question.py -h
```

```
usage: ask_manual_question.py [-h] [-u USERNAME] [-p PASSWORD] [--host HOST]
                              [--port PORT] [-l LOGLEVEL] [-s SENSORS]
                              [-f QUESTION_FILTERS] [-o QUESTION_OPTIONS]
                              [--sensors-help] [--filters-help]
                              [--options-help] [--no-results | --results]
                              [--file REPORT_FILE] [--dir REPORT_DIR]
                              {csv,json} ...

Ask a manual question and save the results as a report format

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

Manual Question Options:
  -s SENSORS, --sensor SENSORS
                        Sensor, optionally describe parameters, options, and a
                        filter; pass --sensors-help to get a full description
                        (default: [])
  -f QUESTION_FILTERS, --filter QUESTION_FILTERS
                        Whole question filter; pass --filters-help to get a
                        full description (default: [])
  -o QUESTION_OPTIONS, --option QUESTION_OPTIONS
                        Whole question option; pass --options-help to get a
                        full description (default: [])
  --sensors-help        Get the full help for sensor strings (default: False)
  --filters-help        Get the full help for filters strings (default: False)
  --options-help        Get the full help for options strings (default: False)
  --no-results          Do not get the results after asking the quesiton
                        action
  --results             Get the results after asking the quesiton (default)
                        (default: True)

Report File Options:
  --file REPORT_FILE    File to save report to (will be automatically
                        generated if not supplied) (default: None)
  --dir REPORT_DIR      Directory to save report to (current directory will be
                        used if not supplied) (default: None)

Export Formats:
  {csv,json}            Export Format choices
    csv                 Produce a CSV report, supply "csv -h" to see CSV
                        options
    json                Produce a JSON report, supply "json -h" to see JSON
                        options

usage: ask_manual_question.py csv [-h]
                                  [--sort HEADER_SORT | --no-sort | --auto_sort]
                                  [--add-sensor | --no-add-sensor]
                                  [--add-type | --no-add-type]
                                  [--expand-columns | --no-columns]

CSV Export Options

optional arguments:
  -h, --help          show this help message and exit
  --sort HEADER_SORT  Sort headers by given names (default: [])
  --no-sort           Do not sort the headers at all
  --auto_sort         Sort the headers with a basic alphanumeric sort
                      (default)
  --add-sensor        Add the sensor names to each header
  --no-add-sensor     Do not add the sensor names to each header (default)
  --add-type          Add the result type to each header
  --no-add-type       Do not add the result type to each header (default)
  --expand-columns    Expand multi-line cells into their own rows that have
                      sensor correlated columns in the new rows
  --no-columns        Do not add expand multi-line cells into their own rows
                      (default)

usage: ask_manual_question.py json [-h]

JSON Export Options

optional arguments:
  -h, --help  show this help message and exit
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


# Print the help for sensors

```bash
ask_manual_question.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --sensors-help csv
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Asking manual question:
{
  "filters_help": false, 
  "get_results": true, 
  "options_help": false, 
  "question_filters": [], 
  "question_options": [], 
  "sensors": [], 
  "sensors_help": true
}

Sensors Help
============

Supplying sensors controls what columns will be showed when you ask a
question.

A sensor string is a human string that describes, at a minimum, a sensor.
It can also optionally define a selector for the sensor, parameters for
the sensor, a filter for the sensor, and options for the filter for the
sensor. Sensors can be provided as a string or a list of strings.

Examples for basic sensors
---------------------------------

Supplying a single sensor:

    'Computer Name'

Supplying two sensors in a list of strings:

    ['Computer Name', 'IP Route Details']

Supplying multiple sensors with selectors (name is the default
selector if none is supplied):

    [
        'Computer Name',
        'name:Computer Name',
        'id:1',
        'hash:123456789',
    ]

Sensor Parameters
-----------------

Supplying parameters to a sensor can control the arguments that are
supplied to a sensor, if that sensor takes any arguments.

Sensor parameters must be surrounded with curly braces '{}',
and must have a key and value specified that is separated by
an equals '='. Multiple parameters must be seperated by
a comma ','. The key should match up to a valid parameter key
for the sensor in question.

If a parameter is supplied and the sensor doesn't have a
corresponding key name, it will be ignored. If the sensor has
parameters and a parameter is NOT supplied then one of two
paths will be taken:

    * if the parameter does not require a default value, the
    parameter is left blank and not supplied.
    * if the parameter does require a value (pulldowns, for
    example), a default value is derived (for pulldowns,
    the first value available as a pulldown entry is used).

Examples for sensors with parameters
------------------------------------

Supplying a single sensor with a single parameter 'dirname':

    'Sensor With Params{dirname=Program Files}'

Supplying a single sensor with two parameters, 'param1' and
'param2':

    'Sensor With Params{param1=value1,param2=value2}'

Sensor Filters
--------------

Supplying a filter to a sensor controls what data will be shown in
those columns (sensors) you've provided.

Sensor filters can be supplied by adding ', that FILTER:VALUE',
where FILTER is a valid filter string, and VALUE is the string
that you want FILTER to match on.

See filter help for a list of all possible FILTER strings.

See options help for a list of options that can control how
the filter works.

Examples for sensors with filters
---------------------------------

Supplying a sensor with a filter that limits the results to only
show column data that matches the regular expression
'.*Windows.*' (Tanium does a case insensitive match by default):

    'Computer Name, that contains:Windows'

Supplying a sensor with a filter that limits the results to only
show column data that matches the regular expression
'Microsoft.*':

    'Computer Name, that starts with:Microsoft'

Supply a sensor with a filter that limits the results to only
show column data that has a version greater or equal to
'39.0.0.0'. Since this sensor uses Version as its default result
type, there is no need to change the value type using filter
options.

    'Installed Application Version' \
    '{Application Name=Google Chrome}, that =>:39.0.0.0'

Sensor Options
--------------

Supplying options to a sensor can change how the filter for
that sensor works.

Sensor options can be supplied by adding ', opt:OPTION' or
', opt:OPTION:VALUE' for those options that require values,
where OPTION is a valid option string, and VALUE is the
appropriate value required by accordant OPTION.

See options help for a list of options that can control how
the filter works.

Examples for sensors with options
---------------------------------

Supplying a sensor with an option that forces tanium to
re-fetch any cached column data that is older than 1 minute:

    'Computer Name, opt:max_data_age:60'

Supplying a sensor with filter and an option that causes
Tanium to match case for the filter value:

    'Computer Name, that contains:Windows, opt:match_case'

Supplying a sensor with a filter and an option that causes
Tanium to match all values supplied:

    'Computer Name, that contains:Windows, opt:match_all_values'

Supplying a sensor with a filter and a set of options that
causes Tanium to recognize the value type as String (which is
the default type for most sensors), re-fetch data older than
10 minutes, match any values, and match case:

    'Computer Name', that contains:Windows, ' \
    opt:value_type:string, opt:max_data_age:600, ' \
    'opt:match_any_value, opt:match_case'
```

  * Validation Test: notexitcode
    * Valid: **True**
    * Messages: Exit Code is not 0



[TOC](#user-content-toc)


# Print the help for filters

```bash
ask_manual_question.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --filters-help csv
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Asking manual question:
{
  "filters_help": true, 
  "get_results": true, 
  "options_help": false, 
  "question_filters": [], 
  "question_options": [], 
  "sensors": [], 
  "sensors_help": false
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
ask_manual_question.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --options-help csv
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Asking manual question:
{
  "filters_help": false, 
  "get_results": true, 
  "options_help": true, 
  "question_filters": [], 
  "question_options": [], 
  "sensors": [], 
  "sensors_help": false
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


# Ask a question example 1

  * Ask a question with a single sensor
  * Save the results to a CSV file

```bash
ask_manual_question.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --sensor "Computer Name" --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv" csv
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Asking manual question:
{
  "filters_help": false, 
  "get_results": true, 
  "options_help": false, 
  "question_filters": [], 
  "question_options": [], 
  "sensors": [
    "Computer Name"
  ], 
  "sensors_help": false
}
2015-02-11 17:08:01,590 INFO     question_progress: Results 0% (Get Computer Name from all machines)
2015-02-11 17:08:06,603 INFO     question_progress: Results 100% (Get Computer Name from all machines)
++ Asked Question 'Get Computer Name from all machines' ID: 11458
++ Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv' written with 56 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv exists, content:

```
Computer Name
Casus-Belli.local
jtanium1.localdomain
```



[TOC](#user-content-toc)


# Ask a question example 2

  * Ask a question with a single sensor by id
  * Save the results to a CSV file

```bash
ask_manual_question.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --sensor "id:1" --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv" csv
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Asking manual question:
{
  "filters_help": false, 
  "get_results": true, 
  "options_help": false, 
  "question_filters": [], 
  "question_options": [], 
  "sensors": [
    "id:1"
  ], 
  "sensors_help": false
}
2015-02-11 17:08:06,784 INFO     question_progress: Results 0% (Get Action Statuses from all machines)
2015-02-11 17:08:11,798 INFO     question_progress: Results 0% (Get Action Statuses from all machines)
2015-02-11 17:08:16,810 INFO     question_progress: Results 0% (Get Action Statuses from all machines)
2015-02-11 17:08:21,825 INFO     question_progress: Results 100% (Get Action Statuses from all machines)
++ Asked Question 'Get Action Statuses from all machines' ID: 11459
++ Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv' written with 3937 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv exists, content:

```
Action Statuses,Count
1363:Completed.,1
1108:Completed.,1
1196:Completed.,1
1319:Completed.,1
1121:Completed.,1
1146:Completed.,1
1294:Completed.,1
1336:Completed.,1
1167:Completed.,1
...trimmed for brevity...
```



[TOC](#user-content-toc)


# Ask a question example 3

  * Ask a question with two sensors
  * Save the results to a CSV file

```bash
ask_manual_question.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --sensor "Computer Name" --sensor "Installed Applications"  --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv" csv
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Asking manual question:
{
  "filters_help": false, 
  "get_results": true, 
  "options_help": false, 
  "question_filters": [], 
  "question_options": [], 
  "sensors": [
    "Computer Name", 
    "Installed Applications"
  ], 
  "sensors_help": false
}
2015-02-11 17:08:22,051 INFO     question_progress: Results 0% (Get Computer Name and Installed Applications from all machines)
2015-02-11 17:08:27,071 INFO     question_progress: Results 0% (Get Computer Name and Installed Applications from all machines)
2015-02-11 17:08:32,091 INFO     question_progress: Results 100% (Get Computer Name and Installed Applications from all machines)
++ Asked Question 'Get Computer Name and Installed Applications from all machines' ID: 11460
++ Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv' written with 22539 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv exists, content:

```
Computer Name,Name,Silent Uninstall String,Uninstallable,Version
Casus-Belli.local,"Google Search
Microsoft Chart Converter
Spotify
Wish
BluetoothUIServer
Time Machine
AppleGraphicsWarning
soagent
AinuIM
...trimmed for brevity...
```



[TOC](#user-content-toc)


# Ask a question example 4

  * Ask a question with a sensor that requires parameters
  * Save the results to a CSV file

```bash
ask_manual_question.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --sensor "Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*}" --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv" csv
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Asking manual question:
{
  "filters_help": false, 
  "get_results": true, 
  "options_help": false, 
  "question_filters": [], 
  "question_options": [], 
  "sensors": [
    "Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*}"
  ], 
  "sensors_help": false
}
2015-02-11 17:08:32,351 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:08:37,369 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:08:42,383 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:08:47,398 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:08:52,414 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:08:57,431 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:09:02,448 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:09:07,461 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:09:12,474 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:09:17,487 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:09:22,502 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:09:27,517 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:09:32,533 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:09:37,548 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:09:42,561 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:09:47,575 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:09:52,598 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:09:57,612 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:10:02,628 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:10:07,648 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:10:12,666 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:10:17,680 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:10:22,697 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:10:27,713 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:10:32,727 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:10:37,748 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:10:42,763 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:10:47,777 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:10:52,795 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:10:57,809 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:11:02,824 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:11:07,842 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:11:12,860 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:11:17,882 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:11:22,901 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:11:27,916 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:11:32,933 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:11:37,951 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:11:42,965 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:11:47,980 INFO     question_progress: Results 50% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 17:11:52,996 INFO     question_progress: Results 100% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
++ Asked Question 'Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines' ID: 11461
++ Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv' written with 33951 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv exists, content:

```
"Folder Name Search with RegEx Match[No, Program Files, No, ]"
C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\cgi-bin
C:\Program Files\VMware\VMware Tools\plugins\vmsvc
C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1040_ITA_LP\x64\1040\help
C:\Program Files\Common Files\Microsoft Shared\VS7Debug
C:\Program Files\Tanium\Tanium Server\Apache24\manual\style
C:\Program Files\Tanium\Tanium Server\Apache24\htdocs\console\history
C:\Program Files\Common Files\VMware\Drivers\vmci\sockets\include
C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
C:\Program Files\Tanium\Tanium Server\plugins\console\Dashboards
...trimmed for brevity...
```



[TOC](#user-content-toc)


# Ask a question example 5

  * Ask a question with a single sensor
  * Supply a filter in the sensor that limits the column data to .*Windows.* matches
  * Supply an option in the sensor that ignores case in the filter
  * Supply an option in the sensor that re-fetches cached data older than 1 minute
  * Save the results to a CSV file

```bash
ask_manual_question.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --sensor "Operating System, that contains:Windows, opt:ignore_case, opt:max_data_age:60" --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv" csv
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Asking manual question:
{
  "filters_help": false, 
  "get_results": true, 
  "options_help": false, 
  "question_filters": [], 
  "question_options": [], 
  "sensors": [
    "Operating System, that contains:Windows, opt:ignore_case, opt:max_data_age:60"
  ], 
  "sensors_help": false
}
2015-02-11 17:11:53,268 INFO     question_progress: Results 0% (Get Operating System contains "Windows" from all machines)
2015-02-11 17:11:58,283 INFO     question_progress: Results 50% (Get Operating System contains "Windows" from all machines)
2015-02-11 17:12:03,300 INFO     question_progress: Results 100% (Get Operating System contains "Windows" from all machines)
++ Asked Question 'Get Operating System contains "Windows" from all machines' ID: 11463
++ Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv' written with 65 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv exists, content:

```
Operating System
[no results]
Windows Server 2008 R2 Standard
```



[TOC](#user-content-toc)


# Ask a question example 6

  * Ask a question with two sensors
  * Supply parameters to the 2nd sensor
  * Supply a filter in the 2nd sensor that limits the column data to .*Shared.*
  * Supply an option in the 2nd sensor that re-fetches cached data older than 1 minute
  * Supply a question filter that limits the rows returned to machines whose Operating System sensor match .*Windows.*
  * Supply a question filter that limits the rows returned to machines whose IP Address filter does not equal 10.10.10.10
  * Supply two question options, one to OR the question filters supplied, and another to ignore the case while matching the question filters
  * Save the results to a CSV file

```bash
ask_manual_question.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 -s "Computer Name" -s "Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*, invalidparam=test}, that regex match:.*Shared.*, opt:max_data_age:3600" -f "Operating System, that contains:Windows" -f "IP Address, that not equals:10.10.10.10" -o "or" -o "ignore_case" --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv" csv
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Asking manual question:
{
  "filters_help": false, 
  "get_results": true, 
  "options_help": false, 
  "question_filters": [
    "Operating System, that contains:Windows", 
    "IP Address, that not equals:10.10.10.10"
  ], 
  "question_options": [
    "or", 
    "ignore_case"
  ], 
  "sensors": [
    "Computer Name", 
    "Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*, invalidparam=test}, that regex match:.*Shared.*, opt:max_data_age:3600"
  ], 
  "sensors_help": false
}
2015-02-11 17:12:03,569 INFO     question_progress: Results 0% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines where Operating System contains "Windows" or IP Address = "10.10.10.10")
2015-02-11 17:12:08,594 INFO     question_progress: Results 0% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines where Operating System contains "Windows" or IP Address = "10.10.10.10")
2015-02-11 17:12:13,618 INFO     question_progress: Results 50% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines where Operating System contains "Windows" or IP Address = "10.10.10.10")
2015-02-11 17:12:18,637 INFO     question_progress: Results 50% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines where Operating System contains "Windows" or IP Address = "10.10.10.10")
2015-02-11 17:12:23,659 INFO     question_progress: Results 100% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines where Operating System contains "Windows" or IP Address = "10.10.10.10")
++ Asked Question 'Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines where Operating System contains "Windows" or IP Address = "10.10.10.10"' ID: 11464
++ Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv' written with 4512 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv exists, content:

```
Computer Name,"Folder Name Search with RegEx Match[No, Program Files, No, ]"
jtanium1.localdomain,"C:\Program Files\Common Files\Microsoft Shared\VS7Debug
C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
C:\Program Files\Common Files\Microsoft Shared\ink\ru-RU
C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\keypad
C:\Program Files\Common Files\Microsoft Shared\ink
C:\Program Files\Common Files\Microsoft Shared\ink\sv-SE
C:\Program Files\Common Files\Microsoft Shared\ink\uk-UA
C:\Program Files\Common Files\Microsoft Shared\ink\sl-SI
C:\Program Files\Common Files\Microsoft Shared\ink\hu-HU
...trimmed for brevity...
```



[TOC](#user-content-toc)


# Ask a question example 7

  * Ask a question with 4 sensors
  * Use filters on 3rd and 4th sensor to limit the column data to only show certain apps
  * Use 2 question filters to limit the row data to only show the same apps used in the sensor filters
  * Supply two question options, one to AND the question filters supplied, and another to ignore the case while matching the question filters
  * Save the results to a CSV file

```bash
ask_manual_question.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 -s "Computer Name" -s "Last Logged In User" -s "Installed Applications, that contains:Google Search" -s "Installed Applications, that contains:Google Chrome" -f "Installed Applications, that contains:Google Search" -f "Installed Applications, that contains:Google Chrome" -o "and" -o "ignore_case" --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv" csv
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Asking manual question:
{
  "filters_help": false, 
  "get_results": true, 
  "options_help": false, 
  "question_filters": [
    "Installed Applications, that contains:Google Search", 
    "Installed Applications, that contains:Google Chrome"
  ], 
  "question_options": [
    "and", 
    "ignore_case"
  ], 
  "sensors": [
    "Computer Name", 
    "Last Logged In User", 
    "Installed Applications, that contains:Google Search", 
    "Installed Applications, that contains:Google Chrome"
  ], 
  "sensors_help": false
}
2015-02-11 17:12:23,937 INFO     question_progress: Results 0% (Get Computer Name and Last Logged In User and Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome" from all machines where Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome")
2015-02-11 17:12:28,967 INFO     question_progress: Results 0% (Get Computer Name and Last Logged In User and Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome" from all machines where Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome")
2015-02-11 17:12:33,997 INFO     question_progress: Results 100% (Get Computer Name and Last Logged In User and Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome" from all machines where Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome")
++ Asked Question 'Get Computer Name and Last Logged In User and Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome" from all machines where Installed Applications contains "Google Search" and Installed Applications contains "Google Chrome"' ID: 11466
++ Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv' written with 275 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv exists, content:

```
Computer Name,Last Logged In User,Name,Name,Silent Uninstall String,Silent Uninstall String,Uninstallable,Uninstallable,Version,Version
Casus-Belli.local,N/A on Mac,Google Search,Google Search,nothing,nothing,Not Uninstallable,Not Uninstallable,37.0.2062.120,37.0.2062.120
```



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Wed Feb 11 17:12:34 2015 EST, Contact info: **Jim Olsen <jim.olsen@tanium.com>**