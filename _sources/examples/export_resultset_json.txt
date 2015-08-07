
Export resultset json
==========================================================================================

Export a ResultSet from asking a question as JSON with the default options

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
    export_kwargs["export_format"] = u'json'
    
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
    2015-08-07 19:49:10,709 DEBUG    pytan.handler.QuestionPoller: ID 1311: id resolved to 1311
    2015-08-07 19:49:10,709 DEBUG    pytan.handler.QuestionPoller: ID 1311: expiration resolved to 2015-08-07T19:59:10
    2015-08-07 19:49:10,709 DEBUG    pytan.handler.QuestionPoller: ID 1311: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:49:10,709 DEBUG    pytan.handler.QuestionPoller: ID 1311: id resolved to 1311
    2015-08-07 19:49:10,709 DEBUG    pytan.handler.QuestionPoller: ID 1311: Object Info resolved to Question ID: 1311, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:49:10,713 DEBUG    pytan.handler.QuestionPoller: ID 1311: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:49:10,713 DEBUG    pytan.handler.QuestionPoller: ID 1311: Timing: Started: 2015-08-07 19:49:10.709830, Expiration: 2015-08-07 19:59:10, Override Timeout: None, Elapsed Time: 0:00:00.003431, Left till expiry: 0:09:59.286741, Loop Count: 1
    2015-08-07 19:49:10,713 INFO     pytan.handler.QuestionPoller: ID 1311: Progress Changed 0% (0 of 2)
    2015-08-07 19:49:15,721 DEBUG    pytan.handler.QuestionPoller: ID 1311: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:49:15,721 DEBUG    pytan.handler.QuestionPoller: ID 1311: Timing: Started: 2015-08-07 19:49:10.709830, Expiration: 2015-08-07 19:59:10, Override Timeout: None, Elapsed Time: 0:00:05.012026, Left till expiry: 0:09:54.278146, Loop Count: 2
    2015-08-07 19:49:20,725 DEBUG    pytan.handler.QuestionPoller: ID 1311: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:49:20,726 DEBUG    pytan.handler.QuestionPoller: ID 1311: Timing: Started: 2015-08-07 19:49:10.709830, Expiration: 2015-08-07 19:59:10, Override Timeout: None, Elapsed Time: 0:00:10.016173, Left till expiry: 0:09:49.274000, Loop Count: 3
    2015-08-07 19:49:25,730 DEBUG    pytan.handler.QuestionPoller: ID 1311: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:49:25,730 DEBUG    pytan.handler.QuestionPoller: ID 1311: Timing: Started: 2015-08-07 19:49:10.709830, Expiration: 2015-08-07 19:59:10, Override Timeout: None, Elapsed Time: 0:00:15.021031, Left till expiry: 0:09:44.269141, Loop Count: 4
    2015-08-07 19:49:30,739 DEBUG    pytan.handler.QuestionPoller: ID 1311: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:49:30,739 DEBUG    pytan.handler.QuestionPoller: ID 1311: Timing: Started: 2015-08-07 19:49:10.709830, Expiration: 2015-08-07 19:59:10, Override Timeout: None, Elapsed Time: 0:00:20.029753, Left till expiry: 0:09:39.260420, Loop Count: 5
    2015-08-07 19:49:30,739 INFO     pytan.handler.QuestionPoller: ID 1311: Progress Changed 50% (1 of 2)
    2015-08-07 19:49:35,743 DEBUG    pytan.handler.QuestionPoller: ID 1311: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:49:35,744 DEBUG    pytan.handler.QuestionPoller: ID 1311: Timing: Started: 2015-08-07 19:49:10.709830, Expiration: 2015-08-07 19:59:10, Override Timeout: None, Elapsed Time: 0:00:25.034248, Left till expiry: 0:09:34.255925, Loop Count: 6
    2015-08-07 19:49:40,751 DEBUG    pytan.handler.QuestionPoller: ID 1311: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-07 19:49:40,751 DEBUG    pytan.handler.QuestionPoller: ID 1311: Timing: Started: 2015-08-07 19:49:10.709830, Expiration: 2015-08-07 19:59:10, Override Timeout: None, Elapsed Time: 0:00:30.041329, Left till expiry: 0:09:29.248843, Loop Count: 7
    2015-08-07 19:49:40,751 INFO     pytan.handler.QuestionPoller: ID 1311: Progress Changed 100% (2 of 2)
    2015-08-07 19:49:40,751 INFO     pytan.handler.QuestionPoller: ID 1311: Reached Threshold of 99% (2 of 2)
    
    print the export_str returned from export_obj():
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
    ..trimmed for brevity..
