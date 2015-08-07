
Invalid export resultset csv bad sort type
==========================================================================================

Export a ResultSet from asking a question using a bad header_sort

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
    
    # setup the export_obj kwargs for later
    export_kwargs = {}
    export_kwargs["export_format"] = u'csv'
    export_kwargs["header_sort"] = u'bad'
    
    # ask the question that will provide the resultset that we want to use
    ask_kwargs = {
        'qtype': 'manual',
        'sensors': [
            "Computer Name"
        ],
    }
    response = handler.ask(**ask_kwargs)
    export_kwargs['obj'] = response['question_results']
    
    # export the object to a string
    # this should throw an exception: pytan.exceptions.HandlerError
    import traceback
    
    try:
        handler.export_obj(**export_kwargs)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
    
    


Output from Python Code
----------------------------------------------------------------------------------------

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
    2015-08-07 19:56:37,342 DEBUG    pytan.handler.QuestionPoller: ID 1324: id resolved to 1324
    2015-08-07 19:56:37,342 DEBUG    pytan.handler.QuestionPoller: ID 1324: expiration resolved to 2015-08-07T20:06:37
    2015-08-07 19:56:37,342 DEBUG    pytan.handler.QuestionPoller: ID 1324: query_text resolved to Get Computer Name from all machines
    2015-08-07 19:56:37,342 DEBUG    pytan.handler.QuestionPoller: ID 1324: id resolved to 1324
    2015-08-07 19:56:37,342 DEBUG    pytan.handler.QuestionPoller: ID 1324: Object Info resolved to Question ID: 1324, Query: Get Computer Name from all machines
    2015-08-07 19:56:37,345 DEBUG    pytan.handler.QuestionPoller: ID 1324: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:56:37,345 DEBUG    pytan.handler.QuestionPoller: ID 1324: Timing: Started: 2015-08-07 19:56:37.342253, Expiration: 2015-08-07 20:06:37, Override Timeout: None, Elapsed Time: 0:00:00.003199, Left till expiry: 0:09:59.654550, Loop Count: 1
    2015-08-07 19:56:37,345 INFO     pytan.handler.QuestionPoller: ID 1324: Progress Changed 0% (0 of 2)
    2015-08-07 19:56:42,353 DEBUG    pytan.handler.QuestionPoller: ID 1324: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:56:42,353 DEBUG    pytan.handler.QuestionPoller: ID 1324: Timing: Started: 2015-08-07 19:56:37.342253, Expiration: 2015-08-07 20:06:37, Override Timeout: None, Elapsed Time: 0:00:05.011079, Left till expiry: 0:09:54.646670, Loop Count: 2
    2015-08-07 19:56:47,361 DEBUG    pytan.handler.QuestionPoller: ID 1324: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:56:47,361 DEBUG    pytan.handler.QuestionPoller: ID 1324: Timing: Started: 2015-08-07 19:56:37.342253, Expiration: 2015-08-07 20:06:37, Override Timeout: None, Elapsed Time: 0:00:10.019651, Left till expiry: 0:09:49.638099, Loop Count: 3
    2015-08-07 19:56:47,361 INFO     pytan.handler.QuestionPoller: ID 1324: Progress Changed 50% (1 of 2)
    2015-08-07 19:56:52,368 DEBUG    pytan.handler.QuestionPoller: ID 1324: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-07 19:56:52,368 DEBUG    pytan.handler.QuestionPoller: ID 1324: Timing: Started: 2015-08-07 19:56:37.342253, Expiration: 2015-08-07 20:06:37, Override Timeout: None, Elapsed Time: 0:00:15.025819, Left till expiry: 0:09:44.631931, Loop Count: 4
    2015-08-07 19:56:52,368 INFO     pytan.handler.QuestionPoller: ID 1324: Progress Changed 100% (2 of 2)
    2015-08-07 19:56:52,368 INFO     pytan.handler.QuestionPoller: ID 1324: Reached Threshold of 99% (2 of 2)
    Traceback (most recent call last):
      File "<string>", line 65, in <module>
      File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2699, in wrap
        ret = f(*args, **kwargs)
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1084, in export_obj
        pytan.utils.check_dictkey(**check_args)
      File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2685, in check_dictkey
        raise pytan.exceptions.HandlerError(err(key, valid_types, k_type))
    HandlerError: 'header_sort' must be one of [<type 'bool'>, <type 'list'>, <type 'tuple'>], you supplied <type 'unicode'>!
