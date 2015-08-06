
Ask manual question complex query2
==========================================================================================

This is another complex query that gets the Computer Name and Last Logged in User and Installed Applications that contains Google Search or Google Chrome and limits the rows that are displayed to computers that contain the Installed Applications of Google Search or Google Chrome

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
    kwargs["question_filters"] = [u'Installed Applications, that regex match:.*Google (Search|Chrome).*']
    kwargs["sensors"] = [u'Computer Name',
     u'Last Logged In User',
     u'Installed Applications, that regex match:.*Google (Search|Chrome).*']
    kwargs["question_options"] = [u'ignore_case', u'or']
    kwargs["qtype"] = u'manual'
    
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
    2015-08-06 14:49:44,500 DEBUG    pytan.handler.QuestionPoller: ID 86263: id resolved to 86263
    2015-08-06 14:49:44,500 DEBUG    pytan.handler.QuestionPoller: ID 86263: expiration resolved to 2015-08-06T14:59:44
    2015-08-06 14:49:44,500 DEBUG    pytan.handler.QuestionPoller: ID 86263: query_text resolved to Get Computer Name and Last Logged In User and Installed Applications contains "Google (Search|Chrome)" from all machines where Installed Applications contains "Google (Search|Chrome)"
    2015-08-06 14:49:44,500 DEBUG    pytan.handler.QuestionPoller: ID 86263: id resolved to 86263
    2015-08-06 14:49:44,500 DEBUG    pytan.handler.QuestionPoller: ID 86263: Object Info resolved to Question ID: 86263, Query: Get Computer Name and Last Logged In User and Installed Applications contains "Google (Search|Chrome)" from all machines where Installed Applications contains "Google (Search|Chrome)"
    2015-08-06 14:49:44,505 DEBUG    pytan.handler.QuestionPoller: ID 86263: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:49:44,505 DEBUG    pytan.handler.QuestionPoller: ID 86263: Timing: Started: 2015-08-06 14:49:44.500666, Expiration: 2015-08-06 14:59:44, Override Timeout: None, Elapsed Time: 0:00:00.004599, Left till expiry: 0:09:59.494737, Loop Count: 1
    2015-08-06 14:49:44,505 INFO     pytan.handler.QuestionPoller: ID 86263: Progress Changed 0% (0 of 2)
    2015-08-06 14:49:49,512 DEBUG    pytan.handler.QuestionPoller: ID 86263: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-06 14:49:49,512 DEBUG    pytan.handler.QuestionPoller: ID 86263: Timing: Started: 2015-08-06 14:49:44.500666, Expiration: 2015-08-06 14:59:44, Override Timeout: None, Elapsed Time: 0:00:05.011544, Left till expiry: 0:09:54.487793, Loop Count: 2
    2015-08-06 14:49:49,512 INFO     pytan.handler.QuestionPoller: ID 86263: Progress Changed 50% (1 of 2)
    2015-08-06 14:49:54,519 DEBUG    pytan.handler.QuestionPoller: ID 86263: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-06 14:49:54,519 DEBUG    pytan.handler.QuestionPoller: ID 86263: Timing: Started: 2015-08-06 14:49:44.500666, Expiration: 2015-08-06 14:59:44, Override Timeout: None, Elapsed Time: 0:00:10.018531, Left till expiry: 0:09:49.480805, Loop Count: 3
    2015-08-06 14:49:54,519 INFO     pytan.handler.QuestionPoller: ID 86263: Progress Changed 100% (2 of 2)
    2015-08-06 14:49:54,519 INFO     pytan.handler.QuestionPoller: ID 86263: Reached Threshold of 99% (2 of 2)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'poller_object': <pytan.pollers.QuestionPoller object at 0x1113c2990>,
     'poller_success': True,
     'question_object': <taniumpy.object_types.question.Question object at 0x111365b90>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10fc0ec10>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Computer Name and Last Logged In User and Installed Applications contains "Google (Search|Chrome)" from all machines where Installed Applications contains "Google (Search|Chrome)"
    
    CSV Results of response: 
    Computer Name,Last Logged In User,Name,Silent Uninstall String,Uninstallable,Version
    jtanium1.localdomain,JTANIUM1\Jim Olsen,Google Chrome,"""C:\Program Files (x86)\Google\Chrome\Application\44.0.2403.130\Installer\setup.exe"" --uninstall --multi-install --chrome --system-level",Not Uninstallable,44.0.2403.130
    Casus-Belli.local,N/A on Mac,"Google Search
    Google Search
    Google Chrome","nothing
    nothing
    nothing","Not Uninstallable
    Not Uninstallable
    Not Uninstallable","42.0.2311.90
    41.0.2272.104
    44.0.2403.130"
    
