
Deploy action simple
==========================================================================================
Deploy an action against all computers using human strings.

Example Python Code
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: python
    :linenos:


    # Path to lib directory which contains pytan package
    PYTAN_LIB_PATH = '../lib'
    
    # connection info for Tanium Server
    USERNAME = "Tanium User"
    PASSWORD = "T@n!um"
    HOST = "172.16.31.128"
    PORT = "444"
    
    # Logging conrols
    LOGLEVEL = 2
    DEBUGFORMAT = False
    
    import sys, tempfile
    sys.path.append(PYTAN_LIB_PATH)
    
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
    
    # call the handler with the deploy_action_human method, passing in kwargs for arguments
    response = handler.deploy_action_human(**kwargs)
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
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
    2015-02-11 12:04:34,212 INFO     question_progress: Results 0% (Get Online = "True" from all machines)
    2015-02-11 12:04:39,226 INFO     question_progress: Results 50% (Get Online = "True" from all machines)
    2015-02-11 12:04:44,244 INFO     question_progress: Results 50% (Get Online = "True" from all machines)
    2015-02-11 12:04:49,258 INFO     question_progress: Results 100% (Get Online = "True" from all machines)
    2015-02-11 12:04:49,318 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:04:50,371 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:04:51,398 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:04:52,423 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:04:53,450 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:04:54,480 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:04:55,509 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:04:56,541 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:04:57,570 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:04:58,594 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:04:59,622 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:05:00,651 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:05:01,680 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:05:02,708 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:05:03,735 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:05:04,762 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:05:05,793 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:05:06,822 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:05:07,851 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:05:08,882 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:05:09,910 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:05:10,942 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:05:11,970 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:05:12,995 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:05:14,024 INFO     action_progress: Action Results Passed: 100% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:05:14,050 INFO     action_progress: Action Results Completed: 100% (API Deploy Distribute Tanium Standard Utilities)
    2015-02-11 12:05:14,050 INFO     action_progress: API Deploy Distribute Tanium Standard Utilities Result Counts:
    	Running Count: 0
    	Success Count: 2
    	Failed Count: 0
    	Unknown Count: 0
    	Finished Count: 2
    	Total Count: 2
    	Finished Count must equal: 2
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'action_object': <taniumpy.object_types.action.Action object at 0x105d5b4d0>,
     'action_progress_human': 'API Deploy Distribute Tanium Standard Utilities Result Counts:\n\tRunning Count: 0\n\tSuccess Count: 2\n\tFailed Count: 0\n\tUnknown Count: 0\n\tFinished Count: 2\n\tTotal Count: 2\n\tFinished Count must equal: 2',
     'action_progress_map': {'Completed.': ['Casus-Belli.local',
                                            'jtanium1.localdomain']},
     'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x105cc1fd0>,
     'pre_action_question_results': {'question_object': <taniumpy.object_types.question.Question object at 0x107b074d0>,
                                     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x1059bcad0>}}
    
    Print of action object: 
    Action, name: 'API Deploy Distribute Tanium Standard Utilities'
    
    CSV Results of response: 
    Action Statuses,Computer Name
    1369:Completed.,Casus-Belli.local
    1369:Completed.,jtanium1.localdomain
    
