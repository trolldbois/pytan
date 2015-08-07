
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


    Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
    2015-08-07 19:42:26,175 DEBUG    pytan.handler.QuestionPoller: ID 1289: id resolved to 1289
    2015-08-07 19:42:26,175 DEBUG    pytan.handler.QuestionPoller: ID 1289: expiration resolved to 2015-08-07T19:52:26
    2015-08-07 19:42:26,175 DEBUG    pytan.handler.QuestionPoller: ID 1289: query_text resolved to Get Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*] containing "Shared" from all machines
    2015-08-07 19:42:26,175 DEBUG    pytan.handler.QuestionPoller: ID 1289: id resolved to 1289
    2015-08-07 19:42:26,175 DEBUG    pytan.handler.QuestionPoller: ID 1289: Object Info resolved to Question ID: 1289, Query: Get Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*] containing "Shared" from all machines
    2015-08-07 19:42:26,178 DEBUG    pytan.handler.QuestionPoller: ID 1289: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:42:26,178 DEBUG    pytan.handler.QuestionPoller: ID 1289: Timing: Started: 2015-08-07 19:42:26.175595, Expiration: 2015-08-07 19:52:26, Override Timeout: None, Elapsed Time: 0:00:00.003209, Left till expiry: 0:09:59.821198, Loop Count: 1
    2015-08-07 19:42:26,178 INFO     pytan.handler.QuestionPoller: ID 1289: Progress Changed 0% (0 of 2)
    2015-08-07 19:42:31,183 DEBUG    pytan.handler.QuestionPoller: ID 1289: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:42:31,183 DEBUG    pytan.handler.QuestionPoller: ID 1289: Timing: Started: 2015-08-07 19:42:26.175595, Expiration: 2015-08-07 19:52:26, Override Timeout: None, Elapsed Time: 0:00:05.007532, Left till expiry: 0:09:54.816876, Loop Count: 2
    2015-08-07 19:42:36,189 DEBUG    pytan.handler.QuestionPoller: ID 1289: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 74
    2015-08-07 19:42:36,189 DEBUG    pytan.handler.QuestionPoller: ID 1289: Timing: Started: 2015-08-07 19:42:26.175595, Expiration: 2015-08-07 19:52:26, Override Timeout: None, Elapsed Time: 0:00:10.013871, Left till expiry: 0:09:49.810537, Loop Count: 3
    2015-08-07 19:42:36,189 INFO     pytan.handler.QuestionPoller: ID 1289: Progress Changed 50% (1 of 2)
    2015-08-07 19:42:41,193 DEBUG    pytan.handler.QuestionPoller: ID 1289: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 74
    2015-08-07 19:42:41,194 DEBUG    pytan.handler.QuestionPoller: ID 1289: Timing: Started: 2015-08-07 19:42:26.175595, Expiration: 2015-08-07 19:52:26, Override Timeout: None, Elapsed Time: 0:00:15.018395, Left till expiry: 0:09:44.806014, Loop Count: 4
    2015-08-07 19:42:46,197 DEBUG    pytan.handler.QuestionPoller: ID 1289: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 74
    2015-08-07 19:42:46,197 DEBUG    pytan.handler.QuestionPoller: ID 1289: Timing: Started: 2015-08-07 19:42:26.175595, Expiration: 2015-08-07 19:52:26, Override Timeout: None, Elapsed Time: 0:00:20.022228, Left till expiry: 0:09:39.802180, Loop Count: 5
    2015-08-07 19:42:51,202 DEBUG    pytan.handler.QuestionPoller: ID 1289: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 74
    2015-08-07 19:42:51,202 DEBUG    pytan.handler.QuestionPoller: ID 1289: Timing: Started: 2015-08-07 19:42:26.175595, Expiration: 2015-08-07 19:52:26, Override Timeout: None, Elapsed Time: 0:00:25.027182, Left till expiry: 0:09:34.797226, Loop Count: 6
    2015-08-07 19:42:56,207 DEBUG    pytan.handler.QuestionPoller: ID 1289: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 75
    2015-08-07 19:42:56,207 DEBUG    pytan.handler.QuestionPoller: ID 1289: Timing: Started: 2015-08-07 19:42:26.175595, Expiration: 2015-08-07 19:52:26, Override Timeout: None, Elapsed Time: 0:00:30.031740, Left till expiry: 0:09:29.792668, Loop Count: 7
    2015-08-07 19:42:56,207 INFO     pytan.handler.QuestionPoller: ID 1289: Progress Changed 100% (2 of 2)
    2015-08-07 19:42:56,207 INFO     pytan.handler.QuestionPoller: ID 1289: Reached Threshold of 99% (2 of 2)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'poller_object': <pytan.pollers.QuestionPoller object at 0x10a614f50>,
     'poller_success': True,
     'question_object': <taniumpy.object_types.question.Question object at 0x10a5f5190>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10a615c10>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*] containing "Shared" from all machines
    
    CSV Results of response: 
    "Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*]"
    [no results]
    C:\Program Files\Common Files\Microsoft Shared\VS7Debug
    C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
    C:\Program Files\Common Files\Microsoft Shared\ink\ru-RU
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\keypad
    C:\Program Files\Common Files\Microsoft Shared\ink
    C:\Program Files\Common Files\Microsoft Shared\ink\sv-SE
    C:\Program Files\Common Files\Microsoft Shared\ink\uk-UA
    C:\Program Files\Common Files\Microsoft Shared\ink\sl-SI
    C:\Program Files\Common Files\Microsoft Shared\ink\hu-HU
    C:\Program Files\Common Files\Microsoft Shared\ink\zh-TW
    C:\Program Files\Common Files\Microsoft Shared\ink\zh-CN
    C:\Program Files\Common Files\Microsoft Shared\ink\fi-FI
    C:\Program Files\Common Files\Microsoft Shared
    ..trimmed for brevity..
