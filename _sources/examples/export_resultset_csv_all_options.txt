
Export resultset csv all options
==========================================================================================

Export a ResultSet from asking a question as CSV with true for header_add_sensor, true for header_add_type, true for header_sort, and true for expand_grouped_columns

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
    export_kwargs["header_sort"] = True
    export_kwargs["export_format"] = u'csv'
    export_kwargs["header_add_type"] = True
    export_kwargs["expand_grouped_columns"] = True
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
    2015-08-07 19:47:40,405 DEBUG    pytan.handler.QuestionPoller: ID 1310: id resolved to 1310
    2015-08-07 19:47:40,405 DEBUG    pytan.handler.QuestionPoller: ID 1310: expiration resolved to 2015-08-07T19:57:40
    2015-08-07 19:47:40,405 DEBUG    pytan.handler.QuestionPoller: ID 1310: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:47:40,405 DEBUG    pytan.handler.QuestionPoller: ID 1310: id resolved to 1310
    2015-08-07 19:47:40,405 DEBUG    pytan.handler.QuestionPoller: ID 1310: Object Info resolved to Question ID: 1310, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:47:40,408 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:47:40,408 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:00:00.003303, Left till expiry: 0:09:59.591432, Loop Count: 1
    2015-08-07 19:47:40,408 INFO     pytan.handler.QuestionPoller: ID 1310: Progress Changed 0% (0 of 2)
    2015-08-07 19:47:45,417 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:47:45,417 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:00:05.011970, Left till expiry: 0:09:54.582765, Loop Count: 2
    2015-08-07 19:47:50,421 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:47:50,421 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:00:10.016661, Left till expiry: 0:09:49.578074, Loop Count: 3
    2015-08-07 19:47:55,425 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:47:55,425 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:00:15.019979, Left till expiry: 0:09:44.574756, Loop Count: 4
    2015-08-07 19:48:00,431 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:48:00,431 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:00:20.025831, Left till expiry: 0:09:39.568904, Loop Count: 5
    2015-08-07 19:48:05,435 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:48:05,435 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:00:25.030218, Left till expiry: 0:09:34.564517, Loop Count: 6
    2015-08-07 19:48:10,440 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:48:10,440 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:00:30.035029, Left till expiry: 0:09:29.559706, Loop Count: 7
    2015-08-07 19:48:15,444 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:48:15,444 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:00:35.039067, Left till expiry: 0:09:24.555668, Loop Count: 8
    2015-08-07 19:48:20,449 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:48:20,449 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:00:40.043950, Left till expiry: 0:09:19.550785, Loop Count: 9
    2015-08-07 19:48:25,453 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:48:25,453 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:00:45.048264, Left till expiry: 0:09:14.546470, Loop Count: 10
    2015-08-07 19:48:30,459 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:48:30,459 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:00:50.054107, Left till expiry: 0:09:09.540628, Loop Count: 11
    2015-08-07 19:48:35,467 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:48:35,467 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:00:55.061952, Left till expiry: 0:09:04.532783, Loop Count: 12
    2015-08-07 19:48:40,473 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:48:40,473 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:01:00.067868, Left till expiry: 0:08:59.526866, Loop Count: 13
    2015-08-07 19:48:45,481 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:48:45,481 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:01:05.075823, Left till expiry: 0:08:54.518912, Loop Count: 14
    2015-08-07 19:48:50,489 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:48:50,489 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:01:10.083874, Left till expiry: 0:08:49.510861, Loop Count: 15
    2015-08-07 19:48:55,493 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:48:55,493 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:01:15.088429, Left till expiry: 0:08:44.506306, Loop Count: 16
    2015-08-07 19:48:55,493 INFO     pytan.handler.QuestionPoller: ID 1310: Progress Changed 50% (1 of 2)
    2015-08-07 19:49:00,497 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:49:00,497 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:01:20.092569, Left till expiry: 0:08:39.502166, Loop Count: 17
    2015-08-07 19:49:05,502 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:49:05,502 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:01:25.096991, Left till expiry: 0:08:34.497743, Loop Count: 18
    2015-08-07 19:49:10,508 DEBUG    pytan.handler.QuestionPoller: ID 1310: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-07 19:49:10,508 DEBUG    pytan.handler.QuestionPoller: ID 1310: Timing: Started: 2015-08-07 19:47:40.405268, Expiration: 2015-08-07 19:57:40, Override Timeout: None, Elapsed Time: 0:01:30.103499, Left till expiry: 0:08:29.491236, Loop Count: 19
    2015-08-07 19:49:10,508 INFO     pytan.handler.QuestionPoller: ID 1310: Progress Changed 100% (2 of 2)
    2015-08-07 19:49:10,508 INFO     pytan.handler.QuestionPoller: ID 1310: Reached Threshold of 99% (2 of 2)
    
    print the export_str returned from export_obj():
    Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
    2015-08-07 19:47:10,227 DEBUG    pytan.handler.QuestionPoller: ID 1309: id resolved to 1309
    2015-08-07 19:47:10,227 DEBUG    pytan.handler.QuestionPoller: ID 1309: expiration resolved to 2015-08-07T19:57:10
    2015-08-07 19:47:10,227 DEBUG    pytan.handler.QuestionPoller: ID 1309: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:47:10,227 DEBUG    pytan.handler.QuestionPoller: ID 1309: id resolved to 1309
    2015-08-07 19:47:10,227 DEBUG    pytan.handler.QuestionPoller: ID 1309: Object Info resolved to Question ID: 1309, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:47:10,231 DEBUG    pytan.handler.QuestionPoller: ID 1309: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:47:10,231 DEBUG    pytan.handler.QuestionPoller: ID 1309: Timing: Started: 2015-08-07 19:47:10.228036, Expiration: 2015-08-07 19:57:10, Override Timeout: None, Elapsed Time: 0:00:00.003356, Left till expiry: 0:09:59.768610, Loop Count: 1
    2015-08-07 19:47:10,231 INFO     pytan.handler.QuestionPoller: ID 1309: Progress Changed 0% (0 of 2)
    2015-08-07 19:47:15,235 DEBUG    pytan.handler.QuestionPoller: ID 1309: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:47:15,235 DEBUG    pytan.handler.QuestionPoller: ID 1309: Timing: Started: 2015-08-07 19:47:10.228036, Expiration: 2015-08-07 19:57:10, Override Timeout: None, Elapsed Time: 0:00:05.007626, Left till expiry: 0:09:54.764341, Loop Count: 2
    2015-08-07 19:47:20,239 DEBUG    pytan.handler.QuestionPoller: ID 1309: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:47:20,239 DEBUG    pytan.handler.QuestionPoller: ID 1309: Timing: Started: 2015-08-07 19:47:10.228036, Expiration: 2015-08-07 19:57:10, Override Timeout: None, Elapsed Time: 0:00:10.011415, Left till expiry: 0:09:49.760552, Loop Count: 3
    2015-08-07 19:47:20,239 INFO     pytan.handler.QuestionPoller: ID 1309: Progress Changed 50% (1 of 2)
    2015-08-07 19:47:25,243 DEBUG    pytan.handler.QuestionPoller: ID 1309: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    ..trimmed for brevity..
