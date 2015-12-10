Print Server Info Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Help for Print Server Info](#user-content-help-for-print-server-info)
  * [Print the server info in JSON format](#user-content-print-the-server-info-in-json-format)

---------------------------

# Help for Print Server Info

  * Print the help for print_server_info.py
  * All scripts in bin/ will supply help if -h is on the command line
  * If passing in a parameter with a space or a special character, you need to surround it with quotes properly. On Windows this means double quotes. On Linux/Mac, this means single or double quotes, depending on what kind of character escaping you need.
  * If running this script on Linux or Mac, use the python scripts directly as the bin/print_server_info.py
  * If running this script on Windows, use the batch script in the winbin/print_server_info.bat so that python is called correctly.

```bash
print_server_info.py -h
```

```
usage: print_server_info.py [-h] [-u USERNAME] [-p PASSWORD]
                            [--session_id SESSION_ID] [--host HOST]
                            [--port PORT] [-l LOGLEVEL] [--debugformat]
                            [--debug_method_locals] [--record_all_requests]
                            [--stats_loop_enabled] [--http_auth_retry]
                            [--http_retry_count HTTP_RETRY_COUNT]
                            [--pytan_user_config PYTAN_USER_CONFIG]
                            [--force_server_version FORCE_SERVER_VERSION]
                            [--json]

Prints server information to stdout

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

Output Options:
  --json                Show a json dump of the server information (default:
                        False)
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Print the server info in JSON format

```bash
bin/print_server_info.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --json
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
{
  "Action History Cache": {
    "Action Stop Count": 0, 
    "Actions": 142
  }, 
  "Active Question Cache": {
    "Active Client Estimate": 3, 
    "Active Question Estimate": 71
  }, 
  "Authenticator": {
    "ActiveSessions": 1, 
    "TotalSessions": 105
  }, 
  "Client Pump": {
    "Connections Active": 2, 
    "Connections Inactive": 1, 
    "Connections Stopped": 97
  }, 
  "Data Interface": {
    "Estimated Node Count": 3, 
    "License Seat Cap": 60, 
    "Reg Connection Count": 0, 
    "Reg Connection Limit": 1000, 
    "Report Cache Count": 54, 
    "Sensor Bytes Per Second Limit": 5242880, 
    "Sensor Bytes Sent Since Last Time": 0, 
    "Sensor Connection Count": 0, 
    "Sensor Connection Limit": 8
  }, 
  "File Request Handler": {
    "Chunk Bytes Sent Since Last Time": 0, 
    "Download Bytes Sent Since Last Time": 0, 
    "Download Connection Count": 0, 
    "Download Connection Limit": 1000
  }, 
  "Group Cache": {
    "ComputerSpecs": 0, 
    "ComputerSpecsGroups": 0, 
    "FilterSpecCount": 275, 
    "GroupCount": 508, 
    "GroupsActionGroupSpecs": 0, 
    "GroupsComputerSpecs": 0, 
    "GroupsTempSensors": 9, 
    "QuestionFilterSpecs": 4, 
    "QuestionSelectSpecs": 3815, 
    "QuestionSubGroups": 3097, 
    "QuestionTextCount": 0, 
    "SavedQuestionTextCount": 112, 
    "SelectSpecCount": 5739
  }, 
  "HTTP File Cache": {
    "Cached File Count": 1, 
    "File Cache Size": 1150
  }, 
  "Memory Info": {
    "DoubleFreeCount": "0", 
    "NonTBBFreeCount": "0", 
    "PageFaultCount": "1077118", 
    "PagefileUsage": "1870147584", 
    "PeakPagefileUsage": "1998979072", 
    "PeakWorkingSetSize": "1.56 GB", 
    "QuotaPagedPoolUsage": "711400", 
    "QuotaPeakNonPagedPoolUsage": "4006860", 
    "QuotaPeakPagedPoolUsage": "711848", 
    "WorkingSetSize": "283.71 MB"
  }, 
  "Module Cache": {
    "127.0.0.1:17477 Module Count": 30, 
    "Module Definition Count": 32
  }, 
  "Network": {
    "Allocated SendOp Count": 110, 
    "Allocated SendOp Limit": 0, 
    "Concurrency": 32, 
    "Concurrency Threads": 32, 
    "Idle Threads": 32, 
    "Max Concurrency Threads": 64, 
    "Min Available Threads": 28, 
    "Pending SendOp Count": 0, 
    "Queue Completion Timeout": 1000, 
    "Running Threads": 32, 
    "SendOpReady FreeCount": 0, 
    "SendOpReady HeadCount": 110, 
    "Threads Reset Interval": 0, 
    "Unpaused Threads": 32
  }, 
  "Package Cache": {
    "Package Count": 93, 
    "Package File Count": 99
  }, 
  "Question History": {
    "History Limit Days": 7, 
    "Last Question ID": 16113, 
    "Last Saved Question ID": 126, 
    "Question Count": 3739
  }, 
  "SOAP Network": {
    "Allocated SendOp Count": 289, 
    "Allocated SendOp Limit": 0, 
    "Concurrency": 32, 
    "Concurrency Threads": 32, 
    "Idle Threads": 31, 
    "Max Concurrency Threads": 64, 
    "Min Available Threads": 24, 
    "Pending SendOp Count": 0, 
    "Queue Completion Timeout": 1000, 
    "Running Threads": 32, 
    "SendOpReady FreeCount": 0, 
    "SendOpReady HeadCount": 289, 
    "Threads Reset Interval": 14400, 
    "Unpaused Threads": 32
  }, 
  "SOAP Pump": {
    "Connections Active": 2, 
    "Connections Inactive": 0, 
    "Connections Stopped": 98
  }, 
  "SOAP Server": {
    "Connections": 2, 
    "Last Reset": "2015-10-02 18:09:43 +0000", 
    "SOAP Busy Handlers": 72, 
    "SOAP Handlers": 16, 
    "Use Compression": "true", 
    "Using IPv6": "true", 
    "Using Keep-Alive": "true", 
    "Using NTLM": "false"
  }, 
  "SOAP Snapshots": {
    "Snapshot Count": 1
  }, 
  "SOAP Timing": {
    "Timing: action": "Average 0ms, Count: 1001, Last: 0ms", 
    "Timing: actions": "Average 3ms, Count: 8, Last: 15ms", 
    "Timing: client_count": "Average 0ms, Count: 2, Last: 0ms", 
    "Timing: client_status": "Average 0ms, Count: 9, Last: 0ms", 
    "Timing: group": "Average 5ms, Count: 25, Last: 0ms", 
    "Timing: groups": "Average 1ms, Count: 22, Last: 0ms", 
    "Timing: package_spec": "Average 0ms, Count: 96, Last: 0ms", 
    "Timing: plugins": "Average 7ms, Count: 2, Last: 0ms", 
    "Timing: question": "Average 9ms, Count: 78, Last: 14ms", 
    "Timing: questions": "Average 102ms, Count: 8, Last: 78ms", 
    "Timing: roles": "Average 0ms, Count: 17, Last: 0ms", 
    "Timing: saved_actions": "Average 4ms, Count: 29, Last: 16ms", 
    "Timing: saved_question": "Average 8ms, Count: 27, Last: 16ms", 
    "Timing: saved_questions": "Average 43ms, Count: 6, Last: 31ms", 
    "Timing: sensor": "Average 3ms, Count: 5, Last: 0ms", 
    "Timing: sensors": "Average 6ms, Count: 118, Last: 46ms", 
    "Timing: system_setting": "Average 0ms, Count: 57, Last: 0ms", 
    "Timing: system_settings": "Average 5ms, Count: 11, Last: 0ms", 
    "Timing: system_status": "Average 0ms, Count: 158, Last: 0ms", 
    "Timing: user": "Average 0ms, Count: 21, Last: 0ms", 
    "Timing: users": "Average 1ms, Count: 23, Last: 0ms", 
    "Timing: white_listed_url": "Average 1ms, Count: 10, Last: 0ms", 
    "Timing: white_listed_urls": "Average 0ms, Count: 22, Last: 0ms"
  }, 
  "Sensor Cache": {
    "Active Preview Sensor Count": 0, 
    "Available Preview Sensor Count": 0, 
    "Preview Sensor Count": 0, 
    "Sensor Count": 568, 
    "Waiting Preview Sensor Count": 0
  }, 
  "Settings": {
    "AllowOldSessionID": "false", 
    "Client Count": "4", 
    "PreFetchRows": "1000", 
    "Server Start Time": "2015-10-02 18:09:42 +0000", 
    "Server Up-Time": "119 minutes", 
    "ServerName": "0.0.0.0", 
    "ServerPort": "17472", 
    "ServerSOAPPort": "443", 
    "UseSOAPIOCP": "true", 
    "UseTBBAllocator": "true", 
    "UseTBBAllocatorStats": "false", 
    "UseTBBScalingAlignment": "false", 
    "Version": "6.5.314.4301"
  }, 
  "String Cache": {
    "NameData": 654, 
    "Sensor 131549066 Refresh Time/String Count": "1 / 2", 
    "Sensor 1511329504 Refresh Time/String Count": "1 / 1758", 
    "Sensor 1559751995 Refresh Time/String Count": "1 / 31", 
    "Sensor 1688928675 Refresh Time/String Count": "1 / 8", 
    "Sensor 1782389954 Refresh Time/String Count": "1 / 5", 
    "Sensor 1792443391 Refresh Time/String Count": "1 / 202", 
    "Sensor 2581054686 Refresh Time/String Count": "1 / 6", 
    "Sensor 2634431519 Refresh Time/String Count": "1 / 11", 
    "Sensor 2944509120 Refresh Time/String Count": "1 / 20", 
    "Sensor 2944509990 Refresh Time/String Count": "1 / 20", 
    "Sensor 2944510860 Refresh Time/String Count": "1 / 19", 
    "Sensor 2944511730 Refresh Time/String Count": "1 / 20", 
    "Sensor 2944513470 Refresh Time/String Count": "1 / 19", 
    "Sensor 2944711395 Refresh Time/String Count": "1 / 19", 
    "Sensor 2944712265 Refresh Time/String Count": "1 / 18", 
    "Sensor 2944713135 Refresh Time/String Count": "1 / 19", 
    "Sensor 2944714005 Refresh Time/String Count": "1 / 18", 
    "Sensor 2944717485 Refresh Time/String Count": "1 / 19", 
    "Sensor 2944916280 Refresh Time/String Count": "1 / 3", 
    "Sensor 2944917585 Refresh Time/String Count": "1 / 19", 
    "Sensor 2944918455 Refresh Time/String Count": "1 / 18", 
    "Sensor 3005061811 Refresh Time/String Count": "1 / 4", 
    "Sensor 3209138996 Refresh Time/String Count": "1 / 13", 
    "Sensor 322086833 Refresh Time/String Count": "1 / 49", 
    "Sensor 3409330187 Refresh Time/String Count": "1 / 5", 
    "Sensor 3556221173 Refresh Time/String Count": "1 / 6", 
    "Sensor 435227963 Refresh Time/String Count": "1 / 18", 
    "Sensor 45421433 Refresh Time/String Count": "1 / 5", 
    "Sensor 607666494 Refresh Time/String Count": "1 / 4", 
    "Sensor 7318847 Refresh Time/String Count": "1 / 6", 
    "Sensor 889071797 Refresh Time/String Count": "1 / 9", 
    "Total String Count": 2373
  }, 
  "System Performance Info": {
    "CommitLimit": "4193616", 
    "CommitPeak": "952726", 
    "CommitTotal": "913740", 
    "HandleCount": "38425", 
    "KernelNonpaged": "13234", 
    "KernelPaged": "51703", 
    "KernelTotal": "64937", 
    "PageSize": "4096", 
    "PhysicalAvailable": "1507288", 
    "PhysicalTotal": "2097038", 
    "ProcessCount": "50", 
    "ProcessThreadCount": "712", 
    "SystemCache": "327987"
  }, 
  "System Status Cache": {
    "System Count": 2, 
    "blocked_count": 0, 
    "leader_count": 2, 
    "normal_count": 0, 
    "receive_backward_count": 1, 
    "receive_forward_count": 0, 
    "receive_none_count": 1, 
    "receive_ok_count": 0, 
    "send_backward_count": 1, 
    "send_forward_count": 1, 
    "send_none_count": 0, 
    "send_ok_count": 0, 
    "slowlink_count": 0, 
    "version_details_0.0.0.0": "count: 1 filtered: 0", 
    "version_details_5.1.314.7724": "count: 1 filtered: 0", 
    "version_details_6.0.314.1195": "count: 2 filtered: 2"
  }
}
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v2.1.0`, date: Fri Oct  2 16:09:37 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**