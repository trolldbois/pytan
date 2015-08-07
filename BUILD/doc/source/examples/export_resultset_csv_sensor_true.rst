
Export resultset csv sensor true
==========================================================================================

Export a ResultSet from asking a question as CSV with true for header_add_sensor

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
    export_kwargs["header_add_sensor"] = True
    
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
    2015-08-07 19:55:27,070 DEBUG    pytan.handler.QuestionPoller: ID 1321: id resolved to 1321
    2015-08-07 19:55:27,070 DEBUG    pytan.handler.QuestionPoller: ID 1321: expiration resolved to 2015-08-07T20:05:27
    2015-08-07 19:55:27,070 DEBUG    pytan.handler.QuestionPoller: ID 1321: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:55:27,070 DEBUG    pytan.handler.QuestionPoller: ID 1321: id resolved to 1321
    2015-08-07 19:55:27,070 DEBUG    pytan.handler.QuestionPoller: ID 1321: Object Info resolved to Question ID: 1321, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:55:27,074 DEBUG    pytan.handler.QuestionPoller: ID 1321: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:55:27,074 DEBUG    pytan.handler.QuestionPoller: ID 1321: Timing: Started: 2015-08-07 19:55:27.070716, Expiration: 2015-08-07 20:05:27, Override Timeout: None, Elapsed Time: 0:00:00.003559, Left till expiry: 0:09:59.925727, Loop Count: 1
    2015-08-07 19:55:27,074 INFO     pytan.handler.QuestionPoller: ID 1321: Progress Changed 0% (0 of 2)
    2015-08-07 19:55:32,077 DEBUG    pytan.handler.QuestionPoller: ID 1321: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:55:32,077 DEBUG    pytan.handler.QuestionPoller: ID 1321: Timing: Started: 2015-08-07 19:55:27.070716, Expiration: 2015-08-07 20:05:27, Override Timeout: None, Elapsed Time: 0:00:05.007012, Left till expiry: 0:09:54.922275, Loop Count: 2
    2015-08-07 19:55:37,083 DEBUG    pytan.handler.QuestionPoller: ID 1321: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:55:37,083 DEBUG    pytan.handler.QuestionPoller: ID 1321: Timing: Started: 2015-08-07 19:55:27.070716, Expiration: 2015-08-07 20:05:27, Override Timeout: None, Elapsed Time: 0:00:10.012396, Left till expiry: 0:09:49.916892, Loop Count: 3
    2015-08-07 19:55:42,089 DEBUG    pytan.handler.QuestionPoller: ID 1321: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:55:42,089 DEBUG    pytan.handler.QuestionPoller: ID 1321: Timing: Started: 2015-08-07 19:55:27.070716, Expiration: 2015-08-07 20:05:27, Override Timeout: None, Elapsed Time: 0:00:15.018729, Left till expiry: 0:09:44.910557, Loop Count: 4
    2015-08-07 19:55:47,097 DEBUG    pytan.handler.QuestionPoller: ID 1321: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:55:47,097 DEBUG    pytan.handler.QuestionPoller: ID 1321: Timing: Started: 2015-08-07 19:55:27.070716, Expiration: 2015-08-07 20:05:27, Override Timeout: None, Elapsed Time: 0:00:20.026650, Left till expiry: 0:09:39.902636, Loop Count: 5
    2015-08-07 19:55:52,105 DEBUG    pytan.handler.QuestionPoller: ID 1321: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:55:52,105 DEBUG    pytan.handler.QuestionPoller: ID 1321: Timing: Started: 2015-08-07 19:55:27.070716, Expiration: 2015-08-07 20:05:27, Override Timeout: None, Elapsed Time: 0:00:25.034907, Left till expiry: 0:09:34.894380, Loop Count: 6
    2015-08-07 19:55:57,112 DEBUG    pytan.handler.QuestionPoller: ID 1321: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:55:57,112 DEBUG    pytan.handler.QuestionPoller: ID 1321: Timing: Started: 2015-08-07 19:55:27.070716, Expiration: 2015-08-07 20:05:27, Override Timeout: None, Elapsed Time: 0:00:30.041879, Left till expiry: 0:09:29.887407, Loop Count: 7
    2015-08-07 19:56:02,119 DEBUG    pytan.handler.QuestionPoller: ID 1321: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:56:02,119 DEBUG    pytan.handler.QuestionPoller: ID 1321: Timing: Started: 2015-08-07 19:55:27.070716, Expiration: 2015-08-07 20:05:27, Override Timeout: None, Elapsed Time: 0:00:35.049220, Left till expiry: 0:09:24.880067, Loop Count: 8
    2015-08-07 19:56:07,129 DEBUG    pytan.handler.QuestionPoller: ID 1321: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:56:07,129 DEBUG    pytan.handler.QuestionPoller: ID 1321: Timing: Started: 2015-08-07 19:55:27.070716, Expiration: 2015-08-07 20:05:27, Override Timeout: None, Elapsed Time: 0:00:40.058828, Left till expiry: 0:09:19.870460, Loop Count: 9
    2015-08-07 19:56:12,138 DEBUG    pytan.handler.QuestionPoller: ID 1321: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:56:12,138 DEBUG    pytan.handler.QuestionPoller: ID 1321: Timing: Started: 2015-08-07 19:55:27.070716, Expiration: 2015-08-07 20:05:27, Override Timeout: None, Elapsed Time: 0:00:45.068182, Left till expiry: 0:09:14.861106, Loop Count: 10
    2015-08-07 19:56:17,145 DEBUG    pytan.handler.QuestionPoller: ID 1321: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:56:17,145 DEBUG    pytan.handler.QuestionPoller: ID 1321: Timing: Started: 2015-08-07 19:55:27.070716, Expiration: 2015-08-07 20:05:27, Override Timeout: None, Elapsed Time: 0:00:50.074566, Left till expiry: 0:09:09.854721, Loop Count: 11
    2015-08-07 19:56:22,152 DEBUG    pytan.handler.QuestionPoller: ID 1321: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:56:22,152 DEBUG    pytan.handler.QuestionPoller: ID 1321: Timing: Started: 2015-08-07 19:55:27.070716, Expiration: 2015-08-07 20:05:27, Override Timeout: None, Elapsed Time: 0:00:55.082227, Left till expiry: 0:09:04.847060, Loop Count: 12
    2015-08-07 19:56:27,160 DEBUG    pytan.handler.QuestionPoller: ID 1321: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:56:27,160 DEBUG    pytan.handler.QuestionPoller: ID 1321: Timing: Started: 2015-08-07 19:55:27.070716, Expiration: 2015-08-07 20:05:27, Override Timeout: None, Elapsed Time: 0:01:00.089654, Left till expiry: 0:08:59.839633, Loop Count: 13
    2015-08-07 19:56:32,167 DEBUG    pytan.handler.QuestionPoller: ID 1321: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-07 19:56:32,167 DEBUG    pytan.handler.QuestionPoller: ID 1321: Timing: Started: 2015-08-07 19:55:27.070716, Expiration: 2015-08-07 20:05:27, Override Timeout: None, Elapsed Time: 0:01:05.096714, Left till expiry: 0:08:54.832573, Loop Count: 14
    2015-08-07 19:56:32,167 INFO     pytan.handler.QuestionPoller: ID 1321: Progress Changed 100% (2 of 2)
    2015-08-07 19:56:32,167 INFO     pytan.handler.QuestionPoller: ID 1321: Reached Threshold of 99% (2 of 2)
    
    print the export_str returned from export_obj():
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
    ..trimmed for brevity..
