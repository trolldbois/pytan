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
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
{
  "Diagnostics": [
    {
      "Action History Cache": {
        "Action Stop Count": "0", 
        "Actions": "348"
      }
    }, 
    {
      "Active Question Cache": {
        "Active Client Estimate": "2", 
        "Active Question Estimate": "91"
      }
    }, 
    {
      "Authenticator": {
        "ActiveSessions": "1", 
        "OldSessions": "0", 
        "TotalSessions": "1895"
      }
    }, 
    {
      "Data Interface": {
        "Estimated Node Count": "2", 
        "License Seat Cap": "60", 
        "Reg Connection Count": "0", 
        "Reg Connection Limit": "1000", 
        "Sensor Bytes Per Second Limit": "0", 
        "Sensor Bytes Sent Since Last Time": "0", 
        "Sensor Connection Count": "0", 
        "Sensor Connection Limit": "0"
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
        "FilterSpecCount": "297", 
        "GroupCount": "1456", 
        "GroupsTempSensors": "28", 
        "QuestionFilterSpecs": "128", 
        "QuestionSelectSpecs": "6262", 
        "QuestionSubGroups": "2929", 
        "QuestionTextCount": "0", 
        "SavedQuestionTextCount": "193", 
        "SelectSpecCount": "4077"
      }
    }, 
    {
      "Network": {
        "Allocated SendOp Count": "1609", 
        "Allocated SendOp Limit": "0", 
        "Concurrency": "32", 
        "Concurrency Threads": "34", 
        "Idle Threads": "34", 
        "Min Available Threads": "0", 
        "Pending SendOp Count": "0", 
        "Queue Completion Timeout": "1000", 
        "Running Threads": "34", 
        "SendOpReady FreeCount": "0", 
        "SendOpReady HeadCount": "1609", 
        "Threads Reset Interval": "0", 
        "Unpaused Threads": "34"
      }
    }, 
    {
      "Package Cache": {
        "Package Count": "132", 
        "Package File Count": "508"
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
        "Last Question ID": "11478", 
        "Last Saved Question ID": "196", 
        "Question Count": "6128"
      }
    }, 
    {
      "SOAP Network": {
        "Allocated SendOp Count": "2", 
        "Allocated SendOp Limit": "0", 
        "Concurrency": "8", 
        "Concurrency Threads": "10", 
        "Idle Threads": "9", 
        "Min Available Threads": "0", 
        "Pending SendOp Count": "0", 
        "Queue Completion Timeout": "1000", 
        "Running Threads": "10", 
        "SendOpReady FreeCount": "0", 
        "SendOpReady HeadCount": "2", 
        "Threads Reset Interval": "0", 
        "Unpaused Threads": "10"
      }
    }, 
    {
      "SOAP Server": {
        "Connections": "1", 
        "SOAP Handlers": "3", 
        "Use Compression": "1", 
        "Using IPv6": "1"
      }
    }, 
    {
      "SOAP Snapshots": {
        "Snapshot Count": "27"
      }
    }, 
    {
      "Sensor Cache": {
        "Active Preview Sensor Count": "0", 
        "Preview Sensor Count": "0", 
        "Sensor Count": "855"
      }
    }, 
    {
      "String Cache": {
        "NameData": "831", 
        "Total String Count": "1725405"
      }
    }, 
    {
      "Settings": {
        "AllowOldSessionID": "[unset]", 
        "Client Count": "4", 
        "PreFetchRows": "1000", 
        "ServerName": "0.0.0.0", 
        "ServerPort": "17472", 
        "ServerSOAPPort": "444", 
        "UseSOAPIOCP": "[unset]", 
        "UseTBBAllocator": "[unset]", 
        "UseTBBAllocatorStats": "[unset]", 
        "UseTBBScalingAlignment": "[unset]", 
        "Version": "6.2.314.3258"
      }
    }, 
    {
      "Memory Info": {
        "DoubleFreeCount": "0", 
        "NonTBBFreeCount": "0", 
        "PageFaultCount": "9454212", 
        "PagefileUsage": "1366851584", 
        "PeakPagefileUsage": "1383944192", 
        "PeakWorkingSetSize": "505.44 MB", 
        "QuotaPagedPoolUsage": "811800", 
        "QuotaPeakNonPagedPoolUsage": "5986396", 
        "QuotaPeakPagedPoolUsage": "811992", 
        "WorkingSetSize": "451.05 MB"
      }
    }, 
    {
      "System Performance Info": {
        "CommitLimit": "2096393", 
        "CommitPeak": "1012866", 
        "CommitTotal": "784988", 
        "HandleCount": "25689", 
        "KernelNonpaged": "27322", 
        "KernelPaged": "49807", 
        "KernelTotal": "77129", 
        "PageSize": "4096", 
        "PhysicalAvailable": "471026", 
        "PhysicalTotal": "1048429", 
        "ProcessCount": "48", 
        "ProcessThreadCount": "689", 
        "SystemCache": "356655"
      }
    }
  ]
}
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Wed Feb 11 17:18:09 2015 EST, Contact info: **Jim Olsen <jim.olsen@tanium.com>**