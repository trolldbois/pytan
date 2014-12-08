
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
    2014-12-08 15:05:30,714 INFO     question_progress: Results 100% (Get Installed Applications from all machines)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'question_object': <taniumpy.object_types.saved_question.SavedQuestion object at 0x10e1b9290>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10e53bf50>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Installed Applications from all machines
    
    CSV Results of response: 
    Count,Name,Silent Uninstall String,Uninstallable,Version
    1644,[too many results],None,None,None
    1,update-manager-core,nothing,Not Uninstallable,1:0.196.12
    1,libminiupnpc8,nothing,Not Uninstallable,1.6-3ubuntu2.14.04.1
    1,iso-codes,nothing,Not Uninstallable,3.52-1
    1,docbook-dtds,nothing,Not Uninstallable,1.0
    1,libexttextcat-2.0-0,nothing,Not Uninstallable,3.4.3-1ubuntu1
    1,Google Search,nothing,Not Uninstallable,37.0.2062.120
    1,gnome-user-share,nothing,Not Uninstallable,2.28.2
    1,libblkid1:amd64,nothing,Not Uninstallable,2.20.1-5.1ubuntu20.1
    1,fipscheck-lib,nothing,Not Uninstallable,1.2.0
    1,gsm,nothing,Not Uninstallable,1.0.13
    1,VoiceOver Quickstart,nothing,Not Uninstallable,6.0
    1,VoiceOver Utility,nothing,Not Uninstallable,6.0
    1,growisofs,nothing,Not Uninstallable,7.1-10build1
    1,libdrm-radeon1:amd64,nothing,Not Uninstallable,2.4.52-1
    1,findutils,nothing,Not Uninstallable,4.4.2-7
    1,libxcomposite1:amd64,nothing,Not Uninstallable,1:0.4.4-1
    1,pulseaudio-libs,nothing,Not Uninstallable,0.9.21
    1,perl-Pod-Escapes,nothing,Not Uninstallable,1.04
    1,libboost-system1.54.0:amd64,nothing,Not Uninstallable,1.54.0-4ubuntu3.1
    1,kexec-tools,nothing,Not Uninstallable,2.0.0
    1,MakePDF,nothing,Not Uninstallable,10.0
    1,libfftw3-single3:amd64,nothing,Not Uninstallable,3.3.3-7ubuntu3
    1,libart-2.0-2:amd64,nothing,Not Uninstallable,2.3.21-2
    2,Wish,nothing,Not Uninstallable,8.5.9
    1,usb-modeswitch,nothing,Not Uninstallable,2.1.1+repack0-1ubuntu1
    1,libltdl7:amd64,nothing,Not Uninstallable,2.4.2-1.7ubuntu1
    1,device-mapper-persistent-data,nothing,Not Uninstallable,0.1.4
    1,c2070,nothing,Not Uninstallable,0.99
    1,Mail,nothing,Not Uninstallable,7.3
    1,GConf2-gtk,nothing,Not Uninstallable,2.28.0
    1,gnome-speech,nothing,Not Uninstallable,0.4.25
    1,transmission-common,nothing,Not Uninstallable,2.82-1.1ubuntu3.1
    1,gcc-4.8-base:amd64,nothing,Not Uninstallable,4.8.2-19ubuntu1
    1,xorg-x11-drv-vmware,nothing,Not Uninstallable,12.0.2
    1,software-properties-common,nothing,Not Uninstallable,0.92.37.1
    1,libicu,nothing,Not Uninstallable,4.2.1
    1,totem,nothing,Not Uninstallable,3.10.1-1ubuntu4
    1,Build Web Page,nothing,Not Uninstallable,9.2
    1,pyxf86config,nothing,Not Uninstallable,0.3.37
    1,libdaemon,nothing,Not Uninstallable,0.14
    1,EPSON Scanner,nothing,Not Uninstallable,5.6.0
    1,ibus-table,nothing,Not Uninstallable,1.5.0.is.1.5.0.20130419-2
    1,pciutils,nothing,Not Uninstallable,3.1.10
    1,libgc1c2:amd64,nothing,Not Uninstallable,1:7.2d-5ubuntu2
    2,Time Machine,nothing,Not Uninstallable,1.3
    1,OfflineStorageProcess,nothing,Not Uninstallable,9537
    1,time,nothing,Not Uninstallable,1.7-24
    1,libart_lgpl,nothing,Not Uninstallable,2.3.20
    1,fonts-tlwg-waree,nothing,Not Uninstallable,1:0.5.1-3
    1,wacomexpresskeys,nothing,Not Uninstallable,0.4.2
    1,libhx509-5-heimdal:amd64,nothing,Not Uninstallable,1.6~git20131207+dfsg-1ubuntu1
    1,libsecret-common,nothing,Not Uninstallable,0.16-0ubuntu1
    1,libevdocument3-4,nothing,Not Uninstallable,3.10.3-0ubuntu10.1
    1,libpython2.7:amd64,nothing,Not Uninstallable,2.7.6-8
    1,gnome-panel-libs,nothing,Not Uninstallable,2.30.2
    1,grub2-common,nothing,Not Uninstallable,2.02~beta2-9ubuntu1
    1,AppleGraphicsWarning,nothing,Not Uninstallable,2.3.0
    1,libglamor0:amd64,nothing,Not Uninstallable,0.6.0-0ubuntu4
    1,session-migration,nothing,Not Uninstallable,0.2.1
    1,libogg0:amd64,nothing,Not Uninstallable,1.3.1-1ubuntu1
    1,quota,nothing,Not Uninstallable,3.17
    1,libgssapi-krb5-2:amd64,nothing,Not Uninstallable,1.12+dfsg-2ubuntu4
    2,soagent,nothing,Not Uninstallable,7.0
    1,coreutils,nothing,Not Uninstallable,8.4
    1,libqt4-opengl:amd64,nothing,Not Uninstallable,4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    1,libtimezonemap1,nothing,Not Uninstallable,0.4.1
    1,smc-fonts-common,nothing,Not Uninstallable,04.2
    1,python3-apport,nothing,Not Uninstallable,2.14.1-0ubuntu3.2
    1,libxcb-shm0:amd64,nothing,Not Uninstallable,1.10-2ubuntu1
    1,pygobject2,nothing,Not Uninstallable,2.20.0
    1,wpa_supplicant,nothing,Not Uninstallable,0.7.3
    1,mountall,nothing,Not Uninstallable,2.53
    1,gdisk,nothing,Not Uninstallable,0.8.8-1build1
    1,libgnome-keyring0:amd64,nothing,Not Uninstallable,3.8.0-2
    1,libnl-route-3-200:amd64,nothing,Not Uninstallable,3.2.21-1
    1,python3-defer,nothing,Not Uninstallable,1.0.6-2build1
    1,CalendarFileHandler,nothing,Not Uninstallable,7.0
    1,smbclient,nothing,Not Uninstallable,2:4.1.6+dfsg-1ubuntu2.14.04.2
    1,gnomine,nothing,Not Uninstallable,1:3.10.1-0ubuntu1
    1,SpeechService,nothing,Not Uninstallable,5.2.6
    1,libbamf3-2:amd64,nothing,Not Uninstallable,0.5.1+14.04.20140409-0ubuntu1
    1,AinuIM,nothing,Not Uninstallable,1.0
    1,librtmp0:amd64,nothing,Not Uninstallable,2.4+20121230.gitdf6c518-1
    1,rarian-compat,nothing,Not Uninstallable,0.8.1
    1,libqt5sensors5:amd64,nothing,Not Uninstallable,5.2.1+dfsg-2ubuntu2
    1,aisleriot,nothing,Not Uninstallable,1:3.10.2-1
    1,PackageKit-device-rebind,nothing,Not Uninstallable,0.5.8
    1,libpwquality-common,nothing,Not Uninstallable,1.2.3-1ubuntu1
    1,qdbus,nothing,Not Uninstallable,4:4.8.5+git192-g085f851+dfsg-2ubuntu4
    1,sgpio,nothing,Not Uninstallable,1.2.0.10
    1,libecal-1.2-16,nothing,Not Uninstallable,3.10.4-0ubuntu1.1
    1,libuuid,nothing,Not Uninstallable,2.17.2
    1,libpam-modules:amd64,nothing,Not Uninstallable,1.1.8-1ubuntu2
    1,libwayland-server0:amd64,nothing,Not Uninstallable,1.4.0-1ubuntu1
    1,ethtool,nothing,Not Uninstallable,1:3.13-1
    2,Pass Viewer,nothing,Not Uninstallable,1.0
    1,mdadm,nothing,Not Uninstallable,3.2.5
    1,libsasl2-modules-db:amd64,nothing,Not Uninstallable,2.1.25.dfsg1-17build1
    1,iproute2,nothing,Not Uninstallable,3.12.0-2
    1,AutoImporter,nothing,Not Uninstallable,6.5
    1,gnutls,nothing,Not Uninstallable,2.8.5
    1,libspeex1:amd64,nothing,Not Uninstallable,1.2~rc1.1-1ubuntu1
    1,parted,nothing,Not Uninstallable,2.1
    1,libsnmp-base,nothing,Not Uninstallable,5.7.2~dfsg-8.1ubuntu3
    1,libreoffice-calc,nothing,Not Uninstallable,1:4.2.6.3-0ubuntu1
    1,AddPrinter,nothing,Not Uninstallable,9.4
    1,libmbim-glib0:amd64,nothing,Not Uninstallable,1.6.0-2
    1,abrt-libs,nothing,Not Uninstallable,2.0.8
    1,ncurses-bin,nothing,Not Uninstallable,5.9+20140118-1ubuntu1
    1,nautilus-data,nothing,Not Uninstallable,1:3.10.1-0ubuntu9.3
    1,accountsservice,nothing,Not Uninstallable,0.6.35-0ubuntu7
    1,xorg-x11-drv-xgi,nothing,Not Uninstallable,1.6.0
    1,libfprint,nothing,Not Uninstallable,0.1.0
    1,gthumb,nothing,Not Uninstallable,2.10.11
    1,powermgmt-base,nothing,Not Uninstallable,1.31build1
    1,grubby,nothing,Not Uninstallable,7.0.15
    2,PressAndHold,nothing,Not Uninstallable,1.2
    1,pkg-config,nothing,Not Uninstallable,0.26-1ubuntu4
    1,qtdeclarative5-ubuntu-ui-extras-browser-plugin-assets,nothing,Not Uninstallable,0.23+14.04.20140428-0ubuntu1
    1,mime-support,nothing,Not Uninstallable,3.54ubuntu1
    1,xorg-x11-drv-v4l,nothing,Not Uninstallable,0.2.0
    1,xorg-x11-utils,nothing,Not Uninstallable,7.5
    1,plainbox-secure-policy,nothing,Not Uninstallable,0.5.3-2
    1,python-dbus-dev,nothing,Not Uninstallable,1.2.0-2build2
    1,tcp_wrappers,nothing,Not Uninstallable,7.6
    1,iso-codes,nothing,Not Uninstallable,3.16
    1,PluginIM,nothing,Not Uninstallable,15
    1,gutenprint-cups,nothing,Not Uninstallable,5.2.5
    2,UserNotificationCenter,nothing,Not Uninstallable,3.3.0
    1,libelfg0:amd64,nothing,Not Uninstallable,0.8.13-5
    1,vorbis-tools,nothing,Not Uninstallable,1.2.0
    1,un-core-fonts-common,nothing,Not Uninstallable,1.0.2
    1,python-ethtool,nothing,Not Uninstallable,0.6
    1,ibus-gtk:amd64,nothing,Not Uninstallable,1.5.5-1ubuntu3
    1,webkitgtk,nothing,Not Uninstallable,1.2.6
    1,python3-brlapi,nothing,Not Uninstallable,5.0-2ubuntu2
    1,unity-scope-musicstores,nothing,Not Uninstallable,6.9.0+13.10.20131011-0ubuntu1
    1,libgettextpo-dev:amd64,nothing,Not Uninstallable,0.18.3.1-1ubuntu3
    1,Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.6161,MsiExec.exe /X{9BE518E6-ECC6-35A9-88E4-87755C07200F} /qn /noreboot,Is Uninstallable,9.0.30729.6161
    2,FaceTime,nothing,Not Uninstallable,3.0
    2,ScreenSaverEngine,nothing,Not Uninstallable,5.0
    1,iwl6000-firmware,nothing,Not Uninstallable,9.221.4.1
    2,LocationMenu,nothing,Not Uninstallable,1.0
    1,libxkbcommon0:amd64,nothing,Not Uninstallable,0.4.1-0ubuntu1
    1,udisks,nothing,Not Uninstallable,1.0.1
    1,gnome-session-xsession,nothing,Not Uninstallable,2.28.0
    1,CoRD,nothing,Not Uninstallable,0.5.7
    1,xz-libs,nothing,Not Uninstallable,4.999.9
    1,asannotation2,nothing,Not Uninstallable,1308.22.2900.0
    1,Slack,nothing,Not Uninstallable,1.0.2
    1,Microsoft SQL Server 2008 R2 Management Objects,MsiExec.exe /X{83F2B8F4-5CF3-4BE9-9772-9543EAE4AC5F} /qn /noreboot,Is Uninstallable,10.51.2500.0
    1,xdg-user-dirs-gtk,nothing,Not Uninstallable,0.8
    1,lohit-kannada-fonts,nothing,Not Uninstallable,2.4.5
    1,xorg-x11-drv-i740,nothing,Not Uninstallable,1.3.4
    1,python-pycurl,nothing,Not Uninstallable,7.19.0
    1,gstreamer-python,nothing,Not Uninstallable,0.10.16
    2,Dashboard,nothing,Not Uninstallable,1.8
    1,openssh,nothing,Not Uninstallable,5.3p1
    1,system-config-network-tui,nothing,Not Uninstallable,1.6.0.el6.2
    1,enchant,nothing,Not Uninstallable,1.5.0
    1,libutempter,nothing,Not Uninstallable,1.1.5
    2,Proof,nothing,Not Uninstallable,None
    1,gpgme,nothing,Not Uninstallable,1.1.8
    1,boost-system,nothing,Not Uninstallable,1.41.0
    1,iproute,nothing,Not Uninstallable,2.6.32
    1,ConsoleKit-libs,nothing,Not Uninstallable,0.4.1
    1,net-snmp,nothing,Not Uninstallable,5.5
    1,libsmbclient,nothing,Not Uninstallable,3.6.9
    1,Microsoft SQL Server System CLR Types,MsiExec.exe /X{C3F6F200-6D7B-4879-B9EE-700C0CE1FCDA} /qn /noreboot,Is Uninstallable,10.51.2500.0
    1,foomatic,nothing,Not Uninstallable,4.0.4
    1,libbonoboui,nothing,Not Uninstallable,2.24.2
    2,Extract,nothing,Not Uninstallable,None
    1,Speech Downloader,nothing,Not Uninstallable,5.0.25
    1,libreport-plugin-reportuploader,nothing,Not Uninstallable,2.0.9
    1,iTunes,nothing,Not Uninstallable,11.2.1
    1,Disk Inventory X,nothing,Not Uninstallable,1.0
    1,dracut-kernel,nothing,Not Uninstallable,004
    1,nss,nothing,Not Uninstallable,3.14.0.0
    1,Microsoft SQL Server 2012 (64-bit),"""c:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\x64\SetupARP.exe""",Not Uninstallable,64-
    1,Switch Control,nothing,Not Uninstallable,2.0
    1,busybox,nothing,Not Uninstallable,1.15.1
    1,Wireless Diagnostics,nothing,Not Uninstallable,3.0
    1,sqlite,nothing,Not Uninstallable,3.6.20
    1,taglib,nothing,Not Uninstallable,1.6.1
    1,Python,nothing,Not Uninstallable,2.6.9
    1,glibc,nothing,Not Uninstallable,2.12
    1,System Information,nothing,Not Uninstallable,10.10
    1,Transmission,nothing,Not Uninstallable,2.84
    1,pakchois,nothing,Not Uninstallable,0.4
    1,pulseaudio-module-gconf,nothing,Not Uninstallable,0.9.21
    1,sysstat,nothing,Not Uninstallable,9.0.4
    1,gnome-utils,nothing,Not Uninstallable,2.28.1
    1,ca-certificates,nothing,Not Uninstallable,2010.63
    1,IDLE,nothing,Not Uninstallable,2.7.8
    1,gtk2-engines,nothing,Not Uninstallable,2.18.4
    1,bc,nothing,Not Uninstallable,1.06.95
    1,SpeechFeedbackWindow,nothing,Not Uninstallable,4.2.4
    1,policycoreutils,nothing,Not Uninstallable,2.0.83
    1,printer-filters,nothing,Not Uninstallable,1.1
    2,CharacterPalette,nothing,Not Uninstallable,2.0.1
    1,pkgconfig,nothing,Not Uninstallable,0.23
    2,System Events,nothing,Not Uninstallable,1.3.6
    1,libsndfile,nothing,Not Uninstallable,1.0.20
    1,xorg-x11-drv-mouse,nothing,Not Uninstallable,1.8.1
    1,libstdc++,nothing,Not Uninstallable,4.4.7
    1,paps-libs,nothing,Not Uninstallable,0.6.8
    1,MRTAgent,nothing,Not Uninstallable,1.1
    1,libgudev1,nothing,Not Uninstallable,147
    1,gamin,nothing,Not Uninstallable,0.1.10
    1,psmisc,nothing,Not Uninstallable,22.6
    1,file,nothing,Not Uninstallable,5.04
    1,libreport-newt,nothing,Not Uninstallable,2.0.9
    1,perl,nothing,Not Uninstallable,5.10.1
    1,system-config-firewall,nothing,Not Uninstallable,1.2.27
    2,MiniTerm,nothing,Not Uninstallable,1.9
    1,rpm-libs,nothing,Not Uninstallable,4.8.0
    1,My Day,nothing,Not Uninstallable,14.4.6
    1,Reminders,nothing,Not Uninstallable,3.0
    1,Problem Reporter,nothing,Not Uninstallable,10.9
    1,cjkuni-fonts-common,nothing,Not Uninstallable,0.2.20080216.1
    1,apr,nothing,Not Uninstallable,1.3.9
    1,metacity,nothing,Not Uninstallable,2.28.0
    1,gvfs-smb,nothing,Not Uninstallable,1.4.3
    1,pycairo,nothing,Not Uninstallable,1.8.6
    1,cpuspeed,nothing,Not Uninstallable,1.5
    1,gnome-python2-bonobo,nothing,Not Uninstallable,2.28.0
    1,App Store,nothing,Not Uninstallable,1.3
    1,libgnome,nothing,Not Uninstallable,2.28.0
    1,libiptcdata,nothing,Not Uninstallable,1.0.4
    1,xorg-x11-drv-intel,nothing,Not Uninstallable,2.20.2
    1,Wireless Diagnostics,nothing,Not Uninstallable,4.0
    1,Gmail,nothing,Not Uninstallable,37.0.2062.120
    1,cpio,nothing,Not Uninstallable,2.10
    1,pyOpenSSL,nothing,Not Uninstallable,0.10
    1,Digital Color Meter,nothing,Not Uninstallable,5.10
    1,pth,nothing,Not Uninstallable,2.0.7
    1,time,nothing,Not Uninstallable,1.7
    1,Dictation,nothing,Not Uninstallable,1.4.55
    1,biosdevname,nothing,Not Uninstallable,0.4.1
    1,System Information,nothing,Not Uninstallable,10.9
    1,usermode-gtk,nothing,Not Uninstallable,1.102
    1,avahi-ui,nothing,Not Uninstallable,0.6.25
    1,Tunnelblick,nothing,Not Uninstallable,3.4.0 (build 4007)
    1,libsamplerate,nothing,Not Uninstallable,0.1.7
    1,neon,nothing,Not Uninstallable,0.29.3
    1,Memory Clean,nothing,Not Uninstallable,4.7
    1,Java Web Start,nothing,Not Uninstallable,14.8.0
    1,Archive Utility,nothing,Not Uninstallable,10.9.1
    1,xorg-x11-xinit,nothing,Not Uninstallable,1.0.9
    1,control-center-extra,nothing,Not Uninstallable,2.28.1
    1,PackageKit-yum-plugin,nothing,Not Uninstallable,0.5.8
    1,dejavu-serif-fonts,nothing,Not Uninstallable,2.30
    1,Screen Sharing,nothing,Not Uninstallable,1.6
    2,Keychain Circle Notification,nothing,Not Uninstallable,1.0
    1,Microsoft Visual C++ 2012 Redistributable (x86) - 11.0.61030,"""C:\ProgramData\Package Cache\{33d1fd90-4274-48a1-9bc1-97e33d9c2d6f}\vcredist_x86.exe""  /uninstall",Not Uninstallable,11.0.61030.0
    1,ManagedClient,nothing,Not Uninstallable,7.0
    1,mesa-libGL,nothing,Not Uninstallable,9.0
    1,mtr,nothing,Not Uninstallable,0.75
    1,vim-enhanced,nothing,Not Uninstallable,7.2.411
    1,Image Capture,nothing,Not Uninstallable,6.6
    1,librsvg2,nothing,Not Uninstallable,2.26.0
    1,VoiceOver Quickstart,nothing,Not Uninstallable,7.0
    2,Stickies,nothing,Not Uninstallable,10.0
    1,AddressBookManager,nothing,Not Uninstallable,8.0
    1,m2crypto,nothing,Not Uninstallable,0.20.2
    1,libpcap,nothing,Not Uninstallable,1.0.0
    1,libXtst,nothing,Not Uninstallable,1.2.1
    2,TamilIM,nothing,Not Uninstallable,1.6
    1,at-spi,nothing,Not Uninstallable,1.28.1
    1,yum-metadata-parser,nothing,Not Uninstallable,1.1.2
    1,brasero,nothing,Not Uninstallable,2.28.3
    1,jasper-libs,nothing,Not Uninstallable,1.900.1
    1,ModemManager,nothing,Not Uninstallable,0.4.0
    1,rtkit,nothing,Not Uninstallable,0.5
    1,AirPort Base Station Agent,nothing,Not Uninstallable,2.2
    1,setup,nothing,Not Uninstallable,2.8.14
    1,AddressBookManager,nothing,Not Uninstallable,9.0
    1,fipscheck,nothing,Not Uninstallable,1.2.0
    1,plymouth-plugin-two-step,nothing,Not Uninstallable,0.8.3
    1,b43-fwcutter,nothing,Not Uninstallable,012
    1,iw,nothing,Not Uninstallable,0.9.17
    1,foomatic-db-ppds,nothing,Not Uninstallable,4.0
    2,NetAuthAgent,nothing,Not Uninstallable,5.0
    1,cyrus-sasl-plain,nothing,Not Uninstallable,2.1.23
    1,libIDL,nothing,Not Uninstallable,0.8.13
    1,cups,nothing,Not Uninstallable,1.4.2
    2,Directory Utility,nothing,Not Uninstallable,5.0
    2,VietnameseIM,nothing,Not Uninstallable,1.4
    1,Aperture,nothing,Not Uninstallable,3.6
    1,xorg-x11-drv-tdfx,nothing,Not Uninstallable,1.4.5
    1,coreutils-libs,nothing,Not Uninstallable,8.4
    1,ed,nothing,Not Uninstallable,1.1
    1,libudev,nothing,Not Uninstallable,147
    1,Automator Runner,nothing,Not Uninstallable,2.5
    1,gnome-vfs2-smb,nothing,Not Uninstallable,2.24.2
    1,libgnomekbd,nothing,Not Uninstallable,2.28.2
    1,libogg,nothing,Not Uninstallable,1.1.4
    1,Image Capture Extension,nothing,Not Uninstallable,10.0
    1,mod_dnssd,nothing,Not Uninstallable,0.6
    1,EPSON Scanner,nothing,Not Uninstallable,5.7.6
    1,libXft,nothing,Not Uninstallable,2.3.1
    1,xorg-x11-xkb-utils,nothing,Not Uninstallable,7.7
    1,iputils,nothing,Not Uninstallable,20071127
    1,cairomm,nothing,Not Uninstallable,1.8.0
    1,libreport-cli,nothing,Not Uninstallable,2.0.9
    1,CoreServicesUIAgent,nothing,Not Uninstallable,101.3
    1,TextMate,nothing,Not Uninstallable,2.0-beta.6.4
    1,xorg-x11-drivers,nothing,Not Uninstallable,7.3
    1,cracklib-python,nothing,Not Uninstallable,2.8.16
    1,OBEXAgent,nothing,Not Uninstallable,4.3.1
    1,upstart,nothing,Not Uninstallable,0.6.5
    1,Microsoft Chart Converter,nothing,Not Uninstallable,14.4.6
    1,liberation-fonts-common,nothing,Not Uninstallable,1.05.1.20090721
    1,mtools,nothing,Not Uninstallable,4.0.12
    1,Widget Simulator,nothing,Not Uninstallable,1.0
    1,Firefox,nothing,Not Uninstallable,33.1.1
    1,groff,nothing,Not Uninstallable,1.18.1.4
    1,libtheora,nothing,Not Uninstallable,1.1.0
    1,openobex,nothing,Not Uninstallable,1.4
    1,VoiceOver Utility,nothing,Not Uninstallable,7.0
    1,Skype,nothing,Not Uninstallable,6.19
    1,xorg-x11-drv-rendition,nothing,Not Uninstallable,4.2.5
    1,mesa-dri1-drivers,nothing,Not Uninstallable,7.11
    1,libtdb,nothing,Not Uninstallable,1.2.10
    1,Microsoft Visual C++ 2010  x86 Runtime - 10.0.40219,MsiExec.exe /X{5D9ED403-94DE-3BA0-B1D6-71F4BDA412E6} /qn /noreboot,Is Uninstallable,10.0.40219
    1,poppler-glib,nothing,Not Uninstallable,0.12.4
    1,hpijs,nothing,Not Uninstallable,3.12.4
    1,notification-daemon,nothing,Not Uninstallable,0.5.0
    1,Apple80211Agent,nothing,Not Uninstallable,9.3.2
    1,bash,nothing,Not Uninstallable,4.1.2
    1,gnome-keyring-pam,nothing,Not Uninstallable,2.28.2
    1,Office365Service,nothing,Not Uninstallable,14.4.6
    1,httpd,nothing,Not Uninstallable,2.2.15
    1,gstreamer-plugins-good,nothing,Not Uninstallable,0.10.23
    2,50onPaletteServer,nothing,Not Uninstallable,1.1.0
    2,Grab,nothing,Not Uninstallable,1.8
    2,Network Setup Assistant,nothing,Not Uninstallable,10.8.0
    1,gnome-icon-theme,nothing,Not Uninstallable,2.28.0
    2,AOSAlertManager,nothing,Not Uninstallable,1.06
    1,gdm-user-switch-applet,nothing,Not Uninstallable,2.30.4
    1,mtdev,nothing,Not Uninstallable,1.1.2
    1,wqy-zenhei-fonts,nothing,Not Uninstallable,0.9.45
    1,glibc-headers,nothing,Not Uninstallable,2.12
    1,ntp,nothing,Not Uninstallable,4.2.4p8
    1,xorg-x11-drv-void,nothing,Not Uninstallable,1.4.0
    1,xorg-x11-drv-cirrus,nothing,Not Uninstallable,1.5.1
    1,Java Mission Control,nothing,Not Uninstallable,5.4.0
    1,libXfixes,nothing,Not Uninstallable,5.0
    1,gucharmap,nothing,Not Uninstallable,2.28.2
    1,libv4l,nothing,Not Uninstallable,0.6.3
    2,AppleMobileDeviceHelper,nothing,Not Uninstallable,5.0
    1,Sublime Text,nothing,Not Uninstallable,Build 3065
    1,dhcp-common,nothing,Not Uninstallable,4.1.1
    1,Notes,nothing,Not Uninstallable,3.1
    1,libreport-plugin-logger,nothing,Not Uninstallable,2.0.9
    1,pygpgme,nothing,Not Uninstallable,0.1
    1,AOSHeartbeat,nothing,Not Uninstallable,1.06
    1,postfix,nothing,Not Uninstallable,2.6.6
    1,Microsoft SQL Server 2012 Setup (English),MsiExec.exe /X{8CB0713F-CFE0-445D-BCB2-538465860E1A} /qn /noreboot,Is Uninstallable,11.1.3128.0
    1,Google Chrome,nothing,Not Uninstallable,39.0.2171.71
    1,vim-minimal,nothing,Not Uninstallable,7.2.411
    1,libuser,nothing,Not Uninstallable,0.56.13
    1,rdate,nothing,Not Uninstallable,1.4
    1,xz-lzma-compat,nothing,Not Uninstallable,4.999.9
    1,liberation-serif-fonts,nothing,Not Uninstallable,1.05.1.20090721
    1,libfontenc,nothing,Not Uninstallable,1.0.5
    2,universalAccessAuthWarn,nothing,Not Uninstallable,1.0
    1,gutenprint,nothing,Not Uninstallable,5.2.5
    1,Bluetooth Setup Assistant,nothing,Not Uninstallable,4.2.6
    1,file-libs,nothing,Not Uninstallable,5.04
    1,DiskImages UI Agent,nothing,Not Uninstallable,10.9
    1,poppler-utils,nothing,Not Uninstallable,0.12.4
    1,libgomp,nothing,Not Uninstallable,4.4.7
    1,libsigc++20,nothing,Not Uninstallable,2.2.4.2
    1,QuickTime Player,nothing,Not Uninstallable,10.3
    1,libgpod,nothing,Not Uninstallable,0.7.2
    1,bluez,nothing,Not Uninstallable,4.66
    1,comps-extras,nothing,Not Uninstallable,17.8
    1,sos,nothing,Not Uninstallable,2.2
    1,sil-padauk-fonts,nothing,Not Uninstallable,2.6.1
    1,Microsoft SQL Server 2012 Native Client ,MsiExec.exe /X{49D665A2-4C2A-476E-9AB8-FCC425F526FC} /qn /noreboot,Is Uninstallable,11.0.2100.60
    1,mesa-dri-filesystem,nothing,Not Uninstallable,9.0
    1,net-snmp-libs,nothing,Not Uninstallable,5.5
    1,xml-common,nothing,Not Uninstallable,0.6.3
    1,notify-python,nothing,Not Uninstallable,0.1.1
    1,xorg-x11-drv-nv,nothing,Not Uninstallable,2.1.20
    1,lcms-libs,nothing,Not Uninstallable,1.19
    1,xorg-x11-drv-trident,nothing,Not Uninstallable,1.3.6
    1,xorg-x11-drv-keyboard,nothing,Not Uninstallable,1.6.2
    1,Automator,nothing,Not Uninstallable,2.4
    1,Python,nothing,Not Uninstallable,2.7.5
    1,PTPCamera,nothing,Not Uninstallable,9.2
    1,iBooks,nothing,Not Uninstallable,1.0
    1,DatabaseProcess,nothing,Not Uninstallable,10600
    1,DiskImages UI Agent,nothing,Not Uninstallable,10.10
    1,system-config-users,nothing,Not Uninstallable,1.2.106
    1,Spotify,nothing,Not Uninstallable,0.9.14.13.gba5645ad
    1,libtalloc,nothing,Not Uninstallable,2.0.7
    2,Keychain Access,nothing,Not Uninstallable,9.0
    2,loginwindow,nothing,Not Uninstallable,9.0
    1,dosfstools,nothing,Not Uninstallable,3.0.9
    1,pcre,nothing,Not Uninstallable,7.8
    1,ReportPanic,nothing,Not Uninstallable,10.10
    1,libgcc,nothing,Not Uninstallable,4.4.7
    1,Automator Launcher,nothing,Not Uninstallable,1.3
    1,libcurl,nothing,Not Uninstallable,7.19.7
    1,libgweather,nothing,Not Uninstallable,2.28.0
    1,FindReaperFiles,nothing,Not Uninstallable,500
    1,gnome-applets,nothing,Not Uninstallable,2.28.0
    1,xorg-x11-drv-aiptek,nothing,Not Uninstallable,1.4.1
    1,Install OS X Mavericks,nothing,Not Uninstallable,1.3.44
    1,pcmciautils,nothing,Not Uninstallable,015
    1,rpm,nothing,Not Uninstallable,4.8.0
    1,gnome-vfs2,nothing,Not Uninstallable,2.24.2
    1,authconfig-gtk,nothing,Not Uninstallable,6.1.12
    2,Spotlight,nothing,Not Uninstallable,3.0
    1,libcanberra,nothing,Not Uninstallable,0.22
    1,Python Launcher,nothing,Not Uninstallable,2.7.8
    1,sane-backends-libs,nothing,Not Uninstallable,1.0.21
    1,gconfmm26,nothing,Not Uninstallable,2.28.0
    2,Chess,nothing,Not Uninstallable,3.10
    1,pixman,nothing,Not Uninstallable,0.26.2
    2,LaterAgent,nothing,Not Uninstallable,1.0
    1,mingetty,nothing,Not Uninstallable,1.08
    1,python-meh,nothing,Not Uninstallable,0.12.1
    1,SpeechRecognitionServer,nothing,Not Uninstallable,5.0.25
    1,enscript,nothing,Not Uninstallable,1.6.4
    1,python-libs,nothing,Not Uninstallable,2.6.6
    1,libisofs,nothing,Not Uninstallable,0.6.32
    1,mobile-broadband-provider-info,nothing,Not Uninstallable,1.20100122
    1,App Store,nothing,Not Uninstallable,2.0
    1,CoreServicesUIAgent,nothing,Not Uninstallable,134.6
    1,dhclient,nothing,Not Uninstallable,4.1.1
    1,Build Web Page,nothing,Not Uninstallable,10.0
    1,Google Chrome,"""C:\Program Files (x86)\Google\Chrome\Application\39.0.2171.71\Installer\setup.exe"" --uninstall --multi-install --chrome --system-level",Not Uninstallable,39.0.2171.71
    1,pulseaudio-utils,nothing,Not Uninstallable,0.9.21
    1,rhn-client-tools,nothing,Not Uninstallable,1.0.0.1
    1,NetworkManager-glib,nothing,Not Uninstallable,0.8.1
    1,mpfr,nothing,Not Uninstallable,2.4.1
    1,acpid,nothing,Not Uninstallable,1.0.10
    1,redhat-menus,nothing,Not Uninstallable,14.0.0
    1,slang,nothing,Not Uninstallable,2.2.1
    1,Microsoft Outlook,nothing,Not Uninstallable,14.4.6
    1,Console,nothing,Not Uninstallable,10.9
    1,dbus-glib,nothing,Not Uninstallable,0.86
    1,plymouth-utils,nothing,Not Uninstallable,0.8.3
    1,Yap,nothing,Not Uninstallable,None
    1,bzip2,nothing,Not Uninstallable,1.0.5
    1,libopenraw,nothing,Not Uninstallable,0.0.5
    1,sound-juicer,nothing,Not Uninstallable,2.28.1
    1,gpm-libs,nothing,Not Uninstallable,1.20.6
    1,festival-lib,nothing,Not Uninstallable,1.96
    1,AppleGraphicsWarning,nothing,Not Uninstallable,2.2.0
    1,Dropbox,nothing,Not Uninstallable,2.10.29
    1,hplip-common,nothing,Not Uninstallable,3.12.4
    1,liberation-mono-fonts,nothing,Not Uninstallable,1.05.1.20090721
    1,authconfig,nothing,Not Uninstallable,6.1.12
    1,cryptsetup-luks-libs,nothing,Not Uninstallable,1.2.0
    1,TextEdit,nothing,Not Uninstallable,1.9
    1,bind-utils,nothing,Not Uninstallable,9.8.2
    1,hicolor-icon-theme,nothing,Not Uninstallable,0.11
    1,unique,nothing,Not Uninstallable,1.1.4
    1,gnome-desktop,nothing,Not Uninstallable,2.28.2
    1,Microsoft Excel,nothing,Not Uninstallable,14.4.6
    1,GarageBand,nothing,Not Uninstallable,10.0.3
    1,Microsoft Upload Center,nothing,Not Uninstallable,14.4.6
    1,MakePDF,nothing,Not Uninstallable,9.2
    1,Google Docs,nothing,Not Uninstallable,37.0.2062.120
    1,Numbers,nothing,Not Uninstallable,3.5
    1,Maps,nothing,Not Uninstallable,1.0
    1,iptables,nothing,Not Uninstallable,1.4.7
    1,strace,nothing,Not Uninstallable,4.5.19
    1,lua,nothing,Not Uninstallable,5.1.4
    1,wodim,nothing,Not Uninstallable,1.1.9
    1,iTerm,nothing,Not Uninstallable,2.0.0.20141103
    1,smp_utils,nothing,Not Uninstallable,0.94
    1,PluginProcess,nothing,Not Uninstallable,9537
    1,lklug-fonts,nothing,Not Uninstallable,0.6
    1,evince-dvi,nothing,Not Uninstallable,2.28.2
    1,Solver,nothing,Not Uninstallable,1.0
    1,diffutils,nothing,Not Uninstallable,2.8.1
    1,pam_passwdqc,nothing,Not Uninstallable,1.0.5
    1,abrt,nothing,Not Uninstallable,2.0.8
    1,ABAssistantService,nothing,Not Uninstallable,8.0
    1,xorg-x11-drv-wacom,nothing,Not Uninstallable,0.16.1
    1,libnih,nothing,Not Uninstallable,1.0.1
    1,yum-rhn-plugin,nothing,Not Uninstallable,0.9.1
    1,libXv,nothing,Not Uninstallable,1.0.7
    1,xorg-x11-drv-acecad,nothing,Not Uninstallable,1.5.0
    2,Certificate Assistant,nothing,Not Uninstallable,5.0
    1,xorg-x11-drv-ati-firmware,nothing,Not Uninstallable,6.99.99
    1,ManagedClient,nothing,Not Uninstallable,6.0.2
    1,Python,nothing,Not Uninstallable,2.7.8
    1,sed,nothing,Not Uninstallable,4.2.1
    1,AddressBookSourceSync,nothing,Not Uninstallable,8.0
    1,Type8Camera,nothing,Not Uninstallable,9.2
    1,libXcomposite,nothing,Not Uninstallable,0.4.3
    1,xdg-user-dirs,nothing,Not Uninstallable,0.12
    1,tcpdump,nothing,Not Uninstallable,4.0.0
    1,Photo Booth,nothing,Not Uninstallable,7.0
    1,ARDAgent,nothing,Not Uninstallable,3.7.1
    1,libXinerama,nothing,Not Uninstallable,1.1.2
    1,expat,nothing,Not Uninstallable,2.0.1
    1,Microsoft Clip Gallery,nothing,Not Uninstallable,14.4.6
    1,paktype-fonts-common,nothing,Not Uninstallable,2.0
    1,Microsoft Help Viewer 1.1,c:\Program Files\Microsoft Help Viewer\v1.0\Microsoft Help Viewer 1.1\install.exe,Not Uninstallable,1.1.40219
    2,SyncServer,nothing,Not Uninstallable,8.1
    1,obexd,nothing,Not Uninstallable,0.19
    1,Microsoft Visual Studio 2010 Shell (Isolated) - ENU,MsiExec.exe /X{D64B6984-242F-32BC-B008-752806E5FC44} /qn /noreboot,Is Uninstallable,10.0.40219
    1,gmp,nothing,Not Uninstallable,4.3.1
    2,Rename,nothing,Not Uninstallable,None
    1,libvpx,nothing,Not Uninstallable,0.9.0
    1,libXcursor,nothing,Not Uninstallable,1.1.13
    1,libgsf,nothing,Not Uninstallable,1.14.15
    1,xorg-x11-drv-mach64,nothing,Not Uninstallable,6.9.3
    1,League of Legends,nothing,Not Uninstallable,1.0
    1,rhythmbox,nothing,Not Uninstallable,0.12.8
    1,procps,nothing,Not Uninstallable,3.2.8
    1,perl-Module-Pluggable,nothing,Not Uninstallable,3.90
    1,DiskImageMounter,nothing,Not Uninstallable,10.9
    2,Dictionary,nothing,Not Uninstallable,2.2.1
    1,kbd-misc,nothing,Not Uninstallable,1.15
    2,FileSyncAgent,nothing,Not Uninstallable,8.1
    1,mysql-libs,nothing,Not Uninstallable,5.1.66
    1,glibc-common,nothing,Not Uninstallable,2.12
    1,Microsoft SQL Server 2008 Setup Support Files ,MsiExec.exe /X{B40EE88B-400A-4266-A17B-E3DE64E94431} /qn /noreboot,Is Uninstallable,10.1.2731.0
    1,selinux-policy-targeted,nothing,Not Uninstallable,3.7.19
    1,Dictation,nothing,Not Uninstallable,1.3.51
    1,plymouth-core-libs,nothing,Not Uninstallable,0.8.3
    1,madan-fonts,nothing,Not Uninstallable,2.000
    1,python-iniparse,nothing,Not Uninstallable,0.3.1
    1,vino,nothing,Not Uninstallable,2.28.1
    1,PluginProcess,nothing,Not Uninstallable,10600
    1,RegisterPluginIMApp,nothing,Not Uninstallable,15
    1,kpartx,nothing,Not Uninstallable,0.4.9
    1,ipw2200-firmware,nothing,Not Uninstallable,3.1
    1,patch,nothing,Not Uninstallable,2.6
    1,Game Center,nothing,Not Uninstallable,1.1
    1,xorg-x11-xauth,nothing,Not Uninstallable,1.0.2
    1,Automator Runner,nothing,Not Uninstallable,1.2
    1,system-config-date-docs,nothing,Not Uninstallable,1.0.11
    1,Microsoft Document Connection,nothing,Not Uninstallable,14.4.6
    1,openssh-askpass,nothing,Not Uninstallable,5.3p1
    1,glx-utils,nothing,Not Uninstallable,9.0
    1,abrt-addon-python,nothing,Not Uninstallable,2.0.8
    1,dracut,nothing,Not Uninstallable,004
    1,alsa-plugins-pulseaudio,nothing,Not Uninstallable,1.0.21
    1,gtkspell,nothing,Not Uninstallable,2.0.16
    1,libcroco,nothing,Not Uninstallable,0.6.2
    1,AddressBookSync,nothing,Not Uninstallable,8.0
    1,AutoImporter,nothing,Not Uninstallable,6.6
    1,Microsoft Report Viewer 2012 Runtime,MsiExec.exe /X{9CCE40CE-A9E6-4916-8729-B008558EEF3F} /qn /noreboot,Is Uninstallable,11.0.2100.60
    1,cjkuni-uming-fonts,nothing,Not Uninstallable,0.2.20080216.1
    1,gedit,nothing,Not Uninstallable,2.28.4
    1,libreport-plugin-mailx,nothing,Not Uninstallable,2.0.9
    1,ptouch-driver,nothing,Not Uninstallable,1.3
    1,ustr,nothing,Not Uninstallable,1.0.4
    1,DiskImageMounter,nothing,Not Uninstallable,10.10
    1,xorg-x11-drv-sis,nothing,Not Uninstallable,0.10.7
    1,libtar,nothing,Not Uninstallable,1.2.11
    1,Adobe Photoshop Lightroom 5,nothing,Not Uninstallable,Adobe Photoshop Lightroom 5.6 [974614]
    1,Instruments,nothing,Not Uninstallable,6.1
    1,Screen Sharing,nothing,Not Uninstallable,1.5
    1,icedax,nothing,Not Uninstallable,1.1.9
    2,check_afp,nothing,Not Uninstallable,4.0
    1,libreport-python,nothing,Not Uninstallable,2.0.9
    1,AddressBookUrlForwarder,nothing,Not Uninstallable,8.0
    1,xorg-x11-drv-synaptics,nothing,Not Uninstallable,1.6.2
    1,Console,nothing,Not Uninstallable,10.10
    1,gnome-python2-canvas,nothing,Not Uninstallable,2.28.0
    1,Network Diagnostics,nothing,Not Uninstallable,1.3
    1,liboil,nothing,Not Uninstallable,0.3.16
    1,Free42-Decimal,nothing,Not Uninstallable,None
    1,xvattr,nothing,Not Uninstallable,1.3
    1,device-mapper-event-libs,nothing,Not Uninstallable,1.02.77
    1,libtasn1,nothing,Not Uninstallable,2.3
    1,libbonobo,nothing,Not Uninstallable,2.24.2
    1,xorg-x11-drv-modesetting,nothing,Not Uninstallable,0.5.0
    1,ReportPanic,nothing,Not Uninstallable,1.0
    1,pciutils-libs,nothing,Not Uninstallable,3.1.10
    1,lohit-gujarati-fonts,nothing,Not Uninstallable,2.4.4
    1,ql23xx-firmware,nothing,Not Uninstallable,3.03.27
    1,control-center-filesystem,nothing,Not Uninstallable,2.28.1
    1,less,nothing,Not Uninstallable,436
    1,python-dmidecode,nothing,Not Uninstallable,3.10.13
    1,Java Web Start,nothing,Not Uninstallable,15.0.0
    2,Conflict Resolver,nothing,Not Uninstallable,8.1
    1,tzdata,nothing,Not Uninstallable,2012j
    1,binutils,nothing,Not Uninstallable,2.20.51.0.2
    2,Audio MIDI Setup,nothing,Not Uninstallable,3.0.6
    1,openssl,nothing,Not Uninstallable,1.0.0
    1,ORBit2,nothing,Not Uninstallable,2.14.17
    1,bzip2-libs,nothing,Not Uninstallable,1.0.5
    1,Bluetooth Setup Assistant,nothing,Not Uninstallable,4.3.1
    1,wget,nothing,Not Uninstallable,1.12
    1,dejavu-fonts-common,nothing,Not Uninstallable,2.30
    1,firstboot,nothing,Not Uninstallable,1.110.14
    1,gdm,nothing,Not Uninstallable,2.30.4
    1,libusb1,nothing,Not Uninstallable,1.0.9
    1,perl-libs,nothing,Not Uninstallable,5.10.1
    1,eog,nothing,Not Uninstallable,2.28.2
    1,UnRarX,nothing,Not Uninstallable,Version 2.2
    1,evolution-data-server,nothing,Not Uninstallable,2.28.3
    1,man,nothing,Not Uninstallable,1.6f
    1,libxklavier,nothing,Not Uninstallable,4.0
    1,acl,nothing,Not Uninstallable,2.2.49
    1,eject,nothing,Not Uninstallable,2.1.5
    1,python-slip,nothing,Not Uninstallable,0.2.20
    1,X11,nothing,Not Uninstallable,1.0.1
    1,udev,nothing,Not Uninstallable,147
    1,dbus-python,nothing,Not Uninstallable,0.83.0
    1,Switch Control,nothing,Not Uninstallable,1.0
    1,grub,nothing,Not Uninstallable,0.97
    1,atk,nothing,Not Uninstallable,1.28.0
    1,libburn,nothing,Not Uninstallable,0.7.0
    1,gdbm,nothing,Not Uninstallable,1.8.0
    1,AddressBookUrlForwarder,nothing,Not Uninstallable,9.0
    2,Set Info,nothing,Not Uninstallable,None
    1,ghostscript,nothing,Not Uninstallable,8.70
    1,polkit-desktop-policy,nothing,Not Uninstallable,0.96
    1,plymouth-theme-rings,nothing,Not Uninstallable,0.8.3
    1,Installer,nothing,Not Uninstallable,6.0
    1,libdv,nothing,Not Uninstallable,1.0.0
    2,Migration Assistant,nothing,Not Uninstallable,5
    1,libproxy,nothing,Not Uninstallable,0.3.0
    1,gnome-panel,nothing,Not Uninstallable,2.30.2
    1,Git Gui,nothing,Not Uninstallable,0.19.0.2.g3decb8e
    1,libffi,nothing,Not Uninstallable,3.0.5
    1,gnome-utils-libs,nothing,Not Uninstallable,2.28.1
    1,glibc-devel,nothing,Not Uninstallable,2.12
    1,popt,nothing,Not Uninstallable,1.13
    1,bfa-firmware,nothing,Not Uninstallable,3.0.3.1
    1,shadow-utils,nothing,Not Uninstallable,4.1.4.2
    1,Safari,nothing,Not Uninstallable,8.0
    1,libxkbfile,nothing,Not Uninstallable,1.0.6
    2,Disk Utility,nothing,Not Uninstallable,13
    1,PluginIM,nothing,Not Uninstallable,1.4
    1,prelink,nothing,Not Uninstallable,0.4.6
    1,iBooks,nothing,Not Uninstallable,1.1
    1,openssh-clients,nothing,Not Uninstallable,5.3p1
    1,Photosmart 7510 series,nothing,Not Uninstallable,10.0
    1,VLC,nothing,Not Uninstallable,2.1.5
    1,exempi,nothing,Not Uninstallable,2.1.0
    1,seahorse,nothing,Not Uninstallable,2.28.1
    1,Open XML for Excel,nothing,Not Uninstallable,14.4.6
    1,system-config-keyboard-base,nothing,Not Uninstallable,1.3.1
    1,nspr,nothing,Not Uninstallable,4.9.2
    1,lohit-assamese-fonts,nothing,Not Uninstallable,2.4.3
    1,pnm2ppa,nothing,Not Uninstallable,1.04
    1,nss-softokn,nothing,Not Uninstallable,3.12.9
    1,ncurses-base,nothing,Not Uninstallable,5.7
    1,pulseaudio-gdm-hooks,nothing,Not Uninstallable,0.9.21
    1,lohit-oriya-fonts,nothing,Not Uninstallable,2.4.3
    1,python-rhsm,nothing,Not Uninstallable,1.1.8
    1,which,nothing,Not Uninstallable,2.19
    1,Terminal,nothing,Not Uninstallable,2.5
    1,IDSRemoteURLConnectionAgent,nothing,Not Uninstallable,10.0
    1,efibootmgr,nothing,Not Uninstallable,0.5.4
    1,m4,nothing,Not Uninstallable,1.4.13
    1,brasero-libs,nothing,Not Uninstallable,2.28.3
    1,db4,nothing,Not Uninstallable,4.7.25
    1,cronie,nothing,Not Uninstallable,1.4.4
    2,AppleScript Utility,nothing,Not Uninstallable,1.1.2
    1,libgpg-error,nothing,Not Uninstallable,1.7
    1,VMware Fusion,nothing,Not Uninstallable,7.1.0
    1,cdrdao,nothing,Not Uninstallable,1.2.3
    1,plymouth-scripts,nothing,Not Uninstallable,0.8.3
    1,selinux-policy,nothing,Not Uninstallable,3.7.19
    1,gnome-disk-utility-ui-libs,nothing,Not Uninstallable,2.30.1
    1,dmraid-events,nothing,Not Uninstallable,1.0.0.rc16
    1,nautilus-sendto,nothing,Not Uninstallable,2.28.2
    1,hunspell-en,nothing,Not Uninstallable,0.20090216
    1,libmcpp,nothing,Not Uninstallable,2.7.2
    1,lohit-tamil-fonts,nothing,Not Uninstallable,2.4.5
    1,libvisual,nothing,Not Uninstallable,0.4.0
    2,identityservicesd,nothing,Not Uninstallable,10.0
    1,GitHub Conduit,nothing,Not Uninstallable,1.0
    2,Install in Progress,nothing,Not Uninstallable,3.0
    2,Summary Service,nothing,Not Uninstallable,2.0
    1,sudo,nothing,Not Uninstallable,1.8.6p3
    1,nss-tools,nothing,Not Uninstallable,3.14.0.0
    1,Google Drive,nothing,Not Uninstallable,1.18
    1,NetworkProcess,nothing,Not Uninstallable,9537
    1,ARDAgent,nothing,Not Uninstallable,3.8
    1,rhn-check,nothing,Not Uninstallable,1.0.0.1
    1,yum-plugin-security,nothing,Not Uninstallable,1.1.30
    1,redhat-indexhtml,nothing,Not Uninstallable,6
    1,cdparanoia,nothing,Not Uninstallable,10.2
    1,libvorbis,nothing,Not Uninstallable,1.2.3
    1,lohit-devanagari-fonts,nothing,Not Uninstallable,2.4.3
    1,system-icon-theme,nothing,Not Uninstallable,6.0.0
    1,xorg-x11-drv-sisusb,nothing,Not Uninstallable,0.9.6
    1,iwl5000-firmware,nothing,Not Uninstallable,8.83.5.1_1
    1,libpng,nothing,Not Uninstallable,1.2.49
    1,startup-notification,nothing,Not Uninstallable,0.10
    2,ParentalControls,nothing,Not Uninstallable,4.1
    1,Automator,nothing,Not Uninstallable,2.5
    1,gnome-python2-gnome,nothing,Not Uninstallable,2.28.0
    1,system-config-keyboard,nothing,Not Uninstallable,1.3.1
    1,scl-utils,nothing,Not Uninstallable,20120927
    2,SCIM,nothing,Not Uninstallable,102
    1,findutils,nothing,Not Uninstallable,4.4.2
    1,gnupg2,nothing,Not Uninstallable,2.0.14
    1,polkit,nothing,Not Uninstallable,0.96
    1,TextEdit,nothing,Not Uninstallable,1.10
    2,SystemUIServer,nothing,Not Uninstallable,1.7
    1,libreport-plugin-rhtsupport,nothing,Not Uninstallable,2.0.9
    1,chkconfig,nothing,Not Uninstallable,1.3.49.3
    1,xorg-x11-drv-apm,nothing,Not Uninstallable,1.2.5
    1,Bluetooth File Exchange,nothing,Not Uninstallable,4.2.6
    1,AVRCPAgent,nothing,Not Uninstallable,4.2.6
    2,SocialPushAgent,nothing,Not Uninstallable,25
    1,xorg-x11-drv-mutouch,nothing,Not Uninstallable,1.3.0
    1,gnome-media,nothing,Not Uninstallable,2.29.91
    1,Family,nothing,Not Uninstallable,1.0
    1,libertas-usb8388-firmware,nothing,Not Uninstallable,5.110.22.p23
    1,plymouth,nothing,Not Uninstallable,0.8.3
    1,xorg-x11-drv-mga,nothing,Not Uninstallable,1.6.1
    1,NetworkManager,nothing,Not Uninstallable,0.8.1
    1,brasero-nautilus,nothing,Not Uninstallable,2.28.3
    1,libshout,nothing,Not Uninstallable,2.2.2
    1,xorg-x11-server-utils,nothing,Not Uninstallable,7.5
    1,nautilus-open-terminal,nothing,Not Uninstallable,0.17
    1,gnome-bluetooth,nothing,Not Uninstallable,2.28.6
    1,mousetweaks,nothing,Not Uninstallable,2.28.2
    1,GlobalProtect,nothing,Not Uninstallable,2.1.0-50
    1,gvfs,nothing,Not Uninstallable,1.4.3
    1,gvfs-gphoto2,nothing,Not Uninstallable,1.4.3
    1,SourceTree,nothing,Not Uninstallable,2.0.2
    1,iwl6000g2a-firmware,nothing,Not Uninstallable,17.168.5.3
    1,xmlrpc-c-client,nothing,Not Uninstallable,1.16.24
    1,ledmon,nothing,Not Uninstallable,0.74
    1,Red_Hat_Enterprise_Linux-Release_Notes-6-en-US,nothing,Not Uninstallable,4
    1,gnome-python2-extras,nothing,Not Uninstallable,2.25.3
    1,ABAssistantService,nothing,Not Uninstallable,9.0
    1,AskPermissionUI,nothing,Not Uninstallable,1.0
    1,Microsoft Office Reminders,nothing,Not Uninstallable,14.4.6
    1,Finder,nothing,Not Uninstallable,10.9.4
    2,Dock,nothing,Not Uninstallable,1.8
    1,filesystem,nothing,Not Uninstallable,2.4.30
    1,gnome-power-manager,nothing,Not Uninstallable,2.28.3
    1,Python,nothing,Not Uninstallable,2.7.6
    1,system-config-firewall-tui,nothing,Not Uninstallable,1.2.27
    1,Microsoft Error Reporting,nothing,Not Uninstallable,2.2.9
    1,iTerm,nothing,Not Uninstallable,None
    1,firefox,nothing,Not Uninstallable,10.0.12
    1,DigitalColor Meter,nothing,Not Uninstallable,5.9
    1,Microsoft Visual C++ 2010  x86 Redistributable - 10.0.40219,MsiExec.exe /X{F0C3E5D1-1ADE-321E-8167-68EF0DE699A5} /qn /noreboot,Is Uninstallable,10.0.40219
    1,libSM,nothing,Not Uninstallable,1.2.1
    1,info,nothing,Not Uninstallable,4.13a
    1,python-urlgrabber,nothing,Not Uninstallable,3.9.1
    1,Tanium Server 6.2.314.3258,C:\Program Files\Tanium\Tanium Server\uninst.exe,Not Uninstallable,6.2.314.3258
    1,MassStorageCamera,nothing,Not Uninstallable,10.0
    1,basesystem,nothing,Not Uninstallable,10.0
    1,obex-data-server,nothing,Not Uninstallable,0.4.3
    1,libgcrypt,nothing,Not Uninstallable,1.4.5
    1,python-decorator,nothing,Not Uninstallable,3.0.1
    1,libselinux-python,nothing,Not Uninstallable,2.0.94
    1,pywebkitgtk,nothing,Not Uninstallable,1.1.6
    1,gnome-screensaver,nothing,Not Uninstallable,2.28.3
    1,hal-info,nothing,Not Uninstallable,20090716
    1,Python 2.7.8 (64-bit),MsiExec.exe /X{61121B12-88BD-4261-A6EE-AB32610A56DE} /qn /noreboot,Is Uninstallable,2.7.8150
    1,dmidecode,nothing,Not Uninstallable,2.11
    2,eaptlstrust,nothing,Not Uninstallable,13.0
    1,libnl,nothing,Not Uninstallable,1.1
    1,rt61pci-firmware,nothing,Not Uninstallable,1.2
    1,Mail,nothing,Not Uninstallable,8.1
    1,control-center,nothing,Not Uninstallable,2.28.1
    1,module-init-tools,nothing,Not Uninstallable,3.9
    1,libavc1394,nothing,Not Uninstallable,0.5.3
    1,PTPCamera,nothing,Not Uninstallable,10.0
    1,Visual Studio 2010 Prerequisites - English,MsiExec.exe /X{662014D2-0450-37ED-ABAE-157C88127BEB} /qn /noreboot,Is Uninstallable,10.0.40219
    1,vlgothic-fonts-common,nothing,Not Uninstallable,20091202
    2,Expansion Slot Utility,nothing,Not Uninstallable,1.5.1
    1,redhat-logos,nothing,Not Uninstallable,60.0.14
    2,Wish,nothing,Not Uninstallable,8.4.19
    1,evince-libs,nothing,Not Uninstallable,2.28.2
    2,quicklookd32,nothing,Not Uninstallable,5.0
    1,make,nothing,Not Uninstallable,3.81
    1,VoiceOver,nothing,Not Uninstallable,7.0
    1,Application Loader,nothing,Not Uninstallable,3.0
    1,zd1211-firmware,nothing,Not Uninstallable,1.4
    1,gstreamer,nothing,Not Uninstallable,0.10.29
    1,rpm-python,nothing,Not Uninstallable,4.8.0
    1,Microsoft PowerPoint,nothing,Not Uninstallable,14.4.6
    1,PackageKit-gstreamer-plugin,nothing,Not Uninstallable,0.5.8
    1,festival-speechtools-libs,nothing,Not Uninstallable,1.2.96
    1,pulseaudio-module-x11,nothing,Not Uninstallable,0.9.21
    1,iwl100-firmware,nothing,Not Uninstallable,39.31.5.1
    1,VoiceOver,nothing,Not Uninstallable,6.0
    1,libICE,nothing,Not Uninstallable,1.0.6
    1,libXxf86dga,nothing,Not Uninstallable,1.1.3
    2,CIMFindInputCodeTool,nothing,Not Uninstallable,102
    1,rcd,nothing,Not Uninstallable,327.5
    1,AirScanScanner,nothing,Not Uninstallable,10.0
    1,xorg-x11-drv-ati,nothing,Not Uninstallable,6.99.99
    1,media-player-info,nothing,Not Uninstallable,6
    1,Microsoft Visual C++ 2012 Redistributable (x64) - 11.0.61030,"""C:\ProgramData\Package Cache\{ca67548a-5ebe-413a-b50c-4b9ceb6d66c6}\vcredist_x64.exe""  /uninstall",Not Uninstallable,11.0.61030.0
    1,PackageKit-yum,nothing,Not Uninstallable,0.5.8
    1,cheese,nothing,Not Uninstallable,2.28.1
    1,libXdmcp,nothing,Not Uninstallable,1.1.1
    1,Xcode,nothing,Not Uninstallable,6.1.1
    1,ql2100-firmware,nothing,Not Uninstallable,1.19.38
    1,urw-fonts,nothing,Not Uninstallable,2.4
    1,pygtksourceview,nothing,Not Uninstallable,2.8.0
    1,libraw1394,nothing,Not Uninstallable,2.0.4
    1,libreport,nothing,Not Uninstallable,2.0.9
    1,libcanberra-gtk2,nothing,Not Uninstallable,0.22
    1,Feedback Assistant,nothing,Not Uninstallable,3.2.3
    1,WebKitPluginHost,nothing,Not Uninstallable,10600
    1,iCloud Photos,nothing,Not Uninstallable,2.7
    1,checkpolicy,nothing,Not Uninstallable,2.0.22
    1,Microsoft Graph,nothing,Not Uninstallable,14.4.6
    1,lx,nothing,Not Uninstallable,20030328
    2,Calculator,nothing,Not Uninstallable,10.8
    1,glib2,nothing,Not Uninstallable,2.22.5
    1,WebKitPluginHost,nothing,Not Uninstallable,9537
    1,gnome-python2-libegg,nothing,Not Uninstallable,2.25.3
    1,gvfs-obexftp,nothing,Not Uninstallable,1.4.3
    1,e2fsprogs-libs,nothing,Not Uninstallable,1.41.12
    2,Notification Center,nothing,Not Uninstallable,1.0
    1,system-config-printer-udev,nothing,Not Uninstallable,1.1.16
    1,libspectre,nothing,Not Uninstallable,0.2.4
    1,poppler-data,nothing,Not Uninstallable,0.4.0
    1,btparser,nothing,Not Uninstallable,0.17
    1,sgml-common,nothing,Not Uninstallable,0.6.3
    1,Speech Startup,nothing,Not Uninstallable,4.2.4
    1,libgphoto2,nothing,Not Uninstallable,2.4.7
    1,python-markupsafe,nothing,Not Uninstallable,0.9.2
    1,Getty Images Stream,nothing,Not Uninstallable,1.0.0
    2,FontRegistryUIAgent,nothing,Not Uninstallable,81.0
    1,xorg-x11-server-common,nothing,Not Uninstallable,1.13.0
    1,libxslt,nothing,Not Uninstallable,1.1.26
    1,libdrm,nothing,Not Uninstallable,2.4.39
    1,NetworkProcess,nothing,Not Uninstallable,10600
    1,system-config-printer-libs,nothing,Not Uninstallable,1.1.16
    1,bridge-utils,nothing,Not Uninstallable,1.2
    1,kurdit-unikurd-web-fonts,nothing,Not Uninstallable,20020502
    2,Boot Camp Assistant,nothing,Not Uninstallable,5.1.2
    2,Install Command Line Developer Tools,nothing,Not Uninstallable,1.0
    1,Display Calibrator,nothing,Not Uninstallable,4.10.0
    1,libexif,nothing,Not Uninstallable,0.6.21
    1,hdparm,nothing,Not Uninstallable,9.16
    1,initscripts,nothing,Not Uninstallable,9.03.38
    1,elfutils-libelf,nothing,Not Uninstallable,0.152
    1,Feedback Assistant,nothing,Not Uninstallable,4.1.1
    1,System Preferences,nothing,Not Uninstallable,14.0
    1,libthai,nothing,Not Uninstallable,0.1.12
    1,ScriptMonitor,nothing,Not Uninstallable,1.0
    1,pango,nothing,Not Uninstallable,1.28.1
    1,AddressBookSourceSync,nothing,Not Uninstallable,9.0
    1,Keynote,nothing,Not Uninstallable,6.5
    1,gnome-media-libs,nothing,Not Uninstallable,2.29.91
    1,PackageKit-gtk-module,nothing,Not Uninstallable,0.5.8
    1,Jar Launcher,nothing,Not Uninstallable,15.0.0
    1,libXxf86vm,nothing,Not Uninstallable,1.1.2
    1,xorg-x11-drv-ast,nothing,Not Uninstallable,0.97.0
    1,dvd+rw-tools,nothing,Not Uninstallable,7.1
    1,ConsoleKit-x11,nothing,Not Uninstallable,0.4.1
    1,libwacom-data,nothing,Not Uninstallable,0.5
    1,ScreenReaderUIServer,nothing,Not Uninstallable,6.0
    1,smartmontools,nothing,Not Uninstallable,5.43
    1,rarian,nothing,Not Uninstallable,0.8.1
    1,libmtp,nothing,Not Uninstallable,1.0.1
    1,khmeros-fonts-common,nothing,Not Uninstallable,5.0
    1,DeviceKit-power,nothing,Not Uninstallable,014
    1,openldap,nothing,Not Uninstallable,2.4.23
    1,system-config-printer,nothing,Not Uninstallable,1.1.16
    1,kernel-headers,nothing,Not Uninstallable,2.6.32
    1,pulseaudio,nothing,Not Uninstallable,0.9.21
    1,kernel-devel,nothing,Not Uninstallable,2.6.32
    1,util-linux-ng,nothing,Not Uninstallable,2.17.2
    1,festival,nothing,Not Uninstallable,1.96
    1,PrinterProxy,nothing,Not Uninstallable,9.4
    2,Captive Network Assistant,nothing,Not Uninstallable,3.0
    1,libXxf86misc,nothing,Not Uninstallable,1.0.3
    1,newt-python,nothing,Not Uninstallable,0.52.11
    1,libselinux-utils,nothing,Not Uninstallable,2.0.94
    1,Type5Camera,nothing,Not Uninstallable,10.0
    1,xorg-x11-drv-glint,nothing,Not Uninstallable,1.2.8
    1,atmel-firmware,nothing,Not Uninstallable,1.3
    2,Language Chooser,nothing,Not Uninstallable,1.0
    1,ntpdate,nothing,Not Uninstallable,4.2.4p8
    2,InkServer,nothing,Not Uninstallable,10.9
    1,SpeakableItems,nothing,Not Uninstallable,4.2.5
    1,libopenraw-gnome,nothing,Not Uninstallable,0.0.5
    1,System Image Utility,nothing,Not Uninstallable,10.10
    1,net-tools,nothing,Not Uninstallable,1.60
    2,ZoomWindow,nothing,Not Uninstallable,2.0
    1,nautilus-extensions,nothing,Not Uninstallable,2.28.4
    1,gzip,nothing,Not Uninstallable,1.3.12
    1,Cyberduck,nothing,Not Uninstallable,4.5.2
    1,Bluetooth File Exchange,nothing,Not Uninstallable,4.3.1
    1,gnome-backgrounds,nothing,Not Uninstallable,2.28.0
    1,libwnck,nothing,Not Uninstallable,2.28.0
    1,libssh2,nothing,Not Uninstallable,1.4.2
    1,setserial,nothing,Not Uninstallable,2.17
    1,newt,nothing,Not Uninstallable,0.52.11
    1,xorg-x11-drv-nouveau,nothing,Not Uninstallable,1.0.1
    1,NetworkManager-gnome,nothing,Not Uninstallable,0.8.1
    1,libimobiledevice,nothing,Not Uninstallable,0.9.7
    1,libmpcdec,nothing,Not Uninstallable,1.2.6
    1,poppler,nothing,Not Uninstallable,0.12.4
    1,rsync,nothing,Not Uninstallable,3.0.6
    1,iwl6050-firmware,nothing,Not Uninstallable,41.28.5.1
    1,python,nothing,Not Uninstallable,2.6.6
    1,libreport-compat,nothing,Not Uninstallable,2.0.9
    1,libieee1284,nothing,Not Uninstallable,0.2.11
    1,libaio,nothing,Not Uninstallable,0.3.107
    1,Quicksilver,nothing,Not Uninstallable,1.2.1
    1,pulseaudio-module-bluetooth,nothing,Not Uninstallable,0.9.21
    1,pinentry-gtk,nothing,Not Uninstallable,0.7.6
    1,libXvMC,nothing,Not Uninstallable,1.0.7
    1,ethtool,nothing,Not Uninstallable,3.5
    1,SharedWorkerProcess,nothing,Not Uninstallable,9537
    1,TaniumClient,nothing,Not Uninstallable,5.1.314.7778
    1,festvox-slt-arctic-hts,nothing,Not Uninstallable,0.20061229
    1,libreport-plugin-kerneloops,nothing,Not Uninstallable,2.0.9
    1,iPhoto,nothing,Not Uninstallable,9.6
    1,pbm2l2030,nothing,Not Uninstallable,1.4
    1,Microsoft Remote Desktop,nothing,Not Uninstallable,8.0.25189
    1,libss,nothing,Not Uninstallable,1.41.12
    1,ghostscript-fonts,nothing,Not Uninstallable,5.50
    1,WebProcess,nothing,Not Uninstallable,9537
    1,sane-backends,nothing,Not Uninstallable,1.0.21
    1,libcdio,nothing,Not Uninstallable,0.81
    1,freetype,nothing,Not Uninstallable,2.3.11
    1,paktype-naqsh-fonts,nothing,Not Uninstallable,2.0
    1,BluetoothUIServer,nothing,Not Uninstallable,4.2.6
    1,psacct,nothing,Not Uninstallable,6.3.2
    2,CoreLocationAgent,nothing,Not Uninstallable,1486.12
    1,lohit-telugu-fonts,nothing,Not Uninstallable,2.4.5
    1,setuptool,nothing,Not Uninstallable,1.19.9
    2,KeyboardViewer,nothing,Not Uninstallable,3.2
    2,TrackpadIM,nothing,Not Uninstallable,1.5
    1,rhnlib,nothing,Not Uninstallable,2.5.22
    1,gstreamer-plugins-base,nothing,Not Uninstallable,0.10.29
    1,libsemanage,nothing,Not Uninstallable,2.0.43
    1,shared-mime-info,nothing,Not Uninstallable,0.70
    1,xz,nothing,Not Uninstallable,4.999.9
    1,libattr,nothing,Not Uninstallable,2.4.44
    1,words,nothing,Not Uninstallable,3.0
    1,libmusicbrainz3,nothing,Not Uninstallable,3.0.2
    1,crontabs,nothing,Not Uninstallable,1.10
    1,libtiff,nothing,Not Uninstallable,3.9.4
    1,iwl4965-firmware,nothing,Not Uninstallable,228.61.2.24
    2,Mission Control,nothing,Not Uninstallable,1.2
    2,EscrowSecurityAlert,nothing,Not Uninstallable,1.0
    1,rootfiles,nothing,Not Uninstallable,8.1
    1,libcom_err,nothing,Not Uninstallable,1.41.12
    1,SpeechRecognitionServer,nothing,Not Uninstallable,4.2.4
    1,Adobe Flash Player Install Manager,nothing,Not Uninstallable,15.0.0.239
    1,FindMyMacMessenger,nothing,Not Uninstallable,3.1
    1,gnome-bluetooth-libs,nothing,Not Uninstallable,2.28.6
    1,kernel-firmware,nothing,Not Uninstallable,2.6.32
    1,device-mapper-event,nothing,Not Uninstallable,1.02.77
    1,fuse,nothing,Not Uninstallable,2.8.3
    1,pinfo,nothing,Not Uninstallable,0.6.9
    2,Recursive File Processing Droplet,nothing,Not Uninstallable,1.0
    2,Launchpad,nothing,Not Uninstallable,1.0
    1,mozilla-filesystem,nothing,Not Uninstallable,1.9
    1,yum,nothing,Not Uninstallable,3.2.29
    1,PackageKit,nothing,Not Uninstallable,0.5.8
    1,libwacom,nothing,Not Uninstallable,0.5
    1,libuser-python,nothing,Not Uninstallable,0.56.13
    1,system-config-firewall-base,nothing,Not Uninstallable,1.2.27
    1,sound-theme-freedesktop,nothing,Not Uninstallable,0.7
    1,gstreamer-plugins-bad-free,nothing,Not Uninstallable,0.10.19
    2,Folder Actions Dispatcher,nothing,Not Uninstallable,1.0.4
    1,Type8Camera,nothing,Not Uninstallable,10.0
    2,DVD Player,nothing,Not Uninstallable,5.7
    1,cryptsetup-luks,nothing,Not Uninstallable,1.2.0
    1,Preview,nothing,Not Uninstallable,7.0
    1,scenery-backgrounds,nothing,Not Uninstallable,6.0.0
    1,ColorSync Utility,nothing,Not Uninstallable,4.9.0
    1,gnome-system-monitor,nothing,Not Uninstallable,2.28.0
    1,AirPort Base Station Agent,nothing,Not Uninstallable,2.2.1
    1,e2fsprogs,nothing,Not Uninstallable,1.41.12
    1,Microsoft Alerts Daemon,nothing,Not Uninstallable,14.4.6
    1,gnome-packagekit,nothing,Not Uninstallable,2.28.3
    1,libgtop2,nothing,Not Uninstallable,2.28.0
    1,libXau,nothing,Not Uninstallable,1.0.6
    1,libjpeg-turbo,nothing,Not Uninstallable,1.2.1
    1,Microsoft SQL Server 2012 Transact-SQL ScriptDom ,MsiExec.exe /X{0E8670B8-3965-4930-ADA6-570348B67153} /qn /noreboot,Is Uninstallable,11.0.2100.60
    1,Canon IJScanner2,nothing,Not Uninstallable,3.1.0
    1,gvfs-fuse,nothing,Not Uninstallable,1.4.3
    1,abrt-tui,nothing,Not Uninstallable,2.0.8
    1,SpeechSynthesisServer,nothing,Not Uninstallable,5.2.6
    1,Notes,nothing,Not Uninstallable,2.0
    1,cyrus-sasl-lib,nothing,Not Uninstallable,2.1.23
    1,xorg-x11-drv-evdev,nothing,Not Uninstallable,2.7.3
    1,python-mako,nothing,Not Uninstallable,0.3.4
    1,Image Capture,nothing,Not Uninstallable,6.3
    1,Cisco WebEx Start,nothing,Not Uninstallable,0.4.6
    1,Equation Editor,nothing,Not Uninstallable,14.2.0
    1,xorg-x11-drv-openchrome,nothing,Not Uninstallable,0.3.0
    1,thai-scalable-waree-fonts,nothing,Not Uninstallable,0.4.12
    1,Accessibility Inspector,nothing,Not Uninstallable,4.1
    1,libselinux,nothing,Not Uninstallable,2.0.94
    2,Grapher,nothing,Not Uninstallable,2.5
    2,RAID Utility,nothing,Not Uninstallable,4.0
    2,HelpViewer,nothing,Not Uninstallable,5.2
    1,libtool-ltdl,nothing,Not Uninstallable,2.2.6
    1,gnome-session,nothing,Not Uninstallable,2.28.0
    1,libgnomecanvas,nothing,Not Uninstallable,2.26.0
    2,UniversalAccessControl,nothing,Not Uninstallable,7.0
    1,man-pages-overrides,nothing,Not Uninstallable,6.4.1
    1,mesa-dri-drivers,nothing,Not Uninstallable,9.0
    1,libacl,nothing,Not Uninstallable,2.2.49
    1,yelp,nothing,Not Uninstallable,2.28.1
    1,sysvinit-tools,nothing,Not Uninstallable,2.87
    1,mailx,nothing,Not Uninstallable,12.4
    1,Calendar,nothing,Not Uninstallable,8.0
    1,ipw2100-firmware,nothing,Not Uninstallable,1.3
    1,lvm2-libs,nothing,Not Uninstallable,2.02.98
    1,iTunes,nothing,Not Uninstallable,12.0.1
    1,libdmx,nothing,Not Uninstallable,1.1.2
    1,plymouth-graphics-libs,nothing,Not Uninstallable,0.8.3
    1,redhat-bookmarks,nothing,Not Uninstallable,6
    1,device-mapper,nothing,Not Uninstallable,1.02.77
    1,vte,nothing,Not Uninstallable,0.25.1
    1,libXres,nothing,Not Uninstallable,1.0.6
    1,readahead,nothing,Not Uninstallable,1.5.6
    1,cpp,nothing,Not Uninstallable,4.4.7
    1,SpeechService,nothing,Not Uninstallable,4.7.1
    1,system-setup-keyboard,nothing,Not Uninstallable,0.7
    1,lohit-punjabi-fonts,nothing,Not Uninstallable,2.4.4
    1,gnome-settings-daemon,nothing,Not Uninstallable,2.28.2
    1,xorg-x11-drv-penmount,nothing,Not Uninstallable,1.5.0
    1,gnome-doc-utils-stylesheets,nothing,Not Uninstallable,0.18.1
    1,libXfont,nothing,Not Uninstallable,1.4.5
    1,httpd-tools,nothing,Not Uninstallable,2.2.15
    1,hwdata,nothing,Not Uninstallable,0.233
    1,gnome-disk-utility,nothing,Not Uninstallable,2.30.1
    1,AppleScript Editor,nothing,Not Uninstallable,2.6.1
    1,FindReaperFiles,nothing,Not Uninstallable,802
    1,Type4Camera,nothing,Not Uninstallable,9.2
    1,storeuid,nothing,Not Uninstallable,1.0
    1,system-config-users-docs,nothing,Not Uninstallable,1.0.8
    1,file-roller,nothing,Not Uninstallable,2.28.2
    1,libsepol,nothing,Not Uninstallable,2.0.41
    1,nano,nothing,Not Uninstallable,2.0.9
    1,libplist,nothing,Not Uninstallable,1.2
    1,tibetan-machine-uni-fonts,nothing,Not Uninstallable,1.901
    1,orca,nothing,Not Uninstallable,2.28.2
    1,python-dateutil,nothing,Not Uninstallable,1.4.1
    1,gcalctool,nothing,Not Uninstallable,5.28.2
    2,AppDownloadLauncher,nothing,Not Uninstallable,1.0
    1,ql2400-firmware,nothing,Not Uninstallable,5.08.00
    1,bind-libs,nothing,Not Uninstallable,9.8.2
    1,python-simplejson,nothing,Not Uninstallable,2.0.9
    1,gtk2,nothing,Not Uninstallable,2.18.9
    1,gdm-plugin-fingerprint,nothing,Not Uninstallable,2.30.4
    1,desktop-file-utils,nothing,Not Uninstallable,0.15
    1,rsyslog,nothing,Not Uninstallable,5.8.10
    1,keyutils-libs,nothing,Not Uninstallable,1.4
    1,systemtap-runtime,nothing,Not Uninstallable,1.8
    1,Microsoft VSS Writer for SQL Server 2012,MsiExec.exe /X{3E0DD83F-BE4C-4478-86A0-AD0D79D1353E} /qn /noreboot,Is Uninstallable,11.0.2100.60
    1,ppp,nothing,Not Uninstallable,2.4.5
    1,xorg-x11-drv-fpit,nothing,Not Uninstallable,1.4.0
    1,libnotify,nothing,Not Uninstallable,0.5.0
    1,xorg-x11-drv-fbdev,nothing,Not Uninstallable,0.4.3
    1,dejavu-sans-mono-fonts,nothing,Not Uninstallable,2.30
    1,gnome-python2,nothing,Not Uninstallable,2.28.0
    2,imagent,nothing,Not Uninstallable,10.0
    1,thai-scalable-fonts-common,nothing,Not Uninstallable,0.4.12
    1,usermode,nothing,Not Uninstallable,1.102
    1,iwl1000-firmware,nothing,Not Uninstallable,39.31.5.1
    1,libproxy-bin,nothing,Not Uninstallable,0.3.0
    1,perl-version,nothing,Not Uninstallable,0.77
    2,QuickLookUIHelper,nothing,Not Uninstallable,5.0
    1,cloog-ppl,nothing,Not Uninstallable,0.15.7
    1,libcap,nothing,Not Uninstallable,2.16
    1,blktrace,nothing,Not Uninstallable,1.0.1
    1,b43-openfwwf,nothing,Not Uninstallable,5.2
    1,dbus-c++,nothing,Not Uninstallable,0.5.0
    1,lsof,nothing,Not Uninstallable,4.82
    1,xorg-x11-drv-voodoo,nothing,Not Uninstallable,1.2.5
    1,redhat-release-server,nothing,Not Uninstallable,6Server
    1,bluez-libs,nothing,Not Uninstallable,4.66
    1,evince,nothing,Not Uninstallable,2.28.2
    1,VirtualScanner,nothing,Not Uninstallable,3.2
    1,python-gudev,nothing,Not Uninstallable,147.1
    1,gvfs-archive,nothing,Not Uninstallable,1.4.3
    1,Contacts,nothing,Not Uninstallable,9.0
    1,iMovie,nothing,Not Uninstallable,10.0.6
    1,Contacts,nothing,Not Uninstallable,8.0
    1,gnome-menus,nothing,Not Uninstallable,2.28.0
    1,Setup Assistant,nothing,Not Uninstallable,10.10
    1,YouTube,nothing,Not Uninstallable,37.0.2062.120
    1,elfutils-libs,nothing,Not Uninstallable,0.152
    1,hal,nothing,Not Uninstallable,0.5.14
    1,libgail-gnome,nothing,Not Uninstallable,1.20.1
    1,cairo,nothing,Not Uninstallable,1.8.8
    1,AirScanScanner,nothing,Not Uninstallable,9.4
    1,gnome-python2-libwnck,nothing,Not Uninstallable,2.28.0
    1,Reminders,nothing,Not Uninstallable,2.0
    1,libidn,nothing,Not Uninstallable,1.18
    1,gtkmm24,nothing,Not Uninstallable,2.18.2
    2,Folder Actions Setup,nothing,Not Uninstallable,1.1.6
    1,passwd,nothing,Not Uninstallable,0.77
    1,eggdbus,nothing,Not Uninstallable,0.6
    1,portreserve,nothing,Not Uninstallable,0.0.4
    1,tar,nothing,Not Uninstallable,1.23
    1,samba-common,nothing,Not Uninstallable,3.6.9
    1,PackageKit-glib,nothing,Not Uninstallable,0.5.8
    1,Kotoeri,nothing,Not Uninstallable,4.4.0
    1,libgnomeui,nothing,Not Uninstallable,2.24.1
    1,cracklib-dicts,nothing,Not Uninstallable,2.8.16
    1,cronie-anacron,nothing,Not Uninstallable,1.4.4
    1,yum-utils,nothing,Not Uninstallable,1.1.30
    1,Type5Camera,nothing,Not Uninstallable,9.2
    1,wavpack,nothing,Not Uninstallable,4.60
    1,UnmountAssistantAgent,nothing,Not Uninstallable,4.0
    1,mailcap,nothing,Not Uninstallable,2.1.31
    1,abrt-addon-ccpp,nothing,Not Uninstallable,2.0.8
    1,Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.4974,MsiExec.exe /X{B7E38540-E355-3503-AFD7-635B2F2F76E1} /qn /noreboot,Is Uninstallable,9.0.30729.4974
    1,gnome-python2-gnomekeyring,nothing,Not Uninstallable,2.28.0
    1,gnome-python2-gconf,nothing,Not Uninstallable,2.28.0
    1,dbus-x11,nothing,Not Uninstallable,1.2.24
    1,libproxy-python,nothing,Not Uninstallable,0.3.0
    1,Speech Downloader,nothing,Not Uninstallable,1.0
    1,python-slip-dbus,nothing,Not Uninstallable,0.2.20
    1,subscription-manager,nothing,Not Uninstallable,1.1.23
    1,SpeechSynthesisServer,nothing,Not Uninstallable,4.7.1
    1,lm_sensors-libs,nothing,Not Uninstallable,3.1.1
    1,dash,nothing,Not Uninstallable,0.5.5.1
    1,gnome-themes,nothing,Not Uninstallable,2.28.1
    1,Python,nothing,Not Uninstallable,2.6.8
    1,curl,nothing,Not Uninstallable,7.19.7
    1,lockdev,nothing,Not Uninstallable,1.0.1
    1,Microsoft Language Register,nothing,Not Uninstallable,14.4.6
    1,SQL Server Browser for SQL Server 2012,MsiExec.exe /X{4B9E6EB0-0EED-4E74-9479-F982C3254F71} /qn /noreboot,Is Uninstallable,11.0.2100.60
    1,libical,nothing,Not Uninstallable,0.43
    1,Activity Monitor,nothing,Not Uninstallable,10.10.0
    1,ImageCaptureService,nothing,Not Uninstallable,6.6
    1,rhn-setup,nothing,Not Uninstallable,1.0.0.1
    1,dbus-libs,nothing,Not Uninstallable,1.2.24
    1,sg3_utils-libs,nothing,Not Uninstallable,1.28
    1,cyrus-sasl,nothing,Not Uninstallable,2.1.23
    1,xorg-x11-drv-vesa,nothing,Not Uninstallable,2.3.2
    1,dmraid,nothing,Not Uninstallable,1.0.0.rc16
    1,atmsupload,nothing,Not Uninstallable,1408.13.2909.0
    1,system-config-date,nothing,Not Uninstallable,1.9.60
    1,paps,nothing,Not Uninstallable,0.6.8
    1,xkeyboard-config,nothing,Not Uninstallable,2.6
    1,krb5-libs,nothing,Not Uninstallable,1.10.3
    1,Uninstall VMware Tools,nothing,Not Uninstallable,9.8.3
    2,Network Utility,nothing,Not Uninstallable,1.8
    1,ppl,nothing,Not Uninstallable,0.10.2
    1,Safari,nothing,Not Uninstallable,7.0.5
    1,db4-utils,nothing,Not Uninstallable,4.7.25
    1,gawk,nothing,Not Uninstallable,3.1.7
    1,Canon IJScanner4,nothing,Not Uninstallable,2.3.0
    2,AirPlayUIAgent,nothing,Not Uninstallable,2.0
    1,audit,nothing,Not Uninstallable,2.2
    1,unzip,nothing,Not Uninstallable,6.0
    1,desktop-effects,nothing,Not Uninstallable,0.8.4
    1,convertpdf,nothing,Not Uninstallable,1.2
    1,crda,nothing,Not Uninstallable,1.1.1_2010.11.22
    1,flac,nothing,Not Uninstallable,1.2.1
    1,rhn-setup-gnome,nothing,Not Uninstallable,1.0.0.1
    1,iwl5150-firmware,nothing,Not Uninstallable,8.24.2.2
    2,Match,nothing,Not Uninstallable,None
    1,cjet,nothing,Not Uninstallable,0.8.9
    1,libXi,nothing,Not Uninstallable,1.6.1
    1,Tanium Client Deployment Tool,"""C:\Program Files (x86)\Tanium\Tanium Client Deployment Tool\uninstall.exe""",Not Uninstallable,4.0.0.0
    1,Setup Assistant,nothing,Not Uninstallable,10.9
    1,hal-libs,nothing,Not Uninstallable,0.5.14
    1,totem-nautilus,nothing,Not Uninstallable,2.28.6
    1,xorg-x11-drv-dummy,nothing,Not Uninstallable,0.3.6
    1,khmeros-base-fonts,nothing,Not Uninstallable,5.0
    1,libao,nothing,Not Uninstallable,0.8.8
    1,lvm2,nothing,Not Uninstallable,2.02.98
    1,xorg-x11-drv-i128,nothing,Not Uninstallable,1.3.6
    1,Font Book,nothing,Not Uninstallable,5.0
    1,libasyncns,nothing,Not Uninstallable,0.8
    1,subscription-manager-firstboot,nothing,Not Uninstallable,1.1.23
    2,AOSPushRelay,nothing,Not Uninstallable,1.06
    2,KoreanIM,nothing,Not Uninstallable,6.4
    1,Adobe Flash Player 15 ActiveX,C:\Windows\SysWOW64\Macromed\Flash\FlashUtil32_15_0_0_239_ActiveX.exe -maintain activex,Not Uninstallable,15.0.0.239
    1,wdaemon,nothing,Not Uninstallable,0.17
    1,avahi-glib,nothing,Not Uninstallable,0.6.25
    1,psutils,nothing,Not Uninstallable,1.17
    2,SecurityFixer,nothing,Not Uninstallable,10.8
    1,BluetoothUIServer,nothing,Not Uninstallable,4.3.1
    1,Python,nothing,Not Uninstallable,2.5.6
    1,libXrandr,nothing,Not Uninstallable,1.4.0
    1,elfutils,nothing,Not Uninstallable,0.152
    1,Canon IJScanner2,nothing,Not Uninstallable,1.5.1
    1,usbutils,nothing,Not Uninstallable,003
    1,xcb-util,nothing,Not Uninstallable,0.3.6
    1,Free42-Binary,nothing,Not Uninstallable,None
    1,rhnsd,nothing,Not Uninstallable,4.9.3
    1,un-core-dotum-fonts,nothing,Not Uninstallable,1.0.2
    1,libusb,nothing,Not Uninstallable,0.1.12
    1,at-spi-python,nothing,Not Uninstallable,1.28.1
    1,system-gnome-theme,nothing,Not Uninstallable,60.0.2
    1,gnome-python2-applet,nothing,Not Uninstallable,2.28.0
    1,pyorbit,nothing,Not Uninstallable,2.24.0
    1,fprintd,nothing,Not Uninstallable,0.1
    1,boost-filesystem,nothing,Not Uninstallable,1.41.0
    1,numactl,nothing,Not Uninstallable,2.0.7
    1,kbd,nothing,Not Uninstallable,1.15
    1,spice-vdagent,nothing,Not Uninstallable,0.12.0
    1,avahi-autoipd,nothing,Not Uninstallable,0.6.25
    1,foomatic-db-filesystem,nothing,Not Uninstallable,4.0
    1,pulseaudio-libs-glib2,nothing,Not Uninstallable,0.9.21
    1,Microsoft .NET Framework 4 Multi-Targeting Pack,MsiExec.exe /X{CFEF48A8-BFB8-3EAC-8BA5-DE4F8AA267CE} /qn /noreboot,Is Uninstallable,4.0.30319
    2,Show Info,nothing,Not Uninstallable,None
    2,Ticket Viewer,nothing,Not Uninstallable,4.0
    1,ImageCaptureService,nothing,Not Uninstallable,6.5
    1,apr-util-ldap,nothing,Not Uninstallable,1.3.9
    1,alsa-lib,nothing,Not Uninstallable,1.0.22
    1,Activity Monitor,nothing,Not Uninstallable,10.9.0
    1,samba-winbind,nothing,Not Uninstallable,3.6.9
    1,abrt-addon-kerneloops,nothing,Not Uninstallable,2.0.8
    1,gcc,nothing,Not Uninstallable,4.4.7
    2,AppleMobileSync,nothing,Not Uninstallable,5.0
    1,ConsoleKit,nothing,Not Uninstallable,0.4.1
    1,nss-util,nothing,Not Uninstallable,3.14.0.0
    1,genisoimage,nothing,Not Uninstallable,1.1.9
    1,gok,nothing,Not Uninstallable,2.28.1
    1,kernel,nothing,Not Uninstallable,2.6.32
    1,rfkill,nothing,Not Uninstallable,0.3
    2,ODSAgent,nothing,Not Uninstallable,1.8
    1,libdiscid,nothing,Not Uninstallable,0.2.2
    1,Microsoft Visual C++ 2010  x64 Redistributable - 10.0.40219,MsiExec.exe /X{1D8E6291-B0D5-35EC-8441-6616F567A0F7} /qn /noreboot,Is Uninstallable,10.0.40219
    1,xorg-x11-drv-vmmouse,nothing,Not Uninstallable,12.9.0
    1,libX11-common,nothing,Not Uninstallable,1.5.0
    1,hunspell,nothing,Not Uninstallable,1.2.8
    2,Droplet with Settable Properties,nothing,Not Uninstallable,1.0
    2,Remove,nothing,Not Uninstallable,None
    2,Cocoa-AppleScript Applet,nothing,Not Uninstallable,1.0
    1,python-iwlib,nothing,Not Uninstallable,0.1
    1,Calendar,nothing,Not Uninstallable,7.0
    2,Image Events,nothing,Not Uninstallable,1.1.6
    1,tmpwatch,nothing,Not Uninstallable,2.9.16
    1,hplip-libs,nothing,Not Uninstallable,3.12.4
    1,gstreamer-tools,nothing,Not Uninstallable,0.10.29
    1,gnome-user-docs,nothing,Not Uninstallable,2.28.0
    1,cdparanoia-libs,nothing,Not Uninstallable,10.2
    1,PrinterProxy,nothing,Not Uninstallable,10.0
    1,cups-libs,nothing,Not Uninstallable,1.4.2
    1,openjpeg-libs,nothing,Not Uninstallable,1.3
    1,AirPort Utility,nothing,Not Uninstallable,6.3.4
    1,Archive Utility,nothing,Not Uninstallable,10.10
    1,mlocate,nothing,Not Uninstallable,0.22.2
    2,Database Events,nothing,Not Uninstallable,1.0.6
    1,cups-pk-helper,nothing,Not Uninstallable,0.0.4
    1,Photo Booth,nothing,Not Uninstallable,6.0
    2,ChineseTextConverterService,nothing,Not Uninstallable,2.1
    1,Installer,nothing,Not Uninstallable,6.1.0
    1,libXt,nothing,Not Uninstallable,1.1.3
    1,xorg-x11-drv-qxl,nothing,Not Uninstallable,0.1.0
    1,nspluginwrapper,nothing,Not Uninstallable,1.4.4
    1,pangomm,nothing,Not Uninstallable,2.26.0
    1,pm-utils,nothing,Not Uninstallable,1.2.5
    1,JapaneseIM,nothing,Not Uninstallable,5.0
    1,speex,nothing,Not Uninstallable,1.2
    1,Calibration Assistant,nothing,Not Uninstallable,1.0
    1,jomolhari-fonts,nothing,Not Uninstallable,0.003
    1,Maps,nothing,Not Uninstallable,2.0
    1,compiz-gnome,nothing,Not Uninstallable,0.8.2
    1,microcode_ctl,nothing,Not Uninstallable,1.17
    1,pam,nothing,Not Uninstallable,1.1.1
    1,libxcb,nothing,Not Uninstallable,1.8.1
    1,traceroute,nothing,Not Uninstallable,2.0.14
    1,libedit,nothing,Not Uninstallable,2.11
    1,foomatic-db,nothing,Not Uninstallable,4.0
    1,pinentry,nothing,Not Uninstallable,0.7.6
    1,pygtk2-libglade,nothing,Not Uninstallable,2.16.0
    1,Microsoft Office Setup Assistant,nothing,Not Uninstallable,14.4.1
    1,PyCharm CE,nothing,Not Uninstallable,3.4.1
    1,libpanelappletmm,nothing,Not Uninstallable,2.26.0
    1,avahi-libs,nothing,Not Uninstallable,0.6.25
    1,libXScrnSaver,nothing,Not Uninstallable,1.2.2
    1,MassStorageCamera,nothing,Not Uninstallable,9.2
    1,gvfs-afc,nothing,Not Uninstallable,1.4.3
    1,Game Center,nothing,Not Uninstallable,2.0
    1,fontpackages-filesystem,nothing,Not Uninstallable,1.41
    1,stix-fonts,nothing,Not Uninstallable,0.9
    1,virt-what,nothing,Not Uninstallable,1.11
    2,Embed,nothing,Not Uninstallable,None
    1,vconfig,nothing,Not Uninstallable,1.9
    2,Spotlight,nothing,Not Uninstallable,1.0
    1,VirtualScanner,nothing,Not Uninstallable,4.0
    1,xulrunner,nothing,Not Uninstallable,10.0.12
    1,aic94xx-firmware,nothing,Not Uninstallable,30
    1,readline,nothing,Not Uninstallable,6.0
    1,alsa-utils,nothing,Not Uninstallable,1.0.22
    1,gnome-terminal,nothing,Not Uninstallable,2.31.3
    1,Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.6161,MsiExec.exe /X{5FCE6D76-F5DC-37AB-B2B8-22AB8CEDB1D4} /qn /noreboot,Is Uninstallable,9.0.30729.6161
    1,FileMerge,nothing,Not Uninstallable,2.8
    1,gnote,nothing,Not Uninstallable,0.6.3
    2,Software Update,nothing,Not Uninstallable,6
    1,gnome-disk-utility-libs,nothing,Not Uninstallable,2.30.1
    1,compiz,nothing,Not Uninstallable,0.8.2
    1,Microsoft AutoUpdate,nothing,Not Uninstallable,2.3.6
    1,irqbalance,nothing,Not Uninstallable,1.0.4
    1,UnmountAssistantAgent,nothing,Not Uninstallable,5.0
    1,gdm-libs,nothing,Not Uninstallable,2.30.4
    1,Microsoft .NET Framework 4.5.1,C:\Windows\Microsoft.NET\Framework64\v4.0.30319\SetupCache\v4.5.50938\\Setup.exe /repair /x86 /x64,Not Uninstallable,4.5.50938
    1,tcsh,nothing,Not Uninstallable,6.17
    1,abrt-cli,nothing,Not Uninstallable,2.0.8
    1,nss-sysinit,nothing,Not Uninstallable,3.14.0.0
    1,perl-Pod-Simple,nothing,Not Uninstallable,3.13
    1,Font Book,nothing,Not Uninstallable,5.0.1
    2,Messages,nothing,Not Uninstallable,8.0
    1,device-mapper-libs,nothing,Not Uninstallable,1.02.77
    1,Microsoft Database Utility,nothing,Not Uninstallable,14.4.6
    1,rcd,nothing,Not Uninstallable,325.7
    1,X11,nothing,Not Uninstallable,1.0
    1,fuse-libs,nothing,Not Uninstallable,2.8.3
    2,TCIM,nothing,Not Uninstallable,102
    1,plymouth-gdm-hooks,nothing,Not Uninstallable,0.8.3
    1,iCloudUserNotificationsd,nothing,Not Uninstallable,1.0
    1,VMware Tools,MsiExec.exe /X{8CF7A691-09D2-4659-8C84-0406A7B58AE7} /qn /noreboot,Is Uninstallable,9.8.4.2202052
    2,quicklookd,nothing,Not Uninstallable,5.0
    1,libblkid,nothing,Not Uninstallable,2.17.2
    1,CalendarFileHandler,nothing,Not Uninstallable,8.0
    1,gnome-python2-desktop,nothing,Not Uninstallable,2.28.0
    1,Problem Reporter,nothing,Not Uninstallable,10.10
    2,Recursive Image File Processing Droplet,nothing,Not Uninstallable,1.0
    1,dbus,nothing,Not Uninstallable,1.2.24
    1,iptables-ipv6,nothing,Not Uninstallable,1.4.7
    1,dnsmasq,nothing,Not Uninstallable,2.48
    1,glibmm24,nothing,Not Uninstallable,2.22.1
    1,xorg-x11-server-Xorg,nothing,Not Uninstallable,1.13.0
    1,Google Drive,nothing,Not Uninstallable,37.0.2062.120
    1,ncurses-libs,nothing,Not Uninstallable,5.7
    1,vlgothic-fonts,nothing,Not Uninstallable,20091202
    1,zlib,nothing,Not Uninstallable,1.2.3
    1,pbm2l7k,nothing,Not Uninstallable,990321
    2,CMFSyncAgent,nothing,Not Uninstallable,10.0
    1,attr,nothing,Not Uninstallable,2.4.44
    1,Microsoft Ship Asserts,nothing,Not Uninstallable,1.1.4
    1,openssh-server,nothing,Not Uninstallable,5.3p1
    1,Microsoft SQL Server 2012 Transact-SQL Compiler Service ,MsiExec.exe /X{BEB0F91E-F2EA-48A1-B938-7857ABF2A93D} /qn /noreboot,Is Uninstallable,11.0.2100.60
    1,dmz-cursor-themes,nothing,Not Uninstallable,0.4
    1,libreport-gtk,nothing,Not Uninstallable,2.0.9
    1,iwl3945-firmware,nothing,Not Uninstallable,15.32.2.9
    1,lohit-bengali-fonts,nothing,Not Uninstallable,2.4.3
    2,syncuid,nothing,Not Uninstallable,8.1
    1,AddressBookSync,nothing,Not Uninstallable,9.0
    2,Memory Slot Utility,nothing,Not Uninstallable,1.5.1
    1,zip,nothing,Not Uninstallable,3.0
    1,plymouth-plugin-label,nothing,Not Uninstallable,0.8.3
    1,xorg-x11-drv-hyperpen,nothing,Not Uninstallable,1.4.1
    1,AirPort Utility,nothing,Not Uninstallable,6.3.2
    1,c2050,nothing,Not Uninstallable,0.3b
    1,polkit-gnome,nothing,Not Uninstallable,0.96
    1,AddPrinter,nothing,Not Uninstallable,10.0
    1,ntsysv,nothing,Not Uninstallable,1.3.49.3
    1,SyncServicesAgent,nothing,Not Uninstallable,14.4.6
    1,gnome-python2-gnomevfs,nothing,Not Uninstallable,2.28.0
    1,sane-backends-libs-gphoto2,nothing,Not Uninstallable,1.0.21
    1,libXdamage,nothing,Not Uninstallable,1.1.3
    1,gnome-keyring,nothing,Not Uninstallable,2.28.2
    2,IMServicePlugInAgent,nothing,Not Uninstallable,10.0
    1,totem-mozplugin,nothing,Not Uninstallable,2.28.6
    1,totem-pl-parser,nothing,Not Uninstallable,2.28.3
    1,dejavu-sans-fonts,nothing,Not Uninstallable,2.30
    1,liberation-sans-fonts,nothing,Not Uninstallable,1.05.1.20090721
    1,Microsoft Query,nothing,Not Uninstallable,12.0.0
    1,System Image Utility,nothing,Not Uninstallable,10.9.4
    1,smc-meera-fonts,nothing,Not Uninstallable,04.2
    1,kpathsea,nothing,Not Uninstallable,2007
    1,libiec61883,nothing,Not Uninstallable,1.2.0
    1,Script Editor,nothing,Not Uninstallable,2.7
    1,pygtk2,nothing,Not Uninstallable,2.16.0
    1,libatasmart,nothing,Not Uninstallable,0.17
    2,AppleFileServer,nothing,Not Uninstallable,2.0
    1,usbmuxd,nothing,Not Uninstallable,1.0.2
    1,ColorSync Utility,nothing,Not Uninstallable,4.10.0
    1,RegisterPluginIMApp,nothing,Not Uninstallable,1.1
    1,gtksourceview2,nothing,Not Uninstallable,2.8.2
    1,Microsoft System CLR Types for SQL Server 2012 (x64),MsiExec.exe /X{F1949145-EB64-4DE7-9D81-E6D27937146C} /qn /noreboot,Is Uninstallable,11.0.2100.60
    1,Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.4148,MsiExec.exe /X{1F1C2DFC-2D24-3E06-BCB8-725134ADF989} /qn /noreboot,Is Uninstallable,9.0.30729.4148
    1,libarchive,nothing,Not Uninstallable,2.8.3
    1,System Preferences,nothing,Not Uninstallable,13.0
    1,paktype-tehreer-fonts,nothing,Not Uninstallable,2.0
    1,fontconfig,nothing,Not Uninstallable,2.8.0
    1,Finder,nothing,Not Uninstallable,10.10.1
    1,OBEXAgent,nothing,Not Uninstallable,4.2.6
    1,Tanium Client 6.0.314.1190,C:\Program Files (x86)\Tanium\Tanium Client\uninst.exe,Not Uninstallable,6.0.314.1190
    1,libcap-ng,nothing,Not Uninstallable,0.6.4
    1,MemoryCleanHelper,nothing,Not Uninstallable,1.0
    1,libsoup,nothing,Not Uninstallable,2.28.2
    1,geoclue,nothing,Not Uninstallable,0.11.1.1
    1,Microsoft Word,nothing,Not Uninstallable,14.4.6
    1,libXmu,nothing,Not Uninstallable,1.1.1
    1,libXext,nothing,Not Uninstallable,1.3.1
    1,tcp_wrappers-libs,nothing,Not Uninstallable,7.6
    1,Type4Camera,nothing,Not Uninstallable,10.0
    1,Pages,nothing,Not Uninstallable,5.5.1
    1,Canon IJScanner4,nothing,Not Uninstallable,3.1.0
    1,at,nothing,Not Uninstallable,3.1.10
    1,Microsoft Database Daemon,nothing,Not Uninstallable,14.4.6
    1,WebProcess,nothing,Not Uninstallable,10600
    1,Display Calibrator,nothing,Not Uninstallable,4.9.0
    1,xorg-x11-drv-elographics,nothing,Not Uninstallable,1.4.1
    1,libpciaccess,nothing,Not Uninstallable,0.13.1
    1,apr-util,nothing,Not Uninstallable,1.3.9
    1,xdg-utils,nothing,Not Uninstallable,1.0.2
    1,ScreenReaderUIServer,nothing,Not Uninstallable,7.0
    1,Image Capture Extension,nothing,Not Uninstallable,9.2
    2,PubSubAgent,nothing,Not Uninstallable,1.0.5
    1,rt73usb-firmware,nothing,Not Uninstallable,1.8
    1,xorg-x11-drv-siliconmotion,nothing,Not Uninstallable,1.7.7
    1,store_helper,nothing,Not Uninstallable,1.0
    1,rng-tools,nothing,Not Uninstallable,2
    1,audit-libs,nothing,Not Uninstallable,2.2
    1,FindMyMacMessenger,nothing,Not Uninstallable,4.1
    1,Network Diagnostics,nothing,Not Uninstallable,1.2
    1,Cisco WebEx Meeting Center,nothing,Not Uninstallable,1410.10.2910.1
    1,vim-common,nothing,Not Uninstallable,7.2.411
    1,xorg-x11-drv-s3virge,nothing,Not Uninstallable,1.10.6
    1,min12xxw,nothing,Not Uninstallable,0.0.9
    2,File Sync,nothing,Not Uninstallable,8.1
    1,Preview,nothing,Not Uninstallable,8.0
    1,zenity,nothing,Not Uninstallable,2.28.0
    1,xorg-x11-drv-savage,nothing,Not Uninstallable,2.3.6
    1,nautilus,nothing,Not Uninstallable,2.28.4
    1,Soundflowerbed,nothing,Not Uninstallable,1.0
    1,libglade2,nothing,Not Uninstallable,2.6.4
    1,ql2200-firmware,nothing,Not Uninstallable,2.02.08
    1,ql2500-firmware,nothing,Not Uninstallable,5.08.00
    1,GConf2,nothing,Not Uninstallable,2.28.0
    1,man-pages,nothing,Not Uninstallable,3.22
    1,ivtv-firmware,nothing,Not Uninstallable,20080701
    1,nss-softokn-freebl,nothing,Not Uninstallable,3.12.9
    1,xmlrpc-c,nothing,Not Uninstallable,1.16.24
    1,xorg-x11-drv-r128,nothing,Not Uninstallable,6.9.1
    1,abyssinica-fonts,nothing,Not Uninstallable,1.0
    1,libX11,nothing,Not Uninstallable,1.5.0
    1,plymouth-system-theme,nothing,Not Uninstallable,0.8.3
    1,libxml2,nothing,Not Uninstallable,2.7.6
    1,Network Recording Player,nothing,Not Uninstallable,2.2.0
    1,MAKEDEV,nothing,Not Uninstallable,3.24
    1,prezi,nothing,Not Uninstallable,r846
    1,QuickTime Player,nothing,Not Uninstallable,10.4
    1,cracklib,nothing,Not Uninstallable,2.8.16
    1,mcpp,nothing,Not Uninstallable,2.7.2
    2,KeyboardSetupAssistant,nothing,Not Uninstallable,10.7
    1,totem,nothing,Not Uninstallable,2.28.6
    2,nbagent,nothing,Not Uninstallable,1.0
    1,Wi-Fi,nothing,Not Uninstallable,1.0
    1,ncurses,nothing,Not Uninstallable,5.7
    1,logrotate,nothing,Not Uninstallable,3.7.8
    1,subscription-manager-gui,nothing,Not Uninstallable,1.1.23
    1,Jar Launcher,nothing,Not Uninstallable,14.8.0
    1,libXrender,nothing,Not Uninstallable,0.9.7
    1,gnome-mag,nothing,Not Uninstallable,0.15.9
    1,libxml2-python,nothing,Not Uninstallable,2.7.6
    1,fprintd-pam,nothing,Not Uninstallable,0.1
    1,xorg-x11-font-utils,nothing,Not Uninstallable,7.2
    1,samba-winbind-clients,nothing,Not Uninstallable,3.6.9
    1,grep,nothing,Not Uninstallable,2.6.3
    1,wireless-tools,nothing,Not Uninstallable,29
    1,mesa-libGLU,nothing,Not Uninstallable,9.0
    1,python-beaker,nothing,Not Uninstallable,1.3.1
    
