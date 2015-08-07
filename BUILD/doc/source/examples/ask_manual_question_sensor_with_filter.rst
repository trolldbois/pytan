
Ask manual question sensor with filter
==========================================================================================

Ask a manual question using human strings by referencing the name of a single sensor.

Also supply a sensor filter that limits the column data that is shown to values that contain Windows (which is short hand for regex match against .*Windows.*).

No sensor parameters, sensor filter options, question filters or question options supplied.

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
    kwargs["sensors"] = u'Operating System, that contains:Windows'
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
    2015-08-07 19:43:06,319 DEBUG    pytan.handler.QuestionPoller: ID 1291: id resolved to 1291
    2015-08-07 19:43:06,319 DEBUG    pytan.handler.QuestionPoller: ID 1291: expiration resolved to 2015-08-07T19:53:06
    2015-08-07 19:43:06,319 DEBUG    pytan.handler.QuestionPoller: ID 1291: query_text resolved to Get Operating System containing "Windows" from all machines
    2015-08-07 19:43:06,319 DEBUG    pytan.handler.QuestionPoller: ID 1291: id resolved to 1291
    2015-08-07 19:43:06,319 DEBUG    pytan.handler.QuestionPoller: ID 1291: Object Info resolved to Question ID: 1291, Query: Get Operating System containing "Windows" from all machines
    2015-08-07 19:43:06,322 DEBUG    pytan.handler.QuestionPoller: ID 1291: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:43:06,322 DEBUG    pytan.handler.QuestionPoller: ID 1291: Timing: Started: 2015-08-07 19:43:06.319827, Expiration: 2015-08-07 19:53:06, Override Timeout: None, Elapsed Time: 0:00:00.002785, Left till expiry: 0:09:59.677390, Loop Count: 1
    2015-08-07 19:43:06,322 INFO     pytan.handler.QuestionPoller: ID 1291: Progress Changed 0% (0 of 2)
    2015-08-07 19:43:11,327 DEBUG    pytan.handler.QuestionPoller: ID 1291: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:43:11,327 DEBUG    pytan.handler.QuestionPoller: ID 1291: Timing: Started: 2015-08-07 19:43:06.319827, Expiration: 2015-08-07 19:53:06, Override Timeout: None, Elapsed Time: 0:00:05.007434, Left till expiry: 0:09:54.672742, Loop Count: 2
    2015-08-07 19:43:11,327 INFO     pytan.handler.QuestionPoller: ID 1291: Progress Changed 50% (1 of 2)
    2015-08-07 19:43:16,332 DEBUG    pytan.handler.QuestionPoller: ID 1291: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-07 19:43:16,332 DEBUG    pytan.handler.QuestionPoller: ID 1291: Timing: Started: 2015-08-07 19:43:06.319827, Expiration: 2015-08-07 19:53:06, Override Timeout: None, Elapsed Time: 0:00:10.013151, Left till expiry: 0:09:49.667025, Loop Count: 3
    2015-08-07 19:43:16,333 INFO     pytan.handler.QuestionPoller: ID 1291: Progress Changed 100% (2 of 2)
    2015-08-07 19:43:16,333 INFO     pytan.handler.QuestionPoller: ID 1291: Reached Threshold of 99% (2 of 2)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'poller_object': <pytan.pollers.QuestionPoller object at 0x10a614dd0>,
     'poller_success': True,
     'question_object': <taniumpy.object_types.question.Question object at 0x10a614190>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10a5b9cd0>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Operating System containing "Windows" from all machines
    
    CSV Results of response: 
    Operating System
    [no results]
    Windows Server 2008 R2 Standard
    
