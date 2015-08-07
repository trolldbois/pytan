
Deploy action with params against windows computers
==========================================================================================

Deploy an action with parameters against only windows computers using human strings.

This will use the Package 'Custom Tagging - Add Tags' and supply two parameters. The second parameter will be ignored because the package in question only requires one parameter.

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
    kwargs["package"] = u'Custom Tagging - Add Tags{$1=tag_should_be_added,$2=tag_should_be_ignore}'
    
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
    2015-08-07 19:45:48,755 DEBUG    pytan.handler.ActionPoller: ID 59: id resolved to 59
    2015-08-07 19:45:48,755 DEBUG    pytan.handler.ActionPoller: ID 59: package_spec resolved to PackageSpec, name: 'Custom Tagging - Add Tags', id: 81
    2015-08-07 19:45:48,759 DEBUG    pytan.handler.ActionPoller: ID 59: target_group resolved to Group, name: 'Default', id: 208
    2015-08-07 19:45:48,773 DEBUG    pytan.handler.ActionPoller: ID 59: Result Map resolved to {'failed': {'59:NotSucceeded.': [], '59:Stopped.': [], 'total': 0, '59:Expired.': [], '59:Failed.': []}, 'finished': {'59:NotSucceeded.': [], '59:Completed.': [], '59:Stopped.': [], '59:Succeeded.': [], '59:Failed.': [], 'total': 0, '59:Expired.': [], '59:Verified.': []}, 'running': {'59:Downloading.': [], '59:Running.': [], '59:PendingVerification.': [], '59:Waiting.': [], 'total': 0, '59:Copying.': []}, 'success': {'59:Completed.': [], 'total': 0, '59:Verified.': []}, 'unknown': {'total': 0}}
    2015-08-07 19:45:48,773 DEBUG    pytan.handler.ActionPoller: ID 59: expiration_time resolved to 2015-08-07T19:56:50
    2015-08-07 19:45:48,773 DEBUG    pytan.handler.ActionPoller: ID 59: status resolved to Open
    2015-08-07 19:45:48,773 DEBUG    pytan.handler.ActionPoller: ID 59: stopped_flag resolved to 0
    2015-08-07 19:45:48,773 DEBUG    pytan.handler.ActionPoller: ID 59: Object Info resolved to ID 59: Package: 'Custom Tagging - Add Tags', Target: ' Operating System containing "Windows"', Verify: False, Stopped: False, Status: Open
    2015-08-07 19:45:48,773 DEBUG    pytan.handler.ActionPoller: ID 59: Adding Question to derive passed count
    2015-08-07 19:45:48,802 DEBUG    pytan.handler.QuestionPoller: ID 1303: id resolved to 1303
    2015-08-07 19:45:48,802 DEBUG    pytan.handler.QuestionPoller: ID 1303: expiration resolved to 2015-08-07T19:55:48
    2015-08-07 19:45:48,802 DEBUG    pytan.handler.QuestionPoller: ID 1303: query_text resolved to Get number of machines with Operating System containing "Windows"
    2015-08-07 19:45:48,802 DEBUG    pytan.handler.QuestionPoller: ID 1303: id resolved to 1303
    2015-08-07 19:45:48,802 DEBUG    pytan.handler.QuestionPoller: ID 1303: Object Info resolved to Question ID: 1303, Query: Get number of machines with Operating System containing "Windows"
    2015-08-07 19:45:48,805 DEBUG    pytan.handler.QuestionPoller: ID 1303: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-07 19:45:48,805 DEBUG    pytan.handler.QuestionPoller: ID 1303: Timing: Started: 2015-08-07 19:45:48.802305, Expiration: 2015-08-07 19:55:48, Override Timeout: None, Elapsed Time: 0:00:00.003500, Left till expiry: 0:09:59.194197, Loop Count: 1
    2015-08-07 19:45:48,805 INFO     pytan.handler.QuestionPoller: ID 1303: Progress Changed 0% (0 of 2)
    2015-08-07 19:45:53,809 DEBUG    pytan.handler.QuestionPoller: ID 1303: Progress: Tested: 2, Passed: 1, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 0
    2015-08-07 19:45:53,809 DEBUG    pytan.handler.QuestionPoller: ID 1303: Timing: Started: 2015-08-07 19:45:48.802305, Expiration: 2015-08-07 19:55:48, Override Timeout: None, Elapsed Time: 0:00:05.007368, Left till expiry: 0:09:54.190329, Loop Count: 2
    2015-08-07 19:45:53,809 INFO     pytan.handler.QuestionPoller: ID 1303: Progress Changed 100% (2 of 2)
    2015-08-07 19:45:53,809 INFO     pytan.handler.QuestionPoller: ID 1303: Reached Threshold of 99% (2 of 2)
    2015-08-07 19:45:53,809 DEBUG    pytan.handler.ActionPoller: ID 59: Passed Count resolved to 1
    2015-08-07 19:45:53,819 DEBUG    pytan.handler.ActionPoller: ID 59: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
    2015-08-07 19:45:53,819 DEBUG    pytan.handler.ActionPoller: ID 59: Timing: Started: 2015-08-07 19:45:48.773547, Expiration: 2015-08-07 19:56:50, Override Timeout: None, Elapsed Time: 0:00:05.045590, Left till expiry: 0:10:56.180866, Loop Count: 1
    2015-08-07 19:45:53,819 INFO     pytan.handler.ActionPoller: ID 59: Progress Changed for Seen Count 0% (0 of 1)
    2015-08-07 19:45:53,824 DEBUG    pytan.handler.ActionPoller: ID 59: stopped_flag resolved to 0
    2015-08-07 19:45:53,824 DEBUG    pytan.handler.ActionPoller: ID 59: status resolved to Open
    2015-08-07 19:45:58,837 DEBUG    pytan.handler.ActionPoller: ID 59: Progress: Seen Action: 1, Expected Seen: 1, Percent: 100%
    2015-08-07 19:45:58,837 DEBUG    pytan.handler.ActionPoller: ID 59: Timing: Started: 2015-08-07 19:45:48.773547, Expiration: 2015-08-07 19:56:50, Override Timeout: None, Elapsed Time: 0:00:10.064178, Left till expiry: 0:10:51.162277, Loop Count: 2
    2015-08-07 19:45:58,837 INFO     pytan.handler.ActionPoller: ID 59: Progress Changed for Seen Count 100% (1 of 1)
    2015-08-07 19:45:58,843 DEBUG    pytan.handler.ActionPoller: ID 59: stopped_flag resolved to 0
    2015-08-07 19:45:58,844 DEBUG    pytan.handler.ActionPoller: ID 59: status resolved to Open
    2015-08-07 19:45:58,844 INFO     pytan.handler.ActionPoller: ID 59: Reached Threshold for Seen Count of 100% (1 of 1)
    2015-08-07 19:45:58,852 DEBUG    pytan.handler.ActionPoller: ID 59: failed: 0, finished: 0, running: 1, success: 0, unknown: 0, Done Key: success, Passed Count: 1
    2015-08-07 19:45:58,852 DEBUG    pytan.handler.ActionPoller: ID 59: Timing: Started: 2015-08-07 19:45:48.773547, Expiration: 2015-08-07 19:56:50, Override Timeout: None, Elapsed Time: 0:00:10.079198, Left till expiry: 0:10:51.147258, Loop Count: 1
    2015-08-07 19:45:58,852 INFO     pytan.handler.ActionPoller: ID 59: Progress Changed for Finished Count 0% (0 of 1)
    2015-08-07 19:45:58,858 DEBUG    pytan.handler.ActionPoller: ID 59: stopped_flag resolved to 0
    2015-08-07 19:45:58,858 DEBUG    pytan.handler.ActionPoller: ID 59: status resolved to Open
    2015-08-07 19:46:03,873 DEBUG    pytan.handler.ActionPoller: ID 59: failed: 0, finished: 0, running: 1, success: 0, unknown: 0, Done Key: success, Passed Count: 1
    2015-08-07 19:46:03,873 DEBUG    pytan.handler.ActionPoller: ID 59: Timing: Started: 2015-08-07 19:45:48.773547, Expiration: 2015-08-07 19:56:50, Override Timeout: None, Elapsed Time: 0:00:15.100064, Left till expiry: 0:10:46.126391, Loop Count: 2
    2015-08-07 19:46:03,879 DEBUG    pytan.handler.ActionPoller: ID 59: stopped_flag resolved to 0
    2015-08-07 19:46:03,879 DEBUG    pytan.handler.ActionPoller: ID 59: status resolved to Open
    2015-08-07 19:46:08,892 DEBUG    pytan.handler.ActionPoller: ID 59: failed: 0, finished: 1, running: 1, success: 1, unknown: 0, Done Key: success, Passed Count: 1
    2015-08-07 19:46:08,892 DEBUG    pytan.handler.ActionPoller: ID 59: Timing: Started: 2015-08-07 19:45:48.773547, Expiration: 2015-08-07 19:56:50, Override Timeout: None, Elapsed Time: 0:00:20.118648, Left till expiry: 0:10:41.107808, Loop Count: 3
    2015-08-07 19:46:08,892 INFO     pytan.handler.ActionPoller: ID 59: Progress Changed for Finished Count 100% (1 of 1)
    2015-08-07 19:46:08,898 DEBUG    pytan.handler.ActionPoller: ID 59: stopped_flag resolved to 0
    2015-08-07 19:46:08,898 DEBUG    pytan.handler.ActionPoller: ID 59: status resolved to Open
    2015-08-07 19:46:08,898 INFO     pytan.handler.ActionPoller: ID 59: Reached Threshold for Finished Count of 100% (1 of 1)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'action_info': <taniumpy.object_types.result_info.ResultInfo object at 0x10c063090>,
     'action_object': <taniumpy.object_types.action.Action object at 0x10c17ecd0>,
     'action_result_map': {'failed': {'59:Expired.': [],
                                      '59:Failed.': [],
                                      '59:NotSucceeded.': [],
                                      '59:Stopped.': [],
                                      'total': 0},
                           'finished': {'59:Completed.': ['JTANIUM1.localdomain'],
                                        '59:Expired.': [],
                                        '59:Failed.': [],
                                        '59:NotSucceeded.': [],
                                        '59:Stopped.': [],
                                        '59:Succeeded.': [],
                                        '59:Verified.': [],
                                        'total': 1},
                           'running': {'59:Copying.': [],
                                       '59:Downloading.': ['JTANIUM1.localdomain'],
                                       '59:PendingVerification.': [],
                                       '59:Running.': [],
                                       '59:Waiting.': [],
                                       'total': 1},
                           'success': {'59:Completed.': ['JTANIUM1.localdomain'],
                                       '59:Verified.': [],
                                       'total': 1},
                           'unknown': {'total': 0}},
     'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x10c17ec10>,
     'group_object': <taniumpy.object_types.group.Group object at 0x10c03d210>,
     'package_object': <taniumpy.object_types.package_spec.PackageSpec object at 0x10bf69dd0>,
     'poller_object': <pytan.pollers.ActionPoller object at 0x10c063250>,
     'poller_success': True,
     'saved_action_object': <taniumpy.object_types.saved_action.SavedAction object at 0x10c03ddd0>}
    
    Print of action object: 
    Action, name: 'API Deploy Custom Tagging - Add Tags', id: 59
    
    CSV Results of response: 
    Action Statuses,Computer Name
    59:Completed.,JTANIUM1.localdomain
    
