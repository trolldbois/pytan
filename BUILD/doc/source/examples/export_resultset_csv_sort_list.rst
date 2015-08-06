
Export resultset csv sort list
==========================================================================================

Export a ResultSet from asking a question as CSV with Computer Name and IP Address for the header_sort

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
    export_kwargs["header_sort"] = [u'Computer Name', u'IP Address']
    
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
    2015-08-06 15:08:30,980 DEBUG    pytan.handler.QuestionPoller: ID 86286: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 15:08:30,980 DEBUG    pytan.handler.QuestionPoller: ID 86286: Timing: Started: 2015-08-06 15:08:10.929576, Expiration: 2015-08-06 15:18:11, Override Timeout: None, Elapsed Time: 0:00:20.050528, Left till expiry: 0:09:40.019899, Loop Count: 5
    2015-08-06 15:08:35,995 DEBUG    pytan.handler.QuestionPoller: ID 86286: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-06 15:08:35,995 DEBUG    pytan.handler.QuestionPoller: ID 86286: Timing: Started: 2015-08-06 15:08:10.929576, Expiration: 2015-08-06 15:18:11, Override Timeout: None, Elapsed Time: 0:00:25.065986, Left till expiry: 0:09:35.004441, Loop Count: 6
    2015-08-06 15:08:35,995 INFO     pytan.handler.QuestionPoller: ID 86286: Progress Changed 100% (2 of 2)
    2015-08-06 15:08:35,995 INFO     pytan.handler.QuestionPoller: ID 86286: Reached Threshold of 99% (2 of 2)
    
    print the export_str returned from export_obj():
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
    ..trimmed for brevity..
