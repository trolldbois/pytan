
Ask manual question sensor without parameters and supplied parameters
==========================================================================================

Ask a manual question using human strings by referencing the name of a single sensor that does NOT take parameters, but supplying parameters anyways (which will be ignored since the sensor does not take parameters).

No sensor filters, sensor filter options, question filters, or question options supplied.

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
    kwargs["sensors"] = u'Computer Name{fake=Dweedle}'
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
    2015-08-07 19:41:25,887 DEBUG    pytan.handler.QuestionPoller: ID 1286: id resolved to 1286
    2015-08-07 19:41:25,887 DEBUG    pytan.handler.QuestionPoller: ID 1286: expiration resolved to 2015-08-07T19:51:26
    2015-08-07 19:41:25,887 DEBUG    pytan.handler.QuestionPoller: ID 1286: query_text resolved to Get Computer Name[Dweedle] from all machines
    2015-08-07 19:41:25,887 DEBUG    pytan.handler.QuestionPoller: ID 1286: id resolved to 1286
    2015-08-07 19:41:25,887 DEBUG    pytan.handler.QuestionPoller: ID 1286: Object Info resolved to Question ID: 1286, Query: Get Computer Name[Dweedle] from all machines
    2015-08-07 19:41:25,892 DEBUG    pytan.handler.QuestionPoller: ID 1286: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:41:25,892 DEBUG    pytan.handler.QuestionPoller: ID 1286: Timing: Started: 2015-08-07 19:41:25.887268, Expiration: 2015-08-07 19:51:26, Override Timeout: None, Elapsed Time: 0:00:00.005356, Left till expiry: 0:10:00.107378, Loop Count: 1
    2015-08-07 19:41:25,892 INFO     pytan.handler.QuestionPoller: ID 1286: Progress Changed 0% (0 of 2)
    2015-08-07 19:41:30,900 DEBUG    pytan.handler.QuestionPoller: ID 1286: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:41:30,900 DEBUG    pytan.handler.QuestionPoller: ID 1286: Timing: Started: 2015-08-07 19:41:25.887268, Expiration: 2015-08-07 19:51:26, Override Timeout: None, Elapsed Time: 0:00:05.013603, Left till expiry: 0:09:55.099132, Loop Count: 2
    2015-08-07 19:41:35,905 DEBUG    pytan.handler.QuestionPoller: ID 1286: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:41:35,905 DEBUG    pytan.handler.QuestionPoller: ID 1286: Timing: Started: 2015-08-07 19:41:25.887268, Expiration: 2015-08-07 19:51:26, Override Timeout: None, Elapsed Time: 0:00:10.018106, Left till expiry: 0:09:50.094629, Loop Count: 3
    2015-08-07 19:41:40,908 DEBUG    pytan.handler.QuestionPoller: ID 1286: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:41:40,908 DEBUG    pytan.handler.QuestionPoller: ID 1286: Timing: Started: 2015-08-07 19:41:25.887268, Expiration: 2015-08-07 19:51:26, Override Timeout: None, Elapsed Time: 0:00:15.021693, Left till expiry: 0:09:45.091042, Loop Count: 4
    2015-08-07 19:41:45,915 DEBUG    pytan.handler.QuestionPoller: ID 1286: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:41:45,915 DEBUG    pytan.handler.QuestionPoller: ID 1286: Timing: Started: 2015-08-07 19:41:25.887268, Expiration: 2015-08-07 19:51:26, Override Timeout: None, Elapsed Time: 0:00:20.028355, Left till expiry: 0:09:40.084380, Loop Count: 5
    2015-08-07 19:41:50,919 DEBUG    pytan.handler.QuestionPoller: ID 1286: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:41:50,919 DEBUG    pytan.handler.QuestionPoller: ID 1286: Timing: Started: 2015-08-07 19:41:25.887268, Expiration: 2015-08-07 19:51:26, Override Timeout: None, Elapsed Time: 0:00:25.032268, Left till expiry: 0:09:35.080466, Loop Count: 6
    2015-08-07 19:41:55,923 DEBUG    pytan.handler.QuestionPoller: ID 1286: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:41:55,924 DEBUG    pytan.handler.QuestionPoller: ID 1286: Timing: Started: 2015-08-07 19:41:25.887268, Expiration: 2015-08-07 19:51:26, Override Timeout: None, Elapsed Time: 0:00:30.036709, Left till expiry: 0:09:30.076025, Loop Count: 7
    2015-08-07 19:41:55,924 INFO     pytan.handler.QuestionPoller: ID 1286: Progress Changed 50% (1 of 2)
    2015-08-07 19:42:00,928 DEBUG    pytan.handler.QuestionPoller: ID 1286: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:42:00,929 DEBUG    pytan.handler.QuestionPoller: ID 1286: Timing: Started: 2015-08-07 19:41:25.887268, Expiration: 2015-08-07 19:51:26, Override Timeout: None, Elapsed Time: 0:00:35.041723, Left till expiry: 0:09:25.071012, Loop Count: 8
    2015-08-07 19:42:05,933 DEBUG    pytan.handler.QuestionPoller: ID 1286: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-07 19:42:05,933 DEBUG    pytan.handler.QuestionPoller: ID 1286: Timing: Started: 2015-08-07 19:41:25.887268, Expiration: 2015-08-07 19:51:26, Override Timeout: None, Elapsed Time: 0:00:40.046204, Left till expiry: 0:09:20.066531, Loop Count: 9
    2015-08-07 19:42:05,933 INFO     pytan.handler.QuestionPoller: ID 1286: Progress Changed 100% (2 of 2)
    2015-08-07 19:42:05,933 INFO     pytan.handler.QuestionPoller: ID 1286: Reached Threshold of 99% (2 of 2)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'poller_object': <pytan.pollers.QuestionPoller object at 0x10a614e10>,
     'poller_success': True,
     'question_object': <taniumpy.object_types.question.Question object at 0x10a613450>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10a614490>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Computer Name[Dweedle] from all machines
    
    CSV Results of response: 
    Computer Name[Dweedle]
    [no results]
    JTANIUM1
    
