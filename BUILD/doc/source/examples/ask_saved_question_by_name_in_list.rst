
Ask saved question by name in list
====================================================================================================
Ask a saved question by referencing the name of a saved question in a list of strings.

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
    
    # setup the arguments for the handler method
    kwargs = {}
    kwargs["qtype"] = u'saved'
    kwargs["name"] = [u'Installed Applications']
    
    # call the handler with the ask method, passing in kwargs for arguments
    response = handler.ask(**kwargs)
    import pprint, io
    
    print ""
    print "Type of response: ", type(response)
    
    print ""
    print "Pretty print of response:"
    print pprint.pformat(response)
    
    print ""
    print "Equivalent Question if it were to be asked in the Tanium Console: "
    print response['question_object'].query_text
    
    # create an IO stream to store CSV results to
    out = io.BytesIO()
    
    # call the write_csv() method to convert response to CSV and store it in out
    response['question_results'].write_csv(out, response['question_results'])
    
    print ""
    print "CSV Results of response: "
    print out.getvalue()
    
    


Output from Python Code
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
    2014-12-07 01:02:22,054 INFO     question_progress: Results 149% (Get Installed Applications from all machines)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'question_object': <taniumpy.object_types.saved_question.SavedQuestion object at 0x10214fd50>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x1021691d0>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Installed Applications from all machines
    
    CSV Results of response: 
    Count,Name,Silent Uninstall String,Uninstallable,Version
    2,Google Search,nothing,Not Uninstallable,37.0.2062.120
    2,MakePDF,nothing,Not Uninstallable,10.0
    2,Wish,nothing,Not Uninstallable,8.5.9
    2,Time Machine,nothing,Not Uninstallable,1.3
    2,AppleGraphicsWarning,nothing,Not Uninstallable,2.3.0
    2,soagent,nothing,Not Uninstallable,7.0
    2,SpeechService,nothing,Not Uninstallable,5.2.6
    2,AinuIM,nothing,Not Uninstallable,1.0
    2,Pass Viewer,nothing,Not Uninstallable,1.0
    2,PressAndHold,nothing,Not Uninstallable,1.2
    2,PluginIM,nothing,Not Uninstallable,15
    2,UserNotificationCenter,nothing,Not Uninstallable,3.3.0
    1,Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.6161,MsiExec.exe /X{9BE518E6-ECC6-35A9-88E4-87755C07200F} /qn /noreboot,Is Uninstallable,9.0.30729.6161
    2,FaceTime,nothing,Not Uninstallable,3.0
    2,ScreenSaverEngine,nothing,Not Uninstallable,5.0
    2,LocationMenu,nothing,Not Uninstallable,1.0
    2,CoRD,nothing,Not Uninstallable,0.5.7
    2,asannotation2,nothing,Not Uninstallable,1308.22.2900.0
    2,Slack,nothing,Not Uninstallable,1.0.2
    1,Microsoft SQL Server 2008 R2 Management Objects,MsiExec.exe /X{83F2B8F4-5CF3-4BE9-9772-9543EAE4AC5F} /qn /noreboot,Is Uninstallable,10.51.2500.0
    2,Dashboard,nothing,Not Uninstallable,1.8
    2,Proof,nothing,Not Uninstallable,None
    1,Microsoft SQL Server System CLR Types,MsiExec.exe /X{C3F6F200-6D7B-4879-B9EE-700C0CE1FCDA} /qn /noreboot,Is Uninstallable,10.51.2500.0
    2,Extract,nothing,Not Uninstallable,None
    2,Speech Downloader,nothing,Not Uninstallable,5.0.25
    2,Disk Inventory X,nothing,Not Uninstallable,1.0
    1,Microsoft SQL Server 2012 (64-bit),"""c:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\SetupARP.exe""",Not Uninstallable,64-
    2,Switch Control,nothing,Not Uninstallable,2.0
    2,Python,nothing,Not Uninstallable,2.6.9
    2,System Information,nothing,Not Uninstallable,10.10
    2,Transmission,nothing,Not Uninstallable,2.84
    2,IDLE,nothing,Not Uninstallable,2.7.8
    2,CharacterPalette,nothing,Not Uninstallable,2.0.1
    2,System Events,nothing,Not Uninstallable,1.3.6
    2,MRTAgent,nothing,Not Uninstallable,1.1
    2,MiniTerm,nothing,Not Uninstallable,1.9
    2,My Day,nothing,Not Uninstallable,14.4.6
    2,Reminders,nothing,Not Uninstallable,3.0
    2,Wireless Diagnostics,nothing,Not Uninstallable,4.0
    2,Gmail,nothing,Not Uninstallable,37.0.2062.120
    2,Digital Color Meter,nothing,Not Uninstallable,5.10
    2,Dictation,nothing,Not Uninstallable,1.4.55
    2,Tunnelblick,nothing,Not Uninstallable,3.4.0 (build 4007)
    2,Memory Clean,nothing,Not Uninstallable,4.7
    2,Screen Sharing,nothing,Not Uninstallable,1.6
    2,Keychain Circle Notification,nothing,Not Uninstallable,1.0
    1,Microsoft Visual C++ 2012 Redistributable (x86) - 11.0.61030,"""C:\ProgramData\Package Cache\{33d1fd90-4274-48a1-9bc1-97e33d9c2d6f}\vcredist_x86.exe""  /uninstall",Not Uninstallable,11.0.61030.0
    2,ManagedClient,nothing,Not Uninstallable,7.0
    2,Image Capture,nothing,Not Uninstallable,6.6
    2,VoiceOver Quickstart,nothing,Not Uninstallable,7.0
    2,Stickies,nothing,Not Uninstallable,10.0
    2,TamilIM,nothing,Not Uninstallable,1.6
    2,AddressBookManager,nothing,Not Uninstallable,9.0
    2,NetAuthAgent,nothing,Not Uninstallable,5.0
    2,Directory Utility,nothing,Not Uninstallable,5.0
    2,VietnameseIM,nothing,Not Uninstallable,1.4
    2,Aperture,nothing,Not Uninstallable,3.6
    2,Automator Runner,nothing,Not Uninstallable,2.5
    2,Image Capture Extension,nothing,Not Uninstallable,10.0
    2,EPSON Scanner,nothing,Not Uninstallable,5.7.6
    2,TextMate,nothing,Not Uninstallable,2.0-beta.6.4
    2,OBEXAgent,nothing,Not Uninstallable,4.3.1
    2,Microsoft Chart Converter,nothing,Not Uninstallable,14.4.6
    2,Widget Simulator,nothing,Not Uninstallable,1.0
    2,Firefox,nothing,Not Uninstallable,33.1.1
    2,VoiceOver Utility,nothing,Not Uninstallable,7.0
    2,Skype,nothing,Not Uninstallable,6.19
    1,Microsoft Visual C++ 2010  x86 Runtime - 10.0.40219,MsiExec.exe /X{5D9ED403-94DE-3BA0-B1D6-71F4BDA412E6} /qn /noreboot,Is Uninstallable,10.0.40219
    2,Office365Service,nothing,Not Uninstallable,14.4.6
    2,50onPaletteServer,nothing,Not Uninstallable,1.1.0
    2,Grab,nothing,Not Uninstallable,1.8
    2,Network Setup Assistant,nothing,Not Uninstallable,10.8.0
    2,AOSAlertManager,nothing,Not Uninstallable,1.06
    2,Java Mission Control,nothing,Not Uninstallable,5.4.0
    2,AppleMobileDeviceHelper,nothing,Not Uninstallable,5.0
    2,Sublime Text,nothing,Not Uninstallable,Build 3065
    2,Notes,nothing,Not Uninstallable,3.1
    2,AOSHeartbeat,nothing,Not Uninstallable,1.06
    1,Microsoft SQL Server 2012 Setup (English),MsiExec.exe /X{8CB0713F-CFE0-445D-BCB2-538465860E1A} /qn /noreboot,Is Uninstallable,11.1.3128.0
    2,Google Chrome,nothing,Not Uninstallable,39.0.2171.71
    2,universalAccessAuthWarn,nothing,Not Uninstallable,1.0
    1,Microsoft SQL Server 2012 Native Client ,MsiExec.exe /X{49D665A2-4C2A-476E-9AB8-FCC425F526FC} /qn /noreboot,Is Uninstallable,11.0.2100.60
    2,DatabaseProcess,nothing,Not Uninstallable,10600
    2,DiskImages UI Agent,nothing,Not Uninstallable,10.10
    2,Spotify,nothing,Not Uninstallable,0.9.14.13.gba5645ad
    2,Keychain Access,nothing,Not Uninstallable,9.0
    2,loginwindow,nothing,Not Uninstallable,9.0
    2,ReportPanic,nothing,Not Uninstallable,10.10
    2,Install OS X Mavericks,nothing,Not Uninstallable,1.3.44
    2,Spotlight,nothing,Not Uninstallable,3.0
    2,Python Launcher,nothing,Not Uninstallable,2.7.8
    2,Chess,nothing,Not Uninstallable,3.10
    2,LaterAgent,nothing,Not Uninstallable,1.0
    2,SpeechRecognitionServer,nothing,Not Uninstallable,5.0.25
    2,App Store,nothing,Not Uninstallable,2.0
    2,CoreServicesUIAgent,nothing,Not Uninstallable,134.6
    2,Build Web Page,nothing,Not Uninstallable,10.0
    1,Google Chrome,"""C:\Program Files (x86)\Google\Chrome\Application\39.0.2171.71\Installer\setup.exe"" --uninstall --multi-install --chrome --system-level",Not Uninstallable,39.0.2171.71
    2,Microsoft Outlook,nothing,Not Uninstallable,14.4.6
    2,Yap,nothing,Not Uninstallable,None
    2,Dropbox,nothing,Not Uninstallable,2.10.29
    2,Microsoft Excel,nothing,Not Uninstallable,14.4.6
    2,GarageBand,nothing,Not Uninstallable,10.0.3
    2,Microsoft Upload Center,nothing,Not Uninstallable,14.4.6
    2,Google Docs,nothing,Not Uninstallable,37.0.2062.120
    2,Numbers,nothing,Not Uninstallable,3.5
    2,iTerm,nothing,Not Uninstallable,2.0.0.20141103
    2,Solver,nothing,Not Uninstallable,1.0
    2,Certificate Assistant,nothing,Not Uninstallable,5.0
    2,Python,nothing,Not Uninstallable,2.7.8
    2,Photo Booth,nothing,Not Uninstallable,7.0
    2,Microsoft Clip Gallery,nothing,Not Uninstallable,14.4.6
    1,Microsoft Help Viewer 1.1,c:\Program Files\Microsoft Help Viewer\v1.0\Microsoft Help Viewer 1.1\install.exe,Not Uninstallable,1.1.40219
    2,SyncServer,nothing,Not Uninstallable,8.1
    1,Microsoft Visual Studio 2010 Shell (Isolated) - ENU,MsiExec.exe /X{D64B6984-242F-32BC-B008-752806E5FC44} /qn /noreboot,Is Uninstallable,10.0.40219
    2,Rename,nothing,Not Uninstallable,None
    2,League of Legends,nothing,Not Uninstallable,1.0
    2,Dictionary,nothing,Not Uninstallable,2.2.1
    2,FileSyncAgent,nothing,Not Uninstallable,8.1
    1,Microsoft SQL Server 2008 Setup Support Files ,MsiExec.exe /X{B40EE88B-400A-4266-A17B-E3DE64E94431} /qn /noreboot,Is Uninstallable,10.1.2731.0
    2,PluginProcess,nothing,Not Uninstallable,10600
    2,RegisterPluginIMApp,nothing,Not Uninstallable,15
    2,Microsoft Document Connection,nothing,Not Uninstallable,14.4.6
    2,AutoImporter,nothing,Not Uninstallable,6.6
    1,Microsoft Report Viewer 2012 Runtime,MsiExec.exe /X{9CCE40CE-A9E6-4916-8729-B008558EEF3F} /qn /noreboot,Is Uninstallable,11.0.2100.60
    2,DiskImageMounter,nothing,Not Uninstallable,10.10
    2,Adobe Photoshop Lightroom 5,nothing,Not Uninstallable,Adobe Photoshop Lightroom 5.6 [974614]
    2,Instruments,nothing,Not Uninstallable,6.1
    2,check_afp,nothing,Not Uninstallable,4.0
    2,Console,nothing,Not Uninstallable,10.10
    2,Network Diagnostics,nothing,Not Uninstallable,1.3
    2,Free42-Decimal,nothing,Not Uninstallable,None
    2,Java Web Start,nothing,Not Uninstallable,15.0.0
    2,Conflict Resolver,nothing,Not Uninstallable,8.1
    2,Audio MIDI Setup,nothing,Not Uninstallable,3.0.6
    2,Bluetooth Setup Assistant,nothing,Not Uninstallable,4.3.1
    2,UnRarX,nothing,Not Uninstallable,Version 2.2
    2,X11,nothing,Not Uninstallable,1.0.1
    2,AddressBookUrlForwarder,nothing,Not Uninstallable,9.0
    2,Set Info,nothing,Not Uninstallable,None
    2,Migration Assistant,nothing,Not Uninstallable,5
    2,Git Gui,nothing,Not Uninstallable,0.19.0.2.g3decb8e
    2,Safari,nothing,Not Uninstallable,8.0
    2,Disk Utility,nothing,Not Uninstallable,13
    2,iBooks,nothing,Not Uninstallable,1.1
    2,Photosmart 7510 series,nothing,Not Uninstallable,10.0
    2,VLC,nothing,Not Uninstallable,2.1.5
    2,Open XML for Excel,nothing,Not Uninstallable,14.4.6
    2,Terminal,nothing,Not Uninstallable,2.5
    2,IDSRemoteURLConnectionAgent,nothing,Not Uninstallable,10.0
    2,AppleScript Utility,nothing,Not Uninstallable,1.1.2
    2,VMware Fusion,nothing,Not Uninstallable,7.1.0
    2,identityservicesd,nothing,Not Uninstallable,10.0
    2,GitHub Conduit,nothing,Not Uninstallable,1.0
    2,Install in Progress,nothing,Not Uninstallable,3.0
    2,Summary Service,nothing,Not Uninstallable,2.0
    2,Google Drive,nothing,Not Uninstallable,1.18
    2,ARDAgent,nothing,Not Uninstallable,3.8
    2,ParentalControls,nothing,Not Uninstallable,4.1
    2,Automator,nothing,Not Uninstallable,2.5
    2,SCIM,nothing,Not Uninstallable,102
    2,TextEdit,nothing,Not Uninstallable,1.10
    2,SystemUIServer,nothing,Not Uninstallable,1.7
    2,SocialPushAgent,nothing,Not Uninstallable,25
    2,Family,nothing,Not Uninstallable,1.0
    2,GlobalProtect,nothing,Not Uninstallable,2.1.0-50
    2,SourceTree,nothing,Not Uninstallable,2.0.2
    2,ABAssistantService,nothing,Not Uninstallable,9.0
    2,AskPermissionUI,nothing,Not Uninstallable,1.0
    2,Microsoft Office Reminders,nothing,Not Uninstallable,14.4.6
    2,Dock,nothing,Not Uninstallable,1.8
    2,Python,nothing,Not Uninstallable,2.7.6
    2,Microsoft Error Reporting,nothing,Not Uninstallable,2.2.9
    2,iTerm,nothing,Not Uninstallable,None
    1,Microsoft Visual C++ 2010  x86 Redistributable - 10.0.40219,MsiExec.exe /X{F0C3E5D1-1ADE-321E-8167-68EF0DE699A5} /qn /noreboot,Is Uninstallable,10.0.40219
    1,Tanium Server 6.2.314.3258,C:\Program Files\Tanium\Tanium Server\uninst.exe,Not Uninstallable,6.2.314.3258
    2,MassStorageCamera,nothing,Not Uninstallable,10.0
    1,Python 2.7.8 (64-bit),MsiExec.exe /X{61121B12-88BD-4261-A6EE-AB32610A56DE} /qn /noreboot,Is Uninstallable,2.7.8150
    2,eaptlstrust,nothing,Not Uninstallable,13.0
    2,Mail,nothing,Not Uninstallable,8.1
    2,PTPCamera,nothing,Not Uninstallable,10.0
    1,Visual Studio 2010 Prerequisites - English,MsiExec.exe /X{662014D2-0450-37ED-ABAE-157C88127BEB} /qn /noreboot,Is Uninstallable,10.0.40219
    2,Expansion Slot Utility,nothing,Not Uninstallable,1.5.1
    2,Wish,nothing,Not Uninstallable,8.4.19
    2,quicklookd32,nothing,Not Uninstallable,5.0
    2,VoiceOver,nothing,Not Uninstallable,7.0
    2,Application Loader,nothing,Not Uninstallable,3.0
    2,Microsoft PowerPoint,nothing,Not Uninstallable,14.4.6
    2,CIMFindInputCodeTool,nothing,Not Uninstallable,102
    2,rcd,nothing,Not Uninstallable,327.5
    2,AirScanScanner,nothing,Not Uninstallable,10.0
    1,Microsoft Visual C++ 2012 Redistributable (x64) - 11.0.61030,"""C:\ProgramData\Package Cache\{ca67548a-5ebe-413a-b50c-4b9ceb6d66c6}\vcredist_x64.exe""  /uninstall",Not Uninstallable,11.0.61030.0
    2,Xcode,nothing,Not Uninstallable,6.1.1
    2,WebKitPluginHost,nothing,Not Uninstallable,10600
    2,iCloud Photos,nothing,Not Uninstallable,2.7
    2,Microsoft Graph,nothing,Not Uninstallable,14.4.6
    2,Calculator,nothing,Not Uninstallable,10.8
    2,Notification Center,nothing,Not Uninstallable,1.0
    2,Getty Images Stream,nothing,Not Uninstallable,1.0.0
    2,FontRegistryUIAgent,nothing,Not Uninstallable,81.0
    2,NetworkProcess,nothing,Not Uninstallable,10600
    2,Boot Camp Assistant,nothing,Not Uninstallable,5.1.2
    2,Install Command Line Developer Tools,nothing,Not Uninstallable,1.0
    2,Display Calibrator,nothing,Not Uninstallable,4.10.0
    2,Feedback Assistant,nothing,Not Uninstallable,4.1.1
    2,System Preferences,nothing,Not Uninstallable,14.0
    2,ScriptMonitor,nothing,Not Uninstallable,1.0
    2,AddressBookSourceSync,nothing,Not Uninstallable,9.0
    2,Keynote,nothing,Not Uninstallable,6.5
    2,Jar Launcher,nothing,Not Uninstallable,15.0.0
    2,Captive Network Assistant,nothing,Not Uninstallable,3.0
    2,Type5Camera,nothing,Not Uninstallable,10.0
    2,Language Chooser,nothing,Not Uninstallable,1.0
    2,InkServer,nothing,Not Uninstallable,10.9
    2,System Image Utility,nothing,Not Uninstallable,10.10
    2,ZoomWindow,nothing,Not Uninstallable,2.0
    2,Cyberduck,nothing,Not Uninstallable,4.5.2
    2,Bluetooth File Exchange,nothing,Not Uninstallable,4.3.1
    2,Quicksilver,nothing,Not Uninstallable,1.2.1
    2,iPhoto,nothing,Not Uninstallable,9.6
    2,Microsoft Remote Desktop,nothing,Not Uninstallable,8.0.25189
    2,CoreLocationAgent,nothing,Not Uninstallable,1486.12
    2,KeyboardViewer,nothing,Not Uninstallable,3.2
    2,TrackpadIM,nothing,Not Uninstallable,1.5
    2,Mission Control,nothing,Not Uninstallable,1.2
    2,EscrowSecurityAlert,nothing,Not Uninstallable,1.0
    2,Adobe Flash Player Install Manager,nothing,Not Uninstallable,15.0.0.239
    2,Recursive File Processing Droplet,nothing,Not Uninstallable,1.0
    2,Launchpad,nothing,Not Uninstallable,1.0
    2,Folder Actions Dispatcher,nothing,Not Uninstallable,1.0.4
    2,Type8Camera,nothing,Not Uninstallable,10.0
    2,DVD Player,nothing,Not Uninstallable,5.7
    2,AirPort Base Station Agent,nothing,Not Uninstallable,2.2.1
    2,Microsoft Alerts Daemon,nothing,Not Uninstallable,14.4.6
    1,Microsoft SQL Server 2012 Transact-SQL ScriptDom ,MsiExec.exe /X{0E8670B8-3965-4930-ADA6-570348B67153} /qn /noreboot,Is Uninstallable,11.0.2100.60
    2,Canon IJScanner2,nothing,Not Uninstallable,3.1.0
    2,SpeechSynthesisServer,nothing,Not Uninstallable,5.2.6
    2,Cisco WebEx Start,nothing,Not Uninstallable,0.4.6
    2,Equation Editor,nothing,Not Uninstallable,14.2.0
    2,Accessibility Inspector,nothing,Not Uninstallable,4.1
    2,Grapher,nothing,Not Uninstallable,2.5
    2,RAID Utility,nothing,Not Uninstallable,4.0
    2,HelpViewer,nothing,Not Uninstallable,5.2
    2,UniversalAccessControl,nothing,Not Uninstallable,7.0
    2,iTunes,nothing,Not Uninstallable,12.0.1
    2,FindReaperFiles,nothing,Not Uninstallable,802
    2,storeuid,nothing,Not Uninstallable,1.0
    2,AppDownloadLauncher,nothing,Not Uninstallable,1.0
    1,Microsoft VSS Writer for SQL Server 2012,MsiExec.exe /X{3E0DD83F-BE4C-4478-86A0-AD0D79D1353E} /qn /noreboot,Is Uninstallable,11.0.2100.60
    2,imagent,nothing,Not Uninstallable,10.0
    2,QuickLookUIHelper,nothing,Not Uninstallable,5.0
    2,Contacts,nothing,Not Uninstallable,9.0
    2,iMovie,nothing,Not Uninstallable,10.0.6
    2,Setup Assistant,nothing,Not Uninstallable,10.10
    2,YouTube,nothing,Not Uninstallable,37.0.2062.120
    2,Folder Actions Setup,nothing,Not Uninstallable,1.1.6
    1,Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.4974,MsiExec.exe /X{B7E38540-E355-3503-AFD7-635B2F2F76E1} /qn /noreboot,Is Uninstallable,9.0.30729.4974
    2,Microsoft Language Register,nothing,Not Uninstallable,14.4.6
    1,SQL Server Browser for SQL Server 2012,MsiExec.exe /X{4B9E6EB0-0EED-4E74-9479-F982C3254F71} /qn /noreboot,Is Uninstallable,11.0.2100.60
    2,Activity Monitor,nothing,Not Uninstallable,10.10.0
    2,ImageCaptureService,nothing,Not Uninstallable,6.6
    2,atmsupload,nothing,Not Uninstallable,1408.13.2909.0
    2,GitHub,nothing,Not Uninstallable,Medium Hefson
    2,Network Utility,nothing,Not Uninstallable,1.8
    2,AirPlayUIAgent,nothing,Not Uninstallable,2.0
    2,convertpdf,nothing,Not Uninstallable,1.2
    2,Match,nothing,Not Uninstallable,None
    1,Tanium Client Deployment Tool,"""C:\Program Files (x86)\Tanium\Tanium Client Deployment Tool\uninstall.exe""",Not Uninstallable,4.0.0.0
    2,Font Book,nothing,Not Uninstallable,5.0
    2,AOSPushRelay,nothing,Not Uninstallable,1.06
    2,KoreanIM,nothing,Not Uninstallable,6.4
    1,Adobe Flash Player 15 ActiveX,C:\Windows\SysWOW64\Macromed\Flash\FlashUtil32_15_0_0_239_ActiveX.exe -maintain activex,Not Uninstallable,15.0.0.239
    2,SecurityFixer,nothing,Not Uninstallable,10.8
    2,BluetoothUIServer,nothing,Not Uninstallable,4.3.1
    2,Free42-Binary,nothing,Not Uninstallable,None
    1,Microsoft .NET Framework 4 Multi-Targeting Pack,MsiExec.exe /X{CFEF48A8-BFB8-3EAC-8BA5-DE4F8AA267CE} /qn /noreboot,Is Uninstallable,4.0.30319
    2,Show Info,nothing,Not Uninstallable,None
    2,Ticket Viewer,nothing,Not Uninstallable,4.0
    2,AppleMobileSync,nothing,Not Uninstallable,5.0
    2,ODSAgent,nothing,Not Uninstallable,1.8
    1,Microsoft Visual C++ 2010  x64 Redistributable - 10.0.40219,MsiExec.exe /X{1D8E6291-B0D5-35EC-8441-6616F567A0F7} /qn /noreboot,Is Uninstallable,10.0.40219
    2,Droplet with Settable Properties,nothing,Not Uninstallable,1.0
    2,Remove,nothing,Not Uninstallable,None
    2,Cocoa-AppleScript Applet,nothing,Not Uninstallable,1.0
    2,Image Events,nothing,Not Uninstallable,1.1.6
    2,PrinterProxy,nothing,Not Uninstallable,10.0
    2,AirPort Utility,nothing,Not Uninstallable,6.3.4
    2,Archive Utility,nothing,Not Uninstallable,10.10
    2,Database Events,nothing,Not Uninstallable,1.0.6
    2,ChineseTextConverterService,nothing,Not Uninstallable,2.1
    2,Installer,nothing,Not Uninstallable,6.1.0
    2,JapaneseIM,nothing,Not Uninstallable,5.0
    2,Calibration Assistant,nothing,Not Uninstallable,1.0
    2,Maps,nothing,Not Uninstallable,2.0
    2,Microsoft Office Setup Assistant,nothing,Not Uninstallable,14.4.1
    2,PyCharm CE,nothing,Not Uninstallable,3.4.1
    2,Game Center,nothing,Not Uninstallable,2.0
    2,Embed,nothing,Not Uninstallable,None
    2,Spotlight,nothing,Not Uninstallable,1.0
    2,VirtualScanner,nothing,Not Uninstallable,4.0
    1,Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.6161,MsiExec.exe /X{5FCE6D76-F5DC-37AB-B2B8-22AB8CEDB1D4} /qn /noreboot,Is Uninstallable,9.0.30729.6161
    2,FileMerge,nothing,Not Uninstallable,2.8
    2,Software Update,nothing,Not Uninstallable,6
    2,Microsoft AutoUpdate,nothing,Not Uninstallable,2.3.6
    2,UnmountAssistantAgent,nothing,Not Uninstallable,5.0
    1,Microsoft .NET Framework 4.5.1,C:\Windows\Microsoft.NET\Framework64\v4.0.30319\SetupCache\v4.5.50938\\Setup.exe /repair /x86 /x64,Not Uninstallable,4.5.50938
    2,Messages,nothing,Not Uninstallable,8.0
    2,Microsoft Database Utility,nothing,Not Uninstallable,14.4.6
    2,TCIM,nothing,Not Uninstallable,102
    2,iCloudUserNotificationsd,nothing,Not Uninstallable,1.0
    1,VMware Tools,MsiExec.exe /X{8CF7A691-09D2-4659-8C84-0406A7B58AE7} /qn /noreboot,Is Uninstallable,9.8.4.2202052
    2,quicklookd,nothing,Not Uninstallable,5.0
    2,CalendarFileHandler,nothing,Not Uninstallable,8.0
    2,Problem Reporter,nothing,Not Uninstallable,10.10
    2,Recursive Image File Processing Droplet,nothing,Not Uninstallable,1.0
    2,Google Drive,nothing,Not Uninstallable,37.0.2062.120
    2,CMFSyncAgent,nothing,Not Uninstallable,10.0
    2,Microsoft Ship Asserts,nothing,Not Uninstallable,1.1.4
    1,Microsoft SQL Server 2012 Transact-SQL Compiler Service ,MsiExec.exe /X{BEB0F91E-F2EA-48A1-B938-7857ABF2A93D} /qn /noreboot,Is Uninstallable,11.0.2100.60
    2,syncuid,nothing,Not Uninstallable,8.1
    2,AddressBookSync,nothing,Not Uninstallable,9.0
    2,Memory Slot Utility,nothing,Not Uninstallable,1.5.1
    2,AddPrinter,nothing,Not Uninstallable,10.0
    2,SyncServicesAgent,nothing,Not Uninstallable,14.4.6
    2,IMServicePlugInAgent,nothing,Not Uninstallable,10.0
    2,Microsoft Query,nothing,Not Uninstallable,12.0.0
    2,Script Editor,nothing,Not Uninstallable,2.7
    2,AppleFileServer,nothing,Not Uninstallable,2.0
    2,ColorSync Utility,nothing,Not Uninstallable,4.10.0
    1,Microsoft System CLR Types for SQL Server 2012 (x64),MsiExec.exe /X{F1949145-EB64-4DE7-9D81-E6D27937146C} /qn /noreboot,Is Uninstallable,11.0.2100.60
    1,Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.4148,MsiExec.exe /X{1F1C2DFC-2D24-3E06-BCB8-725134ADF989} /qn /noreboot,Is Uninstallable,9.0.30729.4148
    2,Finder,nothing,Not Uninstallable,10.10.1
    1,Tanium Client 6.0.314.1190,C:\Program Files (x86)\Tanium\Tanium Client\uninst.exe,Not Uninstallable,6.0.314.1190
    2,MemoryCleanHelper,nothing,Not Uninstallable,1.0
    2,Microsoft Word,nothing,Not Uninstallable,14.4.6
    2,Type4Camera,nothing,Not Uninstallable,10.0
    2,Pages,nothing,Not Uninstallable,5.5.1
    2,Canon IJScanner4,nothing,Not Uninstallable,3.1.0
    2,Microsoft Database Daemon,nothing,Not Uninstallable,14.4.6
    2,WebProcess,nothing,Not Uninstallable,10600
    2,ScreenReaderUIServer,nothing,Not Uninstallable,7.0
    2,PubSubAgent,nothing,Not Uninstallable,1.0.5
    2,FindMyMacMessenger,nothing,Not Uninstallable,4.1
    2,Cisco WebEx Meeting Center,nothing,Not Uninstallable,1410.10.2910.1
    2,File Sync,nothing,Not Uninstallable,8.1
    2,Preview,nothing,Not Uninstallable,8.0
    2,Soundflowerbed,nothing,Not Uninstallable,1.0
    2,Network Recording Player,nothing,Not Uninstallable,2.2.0
    2,prezi,nothing,Not Uninstallable,r846
    2,QuickTime Player,nothing,Not Uninstallable,10.4
    2,KeyboardSetupAssistant,nothing,Not Uninstallable,10.7
    2,nbagent,nothing,Not Uninstallable,1.0
    2,Wi-Fi,nothing,Not Uninstallable,1.0
    
