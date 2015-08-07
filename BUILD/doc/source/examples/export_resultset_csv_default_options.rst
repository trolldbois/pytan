
Export resultset csv default options
==========================================================================================

Export a ResultSet from asking a question as CSV with the default options

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
    2015-08-07 19:46:14,930 DEBUG    pytan.handler.QuestionPoller: ID 1306: id resolved to 1306
    2015-08-07 19:46:14,930 DEBUG    pytan.handler.QuestionPoller: ID 1306: expiration resolved to 2015-08-07T19:56:15
    2015-08-07 19:46:14,930 DEBUG    pytan.handler.QuestionPoller: ID 1306: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:46:14,930 DEBUG    pytan.handler.QuestionPoller: ID 1306: id resolved to 1306
    2015-08-07 19:46:14,930 DEBUG    pytan.handler.QuestionPoller: ID 1306: Object Info resolved to Question ID: 1306, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[Program Files, , No, No, .*Shared.*] from all machines
    2015-08-07 19:46:14,933 DEBUG    pytan.handler.QuestionPoller: ID 1306: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:46:14,933 DEBUG    pytan.handler.QuestionPoller: ID 1306: Timing: Started: 2015-08-07 19:46:14.930494, Expiration: 2015-08-07 19:56:15, Override Timeout: None, Elapsed Time: 0:00:00.003296, Left till expiry: 0:10:00.066212, Loop Count: 1
    2015-08-07 19:46:14,933 INFO     pytan.handler.QuestionPoller: ID 1306: Progress Changed 0% (0 of 2)
    2015-08-07 19:46:19,940 DEBUG    pytan.handler.QuestionPoller: ID 1306: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:46:19,940 DEBUG    pytan.handler.QuestionPoller: ID 1306: Timing: Started: 2015-08-07 19:46:14.930494, Expiration: 2015-08-07 19:56:15, Override Timeout: None, Elapsed Time: 0:00:05.010114, Left till expiry: 0:09:55.059394, Loop Count: 2
    2015-08-07 19:46:24,944 DEBUG    pytan.handler.QuestionPoller: ID 1306: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:46:24,944 DEBUG    pytan.handler.QuestionPoller: ID 1306: Timing: Started: 2015-08-07 19:46:14.930494, Expiration: 2015-08-07 19:56:15, Override Timeout: None, Elapsed Time: 0:00:10.014077, Left till expiry: 0:09:50.055431, Loop Count: 3
    2015-08-07 19:46:29,951 DEBUG    pytan.handler.QuestionPoller: ID 1306: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:46:29,951 DEBUG    pytan.handler.QuestionPoller: ID 1306: Timing: Started: 2015-08-07 19:46:14.930494, Expiration: 2015-08-07 19:56:15, Override Timeout: None, Elapsed Time: 0:00:15.020891, Left till expiry: 0:09:45.048618, Loop Count: 4
    2015-08-07 19:46:34,955 DEBUG    pytan.handler.QuestionPoller: ID 1306: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:46:34,955 DEBUG    pytan.handler.QuestionPoller: ID 1306: Timing: Started: 2015-08-07 19:46:14.930494, Expiration: 2015-08-07 19:56:15, Override Timeout: None, Elapsed Time: 0:00:20.024786, Left till expiry: 0:09:40.044723, Loop Count: 5
    2015-08-07 19:46:39,959 DEBUG    pytan.handler.QuestionPoller: ID 1306: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:46:39,959 DEBUG    pytan.handler.QuestionPoller: ID 1306: Timing: Started: 2015-08-07 19:46:14.930494, Expiration: 2015-08-07 19:56:15, Override Timeout: None, Elapsed Time: 0:00:25.029330, Left till expiry: 0:09:35.040179, Loop Count: 6
    2015-08-07 19:46:39,959 INFO     pytan.handler.QuestionPoller: ID 1306: Progress Changed 50% (1 of 2)
    2015-08-07 19:46:44,964 DEBUG    pytan.handler.QuestionPoller: ID 1306: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:46:44,965 DEBUG    pytan.handler.QuestionPoller: ID 1306: Timing: Started: 2015-08-07 19:46:14.930494, Expiration: 2015-08-07 19:56:15, Override Timeout: None, Elapsed Time: 0:00:30.034524, Left till expiry: 0:09:30.034985, Loop Count: 7
    2015-08-07 19:46:49,971 DEBUG    pytan.handler.QuestionPoller: ID 1306: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-07 19:46:49,971 DEBUG    pytan.handler.QuestionPoller: ID 1306: Timing: Started: 2015-08-07 19:46:14.930494, Expiration: 2015-08-07 19:56:15, Override Timeout: None, Elapsed Time: 0:00:35.041015, Left till expiry: 0:09:25.028494, Loop Count: 8
    2015-08-07 19:46:49,971 INFO     pytan.handler.QuestionPoller: ID 1306: Progress Changed 100% (2 of 2)
    2015-08-07 19:46:49,971 INFO     pytan.handler.QuestionPoller: ID 1306: Reached Threshold of 99% (2 of 2)
    
    print the export_str returned from export_obj():
    Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
    2015-08-07 19:46:14,843 INFO     pytan.handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/SystemSettingList_2015_08_07-15_46_14-EDT.json' written with 327 bytes
    Traceback (most recent call last):
      File "<string>", line 67, in <module>
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 546, in create_from_json
        raise pytan.exceptions.HandlerError(m(objtype, json_createable))
    HandlerError: setting is not a json createable object! Supported objects: user, whitelisted_url, saved_question, group, package, question, action, sensor
    
