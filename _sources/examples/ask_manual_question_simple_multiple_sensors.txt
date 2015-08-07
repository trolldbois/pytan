
Ask manual question simple multiple sensors
==========================================================================================

Ask a manual question using human strings by referencing the name of multiple sensors in a list.

No sensor filters, sensor parameters, sensor filter options, question filters, or question options supplied.

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
    kwargs["sensors"] = [u'Computer Name', u'Installed Applications']
    kwargs["qtype"] = u'manual'
    
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
    2015-08-07 19:37:55,255 DEBUG    pytan.handler.QuestionPoller: ID 1280: id resolved to 1280
    2015-08-07 19:37:55,255 DEBUG    pytan.handler.QuestionPoller: ID 1280: expiration resolved to 2015-08-07T19:47:55
    2015-08-07 19:37:55,255 DEBUG    pytan.handler.QuestionPoller: ID 1280: query_text resolved to Get Computer Name and Installed Applications from all machines
    2015-08-07 19:37:55,255 DEBUG    pytan.handler.QuestionPoller: ID 1280: id resolved to 1280
    2015-08-07 19:37:55,255 DEBUG    pytan.handler.QuestionPoller: ID 1280: Object Info resolved to Question ID: 1280, Query: Get Computer Name and Installed Applications from all machines
    2015-08-07 19:37:55,260 DEBUG    pytan.handler.QuestionPoller: ID 1280: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:37:55,260 DEBUG    pytan.handler.QuestionPoller: ID 1280: Timing: Started: 2015-08-07 19:37:55.255851, Expiration: 2015-08-07 19:47:55, Override Timeout: None, Elapsed Time: 0:00:00.004752, Left till expiry: 0:09:59.739401, Loop Count: 1
    2015-08-07 19:37:55,260 INFO     pytan.handler.QuestionPoller: ID 1280: Progress Changed 0% (0 of 2)
    2015-08-07 19:38:00,263 DEBUG    pytan.handler.QuestionPoller: ID 1280: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:38:00,263 DEBUG    pytan.handler.QuestionPoller: ID 1280: Timing: Started: 2015-08-07 19:37:55.255851, Expiration: 2015-08-07 19:47:55, Override Timeout: None, Elapsed Time: 0:00:05.008121, Left till expiry: 0:09:54.736030, Loop Count: 2
    2015-08-07 19:38:00,264 INFO     pytan.handler.QuestionPoller: ID 1280: Progress Changed 50% (1 of 2)
    2015-08-07 19:38:05,271 DEBUG    pytan.handler.QuestionPoller: ID 1280: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:38:05,271 DEBUG    pytan.handler.QuestionPoller: ID 1280: Timing: Started: 2015-08-07 19:37:55.255851, Expiration: 2015-08-07 19:47:55, Override Timeout: None, Elapsed Time: 0:00:10.015351, Left till expiry: 0:09:49.728800, Loop Count: 3
    2015-08-07 19:38:10,277 DEBUG    pytan.handler.QuestionPoller: ID 1280: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-07 19:38:10,277 DEBUG    pytan.handler.QuestionPoller: ID 1280: Timing: Started: 2015-08-07 19:37:55.255851, Expiration: 2015-08-07 19:47:55, Override Timeout: None, Elapsed Time: 0:00:15.021396, Left till expiry: 0:09:44.722755, Loop Count: 4
    2015-08-07 19:38:10,277 INFO     pytan.handler.QuestionPoller: ID 1280: Progress Changed 100% (2 of 2)
    2015-08-07 19:38:10,277 INFO     pytan.handler.QuestionPoller: ID 1280: Reached Threshold of 99% (2 of 2)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'poller_object': <pytan.pollers.QuestionPoller object at 0x10a808810>,
     'poller_success': True,
     'question_object': <taniumpy.object_types.question.Question object at 0x10a810650>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10a6c0410>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Computer Name and Installed Applications from all machines
    
    CSV Results of response: 
    Computer Name,Name,Silent Uninstall String,Uninstallable,Version
    Casus-Belli.local,"Image Capture Extension
    Dictation
    Wish
    Uninstall AnyConnect
    Time Machine
    AppleGraphicsWarning
    soagent
    Feedback Assistant
    AinuIM
    vpndownloader
    Pass Viewer
    ARDAgent
    OBEXAgent
    PressAndHold
    ..trimmed for brevity..
