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
                        444)

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
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
{
  "Diagnostics": [
    {
      "Action History Cache": {
        "Action Stop Count": "0", 
        "Actions": "2017"
      }
    }, 
    {
      "Active Question Cache": {
        "Active Client Estimate": "2", 
        "Active Question Estimate": "38"
      }
    }, 
    {
      "Authenticator": {
        "ActiveSessions": "1", 
        "OldSessions": "0", 
        "TotalSessions": "379"
      }
    }, 
    {
      "Data Interface": {
        "Estimated Node Count": "2", 
        "License Seat Cap": "60", 
        "Reg Connection Count": "0", 
        "Reg Connection Limit": "1000", 
        "Sensor Bytes Per Second Limit": "5242880", 
        "Sensor Bytes Sent Since Last Time": "0", 
        "Sensor Connection Count": "0", 
        "Sensor Connection Limit": "8"
      }
    }, 
    {
      "File Request Handler": {
        "Download Connection Count": "0", 
        "Download Connection Limit": "1000"
      }
    }, 
    {
      "Group Cache": {
        "FilterSpecCount": "4496", 
        "GroupCount": "3635", 
        "GroupsTempSensors": "7", 
        "QuestionFilterSpecs": "93", 
        "QuestionSelectSpecs": "2076", 
        "QuestionSubGroups": "3746", 
        "QuestionTextCount": "0", 
        "SavedQuestionTextCount": "184", 
        "SelectSpecCount": "7343"
      }
    }, 
    {
      "Network": {
        "Allocated SendOp Count": "767", 
        "Allocated SendOp Limit": "0", 
        "Concurrency": "32", 
        "Concurrency Threads": "34", 
        "Idle Threads": "34", 
        "Min Available Threads": "0", 
        "Pending SendOp Count": "0", 
        "Queue Completion Timeout": "1000", 
        "Running Threads": "34", 
        "SendOpReady FreeCount": "0", 
        "SendOpReady HeadCount": "767", 
        "Threads Reset Interval": "0", 
        "Unpaused Threads": "34"
      }
    }, 
    {
      "Package Cache": {
        "Package Count": "465", 
        "Package File Count": "571"
      }
    }, 
    {
      "Plugin Cache": {
        "Plugin Definition Count": "9"
      }
    }, 
    {
      "Question History": {
        "History Limit Days": "7", 
        "Last Question ID": "32494", 
        "Last Saved Question ID": "11656", 
        "Question Count": "1887"
      }
    }, 
    {
      "SOAP Network": {
        "Allocated SendOp Count": "1", 
        "Allocated SendOp Limit": "0", 
        "Concurrency": "8", 
        "Concurrency Threads": "10", 
        "Idle Threads": "9", 
        "Min Available Threads": "6", 
        "Pending SendOp Count": "0", 
        "Queue Completion Timeout": "1000", 
        "Running Threads": "10", 
        "SendOpReady FreeCount": "0", 
        "SendOpReady HeadCount": "1", 
        "Threads Reset Interval": "0", 
        "Unpaused Threads": "10"
      }
    }, 
    {
      "SOAP Server": {
        "Connections": "1", 
        "SOAP Handlers": "2", 
        "Use Compression": "1", 
        "Using IPv6": "1"
      }
    }, 
    {
      "SOAP Snapshots": {
        "Snapshot Count": "26"
      }
    }, 
    {
      "Sensor Cache": {
        "Active Preview Sensor Count": "0", 
        "Preview Sensor Count": "0", 
        "Sensor Count": "667"
      }
    }, 
    {
      "String Cache": {
        "NameData": "824", 
        "Total String Count": "346376"
      }
    }, 
    {
      "Settings": {
        "AllowOldSessionID": "[unset]", 
        "Client Count": "5", 
        "PreFetchRows": "1000", 
        "ServerName": "0.0.0.0", 
        "ServerPort": "17472", 
        "ServerSOAPPort": "444", 
        "UseSOAPIOCP": "[unset]", 
        "UseTBBAllocator": "[unset]", 
        "UseTBBAllocatorStats": "[unset]", 
        "UseTBBScalingAlignment": "[unset]", 
        "Version": "6.2.314.3279"
      }
    }, 
    {
      "Memory Info": {
        "DoubleFreeCount": "0", 
        "NonTBBFreeCount": "0", 
        "PageFaultCount": "1546897", 
        "PagefileUsage": "765468672", 
        "PeakPagefileUsage": "773259264", 
        "PeakWorkingSetSize": "374.20 MB", 
        "QuotaPagedPoolUsage": "556680", 
        "QuotaPeakNonPagedPoolUsage": "3915784", 
        "QuotaPeakPagedPoolUsage": "556872", 
        "WorkingSetSize": "274.84 MB"
      }
    }, 
    {
      "System Performance Info": {
        "CommitLimit": "2096394", 
        "CommitPeak": "541503", 
        "CommitTotal": "533103", 
        "HandleCount": "22158", 
        "KernelNonpaged": "17504", 
        "KernelPaged": "51899", 
        "KernelTotal": "69403", 
        "PageSize": "4096", 
        "PhysicalAvailable": "642591", 
        "PhysicalTotal": "1048429", 
        "ProcessCount": "46", 
        "ProcessThreadCount": "680", 
        "SystemCache": "328086"
      }
    }
  ]
}
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Thu Mar 26 09:28:44 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**