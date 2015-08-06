
Export resultset csv expand true
==========================================================================================

Export a ResultSet from asking a question as CSV with true for expand_grouped_columns

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
    export_kwargs["expand_grouped_columns"] = True
    
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
    2015-08-06 14:58:37,302 DEBUG    pytan.handler.QuestionPoller: ID 86277: id resolved to 86277
    2015-08-06 14:58:37,302 DEBUG    pytan.handler.QuestionPoller: ID 86277: expiration resolved to 2015-08-06T15:08:37
    2015-08-06 14:58:37,302 DEBUG    pytan.handler.QuestionPoller: ID 86277: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 14:58:37,302 DEBUG    pytan.handler.QuestionPoller: ID 86277: id resolved to 86277
    2015-08-06 14:58:37,302 DEBUG    pytan.handler.QuestionPoller: ID 86277: Object Info resolved to Question ID: 86277, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 14:58:37,307 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:58:37,307 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:00:00.004670, Left till expiry: 0:09:59.692356, Loop Count: 1
    2015-08-06 14:58:37,307 INFO     pytan.handler.QuestionPoller: ID 86277: Progress Changed 0% (0 of 2)
    2015-08-06 14:58:42,316 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:58:42,316 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:00:05.013225, Left till expiry: 0:09:54.683801, Loop Count: 2
    2015-08-06 14:58:47,321 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:58:47,321 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:00:10.018281, Left till expiry: 0:09:49.678744, Loop Count: 3
    2015-08-06 14:58:52,332 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:58:52,332 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:00:15.029218, Left till expiry: 0:09:44.667808, Loop Count: 4
    2015-08-06 14:58:57,339 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:58:57,339 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:00:20.036340, Left till expiry: 0:09:39.660685, Loop Count: 5
    2015-08-06 14:59:02,346 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:59:02,346 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:00:25.043544, Left till expiry: 0:09:34.653482, Loop Count: 6
    2015-08-06 14:59:07,353 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:59:07,353 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:00:30.050690, Left till expiry: 0:09:29.646336, Loop Count: 7
    2015-08-06 14:59:12,363 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:59:12,363 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:00:35.060588, Left till expiry: 0:09:24.636438, Loop Count: 8
    2015-08-06 14:59:17,372 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:59:17,372 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:00:40.069857, Left till expiry: 0:09:19.627168, Loop Count: 9
    2015-08-06 14:59:22,381 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:59:22,381 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:00:45.078355, Left till expiry: 0:09:14.618673, Loop Count: 10
    2015-08-06 14:59:27,392 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:59:27,393 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:00:50.090042, Left till expiry: 0:09:09.606984, Loop Count: 11
    2015-08-06 14:59:32,403 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:59:32,403 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:00:55.100134, Left till expiry: 0:09:04.596891, Loop Count: 12
    2015-08-06 14:59:37,414 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:59:37,414 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:01:00.111433, Left till expiry: 0:08:59.585592, Loop Count: 13
    2015-08-06 14:59:42,421 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:59:42,421 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:01:05.118681, Left till expiry: 0:08:54.578345, Loop Count: 14
    2015-08-06 14:59:47,430 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:59:47,430 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:01:10.127483, Left till expiry: 0:08:49.569543, Loop Count: 15
    2015-08-06 14:59:52,439 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:59:52,439 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:01:15.136660, Left till expiry: 0:08:44.560366, Loop Count: 16
    2015-08-06 14:59:57,444 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:59:57,444 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:01:20.142003, Left till expiry: 0:08:39.555023, Loop Count: 17
    2015-08-06 15:00:02,449 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:00:02,449 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:01:25.146794, Left till expiry: 0:08:34.550231, Loop Count: 18
    2015-08-06 15:00:07,455 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:00:07,455 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:01:30.152284, Left till expiry: 0:08:29.544742, Loop Count: 19
    2015-08-06 15:00:12,463 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:00:12,463 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:01:35.160102, Left till expiry: 0:08:24.536924, Loop Count: 20
    2015-08-06 15:00:17,471 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:00:17,471 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:01:40.168292, Left till expiry: 0:08:19.528733, Loop Count: 21
    2015-08-06 15:00:22,479 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:00:22,479 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:01:45.176276, Left till expiry: 0:08:14.520749, Loop Count: 22
    2015-08-06 15:00:27,486 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:00:27,486 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:01:50.183386, Left till expiry: 0:08:09.513640, Loop Count: 23
    2015-08-06 15:00:32,494 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:00:32,494 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:01:55.191492, Left till expiry: 0:08:04.505534, Loop Count: 24
    2015-08-06 15:00:37,506 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:00:37,506 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:02:00.203250, Left till expiry: 0:07:59.493778, Loop Count: 25
    2015-08-06 15:00:42,513 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:00:42,513 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:02:05.210806, Left till expiry: 0:07:54.486219, Loop Count: 26
    2015-08-06 15:00:47,519 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:00:47,519 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:02:10.216196, Left till expiry: 0:07:49.480829, Loop Count: 27
    2015-08-06 15:00:52,528 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:00:52,528 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:02:15.225512, Left till expiry: 0:07:44.471513, Loop Count: 28
    2015-08-06 15:00:57,536 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:00:57,536 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:02:20.233222, Left till expiry: 0:07:39.463803, Loop Count: 29
    2015-08-06 15:01:02,545 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:01:02,545 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:02:25.242244, Left till expiry: 0:07:34.454782, Loop Count: 30
    2015-08-06 15:01:07,555 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:01:07,555 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:02:30.252364, Left till expiry: 0:07:29.444662, Loop Count: 31
    2015-08-06 15:01:12,561 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:01:12,561 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:02:35.258143, Left till expiry: 0:07:24.438882, Loop Count: 32
    2015-08-06 15:01:17,566 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:01:17,566 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:02:40.263464, Left till expiry: 0:07:19.433563, Loop Count: 33
    2015-08-06 15:01:22,576 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:01:22,576 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:02:45.273617, Left till expiry: 0:07:14.423409, Loop Count: 34
    2015-08-06 15:01:27,584 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:01:27,584 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:02:50.281777, Left till expiry: 0:07:09.415249, Loop Count: 35
    2015-08-06 15:01:32,592 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:01:32,592 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:02:55.289605, Left till expiry: 0:07:04.407420, Loop Count: 36
    2015-08-06 15:01:37,601 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:01:37,601 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:03:00.298980, Left till expiry: 0:06:59.398046, Loop Count: 37
    2015-08-06 15:01:42,613 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:01:42,613 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:03:05.310207, Left till expiry: 0:06:54.386819, Loop Count: 38
    2015-08-06 15:01:47,618 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:01:47,618 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:03:10.315517, Left till expiry: 0:06:49.381508, Loop Count: 39
    2015-08-06 15:01:52,624 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:01:52,624 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:03:15.321112, Left till expiry: 0:06:44.375914, Loop Count: 40
    2015-08-06 15:01:57,628 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:01:57,628 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:03:20.325609, Left till expiry: 0:06:39.371416, Loop Count: 41
    2015-08-06 15:02:02,637 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:02:02,638 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:03:25.335045, Left till expiry: 0:06:34.361981, Loop Count: 42
    2015-08-06 15:02:07,647 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:02:07,647 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:03:30.344624, Left till expiry: 0:06:29.352401, Loop Count: 43
    2015-08-06 15:02:12,658 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:02:12,658 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:03:35.355807, Left till expiry: 0:06:24.341219, Loop Count: 44
    2015-08-06 15:02:17,669 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:02:17,669 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:03:40.366872, Left till expiry: 0:06:19.330153, Loop Count: 45
    2015-08-06 15:02:22,674 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:02:22,674 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:03:45.371879, Left till expiry: 0:06:14.325147, Loop Count: 46
    2015-08-06 15:02:27,680 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:02:27,680 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:03:50.377157, Left till expiry: 0:06:09.319868, Loop Count: 47
    2015-08-06 15:02:32,685 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:02:32,686 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:03:55.383081, Left till expiry: 0:06:04.313944, Loop Count: 48
    2015-08-06 15:02:37,694 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:02:37,694 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:04:00.391514, Left till expiry: 0:05:59.305512, Loop Count: 49
    2015-08-06 15:02:42,699 DEBUG    pytan.handler.QuestionPoller: ID 86277: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-06 15:02:42,699 DEBUG    pytan.handler.QuestionPoller: ID 86277: Timing: Started: 2015-08-06 14:58:37.302977, Expiration: 2015-08-06 15:08:37, Override Timeout: None, Elapsed Time: 0:04:05.396850, Left till expiry: 0:05:54.300176, Loop Count: 50
    2015-08-06 15:02:42,699 INFO     pytan.handler.QuestionPoller: ID 86277: Progress Changed 100% (2 of 2)
    2015-08-06 15:02:42,699 INFO     pytan.handler.QuestionPoller: ID 86277: Reached Threshold of 99% (2 of 2)
    
    print the export_str returned from export_obj():
    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
    2015-08-06 14:58:11,791 DEBUG    pytan.handler.QuestionPoller: ID 86276: id resolved to 86276
    2015-08-06 14:58:11,792 DEBUG    pytan.handler.QuestionPoller: ID 86276: expiration resolved to 2015-08-06T15:08:11
    2015-08-06 14:58:11,792 DEBUG    pytan.handler.QuestionPoller: ID 86276: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 14:58:11,792 DEBUG    pytan.handler.QuestionPoller: ID 86276: id resolved to 86276
    2015-08-06 14:58:11,792 DEBUG    pytan.handler.QuestionPoller: ID 86276: Object Info resolved to Question ID: 86276, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 14:58:11,797 DEBUG    pytan.handler.QuestionPoller: ID 86276: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:58:11,797 DEBUG    pytan.handler.QuestionPoller: ID 86276: Timing: Started: 2015-08-06 14:58:11.792215, Expiration: 2015-08-06 15:08:11, Override Timeout: None, Elapsed Time: 0:00:00.004865, Left till expiry: 0:09:59.202922, Loop Count: 1
    2015-08-06 14:58:11,797 INFO     pytan.handler.QuestionPoller: ID 86276: Progress Changed 0% (0 of 2)
    2015-08-06 14:58:16,802 DEBUG    pytan.handler.QuestionPoller: ID 86276: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:58:16,802 DEBUG    pytan.handler.QuestionPoller: ID 86276: Timing: Started: 2015-08-06 14:58:11.792215, Expiration: 2015-08-06 15:08:11, Override Timeout: None, Elapsed Time: 0:00:05.010000, Left till expiry: 0:09:54.197787, Loop Count: 2
    2015-08-06 14:58:21,808 DEBUG    pytan.handler.QuestionPoller: ID 86276: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:58:21,808 DEBUG    pytan.handler.QuestionPoller: ID 86276: Timing: Started: 2015-08-06 14:58:11.792215, Expiration: 2015-08-06 15:08:11, Override Timeout: None, Elapsed Time: 0:00:10.016583, Left till expiry: 0:09:49.191204, Loop Count: 3
    2015-08-06 14:58:26,816 DEBUG    pytan.handler.QuestionPoller: ID 86276: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:58:26,816 DEBUG    pytan.handler.QuestionPoller: ID 86276: Timing: Started: 2015-08-06 14:58:11.792215, Expiration: 2015-08-06 15:08:11, Override Timeout: None, Elapsed Time: 0:00:15.024291, Left till expiry: 0:09:44.183496, Loop Count: 4
    ..trimmed for brevity..
