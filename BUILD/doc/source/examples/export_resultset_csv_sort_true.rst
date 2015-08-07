
Export resultset csv sort true
==========================================================================================

Export a ResultSet from asking a question as CSV with true for header_sort

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
    export_kwargs["header_sort"] = True
    
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
    2015-08-07 19:51:11,061 DEBUG    pytan.handler.QuestionPoller: ID 1313: id resolved to 1313
    2015-08-07 19:51:11,061 DEBUG    pytan.handler.QuestionPoller: ID 1313: expiration resolved to 2015-08-07T20:01:11
    2015-08-07 19:51:11,061 DEBUG    pytan.handler.QuestionPoller: ID 1313: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:51:11,061 DEBUG    pytan.handler.QuestionPoller: ID 1313: id resolved to 1313
    2015-08-07 19:51:11,061 DEBUG    pytan.handler.QuestionPoller: ID 1313: Object Info resolved to Question ID: 1313, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:51:11,066 DEBUG    pytan.handler.QuestionPoller: ID 1313: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:51:11,066 DEBUG    pytan.handler.QuestionPoller: ID 1313: Timing: Started: 2015-08-07 19:51:11.061733, Expiration: 2015-08-07 20:01:11, Override Timeout: None, Elapsed Time: 0:00:00.004730, Left till expiry: 0:09:59.933541, Loop Count: 1
    2015-08-07 19:51:11,066 INFO     pytan.handler.QuestionPoller: ID 1313: Progress Changed 0% (0 of 2)
    2015-08-07 19:51:16,074 DEBUG    pytan.handler.QuestionPoller: ID 1313: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:51:16,074 DEBUG    pytan.handler.QuestionPoller: ID 1313: Timing: Started: 2015-08-07 19:51:11.061733, Expiration: 2015-08-07 20:01:11, Override Timeout: None, Elapsed Time: 0:00:05.013140, Left till expiry: 0:09:54.925130, Loop Count: 2
    2015-08-07 19:51:21,079 DEBUG    pytan.handler.QuestionPoller: ID 1313: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:51:21,079 DEBUG    pytan.handler.QuestionPoller: ID 1313: Timing: Started: 2015-08-07 19:51:11.061733, Expiration: 2015-08-07 20:01:11, Override Timeout: None, Elapsed Time: 0:00:10.017897, Left till expiry: 0:09:49.920373, Loop Count: 3
    2015-08-07 19:51:26,083 DEBUG    pytan.handler.QuestionPoller: ID 1313: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:51:26,083 DEBUG    pytan.handler.QuestionPoller: ID 1313: Timing: Started: 2015-08-07 19:51:11.061733, Expiration: 2015-08-07 20:01:11, Override Timeout: None, Elapsed Time: 0:00:15.021583, Left till expiry: 0:09:44.916686, Loop Count: 4
    2015-08-07 19:51:31,089 DEBUG    pytan.handler.QuestionPoller: ID 1313: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:51:31,089 DEBUG    pytan.handler.QuestionPoller: ID 1313: Timing: Started: 2015-08-07 19:51:11.061733, Expiration: 2015-08-07 20:01:11, Override Timeout: None, Elapsed Time: 0:00:20.027889, Left till expiry: 0:09:39.910381, Loop Count: 5
    2015-08-07 19:51:36,093 DEBUG    pytan.handler.QuestionPoller: ID 1313: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:51:36,093 DEBUG    pytan.handler.QuestionPoller: ID 1313: Timing: Started: 2015-08-07 19:51:11.061733, Expiration: 2015-08-07 20:01:11, Override Timeout: None, Elapsed Time: 0:00:25.032224, Left till expiry: 0:09:34.906045, Loop Count: 6
    2015-08-07 19:51:41,099 DEBUG    pytan.handler.QuestionPoller: ID 1313: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:51:41,099 DEBUG    pytan.handler.QuestionPoller: ID 1313: Timing: Started: 2015-08-07 19:51:11.061733, Expiration: 2015-08-07 20:01:11, Override Timeout: None, Elapsed Time: 0:00:30.037412, Left till expiry: 0:09:29.900858, Loop Count: 7
    2015-08-07 19:51:46,107 DEBUG    pytan.handler.QuestionPoller: ID 1313: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:51:46,107 DEBUG    pytan.handler.QuestionPoller: ID 1313: Timing: Started: 2015-08-07 19:51:11.061733, Expiration: 2015-08-07 20:01:11, Override Timeout: None, Elapsed Time: 0:00:35.045895, Left till expiry: 0:09:24.892375, Loop Count: 8
    2015-08-07 19:51:51,112 DEBUG    pytan.handler.QuestionPoller: ID 1313: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:51:51,112 DEBUG    pytan.handler.QuestionPoller: ID 1313: Timing: Started: 2015-08-07 19:51:11.061733, Expiration: 2015-08-07 20:01:11, Override Timeout: None, Elapsed Time: 0:00:40.051191, Left till expiry: 0:09:19.887079, Loop Count: 9
    2015-08-07 19:51:56,117 DEBUG    pytan.handler.QuestionPoller: ID 1313: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:51:56,117 DEBUG    pytan.handler.QuestionPoller: ID 1313: Timing: Started: 2015-08-07 19:51:11.061733, Expiration: 2015-08-07 20:01:11, Override Timeout: None, Elapsed Time: 0:00:45.055599, Left till expiry: 0:09:14.882671, Loop Count: 10
    2015-08-07 19:52:01,121 DEBUG    pytan.handler.QuestionPoller: ID 1313: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:52:01,122 DEBUG    pytan.handler.QuestionPoller: ID 1313: Timing: Started: 2015-08-07 19:51:11.061733, Expiration: 2015-08-07 20:01:11, Override Timeout: None, Elapsed Time: 0:00:50.060261, Left till expiry: 0:09:09.878009, Loop Count: 11
    2015-08-07 19:52:06,125 DEBUG    pytan.handler.QuestionPoller: ID 1313: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:52:06,126 DEBUG    pytan.handler.QuestionPoller: ID 1313: Timing: Started: 2015-08-07 19:51:11.061733, Expiration: 2015-08-07 20:01:11, Override Timeout: None, Elapsed Time: 0:00:55.064280, Left till expiry: 0:09:04.873989, Loop Count: 12
    2015-08-07 19:52:11,132 DEBUG    pytan.handler.QuestionPoller: ID 1313: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:52:11,133 DEBUG    pytan.handler.QuestionPoller: ID 1313: Timing: Started: 2015-08-07 19:51:11.061733, Expiration: 2015-08-07 20:01:11, Override Timeout: None, Elapsed Time: 0:01:00.071279, Left till expiry: 0:08:59.866991, Loop Count: 13
    2015-08-07 19:52:16,136 DEBUG    pytan.handler.QuestionPoller: ID 1313: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:52:16,136 DEBUG    pytan.handler.QuestionPoller: ID 1313: Timing: Started: 2015-08-07 19:51:11.061733, Expiration: 2015-08-07 20:01:11, Override Timeout: None, Elapsed Time: 0:01:05.075223, Left till expiry: 0:08:54.863047, Loop Count: 14
    2015-08-07 19:52:21,142 DEBUG    pytan.handler.QuestionPoller: ID 1313: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-07 19:52:21,142 DEBUG    pytan.handler.QuestionPoller: ID 1313: Timing: Started: 2015-08-07 19:51:11.061733, Expiration: 2015-08-07 20:01:11, Override Timeout: None, Elapsed Time: 0:01:10.080823, Left till expiry: 0:08:49.857446, Loop Count: 15
    2015-08-07 19:52:21,142 INFO     pytan.handler.QuestionPoller: ID 1313: Progress Changed 100% (2 of 2)
    2015-08-07 19:52:21,142 INFO     pytan.handler.QuestionPoller: ID 1313: Reached Threshold of 99% (2 of 2)
    
    print the export_str returned from export_obj():
    Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
    2015-08-07 19:49:40,850 DEBUG    pytan.handler.QuestionPoller: ID 1312: id resolved to 1312
    2015-08-07 19:49:40,850 DEBUG    pytan.handler.QuestionPoller: ID 1312: expiration resolved to 2015-08-07T19:59:41
    2015-08-07 19:49:40,850 DEBUG    pytan.handler.QuestionPoller: ID 1312: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:49:40,850 DEBUG    pytan.handler.QuestionPoller: ID 1312: id resolved to 1312
    2015-08-07 19:49:40,850 DEBUG    pytan.handler.QuestionPoller: ID 1312: Object Info resolved to Question ID: 1312, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:49:40,853 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:49:40,853 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:00:00.003307, Left till expiry: 0:10:00.146043, Loop Count: 1
    2015-08-07 19:49:40,854 INFO     pytan.handler.QuestionPoller: ID 1312: Progress Changed 0% (0 of 2)
    2015-08-07 19:49:45,859 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:49:45,859 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:00:05.008874, Left till expiry: 0:09:55.140477, Loop Count: 2
    2015-08-07 19:49:50,863 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:49:50,863 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:00:10.013265, Left till expiry: 0:09:50.136086, Loop Count: 3
    2015-08-07 19:49:55,870 DEBUG    pytan.handler.QuestionPoller: ID 1312: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:49:55,870 DEBUG    pytan.handler.QuestionPoller: ID 1312: Timing: Started: 2015-08-07 19:49:40.850652, Expiration: 2015-08-07 19:59:41, Override Timeout: None, Elapsed Time: 0:00:15.019570, Left till expiry: 0:09:45.129781, Loop Count: 4
    ..trimmed for brevity..
