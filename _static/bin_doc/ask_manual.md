Ask Manual Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Help for Ask Manual](#user-content-help-for-ask-manual)
  * [Ask a question example 1](#user-content-ask-a-question-example-1)
  * [Ask a question example 2](#user-content-ask-a-question-example-2)
  * [Ask a question example 3](#user-content-ask-a-question-example-3)
  * [Ask a question example 4](#user-content-ask-a-question-example-4)
  * [Ask a question example 5](#user-content-ask-a-question-example-5)
  * [Ask a question example 6](#user-content-ask-a-question-example-6)
  * [Ask a question example 7](#user-content-ask-a-question-example-7)
  * [Print the help for sensors](#user-content-print-the-help-for-sensors)
  * [Print the help for filters](#user-content-print-the-help-for-filters)
  * [Print the help for options](#user-content-print-the-help-for-options)

---------------------------

# Help for Ask Manual

  * Print the help for ask_manual.py
  * All scripts in bin/ will supply help if -h is on the command line
  * If passing in a parameter with a space or a special character, you need to surround it with quotes properly. On Windows this means double quotes. On Linux/Mac, this means single or double quotes, depending on what kind of character escaping you need.
  * If running this script on Linux or Mac, use the python scripts directly as the bin/ask_manual.py
  * If running this script on Windows, use the batch script in the winbin/ask_manual.bat so that python is called correctly.

```bash
ask_manual.py -h
```

```
usage: ask_manual.py [-h] [-u USERNAME] [-p PASSWORD]
                     [--session_id SESSION_ID] [--host HOST] [--port PORT]
                     [-l LOGLEVEL] [--debugformat] [--debug_method_locals]
                     [--record_all_requests] [--stats_loop_enabled]
                     [--http_auth_retry] [--http_retry_count HTTP_RETRY_COUNT]
                     [--pytan_user_config PYTAN_USER_CONFIG]
                     [--force_server_version FORCE_SERVER_VERSION]
                     [-s SENSORS] [-f QUESTION_FILTERS] [-o QUESTION_OPTIONS]
                     [--sensors-help] [--filters-help] [--options-help]
                     [--no-results | --results] [--file REPORT_FILE]
                     [--dir REPORT_DIR] [--enable_sse | --disable_sse]
                     [--sse_format {csv,xml,xml_obj,cef}] [--leading LEADING]
                     [--trailing TRAILING] [--export_format {csv,xml,json}]
                     [--sort HEADER_SORT | --no-sort | --auto_sort]
                     [--add-sensor | --no-add-sensor]
                     [--add-type | --no-add-type]
                     [--expand-columns | --no-columns]

Ask a manual question and save the results as a report format

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


# Ask a question example 1

  * Ask a question with a single sensor
  * Save the results to a CSV file

```bash
bin/ask_manual.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --sensor "Computer Name" --file "/tmp/out.csv"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
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
2015-10-02 20:03:18,450 INFO     pytan.pollers.QuestionPoller: ID 16095: Reached Threshold of 99% (3 of 3)
++ Asked Question 'Get Computer Name from all machines' ID: 16095
++ Report file '/tmp/out.csv' written with 81 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/out.csv exists, content:

```
Computer Name
c1u14-virtual-machine.(none)
WIN-6U71ED4M23D
TPT1.pytanlab.com
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Ask a question example 2

  * Ask a question with a single sensor by id
  * Save the results to a CSV file

```bash
bin/ask_manual.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --sensor "id:1" --file "/tmp/out.csv"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
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
2015-10-02 20:03:23,919 INFO     pytan.pollers.QuestionPoller: ID 16096: Reached Threshold of 99% (3 of 3)
++ Asked Question 'Get Action Statuses from all machines' ID: 16096
++ Report file '/tmp/out.csv' written with 311 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/out.csv exists, content:

```
Action Statuses,Count
121:Completed.,2
134:Completed.,3
123:Completed.,2
136:Completed.,2
137:Completed.,3
132:Completed.,3
138:Completed.,2
128:Completed.,2
139:Completed.,3
...trimmed for brevity...
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Ask a question example 3

  * Ask a question with two sensors
  * Save the results to a CSV file

```bash
bin/ask_manual.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --sensor "Computer Name" --sensor "Installed Applications" --file "/tmp/out.csv"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
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
2015-10-02 20:03:34,389 INFO     pytan.pollers.QuestionPoller: ID 16097: Reached Threshold of 99% (3 of 3)
++ Asked Question 'Get Computer Name and Installed Applications from all machines' ID: 16097
++ Report file '/tmp/out.csv' written with 116744 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/out.csv exists, content:

```
Computer Name,Name,Silent Uninstall String,Uninstallable,Version
c1u14-virtual-machine.(none),"libminiupnpc8
iso-codes
libexttextcat-2.0-0
growisofs
libxml2:i386
libsm6:i386
findutils
libgcr-base-3-1:i386
thunderbird-locale-en
...trimmed for brevity...
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Ask a question example 4

  * Ask a question with a sensor that requires parameters
  * Save the results to a CSV file

```bash
bin/ask_manual.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --sensor "Folder Contents{folderPath=C:\Program Files}" --file "/tmp/out.csv"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
++ Asking manual question:
{
  "filters_help": false, 
  "get_results": true, 
  "options_help": false, 
  "question_filters": [], 
  "question_options": [], 
  "sensors": [
    "Folder Contents{folderPath=C:\\Program Files}"
  ], 
  "sensors_help": false
}
2015-10-02 20:04:50,047 INFO     pytan.pollers.QuestionPoller: ID 16098: Reached Threshold of 99% (3 of 3)
++ Asked Question 'Get Folder Contents[C:\\Program Files] from all machines' ID: 16098
++ Report file '/tmp/out.csv' written with 502 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/out.csv exists, content:

```
Count,Folder Contents[C:\Program Files]
1,Folder : Microsoft Visual Studio 10.0
2,desktop.ini
1,Folder : Windows NT
1,Folder : Microsoft Help Viewer
1,Folder : Reference Assemblies
1,Folder : WindowsPowerShell
2,Folder : Common Files
1,Folder : Tanium
1,Folder : Microsoft.NET
...trimmed for brevity...
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Ask a question example 5

  * Ask a question with a single sensor
  * Supply a filter in the sensor that limits the column data to .*Windows.* matches
  * Supply an option in the sensor that ignores case in the filter
  * Supply an option in the sensor that re-fetches cached data older than 1 minute
  * Save the results to a CSV file

```bash
bin/ask_manual.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --sensor "Operating System, that contains:Windows, opt:ignore_case, opt:max_data_age:60" --file "/tmp/out.csv"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
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
2015-10-02 20:05:00,548 INFO     pytan.pollers.QuestionPoller: ID 16100: Reached Threshold of 99% (3 of 3)
++ Asked Question 'Get Operating System containing "Windows" from all machines' ID: 16100
++ Report file '/tmp/out.csv' written with 98 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/out.csv exists, content:

```
Operating System
[no results]
Windows Server 2008 R2 Standard
Windows Server 2012 R2 Standard
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



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
bin/ask_manual.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 -s "Computer Name" -s "Folder Contents{folderPath=C:\Program Files, invalidparam=test}, that regex match:.*Shared.*, opt:max_data_age:3600" -f "Operating System, that contains:Windows" -f "IP Address, that not equals:10.10.10.10" -o "or" -o "ignore_case" --file "/tmp/out.csv"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
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
    "Folder Contents{folderPath=C:\\Program Files, invalidparam=test}, that regex match:.*Shared.*, opt:max_data_age:3600"
  ], 
  "sensors_help": false
}
2015-10-02 20:05:41,139 INFO     pytan.pollers.QuestionPoller: ID 16101: Reached Threshold of 99% (3 of 3)
++ Asked Question 'Get Computer Name and Folder Contents[C:\\Program Files, test] containing "Shared" from all machines with ( Operating System containing "Windows" or any IP Address != "10.10.10.10" )' ID: 16101
++ Report file '/tmp/out.csv' written with 178 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/out.csv exists, content:

```
Computer Name,"Folder Contents[C:\Program Files, test]"
c1u14-virtual-machine.(none),[no results]
WIN-6U71ED4M23D,[current result unavailable]
TPT1.pytanlab.com,[no results]
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Ask a question example 7

  * Ask a question with 4 sensors
  * Use filters on 3rd and 4th sensor to limit the column data to only show certain apps
  * Use 2 question filters to limit the row data to only show the same apps used in the sensor filters
  * Supply two question options, one to OR the question filters supplied, and another to ignore the case while matching the question filters
  * Save the results to a CSV file

```bash
bin/ask_manual.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 -s "Computer Name" -s "Last Logged In User" -s "Installed Applications, that contains:Google" -f "Installed Applications, that contains:Google" -f "Installed Applications, that contains:Chrome" -o "or" -o "ignore_case" --file "/tmp/out.csv"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
++ Asking manual question:
{
  "filters_help": false, 
  "get_results": true, 
  "options_help": false, 
  "question_filters": [
    "Installed Applications, that contains:Google", 
    "Installed Applications, that contains:Chrome"
  ], 
  "question_options": [
    "or", 
    "ignore_case"
  ], 
  "sensors": [
    "Computer Name", 
    "Last Logged In User", 
    "Installed Applications, that contains:Google"
  ], 
  "sensors_help": false
}
2015-10-02 20:05:46,653 INFO     pytan.pollers.QuestionPoller: ID 16102: Reached Threshold of 99% (3 of 3)
++ Asked Question 'Get Computer Name and Last Logged In User and Installed Applications containing "Google" from all machines with ( Installed Applications containing "Google" or Installed Applications containing "Chrome" )' ID: 16102
++ Report file '/tmp/out.csv' written with 521 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/out.csv exists, content:

```
Computer Name,Last Logged In User,Name,Silent Uninstall String,Uninstallable,Version
TPT1.pytanlab.com,TPT1\Administrator,Google Chrome,"""C:\Program Files (x86)\Google\Chrome\Application\45.0.2454.101\Installer\setup.exe"" --uninstall --multi-install --chrome --system-level",Not Uninstallable,45.0.2454.101
c1u14-virtual-machine.(none),tanium,"libaccount-plugin-google
account-plugin-google","nothing
nothing","Not Uninstallable
Not Uninstallable","0.11+14.04.20140409.1-0ubuntu2
0.11+14.04.20140409.1-0ubuntu2"
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Print the help for sensors

```bash
bin/ask_manual.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --sensors-help
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
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


Error occurred: 
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

```STDERR
Traceback (most recent call last):
  File "/Users/jolsen/gh/pytan/lib/pytan/binsupport.py", line 2636, in process_ask_manual_args
    response = handler.ask(qtype='manual', **obj_grp_args)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 388, in ask
    result = method(**clean_kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 675, in ask_manual
    pytan.utils.check_for_help(kwargs=kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2082, in check_for_help
    raise pytan.exceptions.PytanHelp(help_out)
PytanHelp: 
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
bin/ask_manual.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --filters-help
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
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


Error occurred: 
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

```STDERR
Traceback (most recent call last):
  File "/Users/jolsen/gh/pytan/lib/pytan/binsupport.py", line 2636, in process_ask_manual_args
    response = handler.ask(qtype='manual', **obj_grp_args)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 388, in ask
    result = method(**clean_kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 675, in ask_manual
    pytan.utils.check_for_help(kwargs=kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2082, in check_for_help
    raise pytan.exceptions.PytanHelp(help_out)
PytanHelp: 
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
bin/ask_manual.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --options-help
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
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


Error occurred: 
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

```STDERR
Traceback (most recent call last):
  File "/Users/jolsen/gh/pytan/lib/pytan/binsupport.py", line 2636, in process_ask_manual_args
    response = handler.ask(qtype='manual', **obj_grp_args)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 388, in ask
    result = method(**clean_kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 675, in ask_manual
    pytan.utils.check_for_help(kwargs=kwargs)
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2082, in check_for_help
    raise pytan.exceptions.PytanHelp(help_out)
PytanHelp: 
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


###### generated by: `build_bin_doc v2.1.0`, date: Fri Oct  2 16:05:47 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**