
Deploy action simple
==========================================================================================

Deploy an action against all computers using human strings.

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
    kwargs["run"] = True
    kwargs["package"] = u'Distribute Tanium Standard Utilities'
    
    # call the handler with the deploy_action method, passing in kwargs for arguments
    response = handler.deploy_action(**kwargs)
    import pprint, io
    
    print ""
    print "Type of response: ", type(response)
    
    print ""
    print "Pretty print of response:"
    print pprint.pformat(response)
    
    print ""
    print "Print of action object: "
    print response['action_object']
    
    # create an IO stream to store CSV results to
    out = io.BytesIO()
    
    # if results were returned (i.e. get_results=True was one of the kwargs passed in):
    if response['action_results']:
        # call the write_csv() method to convert response to CSV and store it in out
        response['action_results'].write_csv(out, response['action_results'])
    
        print ""
        print "CSV Results of response: "
        print out.getvalue()
    
    


Output from Python Code
----------------------------------------------------------------------------------------

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
    2015-08-07 19:45:08,345 DEBUG    pytan.handler.ActionPoller: ID 56: id resolved to 56
    2015-08-07 19:45:08,345 DEBUG    pytan.handler.ActionPoller: ID 56: package_spec resolved to PackageSpec, name: 'Distribute Tanium Standard Utilities', id: 20
    2015-08-07 19:45:08,353 DEBUG    pytan.handler.ActionPoller: ID 56: target_group resolved to Group, name: 'Default'
    2015-08-07 19:45:08,353 DEBUG    pytan.handler.ActionPoller: ID 56: Result Map resolved to {'failed': {'total': 0, '56:Failed.': [], '56:NotSucceeded.': [], '56:Expired.': [], '56:Stopped.': []}, 'finished': {'56:NotSucceeded.': [], '56:Failed.': [], '56:Succeeded.': [], '56:Expired.': [], '56:Stopped.': [], '56:Verified.': [], 'total': 0, '56:Completed.': []}, 'running': {'56:Running.': [], '56:Downloading.': [], '56:Copying.': [], '56:Waiting.': [], 'total': 0, '56:PendingVerification.': []}, 'success': {'total': 0, '56:Verified.': [], '56:Completed.': []}, 'unknown': {'total': 0}}
    2015-08-07 19:45:08,353 DEBUG    pytan.handler.ActionPoller: ID 56: expiration_time resolved to 2015-08-07T20:40:10
    2015-08-07 19:45:08,353 DEBUG    pytan.handler.ActionPoller: ID 56: status resolved to Open
    2015-08-07 19:45:08,353 DEBUG    pytan.handler.ActionPoller: ID 56: stopped_flag resolved to 0
    2015-08-07 19:45:08,353 DEBUG    pytan.handler.ActionPoller: ID 56: Object Info resolved to ID 56: Package: 'Distribute Tanium Standard Utilities', Target: 'None', Verify: False, Stopped: False, Status: Open
    2015-08-07 19:45:08,353 DEBUG    pytan.handler.ActionPoller: ID 56: Adding Question to derive passed count
    2015-08-07 19:45:08,365 DEBUG    pytan.handler.QuestionPoller: ID 1299: id resolved to 1299
    2015-08-07 19:45:08,365 DEBUG    pytan.handler.QuestionPoller: ID 1299: expiration resolved to 2015-08-07T19:55:08
    2015-08-07 19:45:08,365 DEBUG    pytan.handler.QuestionPoller: ID 1299: query_text resolved to Get number of machines
    2015-08-07 19:45:08,365 DEBUG    pytan.handler.QuestionPoller: ID 1299: id resolved to 1299
    2015-08-07 19:45:08,365 DEBUG    pytan.handler.QuestionPoller: ID 1299: Object Info resolved to Question ID: 1299, Query: Get number of machines
    2015-08-07 19:45:08,368 DEBUG    pytan.handler.QuestionPoller: ID 1299: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:45:08,368 DEBUG    pytan.handler.QuestionPoller: ID 1299: Timing: Started: 2015-08-07 19:45:08.365942, Expiration: 2015-08-07 19:55:08, Override Timeout: None, Elapsed Time: 0:00:00.002560, Left till expiry: 0:09:59.631500, Loop Count: 1
    2015-08-07 19:45:08,368 INFO     pytan.handler.QuestionPoller: ID 1299: Progress Changed 0% (0 of 2)
    2015-08-07 19:45:13,372 DEBUG    pytan.handler.QuestionPoller: ID 1299: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 0
    2015-08-07 19:45:13,372 DEBUG    pytan.handler.QuestionPoller: ID 1299: Timing: Started: 2015-08-07 19:45:08.365942, Expiration: 2015-08-07 19:55:08, Override Timeout: None, Elapsed Time: 0:00:05.006752, Left till expiry: 0:09:54.627310, Loop Count: 2
    2015-08-07 19:45:13,372 INFO     pytan.handler.QuestionPoller: ID 1299: Progress Changed 50% (1 of 2)
    2015-08-07 19:45:18,379 DEBUG    pytan.handler.QuestionPoller: ID 1299: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 0
    2015-08-07 19:45:18,379 DEBUG    pytan.handler.QuestionPoller: ID 1299: Timing: Started: 2015-08-07 19:45:08.365942, Expiration: 2015-08-07 19:55:08, Override Timeout: None, Elapsed Time: 0:00:10.013996, Left till expiry: 0:09:49.620065, Loop Count: 3
    2015-08-07 19:45:18,380 INFO     pytan.handler.QuestionPoller: ID 1299: Progress Changed 100% (2 of 2)
    2015-08-07 19:45:18,380 INFO     pytan.handler.QuestionPoller: ID 1299: Reached Threshold of 99% (2 of 2)
    2015-08-07 19:45:18,380 DEBUG    pytan.handler.ActionPoller: ID 56: Passed Count resolved to 2
    2015-08-07 19:45:18,390 DEBUG    pytan.handler.ActionPoller: ID 56: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-07 19:45:18,390 DEBUG    pytan.handler.ActionPoller: ID 56: Timing: Started: 2015-08-07 19:45:08.353365, Expiration: 2015-08-07 20:40:10, Override Timeout: None, Elapsed Time: 0:00:10.037247, Left till expiry: 0:54:51.609390, Loop Count: 1
    2015-08-07 19:45:18,390 INFO     pytan.handler.ActionPoller: ID 56: Progress Changed for Seen Count 0% (0 of 2)
    2015-08-07 19:45:18,397 DEBUG    pytan.handler.ActionPoller: ID 56: stopped_flag resolved to 0
    2015-08-07 19:45:18,397 DEBUG    pytan.handler.ActionPoller: ID 56: status resolved to Open
    2015-08-07 19:45:23,411 DEBUG    pytan.handler.ActionPoller: ID 56: Progress: Seen Action: 1, Expected Seen: 2, Percent: 50%
    2015-08-07 19:45:23,411 DEBUG    pytan.handler.ActionPoller: ID 56: Timing: Started: 2015-08-07 19:45:08.353365, Expiration: 2015-08-07 20:40:10, Override Timeout: None, Elapsed Time: 0:00:15.058175, Left till expiry: 0:54:46.588462, Loop Count: 2
    2015-08-07 19:45:23,411 INFO     pytan.handler.ActionPoller: ID 56: Progress Changed for Seen Count 50% (1 of 2)
    2015-08-07 19:45:23,417 DEBUG    pytan.handler.ActionPoller: ID 56: stopped_flag resolved to 0
    2015-08-07 19:45:23,417 DEBUG    pytan.handler.ActionPoller: ID 56: status resolved to Open
    2015-08-07 19:45:28,427 DEBUG    pytan.handler.ActionPoller: ID 56: Progress: Seen Action: 2, Expected Seen: 2, Percent: 100%
    2015-08-07 19:45:28,427 DEBUG    pytan.handler.ActionPoller: ID 56: Timing: Started: 2015-08-07 19:45:08.353365, Expiration: 2015-08-07 20:40:10, Override Timeout: None, Elapsed Time: 0:00:20.074266, Left till expiry: 0:54:41.572371, Loop Count: 3
    2015-08-07 19:45:28,427 INFO     pytan.handler.ActionPoller: ID 56: Progress Changed for Seen Count 100% (2 of 2)
    2015-08-07 19:45:28,433 DEBUG    pytan.handler.ActionPoller: ID 56: stopped_flag resolved to 0
    2015-08-07 19:45:28,433 DEBUG    pytan.handler.ActionPoller: ID 56: status resolved to Open
    2015-08-07 19:45:28,433 INFO     pytan.handler.ActionPoller: ID 56: Reached Threshold for Seen Count of 100% (2 of 2)
    2015-08-07 19:45:28,443 DEBUG    pytan.handler.ActionPoller: ID 56: failed: 0, finished: 2, running: 0, success: 2, unknown: 0, Done Key: success, Passed Count: 2
    2015-08-07 19:45:28,443 DEBUG    pytan.handler.ActionPoller: ID 56: Timing: Started: 2015-08-07 19:45:08.353365, Expiration: 2015-08-07 20:40:10, Override Timeout: None, Elapsed Time: 0:00:20.089896, Left till expiry: 0:54:41.556741, Loop Count: 1
    2015-08-07 19:45:28,443 INFO     pytan.handler.ActionPoller: ID 56: Progress Changed for Finished Count 100% (2 of 2)
    2015-08-07 19:45:28,448 DEBUG    pytan.handler.ActionPoller: ID 56: stopped_flag resolved to 0
    2015-08-07 19:45:28,448 DEBUG    pytan.handler.ActionPoller: ID 56: status resolved to Open
    2015-08-07 19:45:28,448 INFO     pytan.handler.ActionPoller: ID 56: Reached Threshold for Finished Count of 100% (2 of 2)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'action_info': <taniumpy.object_types.result_info.ResultInfo object at 0x10c063810>,
     'action_object': <taniumpy.object_types.action.Action object at 0x10c063a50>,
     'action_result_map': {'failed': {'56:Expired.': [],
                                      '56:Failed.': [],
                                      '56:NotSucceeded.': [],
                                      '56:Stopped.': [],
                                      'total': 0},
                           'finished': {'56:Completed.': ['Casus-Belli.local',
                                                          'JTANIUM1.localdomain'],
                                        '56:Expired.': [],
                                        '56:Failed.': [],
                                        '56:NotSucceeded.': [],
                                        '56:Stopped.': [],
                                        '56:Succeeded.': [],
                                        '56:Verified.': [],
                                        'total': 2},
                           'running': {'56:Copying.': [],
                                       '56:Downloading.': [],
                                       '56:PendingVerification.': [],
                                       '56:Running.': [],
                                       '56:Waiting.': [],
                                       'total': 0},
                           'success': {'56:Completed.': ['Casus-Belli.local',
                                                         'JTANIUM1.localdomain'],
                                       '56:Verified.': [],
                                       'total': 2},
                           'unknown': {'total': 0}},
     'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x11acb14d0>,
     'group_object': None,
     'package_object': <taniumpy.object_types.package_spec.PackageSpec object at 0x10c03d0d0>,
     'poller_object': <pytan.pollers.ActionPoller object at 0x10c063b10>,
     'poller_success': True,
     'saved_action_object': <taniumpy.object_types.saved_action.SavedAction object at 0x10bf69750>}
    
    Print of action object: 
    Action, name: 'API Deploy Distribute Tanium Standard Utilities', id: 56
    
    CSV Results of response: 
    Action Statuses,Computer Name
    56:Completed.,Casus-Belli.local
    56:Completed.,JTANIUM1.localdomain
    
