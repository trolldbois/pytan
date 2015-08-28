
Invalid deploy action run false
==========================================================================================

Deploy an action without run=True, which will only run the pre-deploy action question that matches action_filters, export the results to a file, and raise a RunFalse exception

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
    kwargs['report_dir'] = tempfile.gettempdir()
    kwargs["package"] = u'Distribute Tanium Standard Utilities'
    
    
    # call the handler with the deploy_action method, passing in kwargs for arguments
    # this should throw an exception: pytan.exceptions.RunFalse
    import traceback
    try:
        handler.deploy_action(**kwargs)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
    
    


Output from Python Code
----------------------------------------------------------------------------------------

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
    2015-08-07 19:46:08,957 DEBUG    pytan.handler.QuestionPoller: ID 1304: id resolved to 1304
    2015-08-07 19:46:08,957 DEBUG    pytan.handler.QuestionPoller: ID 1304: expiration resolved to 2015-08-07T19:56:09
    2015-08-07 19:46:08,957 DEBUG    pytan.handler.QuestionPoller: ID 1304: query_text resolved to Get Computer Name and Online = "True" from all machines
    2015-08-07 19:46:08,957 DEBUG    pytan.handler.QuestionPoller: ID 1304: id resolved to 1304
    2015-08-07 19:46:08,957 DEBUG    pytan.handler.QuestionPoller: ID 1304: Object Info resolved to Question ID: 1304, Query: Get Computer Name and Online = "True" from all machines
    2015-08-07 19:46:08,962 DEBUG    pytan.handler.QuestionPoller: ID 1304: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:46:08,962 DEBUG    pytan.handler.QuestionPoller: ID 1304: Timing: Started: 2015-08-07 19:46:08.957905, Expiration: 2015-08-07 19:56:09, Override Timeout: None, Elapsed Time: 0:00:00.004813, Left till expiry: 0:10:00.037284, Loop Count: 1
    2015-08-07 19:46:08,962 INFO     pytan.handler.QuestionPoller: ID 1304: Progress Changed 0% (0 of 2)
    2015-08-07 19:46:13,969 DEBUG    pytan.handler.QuestionPoller: ID 1304: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-07 19:46:13,969 DEBUG    pytan.handler.QuestionPoller: ID 1304: Timing: Started: 2015-08-07 19:46:08.957905, Expiration: 2015-08-07 19:56:09, Override Timeout: None, Elapsed Time: 0:00:05.011888, Left till expiry: 0:09:55.030210, Loop Count: 2
    2015-08-07 19:46:13,969 INFO     pytan.handler.QuestionPoller: ID 1304: Progress Changed 100% (2 of 2)
    2015-08-07 19:46:13,969 INFO     pytan.handler.QuestionPoller: ID 1304: Reached Threshold of 99% (2 of 2)
    2015-08-07 19:46:13,974 INFO     pytan.handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/VERIFY_BEFORE_DEPLOY_ACTION_ResultSet_2015_08_07-15_46_13-EDT.csv' written with 73 bytes
    Traceback (most recent call last):
      File "<string>", line 55, in <module>
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 404, in deploy_action
        **kwargs
      File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2699, in wrap
        ret = f(*args, **kwargs)
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1662, in _deploy_action
        raise pytan.exceptions.RunFalse(m(report_path, len(result)))
    RunFalse: 'Run' is not True!!
    View and verify the contents of /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/VERIFY_BEFORE_DEPLOY_ACTION_ResultSet_2015_08_07-15_46_13-EDT.csv (length: 73 bytes)
    Re-run this deploy action with run=True after verifying
