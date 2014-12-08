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
usage: print_sensor.py [-h] -u USERNAME -p PASSWORD --host HOST [--port PORT]
                       [-l LOGLEVEL] [--all] [--id ID] [--name NAME]
                       [--hash HASH] [--category CATEGORIES]
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
    Actions: 39
  Active Question Cache: 
    Active Client Estimate: 6
    Active Question Estimate: 45
  Authenticator: 
    TotalSessions: 746
    ActiveSessions: 1
    OldSessions: 0
  Data Interface: 
    Sensor Bytes Per Second Limit: 0
    Reg Connection Count: 0
    Sensor Connection Limit: 0
    Sensor Connection Count: 0
    License Seat Cap: 60
    Sensor Bytes Sent Since Last Time: 0
    Estimated Node Count: 6
    Reg Connection Limit: 1000
  File Request Handler: 
    Download Connection Limit: 1000
    Download Connection Count: 0
  Group Cache: 
    GroupsTempSensors: 13
    QuestionSubGroups: 169
    QuestionFilterSpecs: 3
    SavedQuestionTextCount: 179
    GroupCount: 344
    QuestionTextCount: 0
    FilterSpecCount: 164
    QuestionSelectSpecs: 353
    SelectSpecCount: 621
  Network: 
    Allocated SendOp Count: 1699
    Concurrency Threads: 34
    SendOpReady HeadCount: 1699
    Min Available Threads: 30
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
    Package Count: 104
    Package File Count: 234
  Plugin Cache: 
    Plugin Definition Count: 9
  Question History: 
    History Limit Days: 7
    Last Question ID: 354
    Last Saved Question ID: 179
    Question Count: 181
  SOAP Network: 
    Allocated SendOp Count: 3
    Concurrency Threads: 10
    SendOpReady HeadCount: 3
    Min Available Threads: 7
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
    Snapshot Count: 27
  Sensor Cache: 
    Preview Sensor Count: 0
    Active Preview Sensor Count: 0
    Sensor Count: 508
  String Cache: 
    NameData: 824
    Total String Count: 239021
  Settings: 
    UseTBBScalingAlignment: [unset]
    Client Count: 6
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
    QuotaPagedPoolUsage: 427984
    QuotaPeakPagedPoolUsage: 428176
    PageFaultCount: 570113
    PeakWorkingSetSize: 401.77 MB
    QuotaPeakNonPagedPoolUsage: 7148584
    PeakPagefileUsage: 750006272
    PagefileUsage: 741257216
    DoubleFreeCount: 0
    WorkingSetSize: 222.46 MB
  System Performance Info: 
    PhysicalTotal: 1048429
    PageSize: 4096
    HandleCount: 21831
    KernelPaged: 48434
    CommitTotal: 624629
    ProcessThreadCount: 682
    SystemCache: 472583
    CommitPeak: 1066170
    PhysicalAvailable: 529425
    ProcessCount: 47
    KernelTotal: 70096
    KernelNonpaged: 21662
    CommitLimit: 2096392
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Mon Dec  8 15:35:55 2014 EST, Contact info: **Jim Olsen <jim.olsen@tanium.com>**