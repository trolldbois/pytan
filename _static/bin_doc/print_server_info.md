Print Server Info Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Print Server Info Help](#user-content-print-server-info-help)
  * [Print the server info in JSON format](#user-content-print-the-server-info-in-json-format)

---------------------------

# Print Server Info Help

  * Get server info

```bash
print_server_info.py -h
```

```
usage: print_server_info.py [-h] [-u USERNAME] [-p PASSWORD] [--host HOST]
                            [--port PORT] [-l LOGLEVEL] [--json]

Get server info

optional arguments:
  -h, --help            show this help message and exit
  --json                Show a json dump of the server information (default:
                        False)

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
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


# Print the server info in JSON format

```bash
print_server_info.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --json
```

```
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
{
  "Action History Cache": {
    "Action Stop Count": 0, 
    "Actions": 55
  }, 
  "Active Question Cache": {
    "Active Client Estimate": 2, 
    "Active Question Estimate": 43
  }, 
  "Authenticator": {
    "ActiveSessions": 1, 
    "TotalSessions": 270
  }, 
  "Client Pump": {
    "Connections Active": 1, 
    "Connections Inactive": 1, 
    "Connections Stopped": 98
  }, 
  "Data Interface": {
    "Estimated Node Count": 2, 
    "License Seat Cap": 60, 
    "Reg Connection Count": 0, 
    "Reg Connection Limit": 1000, 
    "Report Cache Count": 37, 
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
    "FilterSpecCount": 123, 
    "GroupCount": 190, 
    "GroupsActionGroupSpecs": 0, 
    "GroupsComputerSpecs": 0, 
    "GroupsTempSensors": 3, 
    "QuestionFilterSpecs": 3, 
    "QuestionSelectSpecs": 245, 
    "QuestionSubGroups": 139, 
    "QuestionTextCount": 0, 
    "SavedQuestionTextCount": 110, 
    "SelectSpecCount": 419
  }, 
  "HTTP File Cache": {
    "Cached File Count": 107, 
    "File Cache Size": 7959454
  }, 
  "Memory Info": {
    "DoubleFreeCount": "0", 
    "NonTBBFreeCount": "0", 
    "PageFaultCount": "232166", 
    "PagefileUsage": "528596992", 
    "PeakPagefileUsage": "545472512", 
    "PeakWorkingSetSize": "310.72 MB", 
    "QuotaPagedPoolUsage": "661944", 
    "QuotaPeakNonPagedPoolUsage": "3430356", 
    "QuotaPeakPagedPoolUsage": "662072", 
    "WorkingSetSize": "310.51 MB"
  }, 
  "Module Cache": {
    "127.0.0.1:17477 Module Count": 30, 
    "Module Definition Count": 32
  }, 
  "Network": {
    "Allocated SendOp Count": 93, 
    "Allocated SendOp Limit": 0, 
    "Concurrency": 32, 
    "Concurrency Threads": 32, 
    "Idle Threads": 32, 
    "Max Concurrency Threads": 64, 
    "Min Available Threads": 29, 
    "Pending SendOp Count": 0, 
    "Queue Completion Timeout": 1000, 
    "Running Threads": 32, 
    "SendOpReady FreeCount": 0, 
    "SendOpReady HeadCount": 93, 
    "Threads Reset Interval": 0, 
    "Unpaused Threads": 32
  }, 
  "Package Cache": {
    "Package Count": 75, 
    "Package File Count": 103
  }, 
  "Question History": {
    "History Limit Days": 7, 
    "Last Question ID": 1276, 
    "Last Saved Question ID": 110, 
    "Question Count": 174
  }, 
  "SOAP Network": {
    "Allocated SendOp Count": 215, 
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
    "SendOpReady HeadCount": 215, 
    "Threads Reset Interval": 14400, 
    "Unpaused Threads": 32
  }, 
  "SOAP Pump": {
    "Connections Active": 6, 
    "Connections Inactive": 0, 
    "Connections Stopped": 94
  }, 
  "SOAP Server": {
    "Connections": 6, 
    "Last Reset": "2015-08-07 19:12:36 +0000", 
    "SOAP Busy Handlers": 183, 
    "SOAP Handlers": 0, 
    "Use Compression": "true", 
    "Using IPv6": "true", 
    "Using Keep-Alive": "true", 
    "Using NTLM": "false"
  }, 
  "SOAP Snapshots": {
    "Snapshot Count": 3
  }, 
  "SOAP Timing": {
    "Timing: action": "Average 5ms, Count: 35, Last: 0ms", 
    "Timing: actions": "Average 0ms, Count: 6, Last: 0ms", 
    "Timing: client_count": "Average 0ms, Count: 1, Last: 0ms", 
    "Timing: client_status": "Average 0ms, Count: 6, Last: 0ms", 
    "Timing: group": "Average 11ms, Count: 10, Last: 0ms", 
    "Timing: groups": "Average 1ms, Count: 11, Last: 0ms", 
    "Timing: package_spec": "Average 2ms, Count: 36, Last: 0ms", 
    "Timing: plugins": "Average 14ms, Count: 1, Last: 14ms", 
    "Timing: question": "Average 17ms, Count: 43, Last: 16ms", 
    "Timing: questions": "Average 7ms, Count: 4, Last: 16ms", 
    "Timing: roles": "Average 0ms, Count: 8, Last: 0ms", 
    "Timing: saved_actions": "Average 4ms, Count: 13, Last: 0ms", 
    "Timing: saved_question": "Average 8ms, Count: 13, Last: 16ms", 
    "Timing: saved_questions": "Average 30ms, Count: 5, Last: 15ms", 
    "Timing: sensor": "Average 7ms, Count: 2, Last: 0ms", 
    "Timing: sensors": "Average 6ms, Count: 83, Last: 30ms", 
    "Timing: system_setting": "Average 13ms, Count: 16, Last: 0ms", 
    "Timing: system_settings": "Average 8ms, Count: 7, Last: 0ms", 
    "Timing: user": "Average 1ms, Count: 10, Last: 0ms", 
    "Timing: users": "Average 0ms, Count: 8, Last: 0ms", 
    "Timing: white_listed_url": "Average 1ms, Count: 26, Last: 0ms", 
    "Timing: white_listed_urls": "Average 0ms, Count: 10, Last: 0ms"
  }, 
  "Sensor Cache": {
    "Active Preview Sensor Count": 0, 
    "Available Preview Sensor Count": 0, 
    "Preview Sensor Count": 0, 
    "Sensor Count": 405, 
    "Waiting Preview Sensor Count": 0
  }, 
  "Settings": {
    "AllowOldSessionID": "false", 
    "Client Count": "2", 
    "PreFetchRows": "1000", 
    "Server Start Time": "2015-08-07 19:12:33 +0000", 
    "Server Up-Time": "22 minutes", 
    "ServerName": "0.0.0.0", 
    "ServerPort": "17472", 
    "ServerSOAPPort": "443", 
    "UseSOAPIOCP": "true", 
    "UseTBBAllocator": "true", 
    "UseTBBAllocatorStats": "false", 
    "UseTBBScalingAlignment": "false", 
    "Version": "6.5.314.4268"
  }, 
  "String Cache": {
    "NameData": 636, 
    "Sensor 131549066 Refresh Time/String Count": "1 / 2", 
    "Sensor 1488545663 Refresh Time/String Count": "1 / 548", 
    "Sensor 1488547403 Refresh Time/String Count": "1 / 548", 
    "Sensor 1488548273 Refresh Time/String Count": "1 / 548", 
    "Sensor 1488549143 Refresh Time/String Count": "1 / 548", 
    "Sensor 1488550013 Refresh Time/String Count": "1 / 548", 
    "Sensor 1488748373 Refresh Time/String Count": "1 / 25602", 
    "Sensor 1488749243 Refresh Time/String Count": "1 / 534", 
    "Sensor 1488750113 Refresh Time/String Count": "1 / 534", 
    "Sensor 1488750548 Refresh Time/String Count": "1 / 533", 
    "Sensor 1488751418 Refresh Time/String Count": "1 / 548", 
    "Sensor 1489697108 Refresh Time/String Count": "1 / 534", 
    "Sensor 1489697978 Refresh Time/String Count": "1 / 534", 
    "Sensor 1511329504 Refresh Time/String Count": "1 / 1417", 
    "Sensor 1559751995 Refresh Time/String Count": "1 / 50", 
    "Sensor 1688928675 Refresh Time/String Count": "1 / 14", 
    "Sensor 1782389954 Refresh Time/String Count": "1 / 16", 
    "Sensor 1792443391 Refresh Time/String Count": "1 / 231", 
    "Sensor 2581054686 Refresh Time/String Count": "1 / 5", 
    "Sensor 2721439124 Refresh Time/String Count": "1 / 3", 
    "Sensor 28471576 Refresh Time/String Count": "1 / 20", 
    "Sensor 3005061811 Refresh Time/String Count": "1 / 7", 
    "Sensor 3209138996 Refresh Time/String Count": "1 / 66", 
    "Sensor 322086833 Refresh Time/String Count": "1 / 59", 
    "Sensor 3409330187 Refresh Time/String Count": "1 / 4", 
    "Sensor 3556221173 Refresh Time/String Count": "1 / 49", 
    "Sensor 435227963 Refresh Time/String Count": "1 / 39", 
    "Sensor 443412787 Refresh Time/String Count": "1 / 25", 
    "Sensor 45421433 Refresh Time/String Count": "1 / 5", 
    "Sensor 7318847 Refresh Time/String Count": "1 / 6", 
    "Sensor 889071797 Refresh Time/String Count": "1 / 6", 
    "Total String Count": 33583
  }, 
  "System Performance Info": {
    "CommitLimit": "2073871", 
    "CommitPeak": "435033", 
    "CommitTotal": "417369", 
    "HandleCount": "30759", 
    "KernelNonpaged": "17415", 
    "KernelPaged": "35732", 
    "KernelTotal": "53147", 
    "PageSize": "4096", 
    "PhysicalAvailable": "688484", 
    "PhysicalTotal": "1037165", 
    "ProcessCount": "38", 
    "ProcessThreadCount": "609", 
    "SystemCache": "245121"
  }, 
  "System Status Cache": {
    "System Count": 2, 
    "blocked_count": 0, 
    "leader_count": 2, 
    "normal_count": 0, 
    "receive_backward_count": 1, 
    "receive_forward_count": 0, 
    "receive_none_count": 0, 
    "receive_ok_count": 1, 
    "send_backward_count": 1, 
    "send_forward_count": 1, 
    "send_none_count": 0, 
    "send_ok_count": 0, 
    "slowlink_count": 1, 
    "version_details_5.1.314.7724": "count: 1 filtered: 1", 
    "version_details_5.1.314.7778": "count: 1 filtered: 0", 
    "version_details_6.0.314.1195": "count: 2 filtered: 1"
  }
}
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Fri Aug  7 15:34:34 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**