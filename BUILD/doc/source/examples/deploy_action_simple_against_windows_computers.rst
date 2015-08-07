
Deploy action simple against windows computers
==========================================================================================

Deploy an action against only windows computers using human strings. This requires passing in an action filter

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
    kwargs["action_filters"] = u'Operating System, that contains:Windows'
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
    2015-08-07 19:45:28,560 DEBUG    pytan.handler.ActionPoller: ID 58: id resolved to 58
    2015-08-07 19:45:28,561 DEBUG    pytan.handler.ActionPoller: ID 58: package_spec resolved to PackageSpec, name: 'Distribute Tanium Standard Utilities', id: 20
    2015-08-07 19:45:28,567 DEBUG    pytan.handler.ActionPoller: ID 58: target_group resolved to Group, name: 'Default', id: 206
    2015-08-07 19:45:28,583 DEBUG    pytan.handler.ActionPoller: ID 58: Result Map resolved to {'failed': {'58:Failed.': [], '58:NotSucceeded.': [], '58:Stopped.': [], 'total': 0, '58:Expired.': []}, 'finished': {'58:Stopped.': [], '58:Failed.': [], '58:Succeeded.': [], '58:Expired.': [], '58:NotSucceeded.': [], '58:Completed.': [], 'total': 0, '58:Verified.': []}, 'running': {'58:Waiting.': [], '58:Copying.': [], '58:Downloading.': [], '58:Running.': [], '58:PendingVerification.': [], 'total': 0}, 'success': {'58:Completed.': [], 'total': 0, '58:Verified.': []}, 'unknown': {'total': 0}}
    2015-08-07 19:45:28,583 DEBUG    pytan.handler.ActionPoller: ID 58: expiration_time resolved to 2015-08-07T20:40:30
    2015-08-07 19:45:28,583 DEBUG    pytan.handler.ActionPoller: ID 58: status resolved to Open
    2015-08-07 19:45:28,584 DEBUG    pytan.handler.ActionPoller: ID 58: stopped_flag resolved to 0
    2015-08-07 19:45:28,584 DEBUG    pytan.handler.ActionPoller: ID 58: Object Info resolved to ID 58: Package: 'Distribute Tanium Standard Utilities', Target: ' Operating System containing "Windows"', Verify: False, Stopped: False, Status: Open
    2015-08-07 19:45:28,584 DEBUG    pytan.handler.ActionPoller: ID 58: Adding Question to derive passed count
    2015-08-07 19:45:28,615 DEBUG    pytan.handler.QuestionPoller: ID 1302: id resolved to 1302
    2015-08-07 19:45:28,615 DEBUG    pytan.handler.QuestionPoller: ID 1302: expiration resolved to 2015-08-07T19:55:28
    2015-08-07 19:45:28,615 DEBUG    pytan.handler.QuestionPoller: ID 1302: query_text resolved to Get number of machines with Operating System containing "Windows"
    2015-08-07 19:45:28,615 DEBUG    pytan.handler.QuestionPoller: ID 1302: id resolved to 1302
    2015-08-07 19:45:28,615 DEBUG    pytan.handler.QuestionPoller: ID 1302: Object Info resolved to Question ID: 1302, Query: Get number of machines with Operating System containing "Windows"
    2015-08-07 19:45:28,618 DEBUG    pytan.handler.QuestionPoller: ID 1302: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:45:28,618 DEBUG    pytan.handler.QuestionPoller: ID 1302: Timing: Started: 2015-08-07 19:45:28.615340, Expiration: 2015-08-07 19:55:28, Override Timeout: None, Elapsed Time: 0:00:00.003187, Left till expiry: 0:09:59.381475, Loop Count: 1
    2015-08-07 19:45:28,618 INFO     pytan.handler.QuestionPoller: ID 1302: Progress Changed 0% (0 of 2)
    2015-08-07 19:45:33,623 DEBUG    pytan.handler.QuestionPoller: ID 1302: Progress: Tested: 1, Passed: 1, MR Tested: 1, MR Passed: 1, Est Total: 2, Row Count: 0
    2015-08-07 19:45:33,623 DEBUG    pytan.handler.QuestionPoller: ID 1302: Timing: Started: 2015-08-07 19:45:28.615340, Expiration: 2015-08-07 19:55:28, Override Timeout: None, Elapsed Time: 0:00:05.007761, Left till expiry: 0:09:54.376902, Loop Count: 2
    2015-08-07 19:45:33,623 INFO     pytan.handler.QuestionPoller: ID 1302: Progress Changed 50% (1 of 2)
    2015-08-07 19:45:38,626 DEBUG    pytan.handler.QuestionPoller: ID 1302: Progress: Tested: 2, Passed: 1, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 0
    2015-08-07 19:45:38,626 DEBUG    pytan.handler.QuestionPoller: ID 1302: Timing: Started: 2015-08-07 19:45:28.615340, Expiration: 2015-08-07 19:55:28, Override Timeout: None, Elapsed Time: 0:00:10.011393, Left till expiry: 0:09:49.373270, Loop Count: 3
    2015-08-07 19:45:38,626 INFO     pytan.handler.QuestionPoller: ID 1302: Progress Changed 100% (2 of 2)
    2015-08-07 19:45:38,626 INFO     pytan.handler.QuestionPoller: ID 1302: Reached Threshold of 99% (2 of 2)
    2015-08-07 19:45:38,626 DEBUG    pytan.handler.ActionPoller: ID 58: Passed Count resolved to 1
    2015-08-07 19:45:38,638 DEBUG    pytan.handler.ActionPoller: ID 58: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
    2015-08-07 19:45:38,638 DEBUG    pytan.handler.ActionPoller: ID 58: Timing: Started: 2015-08-07 19:45:28.584064, Expiration: 2015-08-07 20:40:30, Override Timeout: None, Elapsed Time: 0:00:10.054787, Left till expiry: 0:54:51.361151, Loop Count: 1
    2015-08-07 19:45:38,638 INFO     pytan.handler.ActionPoller: ID 58: Progress Changed for Seen Count 0% (0 of 1)
    2015-08-07 19:45:38,645 DEBUG    pytan.handler.ActionPoller: ID 58: stopped_flag resolved to 0
    2015-08-07 19:45:38,645 DEBUG    pytan.handler.ActionPoller: ID 58: status resolved to Open
    2015-08-07 19:45:43,660 DEBUG    pytan.handler.ActionPoller: ID 58: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
    2015-08-07 19:45:43,660 DEBUG    pytan.handler.ActionPoller: ID 58: Timing: Started: 2015-08-07 19:45:28.584064, Expiration: 2015-08-07 20:40:30, Override Timeout: None, Elapsed Time: 0:00:15.076845, Left till expiry: 0:54:46.339093, Loop Count: 2
    2015-08-07 19:45:43,667 DEBUG    pytan.handler.ActionPoller: ID 58: stopped_flag resolved to 0
    2015-08-07 19:45:43,667 DEBUG    pytan.handler.ActionPoller: ID 58: status resolved to Open
    2015-08-07 19:45:48,677 DEBUG    pytan.handler.ActionPoller: ID 58: Progress: Seen Action: 1, Expected Seen: 1, Percent: 100%
    2015-08-07 19:45:48,677 DEBUG    pytan.handler.ActionPoller: ID 58: Timing: Started: 2015-08-07 19:45:28.584064, Expiration: 2015-08-07 20:40:30, Override Timeout: None, Elapsed Time: 0:00:20.093828, Left till expiry: 0:54:41.322110, Loop Count: 3
    2015-08-07 19:45:48,677 INFO     pytan.handler.ActionPoller: ID 58: Progress Changed for Seen Count 100% (1 of 1)
    2015-08-07 19:45:48,684 DEBUG    pytan.handler.ActionPoller: ID 58: stopped_flag resolved to 0
    2015-08-07 19:45:48,684 DEBUG    pytan.handler.ActionPoller: ID 58: status resolved to Open
    2015-08-07 19:45:48,684 INFO     pytan.handler.ActionPoller: ID 58: Reached Threshold for Seen Count of 100% (1 of 1)
    2015-08-07 19:45:48,692 DEBUG    pytan.handler.ActionPoller: ID 58: failed: 0, finished: 1, running: 0, success: 1, unknown: 0, Done Key: success, Passed Count: 1
    2015-08-07 19:45:48,692 DEBUG    pytan.handler.ActionPoller: ID 58: Timing: Started: 2015-08-07 19:45:28.584064, Expiration: 2015-08-07 20:40:30, Override Timeout: None, Elapsed Time: 0:00:20.108869, Left till expiry: 0:54:41.307069, Loop Count: 1
    2015-08-07 19:45:48,692 INFO     pytan.handler.ActionPoller: ID 58: Progress Changed for Finished Count 100% (1 of 1)
    2015-08-07 19:45:48,698 DEBUG    pytan.handler.ActionPoller: ID 58: stopped_flag resolved to 0
    2015-08-07 19:45:48,698 DEBUG    pytan.handler.ActionPoller: ID 58: status resolved to Open
    2015-08-07 19:45:48,698 INFO     pytan.handler.ActionPoller: ID 58: Reached Threshold for Finished Count of 100% (1 of 1)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'action_info': <taniumpy.object_types.result_info.ResultInfo object at 0x11aadbcd0>,
     'action_object': <taniumpy.object_types.action.Action object at 0x11aae6090>,
     'action_result_map': {'failed': {'58:Expired.': [],
                                      '58:Failed.': [],
                                      '58:NotSucceeded.': [],
                                      '58:Stopped.': [],
                                      'total': 0},
                           'finished': {'58:Completed.': ['JTANIUM1.localdomain'],
                                        '58:Expired.': [],
                                        '58:Failed.': [],
                                        '58:NotSucceeded.': [],
                                        '58:Stopped.': [],
                                        '58:Succeeded.': [],
                                        '58:Verified.': [],
                                        'total': 1},
                           'running': {'58:Copying.': [],
                                       '58:Downloading.': [],
                                       '58:PendingVerification.': [],
                                       '58:Running.': [],
                                       '58:Waiting.': [],
                                       'total': 0},
                           'success': {'58:Completed.': ['JTANIUM1.localdomain'],
                                       '58:Verified.': [],
                                       'total': 1},
                           'unknown': {'total': 0}},
     'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x11ac77c90>,
     'group_object': <taniumpy.object_types.group.Group object at 0x10c03db90>,
     'package_object': <taniumpy.object_types.package_spec.PackageSpec object at 0x11aae6050>,
     'poller_object': <pytan.pollers.ActionPoller object at 0x10bea6950>,
     'poller_success': True,
     'saved_action_object': <taniumpy.object_types.saved_action.SavedAction object at 0x11acb14d0>}
    
    Print of action object: 
    Action, name: 'API Deploy Distribute Tanium Standard Utilities', id: 58
    
    CSV Results of response: 
    Action Statuses,Computer Name
    58:Completed.,JTANIUM1.localdomain
    
