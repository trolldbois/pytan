
Export resultset csv sort false
==========================================================================================

Export a ResultSet from asking a question as CSV with false for header_sort

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
    export_kwargs["header_sort"] = False
    
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
    2015-08-06 15:06:20,526 DEBUG    pytan.handler.QuestionPoller: ID 86284: id resolved to 86284
    2015-08-06 15:06:20,526 DEBUG    pytan.handler.QuestionPoller: ID 86284: expiration resolved to 2015-08-06T15:16:20
    2015-08-06 15:06:20,526 DEBUG    pytan.handler.QuestionPoller: ID 86284: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 15:06:20,526 DEBUG    pytan.handler.QuestionPoller: ID 86284: id resolved to 86284
    2015-08-06 15:06:20,526 DEBUG    pytan.handler.QuestionPoller: ID 86284: Object Info resolved to Question ID: 86284, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 15:06:20,533 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:06:20,533 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:00:00.006509, Left till expiry: 0:09:59.466672, Loop Count: 1
    2015-08-06 15:06:20,533 INFO     pytan.handler.QuestionPoller: ID 86284: Progress Changed 0% (0 of 2)
    2015-08-06 15:06:25,540 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:06:25,540 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:00:05.013477, Left till expiry: 0:09:54.459704, Loop Count: 2
    2015-08-06 15:06:30,549 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:06:30,549 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:00:10.022854, Left till expiry: 0:09:49.450328, Loop Count: 3
    2015-08-06 15:06:35,559 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:06:35,559 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:00:15.032749, Left till expiry: 0:09:44.440432, Loop Count: 4
    2015-08-06 15:06:40,570 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:06:40,570 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:00:20.043809, Left till expiry: 0:09:39.429372, Loop Count: 5
    2015-08-06 15:06:45,577 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:06:45,577 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:00:25.050916, Left till expiry: 0:09:34.422266, Loop Count: 6
    2015-08-06 15:06:50,585 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:06:50,585 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:00:30.058525, Left till expiry: 0:09:29.414657, Loop Count: 7
    2015-08-06 15:06:55,590 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:06:55,590 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:00:35.063747, Left till expiry: 0:09:24.409435, Loop Count: 8
    2015-08-06 15:07:00,599 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:07:00,599 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:00:40.072301, Left till expiry: 0:09:19.400881, Loop Count: 9
    2015-08-06 15:07:05,607 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:07:05,607 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:00:45.080639, Left till expiry: 0:09:14.392543, Loop Count: 10
    2015-08-06 15:07:10,617 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:07:10,617 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:00:50.090444, Left till expiry: 0:09:09.382737, Loop Count: 11
    2015-08-06 15:07:15,622 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:07:15,622 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:00:55.095314, Left till expiry: 0:09:04.377868, Loop Count: 12
    2015-08-06 15:07:20,627 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:07:20,627 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:01:00.100727, Left till expiry: 0:08:59.372455, Loop Count: 13
    2015-08-06 15:07:25,634 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:07:25,634 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:01:05.107652, Left till expiry: 0:08:54.365529, Loop Count: 14
    2015-08-06 15:07:30,644 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:07:30,644 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:01:10.117962, Left till expiry: 0:08:49.355220, Loop Count: 15
    2015-08-06 15:07:35,651 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:07:35,651 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:01:15.125050, Left till expiry: 0:08:44.348132, Loop Count: 16
    2015-08-06 15:07:40,658 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:07:40,658 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:01:20.132101, Left till expiry: 0:08:39.341080, Loop Count: 17
    2015-08-06 15:07:45,663 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:07:45,663 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:01:25.137033, Left till expiry: 0:08:34.336149, Loop Count: 18
    2015-08-06 15:07:50,670 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:07:50,670 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:01:30.143365, Left till expiry: 0:08:29.329816, Loop Count: 19
    2015-08-06 15:07:55,680 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:07:55,680 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:01:35.154036, Left till expiry: 0:08:24.319146, Loop Count: 20
    2015-08-06 15:08:00,687 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:08:00,687 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:01:40.160913, Left till expiry: 0:08:19.312269, Loop Count: 21
    2015-08-06 15:08:05,703 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:08:05,703 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:01:45.176595, Left till expiry: 0:08:14.296586, Loop Count: 22
    2015-08-06 15:08:10,714 DEBUG    pytan.handler.QuestionPoller: ID 86284: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-06 15:08:10,714 DEBUG    pytan.handler.QuestionPoller: ID 86284: Timing: Started: 2015-08-06 15:06:20.526821, Expiration: 2015-08-06 15:16:20, Override Timeout: None, Elapsed Time: 0:01:50.187801, Left till expiry: 0:08:09.285380, Loop Count: 23
    2015-08-06 15:08:10,714 INFO     pytan.handler.QuestionPoller: ID 86284: Progress Changed 100% (2 of 2)
    2015-08-06 15:08:10,714 INFO     pytan.handler.QuestionPoller: ID 86284: Reached Threshold of 99% (2 of 2)
    
    print the export_str returned from export_obj():
    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
    2015-08-06 15:03:59,519 DEBUG    pytan.handler.QuestionPoller: ID 86283: id resolved to 86283
    2015-08-06 15:03:59,519 DEBUG    pytan.handler.QuestionPoller: ID 86283: expiration resolved to 2015-08-06T15:13:59
    2015-08-06 15:03:59,519 DEBUG    pytan.handler.QuestionPoller: ID 86283: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 15:03:59,519 DEBUG    pytan.handler.QuestionPoller: ID 86283: id resolved to 86283
    2015-08-06 15:03:59,519 DEBUG    pytan.handler.QuestionPoller: ID 86283: Object Info resolved to Question ID: 86283, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 15:03:59,524 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:03:59,524 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:00:00.004793, Left till expiry: 0:09:59.475810, Loop Count: 1
    2015-08-06 15:03:59,524 INFO     pytan.handler.QuestionPoller: ID 86283: Progress Changed 0% (0 of 2)
    2015-08-06 15:04:04,529 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:04:04,529 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:00:05.010366, Left till expiry: 0:09:54.470237, Loop Count: 2
    2015-08-06 15:04:09,538 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:04:09,538 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:00:10.018850, Left till expiry: 0:09:49.461753, Loop Count: 3
    2015-08-06 15:04:14,549 DEBUG    pytan.handler.QuestionPoller: ID 86283: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:04:14,549 DEBUG    pytan.handler.QuestionPoller: ID 86283: Timing: Started: 2015-08-06 15:03:59.519400, Expiration: 2015-08-06 15:13:59, Override Timeout: None, Elapsed Time: 0:00:15.030350, Left till expiry: 0:09:44.450253, Loop Count: 4
    ..trimmed for brevity..
