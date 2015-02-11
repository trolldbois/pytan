
Ask saved question by name
==========================================================================================
Ask a saved question by referencing the name of a saved question in a string.

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
    kwargs["name"] = u'Installed Applications'
    
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
    out = out.getvalue()
    if len(out.splitlines()) > 15:
        out = out.splitlines()[0:15]
        out.append('..trimmed for brevity..')
        out = '\n'.join(out)
    print out
    


Output from Python Code
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
    2015-02-11 11:59:06,525 INFO     question_progress: Results 20000% (Get Installed Applications from all machines)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'question_object': <taniumpy.object_types.saved_question.SavedQuestion object at 0x105a35550>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x105c41d10>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Installed Applications from all machines
    
    CSV Results of response: 
    Name,Silent Uninstall String,Uninstallable,Version
    Google Search,nothing,Not Uninstallable,37.0.2062.120
    Microsoft Chart Converter,nothing,Not Uninstallable,14.4.7
    Spotify,nothing,Not Uninstallable,0.9.15.27.g87efe634
    Wish,nothing,Not Uninstallable,8.5.9
    BluetoothUIServer,nothing,Not Uninstallable,4.3.2
    Time Machine,nothing,Not Uninstallable,1.3
    AppleGraphicsWarning,nothing,Not Uninstallable,2.3.0
    Python 2.7 py2exe-0.6.9,"""C:\Python27\Removepy2exe.exe"" -u ""C:\Python27\py2exe-wininst.log""",Not Uninstallable,-0.6.9
    soagent,nothing,Not Uninstallable,7.0
    AinuIM,nothing,Not Uninstallable,1.0
    ARDAgent,nothing,Not Uninstallable,3.8.2
    Microsoft Clip Gallery,nothing,Not Uninstallable,14.4.7
    Pass Viewer,nothing,Not Uninstallable,1.0
    PressAndHold,nothing,Not Uninstallable,1.2
    ..trimmed for brevity..
