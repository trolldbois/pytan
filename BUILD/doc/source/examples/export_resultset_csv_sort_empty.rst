
Export resultset csv sort empty
==========================================================================================

Export a ResultSet from asking a question as CSV with an empty list for header_sort

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
    
    # setup the export_obj kwargs for later
    export_kwargs = {}
    export_kwargs["export_format"] = u'csv'
    export_kwargs["header_sort"] = []
    
    # ask the question that will provide the resultset that we want to use
    ask_kwargs = {
        'qtype': 'manual',
        'sensors': [
            "Computer Name", "IP Route Details", "IP Address",
            'Folder Name Search with RegEx Match{dirname=Program Files,regex=.*Shared.*}',
        ],
    }
    response = handler.ask(**ask_kwargs)
    
    # export the object to a string
    # (we could just as easily export to a file using export_to_report_file)
    export_kwargs['obj'] = response['question_results']
    export_str = handler.export_obj(**export_kwargs)
    
    
    print ""
    print "print the export_str returned from export_obj():"
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
    2015-08-06 15:03:34,315 DEBUG    pytan.handler.QuestionPoller: ID 86282: id resolved to 86282
    2015-08-06 15:03:34,315 DEBUG    pytan.handler.QuestionPoller: ID 86282: expiration resolved to 2015-08-06T15:13:34
    2015-08-06 15:03:34,315 DEBUG    pytan.handler.QuestionPoller: ID 86282: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 15:03:34,315 DEBUG    pytan.handler.QuestionPoller: ID 86282: id resolved to 86282
    2015-08-06 15:03:34,315 DEBUG    pytan.handler.QuestionPoller: ID 86282: Object Info resolved to Question ID: 86282, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 15:03:34,320 DEBUG    pytan.handler.QuestionPoller: ID 86282: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:03:34,320 DEBUG    pytan.handler.QuestionPoller: ID 86282: Timing: Started: 2015-08-06 15:03:34.315567, Expiration: 2015-08-06 15:13:34, Override Timeout: None, Elapsed Time: 0:00:00.004867, Left till expiry: 0:09:59.679569, Loop Count: 1
    2015-08-06 15:03:34,320 INFO     pytan.handler.QuestionPoller: ID 86282: Progress Changed 0% (0 of 2)
    2015-08-06 15:03:39,325 DEBUG    pytan.handler.QuestionPoller: ID 86282: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:03:39,325 DEBUG    pytan.handler.QuestionPoller: ID 86282: Timing: Started: 2015-08-06 15:03:34.315567, Expiration: 2015-08-06 15:13:34, Override Timeout: None, Elapsed Time: 0:00:05.010254, Left till expiry: 0:09:54.674182, Loop Count: 2
    2015-08-06 15:03:44,335 DEBUG    pytan.handler.QuestionPoller: ID 86282: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-06 15:03:44,335 DEBUG    pytan.handler.QuestionPoller: ID 86282: Timing: Started: 2015-08-06 15:03:34.315567, Expiration: 2015-08-06 15:13:34, Override Timeout: None, Elapsed Time: 0:00:10.019513, Left till expiry: 0:09:49.664923, Loop Count: 3
    2015-08-06 15:03:44,335 INFO     pytan.handler.QuestionPoller: ID 86282: Progress Changed 50% (1 of 2)
    2015-08-06 15:03:49,342 DEBUG    pytan.handler.QuestionPoller: ID 86282: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-06 15:03:49,342 DEBUG    pytan.handler.QuestionPoller: ID 86282: Timing: Started: 2015-08-06 15:03:34.315567, Expiration: 2015-08-06 15:13:34, Override Timeout: None, Elapsed Time: 0:00:15.026512, Left till expiry: 0:09:44.657923, Loop Count: 4
    2015-08-06 15:03:54,348 DEBUG    pytan.handler.QuestionPoller: ID 86282: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-06 15:03:54,348 DEBUG    pytan.handler.QuestionPoller: ID 86282: Timing: Started: 2015-08-06 15:03:34.315567, Expiration: 2015-08-06 15:13:34, Override Timeout: None, Elapsed Time: 0:00:20.032729, Left till expiry: 0:09:39.651707, Loop Count: 5
    2015-08-06 15:03:59,355 DEBUG    pytan.handler.QuestionPoller: ID 86282: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-06 15:03:59,355 DEBUG    pytan.handler.QuestionPoller: ID 86282: Timing: Started: 2015-08-06 15:03:34.315567, Expiration: 2015-08-06 15:13:34, Override Timeout: None, Elapsed Time: 0:00:25.040088, Left till expiry: 0:09:34.644347, Loop Count: 6
    2015-08-06 15:03:59,355 INFO     pytan.handler.QuestionPoller: ID 86282: Progress Changed 100% (2 of 2)
    2015-08-06 15:03:59,355 INFO     pytan.handler.QuestionPoller: ID 86282: Reached Threshold of 99% (2 of 2)
    
    print the export_str returned from export_obj():
    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
    2015-08-06 15:03:14,128 DEBUG    pytan.handler.QuestionPoller: ID 86281: id resolved to 86281
    2015-08-06 15:03:14,128 DEBUG    pytan.handler.QuestionPoller: ID 86281: expiration resolved to 2015-08-06T15:13:14
    2015-08-06 15:03:14,128 DEBUG    pytan.handler.QuestionPoller: ID 86281: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 15:03:14,128 DEBUG    pytan.handler.QuestionPoller: ID 86281: id resolved to 86281
    2015-08-06 15:03:14,128 DEBUG    pytan.handler.QuestionPoller: ID 86281: Object Info resolved to Question ID: 86281, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 15:03:14,133 DEBUG    pytan.handler.QuestionPoller: ID 86281: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:03:14,133 DEBUG    pytan.handler.QuestionPoller: ID 86281: Timing: Started: 2015-08-06 15:03:14.128736, Expiration: 2015-08-06 15:13:14, Override Timeout: None, Elapsed Time: 0:00:00.004741, Left till expiry: 0:09:59.866525, Loop Count: 1
    2015-08-06 15:03:14,133 INFO     pytan.handler.QuestionPoller: ID 86281: Progress Changed 0% (0 of 2)
    2015-08-06 15:03:19,140 DEBUG    pytan.handler.QuestionPoller: ID 86281: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:03:19,140 DEBUG    pytan.handler.QuestionPoller: ID 86281: Timing: Started: 2015-08-06 15:03:14.128736, Expiration: 2015-08-06 15:13:14, Override Timeout: None, Elapsed Time: 0:00:05.011756, Left till expiry: 0:09:54.859510, Loop Count: 2
    2015-08-06 15:03:24,148 DEBUG    pytan.handler.QuestionPoller: ID 86281: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:03:24,148 DEBUG    pytan.handler.QuestionPoller: ID 86281: Timing: Started: 2015-08-06 15:03:14.128736, Expiration: 2015-08-06 15:13:14, Override Timeout: None, Elapsed Time: 0:00:10.019819, Left till expiry: 0:09:49.851447, Loop Count: 3
    2015-08-06 15:03:29,155 DEBUG    pytan.handler.QuestionPoller: ID 86281: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:03:29,155 DEBUG    pytan.handler.QuestionPoller: ID 86281: Timing: Started: 2015-08-06 15:03:14.128736, Expiration: 2015-08-06 15:13:14, Override Timeout: None, Elapsed Time: 0:00:15.027080, Left till expiry: 0:09:44.844186, Loop Count: 4
    ..trimmed for brevity..
