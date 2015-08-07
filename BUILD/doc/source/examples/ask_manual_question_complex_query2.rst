
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


    Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
    2015-08-07 19:44:31,762 DEBUG    pytan.handler.QuestionPoller: ID 1297: id resolved to 1297
    2015-08-07 19:44:31,763 DEBUG    pytan.handler.QuestionPoller: ID 1297: expiration resolved to 2015-08-07T19:54:31
    2015-08-07 19:44:31,763 DEBUG    pytan.handler.QuestionPoller: ID 1297: query_text resolved to Get Computer Name and Last Logged In User and Installed Applications containing "Google (Search|Chrome)" from all machines with Installed Applications containing "Google (Search|Chrome)"
    2015-08-07 19:44:31,763 DEBUG    pytan.handler.QuestionPoller: ID 1297: id resolved to 1297
    2015-08-07 19:44:31,763 DEBUG    pytan.handler.QuestionPoller: ID 1297: Object Info resolved to Question ID: 1297, Query: Get Computer Name and Last Logged In User and Installed Applications containing "Google (Search|Chrome)" from all machines with Installed Applications containing "Google (Search|Chrome)"
    2015-08-07 19:44:31,766 DEBUG    pytan.handler.QuestionPoller: ID 1297: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:44:31,766 DEBUG    pytan.handler.QuestionPoller: ID 1297: Timing: Started: 2015-08-07 19:44:31.763180, Expiration: 2015-08-07 19:54:31, Override Timeout: None, Elapsed Time: 0:00:00.003000, Left till expiry: 0:09:59.233822, Loop Count: 1
    2015-08-07 19:44:31,766 INFO     pytan.handler.QuestionPoller: ID 1297: Progress Changed 0% (0 of 2)
    2015-08-07 19:44:36,774 DEBUG    pytan.handler.QuestionPoller: ID 1297: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:44:36,774 DEBUG    pytan.handler.QuestionPoller: ID 1297: Timing: Started: 2015-08-07 19:44:31.763180, Expiration: 2015-08-07 19:54:31, Override Timeout: None, Elapsed Time: 0:00:05.011630, Left till expiry: 0:09:54.225197, Loop Count: 2
    2015-08-07 19:44:41,779 DEBUG    pytan.handler.QuestionPoller: ID 1297: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-07 19:44:41,779 DEBUG    pytan.handler.QuestionPoller: ID 1297: Timing: Started: 2015-08-07 19:44:31.763180, Expiration: 2015-08-07 19:54:31, Override Timeout: None, Elapsed Time: 0:00:10.016212, Left till expiry: 0:09:49.220610, Loop Count: 3
    2015-08-07 19:44:41,779 INFO     pytan.handler.QuestionPoller: ID 1297: Progress Changed 50% (1 of 2)
    2015-08-07 19:44:46,783 DEBUG    pytan.handler.QuestionPoller: ID 1297: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-07 19:44:46,783 DEBUG    pytan.handler.QuestionPoller: ID 1297: Timing: Started: 2015-08-07 19:44:31.763180, Expiration: 2015-08-07 19:54:31, Override Timeout: None, Elapsed Time: 0:00:15.020382, Left till expiry: 0:09:44.216440, Loop Count: 4
    2015-08-07 19:44:46,783 INFO     pytan.handler.QuestionPoller: ID 1297: Progress Changed 100% (2 of 2)
    2015-08-07 19:44:46,783 INFO     pytan.handler.QuestionPoller: ID 1297: Reached Threshold of 99% (2 of 2)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'poller_object': <pytan.pollers.QuestionPoller object at 0x10a615950>,
     'poller_success': True,
     'question_object': <taniumpy.object_types.question.Question object at 0x10a5e1bd0>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10a5e1d90>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Computer Name and Last Logged In User and Installed Applications containing "Google (Search|Chrome)" from all machines with Installed Applications containing "Google (Search|Chrome)"
    
    CSV Results of response: 
    Computer Name,Last Logged In User,Name,Silent Uninstall String,Uninstallable,Version
    JTANIUM1.localdomain,Uninitialized - waiting for login,Google Chrome,"""C:\Program Files (x86)\Google\Chrome\Application\44.0.2403.130\Installer\setup.exe"" --uninstall --multi-install --chrome --system-level",Not Uninstallable,44.0.2403.130
    Casus-Belli.local,jolsen,"Google Search
    Google Search
    Google Chrome","nothing
    nothing
    nothing","Not Uninstallable
    Not Uninstallable
    Not Uninstallable","42.0.2311.90
    41.0.2272.104
    44.0.2403.130"
    
