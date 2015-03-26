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
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
Diagnostics: 
  Action History Cache: 
    Action Stop Count: 0
    Actions: 2017
  Active Question Cache: 
    Active Client Estimate: 2
    Active Question Estimate: 38
  Authenticator: 
    TotalSessions: 377
    ActiveSessions: 1
    OldSessions: 0
  Data Interface: 
    Sensor Bytes Per Second Limit: 5242880
    Reg Connection Count: 0
    Sensor Connection Limit: 8
    Sensor Connection Count: 0
    License Seat Cap: 60
    Sensor Bytes Sent Since Last Time: 0
    Estimated Node Count: 2
    Reg Connection Limit: 1000
  File Request Handler: 
    Download Connection Limit: 1000
    Download Connection Count: 0
  Group Cache: 
    GroupsTempSensors: 7
    QuestionSubGroups: 3746
    QuestionFilterSpecs: 93
    SavedQuestionTextCount: 184
    GroupCount: 3635
    QuestionTextCount: 0
    FilterSpecCount: 4496
    QuestionSelectSpecs: 2076
    SelectSpecCount: 7343
  Network: 
    Allocated SendOp Count: 767
    Concurrency Threads: 34
    SendOpReady HeadCount: 767
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
    Package Count: 465
    Package File Count: 571
  Plugin Cache: 
    Plugin Definition Count: 9
  Question History: 
    History Limit Days: 7
    Last Question ID: 32494
    Last Saved Question ID: 11656
    Question Count: 1887
  SOAP Network: 
    Allocated SendOp Count: 1
    Concurrency Threads: 10
    SendOpReady HeadCount: 1
    Min Available Threads: 6
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
    SOAP Handlers: 2
    Use Compression: 1
    Using IPv6: 1
  SOAP Snapshots: 
    Snapshot Count: 26
  Sensor Cache: 
    Preview Sensor Count: 0
    Active Preview Sensor Count: 0
    Sensor Count: 667
  String Cache: 
    NameData: 824
    Total String Count: 346376
  Settings: 
    UseTBBScalingAlignment: [unset]
    Client Count: 5
    ServerName: 0.0.0.0
    ServerSOAPPort: 444
    AllowOldSessionID: [unset]
    UseSOAPIOCP: [unset]
    Version: 6.2.314.3279
    ServerPort: 17472
    UseTBBAllocator: [unset]
    PreFetchRows: 1000
    UseTBBAllocatorStats: [unset]
  Memory Info: 
    NonTBBFreeCount: 0
    QuotaPagedPoolUsage: 556680
    QuotaPeakPagedPoolUsage: 556872
    PageFaultCount: 1546894
    PeakWorkingSetSize: 374.20 MB
    QuotaPeakNonPagedPoolUsage: 3915784
    PeakPagefileUsage: 773259264
    PagefileUsage: 765468672
    DoubleFreeCount: 0
    WorkingSetSize: 274.84 MB
  System Performance Info: 
    PhysicalTotal: 1048429
    PageSize: 4096
    HandleCount: 22161
    KernelPaged: 51899
    CommitTotal: 533104
    ProcessThreadCount: 680
    SystemCache: 328056
    CommitPeak: 541503
    PhysicalAvailable: 642597
    ProcessCount: 46
    KernelTotal: 69403
    KernelNonpaged: 17504
    CommitLimit: 2096394
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Thu Mar 26 09:28:44 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**