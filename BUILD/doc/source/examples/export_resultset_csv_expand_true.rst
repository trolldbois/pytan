
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
    2015-08-07 19:47:25,243 DEBUG    pytan.handler.QuestionPoller: ID 1309: Timing: Started: 2015-08-07 19:47:10.228036, Expiration: 2015-08-07 19:57:10, Override Timeout: None, Elapsed Time: 0:00:15.015122, Left till expiry: 0:09:44.756845, Loop Count: 4
    2015-08-07 19:47:30,250 DEBUG    pytan.handler.QuestionPoller: ID 1309: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:47:30,250 DEBUG    pytan.handler.QuestionPoller: ID 1309: Timing: Started: 2015-08-07 19:47:10.228036, Expiration: 2015-08-07 19:57:10, Override Timeout: None, Elapsed Time: 0:00:20.022792, Left till expiry: 0:09:39.749174, Loop Count: 5
    2015-08-07 19:47:35,255 DEBUG    pytan.handler.QuestionPoller: ID 1309: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:47:35,255 DEBUG    pytan.handler.QuestionPoller: ID 1309: Timing: Started: 2015-08-07 19:47:10.228036, Expiration: 2015-08-07 19:57:10, Override Timeout: None, Elapsed Time: 0:00:25.027209, Left till expiry: 0:09:34.744758, Loop Count: 6
    2015-08-07 19:47:40,259 DEBUG    pytan.handler.QuestionPoller: ID 1309: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-07 19:47:40,259 DEBUG    pytan.handler.QuestionPoller: ID 1309: Timing: Started: 2015-08-07 19:47:10.228036, Expiration: 2015-08-07 19:57:10, Override Timeout: None, Elapsed Time: 0:00:30.031449, Left till expiry: 0:09:29.740517, Loop Count: 7
    2015-08-07 19:47:40,259 INFO     pytan.handler.QuestionPoller: ID 1309: Progress Changed 100% (2 of 2)
    2015-08-07 19:47:40,259 INFO     pytan.handler.QuestionPoller: ID 1309: Reached Threshold of 99% (2 of 2)
    
    print the export_str returned from export_obj():
    Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
    2015-08-07 19:46:50,080 DEBUG    pytan.handler.QuestionPoller: ID 1307: id resolved to 1307
    2015-08-07 19:46:50,080 DEBUG    pytan.handler.QuestionPoller: ID 1307: expiration resolved to 2015-08-07T19:56:50
    2015-08-07 19:46:50,080 DEBUG    pytan.handler.QuestionPoller: ID 1307: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:46:50,080 DEBUG    pytan.handler.QuestionPoller: ID 1307: id resolved to 1307
    2015-08-07 19:46:50,080 DEBUG    pytan.handler.QuestionPoller: ID 1307: Object Info resolved to Question ID: 1307, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:46:50,083 DEBUG    pytan.handler.QuestionPoller: ID 1307: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:46:50,083 DEBUG    pytan.handler.QuestionPoller: ID 1307: Timing: Started: 2015-08-07 19:46:50.080614, Expiration: 2015-08-07 19:56:50, Override Timeout: None, Elapsed Time: 0:00:00.003206, Left till expiry: 0:09:59.916182, Loop Count: 1
    2015-08-07 19:46:50,083 INFO     pytan.handler.QuestionPoller: ID 1307: Progress Changed 0% (0 of 2)
    2015-08-07 19:46:55,088 DEBUG    pytan.handler.QuestionPoller: ID 1307: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:46:55,088 DEBUG    pytan.handler.QuestionPoller: ID 1307: Timing: Started: 2015-08-07 19:46:50.080614, Expiration: 2015-08-07 19:56:50, Override Timeout: None, Elapsed Time: 0:00:05.007874, Left till expiry: 0:09:54.911514, Loop Count: 2
    2015-08-07 19:46:55,088 INFO     pytan.handler.QuestionPoller: ID 1307: Progress Changed 50% (1 of 2)
    2015-08-07 19:47:00,092 DEBUG    pytan.handler.QuestionPoller: ID 1307: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:47:00,092 DEBUG    pytan.handler.QuestionPoller: ID 1307: Timing: Started: 2015-08-07 19:46:50.080614, Expiration: 2015-08-07 19:56:50, Override Timeout: None, Elapsed Time: 0:00:10.012245, Left till expiry: 0:09:49.907144, Loop Count: 3
    2015-08-07 19:47:05,096 DEBUG    pytan.handler.QuestionPoller: ID 1307: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    ..trimmed for brevity..
