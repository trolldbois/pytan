Print Sensor Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Print Sensor Help](#user-content-print-sensor-help)
  * [Print the server info](#user-content-print-the-server-info)

---------------------------

# Print Sensor Help

  * Prints sensor information to stdout

```bash
print_sensor.py -h
```

```
usage: print_sensor.py [-h] [-u USERNAME] [-p PASSWORD] [--host HOST]
                       [--port PORT] [-l LOGLEVEL] [--all] [--id ID]
                       [--name NAME] [--hash HASH] [--category CATEGORIES]
                       [--platform PLATFORMS] [--hide_params] [--params_only]
                       [--json]

Prints sensor information to stdout

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

Get Sensor Options:
  --all                 Get all sensors (default: False)
  --id ID               id of sensor to get (default: [])
  --name NAME           name of sensor to get (default: [])
  --hash HASH           hash of sensor to get (default: [])

Output Options:
  --category CATEGORIES
                        Only show sensors in given category (default: [])
  --platform PLATFORMS  Only show sensors for given platform (default: [])
  --hide_params         Do not show parameters in output (default: False)
  --params_only         Only show sensors with parameters (default: False)
  --json                Show a json dump of the server information (default:
                        False)
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


# Print the server info

```bash
print_server_info.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
Diagnostics: 
  Action History Cache: 
    Action Stop Count: 0
    Actions: 348
  Active Question Cache: 
    Active Client Estimate: 2
    Active Question Estimate: 91
  Authenticator: 
    TotalSessions: 1893
    ActiveSessions: 1
    OldSessions: 0
  Data Interface: 
    Sensor Bytes Per Second Limit: 0
    Reg Connection Count: 0
    Sensor Connection Limit: 0
    Sensor Connection Count: 0
    License Seat Cap: 60
    Sensor Bytes Sent Since Last Time: 0
    Estimated Node Count: 2
    Reg Connection Limit: 1000
  File Request Handler: 
    Download Connection Limit: 1000
    Download Connection Count: 0
  Group Cache: 
    GroupsTempSensors: 28
    QuestionSubGroups: 2929
    QuestionFilterSpecs: 128
    SavedQuestionTextCount: 193
    GroupCount: 1456
    QuestionTextCount: 0
    FilterSpecCount: 297
    QuestionSelectSpecs: 6262
    SelectSpecCount: 4077
  Network: 
    Allocated SendOp Count: 1609
    Concurrency Threads: 34
    SendOpReady HeadCount: 1609
    Min Available Threads: 0
    Allocated SendOp Limit: 0
    SendOpReady FreeCount: 0
    Idle Threads: 34
    Pending SendOp Count: 0
    Unpaused Threads: 34
    Running Threads: 34
    Concurrency: 32
    Queue Completion Timeout: 1000
    Threads Reset Interval: 0
  Package Cache: 
    Package Count: 132
    Package File Count: 508
  Plugin Cache: 
    Plugin Definition Count: 9
  Question History: 
    History Limit Days: 7
    Last Question ID: 11478
    Last Saved Question ID: 196
    Question Count: 6128
  SOAP Network: 
    Allocated SendOp Count: 2
    Concurrency Threads: 10
    SendOpReady HeadCount: 2
    Min Available Threads: 0
    Allocated SendOp Limit: 0
    SendOpReady FreeCount: 0
    Idle Threads: 9
    Pending SendOp Count: 0
    Unpaused Threads: 10
    Running Threads: 10
    Concurrency: 8
    Queue Completion Timeout: 1000
    Threads Reset Interval: 0
  SOAP Server: 
    Connections: 1
    SOAP Handlers: 3
    Use Compression: 1
    Using IPv6: 1
  SOAP Snapshots: 
    Snapshot Count: 27
  Sensor Cache: 
    Preview Sensor Count: 0
    Active Preview Sensor Count: 0
    Sensor Count: 855
  String Cache: 
    NameData: 831
    Total String Count: 1725405
  Settings: 
    UseTBBScalingAlignment: [unset]
    Client Count: 4
    ServerName: 0.0.0.0
    ServerSOAPPort: 444
    AllowOldSessionID: [unset]
    UseSOAPIOCP: [unset]
    Version: 6.2.314.3258
    ServerPort: 17472
    UseTBBAllocator: [unset]
    PreFetchRows: 1000
    UseTBBAllocatorStats: [unset]
  Memory Info: 
    NonTBBFreeCount: 0
    QuotaPagedPoolUsage: 811800
    QuotaPeakPagedPoolUsage: 811992
    PageFaultCount: 9454210
    PeakWorkingSetSize: 505.44 MB
    QuotaPeakNonPagedPoolUsage: 5986396
    PeakPagefileUsage: 1383944192
    PagefileUsage: 1366851584
    DoubleFreeCount: 0
    WorkingSetSize: 451.05 MB
  System Performance Info: 
    PhysicalTotal: 1048429
    PageSize: 4096
    HandleCount: 25688
    KernelPaged: 49807
    CommitTotal: 784989
    ProcessThreadCount: 689
    SystemCache: 356655
    CommitPeak: 1012866
    PhysicalAvailable: 471032
    ProcessCount: 48
    KernelTotal: 77129
    KernelNonpaged: 27322
    CommitLimit: 2096393
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Wed Feb 11 17:18:08 2015 EST, Contact info: **Jim Olsen <jim.olsen@tanium.com>**