
Ask manual question simple single sensor
==========================================================================================

Ask a manual question using human strings by referencing the name of a single sensor in a string.

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
    kwargs["sensors"] = u'Computer Name'
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
    2015-08-07 19:38:10,340 DEBUG    pytan.handler.QuestionPoller: ID 1281: id resolved to 1281
    2015-08-07 19:38:10,340 DEBUG    pytan.handler.QuestionPoller: ID 1281: expiration resolved to 2015-08-07T19:48:10
    2015-08-07 19:38:10,340 DEBUG    pytan.handler.QuestionPoller: ID 1281: query_text resolved to Get Computer Name from all machines
    2015-08-07 19:38:10,340 DEBUG    pytan.handler.QuestionPoller: ID 1281: id resolved to 1281
    2015-08-07 19:38:10,340 DEBUG    pytan.handler.QuestionPoller: ID 1281: Object Info resolved to Question ID: 1281, Query: Get Computer Name from all machines
    2015-08-07 19:38:10,343 DEBUG    pytan.handler.QuestionPoller: ID 1281: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:38:10,343 DEBUG    pytan.handler.QuestionPoller: ID 1281: Timing: Started: 2015-08-07 19:38:10.340345, Expiration: 2015-08-07 19:48:10, Override Timeout: None, Elapsed Time: 0:00:00.003377, Left till expiry: 0:09:59.656281, Loop Count: 1
    2015-08-07 19:38:10,343 INFO     pytan.handler.QuestionPoller: ID 1281: Progress Changed 0% (0 of 2)
    2015-08-07 19:38:15,351 DEBUG    pytan.handler.QuestionPoller: ID 1281: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:38:15,351 DEBUG    pytan.handler.QuestionPoller: ID 1281: Timing: Started: 2015-08-07 19:38:10.340345, Expiration: 2015-08-07 19:48:10, Override Timeout: None, Elapsed Time: 0:00:05.011211, Left till expiry: 0:09:54.648447, Loop Count: 2
    2015-08-07 19:38:15,351 INFO     pytan.handler.QuestionPoller: ID 1281: Progress Changed 50% (1 of 2)
    2015-08-07 19:38:20,357 DEBUG    pytan.handler.QuestionPoller: ID 1281: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-07 19:38:20,357 DEBUG    pytan.handler.QuestionPoller: ID 1281: Timing: Started: 2015-08-07 19:38:10.340345, Expiration: 2015-08-07 19:48:10, Override Timeout: None, Elapsed Time: 0:00:10.017192, Left till expiry: 0:09:49.642466, Loop Count: 3
    2015-08-07 19:38:20,357 INFO     pytan.handler.QuestionPoller: ID 1281: Progress Changed 100% (2 of 2)
    2015-08-07 19:38:20,357 INFO     pytan.handler.QuestionPoller: ID 1281: Reached Threshold of 99% (2 of 2)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'poller_object': <pytan.pollers.QuestionPoller object at 0x10a7ecb90>,
     'poller_success': True,
     'question_object': <taniumpy.object_types.question.Question object at 0x10a808290>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10a6133d0>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Computer Name from all machines
    
    CSV Results of response: 
    Computer Name
    Casus-Belli.local
    JTANIUM1.localdomain
    
