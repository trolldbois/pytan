Print Sensors Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Help for Print Sensors](#user-content-help-for-print-sensors)
  * [Print all sensors](#user-content-print-all-sensors)
  * [Print all Linux sensors](#user-content-print-all-linux-sensors)
  * [Print all Linux sensors that fall under the category "Operating System"](#user-content-print-all-linux-sensors-that-fall-under-the-category-"operating-system")
  * [Print all Mac and Windows sensors that fall under the category "User"](#user-content-print-all-mac-and-windows-sensors-that-fall-under-the-category-"user")

---------------------------

# Help for Print Sensors

  * Print the help for print_sensors.py
  * All scripts in bin/ will supply help if -h is on the command line
  * If passing in a parameter with a space or a special character, you need to surround it with quotes properly. On Windows this means double quotes. On Linux/Mac, this means single or double quotes, depending on what kind of character escaping you need.
  * If running this script on Linux or Mac, use the python scripts directly as the bin/print_sensors.py
  * If running this script on Windows, use the batch script in the winbin/print_sensors.bat so that python is called correctly.

```bash
print_sensors.py -h
```

```
usage: print_sensors.py [-h] [-u USERNAME] [-p PASSWORD]
                        [--session_id SESSION_ID] [--host HOST] [--port PORT]
                        [-l LOGLEVEL] [--debugformat] [--debug_method_locals]
                        [--record_all_requests] [--stats_loop_enabled]
                        [--http_auth_retry]
                        [--http_retry_count HTTP_RETRY_COUNT]
                        [--pytan_user_config PYTAN_USER_CONFIG]
                        [--force_server_version FORCE_SERVER_VERSION] [--all]
                        [--id ID] [--name NAME] [--hash HASH]
                        [--category CATEGORIES] [--platform PLATFORMS]
                        [--hide_params] [--params_only] [--json]

Collection of classes and methods used throughout :mod:`pytan` for command line support

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

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Print all sensors

```bash
bin/print_sensors.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --all
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
Found items:  SensorList, len: 567
Filtered out sourced sensors: 332
Filtered out sensors based on user filters: 332

  * Sensor Name: 'AD Organizational Unit', Platforms: Windows, Category: Active Directory
  * Description: The Active Directory organizational unit (OU) where the machine is located. Example: CN=Computers,DC=corp,DC=com

  * Sensor Name: 'AD Computer Groups', Platforms: Windows, Category: Active Directory
  * Description: All computer groups (if any) that a computer is a member of in Active Directory. Example: Berkeley Workstations

  * Sensor Name: 'Domain Controller SYSVOL Size', Platforms: Windows, Category: Active Directory
  * Description: Returns the SYSVOL size on Domain Controllers Example: 2.2 GB

  * Sensor Name: 'AD Short Domain', Platforms: Windows, Category: Active Directory
  * Description: Returns the short, NetBIOS name of a machine's domain. Example: CORP

  * Sensor Name: 'AD Distinguished Name', Platforms: Windows, Category: Active Directory
  * Description: The full Active Directory distinguished name for the computer Example: CN=Win8-test5,CN=Computers,DC=corp,DC=com

  * Sensor Name: 'AD Forest', Platforms: Windows, Category: Active Directory
  * Description: Returns the name of the Active Directory Forest that a machine is a member of.  This may produce the same value that the Sensor named AD Domain produces. Example: corp.domain.com

  * Sensor Name: 'AD User Groups', Platforms: Windows, Category: Active Directory
  * Description: Any Active Directory groups that the currently logged in user is a member of. Example: CN=Domain Admins,CN=Users,DC=corp,DC=com

  * Sensor Name: 'AD Domain', Platforms: Windows, Category: Active Directory
  * Description: The Active Directory domain name (if any) that the computer is joined to. Example: intra.company.com

  * Sensor Name: 'Cached AD Logins', Platforms: Windows, Category: Active Directory
  * Description: Returns information on AD accounts which are logged in using cached credentials. Example:john.doe Cached - RDP

  * Sensor Name: 'Installed Applications', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Applications
  * Description: List of the applications and versions of those applications installed on the client machine. Example: Mozilla Firefox | 16.0.1

  * Sensor Name: 'Running Processes', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Applications
  * Description: Provides a list of processes currently running on the client machine. Example: svchost.exe

  * Sensor Name: 'Running Service', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Applications
  * Description: Provides a list of currently running services on the client machine. Example: DHCP Client

  * Sensor Name: 'Stopped Service', Platforms: Windows, Mac, Category: Applications
  * Description: Returns a list of all services currently stopped on the client machine. Example: DHCP Client

  * Sensor Name: 'Running Applications', Platforms: Windows, Category: Applications
  * Description: Provides a list of applications that are running at the present time on the client machine. Example: Google Chrome | 23.0.1271.64

  * Sensor Name: 'Application Crashes Yesterday', Platforms: Windows, Category: Applications
  * Description: A multi-column Sensor that shows processes that have crashed yesterday, including the instance number to capture multiple crashes by the same process. Example: firefox.exe | 3

  * Sensor Name: 'Application Crashes in Last X Days', Platforms: Windows, Category: Applications
  * Description: A parameterized Sensor that queries for any processes that have crashed in the last X days. Example: chrome.exe
  * Parameter 'days':
    - 'defaultValue': 5
    - 'helpString': Enter the number of days to query for Application Crashes
    - 'label': Number of Days
    - 'maximum': 365
    - 'minimum': 1
    - 'stepSize': 1
    - 'value': 5

  * Sensor Name: 'Internet Explorer Version', Platforms: Windows, Category: Applications
  * Description: Returns the version of Internet Explorer installed on a system. Example:8.0.6001.18702

  * Sensor Name: 'Service Details', Platforms: Windows, Category: Applications
  * Description: Details about all running services on the client machine, including name, display name, running status, and startup mode. Example: MDM | Machine Debug Manager | Running | Auto

  * Sensor Name: 'NET Version', Platforms: Windows, Category: Applications
  * Description: Returns the full versions numbers of all installed .NET.

  * Sensor Name: 'Last Application Launch Date', Platforms: Windows, Category: Applications
  * Description: Returns the date that each application was last launched on. Example: Notepad | 9/18/2012

  * Sensor Name: 'Stopped Service Short Name', Platforms: Windows, Category: Applications
  * Description: A list of the short names of all services currently in the stopped state. Example: defragsvc

  * Sensor Name: 'Installed Application Version', Platforms: Windows, Linux, Mac, AIX, Category: Applications
  * Description: The version string of applications which match the parameter given. Example:  11.5.502.146
  * Parameter 'application':
    - 'helpString': Enter the application name to search for
    - 'label': Application Name
    - 'promptText': e.g. Adobe Flash Player

  * Sensor Name: 'Default Web Browser', Platforms: Windows, Category: Applications
  * Description: Default web browser for new users.  Note that this can be changed per user. Example: Internet Explorer

  * Sensor Name: 'Internet Explorer Add-Ons', Platforms: Windows, Category: Applications
  * Description: List of add-ons to Internet Explorer and indicates whether they are a Toolbar, Extension, or Browser Helper Objects. Example: Java(tm) Plug-In SSV Helper|BHO

  * Sensor Name: 'Running Processes Memory Usage', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Applications
  * Description: Returns all running processes along with the memory each process uses.  This is the process's working set. Example: lsass.exe|23 MB

  * Sensor Name: 'Recently Run Applications', Platforms: Windows, Category: Applications
  * Description: Returns applications that have been launched in the last number of days supplied. Example: Microsoft Excel
  * Parameter 'days':
    - 'defaultValue': 7
    - 'helpString': Enter the number of previous days to search
    - 'label': Number of Previous Days to Search
    - 'maximum': 365
    - 'minimum': 1
    - 'stepSize': 1
    - 'value': 7
  * Parameter 'showDate':
    - 'helpString': Enter True or False whether to show the date.
    - 'label': Show Date?
    - 'requireSelection': True
    - 'values': [u'True', u'False']

  * Sensor Name: 'Installed Pkgs', Platforms: Linux, Mac, Solaris, AIX, Category: Applications
  * Description: Returns a list of installed Packages by name on Solaris systems. Example: glibc-2.5-12

  * Sensor Name: 'Application Run Time', Platforms: Windows, Linux, Solaris, AIX, Category: Applications
  * Description: Shows applications that are currently running and how long they have been running for. Example: Dropbox - 3 days

  * Sensor Name: 'Installed RPMs', Platforms: Linux, AIX, Category: Applications
  * Description: Returns a list of installed RPMs by name on Linux systems. Example: glibc-2.5-12

  * Sensor Name: 'Service', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Applications
  * Description: Gets a list of all Services on the client machine. Example: Task Scheduler

  * Sensor Name: 'Folder Exists', Platforms: Windows, Linux, Mac, Category: File System
  * Description: A parameterized Sensor that checks to see if a folder exists on a machine.  If it does, it returns back the full path of the folder. Will expand environment variables, and will expand %userprofile%/folder or "~/folder" to search all user home directories. Example: C:\Windows\system32
  * Parameter 'folder':
    - 'helpString': Enter the full drive letter and folder path of the folder. Environment variables accepted.
    - 'label': Folder path to search for
    - 'promptText': e.g. c:\Program Files\MyApp

  * Sensor Name: 'File Version', Platforms: Windows, Category: File System
  * Description: Returns the version of the file specified. Example: 1.0
  * Parameter 'file':
    - 'helpString': Enter the full drive letter, folder path and file name of the file.
    - 'label': File path and name
    - 'promptText': c:\windows\test.txt

  * Sensor Name: 'Physical Volumes', Platforms: Linux, AIX, Category: File System
  * Description: 

  * Sensor Name: 'Path Permissions', Platforms: Windows, Category: File System
  * Description: Returns the permissions of the given file or folder path Example:  NT AUTHORITY\SYSTEM (I)(F)
  * Parameter 'file':
    - 'label': The path to the file or folder permissions to return.
    - 'promptText': File or Folder Path

  * Sensor Name: 'Volume Group Names', Platforms: Linux, Category: File System
  * Description: Display Volume Group Names

  * Sensor Name: 'File Creation Date', Platforms: Windows, Mac, Category: File System
  * Description: Returns the creation date of the file specified by the parameter. Example: 12-12-2014 18:00
  * Parameter 'filepath':
    - 'helpString': Enter the file path of which to return the creation date.  Only %userprofile% is acceptable to loop through user directories.
    - 'label': File path and name to search for
    - 'promptText': e.g. c:\windows\test.txt, or %userprofile%\test.txt

  * Sensor Name: 'File Exists', Platforms: Windows, Linux, Mac, Category: File System
  * Description: A parameterized Sensor that checks to see if a file exists on a machine.  If it does, it returns back the full path of the file. Will expand environment variables, and will expand %userprofile%/file or "~/file" to search all user home directories. Example: C:\Windows\system32\notepad.exe
  * Parameter 'file':
    - 'helpString': Enter the file path and name to search for.
    - 'label': File path and name to search for
    - 'promptText': e.g. c:\windows\test.txt

  * Sensor Name: 'Folder Contents', Platforms: Windows, Category: File System
  * Description: Returns the contents of the specified folder. Example: 0.log
  * Parameter 'folderPath':
    - 'helpString': Enter the full drive letter and folder path of the folder. Only %userprofile% is acceptable to loop through user directories.
    - 'label': Folder path to search for
    - 'promptText': e.g. c:\Temp, or %userprofile%\Desktop

  * Sensor Name: 'File Modification Date', Platforms: Windows, Category: File System
  * Description: Returns the modification date of the file specified by the parameter. Example: 12/12/2014 18:00
  * Parameter 'filepath':
    - 'helpString': Enter the file path of which to return the modification date.  Only %userprofile% is acceptable to loop through user directories.
    - 'label': File path and name to search for
    - 'promptText': e.g. c:\windows\test.txt, or %userprofile%\test.txt

  * Sensor Name: 'Logical Volumes', Platforms: Linux, AIX, Category: File System
  * Description: Display Logical Volume Names

  * Sensor Name: 'File Size', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: File System
  * Description: Returns the size of the file specified by the parameter. Example: 69120
  * Parameter 'filename':
    - 'helpString': Enter the full drive letter, folder path and file name of the file.
    - 'label': File name to search for
    - 'promptText': e.g. c:\windows\test.txt

  * Sensor Name: 'Folder Size', Platforms: Windows, Category: File System
  * Description: Folder size (in GB, MB, KB, or B) Example: 62 GB
  * Parameter 'strFolder':
    - 'helpString': Enter the full drive letter and folder path of the folder
    - 'label': Folder path to search for
    - 'promptText': e.g. c:\Program Files\MyApp

  * Sensor Name: 'Is Virtual', Platforms: Windows, Mac, Solaris, AIX, Category: Hardware
  * Description: Returns Yes or No to indicate whether the hardware is virtual. Echo: Yes

  * Sensor Name: 'USB Storage Devices', Platforms: Windows, Linux, Category: Hardware
  * Description: Returns a list of USB storage devices currently plugged in to the client machine. Example: USB Mass Storage Device

  * Sensor Name: 'CPU Speed Mhz', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: The speed of the processor in Mhz. Example: 3200 Mhz

  * Sensor Name: 'CPU Consumption', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: Current total CPU consumption in %. Example: 50%

  * Sensor Name: 'Disk Free Space Below Threshold', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: If a drive has less free space than the configured threshold, the drive and remaining free space is returned.  The threshold defaults to 2048 MB and can be altered. Example: C: 1 GB

  * Sensor Name: 'RAM', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: Returns the total amount of installed RAM, in Megabytes. Example: 2048 MB

  * Sensor Name: 'Chassis Type', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: The machine or chassis type for the machine. Example: Server or Virtual

  * Sensor Name: 'Monitor Details', Platforms: Windows, Mac, Category: Hardware
  * Description: Returns details of attached physical monitors. Example: Model Name, Serial Number, VESA Manufacturer ID, Manufacture Date

  * Sensor Name: 'CPU Details', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: A multi-column sensor that provides CPU details: system type, CPU description, speed, # of processors, # of cores, and # of logical processors. Example: x64-based PC | Intel(R) Xeon(R) CPU X3430 | 2390 Mhz | 1 | 4 | 4

  * Sensor Name: 'Disk Drives', Platforms: Windows, Mac, Solaris, Category: Hardware
  * Description: Descriptions of any installed disk drives, including external or USB drives. Example: ST3808110AS ATA Device

  * Sensor Name: 'Disk Total Space', Platforms: Windows, Linux, Mac, AIX, Category: Hardware
  * Description: The amount of total disk space per drive. Example: C: 100 GB

  * Sensor Name: 'Disk Free Space', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: The amount of free disk space per drive. Example: C: 40 GB

  * Sensor Name: 'Disk Used Percentage', Platforms: Windows, Linux, Mac, AIX, Category: Hardware
  * Description: The percentage of used disk space per partition. Example: C: 24%

  * Sensor Name: 'BIOS Name', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: Name of BIOS. Example: Phoenix ROM BIOS PLUS Version 1.10 A10

  * Sensor Name: 'BIOS Release Date', Platforms: Windows, Linux, Mac, AIX, Category: Hardware
  * Description: Release date of the BIOS. Example: 20080436.2.314..016400+000

  * Sensor Name: 'BIOS Version', Platforms: Windows, Linux, AIX, Category: Hardware
  * Description: Version of the BIOS. Example: A11

  * Sensor Name: 'Computer Serial Number', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: The serial number, if available, provided by the computer manufacturer. Example: 123ABC1

  * Sensor Name: 'Virtual Platform', Platforms: Windows, Solaris, AIX, Category: Hardware
  * Description: Returns the virtual platform or technology used for the virtual machine, if it is a virtual machine. Example: VMware

  * Sensor Name: 'Free Memory', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: Indicates the free RAM available to the operating system. Example: 1024MB

  * Sensor Name: 'Used Memory', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: Memory in use in MB from client machine. Example: 6348 MB

  * Sensor Name: 'Printers', Platforms: Windows, Category: Hardware
  * Description: Returns printers connected to a system. Example:HP LaserJet 4400c

  * Sensor Name: 'Onboard Devices', Platforms: Windows, Category: Hardware
  * Description: Returns the name of any device which is built into the motherboard. Example: ES1371

  * Sensor Name: 'USB Device', Platforms: Windows, Category: Hardware
  * Description: Returns a list of USB devices currently plugged in to the client machine. Example: HID Keyboard Device

  * Sensor Name: 'Sound Card', Platforms: Windows, Mac, Category: Hardware
  * Description: Name of sound card in client machine. Example: SoundMAX Integrated Digital HD Audio

  * Sensor Name: 'BIOS Vendor', Platforms: Windows, Linux, AIX, Category: Hardware
  * Description: Manufacturer or vendor of the BIOS. Example: Dell, Inc.

  * Sensor Name: 'Disk Drive Details', Platforms: Windows, Category: Hardware
  * Description: Multi-column sensor that returns details on the type, size, and free space of all partitions on the machine. Example:ST3808110AS ATA Device|C:|250G|120G

  * Sensor Name: 'High Memory Consumption', Platforms: Windows, Category: Hardware
  * Description: Indicates whether the machine is above an acceptable threshold for memory utilization. Example: Under threshold

  * Sensor Name: 'x64/x86?', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: Returns whether the client machine is 64-bit or 32-bit (x86). Example: X86-based PC

  * Sensor Name: 'Ram Slots Unused', Platforms: Windows, Category: Hardware
  * Description: Returns the number of empty, unused RAM slots. Example:2

  * Sensor Name: 'Network Printers', Platforms: Windows, Category: Hardware
  * Description: Returns printers which are connected via Network Example: HP LaserJet 4400c

  * Sensor Name: 'Audio Controller', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: Description of the onboard audio controller for the computer. Example: Intel(R) High Definition Audio Controller

  * Sensor Name: 'Active Devices', Platforms: Windows, Category: Hardware
  * Description: All hardware devices currently in use by a computer. Example: Microsoft PS/2 Mouse

  * Sensor Name: 'CPU Manufacturer', Platforms: Windows, Linux, Mac, Solaris, Category: Hardware
  * Description: The manufacturer of the CPU. Example: GenuineIntel

  * Sensor Name: 'Monitor Resolution', Platforms: Windows, Category: Hardware
  * Description: Returns details about connected displays. Example:1024 by 768 pixels, True Color, 60 Hertz

  * Sensor Name: 'Predicted Disk Failures', Platforms: Windows, Category: Hardware
  * Description: Returns drives and the S.M.A.R.T. status of the drives on machines which have a failing drive reporting through S.M.A.R.T. Example: Drive | SMART Report

  * Sensor Name: 'CPU Architecture', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: Describes the architecture of the CPU/processor. Example: i386, X86-based PC

  * Sensor Name: 'Default Printer', Platforms: Windows, Category: Hardware
  * Description: Name of the default printer. Example: HP Color LaserJet 3500

  * Sensor Name: 'Manufacturer', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: Returns System or Motherboard manufacturer (OS Dependent). Example: Apple

  * Sensor Name: 'Motherboard Name', Platforms: Windows, Linux, Category: Hardware
  * Description: Returns the motherboard product name of a system. Example: 440BX Desktop Reference Platform

  * Sensor Name: 'Video Graphics Card RAM', Platforms: Windows, Category: Hardware
  * Description: Amount of RAM in the video card in the client machine. Example: 256MB

  * Sensor Name: 'Local Printers', Platforms: Windows, Category: Hardware
  * Description: Returns printers which are not connected via Network Example: HP LaserJet 4400c

  * Sensor Name: 'BIOS Current Language', Platforms: Windows, Category: Hardware
  * Description: Currently configured language for the BIOS. Example: en|US|iso8859-1

  * Sensor Name: 'Network Adapter Name', Platforms: Windows, Linux, Solaris, AIX, Category: Hardware
  * Description: Returns the names of network adapters that are active. Example: VMware Accelerated AMD PCNet Adapter

  * Sensor Name: 'CPU', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: Description of the CPU. Example: Intel(R) Core(TM) i5-2500 CPU @ 3.30GHz

  * Sensor Name: 'Model', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: Returns the Model of a system. Example: Precision T1600

  * Sensor Name: 'Number of Processor Cores', Platforms: Windows, Category: Hardware
  * Description: Returns the number of processor cores in all installed processors.  Not supported on all OS patch levels. Example:2

  * Sensor Name: 'Motherboard Version', Platforms: Windows, Linux, Category: Hardware
  * Description: Returns the Version of a motherboard. Example:9230

  * Sensor Name: 'Revision of CPU', Platforms: Windows, Category: Hardware
  * Description: Returns the revision number of installed CPUs. Example: 5898

  * Sensor Name: 'USB Device Details', Platforms: Windows, Category: Hardware
  * Description: Returns of details of attached USB devices, including Description, vendor ID, and product ID. Example:  Generic USB Hub|VMware, Inc.|Virtual USB Hub

  * Sensor Name: 'Hardware Device Failed to Load', Platforms: Windows, Category: Hardware
  * Description: Provides errors codes for hardware devices that failed to load correctly at last boot. Example: none

  * Sensor Name: 'Total Memory', Platforms: Windows, Linux, Mac, AIX, Category: Hardware
  * Description: The total physical memory installed in the client machine. Example: 8000 MB

  * Sensor Name: 'PCI Device', Platforms: Windows, Category: Hardware
  * Description: Returns the names of PCI devices in the system. Example:Intel(R) 82371AB/EB PCI Bus Master IDE Controller

  * Sensor Name: 'Network Adapter Type', Platforms: Windows, Category: Hardware
  * Description: Returns the names of the network connections which are active. Example: Local Area Connection

  * Sensor Name: 'Number of Processors', Platforms: Windows, Linux, Mac, Solaris, Category: Hardware
  * Description: Returns the number of physical processors on a system.  This may differ from the number of cores or number of logical processors. Example:1

  * Sensor Name: 'Human Interface Device', Platforms: Windows, Category: Hardware
  * Description: Indicates any human interface devices connected to the client machine. Example: HID-compliant mouse

  * Sensor Name: 'CPU Cache Size', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: CPU cache size in KB. Example: 1024 KB

  * Sensor Name: 'CPU Family', Platforms: Windows, Linux, Solaris, AIX, Category: Hardware
  * Description: The family of the processor or CPU (Windows provides a family ID). Example: Xeon, Family 198

  * Sensor Name: 'Power Plans Active', Platforms: Windows, Category: Hardware
  * Description: 

  * Sensor Name: 'CD-ROM Drive Loaded', Platforms: Windows, Category: Hardware
  * Description: Checks if CD-ROM/DVD-ROM drive is loaded. Example:  True or False

  * Sensor Name: 'Attached Battery', Platforms: Windows, Mac, Category: Hardware
  * Description: Device name for any attached batteries for a machine, commonly found in laptops. Example: DELL V57XN24

  * Sensor Name: 'System Slots Available', Platforms: Windows, Category: Hardware
  * Description: Returns the number of open slots in the system on Windows client machines. Example: 3

  * Sensor Name: 'Power Plans Available', Platforms: Windows, Category: Hardware
  * Description: 

  * Sensor Name: 'Disk Used Space', Platforms: Windows, Linux, Mac, AIX, Category: Hardware
  * Description: The amount of used disk space per partition. Example: C: 40 GB

  * Sensor Name: 'System Slots In Use', Platforms: Windows, Category: Hardware
  * Description: Returns the number of used slots in the system on Windows client machines. Example: 1

  * Sensor Name: 'RAM Max Capacity', Platforms: Windows, Category: Hardware
  * Description: Returns the size of the maximum amount of RAM a machine can carry. Example: 8 GB

  * Sensor Name: 'Defrag Needed', Platforms: Windows, Category: Hardware
  * Description: Indicates whether the machine's harddrive requires defragmentation Example: Yes

  * Sensor Name: 'Video Driver Version', Platforms: Windows, Category: Hardware
  * Description: The version number of the video driver on the client machine. Example: 6.1.7600.16385

  * Sensor Name: 'Shared Network Printer Details', Platforms: Windows, Category: Hardware
  * Description: Details on any shared printers available from the client machine.  Details include printer name, print server, and share name. Example: \\PRINTSERVER1\PRINTER2 | netserver | \\PRINTSERVER1\PRINTER2

  * Sensor Name: 'Hyperthreading Enabled', Platforms: Windows, Category: Hardware
  * Description: Indicates whether hyperthreading is enabled on the client machine.  This is not supported on all OS patch levels. Example: Yes

  * Sensor Name: 'Network Printer Details', Platforms: Windows, Category: Hardware
  * Description: Returns the connected network printers. Example: printer_name | driver | port

  * Sensor Name: 'Motherboard Manufacturer', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: Returns the Motherboard Manufacturer of a system. Example:Lenovo

  * Sensor Name: 'CD-ROM Drive', Platforms: Windows, Linux, Category: Hardware
  * Description: Name of any installed CD-ROM or DVD-ROM drives. Example: SONY DVD-ROM DDU1615 ATA Device

  * Sensor Name: 'Video/Graphics Card', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: Description of the video card in the client machine. Example: ATI Radeon HD 2400 Pro

  * Sensor Name: 'Installed Java Runtimes', Platforms: Windows, Category: Java
  * Description: Returns a list of all installed Java runtimes on the client machine. Example: Java(TM) 6 Update 20

  * Sensor Name: 'Java Auto Update', Platforms: Windows, Category: Java
  * Description: Returns the state of the Java Auto Update service, per architecture. Example: Enabled 32-bit

  * Sensor Name: 'Online', Platforms: Windows, Linux, Mac, AIX, Category: Miscellaneous
  * Description: Returns, in all cases, the word True.  This sensor is used in many ways, including to find a common target for machines which may have responded to a question with a 'where' clause - get "online from machines where IP address starts with 192.168.10." will allow you to target the respondents with an action or count responses. Example:True

  * Sensor Name: 'Open Share Details', Platforms: Windows, Category: Miscellaneous
  * Description: Returns a set of columns with details about open shares on a machine. Example: name | path | status | type | permissions

  * Sensor Name: 'High CPU Processes', Platforms: Windows, Linux, Mac, Category: Miscellaneous
  * Description: Lists the specified number of processes that are using the highest amount of CPU. Example: cmd
  * Parameter 'numOutput':
    - 'defaultValue': 5
    - 'helpString': Enter the number of processes to return
    - 'label': Number of Processes
    - 'maximum': 50
    - 'minimum': 1
    - 'stepSize': 1
    - 'value': 5

  * Sensor Name: 'High Memory Processes', Platforms: Windows, Linux, Mac, Category: Miscellaneous
  * Description: Lists the specified number processes based on ordering on amount of memory used. Example: cmd
  * Parameter 'numOutput':
    - 'defaultValue': 5
    - 'helpString': Enter the number of processes to return
    - 'label': Number of Processes
    - 'maximum': 50
    - 'minimum': 1
    - 'stepSize': 1
    - 'value': 5

  * Sensor Name: 'Client Time', Platforms: Windows, Linux, Mac, Category: Miscellaneous
  * Description: The local time on the managed client. Example: 5:17:44 PM

  * Sensor Name: 'Application Event Log Search', Platforms: Windows, Category: Miscellaneous
  * Description: A parameterized Sensor that allows an operator to search for a particular string in the Windows application event logs. Example: The Apache service reported the following error: [Tue Jan 01 17:14:24 2010] [warn] PassEnv variable CommonProgramFiles(x86) was undefined
  * Parameter 'EVENT':
    - 'helpString': Enter the event string to search for
    - 'label': Event string to search for
    - 'promptText': e.g. terminated unexpectedly

  * Sensor Name: 'Client Date', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Miscellaneous
  * Description: The calendar date on the managed client. Example: 01/30/2012

  * Sensor Name: 'RAM Slots Used and Unused', Platforms: Windows, Category: Miscellaneous
  * Description: Returns the number of used and unused RAM slots. Example:2 6

  * Sensor Name: 'Number of Fixed Drives', Platforms: Windows, Category: Miscellaneous
  * Description: Returns the number of fixed drives installed in the system. Example:4

  * Sensor Name: 'Target', Platforms: Windows, Category: Miscellaneous
  * Description: Simple sensor that returns the word "Target" that is used when targeting actions within Tanium. Example: Target

  * Sensor Name: 'IP Address', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Network
  * Description: Current IP Addresses of client machine. Example: 192.168.1.1

  * Sensor Name: 'MAC Address', Platforms: Windows, Linux, Mac, Solaris, Category: Network
  * Description: Returns MAC addresses for all IP enabled network connections. Example:00:0C:29:68:6A:D8

  * Sensor Name: 'DHCP Enabled?', Platforms: Windows, Category: Network
  * Description: Whether or not a machine has an network adapter set to DHCP.  Note, a machine may have multiple active adapters and may return multiple lines.  If a machine has multiple adapters on DCHP, TRUE is returned only once. Example: TRUE, FALSE

  * Sensor Name: 'Firewall Status', Platforms: Windows, Mac, Category: Network
  * Description: Returns the current status of the Windows firewalls. Example: DomainProfile enabled

  * Sensor Name: 'DNS Server', Platforms: Windows, Linux, Mac, Solaris, Category: Network
  * Description: Addresses of any configured DNS servers for active network adapters. Example: 192.168.1.1, 8.8.8.8

  * Sensor Name: 'Non-Approved Established Connections', Platforms: Windows, Mac, Category: Network
  * Description: Any established connections currently being made from a process that is not allowed or to a destination that is not allowed.  This multi-column Sensor displays the process responsible for the connection, the display name of the process (if available), and the target IP Address and port.  Processes and IP ranges can be excluded in the Sensor definition. Example: chrome.exe | Google Chrome | 173.194.79.99:80

  * Sensor Name: 'Wireless Network Connected SSID', Platforms: Windows, Mac, Category: Network
  * Description: Returns the SSID (name) of a wireless network a machine is connected to. Example: linksys

  * Sensor Name: 'Wireless Networks Visible', Platforms: Windows, Mac, Category: Network
  * Description: Returns details of all wireless networks a machine can see, whether they are connected or not.  Details include SSID, Network Type, Authentication Method, and Encryption Level. Example: hotspotwifi | Infrastructure | WPA2-Personal

  * Sensor Name: 'Wireless Network Details', Platforms: Windows, Mac, Category: Network
  * Description: Details of currently active wireless network connection by client machine.  Details include SSID, MAC address, connection state, network type, radio type, authentication, receive rate, transmit rate, and signal strength. Example: hotspotwifi | xx-xx-xx-xx-xx-xx | connected | Infrastructure | 802.11g | WPA2-Personal | 54 | 54 | 99%

  * Sensor Name: 'Hosted Wireless Ad-Hoc Networks', Platforms: Windows, Mac, Category: Network
  * Description: Returns details of ad-hoc wireless networks are hosted in your environment.  Details include SSID, Mode, Max Clients, Auth, Status, BSSID, Radio Type, Channel, and Connections. Example: personalwifi | ad-hoc | 1 | Open | active | xx:xx:xx:xx:xx:xx | 802.11g | 11 | 1

  * Sensor Name: 'Wireless Networks Using WEP', Platforms: Windows, Mac, Category: Network
  * Description: Details of currently active wireless network connection using WEP authentication by client machine.  Details include SSID, MAC address, connection state, network type, radio type, authentication, receive rate, transmit rate, and signal strength. Example: hotspotwifi | xx-xx-xx-xx-xx-xx | connected | Infrastructure | 802.11g | WEP | 54 | 54 | 99%

  * Sensor Name: 'Unencrypted Wireless Networks', Platforms: Windows, Mac, Category: Network
  * Description: Details of wireless networks that are currently open and unencrypted.  Details include SSID, MAC address, connection state, network type, radio type, authentication, receive rate, transmit rate, and signal strength. Example: hotspotwifi | xx-xx-xx-xx-xx-xx | connected | Infrastructure | 802.11g | WEP | 54 | 54 | 99%

  * Sensor Name: 'Wireless Network SSID Strength', Platforms: Windows, Mac, Category: Network
  * Description: Returns the SSID name and signal strength of a connected wireless network where signal strength is 0-5. Example: linksys|4

  * Sensor Name: 'Wireless Network Used by Tanium', Platforms: Windows, Mac, Category: Network
  * Description: Returns the SSID name, the IP Address, and the MAC address of connected wireless networks only if the Tanium Client is using those networks to communicate. Example: linksys|192.168.10.5|00D55FED214C1A2C

  * Sensor Name: 'Domain Name', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Network
  * Description: The domain name (if any) that the computer is joined to or configured for. Example: intra.company.com

  * Sensor Name: 'Network Adapter Details', Platforms: Windows, Solaris, Category: Network
  * Description: Returns information on network adapters. Example:Intel(R) Centrino(R) Ultimate-N 6300 AGN|Intel Corporation|Ethernet 802.3|00:24:D7:21:9C:70|65 Mbps|Wi-Fi

  * Sensor Name: 'Network Link Speed', Platforms: Windows, Solaris, Category: Network
  * Description: Returns the names and speeds of all network connections. Example: WAN Miniport (IP) | 10000

  * Sensor Name: 'DHCP Server', Platforms: Windows, Category: Network
  * Description: The addresses of the configured DHCP servers, If a machine is on DHCP. Example: 192.168.1.1

  * Sensor Name: 'Established Connections', Platforms: Windows, Linux, Mac, Category: Network
  * Description: Any established connections currently being made.  This multi-column Sensor displays the process responsible for the connection, the display name of the process (if available), and the target IP Address and port.  Processes and IP ranges can be excluded in the Sensor definition. Example: chrome.exe | Google Chrome | 173.194.79.99:80

  * Sensor Name: 'Network Throughput Outbound', Platforms: Windows, Linux, Solaris, Category: Network
  * Description: Returns the current output throughput, in KB/Sec, of the network interface used to connect to the tanium server. Example: 1024 KB/S

  * Sensor Name: 'Established Ports by Application', Platforms: Windows, Linux, Mac, Category: Network
  * Description: Parameterized Sensor that shows which addresses the process is connecting to and over what local port. Example: 0.0.0.0:17500
  * Parameter 'app':
    - 'helpString': Enter the process name to query
    - 'label': Process Name to examine
    - 'promptText': e.g. svchost.exe

  * Sensor Name: 'Network Throughput Percentage', Platforms: Windows, Category: Network
  * Description: Returns the current throughput, as a percentage of total possible, of the network interface used to connect to the tanium server. Example: 50%

  * Sensor Name: 'Recently Closed Connections', Platforms: Windows, Category: Network
  * Description: Returns any recently closed connection, ie those connection currently in CLOSED_WAIT or TIME_WAIT.  If the process that owned the connection can be determined, it will be included. Example: Google Chrome | 173.194.79.99:80

  * Sensor Name: 'Network Drives Accessed', Platforms: Windows, Category: Network
  * Description: Returns the share path of network shares the host is connected to. Example: \\\\server\\share

  * Sensor Name: 'Network Throughput Total', Platforms: Windows, Category: Network
  * Description: Returns the current total throughput, in KB/Sec, of the network interface used to connect to the tanium server. Example: 2048 KB/S

  * Sensor Name: 'Packet Loss', Platforms: Windows, Category: Network
  * Description: Returns data about percent of packet loss on Windows machines. Example: 5 %

  * Sensor Name: 'IP Connections', Platforms: Windows, Category: Network
  * Description: Returns the protocol, local address / port, process name, application name, remote port, and connection state for all active IP connections on an endpoint. Example: tcp|192.168.95.186:51866|explorer.exe|Windows Explorer|165.254.58.66:80|established

  * Sensor Name: 'Network Throughput Inbound', Platforms: Windows, Linux, Solaris, Category: Network
  * Description: Returns the current inbound throughput, in KB/Sec, of the network interface used to connect to the tanium server. Example: 1024 KB/S

  * Sensor Name: 'TCP connections', Platforms: Linux, Category: Network
  * Description: Lists all TCP connections on a machine wth their state. Example: TaniumClient|

  * Sensor Name: 'Subnet Mask', Platforms: Windows, Solaris, Category: Network
  * Description: A list of all of the configured subnet masks for the network adapters of the client machine. Example: 255.255.0.0

  * Sensor Name: 'Listen Ports', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Network
  * Description: Returns information network-aware processes and the ports they have bound to. Example: googletalkplugin.exe Google Talk Plugin :60042

  * Sensor Name: 'UDP Connections', Platforms: Linux, Category: Network
  * Description: 

  * Sensor Name: 'Hosts File Entries', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Network
  * Description: Provides a list of hosts file entries for the local operating system. Example: myserver.com , 192.168.1.100

  * Sensor Name: 'Network IP Gateway', Platforms: Windows, Category: Network
  * Description: Returns the default gateway for all IP enabled network adapters. Example: 192.168.10.254

  * Sensor Name: 'Primary WINS Server', Platforms: Windows, Category: Network
  * Description: Returns the primary WINS server of a machine. Example: WINS1

  * Sensor Name: 'Static IP Addresses', Platforms: Windows, Category: Network
  * Description: A list of the static IP addresses currently held by the client machine. Example: 192.168.1.1

  * Sensor Name: 'IP Route Details', Platforms: Windows, Linux, Mac, Solaris, Category: Network
  * Description: Returns IPv4 network routes, filtered to exclude noise. With Flags, Metric, Interface columns. Example:  172.16.0.0|192.168.1.1|255.255.0.0|UG|100|eth0

  * Sensor Name: 'IP Routes', Platforms: Windows, Linux, Mac, Solaris, Category: Network
  * Description: Returns IPv4 network routes, filtered to exclude noise. Example:  172.16.0.0|192.168.1.1|255.255.0.0

  * Sensor Name: 'Open Port', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Network
  * Description: Returns the ports which are listening on a local machine and the IP address the port is bound to.  0.0.0.0 indicates that the port is bound to all IP addresses. Example: 0.0.0.0:80

  * Sensor Name: 'Workgroup', Platforms: Windows, Category: Network
  * Description: The configured workgroup or computer domain for each client machine. Example: mycompanydomain

  * Sensor Name: 'Outlook Version', Platforms: Windows, Category: Office
  * Description: Returns the version of Microsoft Office Outlook installed. Example: Outlook 2003, Version: 11.0

  * Sensor Name: 'PST Information', Platforms: Windows, Category: Office
  * Description: Returns details of PST files that have been mounted by users on a system. Example: c:\psts\huge.pst 4088 MB

  * Sensor Name: 'Operating System', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns the name of the Operating System from all machines.  This name may be localized. Example: Windows Server 2008 R2 Enterprise

  * Sensor Name: 'Is Windows', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns whether the machine runs Windows.  True if so, False if not. Example: True

  * Sensor Name: 'Username', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns the currently logged in user, and No User if nobody is logged in. Example: Domain\JDoe

  * Sensor Name: 'USB Write Protected', Platforms: Windows, Category: Operating System
  * Description: Outputs True if USB storage devices connected to the client machine are set to write protected mode and false if not. Example: False

  * Sensor Name: 'Reboot Required', Platforms: Windows, Linux, Mac, Category: Operating System
  * Description: Returns data indicating that a reboot is required and, if so, for which reason. Example: Yes

  * Sensor Name: 'Memory Consumption', Platforms: Windows, Linux, Mac, Solaris, Category: Operating System
  * Description: Returns the percentage of used (committed) memory on a system. Example: 27 percent

  * Sensor Name: 'Service Pack', Platforms: Windows, AIX, Category: Operating System
  * Description: The Service Pack level of the machine if available, and "No Service Pack found" if unavailable. Example: Service Pack 1

  * Sensor Name: 'Last System Crash', Platforms: Windows, Category: Operating System
  * Description: Returns the date of the last system crash that occurred. Example: 8/2/2012

  * Sensor Name: 'Last System Crash in X Days', Platforms: Windows, Category: Operating System
  * Description: Returns the date at which the last system crash occurred. Example:5/2/2012
  * Parameter 'dayThresh':
    - 'defaultValue': 5
    - 'helpString': Enter the number of days to query and return system crashes
    - 'label': Number of Days
    - 'maximum': 365
    - 'minimum': 1
    - 'stepSize': 1
    - 'value': 5

  * Sensor Name: 'Uptime', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Time since reboot in days of the client machine. Example: 48 days

  * Sensor Name: 'Disk Type of C:', Platforms: Windows, Category: Operating System
  * Description: File system type of the C drive. Example: NTFS

  * Sensor Name: 'Operating System Build Number', Platforms: Windows, Category: Operating System
  * Description: Returns the build number of the installed operating system. Example:7601

  * Sensor Name: 'Operating System Install Date', Platforms: Windows, Solaris, AIX, Category: Operating System
  * Description: Returns the date the OS was installed. Example: 8/24/2012

  * Sensor Name: 'Boot Device', Platforms: Windows, AIX, Category: Operating System
  * Description: Hard disk device that the operating system uses to boot from. Example: \\Device\\HarddiskVolume1

  * Sensor Name: 'Open Shares', Platforms: Windows, Mac, Category: Operating System
  * Description: Returns information about shares on a PC. Example: SHARENAME

  * Sensor Name: 'Disk IOPS', Platforms: Windows, Category: Operating System
  * Description: Returns the current total number of disk IOPS currently occurring Example: 86

  * Sensor Name: 'Service Login Names', Platforms: Windows, Category: Operating System
  * Description: A list of accounts under which services are configured to run.  This list will not include the default accounts, including LocalSystem, LocalService, and NetworkService. Example: .\\servuser

  * Sensor Name: 'Default Login Domain', Platforms: Windows, Category: Operating System
  * Description: Name of the domain of the most recently logged in user. Example: CORP

  * Sensor Name: 'Startup Programs', Platforms: Windows, Category: Operating System
  * Description: A list of programs configured to automatically run on the client machine.  Also includes the command line entry to run the program. Example: Windows Mobile Device Center | C:\Windows\WindowsMobile\wmdc.exe

  * Sensor Name: 'Screen Saver Active', Platforms: Windows, Category: Operating System
  * Description: Indicates whether a screen saver is enabled on the client machine. Example: True

  * Sensor Name: 'Operating System Boot Directory', Platforms: Windows, Solaris, Category: Operating System
  * Description: Returns the directory the Operating System boots from. Example:\\Windows

  * Sensor Name: 'High CPU Consumption', Platforms: Windows, Category: Operating System
  * Description: Indicates whether the client machine is currently experiencing high utilization of its CPU. Example: Under threshold

  * Sensor Name: 'System Drive', Platforms: Windows, Category: Operating System
  * Description: Hard drive location hosting system directory on Windows machines. Example: C:

  * Sensor Name: 'Run Once Keys', Platforms: Windows, Category: Operating System
  * Description: Returns the run once keys that define which programs will be started when a user logs in. Example:  System|GlobalProtect|"C:\Program Files\Palo Alto Networks\GlobalProtect\PanGPA.exe"

  * Sensor Name: 'System Environment Variables', Platforms: Windows, Category: Operating System
  * Description: Returns the currently defined system variables Example:  windir=c:\Windows

  * Sensor Name: 'Driver Details', Platforms: Windows, Category: Operating System
  * Description: Return details about loaded drivers Example: WIMMount|Stopped|C:\Windows\system32\drivers\wimmount.sys|6.3.9600.16384

  * Sensor Name: 'Time Zone', Platforms: Windows, Solaris, Category: Operating System
  * Description: The currently specified time zone for the client machine. Example: (UTC-08:00) Pacific Time (US & Canada)

  * Sensor Name: 'Local Administrators Without Groups', Platforms: Windows, Category: Operating System
  * Description: Returns users (but not groups) who are members of the Local Administrators group on Windows.  Will not list the individual members of groups in the Local Administrators group. Example: Administrator

  * Sensor Name: 'Default Login UserID', Platforms: Windows, Category: Operating System
  * Description: Last user name entered in the "Log On to Windows" dialog box. Example: tanium_admin

  * Sensor Name: 'Operating System Temp Directory', Platforms: Windows, Solaris, AIX, Category: Operating System
  * Description: Returns the gobal temp directory of the Operating System. Example: C:\Temp

  * Sensor Name: 'Load Average', Platforms: Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns the average CPU load on a Mac or Linux system  Example: 0.00 0.03 0.10

  * Sensor Name: 'Installed HotFixes', Platforms: Windows, AIX, Category: Operating System
  * Description: Returns a list of hotfixes that have previously been applied to the client machine. Example: Microsoft National Language Support Downlevel APIs

  * Sensor Name: 'UAC Status', Platforms: Windows, Category: Operating System
  * Description: Returns Enabled or Disabled based on the status of Windows User Access Control on the client machine. Example: Enabled

  * Sensor Name: 'Domain Member', Platforms: Windows, Category: Operating System
  * Description: Returns true if the machine is part of an Active Directory domain. Example: TRUE, FALSE

  * Sensor Name: 'Primary Owner Name', Platforms: Windows, Category: Operating System
  * Description: Returns the name of the Primary System Owner on Windows.  This  is set at OS install time. Example: John Doe

  * Sensor Name: 'Maximum Process Memory Size', Platforms: Windows, Linux, Mac, Solaris, Category: Operating System
  * Description: Returns the maximum amount of memory, in Kilobytes, that a process can use.  This may be free physical RAM and virtual RAM combined, or may be an arbitrary upper ceiling. Example: 2097024

  * Sensor Name: 'Is Mac', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns whether the machine is a Mac.  True if so, False if not. Example: True

  * Sensor Name: 'Last Reboot', Platforms: Windows, Linux, Mac, Solaris, Category: Operating System
  * Description: Returns the time the last reboot occurred. Example: 2012-12-11 09:01

  * Sensor Name: 'Time Zone Offset', Platforms: Windows, Linux, Mac, Solaris, Category: Operating System
  * Description: Returns the time offset in minutes. Example: -0700

  * Sensor Name: 'Low Disk Space', Platforms: Windows, Linux, Solaris, Category: Operating System
  * Description: Returns disk drives which have less than 2 gigabytes free. Example: C:

  * Sensor Name: 'Number Of Users', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns the number of user sessions for which the operating system is storing state.  This may differ from the number of interactively logged in users. Example:3

  * Sensor Name: 'Operating System Language Code', Platforms: Windows, Category: Operating System
  * Description: Returns the Language Code (LCID) of the Operating System.  This differs from the Locale Code returned in the Locale Code sensor. Example: 1033

  * Sensor Name: 'Total Swap', Platforms: Linux, Solaris, AIX, Category: Operating System
  * Description: Total swap space configured by client machine. Example: 4000 MB

  * Sensor Name: 'Locale Code', Platforms: Windows, Category: Operating System
  * Description: Returns the OS Locale Code from the installed operating system.  This differs from the LCID returned in the OS language sensor. Example:0409

  * Sensor Name: 'OS Boot Time', Platforms: Windows, Category: Operating System
  * Description: Returns the Date and Time that the OS last booted in UTC. Example:  Mon, 05 Jan 2015 15:17:59 +0000

  * Sensor Name: 'Organization', Platforms: Windows, Category: Operating System
  * Description: Returns the Organization defined at OS install time. Example: YourCorp

  * Sensor Name: 'System Directory', Platforms: Windows, Category: Operating System
  * Description: The location of the system directory on Windows machines. Example: C:\\Windows\\system32

  * Sensor Name: 'Page File Details', Platforms: Windows, Category: Operating System
  * Description: Returns information about the Page File(s) on a Windows system. Path, initial size, maximum size, size on disk, current used, and peak used. Example: C:\pagefile.sys|3050 MB|3050 MB|3050 MB|413 MB|517 MB

  * Sensor Name: 'Is Linux', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns whether the machine runs a Linux-based OS.  True if so, False if not. Example: True

  * Sensor Name: 'Local Administrators', Platforms: Windows, Category: Operating System
  * Description: Returns users and groups who are members of the Local Administrators group on Windows.  Will not list the individual members of groups in the Local Administrators group. Example: Administrator

  * Sensor Name: 'Tanium Reboot Days Ago', Platforms: Windows, Category: Operating System
  * Description: Returns the number of days since a Tanium Reboot Action occurred. Example: 2

  * Sensor Name: 'Processes Using Module', Platforms: Windows, Category: Operating System
  * Description: Lists processes that use a module supplied to the sensor. Example: explorer.exe
  * Parameter 'search':
    - 'helpString': Enter the Module to search for
    - 'label': Module to search for
    - 'promptText': e.g. wbem* or kernel32.dll

  * Sensor Name: 'Is Terminal Server', Platforms: Windows, Category: Operating System
  * Description: Returns Yes or No depending on whether a Windows machine is a Terminal Server Example: Yes

  * Sensor Name: 'Is AIX', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns whether the machine runs a AIX OS.  True if so, False if not. Example: True

  * Sensor Name: 'SCSI Controller Driver Name', Platforms: Windows, Category: Operating System
  * Description: Name for SCSI Controller Driver as provided by the manufacturer. Example: VClone

  * Sensor Name: 'Is Solaris', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns whether the machine runs a Solaris-based OS.  True if so, False if not. Example: True

  * Sensor Name: 'Used Swap', Platforms: Linux, Solaris, Category: Operating System
  * Description: Swap space in use in MB by the client machine. Example: 2164 MB

  * Sensor Name: 'System UUID', Platforms: Linux, Mac, Category: Operating System
  * Description: System unique identifier UUID on Mac or Linux machines. Example: 3e6be9de-8139-11d1-9106-a43f08d823a6

  * Sensor Name: 'Run Keys', Platforms: Windows, Category: Operating System
  * Description: Returns the run keys that define which programs will be started when a user logs in. Example:  System|GlobalProtect|"C:\Program Files\Palo Alto Networks\GlobalProtect\PanGPA.exe"

  * Sensor Name: 'SCSI Controller Caption', Platforms: Windows, Category: Operating System
  * Description: A short description of the SCSI Controller as provided by the manufacturer. Example: Dell PERC S100 S300 Controller

  * Sensor Name: 'System Disk Free Space', Platforms: Windows, Category: Operating System
  * Description: The amount of free disk space on the main system drive. Example: C:|4 GB

  * Sensor Name: 'Free Swap', Platforms: Linux, Solaris, AIX, Category: Operating System
  * Description: Indicates the free swap space available to the operating system. Example: 640MB

  * Sensor Name: 'Disk Total Size of System Drive', Platforms: Windows, Category: Operating System
  * Description: The amount of total disk space on the main system drive. Example: C: 100 GB

  * Sensor Name: 'Run Level', Platforms: Linux, Solaris, AIX, Category: Operating System
  * Description: Returns the set run level of Linux systems Example: 3

  * Sensor Name: 'Operating System Language', Platforms: Windows, Category: Operating System
  * Description: Returns the OS language along with any Language Packs installed. Example: English-United States en-US

  * Sensor Name: 'CPU by Process', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: A multi-column sensor that lists every running process and the amount of CPU usage they are taking up. Example: svchost | 15

  * Sensor Name: 'Windows OS Type', Platforms: Windows, Linux, Mac, Category: Operating System
  * Description: Will output "Windows Server" or "Windows Workstation" depending on the OS type. Example: Windows Server

  * Sensor Name: 'Kernel Modules', Platforms: Linux, Solaris, Category: Operating System
  * Description: Returns loaded kernel modules on Linux systems. Example:dcdbas

  * Sensor Name: 'Country Code', Platforms: Windows, Category: Operating System
  * Description: Shows the currently specified country code used by the operating system. Example: 1    (United States)

  * Sensor Name: 'Data Execution Prevention Enabled', Platforms: Windows, Category: Operating System
  * Description: Whether data execution prevention is enabled for 32-bit machines.  If disabled, code can be executed from a non-executable memory region. Example: TRUE, FALSE

  * Sensor Name: 'Boot Time', Platforms: Windows, Category: Operating System
  * Description: The amount of time, in seconds, that the last boot of this machine took. Example:  100

  * Sensor Name: 'Is Mac API TEST', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns whether the machine is a Mac.  True if so, False if not. Example: True

  * Sensor Name: 'PowerShell Version', Platforms: Windows, Category: PowerShell
  * Description: Returns the version(s) of PowerShell installed on a system Example: 2.0

  * Sensor Name: 'Registry Key Value Exists', Platforms: Windows, Category: Registry
  * Description: Returns True if the Registry Value exists, False if not.
  * Parameter 'strKey':
    - 'helpString': Enter the key path to query
    - 'label': Registry Key
    - 'promptText': e.g. HKEY_LOCAL_MACHINE\Software\Microsoft
  * Parameter 'strValue':
    - 'helpString': Enter the key value to query
    - 'label': Registry Value
    - 'promptText': e.g. Version

  * Sensor Name: 'Registry Value Data', Platforms: Windows, Category: Registry
  * Description: Returns the data of a supplied value in a supplied registry key.  If the hive is HKEY_USERS, it will attempt to output the user name associated with the key.  HKEY_CURRENT_USER will only return data for the SYSTEM account which the Tanium Client runs as. Example: John | 4.1.314.7020 | REG_SZ|32-bit
  * Parameter 'strKey':
    - 'helpString': Enter the key path to query
    - 'label': Registry Key
    - 'promptText': e.g. HKEY_LOCAL_MACHINE\Software\Microsoft
  * Parameter 'strValue':
    - 'helpString': Enter the key value to query
    - 'label': Registry Value
    - 'promptText': e.g. Version. Use (Default) to get default value.

  * Sensor Name: 'Registry Key Exists', Platforms: Windows, Category: Registry
  * Description: Returns True if the Registry Key exists, False if not.
  * Parameter 'strKey':
    - 'helpString': Enter the registry key to query
    - 'label': Registry Key
    - 'promptText': e.g. HKEY_USERS\Software\Key

  * Sensor Name: 'Registry Key Subkeys', Platforms: Windows, Category: Registry
  * Description: Returns all subkeys of a supplied key.  If the hive is HKEY_USERS, it will attempt to output the user name associated with the key.  HKEY_CURRENT_USER will only return data for the SYSTEM account which the Tanium Client runs as. Example: John |Sensor Data | 32-bit
  * Parameter 'strKey':
    - 'helpString': Enter the registry key to query
    - 'label': Registry Key
    - 'promptText': e.g. HKEY_USERS\Software\Key

  * Sensor Name: 'Registry Key Value Names with Data', Platforms: Windows, Category: Registry
  * Description: Returns the data and values in a supplied registry key.  If the hive is HKEY_USERS, it will attempt to output the user name associated with the key.  HKEY_CURRENT_USER will only return data for the SYSTEM account which the Tanium Client runs as. Example: John | 4.1.314.7020 | REG_SZ | 32-bit | HKLM\Software\Tanium\Tanium Client | Version
  * Parameter 'strKey':
    - 'helpString': Enter the key path to query
    - 'label': Registry Key
    - 'promptText': e.g. HKEY_LOCAL_MACHINE\Software\Microsoft

  * Sensor Name: 'Registry Key Value Names', Platforms: Windows, Category: Registry
  * Description: Returns all values contained in a supplied key.  If the hive is HKEY_USERS, it will attempt to output the user name associated with the key.  HKEY_CURRENT_USER will only return data for the SYSTEM account which the Tanium Client runs as. Example: John | Version | 32-bit
  * Parameter 'strKey':
    - 'helpString': Enter the registry key to query
    - 'label': Registry Key
    - 'promptText': e.g. HKEY_USERS\Software\Key

  * Sensor Name: 'Action Statuses', Platforms: Windows, Category: Reserved
  * Description: The recorded state of each action a client has taken recently in the form of id:status. Example: 1:Completed

  * Sensor Name: 'Computer ID', Platforms: Windows, Category: Reserved
  * Description: A unique identifier of each computer for internal use. Example: 4202979704

  * Sensor Name: 'Computer Name', Platforms: Windows, Category: Reserved
  * Description: The assigned name of the client machine. Example: workstation-1.company.com

  * Sensor Name: 'Download Statuses', Platforms: Windows, Category: Reserved
  * Description: The recorded state of each download a client has made recently in the form of hash:completion percentage. Example: 05839407baccdfccfd8e2c1ffc0ff27541cc053d15b52cfd4ed904510e59b428:100

  * Sensor Name: 'Action Statuses CMDLINE TEST 2119', Platforms: Windows, Category: Reserved
  * Description: The recorded state of each action a client has taken recently in the form of id:status. Example: 1:Completed

  * Sensor Name: 'Action Statuses CMDLINE TEST 3725', Platforms: Windows, Category: Reserved
  * Description: The recorded state of each action a client has taken recently in the form of id:status. Example: 1:Completed

  * Sensor Name: 'Action Statuses CMDLINE TEST 2368', Platforms: Windows, Category: Reserved
  * Description: The recorded state of each action a client has taken recently in the form of id:status. Example: 1:Completed

  * Sensor Name: 'Action Statuses CMDLINE TEST 3082', Platforms: Windows, Category: Reserved
  * Description: The recorded state of each action a client has taken recently in the form of id:status. Example: 1:Completed

  * Sensor Name: 'Action Statuses CMDLINE TEST 6173', Platforms: Windows, Category: Reserved
  * Description: The recorded state of each action a client has taken recently in the form of id:status. Example: 1:Completed

  * Sensor Name: 'Action Statuses CMDLINE TEST 7043', Platforms: Windows, Category: Reserved
  * Description: The recorded state of each action a client has taken recently in the form of id:status. Example: 1:Completed

  * Sensor Name: 'Action Statuses CMDLINE TEST 6698', Platforms: Windows, Category: Reserved
  * Description: The recorded state of each action a client has taken recently in the form of id:status. Example: 1:Completed

  * Sensor Name: 'SQL Database Count', Platforms: Windows, Category: SQL
  * Description: The number of databases in SQL Server on the client machine. Example: 4

  * Sensor Name: 'SQL Server Edition', Platforms: Windows, Category: SQL
  * Description: Returns the Edition of SQL Server installed on the client machine if it exists. Example: Enterprise Edition (64-bit)

  * Sensor Name: 'SQL Product Version', Platforms: Windows, Category: SQL
  * Description: Product version from SQL Server on client machine. Example: 10.50.1617.0

  * Sensor Name: 'SQL Product Level', Platforms: Windows, Category: SQL
  * Description: Product level for SQL Server on client machine. Example: SP4

  * Sensor Name: 'SQL Database Sizes', Platforms: Windows, Category: SQL
  * Description: 

  * Sensor Name: 'SQL Log Sizes', Platforms: Windows, Category: SQL
  * Description: 

  * Sensor Name: 'SQL Database Recovery Mode', Platforms: Windows, Category: SQL
  * Description: 

  * Sensor Name: 'SQL Clustered', Platforms: Windows, Category: SQL
  * Description: Returns whether or not the SQL server instance is clustered Example: True

  * Sensor Name: 'SQL Server CPU Consumption', Platforms: Windows, Category: SQL
  * Description: Current CPU utilization percentage by SQL Server process on client machine. Example: 8%

  * Sensor Name: 'SQL Recovery Mode', Platforms: Windows, Category: SQL
  * Description: Returns database name and recovery mode for that database from all databases in SQL Server on client machine. Example: ReportServer SIMPLE

  * Sensor Name: 'SQL Server Agent Long Running Jobs', Platforms: Windows, Category: SQL
  * Description: Returns a list of long running SQL Server jobs on the client machine.  Details include job name, start date, and duration. Example: backupjob | 22-july-12 12:00 Am | 00:01:00:00

  * Sensor Name: 'SQL Buffer Hit Ratio', Platforms: Windows, Category: SQL
  * Description: Returns the buffer cache hit ratio from SQL Server on the client machine. Example: .5

  * Sensor Name: 'Password Policy Details', Platforms: Windows, Category: Security
  * Description: Returns various data about a machines externally or locally defined Password Policy. Example: maximum age | minimum age | enforced history | minimum length | lockout duration | lockout threshold | lockout observation window

  * Sensor Name: 'No Screen Saver Password', Platforms: Windows, Category: Security
  * Description: Returns the users which have no screen saver password set. Example: Domain\John.Doe

  * Sensor Name: 'BitLocker Details', Platforms: Windows, Category: Security
  * Description: Returns information on the BitLocker status of a machine. Example: Drive | Device ID | Encryption Method

  * Sensor Name: 'FileVault Details', Platforms: Mac, Category: Security
  * Description: Returns information on the FileVault status of a machine Example: If Available | Fully Secure | Status

  * Sensor Name: 'Local User Password Change Dates', Platforms: Windows, Linux, Mac, Category: Security
  * Description: Returns the last time the password was set for each user account. Example:  taniumuser|2013-10-31

  * Sensor Name: 'Share Folder Permissions', Platforms: Windows, Category: Security
  * Description: A list of all shared folders and the permissions currently enabled for those folders. Example: Downloads, BUILTIN\Administrators-FULL | \CREATOR OWNER-FULL | NT AUTHORITY\SYSTEM-FULL

  * Sensor Name: 'High Uptime', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Software
  * Description: Indicates whether the client machine has been online for more than 30 days. Example: Less than 30 days

  * Sensor Name: 'Number of Application Crashes in Last X Days', Platforms: Windows, Category: Software
  * Description: Returns the number of application crashes that have occurred in the last number of days supplied to the sensor. Example: 3
  * Parameter 'days':
    - 'defaultValue': 5
    - 'helpString': Enter the number of days to query for Application Crashes
    - 'label': Number of Days
    - 'maximum': 365
    - 'minimum': 1
    - 'stepSize': 1
    - 'value': 5

  * Sensor Name: 'Local User Login Dates', Platforms: Windows, Solaris, Category: Software
  * Description: Returns the names and dates of the last users to log in. Example: John.Doe 7/25/2012

  * Sensor Name: 'SQL Server Databases', Platforms: Windows, Category: Software
  * Description: List of database names from SQL Server on client machines. Example: tanium

  * Sensor Name: 'VMware Guest', Platforms: Windows, Linux, Category: Software
  * Description: Returns True if client machine is a guest VM in VMware. Example: True

  * Sensor Name: 'Windows Server Installed Roles', Platforms: Windows, Category: Software
  * Description: Returns the currently installed roles on a Windows Server. Example:  File Server

  * Sensor Name: 'Custom Tags', Platforms: Windows, Linux, Mac, Category: Tags
  * Description: Any specified custom tags that have been set for this machine.  See the Custom Tagging Dashboard. Example:  Development, Test-Machines

  * Sensor Name: 'Tanium Client Version', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Tanium
  * Description: Version number of the Tanium Client on the client machine. Example: 4.1.314.7020

  * Sensor Name: 'Action Lock Status', Platforms: Windows, Category: Tanium
  * Description: Returns whether the client is in a 'locked' state. Use the package "Tanium Client Action Unlock" to unlock the Client and allow actions. Example: Action Lock On

  * Sensor Name: 'Tanium PowerShell Execution Policy', Platforms: Windows, Category: Tanium
  * Description: Retrieves the PowerShell Execution Policy as the Tanium Client sees it

  * Sensor Name: 'Tanium Server Version', Platforms: Windows, Category: Tanium
  * Description: Version number of  Tanium Server installed.  Example: 6.2.314.3218

  * Sensor Name: 'Tanium Zone Server Version', Platforms: Windows, Category: Tanium
  * Description: Version number of  Tanium Zone Server installed.  Example: 6.2.314.3218

  * Sensor Name: 'Tanium Client Explicit Setting', Platforms: Windows, Category: Tanium
  * Description: Returns the value of a supplied Tanium Client Setting fom the Tanium Clients registry key.  Supply only the client setting name, for instance: ServerName and the output will appear as follows: Example: berkeley.tanium.com
  * Parameter 'setting':
    - 'helpString': The Client Setting Name must be typed exactly as it appears in the client registry, including necessary underscores. NOTE: most settings have no spaces (Example: LogVerbosityLevel)
    - 'label': Client Setting Name
    - 'maxChars': 64
    - 'promptText': Enter the Client Setting Name

  * Sensor Name: 'Tanium Client Subnet', Platforms: Windows, Linux, Mac, Category: Tanium
  * Description: The Subnet in use by the Tanium Client. Example: 192.168.10.0/24

  * Sensor Name: 'Has Application Management Tools', Platforms: Windows, Category: Tanium
  * Description: Returns whether a machine has the application management tools which may be necessary for parameterized actions or sensor-fed actions. Example: Yes

  * Sensor Name: 'Has Hardware Tools', Platforms: Windows, Category: Tanium
  * Description: Returns whether a machine has the hardware tools, which are used to identify specific types of hardware. Example: Yes

  * Sensor Name: 'Has Tanium Standard Utilities', Platforms: Windows, Category: Tanium
  * Description: Returns whether a machine has the Tanium Standard Utilities Example: Yes

  * Sensor Name: 'Tanium Client Downloads Directory Details', Platforms: Windows, Category: Tanium
  * Description: Returns the path to and size of the Tanium Client "Downloads" directory.  This is the directory to which Tanium Package files are downloaded.  It is considered temporary space and will clean itself out periodically. Example: C:\Program Files (x86)\Tanium\Tanium Client\Downloads|139.4 MB

  * Sensor Name: 'Tanium Client Installation Date', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Tanium
  * Description: The date on which the currently installed Tanium Client was installed on each client machine. Example: Wed, 13 Nov 2013 00:00:00 -0480

  * Sensor Name: 'Tanium Client Installation Time', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Tanium
  * Description: The date and time on which the currently installed Tanium Client was installed on each client machine. Example: Wed, 13 Nov 2013 08:18:00 -0480

  * Sensor Name: 'Tanium Client CPU', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Tanium
  * Description: The current cpu utilization being used by the Tanium Client process on each client machine.  The reported value will be higher than average since the Tanium Client is actively in use while evaluating this Sensor. Example: 1%

  * Sensor Name: 'Tanium File Exists', Platforms: Windows, Category: Tanium
  * Description: Provided with a parameter indicating the path to a file in the Tanium current directory, returns True or False based on whether that file exists in the specified location. Example: True
  * Parameter 'file':
    - 'helpString': Starting from the Client installation directory, complete the file path to get contents for.
    - 'label': Relative file path from <Tanium Client Installation Dir>
    - 'promptText': e.g. uninst.exe or Tools\Wsusscn2.cab

  * Sensor Name: 'Tanium Client Core Health', Platforms: Windows, Linux, Mac, Category: Tanium Diagnostics
  * Description: Determines whether the Tanium Client is able to execute the default content set successfully.  Returns any error conditions. Example: Error: Windows Script Host version must be at least 5.6

  * Sensor Name: 'Tanium Client Logging Level', Platforms: Windows, Linux, Mac, Category: Tanium Diagnostics
  * Description: Logging level setting between 1 and 100 of the Tanium Client on the client machine. Example: 41

  * Sensor Name: 'Tanium Client IP Address', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Tanium Diagnostics
  * Description: The local IP address the client is using to communicate with the Tanium Server. Example: 192.168.10.2

  * Sensor Name: 'Tanium Server Name List', Platforms: Windows, Category: Tanium Diagnostics
  * Description: Retrieves the Tanium Server Name List from the Client's Registry Example: server.domain.com,server1.domain.com

  * Sensor Name: 'Tanium Buffer Count', Platforms: Windows, Category: Tanium Diagnostics
  * Description: The number of buffered messages currently queued to be processed by the Tanium client on each client machine. Example: 2

  * Sensor Name: 'Tanium Client Neighborhood', Platforms: Windows, Linux, Category: Tanium Diagnostics
  * Description: Returns the Forward Peers and Backwards Peers returned by the server with which the client should communicate. Example: 10.0.0.1:17472, 10.0.02:17472 | 10.0.0.10:17472

  * Sensor Name: 'Tanium Client Action Timing', Platforms: Windows, Category: Tanium Diagnostics
  * Description: The number of seconds it took to download and complete the Action once a Client first sees the Action. Example: 300 seconds
  * Parameter 'strId':
    - 'helpString': Enter the Action ID number as seen in the Action History
    - 'label': Action ID number
    - 'promptText': e.g. 1234

  * Sensor Name: 'Tanium Client Dump Files', Platforms: Windows, Category: Tanium Diagnostics
  * Description: Report date and size of Tanium Client dumpfiles.

  * Sensor Name: 'Tanium Sensor Randomization Enabled', Platforms: Windows, Category: Tanium Diagnostics
  * Description: Returns if sensor execution is randomized on an endpoint, for better distribution on VDI / VM environments. Example: Yes

  * Sensor Name: 'Tanium Client NAT IP Address', Platforms: Windows, Category: Tanium Diagnostics
  * Description: The IP address the Tanium Client is communicating to the server with.  This can be a public IP, or IP of a NAT device, for example. Example: 65.128.25.253

  * Sensor Name: 'Tanium File Contents', Platforms: Windows, Category: Tanium Diagnostics
  * Description: Provided with a parameter indicating the path to a file in the Tanium current directory, this sensor will return the contents of that file. Example: <arbitrary file output>
  * Parameter 'filePath':
    - 'helpString': Starting from the Client installation directory, complete the file path to get contents for.
    - 'label': Relative file path from <Tanium Client Installation Dir>
    - 'promptText': e.g. Tools\MyTool\MyLog.txt

  * Sensor Name: 'Tanium Server Name', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Tanium Diagnostics
  * Description: Retrieves the Tanium Server Name from the Client's Registry Example: server.domain.com

  * Sensor Name: 'Tanium Current Directory', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Tanium Diagnostics
  * Description: Installation directory of the Tanium Client on the client machine. Example: C:\Program Files\Tanium\Tanium Client

  * Sensor Name: 'Tanium Peer Address', Platforms: Windows, Linux, Mac, Category: Tanium Diagnostics
  * Description: Returns the IP address of the peer specified in th Tanium registry entry at HKLM\SOFTWARE\Tanium\Tanium Client\Status\PeerAddress on windows and TaniumClientStatus.ini on non-windows endpoints. Example: 192.168.1.123

  * Sensor Name: 'Tanium Back Peer Address', Platforms: Windows, Linux, Mac, Category: Tanium Diagnostics
  * Description: Returns the IP address of the back peer specified in th Tanium registry entry at HKLM\SOFTWARE\Tanium\Tanium Client\Status\PeerAddress on windows and TaniumClientStatus.ini on non-windows endpoints. Example: 192.168.1.123

  * Sensor Name: 'Tanium Action Log', Platforms: Windows, Linux, Category: Tanium Diagnostics
  * Description: Provided with an action number as a parameter, this sensor returns the log from the action from each client machine that executed the action. Example: 2012-11-02 03:30:17 +0000|Command Completed
  * Parameter 'actionNumber':
    - 'helpString': Enter a valid Action ID Number from the Action History tab
    - 'label': Action ID Number
    - 'promptText': e.g. 1234

  * Sensor Name: 'Has Stale Tanium Client Data', Platforms: Windows, Category: Tanium Diagnostics
  * Description: Evaluates whether a machine has stale Tanium Client data - long running processes, old action status/log files, action folders, or sensor output. Example: Yes

  * Sensor Name: 'Tanium Client Action Folder Sizes', Platforms: Windows, Mac, Category: Tanium Diagnostics
  * Description: Returns the combined size of all Action_XXXX subdirectories in the Tanium Client\Downloads directory. Example: 351 MB

  * Sensor Name: 'Last Date of Local Administrator Login', Platforms: Windows, Mac, Category: User
  * Description: Provides the last time a local administrator logged into the machine. Example: Administrator 5/10/2012

  * Sensor Name: 'Logged In Users', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: User
  * Description: Provides a list of users currently logged in to the client machine.  Includes Remote Desktop sessions on Windows. Example: Administrator

  * Sensor Name: 'Last Logged In User', Platforms: Windows, Linux, Mac, AIX, Category: User
  * Description: If no user is logged in, returns the last user to log in is reported.  If a user is currently logged in, that user is returned. Example: DOMAIN\Jane.Doe

  * Sensor Name: 'User Sessions', Platforms: Windows, Mac, Category: User
  * Description: Provides the terminal services session information, similar to what is available from the "query session" command. Example:console|Administrator|1|Active||

  * Sensor Name: 'User Accounts', Platforms: Linux, AIX, Category: User
  * Description: List of user accounts on a linux client machine. Example: webadmin

  * Sensor Name: 'Logged in User Details', Platforms: Windows, Solaris, AIX, Category: User
  * Description: Provides various properties for users which are currently logged into the machine. Example: CORP\john.doe | John Doe | john.doe@organization.com

  * Sensor Name: 'Last Logins', Platforms: Linux, Solaris, AIX, Category: User
  * Description: Returns details about last logins on systems. Example: user.name      pts/1    192.168.1.2  Thu Nov  8 22:07:30 -0800 2012

  * Sensor Name: 'Local Account Last Password Change Days Ago', Platforms: Windows, Category: User
  * Description: Returns local accounts and number of days ago that the password was changed. Example: user.name|19

  * Sensor Name: 'Number of Logged In Users', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: User
  * Description: Returns the number of interactively logged in users.  On Windows, this will include Remote Desktop sessions. Example: 2

  * Sensor Name: 'Local Account Expiration Details', Platforms: Windows, Category: User
  * Description: Returns local accounts and days until they expire. Accounts which have no expiration date return "N/A" Example: user.name|19

  * Sensor Name: 'User Profile Directory Details', Platforms: Windows, Category: User
  * Description: Returns the location of all user profiles and their sizes Example:C:\Users\John.Doe 28.2 GB

  * Sensor Name: 'User Details', Platforms: Windows, Linux, Mac, AIX, Category: User
  * Description: Returns a list of local users to the Windows machine and the user's full name. Example:johndoe|John Doe

  * Sensor Name: 'Security Event Log IDs', Platforms: Windows, Category: Windows Event Logs
  * Description: Event identifier code for Security log events as shown in the Windows NT Event Viewer tool. Example: 4648

  * Sensor Name: 'System Event Log IDs', Platforms: Windows, Category: Windows Event Logs
  * Description: Event codes for Windows event logs of type System and Error. Example: 8009

  * Sensor Name: 'Application Event Log IDs', Platforms: Windows, Category: Windows Event Logs
  * Description: Recent event codes from the application event logs in Windows. Example: 1001
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Print all Linux sensors

```bash
bin/print_sensors.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --all --platform Linux
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
Found items:  SensorList, len: 567
Filtered out sourced sensors: 332
Filtered out sensors based on user filters: 119

  * Sensor Name: 'Installed Applications', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Applications
  * Description: List of the applications and versions of those applications installed on the client machine. Example: Mozilla Firefox | 16.0.1

  * Sensor Name: 'Running Processes', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Applications
  * Description: Provides a list of processes currently running on the client machine. Example: svchost.exe

  * Sensor Name: 'Running Service', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Applications
  * Description: Provides a list of currently running services on the client machine. Example: DHCP Client

  * Sensor Name: 'Installed Application Version', Platforms: Windows, Linux, Mac, AIX, Category: Applications
  * Description: The version string of applications which match the parameter given. Example:  11.5.502.146
  * Parameter 'application':
    - 'helpString': Enter the application name to search for
    - 'label': Application Name
    - 'promptText': e.g. Adobe Flash Player

  * Sensor Name: 'Running Processes Memory Usage', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Applications
  * Description: Returns all running processes along with the memory each process uses.  This is the process's working set. Example: lsass.exe|23 MB

  * Sensor Name: 'Installed Pkgs', Platforms: Linux, Mac, Solaris, AIX, Category: Applications
  * Description: Returns a list of installed Packages by name on Solaris systems. Example: glibc-2.5-12

  * Sensor Name: 'Application Run Time', Platforms: Windows, Linux, Solaris, AIX, Category: Applications
  * Description: Shows applications that are currently running and how long they have been running for. Example: Dropbox - 3 days

  * Sensor Name: 'Installed RPMs', Platforms: Linux, AIX, Category: Applications
  * Description: Returns a list of installed RPMs by name on Linux systems. Example: glibc-2.5-12

  * Sensor Name: 'Service', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Applications
  * Description: Gets a list of all Services on the client machine. Example: Task Scheduler

  * Sensor Name: 'Folder Exists', Platforms: Windows, Linux, Mac, Category: File System
  * Description: A parameterized Sensor that checks to see if a folder exists on a machine.  If it does, it returns back the full path of the folder. Will expand environment variables, and will expand %userprofile%/folder or "~/folder" to search all user home directories. Example: C:\Windows\system32
  * Parameter 'folder':
    - 'helpString': Enter the full drive letter and folder path of the folder. Environment variables accepted.
    - 'label': Folder path to search for
    - 'promptText': e.g. c:\Program Files\MyApp

  * Sensor Name: 'Physical Volumes', Platforms: Linux, AIX, Category: File System
  * Description: 

  * Sensor Name: 'Volume Group Names', Platforms: Linux, Category: File System
  * Description: Display Volume Group Names

  * Sensor Name: 'File Exists', Platforms: Windows, Linux, Mac, Category: File System
  * Description: A parameterized Sensor that checks to see if a file exists on a machine.  If it does, it returns back the full path of the file. Will expand environment variables, and will expand %userprofile%/file or "~/file" to search all user home directories. Example: C:\Windows\system32\notepad.exe
  * Parameter 'file':
    - 'helpString': Enter the file path and name to search for.
    - 'label': File path and name to search for
    - 'promptText': e.g. c:\windows\test.txt

  * Sensor Name: 'Logical Volumes', Platforms: Linux, AIX, Category: File System
  * Description: Display Logical Volume Names

  * Sensor Name: 'File Size', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: File System
  * Description: Returns the size of the file specified by the parameter. Example: 69120
  * Parameter 'filename':
    - 'helpString': Enter the full drive letter, folder path and file name of the file.
    - 'label': File name to search for
    - 'promptText': e.g. c:\windows\test.txt

  * Sensor Name: 'USB Storage Devices', Platforms: Windows, Linux, Category: Hardware
  * Description: Returns a list of USB storage devices currently plugged in to the client machine. Example: USB Mass Storage Device

  * Sensor Name: 'CPU Speed Mhz', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: The speed of the processor in Mhz. Example: 3200 Mhz

  * Sensor Name: 'CPU Consumption', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: Current total CPU consumption in %. Example: 50%

  * Sensor Name: 'Disk Free Space Below Threshold', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: If a drive has less free space than the configured threshold, the drive and remaining free space is returned.  The threshold defaults to 2048 MB and can be altered. Example: C: 1 GB

  * Sensor Name: 'RAM', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: Returns the total amount of installed RAM, in Megabytes. Example: 2048 MB

  * Sensor Name: 'Chassis Type', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: The machine or chassis type for the machine. Example: Server or Virtual

  * Sensor Name: 'CPU Details', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: A multi-column sensor that provides CPU details: system type, CPU description, speed, # of processors, # of cores, and # of logical processors. Example: x64-based PC | Intel(R) Xeon(R) CPU X3430 | 2390 Mhz | 1 | 4 | 4

  * Sensor Name: 'Disk Total Space', Platforms: Windows, Linux, Mac, AIX, Category: Hardware
  * Description: The amount of total disk space per drive. Example: C: 100 GB

  * Sensor Name: 'Disk Free Space', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: The amount of free disk space per drive. Example: C: 40 GB

  * Sensor Name: 'Disk Used Percentage', Platforms: Windows, Linux, Mac, AIX, Category: Hardware
  * Description: The percentage of used disk space per partition. Example: C: 24%

  * Sensor Name: 'BIOS Name', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: Name of BIOS. Example: Phoenix ROM BIOS PLUS Version 1.10 A10

  * Sensor Name: 'BIOS Release Date', Platforms: Windows, Linux, Mac, AIX, Category: Hardware
  * Description: Release date of the BIOS. Example: 20080436.2.314..016400+000

  * Sensor Name: 'BIOS Version', Platforms: Windows, Linux, AIX, Category: Hardware
  * Description: Version of the BIOS. Example: A11

  * Sensor Name: 'Computer Serial Number', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: The serial number, if available, provided by the computer manufacturer. Example: 123ABC1

  * Sensor Name: 'Free Memory', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: Indicates the free RAM available to the operating system. Example: 1024MB

  * Sensor Name: 'Used Memory', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: Memory in use in MB from client machine. Example: 6348 MB

  * Sensor Name: 'BIOS Vendor', Platforms: Windows, Linux, AIX, Category: Hardware
  * Description: Manufacturer or vendor of the BIOS. Example: Dell, Inc.

  * Sensor Name: 'x64/x86?', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: Returns whether the client machine is 64-bit or 32-bit (x86). Example: X86-based PC

  * Sensor Name: 'Audio Controller', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: Description of the onboard audio controller for the computer. Example: Intel(R) High Definition Audio Controller

  * Sensor Name: 'CPU Manufacturer', Platforms: Windows, Linux, Mac, Solaris, Category: Hardware
  * Description: The manufacturer of the CPU. Example: GenuineIntel

  * Sensor Name: 'CPU Architecture', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: Describes the architecture of the CPU/processor. Example: i386, X86-based PC

  * Sensor Name: 'Manufacturer', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: Returns System or Motherboard manufacturer (OS Dependent). Example: Apple

  * Sensor Name: 'Motherboard Name', Platforms: Windows, Linux, Category: Hardware
  * Description: Returns the motherboard product name of a system. Example: 440BX Desktop Reference Platform

  * Sensor Name: 'Network Adapter Name', Platforms: Windows, Linux, Solaris, AIX, Category: Hardware
  * Description: Returns the names of network adapters that are active. Example: VMware Accelerated AMD PCNet Adapter

  * Sensor Name: 'CPU', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: Description of the CPU. Example: Intel(R) Core(TM) i5-2500 CPU @ 3.30GHz

  * Sensor Name: 'Model', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Hardware
  * Description: Returns the Model of a system. Example: Precision T1600

  * Sensor Name: 'Motherboard Version', Platforms: Windows, Linux, Category: Hardware
  * Description: Returns the Version of a motherboard. Example:9230

  * Sensor Name: 'Total Memory', Platforms: Windows, Linux, Mac, AIX, Category: Hardware
  * Description: The total physical memory installed in the client machine. Example: 8000 MB

  * Sensor Name: 'Number of Processors', Platforms: Windows, Linux, Mac, Solaris, Category: Hardware
  * Description: Returns the number of physical processors on a system.  This may differ from the number of cores or number of logical processors. Example:1

  * Sensor Name: 'CPU Cache Size', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: CPU cache size in KB. Example: 1024 KB

  * Sensor Name: 'CPU Family', Platforms: Windows, Linux, Solaris, AIX, Category: Hardware
  * Description: The family of the processor or CPU (Windows provides a family ID). Example: Xeon, Family 198

  * Sensor Name: 'Disk Used Space', Platforms: Windows, Linux, Mac, AIX, Category: Hardware
  * Description: The amount of used disk space per partition. Example: C: 40 GB

  * Sensor Name: 'Motherboard Manufacturer', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: Returns the Motherboard Manufacturer of a system. Example:Lenovo

  * Sensor Name: 'CD-ROM Drive', Platforms: Windows, Linux, Category: Hardware
  * Description: Name of any installed CD-ROM or DVD-ROM drives. Example: SONY DVD-ROM DDU1615 ATA Device

  * Sensor Name: 'Video/Graphics Card', Platforms: Windows, Linux, Mac, Category: Hardware
  * Description: Description of the video card in the client machine. Example: ATI Radeon HD 2400 Pro

  * Sensor Name: 'Online', Platforms: Windows, Linux, Mac, AIX, Category: Miscellaneous
  * Description: Returns, in all cases, the word True.  This sensor is used in many ways, including to find a common target for machines which may have responded to a question with a 'where' clause - get "online from machines where IP address starts with 192.168.10." will allow you to target the respondents with an action or count responses. Example:True

  * Sensor Name: 'High CPU Processes', Platforms: Windows, Linux, Mac, Category: Miscellaneous
  * Description: Lists the specified number of processes that are using the highest amount of CPU. Example: cmd
  * Parameter 'numOutput':
    - 'defaultValue': 5
    - 'helpString': Enter the number of processes to return
    - 'label': Number of Processes
    - 'maximum': 50
    - 'minimum': 1
    - 'stepSize': 1
    - 'value': 5

  * Sensor Name: 'High Memory Processes', Platforms: Windows, Linux, Mac, Category: Miscellaneous
  * Description: Lists the specified number processes based on ordering on amount of memory used. Example: cmd
  * Parameter 'numOutput':
    - 'defaultValue': 5
    - 'helpString': Enter the number of processes to return
    - 'label': Number of Processes
    - 'maximum': 50
    - 'minimum': 1
    - 'stepSize': 1
    - 'value': 5

  * Sensor Name: 'Client Time', Platforms: Windows, Linux, Mac, Category: Miscellaneous
  * Description: The local time on the managed client. Example: 5:17:44 PM

  * Sensor Name: 'Client Date', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Miscellaneous
  * Description: The calendar date on the managed client. Example: 01/30/2012

  * Sensor Name: 'IP Address', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Network
  * Description: Current IP Addresses of client machine. Example: 192.168.1.1

  * Sensor Name: 'MAC Address', Platforms: Windows, Linux, Mac, Solaris, Category: Network
  * Description: Returns MAC addresses for all IP enabled network connections. Example:00:0C:29:68:6A:D8

  * Sensor Name: 'DNS Server', Platforms: Windows, Linux, Mac, Solaris, Category: Network
  * Description: Addresses of any configured DNS servers for active network adapters. Example: 192.168.1.1, 8.8.8.8

  * Sensor Name: 'Domain Name', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Network
  * Description: The domain name (if any) that the computer is joined to or configured for. Example: intra.company.com

  * Sensor Name: 'Established Connections', Platforms: Windows, Linux, Mac, Category: Network
  * Description: Any established connections currently being made.  This multi-column Sensor displays the process responsible for the connection, the display name of the process (if available), and the target IP Address and port.  Processes and IP ranges can be excluded in the Sensor definition. Example: chrome.exe | Google Chrome | 173.194.79.99:80

  * Sensor Name: 'Network Throughput Outbound', Platforms: Windows, Linux, Solaris, Category: Network
  * Description: Returns the current output throughput, in KB/Sec, of the network interface used to connect to the tanium server. Example: 1024 KB/S

  * Sensor Name: 'Established Ports by Application', Platforms: Windows, Linux, Mac, Category: Network
  * Description: Parameterized Sensor that shows which addresses the process is connecting to and over what local port. Example: 0.0.0.0:17500
  * Parameter 'app':
    - 'helpString': Enter the process name to query
    - 'label': Process Name to examine
    - 'promptText': e.g. svchost.exe

  * Sensor Name: 'Network Throughput Inbound', Platforms: Windows, Linux, Solaris, Category: Network
  * Description: Returns the current inbound throughput, in KB/Sec, of the network interface used to connect to the tanium server. Example: 1024 KB/S

  * Sensor Name: 'TCP connections', Platforms: Linux, Category: Network
  * Description: Lists all TCP connections on a machine wth their state. Example: TaniumClient|

  * Sensor Name: 'Listen Ports', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Network
  * Description: Returns information network-aware processes and the ports they have bound to. Example: googletalkplugin.exe Google Talk Plugin :60042

  * Sensor Name: 'UDP Connections', Platforms: Linux, Category: Network
  * Description: 

  * Sensor Name: 'Hosts File Entries', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Network
  * Description: Provides a list of hosts file entries for the local operating system. Example: myserver.com , 192.168.1.100

  * Sensor Name: 'IP Route Details', Platforms: Windows, Linux, Mac, Solaris, Category: Network
  * Description: Returns IPv4 network routes, filtered to exclude noise. With Flags, Metric, Interface columns. Example:  172.16.0.0|192.168.1.1|255.255.0.0|UG|100|eth0

  * Sensor Name: 'IP Routes', Platforms: Windows, Linux, Mac, Solaris, Category: Network
  * Description: Returns IPv4 network routes, filtered to exclude noise. Example:  172.16.0.0|192.168.1.1|255.255.0.0

  * Sensor Name: 'Open Port', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Network
  * Description: Returns the ports which are listening on a local machine and the IP address the port is bound to.  0.0.0.0 indicates that the port is bound to all IP addresses. Example: 0.0.0.0:80

  * Sensor Name: 'Operating System', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns the name of the Operating System from all machines.  This name may be localized. Example: Windows Server 2008 R2 Enterprise

  * Sensor Name: 'Is Windows', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns whether the machine runs Windows.  True if so, False if not. Example: True

  * Sensor Name: 'Username', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns the currently logged in user, and No User if nobody is logged in. Example: Domain\JDoe

  * Sensor Name: 'Reboot Required', Platforms: Windows, Linux, Mac, Category: Operating System
  * Description: Returns data indicating that a reboot is required and, if so, for which reason. Example: Yes

  * Sensor Name: 'Memory Consumption', Platforms: Windows, Linux, Mac, Solaris, Category: Operating System
  * Description: Returns the percentage of used (committed) memory on a system. Example: 27 percent

  * Sensor Name: 'Uptime', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Time since reboot in days of the client machine. Example: 48 days

  * Sensor Name: 'Load Average', Platforms: Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns the average CPU load on a Mac or Linux system  Example: 0.00 0.03 0.10

  * Sensor Name: 'Maximum Process Memory Size', Platforms: Windows, Linux, Mac, Solaris, Category: Operating System
  * Description: Returns the maximum amount of memory, in Kilobytes, that a process can use.  This may be free physical RAM and virtual RAM combined, or may be an arbitrary upper ceiling. Example: 2097024

  * Sensor Name: 'Is Mac', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns whether the machine is a Mac.  True if so, False if not. Example: True

  * Sensor Name: 'Last Reboot', Platforms: Windows, Linux, Mac, Solaris, Category: Operating System
  * Description: Returns the time the last reboot occurred. Example: 2012-12-11 09:01

  * Sensor Name: 'Time Zone Offset', Platforms: Windows, Linux, Mac, Solaris, Category: Operating System
  * Description: Returns the time offset in minutes. Example: -0700

  * Sensor Name: 'Low Disk Space', Platforms: Windows, Linux, Solaris, Category: Operating System
  * Description: Returns disk drives which have less than 2 gigabytes free. Example: C:

  * Sensor Name: 'Number Of Users', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns the number of user sessions for which the operating system is storing state.  This may differ from the number of interactively logged in users. Example:3

  * Sensor Name: 'Total Swap', Platforms: Linux, Solaris, AIX, Category: Operating System
  * Description: Total swap space configured by client machine. Example: 4000 MB

  * Sensor Name: 'Is Linux', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns whether the machine runs a Linux-based OS.  True if so, False if not. Example: True

  * Sensor Name: 'Is AIX', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns whether the machine runs a AIX OS.  True if so, False if not. Example: True

  * Sensor Name: 'Is Solaris', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns whether the machine runs a Solaris-based OS.  True if so, False if not. Example: True

  * Sensor Name: 'Used Swap', Platforms: Linux, Solaris, Category: Operating System
  * Description: Swap space in use in MB by the client machine. Example: 2164 MB

  * Sensor Name: 'System UUID', Platforms: Linux, Mac, Category: Operating System
  * Description: System unique identifier UUID on Mac or Linux machines. Example: 3e6be9de-8139-11d1-9106-a43f08d823a6

  * Sensor Name: 'Free Swap', Platforms: Linux, Solaris, AIX, Category: Operating System
  * Description: Indicates the free swap space available to the operating system. Example: 640MB

  * Sensor Name: 'Run Level', Platforms: Linux, Solaris, AIX, Category: Operating System
  * Description: Returns the set run level of Linux systems Example: 3

  * Sensor Name: 'CPU by Process', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: A multi-column sensor that lists every running process and the amount of CPU usage they are taking up. Example: svchost | 15

  * Sensor Name: 'Windows OS Type', Platforms: Windows, Linux, Mac, Category: Operating System
  * Description: Will output "Windows Server" or "Windows Workstation" depending on the OS type. Example: Windows Server

  * Sensor Name: 'Kernel Modules', Platforms: Linux, Solaris, Category: Operating System
  * Description: Returns loaded kernel modules on Linux systems. Example:dcdbas

  * Sensor Name: 'Is Mac API TEST', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns whether the machine is a Mac.  True if so, False if not. Example: True

  * Sensor Name: 'Local User Password Change Dates', Platforms: Windows, Linux, Mac, Category: Security
  * Description: Returns the last time the password was set for each user account. Example:  taniumuser|2013-10-31

  * Sensor Name: 'High Uptime', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Software
  * Description: Indicates whether the client machine has been online for more than 30 days. Example: Less than 30 days

  * Sensor Name: 'VMware Guest', Platforms: Windows, Linux, Category: Software
  * Description: Returns True if client machine is a guest VM in VMware. Example: True

  * Sensor Name: 'Custom Tags', Platforms: Windows, Linux, Mac, Category: Tags
  * Description: Any specified custom tags that have been set for this machine.  See the Custom Tagging Dashboard. Example:  Development, Test-Machines

  * Sensor Name: 'Tanium Client Version', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Tanium
  * Description: Version number of the Tanium Client on the client machine. Example: 4.1.314.7020

  * Sensor Name: 'Tanium Client Subnet', Platforms: Windows, Linux, Mac, Category: Tanium
  * Description: The Subnet in use by the Tanium Client. Example: 192.168.10.0/24

  * Sensor Name: 'Tanium Client Installation Date', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Tanium
  * Description: The date on which the currently installed Tanium Client was installed on each client machine. Example: Wed, 13 Nov 2013 00:00:00 -0480

  * Sensor Name: 'Tanium Client Installation Time', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Tanium
  * Description: The date and time on which the currently installed Tanium Client was installed on each client machine. Example: Wed, 13 Nov 2013 08:18:00 -0480

  * Sensor Name: 'Tanium Client CPU', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Tanium
  * Description: The current cpu utilization being used by the Tanium Client process on each client machine.  The reported value will be higher than average since the Tanium Client is actively in use while evaluating this Sensor. Example: 1%

  * Sensor Name: 'Tanium Client Core Health', Platforms: Windows, Linux, Mac, Category: Tanium Diagnostics
  * Description: Determines whether the Tanium Client is able to execute the default content set successfully.  Returns any error conditions. Example: Error: Windows Script Host version must be at least 5.6

  * Sensor Name: 'Tanium Client Logging Level', Platforms: Windows, Linux, Mac, Category: Tanium Diagnostics
  * Description: Logging level setting between 1 and 100 of the Tanium Client on the client machine. Example: 41

  * Sensor Name: 'Tanium Client IP Address', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Tanium Diagnostics
  * Description: The local IP address the client is using to communicate with the Tanium Server. Example: 192.168.10.2

  * Sensor Name: 'Tanium Client Neighborhood', Platforms: Windows, Linux, Category: Tanium Diagnostics
  * Description: Returns the Forward Peers and Backwards Peers returned by the server with which the client should communicate. Example: 10.0.0.1:17472, 10.0.02:17472 | 10.0.0.10:17472

  * Sensor Name: 'Tanium Server Name', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Tanium Diagnostics
  * Description: Retrieves the Tanium Server Name from the Client's Registry Example: server.domain.com

  * Sensor Name: 'Tanium Current Directory', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Tanium Diagnostics
  * Description: Installation directory of the Tanium Client on the client machine. Example: C:\Program Files\Tanium\Tanium Client

  * Sensor Name: 'Tanium Peer Address', Platforms: Windows, Linux, Mac, Category: Tanium Diagnostics
  * Description: Returns the IP address of the peer specified in th Tanium registry entry at HKLM\SOFTWARE\Tanium\Tanium Client\Status\PeerAddress on windows and TaniumClientStatus.ini on non-windows endpoints. Example: 192.168.1.123

  * Sensor Name: 'Tanium Back Peer Address', Platforms: Windows, Linux, Mac, Category: Tanium Diagnostics
  * Description: Returns the IP address of the back peer specified in th Tanium registry entry at HKLM\SOFTWARE\Tanium\Tanium Client\Status\PeerAddress on windows and TaniumClientStatus.ini on non-windows endpoints. Example: 192.168.1.123

  * Sensor Name: 'Tanium Action Log', Platforms: Windows, Linux, Category: Tanium Diagnostics
  * Description: Provided with an action number as a parameter, this sensor returns the log from the action from each client machine that executed the action. Example: 2012-11-02 03:30:17 +0000|Command Completed
  * Parameter 'actionNumber':
    - 'helpString': Enter a valid Action ID Number from the Action History tab
    - 'label': Action ID Number
    - 'promptText': e.g. 1234

  * Sensor Name: 'Logged In Users', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: User
  * Description: Provides a list of users currently logged in to the client machine.  Includes Remote Desktop sessions on Windows. Example: Administrator

  * Sensor Name: 'Last Logged In User', Platforms: Windows, Linux, Mac, AIX, Category: User
  * Description: If no user is logged in, returns the last user to log in is reported.  If a user is currently logged in, that user is returned. Example: DOMAIN\Jane.Doe

  * Sensor Name: 'User Accounts', Platforms: Linux, AIX, Category: User
  * Description: List of user accounts on a linux client machine. Example: webadmin

  * Sensor Name: 'Last Logins', Platforms: Linux, Solaris, AIX, Category: User
  * Description: Returns details about last logins on systems. Example: user.name      pts/1    192.168.1.2  Thu Nov  8 22:07:30 -0800 2012

  * Sensor Name: 'Number of Logged In Users', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: User
  * Description: Returns the number of interactively logged in users.  On Windows, this will include Remote Desktop sessions. Example: 2

  * Sensor Name: 'User Details', Platforms: Windows, Linux, Mac, AIX, Category: User
  * Description: Returns a list of local users to the Windows machine and the user's full name. Example:johndoe|John Doe
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Print all Linux sensors that fall under the category "Operating System"

```bash
bin/print_sensors.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --all --platform Linux --category "Operating System"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
Found items:  SensorList, len: 567
Filtered out sourced sensors: 332
Filtered out sensors based on user filters: 25

  * Sensor Name: 'Operating System', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns the name of the Operating System from all machines.  This name may be localized. Example: Windows Server 2008 R2 Enterprise

  * Sensor Name: 'Is Windows', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns whether the machine runs Windows.  True if so, False if not. Example: True

  * Sensor Name: 'Username', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns the currently logged in user, and No User if nobody is logged in. Example: Domain\JDoe

  * Sensor Name: 'Reboot Required', Platforms: Windows, Linux, Mac, Category: Operating System
  * Description: Returns data indicating that a reboot is required and, if so, for which reason. Example: Yes

  * Sensor Name: 'Memory Consumption', Platforms: Windows, Linux, Mac, Solaris, Category: Operating System
  * Description: Returns the percentage of used (committed) memory on a system. Example: 27 percent

  * Sensor Name: 'Uptime', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Time since reboot in days of the client machine. Example: 48 days

  * Sensor Name: 'Load Average', Platforms: Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns the average CPU load on a Mac or Linux system  Example: 0.00 0.03 0.10

  * Sensor Name: 'Maximum Process Memory Size', Platforms: Windows, Linux, Mac, Solaris, Category: Operating System
  * Description: Returns the maximum amount of memory, in Kilobytes, that a process can use.  This may be free physical RAM and virtual RAM combined, or may be an arbitrary upper ceiling. Example: 2097024

  * Sensor Name: 'Is Mac', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns whether the machine is a Mac.  True if so, False if not. Example: True

  * Sensor Name: 'Last Reboot', Platforms: Windows, Linux, Mac, Solaris, Category: Operating System
  * Description: Returns the time the last reboot occurred. Example: 2012-12-11 09:01

  * Sensor Name: 'Time Zone Offset', Platforms: Windows, Linux, Mac, Solaris, Category: Operating System
  * Description: Returns the time offset in minutes. Example: -0700

  * Sensor Name: 'Low Disk Space', Platforms: Windows, Linux, Solaris, Category: Operating System
  * Description: Returns disk drives which have less than 2 gigabytes free. Example: C:

  * Sensor Name: 'Number Of Users', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns the number of user sessions for which the operating system is storing state.  This may differ from the number of interactively logged in users. Example:3

  * Sensor Name: 'Total Swap', Platforms: Linux, Solaris, AIX, Category: Operating System
  * Description: Total swap space configured by client machine. Example: 4000 MB

  * Sensor Name: 'Is Linux', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns whether the machine runs a Linux-based OS.  True if so, False if not. Example: True

  * Sensor Name: 'Is AIX', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns whether the machine runs a AIX OS.  True if so, False if not. Example: True

  * Sensor Name: 'Is Solaris', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns whether the machine runs a Solaris-based OS.  True if so, False if not. Example: True

  * Sensor Name: 'Used Swap', Platforms: Linux, Solaris, Category: Operating System
  * Description: Swap space in use in MB by the client machine. Example: 2164 MB

  * Sensor Name: 'System UUID', Platforms: Linux, Mac, Category: Operating System
  * Description: System unique identifier UUID on Mac or Linux machines. Example: 3e6be9de-8139-11d1-9106-a43f08d823a6

  * Sensor Name: 'Free Swap', Platforms: Linux, Solaris, AIX, Category: Operating System
  * Description: Indicates the free swap space available to the operating system. Example: 640MB

  * Sensor Name: 'Run Level', Platforms: Linux, Solaris, AIX, Category: Operating System
  * Description: Returns the set run level of Linux systems Example: 3

  * Sensor Name: 'CPU by Process', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: A multi-column sensor that lists every running process and the amount of CPU usage they are taking up. Example: svchost | 15

  * Sensor Name: 'Windows OS Type', Platforms: Windows, Linux, Mac, Category: Operating System
  * Description: Will output "Windows Server" or "Windows Workstation" depending on the OS type. Example: Windows Server

  * Sensor Name: 'Kernel Modules', Platforms: Linux, Solaris, Category: Operating System
  * Description: Returns loaded kernel modules on Linux systems. Example:dcdbas

  * Sensor Name: 'Is Mac API TEST', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: Operating System
  * Description: Returns whether the machine is a Mac.  True if so, False if not. Example: True
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Print all Mac and Windows sensors that fall under the category "User"

```bash
bin/print_sensors.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --all --platform Mac --platform Windows --category "User"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
Found items:  SensorList, len: 567
Filtered out sourced sensors: 332
Filtered out sensors based on user filters: 10

  * Sensor Name: 'Last Date of Local Administrator Login', Platforms: Windows, Mac, Category: User
  * Description: Provides the last time a local administrator logged into the machine. Example: Administrator 5/10/2012

  * Sensor Name: 'Logged In Users', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: User
  * Description: Provides a list of users currently logged in to the client machine.  Includes Remote Desktop sessions on Windows. Example: Administrator

  * Sensor Name: 'Last Logged In User', Platforms: Windows, Linux, Mac, AIX, Category: User
  * Description: If no user is logged in, returns the last user to log in is reported.  If a user is currently logged in, that user is returned. Example: DOMAIN\Jane.Doe

  * Sensor Name: 'User Sessions', Platforms: Windows, Mac, Category: User
  * Description: Provides the terminal services session information, similar to what is available from the "query session" command. Example:console|Administrator|1|Active||

  * Sensor Name: 'Logged in User Details', Platforms: Windows, Solaris, AIX, Category: User
  * Description: Provides various properties for users which are currently logged into the machine. Example: CORP\john.doe | John Doe | john.doe@organization.com

  * Sensor Name: 'Local Account Last Password Change Days Ago', Platforms: Windows, Category: User
  * Description: Returns local accounts and number of days ago that the password was changed. Example: user.name|19

  * Sensor Name: 'Number of Logged In Users', Platforms: Windows, Linux, Mac, Solaris, AIX, Category: User
  * Description: Returns the number of interactively logged in users.  On Windows, this will include Remote Desktop sessions. Example: 2

  * Sensor Name: 'Local Account Expiration Details', Platforms: Windows, Category: User
  * Description: Returns local accounts and days until they expire. Accounts which have no expiration date return "N/A" Example: user.name|19

  * Sensor Name: 'User Profile Directory Details', Platforms: Windows, Category: User
  * Description: Returns the location of all user profiles and their sizes Example:C:\Users\John.Doe 28.2 GB

  * Sensor Name: 'User Details', Platforms: Windows, Linux, Mac, AIX, Category: User
  * Description: Returns a list of local users to the Windows machine and the user's full name. Example:johndoe|John Doe
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v2.1.0`, date: Fri Oct  2 16:09:36 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**