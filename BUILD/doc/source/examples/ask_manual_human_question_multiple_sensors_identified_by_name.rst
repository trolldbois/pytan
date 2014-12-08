
Ask manual human question multiple sensors identified by name
====================================================================================================
Ask a manual question using human strings by referencing the name of multiple sensors and providing a selector that tells pytan explicitly that we are providing a name of a sensor.

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
    kwargs["sensors"] = [u'name:Computer Name', u'name:Installed Applications']
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
    2014-12-08 15:05:51,962 INFO     question_progress: Results 0% (Get Computer Name and Installed Applications from all machines)
    2014-12-08 15:05:56,987 INFO     question_progress: Results 50% (Get Computer Name and Installed Applications from all machines)
    2014-12-08 15:06:02,009 INFO     question_progress: Results 100% (Get Computer Name and Installed Applications from all machines)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'question_object': <taniumpy.object_types.question.Question object at 0x10e57dd50>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10e0c9550>}
    
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
    Calendar
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
    8.0
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
    ubuntu.(none),"update-manager-core
    libminiupnpc8
    iso-codes
    libexttextcat-2.0-0
    libblkid1:amd64
    growisofs
    libdrm-radeon1:amd64
    findutils
    libxcomposite1:amd64
    libboost-system1.54.0:amd64
    libfftw3-single3:amd64
    libart-2.0-2:amd64
    usb-modeswitch
    libltdl7:amd64
    transmission-common
    gcc-4.8-base:amd64
    software-properties-common
    totem
    ibus-table
    libgc1c2:amd64
    time
    fonts-tlwg-waree
    libhx509-5-heimdal:amd64
    libsecret-common
    libevdocument3-4
    libpython2.7:amd64
    grub2-common
    libglamor0:amd64
    session-migration
    libogg0:amd64
    libgssapi-krb5-2:amd64
    libqt4-opengl:amd64
    libtimezonemap1
    python3-apport
    libxcb-shm0:amd64
    mountall
    gdisk
    libgnome-keyring0:amd64
    libnl-route-3-200:amd64
    python3-defer
    smbclient
    gnomine
    libbamf3-2:amd64
    librtmp0:amd64
    libqt5sensors5:amd64
    aisleriot
    libpwquality-common
    qdbus
    libecal-1.2-16
    libpam-modules:amd64
    libwayland-server0:amd64
    ethtool
    libsasl2-modules-db:amd64
    iproute2
    libspeex1:amd64
    libsnmp-base
    libreoffice-calc
    libmbim-glib0:amd64
    ncurses-bin
    nautilus-data
    accountsservice
    powermgmt-base
    pkg-config
    qtdeclarative5-ubuntu-ui-extras-browser-plugin-assets
    mime-support
    plainbox-secure-policy
    python-dbus-dev
    libelfg0:amd64
    ibus-gtk:amd64
    python3-brlapi
    unity-scope-musicstores
    libgettextpo-dev:amd64
    libxkbcommon0:amd64
    gvfs-bin
    gir1.2-packagekitglib-1.0
    acpid
    gir1.2-gtk-3.0
    cpp
    libpciaccess0:amd64
    libgsettings-qt1:amd64
    libnss3-nssdb
    libclucene-contribs1:amd64
    libcdr-0.0-0
    libebook-1.2-14
    libtext-wrapi18n-perl
    wireless-regdb
    dh-python
    libqt5svg5:amd64
    libnotify-bin
    libcups2:amd64
    iputils-arping
    python-aptdaemon.gtk3widgets
    libestr0
    dmidecode
    ubuntu-settings
    ifupdown
    libcurl3-gnutls:amd64
    python-chardet
    libxatracker2:amd64
    libcgmanager0:amd64
    mtr-tiny
    python3-pycurl
    libglib2.0-bin
    pulseaudio
    libpam-gnome-keyring:amd64
    libpython3.4:amd64
    ntfs-3g
    python3-distupgrade
    xserver-xorg
    libv4l-0:amd64
    libatk1.0-data
    libsepol1:amd64
    libxcb-dri3-0:amd64
    xml-core
    ubuntu-wallpapers
    qtdeclarative5-ubuntu-ui-extras-browser-plugin:amd64
    dmsetup
    rhythmbox-plugins
    libreoffice-gnome
    libgs9-common
    cpp-4.8
    hunspell-en-us
    libportaudio2:amd64
    libmailtools-perl
    keyboard-configuration
    libdigest-hmac-perl
    libwnck-3-common
    liblockfile1:amd64
    gstreamer1.0-plugins-good:amd64
    libpam-runtime
    sni-qt:amd64
    fonts-kacst-one
    libmission-control-plugins0
    libgrail6
    simple-scan
    gir1.2-soup-2.4
    printer-driver-splix
    libpoppler-glib8:amd64
    libdconf1:amd64
    libnss-mdns:amd64
    libjack-jackd2-0:amd64
    udev
    libtheora0:amd64
    linux-sound-base
    gvfs:amd64
    unity-settings-daemon
    indicator-messages
    poppler-data
    usb-creator-gtk
    xul-ext-webaccounts
    python-ubuntu-sso-client
    xserver-xorg-video-modesetting
    telnet
    cups-ppdc
    humanity-icon-theme
    libasprintf-dev:amd64
    liblightdm-gobject-1-0
    xfonts-mathml
    libasound2-data
    apg
    app-install-data-partner
    python3-problem-report
    wbritish
    liblircclient0
    libupstart1:amd64
    libcmis-0.4-4
    libgcrypt11:amd64
    libpulse0:amd64
    sed
    libyelp0
    libxi6:amd64
    python-samba
    python-cupshelpers
    fontconfig
    libgeoclue0:amd64
    isc-dhcp-client
    libshout3:amd64
    python3-mako
    net-tools
    ssh-import-id
    rsyslog
    libgucharmap-2-90-7
    wireless-tools
    zeitgeist-core
    libpcre3:amd64
    libpangoft2-1.0-0:amd64
    python-httplib2
    xserver-xorg-video-glamoregl
    lsb-release
    libcupscgi1:amd64
    libpolkit-gobject-1-0:amd64
    libavahi-gobject0:amd64
    unity-voice-service:amd64
    gpgv
    webaccounts-extension-common
    xfonts-scalable
    libuuid1:amd64
    update-notifier-common
    gir1.2-notify-0.7
    policykit-1-gnome
    libglew1.10:amd64
    gtk2-engines-murrine:amd64
    python3-debian
    python-qt4-dbus
    hplip-data
    libraw9:amd64
    libxmu6:amd64
    python-tdb
    libgail18:amd64
    xserver-xorg-video-nouveau
    libupower-glib1:amd64
    libaccount-plugin-1.0-0
    unity-control-center-signon
    libcdio13
    gstreamer1.0-x:amd64
    libtdb1:amd64
    libnewt0.52:amd64
    intel-gpu-tools
    gnome-desktop3-data
    firefox-locale-en
    gir1.2-rb-3.0
    lockfile-progs
    account-plugin-aim
    libopenobex1
    libxv1:amd64
    python3-crypto
    gir1.2-ebookcontacts-1.2
    pciutils
    xorg-docs-core
    hyphen-en-us
    libqtwebkit4:amd64
    ubuntu-docs
    unity-lens-music
    libcupsmime1:amd64
    ibus
    xserver-xorg-video-intel
    unity-scope-home
    libaa1:amd64
    libvorbisfile3:amd64
    libgdbm3:amd64
    mawk
    gnome-session-bin
    libpopt0:amd64
    libgraphite2-3:amd64
    gir1.2-secret-1
    libfile-basedir-perl
    gir1.2-edataserver-1.2
    remmina-plugin-vnc
    libxapian22
    libjasper1:amd64
    samba-common-bin
    linux-generic
    indicator-session
    libtelepathy-logger3:amd64
    printer-driver-c2esp
    gnome-orca
    xul-ext-ubufox
    libclutter-1.0-common
    qtdeclarative5-accounts-plugin
    libxft2:amd64
    liblangtag-common
    less
    qtchooser
    dmz-cursor-theme
    libcogl-common
    libdrm-nouveau2:amd64
    libgirepository-1.0-1
    libhyphen0
    xserver-xorg-video-all
    shotwell-common
    gnome-screenshot
    rhythmbox-data
    libfreerdp1:amd64
    crda
    libdbusmenu-qt2:amd64
    python-ldb
    remmina-plugin-rdp
    network-manager-gnome
    libdjvulibre21:amd64
    python-gtk2
    libclutter-gtk-1.0-0:amd64
    libproxy1:amd64
    libgstreamer-plugins-base0.10-0:amd64
    geoclue-ubuntu-geoip
    unity-scope-audacious
    fonts-sil-padauk
    xserver-xorg-video-radeon
    python-cairo
    make
    openssh-server
    sound-theme-freedesktop
    libarchive13:amd64
    xserver-xorg-video-cirrus
    dnsmasq-base
    x11-utils
    libnm-util2
    x11-session-utils
    gvfs-backends
    im-config
    libicu52:amd64
    libmm-glib0:amd64
    gconf2
    fonts-tlwg-garuda
    libopenvg1-mesa:amd64
    python-gobject-2
    landscape-client-ui-install
    fonts-freefont-ttf
    xorg
    libnm-gtk-common
    libapparmor1:amd64
    libclutter-gst-2.0-0:amd64
    python-gdbm
    krb5-locales
    apt-utils
    myspell-en-za
    libnatpmp1
    gvfs-common
    libsamplerate0:amd64
    libxinerama1:amd64
    libxkbfile1:amd64
    xserver-xorg-video-neomagic
    initscripts
    ssh-askpass-gnome
    kbd
    libnautilus-extension1a
    libwebpmux1:amd64
    libdaemon0
    python-dbus
    gnome-icon-theme-symbolic
    python-urllib3
    ttf-ubuntu-font-family
    apturl-common
    nautilus-share
    libgtk-3-bin
    libncurses5:amd64
    libxcb1:amd64
    libqt4-declarative:amd64
    libjson-glib-1.0-0:amd64
    avahi-autoipd
    xterm
    ubuntu-standard
    glib-networking:amd64
    libsensors4:amd64
    python-pkg-resources
    libgtk-3-0:amd64
    dbus
    uno-libs3
    zenity
    software-center-aptdaemon-plugins
    libxcb-render0:amd64
    xserver-xorg-core
    bzip2
    libcdio-cdda1
    ttf-indic-fonts-core
    unity-scope-gourmet
    zenity-common
    gir1.2-totem-1.0
    libatk1.0-0:amd64
    nux-tools
    xz-utils
    espeak-data:amd64
    libunity9:amd64
    libdevmapper1.02.1:amd64
    qtdeclarative5-ubuntu-ui-toolkit-plugin:amd64
    libedata-cal-1.2-23
    openssh-sftp-server
    modemmanager
    dvd+rw-tools
    python-talloc
    python-reportlab
    gnome-menus
    whoopsie
    libsignon-glib1
    unity-scope-firefoxbookmarks
    ubuntu-sso-client
    libwmf0.2-7:amd64
    xbitmaps
    mcp-account-manager-uoa
    gcc-4.9-base:amd64
    fonts-tlwg-mono
    libqt5core5a:amd64
    libufe-xidgetter0
    libreoffice-style-human
    software-properties-gtk
    gir1.2-networkmanager-1.0
    libopencc1:amd64
    libtalloc2:amd64
    libglib2.0-data
    python3-apt
    appmenu-qt
    gconf-service
    libreoffice-gtk
    libaspell15
    login
    gstreamer1.0-tools
    libmpfr4:amd64
    libwbclient0:amd64
    xserver-xorg-video-sisusb
    upower
    libpangox-1.0-0:amd64
    libkrb5support0:amd64
    printer-driver-postscript-hp
    libnet-libidn-perl
    gir1.2-messagingmenu-1.0
    libnet-ip-perl
    eject
    libhunspell-1.3-0:amd64
    libqt5quick5:amd64
    dnsutils
    libmagic1:amd64
    brasero-cdrkit
    ltrace
    linux-headers-generic
    unity-scope-openclipart
    libldap-2.4-2:amd64
    apport-gtk
    libxt6:amd64
    sessioninstaller
    libclass-accessor-perl
    python-gnomekeyring
    libnet-dns-perl
    libapparmor-perl
    libido3-0.1-0:amd64
    libacl1:amd64
    thunderbird
    mscompress
    gedit-common
    libebook-contacts-1.2-0
    libcroco3:amd64
    libsignon-extension1
    libncursesw5:amd64
    gstreamer0.10-plugins-base-apps
    debianutils
    debconf-i18n
    manpages
    libgupnp-igd-1.0-4:amd64
    gstreamer1.0-pulseaudio:amd64
    librhythmbox-core8
    Name
    xcursor-themes
    ibus-gtk3:amd64
    libsndfile1:amd64
    avahi-daemon
    libunity-gtk2-parser0:amd64
    libxcb-icccm4:amd64
    libcairomm-1.0-1:amd64
    libmspub-0.0-0
    tcl8.6
    libqpdf13:amd64
    python3.4-minimal
    libgeis1:amd64
    libcanberra-gtk0:amd64
    gvfs-libs:amd64
    libxxf86dga1:amd64
    libfarstream-0.1-0:amd64
    tk
    libbrasero-media3-1
    samba-libs:amd64
    overlay-scrollbar-gtk3:amd64
    gnome-settings-daemon-schemas
    unity-lens-files
    libwnck22
    unity-scope-guayadeque
    libvpx1:amd64
    cups-filters
    aptdaemon-data
    python-serial
    python-qt4
    libreoffice-impress
    thunderbird-locale-en
    libusb-0.1-4:amd64
    busybox-initramfs
    libsignon-qt5-1
    python-oauthlib
    shared-mime-info
    libgssapi3-heimdal:amd64
    libsnmp30:amd64
    file-roller
    pm-utils
    libsub-name-perl
    libpython2.7-minimal:amd64
    libtxc-dxtn-s2tc0:amd64
    memtest86+
    libcairo-gobject2:amd64
    onboard-data
    libkpathsea6
    libcap2:amd64
    python3-gi
    libproxy1-plugin-networkmanager:amd64
    libframe6:amd64
    grub-pc
    libtext-iconv-perl
    unity-webapps-common
    libjson0:amd64
    acl
    poppler-utils
    appmenu-qt5
    libt1-5
    python3-plainbox
    libdbusmenu-gtk3-4:amd64
    gir1.2-gdata-0.0
    python-gobject
    libp11-kit-gnome-keyring:amd64
    adium-theme-ubuntu
    gettext
    notify-osd-icons
    libarchive-zip-perl
    libsane-hpaio
    libcloog-isl4:amd64
    libijs-0.35
    ubuntu-mono
    unity-scope-clementine
    libunity-core-6.0-9
    gstreamer0.10-nice:amd64
    gir1.2-gst-plugins-base-1.0
    libreoffice-help-en-us
    qtdeclarative5-dialogs-plugin:amd64
    folks-common
    libxcb-sync1:amd64
    libipc-system-simple-perl
    bluez-alsa:amd64
    xinput
    libjson-c2:amd64
    cups-daemon
    python-pil
    libattr1:amd64
    libcdio-paranoia1
    libudev1:amd64
    language-pack-gnome-en
    acpi-support
    vino
    grub-pc-bin
    libqtgui4:amd64
    unity-gtk-module-common
    libappindicator3-1
    branding-ubuntu
    remmina-common
    python-smbc
    dc
    perl-modules
    libselinux1:amd64
    liblcms2-2:amd64
    ure
    libsemanage1:amd64
    plymouth
    libatk-bridge2.0-0:amd64
    libvte-2.90-9
    libdns100
    hplip
    system-config-printer-gnome
    libio-socket-ssl-perl
    python3-minimal
    unity-lens-friends
    libburn4
    openssh-client
    libipc-run-perl
    pulseaudio-utils
    obexd-client
    libgtk2.0-bin
    command-not-found-data
    hud
    onboard
    libc6:amd64
    nautilus-sendto
    libgcr-ui-3-1:amd64
    libavahi-glib1:amd64
    ed
    libxklavier16
    gstreamer1.0-plugins-base:amd64
    libpng12-0:amd64
    libqt4-test:amd64
    tzdata
    gnome-font-viewer
    libklibc
    unity-scope-video-remote
    libc-dev-bin
    libxslt1.1:amd64
    libgtop2-common
    gnome-disk-utility
    libfuse2:amd64
    unattended-upgrades
    libmeanwhile1
    xserver-xorg-video-savage
    libboost-date-time1.54.0:amd64
    libreoffice-writer
    light-themes
    libfarstream-0.2-2:amd64
    libtotem0
    fonts-opensymbol
    libtk8.6:amd64
    unity-scope-colourlovers
    libavahi-client3:amd64
    libpam-modules-bin
    gir1.2-gtksource-3.0
    python-apt-common
    tcpdump
    libxrender1:amd64
    cups-filters-core-drivers
    libavahi-common3:amd64
    libaudio2:amd64
    printer-driver-min12xxw
    ubuntu-artwork
    whoopsie-preferences
    python3-aptdaemon
    fonts-tlwg-purisa
    pptp-linux
    indicator-power
    libclutter-1.0-0:amd64
    python3-checkbox-ng
    libunity-scopes-json-def-desktop
    strace
    python-reportlab-accel
    libwacom2:amd64
    notify-osd
    libflac8:amd64
    libiw30:amd64
    liburl-dispatcher1:amd64
    libmpdec2:amd64
    liburi-perl
    gir1.2-dee-1.0
    sane-utils
    libgbm1:amd64
    libsigc++-2.0-0c2a:amd64
    libatomic1:amd64
    libqt4-xml:amd64
    libgrip0
    libcolamd2.8.0:amd64
    python3-six
    gnome-control-center-shared-data
    libqt4-sql-sqlite:amd64
    libisofs6
    libgles2-mesa:amd64
    libxp6:amd64
    liborc-0.4-0:amd64
    evince-common
    webapp-container
    xul-ext-websites-integration
    evince
    account-plugin-yahoo
    liblangtag1
    libjson-glib-1.0-common
    unity-greeter
    gir1.2-gudev-1.0
    rhythmbox-plugin-zeitgeist
    syslinux-legacy
    libxvmc1:amd64
    libwebp5:amd64
    iptables
    liboxideqt-qmlplugin:amd64
    unity-scope-calculator
    fonts-liberation
    libsub-identify-perl
    libprocps3:amd64
    hwdata
    libnet-domain-tld-perl
    libgnutls26:amd64
    libpci3:amd64
    qtdeclarative5-localstorage-plugin:amd64
    libsoup2.4-1:amd64
    libwps-0.2-2
    libdbus-glib-1-2:amd64
    python-crypto
    libdbusmenu-glib4:amd64
    libpolkit-backend-1-0:amd64
    libgnome-keyring-common
    python3-cairo
    libexpat1:amd64
    python-defer
    language-pack-en
    signon-keyring-extension
    libisl10:amd64
    gir1.2-unity-5.0:amd64
    libisccc90
    gsettings-ubuntu-schemas
    patchutils
    gnome-video-effects
    python-gconf
    libcanberra-pulse:amd64
    libreadline5:amd64
    libgnutls-openssl27:amd64
    gzip
    systemd-shim
    indicator-bluetooth
    totem-mozilla
    libasound2-plugins:amd64
    libmythes-1.2-0
    ssl-cert
    plymouth-label
    libgcc1:amd64
    libvorbisenc2:amd64
    gstreamer0.10-alsa:amd64
    libcupsppdc1:amd64
    libgutenprint2
    apt-xapian-index
    xserver-xorg-input-evdev
    libpoppler44:amd64
    dash
    libheimbase1-heimdal:amd64
    libaccounts-qt5-1
    libgudev-1.0-0:amd64
    libgpm2:amd64
    qt-at-spi:amd64
    python3-piston-mini-client
    unity-scope-tomboy
    remmina
    libasyncns0:amd64
    libcolord1:amd64
    libspectre1:amd64
    gir1.2-freedesktop
    libvorbis0a:amd64
    qtdeclarative5-window-plugin:amd64
    libquadmath0:amd64
    wamerican
    grub-common
    libqt5network5:amd64
    python-sip
    libwayland-cursor0:amd64
    gir1.2-atk-1.0
    python3-urllib3
    activity-log-manager
    libwmf0.2-7-gtk
    gvfs-fuse
    libssh-4:amd64
    signon-plugin-oauth2
    libsocket6-perl
    e2fsprogs
    librsync1:amd64
    cups-server-common
    gnome-session-canberra
    printer-driver-gutenprint
    transmission-gtk
    libx11-xcb1:amd64
    libwhoopsie-preferences0
    libdv4:amd64
    tar
    usb-creator-common
    aspell
    libcupsfilters1:amd64
    libx11-6:amd64
    wpasupplicant
    ttf-punjabi-fonts
    libisc95
    pppconfig
    python-debian
    liblzo2-2:amd64
    python-pam
    gcr
    lightdm
    sphinx-voxforge-hmm-en
    libautodie-perl
    libqt4-svg:amd64
    libatspi2.0-0:amd64
    syslinux
    libsane:amd64
    indicator-application
    liblouis2:amd64
    libreoffice-common
    command-not-found
    libsignon-plugins-common1
    librsvg2-2:amd64
    aspell-en
    libgoa-1.0-0b:amd64
    python-piston-mini-client
    libxkbcommon-x11-0:amd64
    logrotate
    unity-scope-devhelp
    cups-pk-helper
    iputils-tracepath
    multiarch-support
    xserver-xorg-video-vesa
    unity-gtk2-module:amd64
    libfile-mimeinfo-perl
    unity-webapps-qml
    libtag1-vanilla:amd64
    apt
    qtdeclarative5-qtfeedback-plugin:amd64
    unity-scope-zotero
    libqt5sql5-sqlite:amd64
    indicator-sound
    netbase
    gir1.2-gnomekeyring-1.0
    libcupsimage2:amd64
    libreoffice-ogltrans
    libxpm4:amd64
    libnl-3-200:amd64
    libcogl-pango15:amd64
    libgomp1:amd64
    libwhoopsie0
    deja-dup-backend-gvfs
    libexempi3:amd64
    qpdf
    xserver-xorg-video-mga
    libgoa-1.0-common
    fonts-tlwg-kinnari
    fonts-kacst
    brltty
    libmtp-common
    libarchive-extract-perl
    libjte1
    libxres1:amd64
    libedit2:amd64
    libpeas-1.0-0
    liboxideqtcore0:amd64
    libproxy1-plugin-gsettings:amd64
    rfkill
    cheese-common
    libidn11:amd64
    gconf-service-backend
    libmnl0:amd64
    libevent-2.0-5:amd64
    libsqlite3-0:amd64
    gstreamer0.10-plugins-good:amd64
    libfriends0:amd64
    mythes-en-us
    gnome-calculator
    cpio
    python-twisted-bin
    libclucene-core1:amd64
    ubuntu-minimal
    unity-services
    ppp
    libqt4-designer:amd64
    brasero-common
    hostname
    iproute
    libcolumbus1:amd64
    openprinting-ppds
    libenchant1c2a:amd64
    python-aptdaemon
    unity-scopes-master-default
    gir1.2-pango-1.0
    webbrowser-app
    libxfont1:amd64
    python-lxml
    parted
    librasqal3:amd64
    libffi6:amd64
    fontconfig-config
    libc6-dbg:amd64
    libxcb-keysyms1:amd64
    libunityvoice1:amd64
    libaccountsservice0:amd64
    tk8.6
    liblog-message-simple-perl
    xserver-xorg-video-mach64
    libhcrypto4-heimdal:amd64
    usb-modeswitch-data
    psmisc
    telepathy-gabble
    unity-lens-photos
    libnet-smtp-ssl-perl
    python2.7-minimal
    libasan0:amd64
    libplymouth2:amd64
    totem-plugins
    libudisks2-0:amd64
    libvisio-0.0-0
    libsecret-1-0:amd64
    libharfbuzz0b:amd64
    python3-xkit
    tcl
    libdmapsharing-3.0-2
    bluez
    bsdutils
    intltool-debian
    dosfstools
    gir1.2-javascriptcoregtk-3.0
    libss2:amd64
    tcpd
    libgnome-bluetooth11
    ubuntu-session
    libnspr4:amd64
    hardening-includes
    gnome-screensaver
    libfontconfig1:amd64
    libreoffice-presentation-minimizer
    indicator-appmenu
    zip
    libqtcore4:amd64
    liborcus-0.6-0
    libcheese-gtk23:amd64
    unity-lens-video
    xdiagnose
    python-xapian
    desktop-file-utils
    telepathy-logger
    eog
    libpangoxft-1.0-0:amd64
    firefox
    libmhash2:amd64
    python3-httplib2
    libpurple0
    lshw
    checkbox-ng-service
    libcurl3:amd64
    gnome-accessibility-themes
    account-plugin-windows-live
    speech-dispatcher
    ucf
    initramfs-tools-bin
    gnome-keyring
    gsettings-desktop-schemas
    libreoffice-avmedia-backend-gstreamer
    libqt5positioning5:amd64
    libspice-server1:amd64
    kmod
    indicator-keyboard
    ubuntu-sounds
    gir1.2-signon-1.0
    python3.4
    libgck-1-0:amd64
    duplicity
    colord
    libpython3.4-stdlib:amd64
    telepathy-haze
    python-ibus
    gvfs-daemons
    gir1.2-gdkpixbuf-2.0
    printer-driver-foo2zjs
    gnome-bluetooth
    unity-scope-virtualbox
    libxfixes3:amd64
    aptdaemon
    printer-driver-pnm2ppa
    toshset
    myspell-en-gb
    libqtdbus4:amd64
    network-manager-pptp
    libpaper-utils
    libpam-systemd:amd64
    libuuid-perl
    xfonts-encodings
    libqt5widgets5:amd64
    python2.7
    python3-pyparsing
    libassuan0:amd64
    libunity-webapps0
    libaccounts-glib0:amd64
    libqt5qml-graphicaleffects:amd64
    patch
    libmount1:amd64
    makedev
    gir1.2-gnomebluetooth-1.0
    librest-0.7-0:amd64
    libjbig2dec0
    evolution-data-server-common
    libnfnetlink0:amd64
    libiec61883-0:amd64
    libpython3-stdlib:amd64
    libwrap0:amd64
    libgee-0.8-2:amd64
    fonts-dejavu-core
    libtag1c2a:amd64
    libjavascriptcoregtk-3.0-0:amd64
    libpyzy-1.0-0
    cron
    libraw1394-11:amd64
    libgstreamer0.10-0:amd64
    libcomerr2:amd64
    cups-client
    libsoup-gnome2.4-1:amd64
    libxshmfence1:amd64
    libcanberra-gtk-module:amd64
    libgstreamer1.0-0:amd64
    lp-solve
    python3-uno
    openoffice.org-hyphenation
    libzeitgeist-2.0-0:amd64
    seahorse
    libegl1-mesa-drivers:amd64
    ubuntu-keyring
    libdebconfclient0:amd64
    netcat-openbsd
    libgcr-3-common
    signon-plugin-password
    python3-oneconf
    libldb1:amd64
    libauthen-sasl-perl
    linux-headers-3.13.0-32-generic
    libnet-ssleay-perl
    python3-aptdaemon.pkcompat
    libsasl2-modules:amd64
    python-debtagshw
    at-spi2-core
    libkrb5-26-heimdal:amd64
    libgl1-mesa-dri:amd64
    gnome-sudoku
    libpango-1.0-0:amd64
    libsonic0:amd64
    zeitgeist
    libfreerdp-plugins-standard:amd64
    gettext-base
    libneon27-gnutls
    ubuntu-extras-keyring
    libplist1:amd64
    libbluetooth3:amd64
    libsbc1:amd64
    python3-xdg
    libnice10:amd64
    libgnomekbd8
    libqt5printsupport5:amd64
    libgettextpo0:amd64
    libcheese7:amd64
    libdbusmenu-gtk4:amd64
    x11-apps
    libqt5feedback5:amd64
    gir1.2-gstreamer-1.0
    lintian
    libfolks-eds25:amd64
    libgdata-common
    libgtop2-7
    libdrm2:amd64
    sysvinit-utils
    libgstreamer-plugins-base1.0-0:amd64
    libxaw7:amd64
    gnome-mines
    fonts-lao
    libcap2-bin
    python-dirspec
    usbutils
    mobile-broadband-provider-info
    libtelepathy-glib0:amd64
    libcogl15:amd64
    libaccount-plugin-generic-oauth
    libfontembed1:amd64
    libreoffice-pdfimport
    libindicator3-7
    liblzma5:amd64
    wodim
    TaniumClient
    gir1.2-totem-plparser-1.0
    xul-ext-unity
    language-selector-common
    linux-libc-dev:amd64
    libgtk2.0-0:amd64
    python3-gi-cairo
    libatasmart4:amd64
    libqt4-network:amd64
    usbmuxd
    libpipeline1:amd64
    libxcursor1:amd64
    python3-speechd
    python-cups
    libgeoip1:amd64
    libieee1284-3:amd64
    oneconf-common
    apport
    myspell-en-au
    telepathy-salut
    geoip-database
    libdecoration0
    libgweather-3-6
    fonts-nanum
    libreoffice-draw
    fonts-tlwg-sawasdee
    evolution-data-server-online-accounts
    hdparm
    libavahi-core7:amd64
    libparse-debianchangelog-perl
    totem-common
    popularity-contest
    libgs9
    libthumbnailer0:amd64
    gstreamer1.0-clutter
    python3-aptdaemon.gtk3widgets
    apport-symptoms
    python-requests
    libnss3:amd64
    bc
    unity-scope-gdrive
    ibus-pinyin
    libthai0:amd64
    libxcb-render-util0:amd64
    libcanberra-gtk3-module:amd64
    install-info
    diffutils
    update-inetd
    gir1.2-atspi-2.0
    libreadline6:amd64
    gnome-icon-theme
    gkbd-capplet
    x11-xkb-utils
    foomatic-db-compressed-ppds
    libqt4-sql:amd64
    update-notifier
    libice6:amd64
    pppoeconf
    python-gi
    libkmod2:amd64
    python-twisted-web
    printer-driver-pxljr
    libqt5gui5:amd64
    libusbmuxd2
    libgcr-base-3-1:amd64
    libjpeg8:amd64
    libgdk-pixbuf2.0-common
    libck-connector0:amd64
    libpwquality1:amd64
    fonts-tlwg-typo
    libclone-perl
    python3-dbus
    ubuntu-system-service
    libhpmud0
    libjbig0:amd64
    libreoffice-base-core
    libaudit1:amd64
    telepathy-idle
    libxcb-glx0:amd64
    libaudit-common
    iputils-ping
    linux-image-generic
    libfribidi0:amd64
    dconf-gsettings-backend:amd64
    fonts-tibetan-machine
    gstreamer0.10-tools
    xserver-xorg-video-vmware
    cracklib-runtime
    python-openssl
    gir1.2-webkit-3.0
    librsvg2-common:amd64
    system-config-printer-udev
    xdg-user-dirs-gtk
    xserver-xorg-video-s3
    libustr-1.0-1:amd64
    python-oneconf
    libsphinxbase1
    libcolumbus1-common
    python
    libgweather-common
    alsa-utils
    perl
    libedataserver-1.2-18
    libgxps2:amd64
    python-lockfile
    nautilus
    libpcap0.8:amd64
    libpulse-mainloop-glib0:amd64
    binutils
    Err?=(none)/Reinst-required
    base-passwd
    brasero
    libfs6:amd64
    cheese
    python3-software-properties
    libroken18-heimdal:amd64
    libllvm3.4:amd64
    rhythmbox
    openssl
    libnux-4.0-0
    ncurses-base
    gir1.2-ebook-1.2
    libwind0-heimdal:amd64
    lsof
    coreutils
    libdotconf0:amd64
    libperlio-gzip-perl
    libgmp10:amd64
    libunistring0:amd64
    libssl1.0.0:amd64
    fonts-lklug-sinhala
    libapt-inst1.5:amd64
    gir1.2-udisks-2.0
    liblockfile-bin
    compiz-plugins-default
    mousetweaks
    python3-update-manager
    libzephyr4:amd64
    checkbox-gui
    grep
    rhythmbox-mozilla
    libcairo2:amd64
    libedata-book-1.2-20
    obex-data-server
    xauth
    dialog
    gir1.2-ibus-1.0
    xserver-xorg-video-openchrome
    libsgutils2-2
    libgconf-2-4:amd64
    python3-oauthlib
    dbus-x11
    compiz-gnome
    wget
    rsync
    libqt4-scripttools:amd64
    libglu1-mesa:amd64
    media-player-info
    python-imaging
    libemail-valid-perl
    libtiff5:amd64
    libsm6:amd64
    unity-asset-pool
    libgnome-desktop-3-7
    nano
    libtevent0:amd64
    linux-headers-3.13.0-32
    python3-chardet
    libical1
    libpython-stdlib:amd64
    xserver-xorg-video-siliconmotion
    libgpg-error0:amd64
    sudo
    libunity-control-center1
    ubuntu-drivers-common
    libcrack2:amd64
    readline-common
    libapt-pkg-perl
    rhythmbox-plugin-magnatune
    libpangocairo-1.0-0:amd64
    libpod-latex-perl
    qtdeclarative5-qtquick2-plugin:amd64
    libqt5xml5:amd64
    libwacom-common
    libx11-data
    libv4lconvert0:amd64
    ubuntu-release-upgrader-core
    unzip
    unity-lens-applications
    unity-scope-manpages
    gir1.2-appindicator3-0.1
    libgphoto2-6:amd64
    libpackagekit-glib2-16:amd64
    libmtdev1:amd64
    python3-lxml
    ssh
    libgpgme11:amd64
    diffstat
    ubuntu-ui-toolkit-theme
    mlocate
    bash-completion
    libnm-glib-vpn1
    xserver-xorg-input-all
    libtsan0:amd64
    libtimedate-perl
    isc-dhcp-common
    x11-xserver-utils
    libwayland-client0:amd64
    fonts-tlwg-loma
    libcolorhug1:amd64
    libfreetype6:amd64
    whiptail
    python3-pyatspi
    busybox-static
    cups-core-drivers
    libpython3.4-minimal:amd64
    os-prober
    base-files
    libimobiledevice4:amd64
    bsdmainutils
    gdb
    doc-base
    enchant
    libmodule-pluggable-perl
    friends-facebook
    gedit
    libevview3-3
    libxdmcp6:amd64
    gnome-power-manager
    libgphoto2-l10n
    libsmbclient:amd64
    python-renderpm
    ntpdate
    baobab
    procps
    bluez-cups
    libdee-1.0-4:amd64
    python-commandnotfound
    python-ntdb
    libasprintf0c2:amd64
    libx86-1:amd64
    xserver-xorg-input-wacom
    xserver-common
    gcc
    libwebkitgtk-3.0-0:amd64
    printer-driver-ptouch
    libxtables10
    libxml2:amd64
    python3-louis
    gir1.2-glib-2.0
    libtext-charwidth-perl
    python-zeitgeist
    gir1.2-wnck-3.0
    yelp-xsl
    gstreamer0.10-pulseaudio:amd64
    unity-scope-musique
    gnome-session-common
    xdg-user-dirs
    libgdata13
    shotwell
    gstreamer0.10-plugins-base:amd64
    friends
    libc6-dev:amd64
    libxcb-xfixes0:amd64
    gstreamer1.0-plugins-base-apps
    gnome-user-guide
    xkb-data
    zlib1g:amd64
    python-notify
    libraptor2-0:amd64
    libbind9-90
    xserver-xorg-input-synaptics
    apparmor
    libreoffice-core
    libqt4-script:amd64
    libqt4-dbus:amd64
    guile-2.0-libs
    laptop-detect
    gir1.2-goa-1.0
    gnome-system-monitor
    printer-driver-sag-gdi
    libqt5qml5:amd64
    libspeexdsp1:amd64
    apt-transport-https
    libfontenc1:amd64
    dconf-service
    bind9-host
    xserver-xorg-video-fbdev
    libespeak1:amd64
    librdf0:amd64
    libvisual-0.4-0:amd64
    avahi-utils
    libwnck-common
    p11-kit
    xserver-xorg-video-sis
    passwd
    libwavpack1:amd64
    app-install-data
    unity-scopes-runner
    libqt5test5:amd64
    libasn1-8-heimdal:amd64
    libyajl2:amd64
    libgnome-control-center1
    account-plugin-jabber
    ghostscript
    pulseaudio-module-bluetooth
    libasound2:amd64
    fuse
    libpocketsphinx1
    libelf1:amd64
    overlay-scrollbar
    libxtst6:amd64
    libslang2:amd64
    libgtk-3-common
    upstart
    cups-bsd
    rtkit
    libqt5opengl5:amd64
    e2fslibs:amd64
    libgtk2.0-common
    libnux-4.0-common
    libpam0g:amd64
    grub-gfxpayload-lists
    libcrypt-passwdmd5-perl
    libpurple-bin
    language-selector-gnome
    thunderbird-gnome-support
    cups
    libyaml-tiny-perl
    libdbus-1-3:amd64
    vbetool
    rhythmbox-plugin-cdrecorder
    signond
    libpeas-common
    libxrandr2:amd64
    xdg-utils
    libsemanage-common
    samba-common
    libgpod4:amd64
    libunity-misc4
    libmtp-runtime
    xserver-xorg-video-r128
    zeitgeist-datahub
    man-db
    initramfs-tools
    libvncserver0:amd64
    yelp
    unity-scope-yelp
    gnupg
    speech-dispatcher-audio-plugins:amd64
    libmpc3:amd64
    libgtksourceview-3.0-common
    fonts-tlwg-umpush
    python-pycurl
    account-plugin-twitter
    libxcb-image0:amd64
    libqt5multimedia5:amd64
    gir1.2-dbusmenu-glib-0.4
    syslinux-common
    libnm-gtk0
    activity-log-manager-control-center
    python-pexpect
    libgmime-2.6-0:amd64
    python-minimal
    None
    libtelepathy-farstream3:amd64
    libnettle4:amd64
    libheimntlm0-heimdal:amd64
    libparted0debian1:amd64
    lsb-base
    linux-image-extra-3.13.0-32-generic
    libpython2.7-stdlib:amd64
    libxcb-xkb1:amd64
    libqt5webkit5:amd64
    sensible-utils
    libgpod-common
    ftp
    adduser
    libaccount-plugin-google
    irqbalance
    policykit-1
    account-plugin-flickr
    python-xdg
    python-apt
    sgml-base
    nautilus-sendto-empathy
    xserver-xorg-input-vmmouse
    libmtp9:amd64
    plymouth-theme-ubuntu-logo
    xserver-xorg-video-tdfx
    libcdparanoia0:amd64
    libterm-ui-perl
    ncurses-term
    liboauth0:amd64
    libxdamage1:amd64
    fonts-thai-tlwg
    gstreamer1.0-nice:amd64
    software-center
    libmetacity-private0a
    libtext-levenshtein-perl
    libpcsclite1:amd64
    language-pack-en-base
    libkrb5-3:amd64
    libcap-ng0
    libqt5organizer5:amd64
    libgphoto2-port10:amd64
    libcanberra-gtk3-0:amd64
    telepathy-indicator
    metacity-common
    unity-control-center
    libfile-copy-recursive-perl
    apturl
    gsfonts
    libgusb2:amd64
    libfile-fcntllock-perl
    libxcb-util0:amd64
    qtdeclarative5-privatewidgets-plugin:amd64
    plymouth-theme-ubuntu-text
    libpaper1:amd64
    friendly-recovery
    libmessaging-menu0
    gstreamer0.10-x:amd64
    unity-scope-gmusicbrowser
    libapt-pkg4.12:amd64
    libnuma1:amd64
    libgail-3-0:amd64
    evolution-data-server
    libnetfilter-conntrack3:amd64
    qtcore4-l10n
    libavahi-common-data:amd64
    indicator-datetime
    language-pack-gnome-en-base
    libvte-2.90-common
    gnome-contacts
    libstartup-notification0:amd64
    insserv
    libcaca0:amd64
    libnl-genl-3-200:amd64
    libio-pty-perl
    libharfbuzz-icu0:amd64
    unity-webapps-service
    libegl1-mesa:amd64
    libglewmx1.10:amd64
    libsystemd-journal0:amd64
    libqmi-glib0:amd64
    libzeitgeist-1.0-1
    libjpeg-turbo8:amd64
    libstdc++6:amd64
    libnih1:amd64
    update-manager
    libperl5.18
    vim-common
    libsasl2-2:amd64
    mount
    libibus-1.0-5:amd64
    libfolks-telepathy25:amd64
    xfonts-base
    libprotobuf8:amd64
    xinit
    init-system-helpers
    libsystemd-login0:amd64
    libqt5webkit5-qmlwebkitplugin:amd64
    python3-feedparser
    libgssdp-1.0-3
    dpkg
    libexif12:amd64
    ubuntuone-client-data
    libdpkg-perl
    libc-bin
    genisoimage
    libxext6:amd64
    libspeechd2:amd64
    liblist-moreutils-perl
    account-plugin-google
    fonts-tlwg-typist
    unity-scope-texdoc
    policykit-desktop-privileges
    libgupnp-1.0-4
    libgail-common:amd64
    libp11-kit0:amd64
    ubuntu-wallpapers-trusty
    libntdb1:amd64
    gstreamer1.0-alsa:amd64
    Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
    libgtkmm-3.0-1:amd64
    fonts-sil-abyssinica
    libxcb-present0:amd64
    libreoffice-math
    libxcb-shape0:amd64
    groff-base
    libwnck-3-0:amd64
    x11-common
    indicator-printers
    udisks2
    libxxf86vm1:amd64
    ghostscript-x
    libxcb-dri2-0:amd64
    libqt4-xmlpatterns:amd64
    libdb5.3:amd64
    util-linux
    libtasn1-6:amd64
    fonts-takao-pgothic
    libgstreamer-plugins-good1.0-0:amd64
    libnih-dbus1:amd64
    ubuntu-release-upgrader-gtk
    libsane-common
    pulseaudio-module-x11
    libgd3:amd64
    libwayland-egl1-mesa:amd64
    gconf2-common
    libgdk-pixbuf2.0-0:amd64
    liblwres90
    sphinx-voxforge-lm-en
    fonts-khmeros-core
    klibc-utils
    gir1.2-gmenu-3.0
    libexttextcat-data
    dictionaries-common
    mtools
    libitm1:amd64
    python-zope.interface
    perl-base
    ca-certificates
    python3
    libglapi-mesa:amd64
    gtk3-engines-unico:amd64
    ufw
    alsa-base
    linux-firmware
    libdjvulibre-text
    libqt5sql5:amd64
    libxau6:amd64
    signon-ui
    python3-requests
    account-plugin-facebook
    python3-markupsafe
    gnome-user-share
    gcc-4.8
    libpulsedsp:amd64
    gnome-mahjongg
    libgcc-4.8-dev:amd64
    libgtksourceview-3.0-1:amd64
    libxss1:amd64
    locales
    gir1.2-vte-2.90
    oneconf
    libgnome-menu-3-0
    libtext-soundex-perl
    friends-dispatcher
    python-libxml2
    liblua5.2-0:amd64
    libcamel-1.2-45
    libbsd0:amd64
    python-twisted-core
    system-config-printer-common
    overlay-scrollbar-gtk2:amd64
    bamfdaemon
    systemd-services
    qtdeclarative5-unity-action-plugin:amd64
    gnome-system-log
    libpangomm-1.4-1:amd64
    libatkmm-1.6-1:amd64
    checkbox-ng
    libpixman-1-0:amd64
    python3-commandnotfound
    libcanberra0:amd64
    libtcl8.6:amd64
    hicolor-icon-theme
    oxideqt-codecs:amd64
    account-plugin-salut
    libglib2.0-0:amd64
    libio-socket-inet6-perl
    ubuntu-desktop
    deja-dup
    bash
    gucharmap
    libbrlapi0.6:amd64
    inputattach
    glib-networking-services
    libusb-1.0-0:amd64
    libthai-data
    x11-xfs-utils
    uuid-runtime
    module-init-tools
    libtinfo5:amd64
    printer-driver-hpcups
    unity
    t1utils
    libio-string-perl
    xserver-xorg-input-mouse
    p11-kit-modules:amd64
    libunity-protocol-private0:amd64
    libwebkitgtk-3.0-common
    ureadahead
    libkeyutils1:amd64
    libpango1.0-0:amd64
    gnome-terminal-data
    info
    plainbox-provider-checkbox
    libhud2:amd64
    plainbox-provider-resource-generic
    friends-twitter
    unity-gtk3-module:amd64
    fonts-droid
    libqt5dbus5:amd64
    libqt4-help:amd64
    fonts-tlwg-norasi
    libxcb-randr0:amd64
    libpam-cap:amd64
    example-content
    libqtassistantclient4:amd64
    cups-browsed
    libcompizconfig0
    xserver-xorg-video-qxl
    console-setup
    libdatrie1:amd64
    libebackend-1.2-7
    printer-driver-foo2zjs-common
    compiz
    libnotify4:amd64
    python3-gdbm:amd64
    libgnomekbd-common
    libvisual-0.4-plugins:amd64
    libpolkit-agent-1-0:amd64
    python-gi-cairo
    libfolks25:amd64
    manpages-dev
    libk5crypto3:amd64
    glib-networking-common
    xserver-xorg-video-ati
    pcmciautils
    thunderbird-locale-en-us
    gir1.2-peas-1.0
    file
    libgee2:amd64
    libwpg-0.2-2
    empathy
    geoclue
    libavc1394-0:amd64
    linux-image-3.13.0-32-generic
    xfonts-utils
    telepathy-mission-control-5
    ubuntu-sso-client-qt
    liblocale-gettext-perl
    libunity-gtk3-parser0:amd64
    libutempter0
    libbz2-1.0:amd64
    gir1.2-accounts-1.0
    python3-checkbox-support
    compiz-core
    dconf-cli
    libgexiv2-2:amd64
    network-manager-pptp-gnome
    debconf
    python-six
    libtotem-plparser18
    sysv-rc
    cups-common
    libnm-glib4
    libisccfg90
    fonts-tlwg-typewriter
    python3-pkg-resources
    resolvconf
    vim-tiny
    liblouis-data
    network-manager
    libsystemd-daemon0:amd64
    kerneloops-daemon
    libdbusmenu-qt5:amd64
    libxmuu1:amd64
    libglibmm-2.4-1c2a:amd64
    empathy-common
    unity-scope-chromiumbookmarks
    libatk-adaptor:amd64
    libwpd-0.9-9
    libgl1-mesa-glx:amd64
    anacron
    iw
    libfile-desktopentry-perl
    xserver-xorg-video-trident
    gnome-terminal
    libdrm-intel1:amd64
    libexiv2-12
    libunity-action-qt1:amd64","nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
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
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable","1:0.196.12
    1.6-3ubuntu2.14.04.1
    3.52-1
    3.4.3-1ubuntu1
    2.20.1-5.1ubuntu20.1
    7.1-10build1
    2.4.52-1
    4.4.2-7
    1:0.4.4-1
    1.54.0-4ubuntu3.1
    3.3.3-7ubuntu3
    2.3.21-2
    2.1.1+repack0-1ubuntu1
    2.4.2-1.7ubuntu1
    2.82-1.1ubuntu3.1
    4.8.2-19ubuntu1
    0.92.37.1
    3.10.1-1ubuntu4
    1.5.0.is.1.5.0.20130419-2
    1:7.2d-5ubuntu2
    1.7-24
    1:0.5.1-3
    1.6~git20131207+dfsg-1ubuntu1
    0.16-0ubuntu1
    3.10.3-0ubuntu10.1
    2.7.6-8
    2.02~beta2-9ubuntu1
    0.6.0-0ubuntu4
    0.2.1
    1.3.1-1ubuntu1
    1.12+dfsg-2ubuntu4
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    0.4.1
    2.14.1-0ubuntu3.2
    1.10-2ubuntu1
    2.53
    0.8.8-1build1
    3.8.0-2
    3.2.21-1
    1.0.6-2build1
    2:4.1.6+dfsg-1ubuntu2.14.04.2
    1:3.10.1-0ubuntu1
    0.5.1+14.04.20140409-0ubuntu1
    2.4+20121230.gitdf6c518-1
    5.2.1+dfsg-2ubuntu2
    1:3.10.2-1
    1.2.3-1ubuntu1
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    3.10.4-0ubuntu1.1
    1.1.8-1ubuntu2
    1.4.0-1ubuntu1
    1:3.13-1
    2.1.25.dfsg1-17build1
    3.12.0-2
    1.2~rc1.1-1ubuntu1
    5.7.2~dfsg-8.1ubuntu3
    1:4.2.6.3-0ubuntu1
    1.6.0-2
    5.9+20140118-1ubuntu1
    1:3.10.1-0ubuntu9.3
    0.6.35-0ubuntu7
    1.31build1
    0.26-1ubuntu4
    0.23+14.04.20140428-0ubuntu1
    3.54ubuntu1
    0.5.3-2
    1.2.0-2build2
    0.8.13-5
    1.5.5-1ubuntu3
    5.0-2ubuntu2
    6.9.0+13.10.20131011-0ubuntu1
    0.18.3.1-1ubuntu3
    0.4.1-0ubuntu1
    1.20.1-1ubuntu1
    0.8.12-1ubuntu5
    1:2.0.21-1ubuntu2
    3.10.8-0ubuntu1.1
    4:4.8.2-1ubuntu6
    0.13.2-1
    0.1+14.04.20140408-0ubuntu1
    2:3.15.4-1ubuntu7
    2.3.3.4-4build1
    0.0.15-1ubuntu1
    3.10.4-0ubuntu1.1
    0.06-7
    2013.02.13-1ubuntu1
    1.20140128-1ubuntu8
    5.2.1-1
    0.7.6-1ubuntu3
    1.7.2-0ubuntu1.1
    3:20121221-4ubuntu1.1
    1.1.1-1ubuntu5
    0.1.9-0ubuntu2
    2.12-2
    14.04.5
    0.7.47.2ubuntu4.1
    7.35.0-1ubuntu2
    2.0.1-2build2
    10.1.3-0ubuntu0.1
    0.24-0ubuntu7
    0.85-2
    7.19.3-0ubuntu3
    2.40.0-2
    1:4.0-0ubuntu11
    3.10.1-1ubuntu4
    3.4.0-2ubuntu1
    1:2013.1.13AR.1-2ubuntu2
    1:0.220.2
    1:7.7+1ubuntu8
    1.0.1-1
    2.10.0-2ubuntu2
    2.2-1
    1.10-2ubuntu1
    0.13+nmu2
    14.04.0.1-0ubuntu1
    0.23+14.04.20140428-0ubuntu1
    2:1.02.77-6ubuntu2
    3.0.2-0ubuntu2
    1:4.2.6.3-0ubuntu1
    9.10~dfsg-0ubuntu10.2
    4.8.2-19ubuntu1
    20070829-4ubuntu3
    19+svn20140130-1
    2.12-1
    1.70ubuntu8
    1.03+dfsg-1
    3.4.7-0ubuntu3
    1.09-6ubuntu1
    1.2.4-1~ubuntu1
    1.1.8-1ubuntu2
    0.2.6-0ubuntu1
    5.0+svn11846-7
    1:5.16.1-1ubuntu3
    3.1.0daily13.06.05-0ubuntu1
    3.12.1-0ubuntu1
    2.44.2-1ubuntu2
    2.0.0+svn315-2fakesync1
    0.24.5-2ubuntu4
    0.20.0-1
    0.10-6
    1.9.9.5+20130622git7de15e7a-1ubuntu1
    204-5ubuntu20.3
    1.1.1+dfsg.1-3.2
    1.0.25+dfsg-0ubuntu4
    1.20.1-1ubuntu1
    14.04.0+14.04.20140606-0ubuntu1
    13.10.1+14.04.20140410-0ubuntu1
    0.4.6-4
    0.2.56.1
    0.5-0ubuntu2
    13.10-0ubuntu6
    0.8.1-1build1
    0.17-36build2
    1.7.2-0ubuntu1.1
    0.6.5
    0.18.3.1-1ubuntu3
    1.10.1-0ubuntu1
    6ubuntu1
    1.0.27.2-3ubuntu7
    2.2.3.dfsg.1-2ubuntu1
    13.04
    2.14.1-0ubuntu3.2
    7.1-1
    0.9.0-0ubuntu5
    1.12.1-0ubuntu4.2
    0.4.1-3ubuntu4
    1.5.3-2ubuntu4
    1:4.0-0ubuntu11
    4.2.2-4ubuntu1
    3.10.2-0ubuntu1
    2:1.7.1.901-1ubuntu1
    2:4.1.6+dfsg-1ubuntu2.14.04.2
    1.4.3+20140219-0ubuntu2.1
    2.11.0-0ubuntu4.1
    0.12.99-3ubuntu1
    4.2.4-7ubuntu12
    2.3.1-3
    0.9.1-1
    1.60-25ubuntu2
    3.21-0ubuntu1
    7.4.4-1ubuntu2
    1:3.10.1-0ubuntu2
    30~pre9-8ubuntu1
    0.9.14-0ubuntu4
    1:8.31-2ubuntu2
    1.36.3-1ubuntu1
    0.8-2build1
    0.6.0-0ubuntu4
    4.1+Debian11ubuntu6
    1.7.2-0ubuntu1.1
    0.105-4ubuntu2
    0.6.31-4ubuntu1
    0.1+14.04.20140304-0ubuntu1
    1.4.16-1ubuntu2.1
    0.5-0ubuntu2
    1:1.0.3-1
    2.20.1-5.1ubuntu20.1
    0.154.1
    0.7.6-1ubuntu3
    0.105-1ubuntu4
    1.10.0-3
    0.98.2-0ubuntu2
    0.1.21+nmu2ubuntu2
    4.10.4+dfsg-1ubuntu1
    3.14.3-0ubuntu3.2
    0.15.4-1
    2:1.1.1-1
    1.2.12-1
    2.24.23-0ubuntu1.1
    1:1.0.10-1ubuntu2
    0.9.23-2ubuntu1
    0.1.7~+14.04.20140211.2-0ubuntu4
    0.1.7~+14.04.20140211.2-0ubuntu4
    0.83-4.1ubuntu1
    1.2.4-1~ubuntu1
    1.2.12-1
    0.52.15-2ubuntu5
    1.3-0ubuntu2.1
    3.8.4-0ubuntu3
    32.0+build1-0ubuntu0.14.04.1
    3.0.2-0ubuntu2
    0.1.17
    3.8.6-0ubuntu9.1
    1.5-2.1
    2:1.0.10-1
    2.6.1-4build1
    3.10.4-0ubuntu1.1
    1:3.2.1-1ubuntu5
    1:1.7-1
    2.8.6-3ubuntu2
    2.3.2-0ubuntu7
    14.04.4
    6.9.0+13.10.20131011-0ubuntu1
    1.7.2-0ubuntu1.1
    1.5.5-1ubuntu3
    2:2.99.910-0ubuntu1
    6.8.2+14.04.20131029.1-0ubuntu1
    1.4p5-41
    1.3.2-1.3ubuntu1
    1.8.3-12build1
    1.3.3-17ubuntu2
    3.9.90-0ubuntu12
    1.16-8ubuntu1
    1.2.4-1ubuntu1
    0.16-0ubuntu1
    0.03-1fakesync1
    3.10.4-0ubuntu1.1
    1.0.0-4ubuntu3
    1.2.16-2ubuntu1
    1.900.1-14ubuntu3
    2:4.1.6+dfsg-1ubuntu2.14.04.2
    3.13.0.32.38
    12.10.5+14.04.20140410-0ubuntu1
    0.8.0-3
    27~rc1-1
    3.10.3-0ubuntu1
    2.9-0ubuntu0.14.04.1
    1.16.4-0ubuntu2
    0.4+14.04.20140317-0ubuntu1
    2.3.1-2
    0.5.1-2
    458-2
    39-g4717841-3
    0.4.4ubuntu1
    1.16.2-1
    2.4.52-1
    1.40.0-1ubuntu0.1
    2.8.6-3ubuntu2
    1:7.7+1ubuntu8
    0.18.0-0ubuntu4.1
    3.10.1-0ubuntu1
    3.0.2-0ubuntu2
    1.0.2-2ubuntu1
    1.1.2-1ubuntu2
    0.9.3+14.04.20140314-0ubuntu1
    1:1.1.16-1
    1.0.0-4ubuntu3
    0.9.8.8-0ubuntu4.2
    3.5.25.4-3
    2.24.0-3ubuntu3
    1.4.4-3ubuntu2
    0.4.11-0ubuntu4
    0.10.36-1.1ubuntu2
    1.0.2+14.04.20131125-0ubuntu2
    0.1+13.10.20130927.1-0ubuntu1
    2.80-2
    1:7.3.0-1ubuntu3.1
    1.8.8-1ubuntu5
    3.81-8.2ubuntu3
    1:6.6p1-2ubuntu2
    0.8-1
    3.1.2-7ubuntu2
    1:1.5.2-1build1
    2.68-1
    7.7+1
    0.9.8.8-0ubuntu7
    7.7+1
    1.20.1-1ubuntu1
    0.24-1ubuntu4.1
    52.1-3
    1.0.0-2ubuntu1
    3.2.6-0ubuntu2
    1:0.5.1-3
    10.1.3-0ubuntu0.1
    2.28.6-12build1
    14.01-0ubuntu3
    20120503-4
    1:7.7+1ubuntu8
    0.9.8.8-0ubuntu4.2
    2.8.95~2430-0ubuntu5
    2.0.8-1build1
    2.7.5-1ubuntu1
    1.12+dfsg-2ubuntu4
    1.0.1ubuntu2.1
    1:4.2.1-0ubuntu1
    20110808-3ubuntu2
    1.20.1-1ubuntu1
    0.1.8-7
    2:1.1.3-1
    1:1.0.8-1
    1:1.2.8-1build1
    2.88dsf-41ubuntu6
    1:6.6p1-2ubuntu2
    1.15.5-1ubuntu1
    1:3.10.1-0ubuntu9.3
    0.4.0-4
    0.14-2ubuntu1
    1.2.0-2build2
    3.10.1-1ubuntu1
    1.7.1-1build1
    0.80-0ubuntu6
    0.5.2ubuntu4
    0.7.3-1ubuntu5
    3.10.8-0ubuntu1.1
    5.9+20140118-1ubuntu1
    1.10-2ubuntu1
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    0.16.2-1ubuntu1
    0.6.31-4ubuntu1
    297-1ubuntu1
    1.325
    2.40.0-1
    1:3.3.4-2ubuntu1
    3.3-1ubuntu1
    3.10.8-0ubuntu1.1
    1.6.18-0ubuntu4.1
    4.2.4-0ubuntu2
    3.8.0-1ubuntu1
    0.1.6build1
    1.10-2ubuntu1
    2:1.15.1-0ubuntu2
    1.0.6-5
    0.83-4.1ubuntu1
    1:0.5.14ubuntu1
    0.1+13.10.20130723-0ubuntu1
    3.8.0-1ubuntu1
    3.10.1-1ubuntu4
    2.10.0-2ubuntu2
    4.0.6+14.04.20140409-0ubuntu1
    5.1.1alpha+20120614-2ubuntu2
    1.47.11-1ubuntu1
    7.1.4+14.04.20140210-0ubuntu1
    2:1.02.77-6ubuntu2
    0.1.46+14.04.20140408.1-0ubuntu1
    3.10.4-0ubuntu1.1
    1:6.6p1-2ubuntu2
    1.0.0-2ubuntu1
    7.1-10build1
    2.1.0-1
    3.0-1build1
    3.10.1-0ubuntu2
    0.2.24.6
    1.10daily13.06.25-0ubuntu2
    0.1+13.10.20130809.1-0ubuntu1
    13.10-0ubuntu6
    0.2.8.4-10.3ubuntu1
    1.1.1-2
    3.8.6-0ubuntu9.1
    4.9-20140406-0ubuntu1
    1:0.5.1-3
    5.2.1+dfsg-1ubuntu14.2
    3.0.0+14.04.20140416-0ubuntu1
    1:4.2.4-0ubuntu2
    0.92.37.1
    0.9.8.8-0ubuntu7
    0.4.3-2build1
    2.1.0-1
    2.40.0-2
    0.9.3.5
    0.2.7+14.04.20140305-0ubuntu1
    3.2.6-0ubuntu2
    1:4.2.6.3-0ubuntu1
    0.60.7~20110707-1ubuntu1
    1:4.1.5.1-1ubuntu9
    1.2.4-0ubuntu1
    3.1.2-1
    2:4.1.6+dfsg-1ubuntu2.14.04.2
    1:0.9.6-2build1
    0.9.23-2ubuntu1
    0.0.2-4ubuntu1
    1.12+dfsg-2ubuntu4
    3.14.3-0ubuntu3.2
    0.12.ds-1build4
    13.10.1+14.04.20140410-0ubuntu1
    1.26-1
    2.1.5+deb1+cvs20081104-13.1
    1.3.2-6ubuntu2
    5.2.1-3ubuntu15.1
    1:9.9.5.dfsg-3
    1:5.14-2ubuntu3.1
    3.10.0-0ubuntu1
    0.7.3-4ubuntu5.1
    3.13.0.32.38
    0.1+13.10.20130723-0ubuntu1
    2.4.31-1+nmu2ubuntu8
    2.14.1-0ubuntu3.2
    1:1.1.4-1
    0.20+bzr141-0ubuntu4
    0.34-1
    2.32.0+dfsg-3
    0.68-1.2build1
    2.8.95~2430-0ubuntu5
    13.10.0+14.04.20140423-0ubuntu1
    2.2.52-1
    1:31.0+build1-0ubuntu0.14.04.1
    0.4-3
    3.10.4-0ubuntu4
    3.10.4-0ubuntu1.1
    0.6.8-2ubuntu1
    8.56+14.04.20140307-0ubuntu2
    5.9+20140118-1ubuntu1
    0.10.36-1.1ubuntu2
    4.4
    1.5.51ubuntu2
    3.54-1ubuntu1
    0.2.2-1
    1.2.4-1~ubuntu1
    3.0.2-0ubuntu2
    Version
    1.0.3-1
    1.5.5-1ubuntu3
    1.0.25-7ubuntu2
    0.6.31-4ubuntu1
    0.0.0+14.04.20140403-0ubuntu1
    0.4.1-1ubuntu1
    1.10.0-1ubuntu3
    0.0.6-1ubuntu2
    8.6.1-4ubuntu1
    5.1.1-1
    3.4.0-2ubuntu1
    2.2.16+14.04.20140303-0ubuntu1
    0.30-0ubuntu3
    1.20.1-1ubuntu1
    2:1.1.4-1
    0.1.2-1ubuntu3
    8.6.0+6ubuntu3
    3.10.0-0ubuntu1
    2:4.1.6+dfsg-1ubuntu2.14.04.2
    0.2.16+r359+14.04.20131129-0ubuntu1
    3.8.6.1-0ubuntu11.2
    7.1.0+13.10.20130920-0ubuntu1
    1:2.30.7-0ubuntu4
    0.1+13.10.20130927.1-0ubuntu1
    1.3.0-2
    1.0.52-0ubuntu1.2
    1.1.1-1ubuntu5
    2.6-1build1
    4.10.4+dfsg-1ubuntu1
    1:4.2.6.3-0ubuntu1
    1:31.0+build1-0ubuntu0.14.04.1
    2:0.1.12-23.3ubuntu1
    1:1.21.0-1ubuntu1
    8.56+14.04.20140307-0ubuntu2
    0.6.1-1
    1.2-0ubuntu3
    1.6~git20131207+dfsg-1ubuntu1
    5.7.2~dfsg-8.1ubuntu3
    3.10.2.1-0ubuntu4.1
    1.4.1-13ubuntu0.1
    0.05-1build4
    2.7.6-8
    0~git20131104-1.1
    4.20-1.1ubuntu8
    1.13.0~20140204-0ubuntu1
    1.0.0-0ubuntu4
    2013.20130729.30972-2build3
    1:2.24-0ubuntu2
    3.12.0-1
    0.4.11-0ubuntu4
    2.5.0daily13.06.05-0ubuntu1
    2.02~beta2-9ubuntu1
    1.7-5build2
    2.4.17+14.04.20140416-0ubuntu1
    0.11-3ubuntu1.2
    2.2.52-1
    0.24.5-2ubuntu4
    0.3.0+14.04.20140415-0ubuntu1
    5.1.2-3.6ubuntu1
    0.5.3-2
    12.10.3+14.04.20140612-0ubuntu1
    0.14.1-1
    3.12.0-1
    3.10.1-1ubuntu4
    0.3.4-0ubuntu1
    0.18.3.1-1ubuntu3
    0.8+14.04.20131204-0ubuntu1
    1.30-7
    3.14.3-0ubuntu3.2
    0.18.2-1
    0.35-8build1
    14.04+14.04.20140410-0ubuntu1
    0.1+13.10.20130723-0ubuntu1
    7.2.2+14.04.20140714-0ubuntu1
    0.1.4-1
    1.2.4-1~ubuntu1
    1:4.2.6.3-0ubuntu1
    5.2.1-3ubuntu15.1
    0.9.5-1ubuntu5
    1.10-2ubuntu1
    1.25-2
    4.101-0ubuntu13
    1.6.1-1
    0.11-3ubuntu1.2
    1.7.2-0ubuntu1.1
    2.3.0-1ubuntu3
    1:2.4.47-1ubuntu1
    0.83-4.1ubuntu1
    204-5ubuntu20.3
    1:14.04+20140707
    0.142
    3.8.1-0ubuntu1
    2.02~beta2-9ubuntu1
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    0.0.0+14.04.20140403-0ubuntu1
    12.10.1+13.10.20130920-0ubuntu4
    0.8
    1.0.0-4ubuntu3
    1.0.14.1-0ubuntu2
    1.06.95-8ubuntu1
    5.18.2-2ubuntu1
    2.2.2-1ubuntu0.1
    2.5-0ubuntu4
    4.2.4-0ubuntu2
    2.2-1
    0.8.8-0ubuntu17
    2.10.2-2ubuntu1
    1:0.34.9-1ubuntu1
    1:9.9.5.dfsg-3
    3.14.3-0ubuntu3.2
    1.4.3+20140219-0ubuntu2.1
    1.965-1ubuntu1
    3.4.0-0ubuntu2
    0.1.3+14.04.20140317-0ubuntu1
    1.3.4-0ubuntu1
    1:6.6p1-2ubuntu2
    0.92-1
    1:4.0-0ubuntu11
    0.46-1ubuntu7
    2.24.23-0ubuntu1.1
    0.3ubuntu12
    14.04+14.04.20140604-0ubuntu1
    1.0.0-0ubuntu4
    2.19-0ubuntu6
    3.6.1-2ubuntu1
    3.10.1-1
    0.6.31-4ubuntu1
    1.9-2
    5.4-0ubuntu1
    1.2.4-1~ubuntu1
    1.2.50-1ubuntu2
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    2014e-0ubuntu0.14.04
    3.8.0-1build1
    2.0.3-0ubuntu1
    0.3.15+13.10.20130920-0ubuntu1
    2.19-0ubuntu6
    1.1.28-2build1
    2.28.5-2
    3.10.0-1ubuntu3
    2.9.2-4ubuntu4
    0.82.1ubuntu2
    1.0.2-4.1ubuntu1
    1:2.3.7-2ubuntu2
    1.54.0-4ubuntu3.1
    1:4.2.6.3-0ubuntu1
    14.04+14.04.20140410-0ubuntu1
    0.2.3-1ubuntu2
    3.10.1-1ubuntu4
    2:102.6+LibO4.2.4-0ubuntu2
    8.6.1-3ubuntu2
    0.1+13.10.20130723-0ubuntu1
    0.6.31-4ubuntu1
    1.1.8-1ubuntu2
    3.10.2-0ubuntu1
    0.9.3.5
    4.5.1-2ubuntu1
    1:0.9.8-1
    1.0.52-0ubuntu1.2
    0.6.31-4ubuntu1
    1.9.4-1
    0.0.9-8ubuntu1
    1:14.04+14.04.20140410-0ubuntu1
    0.12
    1.1.1-1ubuntu5
    1:0.5.1-3
    1.7.2-7
    12.10.6+14.04.20140411-0ubuntu1
    1.16.4-0ubuntu2
    0.3-2
    7.1.4+14.04.20140210-0ubuntu1
    4.8-1ubuntu5
    3.0-1build1
    0.8-1
    0.9.35+14.04.20140213-0ubuntu1
    1.3.0-2
    30~pre9-8ubuntu1
    0.1+14.04.20140403-0ubuntu1
    2.4.0-6
    1.60-1
    1.2.7+14.04.20140324-0ubuntu1
    1.0.23-3ubuntu3.1
    10.1.3-0ubuntu0.1
    2.2.10-0.2ubuntu2
    4.8.2-19ubuntu1
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    0.3.7+14.04.20140303-0ubuntu1
    1:4.2.1-3ubuntu1
    1.5.2-1
    1:3.6.3-0ubuntu56.1
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    1.3.4-0ubuntu1
    10.1.3-0ubuntu0.1
    1:1.0.2-1ubuntu1
    1:0.4.18-1ubuntu1
    3.10.3-0ubuntu10.1
    0.23+14.04.20140428-0ubuntu1
    2.3.6+13.10.20130920.1-0ubuntu1
    3.10.3-0ubuntu10.1
    3.8.6-0ubuntu9.1
    0.5.1-2
    0.16.2-1ubuntu1
    14.04.10-0ubuntu1
    1:204-5ubuntu20.3
    3.0.2-0ubuntu2
    2:3.63+dfsg-2ubuntu5
    2:1.0.8-1ubuntu1
    0.4.0-4
    1.4.21-1ubuntu1
    1.0.0~bzr501-0ubuntu2
    0.1+14.04.20140328-0ubuntu1
    1.07.3-3
    0.04-1build3
    1:3.3.9-1ubuntu2
    0.249-1
    1.70-1
    2.12.23-12ubuntu2.1
    1:3.2.1-1ubuntu5
    5.2.1-3ubuntu15.1
    2.44.2-1ubuntu2
    0.2.9-2ubuntu1
    0.100.2-1
    2.6.1-4build1
    12.10.3+14.04.20140612-0ubuntu1
    0.105-4ubuntu2
    3.8.0-2
    1.10.0+dfsg-3ubuntu2
    2.1.0-4ubuntu1
    1.0.6-2build1
    1:14.04+20140707
    0.6+14.04.20140307-0ubuntu1
    0.12.2-1
    7.1.4+14.04.20140210-0ubuntu1
    1:9.9.5.dfsg-3
    0.0.1+14.04.20140401-0ubuntu1
    0.3.2-3
    0.4.1-0ubuntu1
    2.28.1+dfsg-1ubuntu2
    0.30-0ubuntu3
    5.2+dfsg-2
    2.12.23-12ubuntu2.1
    1.6-3ubuntu1
    6-2bzr1
    0.0.6+14.04.20140207-0ubuntu2
    3.10.1-1ubuntu4
    1.0.27-2ubuntu2
    2:1.2.2-1ubuntu2
    1.0.33
    0.8.8-0ubuntu17
    1:4.9-20140406-0ubuntu1
    1.3.2-1.3ubuntu1
    0.10.36-1.1ubuntu2
    1.7.2-0ubuntu1.1
    5.2.10~pre2-0ubuntu2
    0.45ubuntu4
    1:2.8.2-1ubuntu2
    0.24.5-2ubuntu4
    0.5.7-4ubuntu1
    1.6~git20131207+dfsg-1ubuntu1
    1.11+14.04.20140410.1-0ubuntu1
    1:204-5ubuntu20.3
    1.20.4-6.1
    0.3.1-4fakesync1
    0.7.5-0ubuntu2
    0.1+13.10.20130723-0ubuntu1
    1.0.0-4ubuntu3
    0.8-4ubuntu2
    1.0.6-1
    0.2.7-2ubuntu1.1
    1.40.0-1ubuntu0.1
    1.3.2-1.3ubuntu1
    5.2.1-3ubuntu15.1
    4.8.2-19ubuntu1
    7.1-1
    2.02~beta2-9ubuntu1
    5.2.1+dfsg-1ubuntu14.2
    4.15.5-1build1
    1.4.0-1ubuntu1
    2.10.0-2ubuntu2
    1.7.1-1build1
    0.9.7-0ubuntu14
    0.2.8.4-10.3ubuntu1
    1.20.1-1ubuntu1
    0.6.1-0ubuntu3
    0.19+14.04.20140305-0ubuntu2
    0.25-1
    1.42.9-3ubuntu1
    0.9.7-10
    1.7.2-0ubuntu1.1
    0.30-0ubuntu3
    5.2.10~pre2-0ubuntu2
    2.82-1.1ubuntu3.1
    2:1.6.2-1ubuntu2
    0.12
    1.0.0-6
    1.27.1-1
    0.2.56.1
    0.60.7~20110707-1ubuntu1
    1.0.52-0ubuntu1.2
    2:1.6.2-1ubuntu2
    2.1-0ubuntu1
    1:0.5.14ubuntu1
    1:9.9.5.dfsg-3
    2.3.19ubuntu1
    0.1.21+nmu2ubuntu2
    2.06-1.2ubuntu1
    0.4.2-13.1ubuntu3
    3.10.1-1
    1.10.1-0ubuntu1
    0.1.1~daily20130301-0ubuntu1
    2.23-1
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    2.10.2.is.2.10.1-0ubuntu1
    3:4.05+dfsg-6+deb8u1
    1.0.23-3ubuntu3.1
    12.10.1+14.04.20140407-0ubuntu1
    2.5.3-2ubuntu1
    1:4.2.6.3-0ubuntu1
    0.3ubuntu12
    8.56+14.04.20140307-0ubuntu2
    2.40.2-1
    7.1-0-1
    3.10.3-0ubuntu1
    0.7.5-0ubuntu2
    0.4.1-0ubuntu1
    3.8.7-1ubuntu1
    0.1+14.04.20140328-0ubuntu1
    0.2.5-0ubuntu1
    3:20121221-4ubuntu1.1
    2.19-0ubuntu6
    1:2.3.3-1build1
    0.0.0+14.04.20140403-0ubuntu1
    0.22-1
    0.1+14.04.20140408-0ubuntu1
    1.9.1-2
    1.0.1ubuntu2.1
    5.0~git20130529-0ubuntu3
    0.1+13.10.20130723-0ubuntu1
    5.2.1+dfsg-1ubuntu14.2
    12.10.2+14.04.20140401-0ubuntu1
    5.2
    3.8.0-2
    1.7.2-0ubuntu1.1
    1:4.2.4-0ubuntu2
    1:3.5.10-1
    3.2.21-1
    1.16.2-1
    4.8.2-19ubuntu1
    0.2.24.6
    30.0-0ubuntu4
    2.2.1-1ubuntu1
    5.1.1-1
    1:1.6.3-1build1
    3.10.3-0ubuntu1
    1:0.5.1-3
    2.01+mry-10
    5.0-2ubuntu2
    1.1.6-20-g1b9f164-1ubuntu2
    0.70-1
    1.19-2
    2:1.0.7-1
    3.1-20130712-2
    1.8.1-2ubuntu2
    1.0.0~bzr501-0ubuntu2
    0.4.11-0ubuntu4
    0.5-1ubuntu1
    3.10.2-0ubuntu2
    1.28-1ubuntu2
    3.2.6-0ubuntu2
    1.0.3-3ubuntu1
    2.0.21-stable-1ubuntu1
    3.8.2-1ubuntu2
    0.10.31-3+nmu1ubuntu5
    0.1.2+14.04.20131108.1-0ubuntu1
    1:4.2.1-0ubuntu1
    1:3.10.2-0ubuntu1.1
    2.11+dfsg-1ubuntu1
    13.2.0-1ubuntu1
    2.3.3.4-4build1
    1.325
    7.2.2+14.04.20140714-0ubuntu1
    2.4.5-5.1ubuntu2
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    3.10.0-0ubuntu1
    3.15ubuntu1
    1:3.12.0-2
    1.1.0+14.04.20140325.3-0ubuntu1
    20140410-0ubuntu1
    1.6.0-10ubuntu1
    1.1.1-1ubuntu5
    6.8.2+14.04.20131029.1-0ubuntu1
    1.36.3-1ubuntu1
    0.23+14.04.20140428-0ubuntu1
    1:1.4.7-1ubuntu0.1
    3.3.3-1ubuntu0.1
    2.3-19ubuntu1
    0.9.32-1
    3.1~rc1+r3.0.13-12
    2.11.0-0ubuntu4.1
    2.19-0ubuntu6
    0.3.9-1ubuntu1
    0.1+14.04.20140304-0ubuntu1
    0.6.35-0ubuntu7
    8.6.1-3ubuntu2
    0.10-1
    6.9.4-1build1
    1.6~git20131207+dfsg-1ubuntu1
    20140327-1
    22.20-1ubuntu2
    0.18.3-0ubuntu0.1
    1.0+14.04.20140318-0ubuntu1
    1.01-3
    2.7.6-8
    4.8.2-19ubuntu1
    0.8.8-0ubuntu17
    3.10.1-1ubuntu4
    2.1.3-1
    0.0.31-1ubuntu2
    0.16-0ubuntu1
    0.9.27-1
    0.5.0ubuntu2
    8.6.0+6ubuntu3
    2.9.24-0ubuntu1
    4.101-0ubuntu13
    1:2.20.1-5.1ubuntu20.1
    0.35.0+20060710.1
    3.0.26-1
    2.4.3-1ubuntu2
    1.42.9-3ubuntu1
    7.6.q-25
    3.8.2.1-0ubuntu4
    3.9.90-0ubuntu12
    2:4.10.2-1ubuntu1.1
    2.5ubuntu2
    3.6.1-0ubuntu13
    2.11.0-0ubuntu4.1
    1:4.2.4-0ubuntu2
    13.01.0+14.04.20140404-0ubuntu1
    3.0-8
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    0.5.1-7
    3.10.2-0ubuntu2
    0.3.15+13.10.20130920-0ubuntu1
    3.6.3build2
    1.2.16-2ubuntu1
    0.22-1ubuntu1
    0.8.0-3
    3.10.2-0ubuntu5
    1.36.3-1ubuntu1
    31.0+build1-0ubuntu0.14.04.1
    0.9.9.9-4
    0.8-2build1
    1:2.10.9-0ubuntu3.1
    02.16-2ubuntu1
    0.3-2
    7.35.0-1ubuntu2
    3.10.0-1ubuntu2
    0.11+14.04.20140409.1-0ubuntu1
    0.8-5ubuntu1
    3.0027+nmu1
    0.103ubuntu4.2
    3.10.1-1ubuntu4
    3.10.1-0ubuntu1
    1:4.2.4-0ubuntu2
    5.2.1-1ubuntu2
    0.12.4-0nocelt2
    15-0ubuntu6
    0.0.0+14.04.20140410.1-0ubuntu1
    0.13
    1.10daily13.06.25-0ubuntu2
    3.4.0-2ubuntu1
    3.10.1-1
    0.6.23-1ubuntu4.1
    1.0.6-1
    3.4.0-2ubuntu1
    0.8.0-1
    1.5.5-1ubuntu3
    1.20.1-1ubuntu1
    2.30.7-0ubuntu1
    20140209dfsg0-1ubuntu1
    3.8.2.1-0ubuntu4
    0.1+13.10.20130723-0ubuntu1
    1:5.0.1-1ubuntu1
    1.1.1-1ubuntu5
    1.13+nondbs-0ubuntu4
    1.76-4
    1:4.2.1-0ubuntu1
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    0.9.8.2-1ubuntu2
    1.1.24+nmu2ubuntu3
    204-5ubuntu20.3
    0.05-1
    1:1.0.4-1ubuntu1
    5.2.1+dfsg-1ubuntu14.2
    2.7.6-8
    2.0.1+dfsg1-1build1
    2.1.1-1ubuntu1
    2.5.0~+14.04.20140409-0ubuntu1
    1.15+14.04.20131126.2-0ubuntu3
    5.2.1-1
    2.7.1-4ubuntu1
    2.20.1-5.1ubuntu20.1
    2.3.1-93ubuntu1
    3.8.2.1-0ubuntu4
    0.7.90-0ubuntu1
    0.11+20120125-1ubuntu1
    3.10.4-0ubuntu1.1
    1.0.1-2
    1.2.0-0.1ubuntu3
    3.4.0-0ubuntu2
    7.6.q-25
    0.10.5-1ubuntu1
    2.34-1ubuntu1
    1.9.1-2
    2.4.3-1ubuntu2
    1.0.1-4
    3.0pl1-124ubuntu2
    2.1.0-1ubuntu1
    0.10.36-1.2ubuntu3
    1.42.9-3ubuntu1
    1.7.2-0ubuntu1.1
    2.44.2-1ubuntu2
    1.1-2
    0.30-0ubuntu3
    1.2.4-0ubuntu1
    5.5.0.13-7build1
    1:4.2.6.3-0ubuntu1
    0.7
    0.9.14-0ubuntu4
    3.10.2-0ubuntu1
    10.1.3-0ubuntu0.1
    2012.05.19
    0.187ubuntu1
    1.105-7ubuntu1
    3.10.1-1
    8.56+14.04.20140307-0ubuntu2
    0.3.7
    1:1.1.16-1
    2.1500-1
    3.13.0-32.57
    1.58-1
    1.1.1-1ubuntu5
    2.1.25.dfsg1-17build1
    1.12ubuntu2
    2.10.2.is.2.10.1-0ubuntu1
    1.6~git20131207+dfsg-1ubuntu1
    10.1.3-0ubuntu0.1
    1:3.10.2-0ubuntu3.1
    1.36.3-1ubuntu1
    0.1.18-0ubuntu1
    0.9.14-0ubuntu4
    1.0.2-2ubuntu1
    0.18.3.1-1ubuntu3
    0.30.0-1ubuntu1
    2010.09.27
    1.10-1
    4.101-0ubuntu13
    1.1-2ubuntu2
    0.25-4
    0.1.4-1
    3.6.0-0ubuntu2
    5.2.1+dfsg-1ubuntu14.2
    0.18.3.1-1ubuntu3
    3.10.2-0ubuntu2
    12.10.3+14.04.20140612-0ubuntu1
    7.7+2
    5.0~git20130529-0ubuntu3
    1.2.4-0ubuntu1
    2.5.22ubuntu1
    0.9.5-1ubuntu5
    0.14.1-1
    2.28.5-2
    2.4.52-1
    2.88dsf-41ubuntu6
    1.2.4-1~ubuntu1
    2:1.0.12-1
    1:3.10.1-0ubuntu1
    0.0.20060226-9
    1:2.24-0ubuntu2
    13.10-0ubuntu2
    1:007-2ubuntu1
    20140317-1
    0.22.1-1ubuntu2
    1.16.2-1
    0.11+14.04.20140409.1-0ubuntu1
    1.0.52-0ubuntu1.2
    1:4.2.4-0ubuntu2
    12.10.2+14.04.20140402-0ubuntu1
    5.1.1alpha+20120614-2ubuntu2
    9:1.1.11-2ubuntu3
    5.1.314.7778
    3.10.2-0ubuntu1
    3.0.0+14.04.20140416-0ubuntu1
    0.129.2
    3.13.0-32.57
    2.24.23-0ubuntu1.1
    3.12.0-1
    0.19-3
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    1.0.8-2ubuntu1
    1.3.0-1
    1:1.1.14-1
    0.8-5ubuntu1
    1.9.66-0ubuntu2
    1.6.0-1
    0.2.11-12
    0.3.7
    2.14.1-0ubuntu3.2
    2.1-5.4
    0.8.1-1ubuntu3
    20140313-1
    1:0.9.11.2+14.04.20140714-0ubuntu1
    3.10.2-0ubuntu1
    20131007-1
    1:4.2.6.3-0ubuntu1
    1:0.5.1-3
    3.10.4-0ubuntu1.1
    9.43-1ubuntu3
    0.6.31-4ubuntu1
    1.2.0-1ubuntu1
    3.10.1-1ubuntu4
    1.57ubuntu1
    9.10~dfsg-0ubuntu10.2
    1.1+14.04.20140401.1-0ubuntu1
    2.0.8-1build1
    1.1.1-1ubuntu5
    0.20
    2.2.1-1
    2:3.15.4-1ubuntu7
    1.06.95-8ubuntu1
    0.9+13.10.20130723-0ubuntu1
    1.5.0-1ubuntu1
    0.1.20-3
    0.3.8-1.1ubuntu1
    0.30-0ubuntu3
    5.2.0.dfsg.1-2
    1:3.3-1
    4.43
    2.10.2.is.2.10.1-0ubuntu1
    6.3-4ubuntu2
    3.10.0-0ubuntu2
    3.6.0-0ubuntu2
    7.7+1
    20140410-0ubuntu1
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    0.154.1
    2:1.0.8-2
    1.20ubuntu1
    3.12.0-1
    15-0ubuntu6
    13.2.0-1ubuntu1
    1.4+repack0-3
    5.2.1+dfsg-1ubuntu14.2
    1.0.8-2ubuntu1
    3.10.1-1
    8c-2ubuntu8
    2.30.7-0ubuntu1
    0.4.5-3.1ubuntu2
    1.2.3-1ubuntu1
    1:0.5.1-3
    0.36-1
    1.2.0-2build2
    0.2.5build1
    3.14.3-0ubuntu3.2
    2.0-2ubuntu4.1
    1:4.2.6.3-0ubuntu1
    1:2.3.2-2ubuntu1
    0.2.0-1
    1.10-2ubuntu1
    1:2.3.2-2ubuntu1
    3:20121221-4ubuntu1.1
    3.13.0.32.38
    0.19.6-1
    0.20.0-1
    1.901b-5
    0.10.36-1.2ubuntu3
    1:13.0.2-2ubuntu1
    2.9.1-1build1
    0.13-2ubuntu6
    2.4.3-1ubuntu2
    2.40.2-1
    1.4.3+20140219-0ubuntu2.1
    0.10-1ubuntu1
    1:0.6.5-0ubuntu4
    1.0.4-3ubuntu2
    0.3.7
    0.8-0ubuntu10
    1.1.0+14.04.20140325.3-0ubuntu1
    2.7.5-5ubuntu3
    3.10.2-0ubuntu1
    1.0.27.2-1ubuntu2
    5.18.2-2ubuntu1
    3.10.4-0ubuntu1.1
    0.2.2-2ubuntu2
    1:0.8-2ubuntu2
    1:3.10.1-0ubuntu9.3
    1.5.3-2
    1:4.0-0ubuntu11
    2.24-5ubuntu3
    (Status,Err:
    3.5.33
    3.10.0-0ubuntu1
    2:1.0.5-1
    3.10.2-0ubuntu2
    0.92.37.1
    1.6~git20131207+dfsg-1ubuntu1
    1:3.4-1ubuntu3
    3.0.2-0ubuntu2
    1.0.1f-1ubuntu2.4
    4.0.6+14.04.20140409-0ubuntu1
    5.9+20140118-1ubuntu1
    3.10.4-0ubuntu1.1
    1.6~git20131207+dfsg-1ubuntu1
    4.86+dfsg-1ubuntu2
    8.21-1ubuntu5
    1.3-0ubuntu2
    0.18-1build3
    2:5.1.3+dfsg-1ubuntu1
    0.9.3-5ubuntu3
    1.0.1f-1ubuntu2.4
    0.6-3
    1.0.1ubuntu2.1
    2.1.3-1
    1.09-6ubuntu1
    1:0.9.11.2+14.04.20140714-0ubuntu1
    3.8.0-2
    1:0.196.12
    3.1.2-1
    0.17.6-0ubuntu6
    2.16-1
    3.0.2-0ubuntu2
    1.13.0~20140204-0ubuntu1
    3.10.4-0ubuntu1.1
    0.4.6-0ubuntu2
    1:1.0.7-1ubuntu1
    1.2-20130928-1
    1.5.5-1ubuntu3
    1:0.3.3-1build1
    1.36-1ubuntu1
    3.2.6-0ubuntu2
    0.6.1-1
    1.6.18-0ubuntu4.1
    1:0.9.11.2+14.04.20140714-0ubuntu1
    1.15-1ubuntu1
    3.1.0-2ubuntu0.1
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    9.0.0-2
    21-0ubuntu1
    2.3.0-1ubuntu3
    1.192-1
    4.0.3-7ubuntu0.1
    2:1.2.1-2
    0.8.24daily13.06.10-0ubuntu1
    3.8.4-0ubuntu3
    2.2.6-1ubuntu1
    0.9.19-1
    3.13.0-32.57
    2.0.1-1
    1.0-0ubuntu1
    2.7.5-5ubuntu3
    1:1.7.7-2build1
    1.12-0.2ubuntu1
    1.8.9p5-1ubuntu1
    14.04.3+14.04.20140604-0ubuntu1
    1:0.2.91.5
    2.9.1-1build1
    6.3-4ubuntu2
    0.1.29build1
    3.0.2-0ubuntu2
    1.36.3-1ubuntu1
    0.61-1
    5.2.1-3ubuntu15.1
    5.2.1+dfsg-1ubuntu14.2
    0.8-1
    2:1.6.2-1ubuntu2
    1.0.1-1
    1:0.220.2
    6.0-9ubuntu1
    7.1.0+13.10.20131011-0ubuntu2
    3.0+14.04.20140324-0ubuntu1
    12.10.1+13.10.20130920-0ubuntu4
    2.5.3.1-1ubuntu2.2
    0.8.12-1ubuntu5
    1.1.4-1ubuntu1
    3.3.3-1ubuntu0.1
    1:6.6p1-2ubuntu2
    1.4.3-0.1ubuntu5
    1.58-1
    0.1.46+14.04.20140408.1-0ubuntu1
    0.26-1ubuntu1
    1:2.1-4
    0.9.8.8-0ubuntu7
    1:7.7+1ubuntu8
    4.8.2-19ubuntu1
    2.3000-1
    4.2.4-7ubuntu12
    7.7+2ubuntu1
    1.4.0-1ubuntu1
    1:0.5.1-3
    1.0.6-1
    2.5.2-1ubuntu2.2
    0.52.15-2ubuntu5
    2.10.0+dfsg-1
    1:1.21.0-1ubuntu1
    1.7.2-0ubuntu1.1
    3.4.0-2ubuntu1
    1.63ubuntu1
    7.2ubuntu5.1
    1.1.5+git20140313.bafe6a9e-0ubuntu1
    9.0.5ubuntu1
    7.7-0ubuntu3.1
    0.10.5
    1.6.0-10ubuntu1
    5.1-1
    0.2.0+14.04.20140217.1-0ubuntu1
    3.10.4-0ubuntu4
    3.10.3-0ubuntu10.1
    1:1.1.1-1
    3.8.2-1ubuntu2
    2.5.3.1-1ubuntu2.2
    2:4.1.6+dfsg-1ubuntu2.14.04.2
    3.0-1build1
    1:4.2.6.p5+dfsg-3ubuntu2
    3.8.2-1ubuntu1
    1:3.3.9-1ubuntu2
    4.101-0ubuntu13
    1.2.7+14.04.20140324-0ubuntu1
    0.3ubuntu12
    1.0-2ubuntu1
    0.18.3.1-1ubuntu3
    1.1+ds1-10
    1:0.23.0-0ubuntu2
    2:1.15.1-0ubuntu2
    4:4.8.2-1ubuntu6
    2.4.3-1ubuntu2
    1.3-8
    1.4.21-1ubuntu1
    2.9.1+dfsg1-3ubuntu4.3
    2.5.3-2ubuntu1
    1.40.0-1ubuntu0.1
    0.04-7build3
    0.9.14-0ubuntu4
    3.4.7-0ubuntu3
    3.10.1-1
    0.10.31-3+nmu1ubuntu5
    0.1+13.10.20130723-0ubuntu1
    3.9.90-0ubuntu12
    0.15-1ubuntu3
    0.14.1-1
    0.18.0-0ubuntu4.1
    0.10.36-1.1ubuntu2
    0.2.0+14.04.20140217.1-0ubuntu1
    2.19-0ubuntu6
    1.10-2ubuntu1
    1.2.4-1~ubuntu1
    3.8.2-1
    2.10.1-1ubuntu1
    1:1.2.8.dfsg-1ubuntu1
    0.1.1-3ubuntu2
    2.0.13-1
    1:9.9.5.dfsg-3
    1.7.4-0ubuntu1
    2.8.95~2430-0ubuntu5
    1:4.2.6.3-0ubuntu1
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    2.0.9+1-1ubuntu1
    0.13.7ubuntu2
    3.10.3-0ubuntu1
    3.8.2.1-2ubuntu1
    0.1-3
    5.2.1-3ubuntu15.1
    1.2~rc1.1-1ubuntu1
    1.0.1ubuntu2.1
    1:1.1.2-1
    0.20.0-1
    1:9.9.5.dfsg-3
    1:0.4.4-1build1
    1.47.11-1ubuntu1
    1.0.17-1
    0.4.0-5
    0.6.31-4ubuntu1
    1:2.30.7-0ubuntu4
    0.20.2-2ubuntu2
    1:0.10.7-0ubuntu6
    1:4.1.5.1-1ubuntu9
    4.70.0-1
    14.04.1
    7.1.4+14.04.20140210-0ubuntu1
    5.2.1+dfsg-1ubuntu14.2
    1.6~git20131207+dfsg-1ubuntu1
    2.0.4-4
    1:3.6.3-0ubuntu56.1
    3.8.6-0ubuntu9.1
    9.10~dfsg-0ubuntu10.2
    1:4.0-0ubuntu11
    1.0.27.2-3ubuntu7
    2.9.2-4ubuntu4
    0.8.0+real-0ubuntu6
    0.158-0ubuntu5.1
    0.2.16+r359+14.04.20131129-0ubuntu1
    2:1.2.2-1
    2.2.4-15ubuntu1
    3.10.8-0ubuntu1.1
    1.12.1-0ubuntu4.2
    1.7.2-0ubuntu1.1
    0.10-3
    5.2.1+dfsg-1ubuntu14.2
    1.42.9-3ubuntu1
    2.24.23-0ubuntu1.1
    4.0.6+14.04.20140409-0ubuntu1
    1.1.8-1ubuntu2
    0.6
    1.3-10
    1:2.10.9-0ubuntu3.1
    0.129.2
    1:31.0+build1-0ubuntu0.14.04.1
    1.7.2-0ubuntu1.1
    1.56-1
    1.6.18-0ubuntu4.1
    1.1-3
    3.0.2-0ubuntu2
    8.56+14.04.20140307-0ubuntu2
    1.8.1-2ubuntu2
    2:1.4.2-1
    1.1.0~rc1-2ubuntu7.1
    2.2-1
    2:4.1.6+dfsg-1ubuntu2.14.04.2
    0.8.3-4ubuntu3
    4.0.5+14.04.20140115-0ubuntu1
    1.1.6-20-g1b9f164-1ubuntu2
    6.9.2-1build1
    0.9.14-0ubuntu4
    2.6.7.1-1
    0.103ubuntu4.2
    0.9.9+dfsg-1ubuntu1
    3.10.2-0ubuntu1
    0.1+13.10.20130723-0ubuntu1
    1.4.16-1ubuntu2.1
    0.8-5ubuntu1
    1.0.1-1ubuntu1
    3.10.2-0ubuntu1
    1:0.5.1-3
    7.19.3-0ubuntu3
    0.11+14.04.20140409.1-0ubuntu1
    0.3.9-1ubuntu2
    5.2.1-0ubuntu5
    12.10.3+14.04.20140612-0ubuntu1
    3:4.05+dfsg-6+deb8u1
    0.9.8.8-0ubuntu4.2
    0.9.7-0ubuntu14
    3.1-1ubuntu0.1
    2.6.20-0ubuntu1
    2.7.5-5ubuntu3
    None
    0.6.1-0ubuntu1
    2.7.1-1
    1.6~git20131207+dfsg-1ubuntu1
    2.3-19ubuntu1
    4.1+Debian11ubuntu6
    3.13.0-32.57
    2.7.6-8
    1.10-2ubuntu1
    5.1.1-1ubuntu8
    0.0.9
    0.8.3-4ubuntu3
    0.17-28
    3.113+nmu3ubuntu3
    0.11+14.04.20140409.1-0ubuntu1
    1.0.6-2
    0.105-4ubuntu2
    0.11+14.04.20140409.1-0ubuntu1
    0.25-4
    0.9.3.5
    1.26+nmu4ubuntu1
    3.8.6-0ubuntu9.1
    1:13.0.0-1build1
    1.1.6-20-g1b9f164-1ubuntu2
    0.8.8-0ubuntu17
    1:1.4.5-1build1
    3.10.2+debian-11
    0.42-1
    5.9+20140118-1ubuntu1
    1.0.1-1
    1:1.1.4-1ubuntu1
    1:0.5.1-3
    0.1.4-1
    13.10-0ubuntu4.1
    1:2.34.13-0ubuntu4
    0.06~01-2
    1.8.10-1ubuntu1
    1:14.04+20140707
    1.12+dfsg-2ubuntu4
    0.7.3-1ubuntu2
    5.0~git20140203~e0c5eebe-0ubuntu2
    2.5.3.1-1ubuntu2.2
    0.30-0ubuntu3
    0.3.1+14.04.20140411-0ubuntu1
    1:2.34.13-0ubuntu4
    14.04.3+14.04.20140604-0ubuntu1
    0.38-1
    0.5.2ubuntu4
    1:8.11+urwcyr1.0.7~pre44-4.2ubuntu1
    0.1.6-5
    0.14-2build1
    0.3.8-2ubuntu1
    5.2.1-3ubuntu15.1
    0.8.8-0ubuntu17
    1.1.24+nmu2ubuntu3
    0.2.25
    13.10.1+14.04.20140410-0ubuntu1
    0.10.36-1.1ubuntu2
    0.1+13.10.20130723-0ubuntu1
    1.0.1ubuntu2.1
    2.0.9~rc5-1ubuntu2
    3.10.8-0ubuntu1.1
    3.10.4-0ubuntu1.1
    1.0.4-1
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    0.6.31-4ubuntu1
    13.10.0+14.04.20140415.3-0ubuntu1
    1:14.04+20140707
    1:0.34.9-1ubuntu1
    3.8.3-1ubuntu1
    0.12-3ubuntu1
    1.14.0-5ubuntu2
    0.99.beta18-1ubuntu5
    3.2.21-1
    1:1.08-1build4
    0.9.27-1
    2.5.0~+14.04.20140409-0ubuntu1
    10.1.3-0ubuntu0.1
    1.10.0-3
    204-5ubuntu20.3
    1.4.0-1
    0.3.18-1ubuntu2
    1.3.0-0ubuntu2
    4.8.2-19ubuntu1
    1.0.3-4ubuntu25
    1:0.196.12
    5.18.2-2ubuntu1
    2:7.4.052-1ubuntu3
    2.1.25.dfsg1-17build1
    2.20.1-5.1ubuntu20.1
    1.5.5-1ubuntu3
    0.9.5-1ubuntu5
    1:1.0.3
    2.5.0-9ubuntu1
    1.3.2-1
    1.14
    204-5ubuntu20.3
    5.1.1-1ubuntu8
    5.1.3-2
    0.14.7-1ubuntu1
    1.17.5ubuntu5.3
    0.6.21-1ubuntu1
    13.05-0ubuntu1
    1.17.5ubuntu5.3
    2.19-0ubuntu6
    9:1.1.11-2ubuntu3
    2:1.3.2-1
    0.8-5ubuntu1
    0.33-1build3
    0.11+14.04.20140409.1-0ubuntu1
    1:0.5.1-3
    0.1+14.04.20140328-0ubuntu1
    0.17
    0.20.10-1ubuntu1
    2.24.23-0ubuntu1.1
    0.20.2-2ubuntu2
    14.04.0.1-0ubuntu1
    1.0-2ubuntu1
    1.2.4-1~ubuntu1
    None
    3.10.1-0ubuntu2
    1.200-6
    1.10-2ubuntu1
    1:4.2.6.3-0ubuntu1
    1.10-2ubuntu1
    1.22.2-5
    3.4.7-0ubuntu3
    1:7.7+1ubuntu8
    0.1.7+14.04.20140527-0ubuntu1
    2.1.3-1
    1:1.1.3-1
    9.10~dfsg-0ubuntu10.2
    1.10-2ubuntu1
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    5.3.28-3ubuntu3
    2.20.1-5.1ubuntu20.1
    3.4-3ubuntu0.1
    003.02.01-9ubuntu2
    1.2.4-1~ubuntu1
    1.0.3-4ubuntu25
    1:0.220.2
    1.0.23-3ubuntu3.1
    1:4.0-0ubuntu11
    2.1.0-3
    10.1.3-0ubuntu0.1
    3.2.6-0ubuntu2
    2.30.7-0ubuntu1
    1:9.9.5.dfsg-3
    0.1.1~daily20130301-0ubuntu1
    5.0-7ubuntu1
    2.0.3-0ubuntu1
    3.10.1-0ubuntu2
    3.4.3-1ubuntu1
    1.20.5
    4.0.18-1ubuntu1
    4.8.2-19ubuntu1
    4.0.5-1ubuntu4
    5.18.2-2ubuntu1
    20130906ubuntu2
    3.4.0-0ubuntu2
    10.1.3-0ubuntu0.1
    1.0.3+14.04.20140109-0ubuntu1
    0.34~rc-0ubuntu2
    1.0.25+dfsg-0ubuntu4
    1.127.5
    3.5.25.4-3
    5.2.1+dfsg-1ubuntu14.2
    1:1.0.8-1
    0.16+14.04.20140304.is.0.15+14.04.20140313-0ubuntu1
    2.2.1-1
    0.11+14.04.20140409.1-0ubuntu1
    0.18-1build2
    3.0.4-0ubuntu1
    4.8.2-19ubuntu1
    1:4.0-0ubuntu11
    1:3.10.2-0ubuntu1
    4.8.2-19ubuntu1
    3.10.2-0ubuntu1
    1:1.2.2-1
    2.13+git20120306-12.1
    1:0.34.9-1ubuntu1
    0.3.7
    3.10.1-0ubuntu2
    3.4-1build1
    0.2.0+14.04.20140217.1-0ubuntu1
    2.9.1+dfsg1-3ubuntu4.3
    5.2.3-1
    3.10.4-0ubuntu1.1
    0.6.0-2ubuntu1
    13.2.0-1ubuntu1
    1.4.3+20140219-0ubuntu2.1
    0.2.16+r359+14.04.20131129-0ubuntu1
    0.5.1+14.04.20140409-0ubuntu1
    204-5ubuntu20.3
    1.1.0+14.04.20140304-0ubuntu1
    3.8.1-1svn1
    2.34.0-1ubuntu1
    2.22.7-2ubuntu1
    0.3-2
    0.30.2-2ubuntu1
    0.3ubuntu12
    0.30-0ubuntu3
    8.6.1-4ubuntu1
    0.13-1
    1.0.0~bzr501-0ubuntu2
    3.8.6-0ubuntu9.1
    2.40.0-2
    2.71-1
    1.325
    30.0-0ubuntu4
    4.3-7ubuntu1
    1:3.10.1-0ubuntu2
    5.0-2ubuntu2
    1:1.4.7-1
    2.40.0-1
    2:1.0.17-1ubuntu2
    0.1.20-3
    7.7+1
    2.20.1-5.1ubuntu20.1
    15-0ubuntu6
    5.9+20140118-1ubuntu1
    3.14.3-0ubuntu3.2
    7.2.2+14.04.20140714-0ubuntu1
    1.37-2ubuntu1
    1.08-3
    1:1.9.0-1build1
    0.20.2-2ubuntu2
    7.1.4+14.04.20140210-0ubuntu1
    2.4.3-1ubuntu2
    0.100.0-16
    1.5.6-1
    1.36.3-1ubuntu1
    3.6.2-0ubuntu1
    5.2.0.dfsg.1-2
    0.4-1
    14.04+14.04.20140604-0ubuntu1
    0.3-1
    0.2.0+14.04.20140217.1-0ubuntu1
    0.0.0+14.04.20140403-0ubuntu1
    1:4.3-3ubuntu1
    5.2.1+dfsg-1ubuntu14.2
    4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    1:0.5.1-3
    1.10-2ubuntu1
    1:2.24-0ubuntu2
    48
    4.6.3-6
    1.0.52-0ubuntu1.2
    1:0.9.11.2+14.04.20140714-0ubuntu1
    0.1.1-0ubuntu3
    1.70ubuntu8
    0.2.8-1
    3.10.4-0ubuntu1.1
    20140209dfsg0-1ubuntu1
    1:0.9.11.2+14.04.20140714-0ubuntu1
    0.7.6-1ubuntu3
    3.4.0-0ubuntu1
    3.6.0-0ubuntu2
    0.4.0.dfsg.1-7build1
    0.105-4ubuntu2
    3.12.0-1
    0.9.5-1ubuntu5
    3.54-1ubuntu1
    1.12+dfsg-2ubuntu4
    2.40.0-1
    1:7.3.0-1ubuntu3.1
    018-8
    1:31.0+build1-0ubuntu0.14.04.1
    1.8.1-2ubuntu2
    1:5.14-2ubuntu3.1
    0.6.8-1ubuntu1
    0.2.2-1ubuntu1
    3.8.6-0ubuntu9.1
    0.12.99-3ubuntu1
    0.5.4-2
    3.13.0-32.57
    1:7.7+1
    1:5.16.1-1ubuntu3
    13.10-0ubuntu6
    1.05-7build3
    0.0.0+14.04.20140403-0ubuntu1
    1.1.5-4build1
    1.0.6-5
    1.15+14.04.20131126.2-0ubuntu3
    0.2-1
    1:0.9.11.2+14.04.20140714-0ubuntu1
    0.20.0-1
    0.10.0-1ubuntu2
    0.9.8.2-1ubuntu2
    1.5.51ubuntu2
    1.5.2-1
    3.10.2-0ubuntu1
    2.88dsf-41ubuntu6
    1.7.2-0ubuntu1.1
    0.9.8.8-0ubuntu7
    1:9.9.5.dfsg-3
    1:0.5.1-3
    3.3-1ubuntu1
    1.69ubuntu1.1
    2:7.4.052-1ubuntu3
    2.5.3-2ubuntu1
    0.9.8.8-0ubuntu7
    204-5ubuntu20.3
    0.12+git20090217-3ubuntu8
    0.9.3+14.04.20140314-0ubuntu1
    2:1.1.1-1
    2.39.93-0ubuntu1
    3.8.6-0ubuntu9.1
    0.1+13.10.20130723-0ubuntu1
    2.10.2-2ubuntu1
    0.9.9-1
    10.1.3-0ubuntu0.1
    2.3-20ubuntu1
    3.4-1
    0.07-1
    1:1.3.6-0ubuntu5
    3.6.2-0ubuntu1
    2.4.52-1
    0.23-1ubuntu2
    1.1.0+14.04.20140304-0ubuntu1"
    localhost.(none),"docbook-dtds
    gnome-user-share
    fipscheck-lib
    gsm
    pulseaudio-libs
    perl-Pod-Escapes
    kexec-tools
    device-mapper-persistent-data
    c2070
    GConf2-gtk
    gnome-speech
    xorg-x11-drv-vmware
    libicu
    pyxf86config
    libdaemon
    pciutils
    libart_lgpl
    wacomexpresskeys
    gnome-panel-libs
    quota
    coreutils
    smc-fonts-common
    pygobject2
    wpa_supplicant
    rarian-compat
    PackageKit-device-rebind
    sgpio
    libuuid
    mdadm
    gnutls
    parted
    abrt-libs
    xorg-x11-drv-xgi
    libfprint
    gthumb
    grubby
    xorg-x11-drv-v4l
    xorg-x11-utils
    tcp_wrappers
    iso-codes
    gutenprint-cups
    vorbis-tools
    un-core-fonts-common
    python-ethtool
    webkitgtk
    iwl6000-firmware
    udisks
    gnome-session-xsession
    xz-libs
    xdg-user-dirs-gtk
    lohit-kannada-fonts
    xorg-x11-drv-i740
    python-pycurl
    gstreamer-python
    openssh
    system-config-network-tui
    enchant
    libutempter
    gpgme
    boost-system
    iproute
    ConsoleKit-libs
    net-snmp
    libsmbclient
    foomatic
    libbonoboui
    libreport-plugin-reportuploader
    dracut-kernel
    nss
    busybox
    sqlite
    taglib
    glibc
    pakchois
    pulseaudio-module-gconf
    sysstat
    gnome-utils
    ca-certificates
    gtk2-engines
    bc
    policycoreutils
    printer-filters
    pkgconfig
    libsndfile
    xorg-x11-drv-mouse
    libstdc++
    paps-libs
    libgudev1
    gamin
    psmisc
    file
    libreport-newt
    perl
    system-config-firewall
    rpm-libs
    cjkuni-fonts-common
    apr
    metacity
    gvfs-smb
    pycairo
    cpuspeed
    gnome-python2-bonobo
    libgnome
    libiptcdata
    xorg-x11-drv-intel
    cpio
    pyOpenSSL
    pth
    time
    biosdevname
    usermode-gtk
    avahi-ui
    libsamplerate
    neon
    xorg-x11-xinit
    control-center-extra
    PackageKit-yum-plugin
    dejavu-serif-fonts
    mesa-libGL
    mtr
    vim-enhanced
    librsvg2
    m2crypto
    libpcap
    libXtst
    at-spi
    yum-metadata-parser
    brasero
    jasper-libs
    ModemManager
    rtkit
    setup
    fipscheck
    plymouth-plugin-two-step
    b43-fwcutter
    iw
    foomatic-db-ppds
    cyrus-sasl-plain
    libIDL
    cups
    xorg-x11-drv-tdfx
    coreutils-libs
    ed
    libudev
    gnome-vfs2-smb
    libgnomekbd
    libogg
    mod_dnssd
    libXft
    xorg-x11-xkb-utils
    iputils
    cairomm
    libreport-cli
    xorg-x11-drivers
    cracklib-python
    upstart
    liberation-fonts-common
    mtools
    groff
    libtheora
    openobex
    xorg-x11-drv-rendition
    mesa-dri1-drivers
    libtdb
    poppler-glib
    hpijs
    notification-daemon
    bash
    gnome-keyring-pam
    httpd
    gstreamer-plugins-good
    gnome-icon-theme
    gdm-user-switch-applet
    mtdev
    wqy-zenhei-fonts
    glibc-headers
    ntp
    xorg-x11-drv-void
    xorg-x11-drv-cirrus
    libXfixes
    gucharmap
    libv4l
    dhcp-common
    libreport-plugin-logger
    pygpgme
    postfix
    vim-minimal
    libuser
    rdate
    xz-lzma-compat
    liberation-serif-fonts
    libfontenc
    gutenprint
    file-libs
    poppler-utils
    libgomp
    libsigc++20
    libgpod
    bluez
    comps-extras
    sos
    sil-padauk-fonts
    mesa-dri-filesystem
    net-snmp-libs
    xml-common
    notify-python
    xorg-x11-drv-nv
    lcms-libs
    xorg-x11-drv-trident
    xorg-x11-drv-keyboard
    system-config-users
    libtalloc
    dosfstools
    pcre
    libgcc
    libcurl
    libgweather
    gnome-applets
    xorg-x11-drv-aiptek
    pcmciautils
    rpm
    gnome-vfs2
    authconfig-gtk
    libcanberra
    sane-backends-libs
    gconfmm26
    pixman
    mingetty
    python-meh
    enscript
    python-libs
    libisofs
    mobile-broadband-provider-info
    dhclient
    pulseaudio-utils
    rhn-client-tools
    NetworkManager-glib
    mpfr
    acpid
    redhat-menus
    slang
    dbus-glib
    plymouth-utils
    bzip2
    libopenraw
    sound-juicer
    gpm-libs
    festival-lib
    hplip-common
    liberation-mono-fonts
    authconfig
    cryptsetup-luks-libs
    bind-utils
    hicolor-icon-theme
    unique
    gnome-desktop
    iptables
    strace
    lua
    wodim
    smp_utils
    lklug-fonts
    evince-dvi
    diffutils
    pam_passwdqc
    abrt
    xorg-x11-drv-wacom
    libnih
    yum-rhn-plugin
    libXv
    xorg-x11-drv-acecad
    xorg-x11-drv-ati-firmware
    sed
    libXcomposite
    xdg-user-dirs
    tcpdump
    libXinerama
    expat
    paktype-fonts-common
    obexd
    gmp
    libvpx
    libXcursor
    libgsf
    xorg-x11-drv-mach64
    rhythmbox
    procps
    perl-Module-Pluggable
    kbd-misc
    mysql-libs
    glibc-common
    selinux-policy-targeted
    plymouth-core-libs
    madan-fonts
    python-iniparse
    vino
    kpartx
    ipw2200-firmware
    patch
    xorg-x11-xauth
    system-config-date-docs
    openssh-askpass
    glx-utils
    abrt-addon-python
    dracut
    alsa-plugins-pulseaudio
    gtkspell
    libcroco
    cjkuni-uming-fonts
    gedit
    libreport-plugin-mailx
    ptouch-driver
    ustr
    xorg-x11-drv-sis
    libtar
    icedax
    libreport-python
    xorg-x11-drv-synaptics
    gnome-python2-canvas
    liboil
    xvattr
    device-mapper-event-libs
    libtasn1
    libbonobo
    xorg-x11-drv-modesetting
    pciutils-libs
    lohit-gujarati-fonts
    ql23xx-firmware
    control-center-filesystem
    less
    python-dmidecode
    tzdata
    binutils
    openssl
    ORBit2
    bzip2-libs
    wget
    dejavu-fonts-common
    firstboot
    gdm
    libusb1
    perl-libs
    eog
    evolution-data-server
    man
    libxklavier
    acl
    eject
    python-slip
    udev
    dbus-python
    grub
    atk
    libburn
    gdbm
    ghostscript
    polkit-desktop-policy
    plymouth-theme-rings
    libdv
    libproxy
    gnome-panel
    libffi
    gnome-utils-libs
    glibc-devel
    popt
    bfa-firmware
    shadow-utils
    libxkbfile
    prelink
    openssh-clients
    exempi
    seahorse
    system-config-keyboard-base
    nspr
    lohit-assamese-fonts
    pnm2ppa
    nss-softokn
    ncurses-base
    pulseaudio-gdm-hooks
    lohit-oriya-fonts
    python-rhsm
    which
    efibootmgr
    m4
    brasero-libs
    db4
    cronie
    libgpg-error
    cdrdao
    plymouth-scripts
    selinux-policy
    gnome-disk-utility-ui-libs
    dmraid-events
    nautilus-sendto
    hunspell-en
    libmcpp
    lohit-tamil-fonts
    libvisual
    sudo
    nss-tools
    rhn-check
    yum-plugin-security
    redhat-indexhtml
    cdparanoia
    libvorbis
    lohit-devanagari-fonts
    system-icon-theme
    xorg-x11-drv-sisusb
    iwl5000-firmware
    libpng
    startup-notification
    gnome-python2-gnome
    system-config-keyboard
    scl-utils
    findutils
    gnupg2
    polkit
    libreport-plugin-rhtsupport
    chkconfig
    xorg-x11-drv-apm
    xorg-x11-drv-mutouch
    gnome-media
    libertas-usb8388-firmware
    plymouth
    xorg-x11-drv-mga
    NetworkManager
    brasero-nautilus
    libshout
    xorg-x11-server-utils
    nautilus-open-terminal
    gnome-bluetooth
    mousetweaks
    gvfs
    gvfs-gphoto2
    iwl6000g2a-firmware
    xmlrpc-c-client
    ledmon
    Red_Hat_Enterprise_Linux-Release_Notes-6-en-US
    gnome-python2-extras
    filesystem
    gnome-power-manager
    system-config-firewall-tui
    firefox
    libSM
    info
    python-urlgrabber
    basesystem
    obex-data-server
    libgcrypt
    python-decorator
    libselinux-python
    pywebkitgtk
    gnome-screensaver
    hal-info
    dmidecode
    libnl
    rt61pci-firmware
    control-center
    module-init-tools
    libavc1394
    vlgothic-fonts-common
    redhat-logos
    evince-libs
    make
    zd1211-firmware
    gstreamer
    rpm-python
    PackageKit-gstreamer-plugin
    festival-speechtools-libs
    pulseaudio-module-x11
    iwl100-firmware
    libICE
    libXxf86dga
    xorg-x11-drv-ati
    media-player-info
    PackageKit-yum
    cheese
    libXdmcp
    ql2100-firmware
    urw-fonts
    pygtksourceview
    libraw1394
    libreport
    libcanberra-gtk2
    checkpolicy
    lx
    glib2
    gnome-python2-libegg
    gvfs-obexftp
    e2fsprogs-libs
    system-config-printer-udev
    libspectre
    poppler-data
    btparser
    sgml-common
    libgphoto2
    python-markupsafe
    xorg-x11-server-common
    libxslt
    libdrm
    system-config-printer-libs
    bridge-utils
    kurdit-unikurd-web-fonts
    libexif
    hdparm
    initscripts
    elfutils-libelf
    libthai
    pango
    gnome-media-libs
    PackageKit-gtk-module
    libXxf86vm
    xorg-x11-drv-ast
    dvd+rw-tools
    ConsoleKit-x11
    libwacom-data
    smartmontools
    rarian
    libmtp
    khmeros-fonts-common
    DeviceKit-power
    openldap
    system-config-printer
    kernel-headers
    pulseaudio
    kernel-devel
    util-linux-ng
    festival
    libXxf86misc
    newt-python
    libselinux-utils
    xorg-x11-drv-glint
    atmel-firmware
    ntpdate
    libopenraw-gnome
    net-tools
    nautilus-extensions
    gzip
    gnome-backgrounds
    libwnck
    libssh2
    setserial
    newt
    xorg-x11-drv-nouveau
    NetworkManager-gnome
    libimobiledevice
    libmpcdec
    poppler
    rsync
    iwl6050-firmware
    python
    libreport-compat
    libieee1284
    libaio
    pulseaudio-module-bluetooth
    pinentry-gtk
    libXvMC
    ethtool
    TaniumClient
    festvox-slt-arctic-hts
    libreport-plugin-kerneloops
    pbm2l2030
    libss
    ghostscript-fonts
    sane-backends
    libcdio
    freetype
    paktype-naqsh-fonts
    psacct
    lohit-telugu-fonts
    setuptool
    rhnlib
    gstreamer-plugins-base
    libsemanage
    shared-mime-info
    xz
    libattr
    words
    libmusicbrainz3
    crontabs
    libtiff
    iwl4965-firmware
    rootfiles
    libcom_err
    gnome-bluetooth-libs
    kernel-firmware
    device-mapper-event
    fuse
    pinfo
    mozilla-filesystem
    yum
    PackageKit
    libwacom
    libuser-python
    system-config-firewall-base
    sound-theme-freedesktop
    gstreamer-plugins-bad-free
    cryptsetup-luks
    scenery-backgrounds
    gnome-system-monitor
    e2fsprogs
    gnome-packagekit
    libgtop2
    libXau
    libjpeg-turbo
    gvfs-fuse
    abrt-tui
    cyrus-sasl-lib
    xorg-x11-drv-evdev
    python-mako
    xorg-x11-drv-openchrome
    thai-scalable-waree-fonts
    libselinux
    libtool-ltdl
    gnome-session
    libgnomecanvas
    man-pages-overrides
    mesa-dri-drivers
    libacl
    yelp
    sysvinit-tools
    mailx
    ipw2100-firmware
    lvm2-libs
    libdmx
    plymouth-graphics-libs
    redhat-bookmarks
    device-mapper
    vte
    libXres
    readahead
    cpp
    system-setup-keyboard
    lohit-punjabi-fonts
    gnome-settings-daemon
    xorg-x11-drv-penmount
    gnome-doc-utils-stylesheets
    libXfont
    httpd-tools
    hwdata
    gnome-disk-utility
    system-config-users-docs
    file-roller
    libsepol
    nano
    libplist
    tibetan-machine-uni-fonts
    orca
    python-dateutil
    gcalctool
    ql2400-firmware
    bind-libs
    python-simplejson
    gtk2
    gdm-plugin-fingerprint
    desktop-file-utils
    rsyslog
    keyutils-libs
    systemtap-runtime
    ppp
    xorg-x11-drv-fpit
    libnotify
    xorg-x11-drv-fbdev
    dejavu-sans-mono-fonts
    gnome-python2
    thai-scalable-fonts-common
    usermode
    iwl1000-firmware
    libproxy-bin
    perl-version
    cloog-ppl
    libcap
    blktrace
    b43-openfwwf
    dbus-c++
    lsof
    xorg-x11-drv-voodoo
    redhat-release-server
    bluez-libs
    evince
    python-gudev
    gvfs-archive
    gnome-menus
    elfutils-libs
    hal
    libgail-gnome
    cairo
    gnome-python2-libwnck
    libidn
    gtkmm24
    passwd
    eggdbus
    portreserve
    tar
    samba-common
    PackageKit-glib
    libgnomeui
    cracklib-dicts
    cronie-anacron
    yum-utils
    wavpack
    mailcap
    abrt-addon-ccpp
    gnome-python2-gnomekeyring
    gnome-python2-gconf
    dbus-x11
    libproxy-python
    python-slip-dbus
    subscription-manager
    lm_sensors-libs
    dash
    gnome-themes
    curl
    lockdev
    libical
    rhn-setup
    dbus-libs
    sg3_utils-libs
    cyrus-sasl
    xorg-x11-drv-vesa
    dmraid
    system-config-date
    paps
    xkeyboard-config
    krb5-libs
    ppl
    db4-utils
    gawk
    audit
    unzip
    desktop-effects
    crda
    flac
    rhn-setup-gnome
    iwl5150-firmware
    cjet
    libXi
    hal-libs
    totem-nautilus
    xorg-x11-drv-dummy
    khmeros-base-fonts
    libao
    lvm2
    xorg-x11-drv-i128
    libasyncns
    subscription-manager-firstboot
    wdaemon
    avahi-glib
    psutils
    libXrandr
    elfutils
    usbutils
    xcb-util
    rhnsd
    un-core-dotum-fonts
    libusb
    at-spi-python
    system-gnome-theme
    gnome-python2-applet
    pyorbit
    fprintd
    boost-filesystem
    numactl
    kbd
    spice-vdagent
    avahi-autoipd
    foomatic-db-filesystem
    pulseaudio-libs-glib2
    apr-util-ldap
    alsa-lib
    samba-winbind
    abrt-addon-kerneloops
    gcc
    ConsoleKit
    nss-util
    genisoimage
    gok
    kernel
    rfkill
    libdiscid
    xorg-x11-drv-vmmouse
    libX11-common
    hunspell
    python-iwlib
    tmpwatch
    hplip-libs
    gstreamer-tools
    gnome-user-docs
    cdparanoia-libs
    cups-libs
    openjpeg-libs
    mlocate
    cups-pk-helper
    libXt
    xorg-x11-drv-qxl
    nspluginwrapper
    pangomm
    pm-utils
    speex
    jomolhari-fonts
    compiz-gnome
    microcode_ctl
    pam
    libxcb
    traceroute
    libedit
    foomatic-db
    pinentry
    pygtk2-libglade
    libpanelappletmm
    avahi-libs
    libXScrnSaver
    gvfs-afc
    fontpackages-filesystem
    stix-fonts
    virt-what
    vconfig
    xulrunner
    aic94xx-firmware
    readline
    alsa-utils
    gnome-terminal
    gnote
    gnome-disk-utility-libs
    compiz
    irqbalance
    gdm-libs
    tcsh
    abrt-cli
    nss-sysinit
    perl-Pod-Simple
    device-mapper-libs
    fuse-libs
    plymouth-gdm-hooks
    libblkid
    gnome-python2-desktop
    dbus
    iptables-ipv6
    dnsmasq
    glibmm24
    xorg-x11-server-Xorg
    ncurses-libs
    vlgothic-fonts
    zlib
    pbm2l7k
    attr
    openssh-server
    dmz-cursor-themes
    libreport-gtk
    iwl3945-firmware
    lohit-bengali-fonts
    zip
    plymouth-plugin-label
    xorg-x11-drv-hyperpen
    c2050
    polkit-gnome
    ntsysv
    gnome-python2-gnomevfs
    sane-backends-libs-gphoto2
    libXdamage
    gnome-keyring
    totem-mozplugin
    totem-pl-parser
    dejavu-sans-fonts
    liberation-sans-fonts
    smc-meera-fonts
    kpathsea
    libiec61883
    pygtk2
    libatasmart
    usbmuxd
    gtksourceview2
    libarchive
    paktype-tehreer-fonts
    fontconfig
    libcap-ng
    libsoup
    geoclue
    libXmu
    libXext
    tcp_wrappers-libs
    at
    xorg-x11-drv-elographics
    libpciaccess
    apr-util
    xdg-utils
    rt73usb-firmware
    xorg-x11-drv-siliconmotion
    rng-tools
    audit-libs
    vim-common
    xorg-x11-drv-s3virge
    min12xxw
    zenity
    xorg-x11-drv-savage
    nautilus
    libglade2
    ql2200-firmware
    ql2500-firmware
    GConf2
    man-pages
    ivtv-firmware
    nss-softokn-freebl
    xmlrpc-c
    xorg-x11-drv-r128
    abyssinica-fonts
    libX11
    plymouth-system-theme
    libxml2
    MAKEDEV
    cracklib
    mcpp
    totem
    ncurses
    logrotate
    subscription-manager-gui
    libXrender
    gnome-mag
    libxml2-python
    fprintd-pam
    xorg-x11-font-utils
    samba-winbind-clients
    grep
    wireless-tools
    mesa-libGLU
    python-beaker","nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
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
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable
    Not Uninstallable","1.0
    2.28.2
    1.2.0
    1.0.13
    0.9.21
    1.04
    2.0.0
    0.1.4
    0.99
    2.28.0
    0.4.25
    12.0.2
    4.2.1
    0.3.37
    0.14
    3.1.10
    2.3.20
    0.4.2
    2.30.2
    3.17
    8.4
    04.2
    2.20.0
    0.7.3
    0.8.1
    0.5.8
    1.2.0.10
    2.17.2
    3.2.5
    2.8.5
    2.1
    2.0.8
    1.6.0
    0.1.0
    2.10.11
    7.0.15
    0.2.0
    7.5
    7.6
    3.16
    5.2.5
    1.2.0
    1.0.2
    0.6
    1.2.6
    9.221.4.1
    1.0.1
    2.28.0
    4.999.9
    0.8
    2.4.5
    1.3.4
    7.19.0
    0.10.16
    5.3p1
    1.6.0.el6.2
    1.5.0
    1.1.5
    1.1.8
    1.41.0
    2.6.32
    0.4.1
    5.5
    3.6.9
    4.0.4
    2.24.2
    2.0.9
    004
    3.14.0.0
    1.15.1
    3.6.20
    1.6.1
    2.12
    0.4
    0.9.21
    9.0.4
    2.28.1
    2010.63
    2.18.4
    1.06.95
    2.0.83
    1.1
    0.23
    1.0.20
    1.8.1
    4.4.7
    0.6.8
    147
    0.1.10
    22.6
    5.04
    2.0.9
    5.10.1
    1.2.27
    4.8.0
    0.2.20080216.1
    1.3.9
    2.28.0
    1.4.3
    1.8.6
    1.5
    2.28.0
    2.28.0
    1.0.4
    2.20.2
    2.10
    0.10
    2.0.7
    1.7
    0.4.1
    1.102
    0.6.25
    0.1.7
    0.29.3
    1.0.9
    2.28.1
    0.5.8
    2.30
    9.0
    0.75
    7.2.411
    2.26.0
    0.20.2
    1.0.0
    1.2.1
    1.28.1
    1.1.2
    2.28.3
    1.900.1
    0.4.0
    0.5
    2.8.14
    1.2.0
    0.8.3
    012
    0.9.17
    4.0
    2.1.23
    0.8.13
    1.4.2
    1.4.5
    8.4
    1.1
    147
    2.24.2
    2.28.2
    1.1.4
    0.6
    2.3.1
    7.7
    20071127
    1.8.0
    2.0.9
    7.3
    2.8.16
    0.6.5
    1.05.1.20090721
    4.0.12
    1.18.1.4
    1.1.0
    1.4
    4.2.5
    7.11
    1.2.10
    0.12.4
    3.12.4
    0.5.0
    4.1.2
    2.28.2
    2.2.15
    0.10.23
    2.28.0
    2.30.4
    1.1.2
    0.9.45
    2.12
    4.2.4p8
    1.4.0
    1.5.1
    5.0
    2.28.2
    0.6.3
    4.1.1
    2.0.9
    0.1
    2.6.6
    7.2.411
    0.56.13
    1.4
    4.999.9
    1.05.1.20090721
    1.0.5
    5.2.5
    5.04
    0.12.4
    4.4.7
    2.2.4.2
    0.7.2
    4.66
    17.8
    2.2
    2.6.1
    9.0
    5.5
    0.6.3
    0.1.1
    2.1.20
    1.19
    1.3.6
    1.6.2
    1.2.106
    2.0.7
    3.0.9
    7.8
    4.4.7
    7.19.7
    2.28.0
    2.28.0
    1.4.1
    015
    4.8.0
    2.24.2
    6.1.12
    0.22
    1.0.21
    2.28.0
    0.26.2
    1.08
    0.12.1
    1.6.4
    2.6.6
    0.6.32
    1.20100122
    4.1.1
    0.9.21
    1.0.0.1
    0.8.1
    2.4.1
    1.0.10
    14.0.0
    2.2.1
    0.86
    0.8.3
    1.0.5
    0.0.5
    2.28.1
    1.20.6
    1.96
    3.12.4
    1.05.1.20090721
    6.1.12
    1.2.0
    9.8.2
    0.11
    1.1.4
    2.28.2
    1.4.7
    4.5.19
    5.1.4
    1.1.9
    0.94
    0.6
    2.28.2
    2.8.1
    1.0.5
    2.0.8
    0.16.1
    1.0.1
    0.9.1
    1.0.7
    1.5.0
    6.99.99
    4.2.1
    0.4.3
    0.12
    4.0.0
    1.1.2
    2.0.1
    2.0
    0.19
    4.3.1
    0.9.0
    1.1.13
    1.14.15
    6.9.3
    0.12.8
    3.2.8
    3.90
    1.15
    5.1.66
    2.12
    3.7.19
    0.8.3
    2.000
    0.3.1
    2.28.1
    0.4.9
    3.1
    2.6
    1.0.2
    1.0.11
    5.3p1
    9.0
    2.0.8
    004
    1.0.21
    2.0.16
    0.6.2
    0.2.20080216.1
    2.28.4
    2.0.9
    1.3
    1.0.4
    0.10.7
    1.2.11
    1.1.9
    2.0.9
    1.6.2
    2.28.0
    0.3.16
    1.3
    1.02.77
    2.3
    2.24.2
    0.5.0
    3.1.10
    2.4.4
    3.03.27
    2.28.1
    436
    3.10.13
    2012j
    2.20.51.0.2
    1.0.0
    2.14.17
    1.0.5
    1.12
    2.30
    1.110.14
    2.30.4
    1.0.9
    5.10.1
    2.28.2
    2.28.3
    1.6f
    4.0
    2.2.49
    2.1.5
    0.2.20
    147
    0.83.0
    0.97
    1.28.0
    0.7.0
    1.8.0
    8.70
    0.96
    0.8.3
    1.0.0
    0.3.0
    2.30.2
    3.0.5
    2.28.1
    2.12
    1.13
    3.0.3.1
    4.1.4.2
    1.0.6
    0.4.6
    5.3p1
    2.1.0
    2.28.1
    1.3.1
    4.9.2
    2.4.3
    1.04
    3.12.9
    5.7
    0.9.21
    2.4.3
    1.1.8
    2.19
    0.5.4
    1.4.13
    2.28.3
    4.7.25
    1.4.4
    1.7
    1.2.3
    0.8.3
    3.7.19
    2.30.1
    1.0.0.rc16
    2.28.2
    0.20090216
    2.7.2
    2.4.5
    0.4.0
    1.8.6p3
    3.14.0.0
    1.0.0.1
    1.1.30
    6
    10.2
    1.2.3
    2.4.3
    6.0.0
    0.9.6
    8.83.5.1_1
    1.2.49
    0.10
    2.28.0
    1.3.1
    20120927
    4.4.2
    2.0.14
    0.96
    2.0.9
    1.3.49.3
    1.2.5
    1.3.0
    2.29.91
    5.110.22.p23
    0.8.3
    1.6.1
    0.8.1
    2.28.3
    2.2.2
    7.5
    0.17
    2.28.6
    2.28.2
    1.4.3
    1.4.3
    17.168.5.3
    1.16.24
    0.74
    4
    2.25.3
    2.4.30
    2.28.3
    1.2.27
    10.0.12
    1.2.1
    4.13a
    3.9.1
    10.0
    0.4.3
    1.4.5
    3.0.1
    2.0.94
    1.1.6
    2.28.3
    20090716
    2.11
    1.1
    1.2
    2.28.1
    3.9
    0.5.3
    20091202
    60.0.14
    2.28.2
    3.81
    1.4
    0.10.29
    4.8.0
    0.5.8
    1.2.96
    0.9.21
    39.31.5.1
    1.0.6
    1.1.3
    6.99.99
    6
    0.5.8
    2.28.1
    1.1.1
    1.19.38
    2.4
    2.8.0
    2.0.4
    2.0.9
    0.22
    2.0.22
    20030328
    2.22.5
    2.25.3
    1.4.3
    1.41.12
    1.1.16
    0.2.4
    0.4.0
    0.17
    0.6.3
    2.4.7
    0.9.2
    1.13.0
    1.1.26
    2.4.39
    1.1.16
    1.2
    20020502
    0.6.21
    9.16
    9.03.38
    0.152
    0.1.12
    1.28.1
    2.29.91
    0.5.8
    1.1.2
    0.97.0
    7.1
    0.4.1
    0.5
    5.43
    0.8.1
    1.0.1
    5.0
    014
    2.4.23
    1.1.16
    2.6.32
    0.9.21
    2.6.32
    2.17.2
    1.96
    1.0.3
    0.52.11
    2.0.94
    1.2.8
    1.3
    4.2.4p8
    0.0.5
    1.60
    2.28.4
    1.3.12
    2.28.0
    2.28.0
    1.4.2
    2.17
    0.52.11
    1.0.1
    0.8.1
    0.9.7
    1.2.6
    0.12.4
    3.0.6
    41.28.5.1
    2.6.6
    2.0.9
    0.2.11
    0.3.107
    0.9.21
    0.7.6
    1.0.7
    3.5
    5.1.314.7778
    0.20061229
    2.0.9
    1.4
    1.41.12
    5.50
    1.0.21
    0.81
    2.3.11
    2.0
    6.3.2
    2.4.5
    1.19.9
    2.5.22
    0.10.29
    2.0.43
    0.70
    4.999.9
    2.4.44
    3.0
    3.0.2
    1.10
    3.9.4
    228.61.2.24
    8.1
    1.41.12
    2.28.6
    2.6.32
    1.02.77
    2.8.3
    0.6.9
    1.9
    3.2.29
    0.5.8
    0.5
    0.56.13
    1.2.27
    0.7
    0.10.19
    1.2.0
    6.0.0
    2.28.0
    1.41.12
    2.28.3
    2.28.0
    1.0.6
    1.2.1
    1.4.3
    2.0.8
    2.1.23
    2.7.3
    0.3.4
    0.3.0
    0.4.12
    2.0.94
    2.2.6
    2.28.0
    2.26.0
    6.4.1
    9.0
    2.2.49
    2.28.1
    2.87
    12.4
    1.3
    2.02.98
    1.1.2
    0.8.3
    6
    1.02.77
    0.25.1
    1.0.6
    1.5.6
    4.4.7
    0.7
    2.4.4
    2.28.2
    1.5.0
    0.18.1
    1.4.5
    2.2.15
    0.233
    2.30.1
    1.0.8
    2.28.2
    2.0.41
    2.0.9
    1.2
    1.901
    2.28.2
    1.4.1
    5.28.2
    5.08.00
    9.8.2
    2.0.9
    2.18.9
    2.30.4
    0.15
    5.8.10
    1.4
    1.8
    2.4.5
    1.4.0
    0.5.0
    0.4.3
    2.30
    2.28.0
    0.4.12
    1.102
    39.31.5.1
    0.3.0
    0.77
    0.15.7
    2.16
    1.0.1
    5.2
    0.5.0
    4.82
    1.2.5
    6Server
    4.66
    2.28.2
    147.1
    1.4.3
    2.28.0
    0.152
    0.5.14
    1.20.1
    1.8.8
    2.28.0
    1.18
    2.18.2
    0.77
    0.6
    0.0.4
    1.23
    3.6.9
    0.5.8
    2.24.1
    2.8.16
    1.4.4
    1.1.30
    4.60
    2.1.31
    2.0.8
    2.28.0
    2.28.0
    1.2.24
    0.3.0
    0.2.20
    1.1.23
    3.1.1
    0.5.5.1
    2.28.1
    7.19.7
    1.0.1
    0.43
    1.0.0.1
    1.2.24
    1.28
    2.1.23
    2.3.2
    1.0.0.rc16
    1.9.60
    0.6.8
    2.6
    1.10.3
    0.10.2
    4.7.25
    3.1.7
    2.2
    6.0
    0.8.4
    1.1.1_2010.11.22
    1.2.1
    1.0.0.1
    8.24.2.2
    0.8.9
    1.6.1
    0.5.14
    2.28.6
    0.3.6
    5.0
    0.8.8
    2.02.98
    1.3.6
    0.8
    1.1.23
    0.17
    0.6.25
    1.17
    1.4.0
    0.152
    003
    0.3.6
    4.9.3
    1.0.2
    0.1.12
    1.28.1
    60.0.2
    2.28.0
    2.24.0
    0.1
    1.41.0
    2.0.7
    1.15
    0.12.0
    0.6.25
    4.0
    0.9.21
    1.3.9
    1.0.22
    3.6.9
    2.0.8
    4.4.7
    0.4.1
    3.14.0.0
    1.1.9
    2.28.1
    2.6.32
    0.3
    0.2.2
    12.9.0
    1.5.0
    1.2.8
    0.1
    2.9.16
    3.12.4
    0.10.29
    2.28.0
    10.2
    1.4.2
    1.3
    0.22.2
    0.0.4
    1.1.3
    0.1.0
    1.4.4
    2.26.0
    1.2.5
    1.2
    0.003
    0.8.2
    1.17
    1.1.1
    1.8.1
    2.0.14
    2.11
    4.0
    0.7.6
    2.16.0
    2.26.0
    0.6.25
    1.2.2
    1.4.3
    1.41
    0.9
    1.11
    1.9
    10.0.12
    30
    6.0
    1.0.22
    2.31.3
    0.6.3
    2.30.1
    0.8.2
    1.0.4
    2.30.4
    6.17
    2.0.8
    3.14.0.0
    3.13
    1.02.77
    2.8.3
    0.8.3
    2.17.2
    2.28.0
    1.2.24
    1.4.7
    2.48
    2.22.1
    1.13.0
    5.7
    20091202
    1.2.3
    990321
    2.4.44
    5.3p1
    0.4
    2.0.9
    15.32.2.9
    2.4.3
    3.0
    0.8.3
    1.4.1
    0.3b
    0.96
    1.3.49.3
    2.28.0
    1.0.21
    1.1.3
    2.28.2
    2.28.6
    2.28.3
    2.30
    1.05.1.20090721
    04.2
    2007
    1.2.0
    2.16.0
    0.17
    1.0.2
    2.8.2
    2.8.3
    2.0
    2.8.0
    0.6.4
    2.28.2
    0.11.1.1
    1.1.1
    1.3.1
    7.6
    3.1.10
    1.4.1
    0.13.1
    1.3.9
    1.0.2
    1.8
    1.7.7
    2
    2.2
    7.2.411
    1.10.6
    0.0.9
    2.28.0
    2.3.6
    2.28.4
    2.6.4
    2.02.08
    5.08.00
    2.28.0
    3.22
    20080701
    3.12.9
    1.16.24
    6.9.1
    1.0
    1.5.0
    0.8.3
    2.7.6
    3.24
    2.8.16
    2.7.2
    2.28.6
    5.7
    3.7.8
    1.1.23
    0.9.7
    0.15.9
    2.7.6
    0.1
    7.2
    3.6.9
    2.6.3
    29
    9.0
    1.3.1"
    Jims-Mac.local,"VoiceOver Quickstart
    VoiceOver Utility
    Wish
    Mail
    Build Web Page
    EPSON Scanner
    Time Machine
    OfflineStorageProcess
    soagent
    CalendarFileHandler
    Pass Viewer
    AutoImporter
    AddPrinter
    PressAndHold
    UserNotificationCenter
    FaceTime
    ScreenSaverEngine
    LocationMenu
    Dashboard
    Proof
    Extract
    iTunes
    Wireless Diagnostics
    SpeechFeedbackWindow
    CharacterPalette
    System Events
    MiniTerm
    Problem Reporter
    App Store
    System Information
    Java Web Start
    Archive Utility
    Keychain Circle Notification
    Stickies
    AddressBookManager
    TamilIM
    AirPort Base Station Agent
    NetAuthAgent
    Directory Utility
    VietnameseIM
    CoreServicesUIAgent
    Apple80211Agent
    50onPaletteServer
    Grab
    Network Setup Assistant
    AOSAlertManager
    AppleMobileDeviceHelper
    universalAccessAuthWarn
    Bluetooth Setup Assistant
    DiskImages UI Agent
    QuickTime Player
    Automator
    Python
    PTPCamera
    iBooks
    Keychain Access
    loginwindow
    Automator Launcher
    FindReaperFiles
    Spotlight
    Chess
    LaterAgent
    Console
    AppleGraphicsWarning
    TextEdit
    MakePDF
    Maps
    PluginProcess
    ABAssistantService
    Certificate Assistant
    ManagedClient
    AddressBookSourceSync
    Type8Camera
    ARDAgent
    SyncServer
    Rename
    DiskImageMounter
    Dictionary
    FileSyncAgent
    Dictation
    Game Center
    Automator Runner
    AddressBookSync
    Screen Sharing
    check_afp
    AddressBookUrlForwarder
    ReportPanic
    Conflict Resolver
    Audio MIDI Setup
    Switch Control
    Set Info
    Installer
    Migration Assistant
    Disk Utility
    PluginIM
    AppleScript Utility
    identityservicesd
    Install in Progress
    Summary Service
    NetworkProcess
    ParentalControls
    SCIM
    SystemUIServer
    Bluetooth File Exchange
    AVRCPAgent
    SocialPushAgent
    Finder
    Dock
    DigitalColor Meter
    eaptlstrust
    Expansion Slot Utility
    Wish
    quicklookd32
    VoiceOver
    CIMFindInputCodeTool
    Feedback Assistant
    Calculator
    WebKitPluginHost
    Notification Center
    Speech Startup
    FontRegistryUIAgent
    Boot Camp Assistant
    Install Command Line Developer Tools
    ScreenReaderUIServer
    PrinterProxy
    Captive Network Assistant
    Language Chooser
    InkServer
    SpeakableItems
    ZoomWindow
    SharedWorkerProcess
    WebProcess
    BluetoothUIServer
    CoreLocationAgent
    KeyboardViewer
    TrackpadIM
    Mission Control
    EscrowSecurityAlert
    SpeechRecognitionServer
    FindMyMacMessenger
    Recursive File Processing Droplet
    Launchpad
    Folder Actions Dispatcher
    DVD Player
    Preview
    ColorSync Utility
    Notes
    Image Capture
    Grapher
    RAID Utility
    HelpViewer
    UniversalAccessControl
    SpeechService
    AppleScript Editor
    Type4Camera
    AppDownloadLauncher
    imagent
    QuickLookUIHelper
    VirtualScanner
    Contacts
    AirScanScanner
    Reminders
    Folder Actions Setup
    Kotoeri
    Type5Camera
    UnmountAssistantAgent
    Speech Downloader
    SpeechSynthesisServer
    Python
    Uninstall VMware Tools
    Network Utility
    Safari
    Canon IJScanner4
    AirPlayUIAgent
    Match
    Setup Assistant
    AOSPushRelay
    KoreanIM
    SecurityFixer
    Python
    Canon IJScanner2
    Show Info
    Ticket Viewer
    ImageCaptureService
    Activity Monitor
    AppleMobileSync
    ODSAgent
    Droplet with Settable Properties
    Remove
    Cocoa-AppleScript Applet
    Calendar
    Image Events
    Database Events
    Photo Booth
    ChineseTextConverterService
    MassStorageCamera
    Embed
    Spotlight
    Software Update
    Font Book
    Messages
    rcd
    X11
    TCIM
    quicklookd
    Recursive Image File Processing Droplet
    CMFSyncAgent
    syncuid
    Memory Slot Utility
    AirPort Utility
    IMServicePlugInAgent
    System Image Utility
    AppleFileServer
    RegisterPluginIMApp
    System Preferences
    OBEXAgent
    Display Calibrator
    Image Capture Extension
    PubSubAgent
    store_helper
    Network Diagnostics
    File Sync
    KeyboardSetupAssistant
    nbagent
    Jar Launcher","nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
    nothing
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
    Not Uninstallable","6.0
    6.0
    8.5.9
    7.3
    9.2
    5.6.0
    1.3
    9537
    7.0
    7.0
    1.0
    6.5
    9.4
    1.2
    3.3.0
    3.0
    5.0
    1.0
    1.8
    None
    None
    11.2.1
    3.0
    4.2.4
    2.0.1
    1.3.6
    1.9
    10.9
    1.3
    10.9
    14.8.0
    10.9.1
    1.0
    10.0
    8.0
    1.6
    2.2
    5.0
    5.0
    1.4
    101.3
    9.3.2
    1.1.0
    1.8
    10.8.0
    1.06
    5.0
    1.0
    4.2.6
    10.9
    10.3
    2.4
    2.7.5
    9.2
    1.0
    9.0
    9.0
    1.3
    500
    3.0
    3.10
    1.0
    10.9
    2.2.0
    1.9
    9.2
    1.0
    9537
    8.0
    5.0
    6.0.2
    8.0
    9.2
    3.7.1
    8.1
    None
    10.9
    2.2.1
    8.1
    1.3.51
    1.1
    1.2
    8.0
    1.5
    4.0
    8.0
    1.0
    8.1
    3.0.6
    1.0
    None
    6.0
    5
    13
    1.4
    1.1.2
    10.0
    3.0
    2.0
    9537
    4.1
    102
    1.7
    4.2.6
    4.2.6
    25
    10.9.4
    1.8
    5.9
    13.0
    1.5.1
    8.4.19
    5.0
    6.0
    102
    3.2.3
    10.8
    9537
    1.0
    4.2.4
    81.0
    5.1.2
    1.0
    6.0
    9.4
    3.0
    1.0
    10.9
    4.2.5
    2.0
    9537
    9537
    4.2.6
    1486.12
    3.2
    1.5
    1.2
    1.0
    4.2.4
    3.1
    1.0
    1.0
    1.0.4
    5.7
    7.0
    4.9.0
    2.0
    6.3
    2.5
    4.0
    5.2
    7.0
    4.7.1
    2.6.1
    9.2
    1.0
    10.0
    5.0
    3.2
    8.0
    9.4
    2.0
    1.1.6
    4.4.0
    9.2
    4.0
    1.0
    4.7.1
    2.6.8
    9.8.3
    1.8
    7.0.5
    2.3.0
    2.0
    None
    10.9
    1.06
    6.4
    10.8
    2.5.6
    1.5.1
    None
    4.0
    6.5
    10.9.0
    5.0
    1.8
    1.0
    None
    1.0
    7.0
    1.1.6
    1.0.6
    6.0
    2.1
    9.2
    None
    1.0
    6
    5.0.1
    8.0
    325.7
    1.0
    102
    5.0
    1.0
    10.0
    8.1
    1.5.1
    6.3.2
    10.0
    10.9.4
    2.0
    1.1
    13.0
    4.2.6
    4.9.0
    9.2
    1.0.5
    1.0
    1.2
    8.1
    10.7
    1.0
    14.8.0"
    WIN-A12SC6N6T7Q,"Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.6161
    VMware Tools
    Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.4148
    Tanium Client 6.0.314.1190","MsiExec.exe /X{5FCE6D76-F5DC-37AB-B2B8-22AB8CEDB1D4} /qn /noreboot
    MsiExec.exe /X{8CF7A691-09D2-4659-8C84-0406A7B58AE7} /qn /noreboot
    MsiExec.exe /X{1F1C2DFC-2D24-3E06-BCB8-725134ADF989} /qn /noreboot
    C:\Program Files (x86)\Tanium\Tanium Client\uninst.exe","Is Uninstallable
    Is Uninstallable
    Is Uninstallable
    Not Uninstallable","9.0.30729.6161
    9.8.4.2202052
    9.0.30729.4148
    6.0.314.1190"
    
