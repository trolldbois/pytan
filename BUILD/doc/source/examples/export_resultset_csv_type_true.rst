
Export resultset csv type true
==========================================================================================

Export a ResultSet from asking a question as CSV with true for header_add_type

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
    export_kwargs["header_add_type"] = True
    
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
    2015-08-06 15:11:06,894 DEBUG    pytan.handler.QuestionPoller: ID 86290: id resolved to 86290
    2015-08-06 15:11:06,894 DEBUG    pytan.handler.QuestionPoller: ID 86290: expiration resolved to 2015-08-06T15:21:06
    2015-08-06 15:11:06,894 DEBUG    pytan.handler.QuestionPoller: ID 86290: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 15:11:06,894 DEBUG    pytan.handler.QuestionPoller: ID 86290: id resolved to 86290
    2015-08-06 15:11:06,894 DEBUG    pytan.handler.QuestionPoller: ID 86290: Object Info resolved to Question ID: 86290, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 15:11:06,898 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:11:06,898 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:00:00.004455, Left till expiry: 0:09:59.101312, Loop Count: 1
    2015-08-06 15:11:06,898 INFO     pytan.handler.QuestionPoller: ID 86290: Progress Changed 0% (0 of 2)
    2015-08-06 15:11:11,908 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:11:11,908 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:00:05.014495, Left till expiry: 0:09:54.091273, Loop Count: 2
    2015-08-06 15:11:16,919 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:11:16,919 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:00:10.025055, Left till expiry: 0:09:49.080713, Loop Count: 3
    2015-08-06 15:11:21,929 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:11:21,929 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:00:15.035633, Left till expiry: 0:09:44.070135, Loop Count: 4
    2015-08-06 15:11:26,946 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:11:26,946 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:00:20.052177, Left till expiry: 0:09:39.053591, Loop Count: 5
    2015-08-06 15:11:31,961 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:11:31,961 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:00:25.066856, Left till expiry: 0:09:34.038911, Loop Count: 6
    2015-08-06 15:11:36,976 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:11:36,976 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:00:30.081988, Left till expiry: 0:09:29.023780, Loop Count: 7
    2015-08-06 15:11:41,990 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:11:41,990 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:00:35.096570, Left till expiry: 0:09:24.009198, Loop Count: 8
    2015-08-06 15:11:47,005 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:11:47,005 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:00:40.111348, Left till expiry: 0:09:18.994419, Loop Count: 9
    2015-08-06 15:11:52,013 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:11:52,013 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:00:45.119132, Left till expiry: 0:09:13.986635, Loop Count: 10
    2015-08-06 15:11:57,026 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:11:57,026 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:00:50.132553, Left till expiry: 0:09:08.973214, Loop Count: 11
    2015-08-06 15:12:02,038 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:12:02,039 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:00:55.144760, Left till expiry: 0:09:03.961007, Loop Count: 12
    2015-08-06 15:12:07,054 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:12:07,054 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:01:00.160741, Left till expiry: 0:08:58.945026, Loop Count: 13
    2015-08-06 15:12:12,062 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:12:12,063 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:01:05.168753, Left till expiry: 0:08:53.937015, Loop Count: 14
    2015-08-06 15:12:17,069 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:12:17,069 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:01:10.175644, Left till expiry: 0:08:48.930124, Loop Count: 15
    2015-08-06 15:12:22,085 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:12:22,085 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:01:15.190987, Left till expiry: 0:08:43.914781, Loop Count: 16
    2015-08-06 15:12:27,097 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:12:27,097 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:01:20.203333, Left till expiry: 0:08:38.902434, Loop Count: 17
    2015-08-06 15:12:32,110 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-06 15:12:32,110 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:01:25.216608, Left till expiry: 0:08:33.889159, Loop Count: 18
    2015-08-06 15:12:32,110 INFO     pytan.handler.QuestionPoller: ID 86290: Progress Changed 50% (1 of 2)
    2015-08-06 15:12:37,119 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-06 15:12:37,119 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:01:30.225611, Left till expiry: 0:08:28.880157, Loop Count: 19
    2015-08-06 15:12:42,128 DEBUG    pytan.handler.QuestionPoller: ID 86290: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-06 15:12:42,128 DEBUG    pytan.handler.QuestionPoller: ID 86290: Timing: Started: 2015-08-06 15:11:06.894235, Expiration: 2015-08-06 15:21:06, Override Timeout: None, Elapsed Time: 0:01:35.234350, Left till expiry: 0:08:23.871418, Loop Count: 20
    2015-08-06 15:12:42,128 INFO     pytan.handler.QuestionPoller: ID 86290: Progress Changed 100% (2 of 2)
    2015-08-06 15:12:42,128 INFO     pytan.handler.QuestionPoller: ID 86290: Reached Threshold of 99% (2 of 2)
    
    print the export_str returned from export_obj():
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
    ..trimmed for brevity..
