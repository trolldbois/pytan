
Ask manual question sensor with parameters and filter and options
==========================================================================================

Ask a manual question using human strings by referencing the name of a single sensor that takes parameters, but supplying only two of the four parameters that are used by the sensor.

Also supply a sensor filter that limits the column data that is shown to values that match the regex '.*Shared.*', and a sensor filter option that re-fetches any cached data that is older than 3600 seconds.

No question filters or question options supplied.

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
    kwargs["sensors"] = u'Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*}, that regex match:.*Shared.*, opt:max_data_age:3600'
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
    2015-08-06 14:48:37,947 DEBUG    pytan.handler.QuestionPoller: ID 86260: id resolved to 86260
    2015-08-06 14:48:37,947 DEBUG    pytan.handler.QuestionPoller: ID 86260: expiration resolved to 2015-08-06T14:58:38
    2015-08-06 14:48:37,947 DEBUG    pytan.handler.QuestionPoller: ID 86260: query_text resolved to Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] contains "Shared" from all machines
    2015-08-06 14:48:37,947 DEBUG    pytan.handler.QuestionPoller: ID 86260: id resolved to 86260
    2015-08-06 14:48:37,947 DEBUG    pytan.handler.QuestionPoller: ID 86260: Object Info resolved to Question ID: 86260, Query: Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] contains "Shared" from all machines
    2015-08-06 14:48:37,953 DEBUG    pytan.handler.QuestionPoller: ID 86260: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:48:37,953 DEBUG    pytan.handler.QuestionPoller: ID 86260: Timing: Started: 2015-08-06 14:48:37.947686, Expiration: 2015-08-06 14:58:38, Override Timeout: None, Elapsed Time: 0:00:00.005818, Left till expiry: 0:10:00.046502, Loop Count: 1
    2015-08-06 14:48:37,953 INFO     pytan.handler.QuestionPoller: ID 86260: Progress Changed 0% (0 of 2)
    2015-08-06 14:48:42,960 DEBUG    pytan.handler.QuestionPoller: ID 86260: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:48:42,960 DEBUG    pytan.handler.QuestionPoller: ID 86260: Timing: Started: 2015-08-06 14:48:37.947686, Expiration: 2015-08-06 14:58:38, Override Timeout: None, Elapsed Time: 0:00:05.012997, Left till expiry: 0:09:55.039320, Loop Count: 2
    2015-08-06 14:48:47,971 DEBUG    pytan.handler.QuestionPoller: ID 86260: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:48:47,971 DEBUG    pytan.handler.QuestionPoller: ID 86260: Timing: Started: 2015-08-06 14:48:37.947686, Expiration: 2015-08-06 14:58:38, Override Timeout: None, Elapsed Time: 0:00:10.023959, Left till expiry: 0:09:50.028357, Loop Count: 3
    2015-08-06 14:48:52,979 DEBUG    pytan.handler.QuestionPoller: ID 86260: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:48:52,979 DEBUG    pytan.handler.QuestionPoller: ID 86260: Timing: Started: 2015-08-06 14:48:37.947686, Expiration: 2015-08-06 14:58:38, Override Timeout: None, Elapsed Time: 0:00:15.032193, Left till expiry: 0:09:45.020124, Loop Count: 4
    2015-08-06 14:48:57,986 DEBUG    pytan.handler.QuestionPoller: ID 86260: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 85
    2015-08-06 14:48:57,986 DEBUG    pytan.handler.QuestionPoller: ID 86260: Timing: Started: 2015-08-06 14:48:37.947686, Expiration: 2015-08-06 14:58:38, Override Timeout: None, Elapsed Time: 0:00:20.039212, Left till expiry: 0:09:40.013105, Loop Count: 5
    2015-08-06 14:48:57,986 INFO     pytan.handler.QuestionPoller: ID 86260: Progress Changed 50% (1 of 2)
    2015-08-06 14:49:02,998 DEBUG    pytan.handler.QuestionPoller: ID 86260: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 86
    2015-08-06 14:49:02,998 DEBUG    pytan.handler.QuestionPoller: ID 86260: Timing: Started: 2015-08-06 14:48:37.947686, Expiration: 2015-08-06 14:58:38, Override Timeout: None, Elapsed Time: 0:00:25.050499, Left till expiry: 0:09:35.001817, Loop Count: 6
    2015-08-06 14:49:02,998 INFO     pytan.handler.QuestionPoller: ID 86260: Progress Changed 100% (2 of 2)
    2015-08-06 14:49:02,998 INFO     pytan.handler.QuestionPoller: ID 86260: Reached Threshold of 99% (2 of 2)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'poller_object': <pytan.pollers.QuestionPoller object at 0x1113adc10>,
     'poller_success': True,
     'question_object': <taniumpy.object_types.question.Question object at 0x10fc74c90>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x111383910>}
    
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
