
Ask saved question refresh data
==========================================================================================

Ask a saved question and refresh the data for the saved question (asks a new question)

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
    PORT = "443"
    
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
    kwargs["refresh_data"] = True
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
----------------------------------------------------------------------------------------

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
    2015-08-07 19:37:49,991 DEBUG    pytan.handler.QuestionPoller: ID 1279: id resolved to 1279
    2015-08-07 19:37:49,991 DEBUG    pytan.handler.QuestionPoller: ID 1279: expiration resolved to 2015-08-07T19:47:50
    2015-08-07 19:37:49,991 DEBUG    pytan.handler.QuestionPoller: ID 1279: query_text resolved to Get number of machines
    2015-08-07 19:37:49,991 DEBUG    pytan.handler.QuestionPoller: ID 1279: id resolved to 1279
    2015-08-07 19:37:49,991 DEBUG    pytan.handler.QuestionPoller: ID 1279: Object Info resolved to Question ID: 1279, Query: Get number of machines
    2015-08-07 19:37:49,997 DEBUG    pytan.handler.QuestionPoller: ID 1279: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:37:49,997 DEBUG    pytan.handler.QuestionPoller: ID 1279: Timing: Started: 2015-08-07 19:37:49.991362, Expiration: 2015-08-07 19:47:50, Override Timeout: None, Elapsed Time: 0:00:00.006572, Left till expiry: 0:10:00.002069, Loop Count: 1
    2015-08-07 19:37:49,997 INFO     pytan.handler.QuestionPoller: ID 1279: Progress Changed 0% (0 of 2)
    2015-08-07 19:37:55,007 DEBUG    pytan.handler.QuestionPoller: ID 1279: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 386
    2015-08-07 19:37:55,008 DEBUG    pytan.handler.QuestionPoller: ID 1279: Timing: Started: 2015-08-07 19:37:49.991362, Expiration: 2015-08-07 19:47:50, Override Timeout: None, Elapsed Time: 0:00:05.016686, Left till expiry: 0:09:54.991955, Loop Count: 2
    2015-08-07 19:37:55,008 INFO     pytan.handler.QuestionPoller: ID 1279: Progress Changed 100% (2 of 2)
    2015-08-07 19:37:55,008 INFO     pytan.handler.QuestionPoller: ID 1279: Reached Threshold of 99% (2 of 2)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'poller_object': <pytan.pollers.QuestionPoller object at 0x10a6c0410>,
     'poller_success': True,
     'question_object': <taniumpy.object_types.question.Question object at 0x10a7e7f50>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10a808190>,
     'saved_question_object': <taniumpy.object_types.saved_question.SavedQuestion object at 0x10a7ecb90>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get number of machines
    
    CSV Results of response: 
    Name,Silent Uninstall String,Uninstallable,Version
    Image Capture Extension,nothing,Not Uninstallable,10.2
    Dictation,nothing,Not Uninstallable,1.6.1
    Wish,nothing,Not Uninstallable,8.5.9
    Uninstall AnyConnect,nothing,Not Uninstallable,3.1.08009
    Time Machine,nothing,Not Uninstallable,1.3
    AppleGraphicsWarning,nothing,Not Uninstallable,2.3.0
    soagent,nothing,Not Uninstallable,7.0
    Feedback Assistant,nothing,Not Uninstallable,4.1.3
    AinuIM,nothing,Not Uninstallable,1.0
    vpndownloader,nothing,Not Uninstallable,3.1.08009
    Pass Viewer,nothing,Not Uninstallable,1.0
    ARDAgent,nothing,Not Uninstallable,3.8.4
    OBEXAgent,nothing,Not Uninstallable,4.3.5
    PressAndHold,nothing,Not Uninstallable,1.2
    ..trimmed for brevity..
