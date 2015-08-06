
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


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
    2015-08-06 14:50:32,113 DEBUG    pytan.handler.ActionPoller: ID 36367: id resolved to 36367
    2015-08-06 14:50:32,113 DEBUG    pytan.handler.ActionPoller: ID 36367: package_spec resolved to PackageSpec, name: 'Distribute Tanium Standard Utilities', id: 20
    2015-08-06 14:50:32,120 DEBUG    pytan.handler.ActionPoller: ID 36367: target_group resolved to Group, name: 'Default'
    2015-08-06 14:50:32,121 DEBUG    pytan.handler.ActionPoller: ID 36367: Result Map resolved to {'failed': {'total': 0, '36367:Stopped.': [], '36367:Failed.': [], '36367:NotSucceeded.': [], '36367:Expired.': []}, 'finished': {'36367:Succeeded.': [], 'total': 0, '36367:NotSucceeded.': [], '36367:Verified.': [], '36367:Expired.': [], '36367:Completed.': [], '36367:Stopped.': [], '36367:Failed.': []}, 'running': {'36367:Waiting.': [], '36367:Downloading.': [], '36367:PendingVerification.': [], '36367:Running.': [], '36367:Copying.': [], 'total': 0}, 'success': {'36367:Verified.': [], '36367:Completed.': [], 'total': 0}, 'unknown': {'total': 0}}
    2015-08-06 14:50:32,121 DEBUG    pytan.handler.ActionPoller: ID 36367: expiration_time resolved to 2015-08-06T16:30:33
    2015-08-06 14:50:32,121 DEBUG    pytan.handler.ActionPoller: ID 36367: status resolved to Active
    2015-08-06 14:50:32,121 DEBUG    pytan.handler.ActionPoller: ID 36367: stopped_flag resolved to 0
    2015-08-06 14:50:32,121 DEBUG    pytan.handler.ActionPoller: ID 36367: Object Info resolved to ID 36367: Package: 'Distribute Tanium Standard Utilities', Target: 'None', Verify: False, Stopped: False, Status: Active
    2015-08-06 14:50:32,121 DEBUG    pytan.handler.ActionPoller: ID 36367: Adding Question to derive passed count
    2015-08-06 14:50:32,141 DEBUG    pytan.handler.QuestionPoller: ID 86265: id resolved to 86265
    2015-08-06 14:50:32,141 DEBUG    pytan.handler.QuestionPoller: ID 86265: expiration resolved to 2015-08-06T15:00:32
    2015-08-06 14:50:32,141 DEBUG    pytan.handler.QuestionPoller: ID 86265: query_text resolved to Get number of machines
    2015-08-06 14:50:32,141 DEBUG    pytan.handler.QuestionPoller: ID 86265: id resolved to 86265
    2015-08-06 14:50:32,141 DEBUG    pytan.handler.QuestionPoller: ID 86265: Object Info resolved to Question ID: 86265, Query: Get number of machines
    2015-08-06 14:50:32,145 DEBUG    pytan.handler.QuestionPoller: ID 86265: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
    2015-08-06 14:50:32,145 DEBUG    pytan.handler.QuestionPoller: ID 86265: Timing: Started: 2015-08-06 14:50:32.141355, Expiration: 2015-08-06 15:00:32, Override Timeout: None, Elapsed Time: 0:00:00.004623, Left till expiry: 0:09:59.854025, Loop Count: 1
    2015-08-06 14:50:32,146 INFO     pytan.handler.QuestionPoller: ID 86265: Progress Changed 0% (0 of 2)
    2015-08-06 14:50:37,150 DEBUG    pytan.handler.QuestionPoller: ID 86265: Progress: Tested: 2, Passed: 2, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 0
    2015-08-06 14:50:37,151 DEBUG    pytan.handler.QuestionPoller: ID 86265: Timing: Started: 2015-08-06 14:50:32.141355, Expiration: 2015-08-06 15:00:32, Override Timeout: None, Elapsed Time: 0:00:05.009666, Left till expiry: 0:09:54.848981, Loop Count: 2
    2015-08-06 14:50:37,151 INFO     pytan.handler.QuestionPoller: ID 86265: Progress Changed 100% (2 of 2)
    2015-08-06 14:50:37,151 INFO     pytan.handler.QuestionPoller: ID 86265: Reached Threshold of 99% (2 of 2)
    2015-08-06 14:50:37,151 DEBUG    pytan.handler.ActionPoller: ID 36367: Passed Count resolved to 2
    2015-08-06 14:50:37,163 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:50:37,163 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:00:05.042296, Left till expiry: 1:39:55.836498, Loop Count: 1
    2015-08-06 14:50:37,163 INFO     pytan.handler.ActionPoller: ID 36367: Progress Changed for Seen Count 0% (0 of 2)
    2015-08-06 14:50:42,236 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:50:42,236 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:00:10.115558, Left till expiry: 1:39:50.763235, Loop Count: 2
    2015-08-06 14:50:47,832 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:50:47,832 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:00:15.711630, Left till expiry: 1:39:45.167163, Loop Count: 3
    2015-08-06 14:50:52,847 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:50:52,847 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:00:20.726235, Left till expiry: 1:39:40.152558, Loop Count: 4
    2015-08-06 14:50:57,899 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:50:57,899 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:00:25.777914, Left till expiry: 1:39:35.100880, Loop Count: 5
    2015-08-06 14:51:02,912 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:51:02,912 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:00:30.791288, Left till expiry: 1:39:30.087506, Loop Count: 6
    2015-08-06 14:51:08,658 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:51:08,658 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:00:36.537588, Left till expiry: 1:39:24.341205, Loop Count: 7
    2015-08-06 14:51:13,694 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:51:13,694 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:00:41.573690, Left till expiry: 1:39:19.305104, Loop Count: 8
    2015-08-06 14:51:18,726 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:51:18,726 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:00:46.605506, Left till expiry: 1:39:14.273287, Loop Count: 9
    2015-08-06 14:51:24,008 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:51:24,008 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:00:51.887081, Left till expiry: 1:39:08.991713, Loop Count: 10
    2015-08-06 14:51:29,089 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:51:29,089 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:00:56.968196, Left till expiry: 1:39:03.910597, Loop Count: 11
    2015-08-06 14:51:34,229 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:51:34,229 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:01:02.107872, Left till expiry: 1:38:58.770922, Loop Count: 12
    2015-08-06 14:51:39,367 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:51:39,367 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:01:07.246739, Left till expiry: 1:38:53.632055, Loop Count: 13
    2015-08-06 14:51:44,687 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:51:44,687 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:01:12.566105, Left till expiry: 1:38:48.312688, Loop Count: 14
    2015-08-06 14:51:49,858 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:51:49,858 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:01:17.737761, Left till expiry: 1:38:43.141033, Loop Count: 15
    2015-08-06 14:51:55,192 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:51:55,192 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:01:23.071072, Left till expiry: 1:38:37.807721, Loop Count: 16
    2015-08-06 14:52:00,219 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:52:00,219 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:01:28.097952, Left till expiry: 1:38:32.780842, Loop Count: 17
    2015-08-06 14:52:05,236 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:52:05,236 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:01:33.115055, Left till expiry: 1:38:27.763738, Loop Count: 18
    2015-08-06 14:52:10,597 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 0, Expected Seen: 2, Percent: 0%
    2015-08-06 14:52:10,597 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:01:38.476750, Left till expiry: 1:38:22.402043, Loop Count: 19
    2015-08-06 14:52:15,612 DEBUG    pytan.handler.ActionPoller: ID 36367: Progress: Seen Action: 2, Expected Seen: 2, Percent: 100%
    2015-08-06 14:52:15,612 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:01:43.491537, Left till expiry: 1:38:17.387257, Loop Count: 20
    2015-08-06 14:52:15,612 INFO     pytan.handler.ActionPoller: ID 36367: Progress Changed for Seen Count 100% (2 of 2)
    2015-08-06 14:52:15,612 INFO     pytan.handler.ActionPoller: ID 36367: Reached Threshold for Seen Count of 100% (2 of 2)
    2015-08-06 14:52:15,630 DEBUG    pytan.handler.ActionPoller: ID 36367: failed: 0, finished: 0, running: 2, success: 0, unknown: 0, Done Key: success, Passed Count: 2
    2015-08-06 14:52:15,630 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:01:43.509485, Left till expiry: 1:38:17.369308, Loop Count: 1
    2015-08-06 14:52:15,630 INFO     pytan.handler.ActionPoller: ID 36367: Progress Changed for Finished Count 0% (0 of 2)
    2015-08-06 14:52:20,648 DEBUG    pytan.handler.ActionPoller: ID 36367: failed: 0, finished: 2, running: 2, success: 2, unknown: 0, Done Key: success, Passed Count: 2
    2015-08-06 14:52:20,648 DEBUG    pytan.handler.ActionPoller: ID 36367: Timing: Started: 2015-08-06 14:50:32.121209, Expiration: 2015-08-06 16:30:33, Override Timeout: None, Elapsed Time: 0:01:48.527015, Left till expiry: 1:38:12.351778, Loop Count: 2
    2015-08-06 14:52:20,648 INFO     pytan.handler.ActionPoller: ID 36367: Progress Changed for Finished Count 100% (2 of 2)
    2015-08-06 14:52:20,648 INFO     pytan.handler.ActionPoller: ID 36367: Reached Threshold for Finished Count of 100% (2 of 2)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'action_info': <taniumpy.object_types.result_info.ResultInfo object at 0x120937c50>,
     'action_object': <taniumpy.object_types.action.Action object at 0x1115fb350>,
     'action_result_map': {'failed': {'36367:Expired.': [],
                                      '36367:Failed.': [],
                                      '36367:NotSucceeded.': [],
                                      '36367:Stopped.': [],
                                      'total': 0},
                           'finished': {'36367:Completed.': ['Casus-Belli.local',
                                                             'jtanium1.localdomain'],
                                        '36367:Expired.': [],
                                        '36367:Failed.': [],
                                        '36367:NotSucceeded.': [],
                                        '36367:Stopped.': [],
                                        '36367:Succeeded.': [],
                                        '36367:Verified.': [],
                                        'total': 2},
                           'running': {'36367:Copying.': [],
                                       '36367:Downloading.': ['Casus-Belli.local',
                                                              'jtanium1.localdomain'],
                                       '36367:PendingVerification.': [],
                                       '36367:Running.': [],
                                       '36367:Waiting.': [],
                                       'total': 2},
                           'success': {'36367:Completed.': ['Casus-Belli.local',
                                                            'jtanium1.localdomain'],
                                       '36367:Verified.': [],
                                       'total': 2},
                           'unknown': {'total': 0}},
     'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x1115fb690>,
     'group_object': None,
     'package_object': <taniumpy.object_types.package_spec.PackageSpec object at 0x120937790>,
     'poller_object': <pytan.pollers.ActionPoller object at 0x120937750>,
     'poller_success': True,
     'saved_action_object': None}
    
    Print of action object: 
    Action, name: 'API Deploy Distribute Tanium Standard Utilities', id: 36367
    
    CSV Results of response: 
    Action Statuses,Computer Name
    36367:Completed.,Casus-Belli.local
    36367:Completed.,jtanium1.localdomain
    
