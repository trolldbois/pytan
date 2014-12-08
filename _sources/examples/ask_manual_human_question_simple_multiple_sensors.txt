
Ask manual human question simple multiple sensors
====================================================================================================
Ask a manual question using human strings by referencing the name of multiple sensors in a list.

No sensor filters, sensor parameters, sensor filter options, question filters, or question options supplied.

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
    kwargs["sensors"] = [u'Computer Name', u'Installed Applications']
    kwargs["qtype"] = u'manual_human'
    
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
    2014-12-07 01:02:27,503 INFO     question_progress: Results 0% (Get Computer Name and Installed Applications from all machines)
    2014-12-07 01:02:32,523 INFO     question_progress: Results 0% (Get Computer Name and Installed Applications from all machines)
    2014-12-07 01:02:37,543 INFO     question_progress: Results 100% (Get Computer Name and Installed Applications from all machines)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'question_object': <taniumpy.object_types.question.Question object at 0x10214fb50>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10204fe50>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Computer Name and Installed Applications from all machines
    
    CSV Results of response: 
    Computer Name,Name,Silent Uninstall String,Uninstallable,Version
    Casus-Belli.local,"Google Search
    MakePDF
    Wish
    Time Machine
    AppleGraphicsWarning
    soagent
    SpeechService
    AinuIM
    Pass Viewer
    PressAndHold
    PluginIM
    UserNotificationCenter
    FaceTime
    ScreenSaverEngine
    LocationMenu
    CoRD
    asannotation2
    Slack
    Dashboard
    Proof
    Extract
    Speech Downloader
    Disk Inventory X
    Switch Control
    Python
    System Information
    Transmission
    IDLE
    CharacterPalette
    System Events
    MRTAgent
    MiniTerm
    My Day
    Reminders
    Wireless Diagnostics
    Gmail
    Digital Color Meter
    Dictation
    Tunnelblick
    Memory Clean
    Screen Sharing
    Keychain Circle Notification
    ManagedClient
    Image Capture
    VoiceOver Quickstart
    Stickies
    TamilIM
    AddressBookManager
    NetAuthAgent
    Directory Utility
    VietnameseIM
    Aperture
    Automator Runner
    Image Capture Extension
    EPSON Scanner
    TextMate
    OBEXAgent
    Microsoft Chart Converter
    Widget Simulator
    Firefox
    VoiceOver Utility
    Skype
    Office365Service
    50onPaletteServer
    Grab
    Network Setup Assistant
    AOSAlertManager
    Java Mission Control
    AppleMobileDeviceHelper
    Sublime Text
    Notes
    AOSHeartbeat
    Google Chrome
    universalAccessAuthWarn
    DatabaseProcess
    DiskImages UI Agent
    Spotify
    Keychain Access
    loginwindow
    ReportPanic
    Install OS X Mavericks
    Spotlight
    Python Launcher
    Chess
    LaterAgent
    SpeechRecognitionServer
    App Store
    CoreServicesUIAgent
    Build Web Page
    Microsoft Outlook
    Yap
    Dropbox
    Microsoft Excel
    GarageBand
    Microsoft Upload Center
    Google Docs
    Numbers
    iTerm
    Solver
    Certificate Assistant
    Python
    Photo Booth
    Microsoft Clip Gallery
    SyncServer
    Rename
    League of Legends
    Dictionary
    FileSyncAgent
    PluginProcess
    RegisterPluginIMApp
    Microsoft Document Connection
    AutoImporter
    DiskImageMounter
    Adobe Photoshop Lightroom 5
    Instruments
    check_afp
    Console
    Network Diagnostics
    Free42-Decimal
    Java Web Start
    Conflict Resolver
    Audio MIDI Setup
    Bluetooth Setup Assistant
    UnRarX
    X11
    AddressBookUrlForwarder
    Set Info
    Migration Assistant
    Git Gui
    Safari
    Disk Utility
    iBooks
    Photosmart 7510 series
    VLC
    Open XML for Excel
    Terminal
    IDSRemoteURLConnectionAgent
    AppleScript Utility
    VMware Fusion
    identityservicesd
    GitHub Conduit
    Install in Progress
    Summary Service
    Google Drive
    ARDAgent
    ParentalControls
    Automator
    SCIM
    TextEdit
    SystemUIServer
    SocialPushAgent
    Family
    GlobalProtect
    SourceTree
    ABAssistantService
    AskPermissionUI
    Microsoft Office Reminders
    Dock
    Python
    Microsoft Error Reporting
    iTerm
    MassStorageCamera
    eaptlstrust
    Mail
    PTPCamera
    Expansion Slot Utility
    Wish
    quicklookd32
    VoiceOver
    Application Loader
    Microsoft PowerPoint
    CIMFindInputCodeTool
    rcd
    AirScanScanner
    Xcode
    WebKitPluginHost
    iCloud Photos
    Microsoft Graph
    Calculator
    Notification Center
    Getty Images Stream
    FontRegistryUIAgent
    NetworkProcess
    Boot Camp Assistant
    Install Command Line Developer Tools
    Display Calibrator
    Feedback Assistant
    System Preferences
    ScriptMonitor
    AddressBookSourceSync
    Keynote
    Jar Launcher
    Captive Network Assistant
    Type5Camera
    Language Chooser
    InkServer
    System Image Utility
    ZoomWindow
    Cyberduck
    Bluetooth File Exchange
    Quicksilver
    iPhoto
    Microsoft Remote Desktop
    CoreLocationAgent
    KeyboardViewer
    TrackpadIM
    Mission Control
    EscrowSecurityAlert
    Adobe Flash Player Install Manager
    Recursive File Processing Droplet
    Launchpad
    Folder Actions Dispatcher
    Type8Camera
    DVD Player
    AirPort Base Station Agent
    Microsoft Alerts Daemon
    Canon IJScanner2
    SpeechSynthesisServer
    Cisco WebEx Start
    Equation Editor
    Accessibility Inspector
    Grapher
    RAID Utility
    HelpViewer
    UniversalAccessControl
    iTunes
    FindReaperFiles
    storeuid
    AppDownloadLauncher
    imagent
    QuickLookUIHelper
    Contacts
    iMovie
    Setup Assistant
    YouTube
    Folder Actions Setup
    Microsoft Language Register
    Activity Monitor
    ImageCaptureService
    atmsupload
    GitHub
    Network Utility
    AirPlayUIAgent
    convertpdf
    Match
    Font Book
    AOSPushRelay
    KoreanIM
    SecurityFixer
    BluetoothUIServer
    Free42-Binary
    Show Info
    Ticket Viewer
    AppleMobileSync
    ODSAgent
    Droplet with Settable Properties
    Remove
    Cocoa-AppleScript Applet
    Image Events
    PrinterProxy
    AirPort Utility
    Archive Utility
    Database Events
    ChineseTextConverterService
    Installer
    JapaneseIM
    Calibration Assistant
    Maps
    Microsoft Office Setup Assistant
    PyCharm CE
    Game Center
    Embed
    Spotlight
    VirtualScanner
    FileMerge
    Software Update
    Microsoft AutoUpdate
    UnmountAssistantAgent
    Messages
    Microsoft Database Utility
    TCIM
    iCloudUserNotificationsd
    quicklookd
    CalendarFileHandler
    Problem Reporter
    Recursive Image File Processing Droplet
    Google Drive
    CMFSyncAgent
    Microsoft Ship Asserts
    syncuid
    AddressBookSync
    Memory Slot Utility
    AddPrinter
    SyncServicesAgent
    IMServicePlugInAgent
    Microsoft Query
    Script Editor
    AppleFileServer
    ColorSync Utility
    Finder
    MemoryCleanHelper
    Microsoft Word
    Type4Camera
    Pages
    Canon IJScanner4
    Microsoft Database Daemon
    WebProcess
    ScreenReaderUIServer
    PubSubAgent
    FindMyMacMessenger
    Cisco WebEx Meeting Center
    File Sync
    Preview
    Soundflowerbed
    Network Recording Player
    prezi
    QuickTime Player
    KeyboardSetupAssistant
    nbagent
    Wi-Fi","nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing","Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable","37.0.2062.120
    10.0
    8.5.9
    1.3
    2.3.0
    7.0
    5.2.6
    1.0
    1.0
    1.2
    15
    3.3.0
    3.0
    5.0
    1.0
    0.5.7
    1308.22.2900.0
    1.0.2
    1.8
    None
    None
    5.0.25
    1.0
    2.0
    2.6.9
    10.10
    2.84
    2.7.8
    2.0.1
    1.3.6
    1.1
    1.9
    14.4.6
    3.0
    4.0
    37.0.2062.120
    5.10
    1.4.55
    3.4.0 (build 4007)
    4.7
    1.6
    1.0
    7.0
    6.6
    7.0
    10.0
    1.6
    9.0
    5.0
    5.0
    1.4
    3.6
    2.5
    10.0
    5.7.6
    2.0-beta.6.4
    4.3.1
    14.4.6
    1.0
    33.1.1
    7.0
    6.19
    14.4.6
    1.1.0
    1.8
    10.8.0
    1.06
    5.4.0
    5.0
    Build 3065
    3.1
    1.06
    39.0.2171.71
    1.0
    10600
    10.10
    0.9.14.13.gba5645ad
    9.0
    9.0
    10.10
    1.3.44
    3.0
    2.7.8
    3.10
    1.0
    5.0.25
    2.0
    134.6
    10.0
    14.4.6
    None
    2.10.29
    14.4.6
    10.0.3
    14.4.6
    37.0.2062.120
    3.5
    2.0.0.20141103
    1.0
    5.0
    2.7.8
    7.0
    14.4.6
    8.1
    None
    1.0
    2.2.1
    8.1
    10600
    15
    14.4.6
    6.6
    10.10
    Adobe Photoshop Lightroom 5.6 [974614]
    6.1
    4.0
    10.10
    1.3
    None
    15.0.0
    8.1
    3.0.6
    4.3.1
    Version 2.2
    1.0.1
    9.0
    None
    5
    0.19.0.2.g3decb8e
    8.0
    13
    1.1
    10.0
    2.1.5
    14.4.6
    2.5
    10.0
    1.1.2
    7.1.0
    10.0
    1.0
    3.0
    2.0
    1.18
    3.8
    4.1
    2.5
    102
    1.10
    1.7
    25
    1.0
    2.1.0-50
    2.0.2
    9.0
    1.0
    14.4.6
    1.8
    2.7.6
    2.2.9
    None
    10.0
    13.0
    8.1
    10.0
    1.5.1
    8.4.19
    5.0
    7.0
    3.0
    14.4.6
    102
    327.5
    10.0
    6.1.1
    10600
    2.7
    14.4.6
    10.8
    1.0
    1.0.0
    81.0
    10600
    5.1.2
    1.0
    4.10.0
    4.1.1
    14.0
    1.0
    9.0
    6.5
    15.0.0
    3.0
    10.0
    1.0
    10.9
    10.10
    2.0
    4.5.2
    4.3.1
    1.2.1
    9.6
    8.0.25189
    1486.12
    3.2
    1.5
    1.2
    1.0
    15.0.0.239
    1.0
    1.0
    1.0.4
    10.0
    5.7
    2.2.1
    14.4.6
    3.1.0
    5.2.6
    0.4.6
    14.2.0
    4.1
    2.5
    4.0
    5.2
    7.0
    12.0.1
    802
    1.0
    1.0
    10.0
    5.0
    9.0
    10.0.6
    10.10
    37.0.2062.120
    1.1.6
    14.4.6
    10.10.0
    6.6
    1408.13.2909.0
    Medium Hefson
    1.8
    2.0
    1.2
    None
    5.0
    1.06
    6.4
    10.8
    4.3.1
    None
    None
    4.0
    5.0
    1.8
    1.0
    None
    1.0
    1.1.6
    10.0
    6.3.4
    10.10
    1.0.6
    2.1
    6.1.0
    5.0
    1.0
    2.0
    14.4.1
    3.4.1
    2.0
    None
    1.0
    4.0
    2.8
    6
    2.3.6
    5.0
    8.0
    14.4.6
    102
    1.0
    5.0
    8.0
    10.10
    1.0
    37.0.2062.120
    10.0
    1.1.4
    8.1
    9.0
    1.5.1
    10.0
    14.4.6
    10.0
    12.0.0
    2.7
    2.0
    4.10.0
    10.10.1
    1.0
    14.4.6
    10.0
    5.5.1
    3.1.0
    14.4.6
    10600
    7.0
    1.0.5
    4.1
    1410.10.2910.1
    8.1
    8.0
    1.0
    2.2.0
    r846
    10.4
    10.7
    1.0
    1.0"
    jtanium1.localdomain,"Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.6161
    Microsoft SQL Server 2008 R2 Management Objects
    Microsoft SQL Server System CLR Types
    Microsoft SQL Server 2012 (64-bit)
    Microsoft Visual C++ 2012 Redistributable (x86) - 11.0.61030
    Microsoft Visual C++ 2010  x86 Runtime - 10.0.40219
    Microsoft SQL Server 2012 Setup (English)
    Microsoft SQL Server 2012 Native Client 
    Google Chrome
    Microsoft Help Viewer 1.1
    Microsoft Visual Studio 2010 Shell (Isolated) - ENU
    Microsoft SQL Server 2008 Setup Support Files 
    Microsoft Report Viewer 2012 Runtime
    Microsoft Visual C++ 2010  x86 Redistributable - 10.0.40219
    Tanium Server 6.2.314.3258
    Python 2.7.8 (64-bit)
    Visual Studio 2010 Prerequisites - English
    Microsoft Visual C++ 2012 Redistributable (x64) - 11.0.61030
    Microsoft SQL Server 2012 Transact-SQL ScriptDom 
    Microsoft VSS Writer for SQL Server 2012
    Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.4974
    SQL Server Browser for SQL Server 2012
    Tanium Client Deployment Tool
    Adobe Flash Player 15 ActiveX
    Microsoft .NET Framework 4 Multi-Targeting Pack
    Microsoft Visual C++ 2010  x64 Redistributable - 10.0.40219
    Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.6161
    Microsoft .NET Framework 4.5.1
    VMware Tools
    Microsoft SQL Server 2012 Transact-SQL Compiler Service 
    Microsoft System CLR Types for SQL Server 2012 (x64)
    Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.4148
    Tanium Client 6.0.314.1190","MsiExec.exe /X{9BE518E6-ECC6-35A9-88E4-87755C07200F} /qn /noreboot
    MsiExec.exe /X{83F2B8F4-5CF3-4BE9-9772-9543EAE4AC5F} /qn /noreboot
    MsiExec.exe /X{C3F6F200-6D7B-4879-B9EE-700C0CE1FCDA} /qn /noreboot
    ""c:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\SetupARP.exe""
    ""C:\ProgramData\Package Cache\{33d1fd90-4274-48a1-9bc1-97e33d9c2d6f}\vcredist_x86.exe""  /uninstall
    MsiExec.exe /X{5D9ED403-94DE-3BA0-B1D6-71F4BDA412E6} /qn /noreboot
    MsiExec.exe /X{8CB0713F-CFE0-445D-BCB2-538465860E1A} /qn /noreboot
    MsiExec.exe /X{49D665A2-4C2A-476E-9AB8-FCC425F526FC} /qn /noreboot
    ""C:\Program Files (x86)\Google\Chrome\Application\39.0.2171.71\Installer\setup.exe"" --uninstall --multi-install --chrome --system-level
    c:\Program Files\Microsoft Help Viewer\v1.0\Microsoft Help Viewer 1.1\install.exe
    MsiExec.exe /X{D64B6984-242F-32BC-B008-752806E5FC44} /qn /noreboot
    MsiExec.exe /X{B40EE88B-400A-4266-A17B-E3DE64E94431} /qn /noreboot
    MsiExec.exe /X{9CCE40CE-A9E6-4916-8729-B008558EEF3F} /qn /noreboot
    MsiExec.exe /X{F0C3E5D1-1ADE-321E-8167-68EF0DE699A5} /qn /noreboot
    C:\Program Files\Tanium\Tanium Server\uninst.exe
    MsiExec.exe /X{61121B12-88BD-4261-A6EE-AB32610A56DE} /qn /noreboot
    MsiExec.exe /X{662014D2-0450-37ED-ABAE-157C88127BEB} /qn /noreboot
    ""C:\ProgramData\Package Cache\{ca67548a-5ebe-413a-b50c-4b9ceb6d66c6}\vcredist_x64.exe""  /uninstall
    MsiExec.exe /X{0E8670B8-3965-4930-ADA6-570348B67153} /qn /noreboot
    MsiExec.exe /X{3E0DD83F-BE4C-4478-86A0-AD0D79D1353E} /qn /noreboot
    MsiExec.exe /X{B7E38540-E355-3503-AFD7-635B2F2F76E1} /qn /noreboot
    MsiExec.exe /X{4B9E6EB0-0EED-4E74-9479-F982C3254F71} /qn /noreboot
    ""C:\Program Files (x86)\Tanium\Tanium Client Deployment Tool\uninstall.exe""
    C:\Windows\SysWOW64\Macromed\Flash\FlashUtil32_15_0_0_239_ActiveX.exe -maintain activex
    MsiExec.exe /X{CFEF48A8-BFB8-3EAC-8BA5-DE4F8AA267CE} /qn /noreboot
    MsiExec.exe /X{1D8E6291-B0D5-35EC-8441-6616F567A0F7} /qn /noreboot
    MsiExec.exe /X{5FCE6D76-F5DC-37AB-B2B8-22AB8CEDB1D4} /qn /noreboot
    C:\Windows\Microsoft.NET\Framework64\v4.0.30319\SetupCache\v4.5.50938\\Setup.exe /repair /x86 /x64
    MsiExec.exe /X{8CF7A691-09D2-4659-8C84-0406A7B58AE7} /qn /noreboot
    MsiExec.exe /X{BEB0F91E-F2EA-48A1-B938-7857ABF2A93D} /qn /noreboot
    MsiExec.exe /X{F1949145-EB64-4DE7-9D81-E6D27937146C} /qn /noreboot
    MsiExec.exe /X{1F1C2DFC-2D24-3E06-BCB8-725134ADF989} /qn /noreboot
    C:\Program Files (x86)\Tanium\Tanium Client\uninst.exe","Is Uninstallable
    Is Uninstallable
    Is Uninstallable
    Not Uninstallable
    Not Uninstallable
    Is Uninstallable
    Is Uninstallable
    Is Uninstallable
    Not Uninstallable
    Not Uninstallable
    Is Uninstallable
    Is Uninstallable
    Is Uninstallable
    Is Uninstallable
    Not Uninstallable
    Is Uninstallable
    Is Uninstallable
    Not Uninstallable
    Is Uninstallable
    Is Uninstallable
    Is Uninstallable
    Is Uninstallable
    Not Uninstallable
    Not Uninstallable
    Is Uninstallable
    Is Uninstallable
    Is Uninstallable
    Not Uninstallable
    Is Uninstallable
    Is Uninstallable
    Is Uninstallable
    Is Uninstallable
    Not Uninstallable","9.0.30729.6161
    10.51.2500.0
    10.51.2500.0
    64-
    11.0.61030.0
    10.0.40219
    11.1.3128.0
    11.0.2100.60
    39.0.2171.71
    1.1.40219
    10.0.40219
    10.1.2731.0
    11.0.2100.60
    10.0.40219
    6.2.314.3258
    2.7.8150
    10.0.40219
    11.0.61030.0
    11.0.2100.60
    11.0.2100.60
    9.0.30729.4974
    11.0.2100.60
    4.0.0.0
    15.0.0.239
    4.0.30319
    10.0.40219
    9.0.30729.6161
    4.5.50938
    9.8.4.2202052
    11.0.2100.60
    11.0.2100.60
    9.0.30729.4148
    6.0.314.1190"
    
