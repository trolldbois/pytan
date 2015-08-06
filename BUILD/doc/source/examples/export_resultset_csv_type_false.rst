
Export resultset csv type false
==========================================================================================

Export a ResultSet from asking a question as CSV with false for header_add_type

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
    export_kwargs["header_add_type"] = False
    
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
    2015-08-06 15:08:36,239 DEBUG    pytan.handler.QuestionPoller: ID 86288: id resolved to 86288
    2015-08-06 15:08:36,239 DEBUG    pytan.handler.QuestionPoller: ID 86288: expiration resolved to 2015-08-06T15:18:36
    2015-08-06 15:08:36,239 DEBUG    pytan.handler.QuestionPoller: ID 86288: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 15:08:36,239 DEBUG    pytan.handler.QuestionPoller: ID 86288: id resolved to 86288
    2015-08-06 15:08:36,239 DEBUG    pytan.handler.QuestionPoller: ID 86288: Object Info resolved to Question ID: 86288, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 15:08:36,243 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:08:36,244 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:00:00.004238, Left till expiry: 0:09:59.756002, Loop Count: 1
    2015-08-06 15:08:36,244 INFO     pytan.handler.QuestionPoller: ID 86288: Progress Changed 0% (0 of 2)
    2015-08-06 15:08:41,255 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:08:41,256 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:00:05.016272, Left till expiry: 0:09:54.743968, Loop Count: 2
    2015-08-06 15:08:46,268 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:08:46,268 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:00:10.028713, Left till expiry: 0:09:49.731528, Loop Count: 3
    2015-08-06 15:08:51,280 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:08:51,280 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:00:15.040790, Left till expiry: 0:09:44.719451, Loop Count: 4
    2015-08-06 15:08:56,292 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:08:56,292 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:00:20.052754, Left till expiry: 0:09:39.707487, Loop Count: 5
    2015-08-06 15:09:01,305 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:09:01,305 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:00:25.065788, Left till expiry: 0:09:34.694452, Loop Count: 6
    2015-08-06 15:09:06,312 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:09:06,312 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:00:30.072941, Left till expiry: 0:09:29.687300, Loop Count: 7
    2015-08-06 15:09:11,326 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:09:11,326 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:00:35.087166, Left till expiry: 0:09:24.673074, Loop Count: 8
    2015-08-06 15:09:16,331 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:09:16,331 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:00:40.091920, Left till expiry: 0:09:19.668321, Loop Count: 9
    2015-08-06 15:09:21,342 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:09:21,342 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:00:45.102956, Left till expiry: 0:09:14.657285, Loop Count: 10
    2015-08-06 15:09:26,348 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:09:26,348 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:00:50.109189, Left till expiry: 0:09:09.651051, Loop Count: 11
    2015-08-06 15:09:31,362 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:09:31,362 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:00:55.122754, Left till expiry: 0:09:04.637487, Loop Count: 12
    2015-08-06 15:09:36,374 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:09:36,374 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:01:00.135072, Left till expiry: 0:08:59.625168, Loop Count: 13
    2015-08-06 15:09:41,380 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:09:41,380 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:01:05.140574, Left till expiry: 0:08:54.619667, Loop Count: 14
    2015-08-06 15:09:46,393 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:09:46,394 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:01:10.154223, Left till expiry: 0:08:49.606019, Loop Count: 15
    2015-08-06 15:09:51,407 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:09:51,407 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:01:15.168062, Left till expiry: 0:08:44.592178, Loop Count: 16
    2015-08-06 15:09:56,417 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:09:56,417 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:01:20.177914, Left till expiry: 0:08:39.582326, Loop Count: 17
    2015-08-06 15:10:01,427 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:10:01,427 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:01:25.187757, Left till expiry: 0:08:34.572484, Loop Count: 18
    2015-08-06 15:10:06,442 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:10:06,442 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:01:30.202387, Left till expiry: 0:08:29.557854, Loop Count: 19
    2015-08-06 15:10:11,458 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:10:11,458 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:01:35.218606, Left till expiry: 0:08:24.541634, Loop Count: 20
    2015-08-06 15:10:16,466 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:10:16,466 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:01:40.226561, Left till expiry: 0:08:19.533680, Loop Count: 21
    2015-08-06 15:10:21,476 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:10:21,476 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:01:45.237146, Left till expiry: 0:08:14.523095, Loop Count: 22
    2015-08-06 15:10:26,490 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:10:26,490 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:01:50.251156, Left till expiry: 0:08:09.509086, Loop Count: 23
    2015-08-06 15:10:31,496 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:10:31,497 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:01:55.257297, Left till expiry: 0:08:04.502943, Loop Count: 24
    2015-08-06 15:10:36,505 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:10:36,505 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:02:00.265997, Left till expiry: 0:07:59.494243, Loop Count: 25
    2015-08-06 15:10:41,518 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:10:41,519 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:02:05.279228, Left till expiry: 0:07:54.481012, Loop Count: 26
    2015-08-06 15:10:46,531 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:10:46,531 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:02:10.291377, Left till expiry: 0:07:49.468864, Loop Count: 27
    2015-08-06 15:10:51,545 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:10:51,545 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:02:15.305433, Left till expiry: 0:07:44.454807, Loop Count: 28
    2015-08-06 15:10:56,557 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:10:56,557 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:02:20.317969, Left till expiry: 0:07:39.442272, Loop Count: 29
    2015-08-06 15:11:01,564 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-06 15:11:01,564 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:02:25.325121, Left till expiry: 0:07:34.435119, Loop Count: 30
    2015-08-06 15:11:01,564 INFO     pytan.handler.QuestionPoller: ID 86288: Progress Changed 50% (1 of 2)
    2015-08-06 15:11:06,573 DEBUG    pytan.handler.QuestionPoller: ID 86288: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-06 15:11:06,573 DEBUG    pytan.handler.QuestionPoller: ID 86288: Timing: Started: 2015-08-06 15:08:36.239762, Expiration: 2015-08-06 15:18:36, Override Timeout: None, Elapsed Time: 0:02:30.333572, Left till expiry: 0:07:29.426669, Loop Count: 31
    2015-08-06 15:11:06,573 INFO     pytan.handler.QuestionPoller: ID 86288: Progress Changed 100% (2 of 2)
    2015-08-06 15:11:06,573 INFO     pytan.handler.QuestionPoller: ID 86288: Reached Threshold of 99% (2 of 2)
    
    print the export_str returned from export_obj():
    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
    2015-08-06 15:08:10,929 DEBUG    pytan.handler.QuestionPoller: ID 86286: id resolved to 86286
    2015-08-06 15:08:10,929 DEBUG    pytan.handler.QuestionPoller: ID 86286: expiration resolved to 2015-08-06T15:18:11
    2015-08-06 15:08:10,929 DEBUG    pytan.handler.QuestionPoller: ID 86286: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 15:08:10,929 DEBUG    pytan.handler.QuestionPoller: ID 86286: id resolved to 86286
    2015-08-06 15:08:10,929 DEBUG    pytan.handler.QuestionPoller: ID 86286: Object Info resolved to Question ID: 86286, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 15:08:10,934 DEBUG    pytan.handler.QuestionPoller: ID 86286: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:08:10,934 DEBUG    pytan.handler.QuestionPoller: ID 86286: Timing: Started: 2015-08-06 15:08:10.929576, Expiration: 2015-08-06 15:18:11, Override Timeout: None, Elapsed Time: 0:00:00.005193, Left till expiry: 0:10:00.065234, Loop Count: 1
    2015-08-06 15:08:10,934 INFO     pytan.handler.QuestionPoller: ID 86286: Progress Changed 0% (0 of 2)
    2015-08-06 15:08:15,949 DEBUG    pytan.handler.QuestionPoller: ID 86286: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:08:15,949 DEBUG    pytan.handler.QuestionPoller: ID 86286: Timing: Started: 2015-08-06 15:08:10.929576, Expiration: 2015-08-06 15:18:11, Override Timeout: None, Elapsed Time: 0:00:05.020180, Left till expiry: 0:09:55.050246, Loop Count: 2
    2015-08-06 15:08:20,961 DEBUG    pytan.handler.QuestionPoller: ID 86286: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:08:20,961 DEBUG    pytan.handler.QuestionPoller: ID 86286: Timing: Started: 2015-08-06 15:08:10.929576, Expiration: 2015-08-06 15:18:11, Override Timeout: None, Elapsed Time: 0:00:10.032312, Left till expiry: 0:09:50.038114, Loop Count: 3
    2015-08-06 15:08:25,969 DEBUG    pytan.handler.QuestionPoller: ID 86286: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:08:25,969 DEBUG    pytan.handler.QuestionPoller: ID 86286: Timing: Started: 2015-08-06 15:08:10.929576, Expiration: 2015-08-06 15:18:11, Override Timeout: None, Elapsed Time: 0:00:15.039880, Left till expiry: 0:09:45.030547, Loop Count: 4
    ..trimmed for brevity..
