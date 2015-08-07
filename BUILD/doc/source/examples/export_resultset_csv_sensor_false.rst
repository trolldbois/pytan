
Export resultset csv sensor false
==========================================================================================

Export a ResultSet from asking a question as CSV with false for header_add_sensor

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
    export_kwargs["header_add_sensor"] = False
    
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


    Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
    2015-08-07 19:54:56,919 DEBUG    pytan.handler.QuestionPoller: ID 1320: id resolved to 1320
    2015-08-07 19:54:56,919 DEBUG    pytan.handler.QuestionPoller: ID 1320: expiration resolved to 2015-08-07T20:04:57
    2015-08-07 19:54:56,919 DEBUG    pytan.handler.QuestionPoller: ID 1320: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:54:56,919 DEBUG    pytan.handler.QuestionPoller: ID 1320: id resolved to 1320
    2015-08-07 19:54:56,919 DEBUG    pytan.handler.QuestionPoller: ID 1320: Object Info resolved to Question ID: 1320, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:54:56,923 DEBUG    pytan.handler.QuestionPoller: ID 1320: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:54:56,923 DEBUG    pytan.handler.QuestionPoller: ID 1320: Timing: Started: 2015-08-07 19:54:56.919779, Expiration: 2015-08-07 20:04:57, Override Timeout: None, Elapsed Time: 0:00:00.003505, Left till expiry: 0:10:00.076719, Loop Count: 1
    2015-08-07 19:54:56,923 INFO     pytan.handler.QuestionPoller: ID 1320: Progress Changed 0% (0 of 2)
    2015-08-07 19:55:01,930 DEBUG    pytan.handler.QuestionPoller: ID 1320: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:55:01,930 DEBUG    pytan.handler.QuestionPoller: ID 1320: Timing: Started: 2015-08-07 19:54:56.919779, Expiration: 2015-08-07 20:04:57, Override Timeout: None, Elapsed Time: 0:00:05.010436, Left till expiry: 0:09:55.069788, Loop Count: 2
    2015-08-07 19:55:06,936 DEBUG    pytan.handler.QuestionPoller: ID 1320: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:55:06,936 DEBUG    pytan.handler.QuestionPoller: ID 1320: Timing: Started: 2015-08-07 19:54:56.919779, Expiration: 2015-08-07 20:04:57, Override Timeout: None, Elapsed Time: 0:00:10.016602, Left till expiry: 0:09:50.063621, Loop Count: 3
    2015-08-07 19:55:11,944 DEBUG    pytan.handler.QuestionPoller: ID 1320: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:55:11,944 DEBUG    pytan.handler.QuestionPoller: ID 1320: Timing: Started: 2015-08-07 19:54:56.919779, Expiration: 2015-08-07 20:04:57, Override Timeout: None, Elapsed Time: 0:00:15.025073, Left till expiry: 0:09:45.055150, Loop Count: 4
    2015-08-07 19:55:16,949 DEBUG    pytan.handler.QuestionPoller: ID 1320: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:55:16,950 DEBUG    pytan.handler.QuestionPoller: ID 1320: Timing: Started: 2015-08-07 19:54:56.919779, Expiration: 2015-08-07 20:04:57, Override Timeout: None, Elapsed Time: 0:00:20.030206, Left till expiry: 0:09:40.050018, Loop Count: 5
    2015-08-07 19:55:21,957 DEBUG    pytan.handler.QuestionPoller: ID 1320: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:55:21,957 DEBUG    pytan.handler.QuestionPoller: ID 1320: Timing: Started: 2015-08-07 19:54:56.919779, Expiration: 2015-08-07 20:04:57, Override Timeout: None, Elapsed Time: 0:00:25.037997, Left till expiry: 0:09:35.042226, Loop Count: 6
    2015-08-07 19:55:21,957 INFO     pytan.handler.QuestionPoller: ID 1320: Progress Changed 50% (1 of 2)
    2015-08-07 19:55:26,962 DEBUG    pytan.handler.QuestionPoller: ID 1320: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-07 19:55:26,962 DEBUG    pytan.handler.QuestionPoller: ID 1320: Timing: Started: 2015-08-07 19:54:56.919779, Expiration: 2015-08-07 20:04:57, Override Timeout: None, Elapsed Time: 0:00:30.042678, Left till expiry: 0:09:30.037545, Loop Count: 7
    2015-08-07 19:55:26,962 INFO     pytan.handler.QuestionPoller: ID 1320: Progress Changed 100% (2 of 2)
    2015-08-07 19:55:26,962 INFO     pytan.handler.QuestionPoller: ID 1320: Reached Threshold of 99% (2 of 2)
    
    print the export_str returned from export_obj():
    Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
    2015-08-07 19:54:36,751 DEBUG    pytan.handler.QuestionPoller: ID 1319: id resolved to 1319
    2015-08-07 19:54:36,751 DEBUG    pytan.handler.QuestionPoller: ID 1319: expiration resolved to 2015-08-07T20:04:36
    2015-08-07 19:54:36,751 DEBUG    pytan.handler.QuestionPoller: ID 1319: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:54:36,751 DEBUG    pytan.handler.QuestionPoller: ID 1319: id resolved to 1319
    2015-08-07 19:54:36,751 DEBUG    pytan.handler.QuestionPoller: ID 1319: Object Info resolved to Question ID: 1319, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:54:36,754 DEBUG    pytan.handler.QuestionPoller: ID 1319: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:54:36,754 DEBUG    pytan.handler.QuestionPoller: ID 1319: Timing: Started: 2015-08-07 19:54:36.751300, Expiration: 2015-08-07 20:04:36, Override Timeout: None, Elapsed Time: 0:00:00.003617, Left till expiry: 0:09:59.245086, Loop Count: 1
    2015-08-07 19:54:36,754 INFO     pytan.handler.QuestionPoller: ID 1319: Progress Changed 0% (0 of 2)
    2015-08-07 19:54:41,761 DEBUG    pytan.handler.QuestionPoller: ID 1319: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:54:41,761 DEBUG    pytan.handler.QuestionPoller: ID 1319: Timing: Started: 2015-08-07 19:54:36.751300, Expiration: 2015-08-07 20:04:36, Override Timeout: None, Elapsed Time: 0:00:05.010033, Left till expiry: 0:09:54.238670, Loop Count: 2
    2015-08-07 19:54:46,767 DEBUG    pytan.handler.QuestionPoller: ID 1319: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:54:46,767 DEBUG    pytan.handler.QuestionPoller: ID 1319: Timing: Started: 2015-08-07 19:54:36.751300, Expiration: 2015-08-07 20:04:36, Override Timeout: None, Elapsed Time: 0:00:10.016411, Left till expiry: 0:09:49.232293, Loop Count: 3
    2015-08-07 19:54:51,771 DEBUG    pytan.handler.QuestionPoller: ID 1319: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:54:51,771 DEBUG    pytan.handler.QuestionPoller: ID 1319: Timing: Started: 2015-08-07 19:54:36.751300, Expiration: 2015-08-07 20:04:36, Override Timeout: None, Elapsed Time: 0:00:15.020504, Left till expiry: 0:09:44.228198, Loop Count: 4
    ..trimmed for brevity..
