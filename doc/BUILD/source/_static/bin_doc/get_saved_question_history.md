Get Saved Question History Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Help for Get Saved Question History](#user-content-help-for-get-saved-question-history)
  * [Get the details about all questions that have data that have been asked because of the Saved Question named "Installed Applications"](#user-content-get-the-details-about-all-questions-that-have-data-that-have-been-asked-because-of-the-saved-question-named-"installed-applications")
  * [Get the details about all questions, whether they have data or not, that have been asked because of the Saved Question named "Installed Applications"](#user-content-get-the-details-about-all-questions,-whether-they-have-data-or-not,-that-have-been-asked-because-of-the-saved-question-named-"installed-applications")
  * [Get the details about all questions that have data](#user-content-get-the-details-about-all-questions-that-have-data)
  * [Get the details about all questions, whether they have data or not](#user-content-get-the-details-about-all-questions,-whether-they-have-data-or-not)

---------------------------

# Help for Get Saved Question History

  * Print the help for get_saved_question_history.py
  * All scripts in bin/ will supply help if -h is on the command line
  * If passing in a parameter with a space or a special character, you need to surround it with quotes properly. On Windows this means double quotes. On Linux/Mac, this means single or double quotes, depending on what kind of character escaping you need.
  * If running this script on Linux or Mac, use the python scripts directly as the bin/get_saved_question_history.py
  * If running this script on Windows, use the batch script in the winbin/get_saved_question_history.bat so that python is called correctly.

```bash
get_saved_question_history.py -h
```

```
usage: get_saved_question_history.py [-h] [-u USERNAME] [-p PASSWORD]
                                     [--session_id SESSION_ID] [--host HOST]
                                     [--port PORT] [-l LOGLEVEL]
                                     [--debugformat] [--debug_method_locals]
                                     [--record_all_requests]
                                     [--stats_loop_enabled]
                                     [--http_auth_retry]
                                     [--http_retry_count HTTP_RETRY_COUNT]
                                     [--pytan_user_config PYTAN_USER_CONFIG]
                                     [--force_server_version FORCE_SERVER_VERSION]
                                     [--no-empty_results | --empty_results]
                                     [--no-all_questions | --all_questions]
                                     [--file REPORT_FILE] [--dir REPORT_DIR]
                                     [--id ID | --name NAME]

Gets the Result Info for all the questions asked for a given saved question, or for all questions asked ever, and exports the question information to a CSV file

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

Saved Question Options:
  --no-empty_results    Do not include details for questions with no data
                        (default)
  --empty_results       Include details for questions with no data
  --no-all_questions    Do not include details for ALL questions, only the
                        ones associated with a given saved question via --name
                        or --id (default)
  --all_questions       Include details for ALL questions

Report File Options:
  --file REPORT_FILE    File to save report to (default:
                        pytan_question_history_2015_10_02-16_08_30-EDT.csv)
  --dir REPORT_DIR      Directory to save report to (current directory will be
                        used if not supplied) (default: None)

Saved Question Selectors:
  --id ID               id of saved_question to ask (default: None)
  --name NAME           name of saved_question to ask (default: None)
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Get the details about all questions that have data that have been asked because of the Saved Question named "Installed Applications"

  * Will produce a CSV file with the details for each question that has data asked because of the Saved Question named "Installed Applications"

```bash
bin/get_saved_question_history.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --name "Installed Applications" --file "/tmp/out.csv"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
++ Finding saved question: {
  "name": "Installed Applications", 
  "objtype": "saved_question"
}
Found Saved Question: 'SavedQuestion, name: 'Installed Applications', id: 59'
Found 3739 Total Questions
Found 2 Questions asked for Saved_question 'SavedQuestion, name: 'Installed Applications', id: 59'
Getting ResultInfo for 2 Questions
Found 2 Questions that actually have data
Wrote 473 bytes to report file: '/tmp/out.csv'
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/out.csv exists, content:

```
"Question ID","Question Text","Spawned by Saved Question ID","Question Started","Question Expired","Row Count","Client Count Right Now","Client Count that saw this question","Client Count that passed this questions filters"
"16093","Get Installed Applications from all machines","59","2015-10-02T20:00:26","2015-10-02T20:10:26","1000","3","3","3"
"16106","Get Installed Applications from all machines","59","2015-10-02T20:05:26","2015-10-02T20:15:26","1004","3","3","3"
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Get the details about all questions, whether they have data or not, that have been asked because of the Saved Question named "Installed Applications"

  * Will produce a CSV file with the details for each question asked because of the Saved Question named "Installed Applications"

```bash
bin/get_saved_question_history.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --name "Installed Applications" --empty_results --file "/tmp/out.csv"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
++ Finding saved question: {
  "name": "Installed Applications", 
  "objtype": "saved_question"
}
Found Saved Question: 'SavedQuestion, name: 'Installed Applications', id: 59'
Found 3739 Total Questions
Found 2 Questions asked for Saved_question 'SavedQuestion, name: 'Installed Applications', id: 59'
Getting ResultInfo for 2 Questions
Wrote 473 bytes to report file: '/tmp/out.csv'
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/out.csv exists, content:

```
"Question ID","Question Text","Spawned by Saved Question ID","Question Started","Question Expired","Row Count","Client Count Right Now","Client Count that saw this question","Client Count that passed this questions filters"
"16093","Get Installed Applications from all machines","59","2015-10-02T20:00:26","2015-10-02T20:10:26","1000","3","3","3"
"16106","Get Installed Applications from all machines","59","2015-10-02T20:05:26","2015-10-02T20:15:26","1004","3","3","3"
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Get the details about all questions that have data

  * Will produce a CSV file with the details for each question with data

```bash
bin/get_saved_question_history.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --all_questions --file "/tmp/out.csv"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
Found 3739 Total Questions
Getting ResultInfo for 3739 Questions
Found 47 Questions that actually have data
Wrote 7383 bytes to report file: '/tmp/out.csv'
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/out.csv exists, content:

```
"Question ID","Question Text","Spawned by Saved Question ID","Question Started","Question Expired","Row Count","Client Count Right Now","Client Count that saw this question","Client Count that passed this questions filters"
"14831","Get Has Hardware Tools from all machines","2","2015-09-30T13:40:35","2015-09-30T13:50:35","2","3","3","3"
"15987","Get Has Stale Tanium Client Data from all machines","100","2015-10-02T18:07:42","2015-10-02T18:17:42","1","3","2","2"
"16016","Get Computer Name from all machines","30","2015-10-02T18:48:16","2015-10-02T18:58:16","4","3","4","4"
"16042","Get Computer Name and Action Statuses matching ""^1\d\d:.*"" from all machines with Action Statuses matching ""^1\d\d:.*""","118","2015-10-02T19:21:53","2015-10-02T20:22:53","3","3","3","3"
"16055","Get Has Application Management Tools from all machines","3","2015-10-02T19:37:51","2015-10-02T19:47:51","2","3","3","3"
"16056","Get Has Tanium Standard Utilities from all machines","1","2015-10-02T19:39:24","2015-10-02T19:49:24","2","3","3","3"
"16069","Get Running Applications from all machines","54","2015-10-02T19:50:52","2015-10-02T20:00:52","19","3","3","3"
"16070","Get Computer Name and Last Date of Local Administrator Login from all machines with Last Date of Local Administrator Login not containing ""no results""","83","2015-10-02T19:51:23","2015-10-02T20:01:23","3","3","3","3"
"16071","Get Folder Contents[C:\Program Files] containing ""Shared"" from all machines","4294967295","2015-10-02T19:51:47","2015-10-02T20:01:47","1","3","3","3"
...trimmed for brevity...
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Get the details about all questions, whether they have data or not

  * Will produce a CSV file with the details for each question

```bash
bin/get_saved_question_history.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --all_questions --empty_results --file "/tmp/out.csv"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
Found 3739 Total Questions
Getting ResultInfo for 3739 Questions
Wrote 526439 bytes to report file: '/tmp/out.csv'
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/out.csv exists, content:

```
"Question ID","Question Text","Spawned by Saved Question ID","Question Started","Question Expired","Row Count","Client Count Right Now","Client Count that saw this question","Client Count that passed this questions filters"
"10394","Get Computer Name and Last Date of Local Administrator Login from all machines with Last Date of Local Administrator Login not containing ""no results""","83","2015-09-25T23:50:45","2015-09-26T00:00:45","0","3","0","0"
"10395","Get Action Statuses matching ""Nil"" from all machines","4294967295","2015-09-25T23:53:30","2015-09-26T00:03:30","0","3","0","0"
"10396","Get Firewall Status containing ""disabled"" from all machines with Firewall Status containing ""disabled""","85","2015-09-25T23:53:51","2015-09-26T00:03:51","0","3","0","0"
"10397","Get Running Applications from all machines","54","2015-09-25T23:54:38","2015-09-26T00:04:38","0","3","0","0"
"10398","Get Running Applications from all machines","54","2015-09-25T23:59:48","2015-09-26T00:09:48","0","3","0","0"
"10399","Get Last Logged In User from all machines","38","2015-09-26T00:02:54","2015-09-26T00:12:54","0","3","0","0"
"10400","Get Action Statuses matching ""Nil"" from all machines","4294967295","2015-09-26T00:03:30","2015-09-26T00:13:30","0","3","0","0"
"10401","Get Running Applications from all machines","54","2015-09-26T00:04:58","2015-09-26T00:14:58","0","3","0","0"
"10402","Get Application Crashes Yesterday from all machines with Application Crashes Yesterday containing "".""","49","2015-09-26T00:05:29","2015-09-26T00:15:29","0","3","0","0"
...trimmed for brevity...
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v2.1.0`, date: Fri Oct  2 16:09:22 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**