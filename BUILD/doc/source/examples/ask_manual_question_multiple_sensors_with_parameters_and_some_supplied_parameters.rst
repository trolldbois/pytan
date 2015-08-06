
Ask manual question multiple sensors with parameters and some supplied parameters
==========================================================================================

Ask a manual question using human strings by referencing the name of multiple sensors, one that takes parameters, but supplying only two of the four parameters that are used by the sensor (and letting pytan automatically determine the appropriate default value for those parameters which require a value and none was supplied), and one that does not take parameters.

No sensor filters, question filters, or question options supplied.

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
    kwargs["sensors"] = [u'Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*}',
     u'Computer Name']
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
    2015-08-06 14:45:50,933 DEBUG    pytan.handler.QuestionPoller: ID 86250: id resolved to 86250
    2015-08-06 14:45:50,933 DEBUG    pytan.handler.QuestionPoller: ID 86250: expiration resolved to 2015-08-06T14:55:51
    2015-08-06 14:45:50,933 DEBUG    pytan.handler.QuestionPoller: ID 86250: query_text resolved to Get Computer Name from all machines
    2015-08-06 14:45:50,933 DEBUG    pytan.handler.QuestionPoller: ID 86250: id resolved to 86250
    2015-08-06 14:45:50,933 DEBUG    pytan.handler.QuestionPoller: ID 86250: Object Info resolved to Question ID: 86250, Query: Get Computer Name from all machines
    2015-08-06 14:45:50,939 DEBUG    pytan.handler.QuestionPoller: ID 86250: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:45:50,939 DEBUG    pytan.handler.QuestionPoller: ID 86250: Timing: Started: 2015-08-06 14:45:50.933511, Expiration: 2015-08-06 14:55:51, Override Timeout: None, Elapsed Time: 0:00:00.005569, Left till expiry: 0:10:00.060923, Loop Count: 1
    2015-08-06 14:45:50,939 INFO     pytan.handler.QuestionPoller: ID 86250: Progress Changed 0% (0 of 2)
    2015-08-06 14:45:55,946 DEBUG    pytan.handler.QuestionPoller: ID 86250: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:45:55,946 DEBUG    pytan.handler.QuestionPoller: ID 86250: Timing: Started: 2015-08-06 14:45:50.933511, Expiration: 2015-08-06 14:55:51, Override Timeout: None, Elapsed Time: 0:00:05.012697, Left till expiry: 0:09:55.053795, Loop Count: 2
    2015-08-06 14:46:00,953 DEBUG    pytan.handler.QuestionPoller: ID 86250: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:46:00,953 DEBUG    pytan.handler.QuestionPoller: ID 86250: Timing: Started: 2015-08-06 14:45:50.933511, Expiration: 2015-08-06 14:55:51, Override Timeout: None, Elapsed Time: 0:00:10.019844, Left till expiry: 0:09:50.046648, Loop Count: 3
    2015-08-06 14:46:05,960 DEBUG    pytan.handler.QuestionPoller: ID 86250: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-06 14:46:05,960 DEBUG    pytan.handler.QuestionPoller: ID 86250: Timing: Started: 2015-08-06 14:45:50.933511, Expiration: 2015-08-06 14:55:51, Override Timeout: None, Elapsed Time: 0:00:15.027094, Left till expiry: 0:09:45.039399, Loop Count: 4
    2015-08-06 14:46:05,960 INFO     pytan.handler.QuestionPoller: ID 86250: Progress Changed 50% (1 of 2)
    2015-08-06 14:46:10,965 DEBUG    pytan.handler.QuestionPoller: ID 86250: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-06 14:46:10,965 DEBUG    pytan.handler.QuestionPoller: ID 86250: Timing: Started: 2015-08-06 14:45:50.933511, Expiration: 2015-08-06 14:55:51, Override Timeout: None, Elapsed Time: 0:00:20.032433, Left till expiry: 0:09:40.034058, Loop Count: 5
    2015-08-06 14:46:15,973 DEBUG    pytan.handler.QuestionPoller: ID 86250: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 1
    2015-08-06 14:46:15,973 DEBUG    pytan.handler.QuestionPoller: ID 86250: Timing: Started: 2015-08-06 14:45:50.933511, Expiration: 2015-08-06 14:55:51, Override Timeout: None, Elapsed Time: 0:00:25.040206, Left till expiry: 0:09:35.026285, Loop Count: 6
    2015-08-06 14:46:20,984 DEBUG    pytan.handler.QuestionPoller: ID 86250: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 2
    2015-08-06 14:46:20,984 DEBUG    pytan.handler.QuestionPoller: ID 86250: Timing: Started: 2015-08-06 14:45:50.933511, Expiration: 2015-08-06 14:55:51, Override Timeout: None, Elapsed Time: 0:00:30.051252, Left till expiry: 0:09:30.015239, Loop Count: 7
    2015-08-06 14:46:20,984 INFO     pytan.handler.QuestionPoller: ID 86250: Progress Changed 100% (2 of 2)
    2015-08-06 14:46:20,984 INFO     pytan.handler.QuestionPoller: ID 86250: Reached Threshold of 99% (2 of 2)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'poller_object': <pytan.pollers.QuestionPoller object at 0x10fc74c90>,
     'poller_success': True,
     'question_object': <taniumpy.object_types.question.Question object at 0x10fbf8e10>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10fc65950>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Computer Name from all machines
    
    CSV Results of response: 
    Computer Name,"Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*]"
    Casus-Belli.local,Windows Only
    jtanium1.localdomain,"C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2674319\ServicePack\1033_enu_lp\x64\setup\sqlsupport_msi\windows\winsxs\5z1v718o.6n8
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2958429\ServicePack\1033_enu_lp\x64\setup\sqlsupport_msi\windows\winsxs\92rg91xw.1p4
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2958429\ServicePack\1033_enu_lp\x64\setup\sqlsupport_msi\windows\winsxs\policies\u1sw1o0k.9hi
    C:\Program Files\VMware\VMware Tools\plugins\vmsvc
    C:\Program Files\Common Files\Microsoft Shared\VS7Debug
    C:\Program Files\Tanium\Tanium Server\Apache24\manual\style
    C:\Program Files\Tanium\Tanium Server\ApacheBackup2015-05-15-15-44-27\manual\images
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2674319\ServicePack\1033_enu_lp\x64\setup\sqlsupport_msi\windows\winsxs\vlv6b2rp.6fi
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Log\20150306_224415\resources
    C:\Program Files\Tanium\Tanium Server\Apache24\htdocs\console\history
    C:\Program Files\Windows Portable Devices
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2977326\GDR\1033_enu_lp\x64\setup\sqlsupport_msi\pfiles\sqlservr\110\keyfile
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2674319\ServicePack\1033_enu_lp\x64\setup\sql_engine_core_inst_loc_msi
    ..trimmed for brevity..
