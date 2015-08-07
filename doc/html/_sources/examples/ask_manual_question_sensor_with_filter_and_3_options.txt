
Ask manual question sensor with filter and 3 options
==========================================================================================

Ask a manual question using human strings by referencing the name of a single sensor.

Also supply a sensor filter that limits the column data that is shown to values that contain Windows (which is short hand for regex match against .*Windows.*).

Also supply filter options that re-fetches any cached data that is older than 3600 seconds, matches all values supplied in the filter, and ignores case for any value match of the filter.

No sensor paramaters, question filters, or question options supplied.

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
    kwargs["sensors"] = u'Operating System, that contains:Windows, opt:match_all_values, opt:ignore_case, opt:max_data_age:3600'
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
    2015-08-07 19:43:51,504 DEBUG    pytan.handler.QuestionPoller: ID 1295: id resolved to 1295
    2015-08-07 19:43:51,504 DEBUG    pytan.handler.QuestionPoller: ID 1295: expiration resolved to 2015-08-07T19:53:51
    2015-08-07 19:43:51,504 DEBUG    pytan.handler.QuestionPoller: ID 1295: query_text resolved to Get Operating System containing "Windows" from all machines
    2015-08-07 19:43:51,504 DEBUG    pytan.handler.QuestionPoller: ID 1295: id resolved to 1295
    2015-08-07 19:43:51,504 DEBUG    pytan.handler.QuestionPoller: ID 1295: Object Info resolved to Question ID: 1295, Query: Get Operating System containing "Windows" from all machines
    2015-08-07 19:43:51,508 DEBUG    pytan.handler.QuestionPoller: ID 1295: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:43:51,508 DEBUG    pytan.handler.QuestionPoller: ID 1295: Timing: Started: 2015-08-07 19:43:51.504895, Expiration: 2015-08-07 19:53:51, Override Timeout: None, Elapsed Time: 0:00:00.003409, Left till expiry: 0:09:59.491698, Loop Count: 1
    2015-08-07 19:43:51,508 INFO     pytan.handler.QuestionPoller: ID 1295: Progress Changed 0% (0 of 2)
    2015-08-07 19:43:56,512 DEBUG    pytan.handler.QuestionPoller: ID 1295: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:43:56,512 DEBUG    pytan.handler.QuestionPoller: ID 1295: Timing: Started: 2015-08-07 19:43:51.504895, Expiration: 2015-08-07 19:53:51, Override Timeout: None, Elapsed Time: 0:00:05.007355, Left till expiry: 0:09:54.487753, Loop Count: 2
    2015-08-07 19:44:01,520 DEBUG    pytan.handler.QuestionPoller: ID 1295: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-07 19:44:01,520 DEBUG    pytan.handler.QuestionPoller: ID 1295: Timing: Started: 2015-08-07 19:43:51.504895, Expiration: 2015-08-07 19:53:51, Override Timeout: None, Elapsed Time: 0:00:10.015495, Left till expiry: 0:09:49.479614, Loop Count: 3
    2015-08-07 19:44:01,520 INFO     pytan.handler.QuestionPoller: ID 1295: Progress Changed 100% (2 of 2)
    2015-08-07 19:44:01,520 INFO     pytan.handler.QuestionPoller: ID 1295: Reached Threshold of 99% (2 of 2)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'poller_object': <pytan.pollers.QuestionPoller object at 0x10a5b98d0>,
     'poller_success': True,
     'question_object': <taniumpy.object_types.question.Question object at 0x10a5b9810>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10a615710>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Operating System containing "Windows" from all machines
    
    CSV Results of response: 
    Operating System
    [no results]
    Windows Server 2008 R2 Standard
    
