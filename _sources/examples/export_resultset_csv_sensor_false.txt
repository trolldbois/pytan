
Export resultset csv sensor false
====================================================================================================
Export a ResultSet from asking a question as CSV with false for header_add_sensor

Example Python Code
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: python
    :linenos:


    # Path to lib directory which contains pytan package
    PYTAN_LIB_PATH = '../lib'
    
    # connection info for Tanium Server
    USERNAME = "Tanium User"
    PASSWORD = "T@n!um"
    HOST = "172.16.31.128"
    PORT = "444"
    
    # Logging conrols
    LOGLEVEL = 2
    DEBUGFORMAT = False
    
    import sys, tempfile
    sys.path.append(PYTAN_LIB_PATH)
    
    import pytan
    handler = pytan.Handler(
        username=USERNAME,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        loglevel=LOGLEVEL,
        debugformat=DEBUGFORMAT,
    )
    
    print handler
    
    # setup the export_obj kwargs for later
    export_kwargs = {}
    export_kwargs["export_format"] = u'csv'
    export_kwargs["header_add_sensor"] = False
    
    # ask the question that will provide the resultset that we want to use
    ask_kwargs = {
        'qtype': 'manual_human',
        'sensors': [
            "Computer Name", "IP Route Details", "IP Address",
            'Folder Name Search with RegEx Match{dirname=Program Files,regex=.*Shared.*}',
        ],
    }
    response = handler.ask(**ask_kwargs)
    
    # export the object to a string
    # (we could just as easily export to a file using export_to_report_file)
    export_kwargs['obj'] = response['question_results']
    export_str = handler.export_obj(**export_kwargs)
    
    
    print ""
    print "print the export_str returned from export_obj():"
    print export_str
    


Output from Python Code
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
    2014-12-07 01:23:22,675 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
    2014-12-07 01:23:27,701 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
    2014-12-07 01:23:32,725 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
    2014-12-07 01:23:37,753 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
    2014-12-07 01:23:42,781 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
    2014-12-07 01:23:47,806 INFO     question_progress: Results 50% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
    2014-12-07 01:23:52,840 INFO     question_progress: Results 100% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
    
    print the export_str returned from export_obj():
    Computer Name,Destination,Flags,"Folder Name Search with RegEx Match[No, Program Files, No, ]",Gateway,IP Address,Interface,Mask,Metric
    Casus-Belli.local,"default
    192.168.0
    169.254
    172.16.31/24
    192.168.0.1/32
    172.16.152/24
    192.168.0.3/32","UGSc
    UCS
    UCS
    UC
    UCS
    UC
    UCS",Windows Only,"192.168.0.1
    link#4
    link#4
    link#13
    link#4
    link#12
    link#4","fe80::e896:c1c9:d927:bbe0
    2604:2000:69e6:1a00:82e6:50ff:fe1d:1dca
    172.16.31.1
    fe80::82e6:50ff:fe1d:1dca
    172.16.152.1
    192.168.0.3
    fe80::2886:21ff:fe7f:3ef4
    2604:2000:69e6:1a00:95ad:5fe5:cf9e:5403
    fd1b:56a6:50eb:cd49:e896:c1c9:d927:bbe0","en0
    en0
    en0
    vmnet8
    en0
    vmnet1
    en0","None
    None
    None
    None
    None
    None
    None","None
    None
    None
    None
    None
    None
    None"
    jtanium1.localdomain,"172.16.31.128
    172.16.31.0
    127.0.0.1
    0.0.0.0
    127.0.0.0","-
    -
    -
    -
    -","C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\cgi-bin
    C:\Program Files\VMware\VMware Tools\plugins\vmsvc
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1040_ITA_LP\x64\1040\help
    C:\Program Files\Common Files\Microsoft Shared\VS7Debug
    C:\Program Files\Tanium\Tanium Server\Apache24\manual\style
    C:\Program Files\Tanium\Tanium Server\Apache24\htdocs\console\history
    C:\Program Files\Common Files\VMware\Drivers\vmci\sockets\include
    C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
    C:\Program Files\Tanium\Tanium Server\plugins\console\Dashboards
    C:\Program Files\Tanium\Tanium Server\CertificateBackup2014-11-17-11-17-33
    C:\Program Files\Common Files\SpeechEngines\Microsoft
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\modules
    C:\Program Files\Common Files\Microsoft Shared\ink\ru-RU
    C:\Program Files\Microsoft SQL Server\110\DTS\ForEachEnumerators\en
    C:\Program Files\Tanium\Tanium Server\Apache24\htdocs\php\Auth
    C:\Program Files\MSBuild\Microsoft\Windows Workflow Foundation\v3.0
    C:\Program Files\MSBuild\Microsoft\Windows Workflow Foundation\v3.5
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\2052_CHS_LP\x64
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\keypad
    C:\Program Files\Tanium\Tanium Server\plugins\console\InstallPlugin
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112831\resources
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Bin
    C:\Program Files\Microsoft SQL Server\110\DTS\ForEachEnumerators
    C:\Program Files\Tanium\Tanium Server\Apache24\conf
    C:\Program Files\MSBuild\Microsoft
    C:\Program Files\Microsoft SQL Server\110\DTS\UpgradeMappings
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\htdocs\php\Auth
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\style\css
    C:\Program Files\Common Files\Microsoft Shared\ink
    C:\Program Files\Common Files\Microsoft Shared\ink\sv-SE
    C:\Program Files\VMware\VMware Tools\messages
    C:\Program Files\Microsoft SQL Server\110\DTS\ForEachEnumerators\Resources
    C:\Program Files\Common Files\Microsoft Shared\ink\uk-UA
    C:\Program Files\Microsoft SQL Server\110\DTS\Binn\Resources\1033
    C:\Program Files\Tanium\Tanium Server\Apache24\manual\platform
    C:\Program Files\Microsoft SQL Server\110\KeyFile
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\3082
    C:\Program Files\Tanium\Tanium Server\CertificateBackup2014-09-16-20-44-23
    C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap\Release\x64\1033
    C:\Program Files\Microsoft.NET\ADOMD.NET
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1028_CHT_LP\x64\1028\help
    C:\Program Files\Common Files\Microsoft Shared\ink\sl-SI
    C:\Program Files\Tanium\Tanium Server\plugins\console\UserGroups
    C:\Program Files\Common Files\Microsoft Shared\ink\hu-HU
    C:\Program Files\Common Files\System\en-US
    C:\Program Files\Common Files\Microsoft Shared\ink\zh-TW
    C:\Program Files\Common Files\Microsoft Shared\ink\zh-CN
    C:\Program Files\Common Files\VMware\Drivers\video_wddm
    C:\Program Files\Common Files\Microsoft Shared\ink\fi-FI
    C:\Program Files\Common Files\Microsoft Shared
    C:\Program Files\Microsoft SQL Server\110\SDK\Include
    C:\Program Files\Common Files\Microsoft Shared\ink\da-DK
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\icons\small
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33
    C:\Program Files\Microsoft Visual Studio 10.0\Common7\IDE\PrivateAssemblies
    C:\Program Files\Microsoft SQL Server\80
    C:\Program Files\Microsoft SQL Server\90
    C:\Program Files\Windows Mail
    C:\Program Files\Common Files\VMware\Drivers\vmci\sockets\bin\win64
    C:\Program Files\Common Files\VMware\Drivers\vmci\sockets\bin\win32
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\oskmenu
    C:\Program Files\Microsoft SQL Server\110\DTS\LogProviders
    C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap\Release\Resources\1033
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1049_RUS_LP\x64\1049
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112604\Datastore_GlobalRules
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\images
    C:\Program Files\Microsoft SQL Server\110\SDK
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1036_FRA_LP\x64
    C:\Program Files\Windows NT\Accessories
    C:\Program Files\Tanium\Tanium Server\content_public_keys
    C:\Program Files\Windows NT\TableTextService\en-US
    C:\Program Files\Tanium\Tanium Server\plugins\console\Manifest
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\bin
    C:\Program Files\Tanium\Tanium Server\Apache24\logs
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1033_ENU_LP
    C:\Program Files\Tanium\Tanium Server\plugins\content
    C:\Program Files\Reference Assemblies\Microsoft\Framework
    C:\Program Files\Microsoft SQL Server\110\DTS\Connections\en
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\icons\small
    C:\Program Files\Common Files\VMware\Drivers\Virtual Printer\TPOG3\amd64
    C:\Program Files\Microsoft Visual Studio 10.0\Common7\IDE\PrivateAssemblies\1033
    C:\Program Files\Common Files\Microsoft Shared\ink\ko-KR
    C:\Program Files\Tanium\Tanium Server\Apache24\manual\ssl
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1042_KOR_LP\x64
    C:\Program Files\Tanium\Tanium Server\Apache24\manual\style\css
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\misc
    C:\Program Files\Microsoft SQL Server\110\SDK\Lib\x64
    C:\Program Files\Microsoft SQL Server\110\SDK\Lib\x86
    C:\Program Files\Tanium\Tanium Server\plugins\console\lib
    C:\Program Files\Common Files\Microsoft Shared\ink\it-IT
    C:\Program Files\Microsoft.NET
    C:\Program Files\Microsoft SQL Server\110\DTS\DataDumps
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\conf
    C:\Program Files\Internet Explorer\images
    C:\Program Files\Windows NT
    C:\Program Files\Microsoft SQL Server\110\COM\Resources\1033
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\JOBS
    C:\Program Files\Tanium\Tanium Server\Apache24\htdocs
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1041_JPN_LP
    C:\Program Files\Tanium\Tanium Server\php55\extras
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1031_DEU_LP\x64\1031\help
    C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap
    C:\Program Files\Common Files\SpeechEngines\Microsoft\TTS20
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23
    C:\Program Files\Common Files\Microsoft Shared\Triedit
    C:\Program Files\Microsoft.NET\ADOMD.NET\110
    C:\Program Files\Microsoft SQL Server\110\Shared
    C:\Program Files\Microsoft SQL Server\110\Tools\Binn
    C:\Program Files\Microsoft Help Viewer
    C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap\Release\x64\Patch
    C:\Program Files\Tanium\Tanium Server\Apache24\bin\iconv
    C:\Program Files\Common Files\VMware\Drivers\memctl
    C:\Program Files\Tanium\Tanium Server\plugins\console
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\conf\original
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\htdocs\php
    C:\Program Files\Microsoft SQL Server\90\License Terms
    C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap\Release\Resources
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\pt
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\ru
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\lib
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\it
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\ko
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\ja
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\es
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\de
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\fr
    C:\Program Files\Common Files\Microsoft Shared\ink\he-IL
    C:\Program Files\Common Files\Microsoft Shared\ink\ro-RO
    C:\Program Files\Common Files\VMware\Drivers\pvscsi
    C:\Program Files\Microsoft Visual Studio 10.0\Common7\Packages
    C:\Program Files\Microsoft Visual Studio 10.0\Common7
    C:\Program Files\Common Files\Services
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\oskpred
    C:\Program Files\Microsoft SQL Server\110\SDK\Lib
    C:\Program Files\Microsoft SQL Server\110\DTS\PipelineComponents\Resources\1033
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\misc
    C:\Program Files\Tanium\Tanium Server\Apache24\manual\misc
    C:\Program Files\Common Files\SpeechEngines\Microsoft\TTS20\en-US
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\modules
    C:\Program Files\Microsoft SQL Server\110\DTS\Connections
    C:\Program Files\Tanium\Tanium Server\Downloads\URLCache
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1046_PTB_LP
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\rewrite
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\images
    C:\Program Files\Common Files\VMware\Drivers\vmci\device
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\rewrite
    C:\Program Files\Common Files
    C:\Program Files\Tanium\Tanium Server\Apache24\manual
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\platform
    C:\Program Files\Tanium\Tanium Server\Apache24\conf\extra
    C:\Program Files\Common Files\VMware\Drivers\vmci
    C:\Program Files\Common Files\System\msadc\en-US
    C:\Program Files\Common Files\System
    C:\Program Files\Windows NT\Accessories\en-US
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1036_FRA_LP\x64\1036
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources
    C:\Program Files\Tanium\Tanium Server\plugins\console\RegistrySetting
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1046_PTB_LP\x64\1046
    C:\Program Files\Tanium\Tanium Server\Apache24\manual\rewrite
    C:\Program Files\VMware\VMware Tools
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\numbers
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1049_RUS_LP\x64
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Log
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\lib
    C:\Program Files\Windows NT\TableTextService
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1055
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1053
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1049
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1041
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1040
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1043
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1042
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1045
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1044
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1046
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1038
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1035
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1036
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1030
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1031
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1032
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1033
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1029
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\1028
    C:\Program Files\Tanium\Tanium Server\Apache24\htdocs\console
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1042_KOR_LP\x64\1042
    C:\Program Files\Tanium\Tanium Server\Apache24\error
    C:\Program Files\Common Files\Microsoft Shared\ink\nb-NO
    C:\Program Files\Tanium\Tanium Server\Apache24\manual\mod
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1041_JPN_LP\x64
    C:\Program Files\Common Files\Microsoft Shared\ink\lv-LV
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1033_ENU_LP\x64\1033
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\conf\original\extra
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\auxpad
    C:\Program Files\Common Files\Microsoft Shared\TextConv
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\developer
    C:\Program Files\Common Files\Microsoft Shared\MSInfo\en-US
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\3082_ESN_LP\x64\3082
    C:\Program Files\Common Files\Microsoft Shared\ink\nl-NL
    C:\Program Files\Tanium
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\howto
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\include
    C:\Program Files\Reference Assemblies\Microsoft\Framework\v3.5\RedistList
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112532\Datastore_LandingPage
    C:\Program Files\Microsoft SQL Server\100\KeyFile\1033
    C:\Program Files\Microsoft SQL Server\110\Tools\Binn\Resources\1033
    C:\Program Files\Tanium\Tanium Server\Downloads\Cache
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\style\latex
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\3082_ESN_LP
    C:\Program Files\Tanium\Tanium Server\php55\dev
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\bin\iconv
    C:\Program Files\VMware\VMware Tools\messages\zh_CN
    C:\Program Files\Tanium\Tanium Server\Apache24\manual\vhosts
    C:\Program Files\Common Files\VMware\Drivers\vmci\sockets
    C:\Program Files\Microsoft SQL Server\90\Shared\Resources\1033
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\conf
    C:\Program Files\Common Files\VMware
    C:\Program Files\Common Files\System\msadc
    C:\Program Files\Microsoft SQL Server\110\Tools
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\htdocs\php
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1040_ITA_LP
    C:\Program Files\Common Files\Microsoft Shared\ink\fr-FR
    C:\Program Files\Common Files\VMware\Drivers\vss
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\bin
    C:\Program Files\Common Files\Microsoft Shared\ink\tr-TR
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\programs
    C:\Program Files\Common Files\Microsoft Shared\VC
    C:\Program Files\Tanium\Tanium Server\php55\ext
    C:\Program Files\Common Files\Microsoft Shared\WF
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\ssl
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\htdocs
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\htdocs\console
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Templates
    C:\Program Files\Tanium\Tanium Server\plugins
    C:\Program Files\Tanium\Tanium Server\Apache24\icons\small
    C:\Program Files\Microsoft SQL Server\110\Shared\en
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\htdocs\php\Auth
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\error\include
    C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap\Release\x64\Help
    C:\Program Files\Microsoft Help Viewer\v1.0\Microsoft Help Viewer 1.1
    C:\Program Files\Microsoft SQL Server\110\Tools\Binn\ManagementStudio
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\symbols
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1036_FRA_LP\x64\1036\help
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual
    C:\Program Files\Common Files\System\Ole DB\en-US
    C:\Program Files\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\Extensions
    C:\Program Files\Microsoft SQL Server\80\Tools\Binn
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\2052_CHS_LP
    C:\Program Files\Common Files\Microsoft Shared\ink\lt-LT
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\htdocs
    C:\Program Files\Microsoft SQL Server\100\KeyFile
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\style
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Install
    C:\Program Files\Common Files\Microsoft Shared\ink\et-EE
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1028_CHT_LP
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1040_ITA_LP\x64\1040
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1028_CHT_LP\x64
    C:\Program Files\Common Files\VMware\Drivers\Virtual Printer\TPOGPS
    C:\Program Files\Common Files\Microsoft Shared\ink\cs-CZ
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\2052_CHS_LP\x64\2052\help
    C:\Program Files\VMware
    C:\Program Files\Microsoft SQL Server\110\Shared\VS2008
    C:\Program Files\Microsoft Visual Studio 10.0\Common7\Packages\Debugger
    C:\Program Files\Common Files\VMware\Drivers\mouse
    C:\Program Files\Common Files\VMware\Drivers\vmci\sockets\bin
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\bin\iconv
    C:\Program Files\Common Files\Microsoft Shared\ink\en-US
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Backup
    C:\Program Files\Tanium\Tanium Server\VB
    C:\Program Files\Microsoft SQL Server\110\DTS\ForEachEnumerators\Resources\1033
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\vhosts
    C:\Program Files\Common Files\Microsoft Shared\ink\bg-BG
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\ssl
    C:\Program Files\Tanium\Tanium Server\Apache24\bin
    C:\Program Files\Common Files\System\Ole DB
    C:\Program Files\Tanium\Tanium Server\Apache24\manual\faq
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS
    C:\Program Files\Common Files\VMware\Drivers\audio
    C:\Program Files\Microsoft SQL Server\110\DTS\Binn\Resources
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1041_JPN_LP\x64\1041
    C:\Program Files\Reference Assemblies\Microsoft\Framework\v3.0\RedistList
    C:\Program Files\Tanium\Tanium Server\Downloads
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1049_RUS_LP\x64\1049\help
    C:\Program Files\Microsoft Visual Studio 10.0\Common7\Packages\Debugger\x86
    C:\Program Files\Microsoft Visual Studio 10.0\Common7\Packages\Debugger\X64
    C:\Program Files\MSBuild\Microsoft\Windows Workflow Foundation
    C:\Program Files\Microsoft SQL Server\100\Shared
    C:\Program Files\Internet Explorer\SIGNUP
    C:\Program Files\Common Files\Microsoft Shared\ink\es-ES
    C:\Program Files\Tanium\Tanium Server\Support
    C:\Program Files\Microsoft SQL Server\110\DTS\Binn
    C:\Program Files\Common Files\Microsoft Shared\MSInfo
    C:\Program Files\Reference Assemblies
    C:\Program Files\Microsoft SQL Server\110\Shared\RsFxInstall
    C:\Program Files\Microsoft Help Viewer\v1.0\CatalogInfo
    C:\Program Files\Microsoft SQL Server\110\DTS\MappingFiles
    C:\Program Files\Microsoft SQL Server\110\DTS\PipelineComponents\Resources
    C:\Program Files\Common Files\Microsoft Shared\WF\amd64
    C:\Program Files\Tanium\Tanium Server\plugins\console\SigVerifier
    C:\Program Files\Tanium\Tanium Server\plugins\console\DashboardGroups
    C:\Program Files\Microsoft SQL Server\80\Tools
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Template Data
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\icons
    C:\Program Files\Common Files\Microsoft Shared\ink\de-DE
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1031_DEU_LP\x64\1031
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1042_KOR_LP
    C:\Program Files\Microsoft Visual Studio 10.0\Common7\IDE
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1033_ENU_LP\x64\1033\help
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\main
    C:\Program Files\Microsoft Help Viewer\v1.0\StopWords
    C:\Program Files\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\Extensions\Application
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\repldata
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\zh-CHT
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\zh-CHS
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\vhosts
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1042_KOR_LP\x64\1042\help
    C:\Program Files\Microsoft SQL Server\110\DTS\Tasks\en
    C:\Program Files\Common Files\SpeechEngines
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\logs
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\mod
    C:\Program Files\VMware\VMware Tools\Drivers\hgfs
    C:\Program Files\Tanium\Tanium Server\Apache24\conf\original
    C:\Program Files\Uninstall Information
    C:\Program Files\Reference Assemblies\Microsoft\Framework\v3.5
    C:\Program Files\Reference Assemblies\Microsoft\Framework\v3.0
    C:\Program Files\Microsoft Visual Studio 10.0\Common7\IDE\Xml
    C:\Program Files\Microsoft SQL Server\110\DTS\PipelineComponents
    C:\Program Files\Microsoft SQL Server\90\Shared\Resources
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1046_PTB_LP\x64\1046\help
    C:\Program Files\Tanium\Tanium Server\Apache24\include
    C:\Program Files\Tanium\Tanium Server\plugins\console\GroupFiliters
    C:\Program Files\VMware\VMware Tools\Drivers
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1041_JPN_LP\x64\1041\help
    C:\Program Files\Tanium\Tanium Server\Downloads\tmp
    C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap\Release
    C:\Program Files\Tanium\Tanium Server\Apache24\conf\original\extra
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\style\scripts
    C:\Program Files\Common Files\Microsoft Shared\ink\sr-Latn-CS
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\osknumpad
    C:\Program Files\Microsoft SQL Server\110\License Terms
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1031_DEU_LP\x64
    C:\Program Files\Common Files\VMware\Drivers\vmxnet
    C:\Program Files\Tanium\Tanium Server\Strings
    C:\Program Files\MSBuild
    C:\Program Files\Microsoft SQL Server\110\COM\Resources
    C:\Program Files\Common Files\VMware\Drivers\Virtual Printer\TPOGPS\amd64
    C:\Program Files\Microsoft SQL Server\80\COM
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\htdocs\console\history
    C:\Program Files\Tanium\Tanium Server\Apache24\manual\howto
    C:\Program Files\Microsoft SQL Server\110\Shared\Resources\1033
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\conf\extra
    C:\Program Files\Common Files\Microsoft Shared\MSEnv
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\2052_CHS_LP\x64\2052
    C:\Program Files\Common Files\VMware\Drivers\Virtual Printer
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\htdocs\console\history
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1028_CHT_LP\x64\1028
    C:\Program Files\Microsoft SQL Server\110\Shared\VS2008\1033
    C:\Program Files\Common Files\Microsoft Shared\ink\pt-BR
    C:\Program Files\Common Files\Microsoft Shared\ink\pt-PT
    C:\Program Files\Common Files\System\ado
    C:\Program Files\Microsoft SQL Server\110\KeyFile\1033
    C:\Program Files\Tanium\Tanium Server\SOAPUpload
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\2052
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112604\resources
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\DATA
    C:\Program Files\Tanium\Tanium Server\php55\extras\ssl
    C:\Program Files\Common Files\Microsoft Shared\ink\el-GR
    C:\Program Files\VMware\VMware Tools\win32
    C:\Program Files\VMware\VMware Tools\win64
    C:\Program Files\Microsoft SQL Server\110\Shared\Resources
    C:\Program Files\Internet Explorer
    C:\Program Files\Tanium\Tanium Server\Apache24\icons
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1033_ENU_LP\x64
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1031_DEU_LP
    C:\Program Files\Tanium\Tanium Server\Apache24\manual\programs
    C:\Program Files\Common Files\VMware\Drivers\vmxnet3
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1049_RUS_LP
    C:\Program Files\VMware\VMware Tools\Drivers\hgfs\wow64
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log
    C:\Program Files\Microsoft SQL Server\90\License Terms\1033
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\logs
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\faq
    C:\Program Files\Tanium\Tanium Server\Suppot_patch1
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\web
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\cgi-bin
    C:\Program Files\Tanium\Tanium Server\Apache24\manual\developer
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\1036
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\1033
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\1031
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\1028
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\1049
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\1046
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\1042
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\1041
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources\1040
    C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap\Release\x64
    C:\Program Files\Tanium\Tanium Server\Apache24\manual\style\latex
    C:\Program Files\Tanium\Tanium Server
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\htdocs\console
    C:\Program Files\Tanium\Tanium Server\http
    C:\Program Files\Common Files\Microsoft Shared\ink\ja-JP
    C:\Program Files\Microsoft SQL Server\110\DTS\Packages
    C:\Program Files\Common Files\Microsoft Shared\ink\sk-SK
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\style\css
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\conf\original
    C:\Program Files\Tanium\Tanium Server\Apache24\htdocs\php
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\howto
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\style\latex
    C:\Program Files\Common Files\Microsoft Shared\ink\hr-HR
    C:\Program Files\Common Files\VMware\Drivers
    C:\Program Files\Tanium\Tanium Server\Apache24\lib
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112532
    C:\Program Files\Microsoft Help Viewer\v1.0
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\conf\extra
    C:\Program Files\Tanium\Tanium Server\Apache24
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\style\scripts
    C:\Program Files\Common Files\Microsoft Shared\VGX
    C:\Program Files\Microsoft SQL Server\110\DTS\ProviderDescriptors
    C:\Program Files\Microsoft SQL Server\110\COM\en
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\faq
    C:\Program Files\Tanium\Tanium Server\Apache24\manual\style\scripts
    C:\Program Files\Common Files\Microsoft Shared\Triedit\en-US
    C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap\Release\x64\Help\1033
    C:\Program Files\Microsoft SQL Server\110\COM
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1046_PTB_LP\x64
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112831\Datastore_GlobalRules
    C:\Program Files\Common Files\Microsoft Shared\TextConv\en-US
    C:\Program Files\VMware\VMware Tools\plugins
    C:\Program Files\Microsoft SQL Server\110\DTS
    C:\Program Files\Tanium\Tanium Server\plugins\console\SavedQuestions
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\error\include
    C:\Program Files\Common Files\System\ado\en-US
    C:\Program Files\Tanium\Tanium Server\Apache24\cgi-bin
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112604
    C:\Program Files\VMware\VMware Tools\plugins\vmusr
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112831\Datastore
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\DllTmp64
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\DllTmp32
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\programs
    C:\Program Files\Microsoft SQL Server\110\Tools\Binn\Resources
    C:\Program Files\Tanium\Tanium Server\php55
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\manual\style
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1040_ITA_LP\x64
    C:\Program Files\Reference Assemblies\Microsoft
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\include
    C:\Program Files\Tanium\Tanium Server\Apache24\manual\images
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions
    C:\Program Files\Microsoft SQL Server\110\SDK\Assemblies\en
    C:\Program Files\Tanium\Tanium Server\Logs
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\mod
    C:\Program Files\Common Files\VMware\Drivers\Virtual Printer\TPOG3
    C:\Program Files\Microsoft SQL Server\110
    C:\Program Files\Microsoft SQL Server\100
    C:\Program Files\Tanium\Tanium Server\Apache24\modules
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\platform
    C:\Program Files\Microsoft Visual Studio 10.0
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\3082
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112831
    C:\Program Files\VMware\VMware Tools\plugins\common
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112804
    C:\Program Files\Common Files\Microsoft Shared\ink\th-TH
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\icons
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20140910_112831\Datastore_ComponentUpdate
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\error
    C:\Program Files\Microsoft SQL Server
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\error
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\3082_ESN_LP\x64
    C:\Program Files\Common Files\Microsoft Shared\SQL Debugging
    C:\Program Files\Tanium\Tanium Server\Apache24\error\include
    C:\Program Files\Microsoft SQL Server\110\SDK\Assemblies
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\Patch
    C:\Program Files\Microsoft Help Viewer\v1.0\en
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\3082_ESN_LP\x64\3082\help
    C:\Program Files\Microsoft SQL Server\90\Shared
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\2052
    C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\Binn\Resources\2070
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\conf\original\extra
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-11-17-11-17-33\manual\developer
    C:\Program Files\Common Files\Microsoft Shared\ink\pl-PL
    C:\Program Files\Common Files\SpeechEngines\Microsoft\TTS20\en-US\enu-dsk
    C:\Program Files\Common Files\Microsoft Shared\Stationery
    C:\Program Files\Common Files\Microsoft Shared\VS7Debug\1033
    C:\Program Files\Microsoft SQL Server\100\Setup Bootstrap\Bin
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\Resources
    C:\Program Files\Microsoft SQL Server\110\Shared\ErrorDumps
    C:\Program Files\Internet Explorer\en-US
    C:\Program Files\VMware\VMware Tools\messages\it
    C:\Program Files\VMware\VMware Tools\messages\ja
    C:\Program Files\VMware\VMware Tools\messages\ko
    C:\Program Files\VMware\VMware Tools\messages\de
    C:\Program Files\VMware\VMware Tools\messages\es
    C:\Program Files\VMware\VMware Tools\messages\fr
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1036_FRA_LP
    C:\Program Files\Microsoft SQL Server\110\DTS\Tasks","0.0.0.0
    0.0.0.0
    0.0.0.0
    172.16.31.2
    0.0.0.0","172.16.31.128
    fe80::5968:4e9d:b4fc:88ef","-
    -
    -
    -
    -","255.255.255.255
    255.255.255.0
    255.255.255.255
    0.0.0.0
    255.0.0.0","266
    266
    306
    266
    306"
    
