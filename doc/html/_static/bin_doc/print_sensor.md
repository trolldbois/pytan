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
    Actions: 27
  Active Question Cache: 
    Active Client Estimate: 6
    Active Question Estimate: 75
  Authenticator: 
    TotalSessions: 332
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
    GroupsTempSensors: 9
    QuestionSubGroups: 115
    QuestionFilterSpecs: 2
    SavedQuestionTextCount: 177
    GroupCount: 283
    QuestionTextCount: 0
    FilterSpecCount: 144
    QuestionSelectSpecs: 270
    SelectSpecCount: 488
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
    Package Count: 98
    Package File Count: 194
  Plugin Cache: 
    Plugin Definition Count: 9
  Question History: 
    History Limit Days: 7
    Last Question ID: 271
    Last Saved Question ID: 177
    Question Count: 98
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
    Sensor Count: 463
  String Cache: 
    NameData: 823
    Total String Count: 200933
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
    QuotaPagedPoolUsage: 423888
    QuotaPeakPagedPoolUsage: 424176
    PageFaultCount: 359839
    PeakWorkingSetSize: 371.47 MB
    QuotaPeakNonPagedPoolUsage: 7148584
    PeakPagefileUsage: 688590848
    PagefileUsage: 684810240
    DoubleFreeCount: 0
    WorkingSetSize: 368.34 MB
  System Performance Info: 
    PhysicalTotal: 1048429
    PageSize: 4096
    HandleCount: 21374
    KernelPaged: 47406
    CommitTotal: 594551
    ProcessThreadCount: 688
    SystemCache: 412123
    CommitPeak: 1066170
    PhysicalAvailable: 522634
    ProcessCount: 46
    KernelTotal: 69032
    KernelNonpaged: 21626
    CommitLimit: 2096392
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Mon Dec  8 15:02:33 2014 EST, Contact info: **Jim Olsen <jim.olsen@tanium.com>**