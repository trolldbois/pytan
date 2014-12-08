
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
    2014-12-08 16:19:51,778 INFO     question_progress: Results 60000% (Get Installed Applications from all machines)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'question_object': <taniumpy.object_types.saved_question.SavedQuestion object at 0x102b24790>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x1029e7fd0>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Installed Applications from all machines
    
    CSV Results of response: 
    Count,Name,Silent Uninstall String,Uninstallable,Version
    714,[too many results],None,None,None
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
    ..trimmed for brevity..
