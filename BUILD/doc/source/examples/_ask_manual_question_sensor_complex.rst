
 ask manual question sensor complex
==========================================================================================

This provides an example for asking a manual question without using human strings.

It uses the Computer Name and Folder Name Search with RegEx Match sensors.

The second sensor has a single parameter, dirname, with a value of 'Program Files'.

The second sensor also has 3 sensor filter options that set the max data age to 3600 seconds, does NOT ignore case, and treats all values as string.

There is also a question filter supplied that limits the rows that are displayed to computers that match an Operating System that contains Windows, and has 3 question filter options supplied that set the max data age to 3600 seconds, does NOT ignore case, and uses 'and' to join all question filters.

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
    
    # setup the arguments for the handler method
    kwargs = {}
    kwargs["question_filter_defs"] = [{u'filter': {u'not_flag': 0,
                  u'operator': u'RegexMatch',
                  u'value': u'.*Windows.*'},
      u'name': u'Operating System'}]
    kwargs["sensor_defs"] = [u'Computer Name',
     {u'filter': {u'not_flag': 0,
                  u'operator': u'RegexMatch',
                  u'value': u'.*Shared.*'},
      u'name': u'Folder Name Search with RegEx Match',
      u'options': {u'ignore_case_flag': 0,
                   u'max_age_seconds': 3600,
                   u'value_type': u'string'},
      u'params': {u'dirname': u'Program Files'}}]
    kwargs["question_option_defs"] = {u'and_flag': 0, u'ignore_case_flag': 0, u'max_age_seconds': 3600}
    kwargs["qtype"] = u'_manual'
    
    # call the handler with the ask method, passing in kwargs for arguments
    response = handler.ask(**kwargs)
    import pprint, io
    
    print ""
    print "Type of response: ", type(response)
    
    print ""
    print "Pretty print of response:"
    print pprint.pformat(response)
    
    print ""
    print "Equivalent Question if it were to be asked in the Tanium Console: "
    print response['question_object'].query_text
    
    # create an IO stream to store CSV results to
    out = io.BytesIO()
    
    # call the write_csv() method to convert response to CSV and store it in out
    response['question_results'].write_csv(out, response['question_results'])
    
    print ""
    print "CSV Results of response: "
    out = out.getvalue()
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
    2015-08-06 14:49:55,598 DEBUG    pytan.handler.QuestionPoller: ID 86264: id resolved to 86264
    2015-08-06 14:49:55,598 DEBUG    pytan.handler.QuestionPoller: ID 86264: expiration resolved to 2015-08-06T14:59:55
    2015-08-06 14:49:55,598 DEBUG    pytan.handler.QuestionPoller: ID 86264: query_text resolved to Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" matching case from all machines where Operating System contains "Windows" matching case
    2015-08-06 14:49:55,598 DEBUG    pytan.handler.QuestionPoller: ID 86264: id resolved to 86264
    2015-08-06 14:49:55,598 DEBUG    pytan.handler.QuestionPoller: ID 86264: Object Info resolved to Question ID: 86264, Query: Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" matching case from all machines where Operating System contains "Windows" matching case
    2015-08-06 14:49:55,603 DEBUG    pytan.handler.QuestionPoller: ID 86264: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:49:55,603 DEBUG    pytan.handler.QuestionPoller: ID 86264: Timing: Started: 2015-08-06 14:49:55.598943, Expiration: 2015-08-06 14:59:55, Override Timeout: None, Elapsed Time: 0:00:00.004205, Left till expiry: 0:09:59.396854, Loop Count: 1
    2015-08-06 14:49:55,603 INFO     pytan.handler.QuestionPoller: ID 86264: Progress Changed 0% (0 of 2)
    2015-08-06 14:50:00,613 DEBUG    pytan.handler.QuestionPoller: ID 86264: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:50:00,613 DEBUG    pytan.handler.QuestionPoller: ID 86264: Timing: Started: 2015-08-06 14:49:55.598943, Expiration: 2015-08-06 14:59:55, Override Timeout: None, Elapsed Time: 0:00:05.014380, Left till expiry: 0:09:54.386679, Loop Count: 2
    2015-08-06 14:50:05,623 DEBUG    pytan.handler.QuestionPoller: ID 86264: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-06 14:50:05,623 DEBUG    pytan.handler.QuestionPoller: ID 86264: Timing: Started: 2015-08-06 14:49:55.598943, Expiration: 2015-08-06 14:59:55, Override Timeout: None, Elapsed Time: 0:00:10.024572, Left till expiry: 0:09:49.376488, Loop Count: 3
    2015-08-06 14:50:05,623 INFO     pytan.handler.QuestionPoller: ID 86264: Progress Changed 50% (1 of 2)
    2015-08-06 14:50:10,633 DEBUG    pytan.handler.QuestionPoller: ID 86264: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-06 14:50:10,633 DEBUG    pytan.handler.QuestionPoller: ID 86264: Timing: Started: 2015-08-06 14:49:55.598943, Expiration: 2015-08-06 14:59:55, Override Timeout: None, Elapsed Time: 0:00:15.034673, Left till expiry: 0:09:44.366386, Loop Count: 4
    2015-08-06 14:50:15,638 DEBUG    pytan.handler.QuestionPoller: ID 86264: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-06 14:50:15,638 DEBUG    pytan.handler.QuestionPoller: ID 86264: Timing: Started: 2015-08-06 14:49:55.598943, Expiration: 2015-08-06 14:59:55, Override Timeout: None, Elapsed Time: 0:00:20.039982, Left till expiry: 0:09:39.361077, Loop Count: 5
    2015-08-06 14:50:20,648 DEBUG    pytan.handler.QuestionPoller: ID 86264: Progress: Tested: 2, Passed: 1, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 1
    2015-08-06 14:50:20,648 DEBUG    pytan.handler.QuestionPoller: ID 86264: Timing: Started: 2015-08-06 14:49:55.598943, Expiration: 2015-08-06 14:59:55, Override Timeout: None, Elapsed Time: 0:00:25.049158, Left till expiry: 0:09:34.351902, Loop Count: 6
    2015-08-06 14:50:20,648 INFO     pytan.handler.QuestionPoller: ID 86264: Progress Changed 100% (2 of 2)
    2015-08-06 14:50:20,648 INFO     pytan.handler.QuestionPoller: ID 86264: Reached Threshold of 99% (2 of 2)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'poller_object': <pytan.pollers.QuestionPoller object at 0x111365850>,
     'poller_success': True,
     'question_object': <taniumpy.object_types.question.Question object at 0x111365c10>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10fc0e5d0>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" matching case from all machines where Operating System contains "Windows" matching case
    
    CSV Results of response: 
    Computer Name,"Folder Name Search with RegEx Match[No, Program Files, No, ]"
    jtanium1.localdomain,"C:\Program Files\Common Files\Microsoft Shared\VS7Debug
    C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
    C:\Program Files\Common Files\Microsoft Shared\ink\ru-RU
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\keypad
    C:\Program Files\Common Files\Microsoft Shared\ink
    C:\Program Files\Common Files\Microsoft Shared\ink\sv-SE
    C:\Program Files\Common Files\Microsoft Shared\ink\uk-UA
    C:\Program Files\Common Files\Microsoft Shared\ink\sl-SI
    C:\Program Files\Common Files\Microsoft Shared\ink\hu-HU
    C:\Program Files\Common Files\Microsoft Shared\ink\zh-TW
    C:\Program Files\Common Files\Microsoft Shared\ink\zh-CN
    C:\Program Files\Common Files\Microsoft Shared\ink\fi-FI
    C:\Program Files\Common Files\Microsoft Shared
    C:\Program Files\Common Files\Microsoft Shared\ink\da-DK
    ..trimmed for brevity..
