
Ask manual question sensor with parameters and filter
==========================================================================================

Ask a manual question using human strings by referencing the name of a single sensor that takes parameters, but supplying only two of the four parameters that are used by the sensor.

Also supply a sensor filter that limits the column data that is shown to values that match the regex '.*Shared.*'.

No sensor filter options, question filters, or question options supplied.

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
    kwargs["sensors"] = u'Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*}, that regex match:.*Shared.*'
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


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
    2015-08-06 14:47:52,475 DEBUG    pytan.handler.QuestionPoller: ID 86256: id resolved to 86256
    2015-08-06 14:47:52,475 DEBUG    pytan.handler.QuestionPoller: ID 86256: expiration resolved to 2015-08-06T14:57:52
    2015-08-06 14:47:52,475 DEBUG    pytan.handler.QuestionPoller: ID 86256: query_text resolved to Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] contains "Shared" from all machines
    2015-08-06 14:47:52,475 DEBUG    pytan.handler.QuestionPoller: ID 86256: id resolved to 86256
    2015-08-06 14:47:52,475 DEBUG    pytan.handler.QuestionPoller: ID 86256: Object Info resolved to Question ID: 86256, Query: Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] contains "Shared" from all machines
    2015-08-06 14:47:52,480 DEBUG    pytan.handler.QuestionPoller: ID 86256: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:47:52,480 DEBUG    pytan.handler.QuestionPoller: ID 86256: Timing: Started: 2015-08-06 14:47:52.476011, Expiration: 2015-08-06 14:57:52, Override Timeout: None, Elapsed Time: 0:00:00.004571, Left till expiry: 0:09:59.519420, Loop Count: 1
    2015-08-06 14:47:52,480 INFO     pytan.handler.QuestionPoller: ID 86256: Progress Changed 0% (0 of 2)
    2015-08-06 14:47:57,488 DEBUG    pytan.handler.QuestionPoller: ID 86256: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:47:57,488 DEBUG    pytan.handler.QuestionPoller: ID 86256: Timing: Started: 2015-08-06 14:47:52.476011, Expiration: 2015-08-06 14:57:52, Override Timeout: None, Elapsed Time: 0:00:05.012248, Left till expiry: 0:09:54.511745, Loop Count: 2
    2015-08-06 14:48:02,495 DEBUG    pytan.handler.QuestionPoller: ID 86256: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 85
    2015-08-06 14:48:02,496 DEBUG    pytan.handler.QuestionPoller: ID 86256: Timing: Started: 2015-08-06 14:47:52.476011, Expiration: 2015-08-06 14:57:52, Override Timeout: None, Elapsed Time: 0:00:10.019998, Left till expiry: 0:09:49.503993, Loop Count: 3
    2015-08-06 14:48:02,496 INFO     pytan.handler.QuestionPoller: ID 86256: Progress Changed 50% (1 of 2)
    2015-08-06 14:48:07,503 DEBUG    pytan.handler.QuestionPoller: ID 86256: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 85
    2015-08-06 14:48:07,503 DEBUG    pytan.handler.QuestionPoller: ID 86256: Timing: Started: 2015-08-06 14:47:52.476011, Expiration: 2015-08-06 14:57:52, Override Timeout: None, Elapsed Time: 0:00:15.027931, Left till expiry: 0:09:44.496060, Loop Count: 4
    2015-08-06 14:48:12,512 DEBUG    pytan.handler.QuestionPoller: ID 86256: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 85
    2015-08-06 14:48:12,513 DEBUG    pytan.handler.QuestionPoller: ID 86256: Timing: Started: 2015-08-06 14:47:52.476011, Expiration: 2015-08-06 14:57:52, Override Timeout: None, Elapsed Time: 0:00:20.037014, Left till expiry: 0:09:39.486979, Loop Count: 5
    2015-08-06 14:48:17,522 DEBUG    pytan.handler.QuestionPoller: ID 86256: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 86
    2015-08-06 14:48:17,522 DEBUG    pytan.handler.QuestionPoller: ID 86256: Timing: Started: 2015-08-06 14:47:52.476011, Expiration: 2015-08-06 14:57:52, Override Timeout: None, Elapsed Time: 0:00:25.046116, Left till expiry: 0:09:34.477875, Loop Count: 6
    2015-08-06 14:48:17,522 INFO     pytan.handler.QuestionPoller: ID 86256: Progress Changed 100% (2 of 2)
    2015-08-06 14:48:17,522 INFO     pytan.handler.QuestionPoller: ID 86256: Reached Threshold of 99% (2 of 2)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'poller_object': <pytan.pollers.QuestionPoller object at 0x10f833c50>,
     'poller_success': True,
     'question_object': <taniumpy.object_types.question.Question object at 0x1113ad310>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10fbf8690>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] contains "Shared" from all machines
    
    CSV Results of response: 
    "Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*]"
    [no results]
    C:\Program Files\Common Files\Microsoft Shared\VS7Debug
    C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
    C:\Program Files\Common Files\Microsoft Shared\ink\ru-RU
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\keypad
    C:\Program Files\Common Files\Microsoft Shared\ink
    C:\Program Files\Common Files\Microsoft Shared\ink\sv-SE
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2977326\GDR\1033_enu_lp\x64\setup\sqlsupport_msi\pfiles32\sqlservr\110\shared
    C:\Program Files\Common Files\Microsoft Shared\ink\uk-UA
    C:\Program Files\Common Files\Microsoft Shared\ink\sl-SI
    C:\Program Files\Common Files\Microsoft Shared\ink\hu-HU
    C:\Program Files\Common Files\Microsoft Shared\ink\zh-TW
    C:\Program Files\Common Files\Microsoft Shared\ink\zh-CN
    C:\Program Files\Common Files\Microsoft Shared\ink\fi-FI
    ..trimmed for brevity..
