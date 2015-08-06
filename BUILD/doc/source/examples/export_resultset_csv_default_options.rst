
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
    2015-08-06 14:56:11,294 DEBUG    pytan.handler.QuestionPoller: ID 86273: id resolved to 86273
    2015-08-06 14:56:11,294 DEBUG    pytan.handler.QuestionPoller: ID 86273: expiration resolved to 2015-08-06T15:06:11
    2015-08-06 14:56:11,294 DEBUG    pytan.handler.QuestionPoller: ID 86273: query_text resolved to Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 14:56:11,294 DEBUG    pytan.handler.QuestionPoller: ID 86273: id resolved to 86273
    2015-08-06 14:56:11,294 DEBUG    pytan.handler.QuestionPoller: ID 86273: Object Info resolved to Question ID: 86273, Query: Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, , .*Shared.*] from all machines
    2015-08-06 14:56:11,299 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:56:11,300 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:00:00.005629, Left till expiry: 0:09:59.699962, Loop Count: 1
    2015-08-06 14:56:11,300 INFO     pytan.handler.QuestionPoller: ID 86273: Progress Changed 0% (0 of 2)
    2015-08-06 14:56:16,308 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:56:16,308 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:00:05.013748, Left till expiry: 0:09:54.691843, Loop Count: 2
    2015-08-06 14:56:21,315 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:56:21,315 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:00:10.021539, Left till expiry: 0:09:49.684051, Loop Count: 3
    2015-08-06 14:56:26,321 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:56:26,321 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:00:15.026771, Left till expiry: 0:09:44.678819, Loop Count: 4
    2015-08-06 14:56:31,327 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:56:31,327 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:00:20.032858, Left till expiry: 0:09:39.672732, Loop Count: 5
    2015-08-06 14:56:36,334 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:56:36,335 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:00:25.040605, Left till expiry: 0:09:34.664985, Loop Count: 6
    2015-08-06 14:56:41,341 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:56:41,341 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:00:30.046840, Left till expiry: 0:09:29.658750, Loop Count: 7
    2015-08-06 14:56:46,351 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:56:46,351 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:00:35.057010, Left till expiry: 0:09:24.648581, Loop Count: 8
    2015-08-06 14:56:51,358 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:56:51,358 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:00:40.064082, Left till expiry: 0:09:19.641508, Loop Count: 9
    2015-08-06 14:56:56,367 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:56:56,367 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:00:45.073149, Left till expiry: 0:09:14.632441, Loop Count: 10
    2015-08-06 14:57:01,374 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:57:01,374 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:00:50.080471, Left till expiry: 0:09:09.625120, Loop Count: 11
    2015-08-06 14:57:06,386 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:57:06,386 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:00:55.092054, Left till expiry: 0:09:04.613537, Loop Count: 12
    2015-08-06 14:57:11,393 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:57:11,393 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:01:00.099565, Left till expiry: 0:08:59.606025, Loop Count: 13
    2015-08-06 14:57:16,402 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:57:16,402 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:01:05.107672, Left till expiry: 0:08:54.597918, Loop Count: 14
    2015-08-06 14:57:21,409 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:57:21,409 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:01:10.114791, Left till expiry: 0:08:49.590799, Loop Count: 15
    2015-08-06 14:57:26,420 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:57:26,420 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:01:15.126060, Left till expiry: 0:08:44.579530, Loop Count: 16
    2015-08-06 14:57:31,427 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:57:31,427 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:01:20.132993, Left till expiry: 0:08:39.572597, Loop Count: 17
    2015-08-06 14:57:36,435 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:57:36,435 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:01:25.141375, Left till expiry: 0:08:34.564215, Loop Count: 18
    2015-08-06 14:57:41,442 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:57:41,442 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:01:30.148201, Left till expiry: 0:08:29.557389, Loop Count: 19
    2015-08-06 14:57:46,449 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:57:46,449 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:01:35.155353, Left till expiry: 0:08:24.550237, Loop Count: 20
    2015-08-06 14:57:51,457 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:57:51,457 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:01:40.163433, Left till expiry: 0:08:19.542157, Loop Count: 21
    2015-08-06 14:57:56,467 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:57:56,467 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:01:45.172988, Left till expiry: 0:08:14.532602, Loop Count: 22
    2015-08-06 14:58:01,472 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:58:01,473 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:01:50.178619, Left till expiry: 0:08:09.526972, Loop Count: 23
    2015-08-06 14:58:06,484 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-06 14:58:06,484 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:01:55.190062, Left till expiry: 0:08:04.515529, Loop Count: 24
    2015-08-06 14:58:06,484 INFO     pytan.handler.QuestionPoller: ID 86273: Progress Changed 50% (1 of 2)
    2015-08-06 14:58:11,492 DEBUG    pytan.handler.QuestionPoller: ID 86273: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-06 14:58:11,492 DEBUG    pytan.handler.QuestionPoller: ID 86273: Timing: Started: 2015-08-06 14:56:11.294412, Expiration: 2015-08-06 15:06:11, Override Timeout: None, Elapsed Time: 0:02:00.198313, Left till expiry: 0:07:59.507278, Loop Count: 25
    2015-08-06 14:58:11,492 INFO     pytan.handler.QuestionPoller: ID 86273: Progress Changed 100% (2 of 2)
    2015-08-06 14:58:11,492 INFO     pytan.handler.QuestionPoller: ID 86273: Reached Threshold of 99% (2 of 2)
    
    print the export_str returned from export_obj():
    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
    2015-08-06 14:56:11,180 INFO     pytan.handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/SystemSettingList_2015_08_06-10_56_11-EDT.json' written with 327 bytes
    Traceback (most recent call last):
      File "<string>", line 67, in <module>
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 547, in create_from_json
        raise pytan.exceptions.HandlerError(m(objtype, json_createable))
    HandlerError: setting is not a json createable object! Supported objects: user, whitelisted_url, saved_question, group, package, question, action, sensor
    
