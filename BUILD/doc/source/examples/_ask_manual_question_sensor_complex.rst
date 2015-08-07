
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


    Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
    2015-08-07 19:44:46,869 DEBUG    pytan.handler.QuestionPoller: ID 1298: id resolved to 1298
    2015-08-07 19:44:46,869 DEBUG    pytan.handler.QuestionPoller: ID 1298: expiration resolved to 2015-08-07T19:54:47
    2015-08-07 19:44:46,869 DEBUG    pytan.handler.QuestionPoller: ID 1298: query_text resolved to Get Computer Name and Folder Name Search with RegEx Match[Program Files, , No, No] containing "Shared" matching case from all machines with Operating System containing "Windows" matching case
    2015-08-07 19:44:46,869 DEBUG    pytan.handler.QuestionPoller: ID 1298: id resolved to 1298
    2015-08-07 19:44:46,869 DEBUG    pytan.handler.QuestionPoller: ID 1298: Object Info resolved to Question ID: 1298, Query: Get Computer Name and Folder Name Search with RegEx Match[Program Files, , No, No] containing "Shared" matching case from all machines with Operating System containing "Windows" matching case
    2015-08-07 19:44:46,872 DEBUG    pytan.handler.QuestionPoller: ID 1298: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:44:46,873 DEBUG    pytan.handler.QuestionPoller: ID 1298: Timing: Started: 2015-08-07 19:44:46.869947, Expiration: 2015-08-07 19:54:47, Override Timeout: None, Elapsed Time: 0:00:00.003070, Left till expiry: 0:10:00.126986, Loop Count: 1
    2015-08-07 19:44:46,873 INFO     pytan.handler.QuestionPoller: ID 1298: Progress Changed 0% (0 of 2)
    2015-08-07 19:44:51,877 DEBUG    pytan.handler.QuestionPoller: ID 1298: Progress: Tested: 1, Passed: 0, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 0
    2015-08-07 19:44:51,877 DEBUG    pytan.handler.QuestionPoller: ID 1298: Timing: Started: 2015-08-07 19:44:46.869947, Expiration: 2015-08-07 19:54:47, Override Timeout: None, Elapsed Time: 0:00:05.007156, Left till expiry: 0:09:55.122900, Loop Count: 2
    2015-08-07 19:44:51,877 INFO     pytan.handler.QuestionPoller: ID 1298: Progress Changed 50% (1 of 2)
    2015-08-07 19:44:56,881 DEBUG    pytan.handler.QuestionPoller: ID 1298: Progress: Tested: 1, Passed: 0, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 0
    2015-08-07 19:44:56,881 DEBUG    pytan.handler.QuestionPoller: ID 1298: Timing: Started: 2015-08-07 19:44:46.869947, Expiration: 2015-08-07 19:54:47, Override Timeout: None, Elapsed Time: 0:00:10.011533, Left till expiry: 0:09:50.118523, Loop Count: 3
    2015-08-07 19:45:01,885 DEBUG    pytan.handler.QuestionPoller: ID 1298: Progress: Tested: 1, Passed: 0, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 0
    2015-08-07 19:45:01,885 DEBUG    pytan.handler.QuestionPoller: ID 1298: Timing: Started: 2015-08-07 19:44:46.869947, Expiration: 2015-08-07 19:54:47, Override Timeout: None, Elapsed Time: 0:00:15.016034, Left till expiry: 0:09:45.114022, Loop Count: 4
    2015-08-07 19:45:06,890 DEBUG    pytan.handler.QuestionPoller: ID 1298: Progress: Tested: 2, Passed: 1, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 1
    2015-08-07 19:45:06,890 DEBUG    pytan.handler.QuestionPoller: ID 1298: Timing: Started: 2015-08-07 19:44:46.869947, Expiration: 2015-08-07 19:54:47, Override Timeout: None, Elapsed Time: 0:00:20.020654, Left till expiry: 0:09:40.109402, Loop Count: 5
    2015-08-07 19:45:06,890 INFO     pytan.handler.QuestionPoller: ID 1298: Progress Changed 100% (2 of 2)
    2015-08-07 19:45:06,890 INFO     pytan.handler.QuestionPoller: ID 1298: Reached Threshold of 99% (2 of 2)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'poller_object': <pytan.pollers.QuestionPoller object at 0x10a5c9c90>,
     'poller_success': True,
     'question_object': <taniumpy.object_types.question.Question object at 0x10a5b98d0>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10a5e1410>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Computer Name and Folder Name Search with RegEx Match[Program Files, , No, No] containing "Shared" matching case from all machines with Operating System containing "Windows" matching case
    
    CSV Results of response: 
    Computer Name,"Folder Name Search with RegEx Match[Program Files, , No, No]"
    JTANIUM1.localdomain,"C:\Program Files\Common Files\Microsoft Shared\VS7Debug
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
