
Ask saved question by name in list
==========================================================================================

Ask a saved question by referencing the name of a saved question in a list of strings.

Example Python Code
----------------------------------------------------------------------------------------

.. code-block:: python
    :linenos:


    
    import os
    import sys
    sys.dont_write_bytecode = True
    
    # Determine our script name, script dir
    my_file = os.path.abspath(sys.argv[0])
    my_dir = os.path.dirname(my_file)
    
    # determine the pytan lib dir and add it to the path
    parent_dir = os.path.dirname(my_dir)
    pytan_root_dir = os.path.dirname(parent_dir)
    lib_dir = os.path.join(pytan_root_dir, 'lib')
    path_adds = [lib_dir]
    
    for aa in path_adds:
        if aa not in sys.path:
            sys.path.append(aa)
    
    
    # connection info for Tanium Server
    USERNAME = "Tanium User"
    PASSWORD = "T@n!um"
    HOST = "172.16.31.128"
    PORT = "444"
    
    # Logging conrols
    LOGLEVEL = 2
    DEBUGFORMAT = False
    
    import tempfile
    
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
    out = out.getvalue()
    if len(out.splitlines()) > 15:
        out = out.splitlines()[0:15]
        out.append('..trimmed for brevity..')
        out = '\n'.join(out)
    print out
    


Output from Python Code
----------------------------------------------------------------------------------------

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
    2015-03-26 11:37:59,316 INFO     question_progress: Results 100% (Get Installed Applications from all machines)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'question_object': <taniumpy.object_types.saved_question.SavedQuestion object at 0x107608b90>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x107646690>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Installed Applications from all machines
    
    CSV Results of response: 
    Name,Silent Uninstall String,Uninstallable,Version
    Google Search,nothing,Not Uninstallable,37.0.2062.120
    Microsoft Chart Converter,nothing,Not Uninstallable,14.4.7
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
    PluginIM,nothing,Not Uninstallable,15
    ..trimmed for brevity..
