
Deploy action simple against windows computers
====================================================================================================
Deploy an action against only windows computers using human strings. This requires passing in an action filter

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
    kwargs["action_filters"] = u'Operating System, that contains:Windows'
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
    2014-12-08 15:15:29,145 INFO     question_progress: Results 0% (Get Online = "True" from all machines where Operating System contains "Windows")
    2014-12-08 15:15:34,162 INFO     question_progress: Results 83% (Get Online = "True" from all machines where Operating System contains "Windows")
    2014-12-08 15:15:39,180 INFO     question_progress: Results 100% (Get Online = "True" from all machines where Operating System contains "Windows")
    2014-12-08 15:15:39,253 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:40,281 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:41,314 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:42,344 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:43,378 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:44,407 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:45,435 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:46,465 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:47,491 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:48,518 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:49,545 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:50,576 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:51,602 INFO     action_progress: Action Results Passed: 100% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:51,627 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:52,656 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:53,685 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:54,735 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:55,764 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:56,858 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:57,886 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:58,912 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:15:59,941 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:16:00,972 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:16:02,001 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:16:03,029 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:16:04,059 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:16:05,089 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:16:06,114 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:16:07,144 INFO     action_progress: Action Results Completed: 100% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 15:16:07,145 INFO     action_progress: API Deploy Distribute Tanium Standard Utilities Result Counts:
    	Running Count: 0
    	Success Count: 2
    	Failed Count: 0
    	Unknown Count: 0
    	Finished Count: 2
    	Total Count: 2
    	Finished Count must equal: 2
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'action_object': <taniumpy.object_types.action.Action object at 0x10e1aa6d0>,
     'action_progress_human': 'API Deploy Distribute Tanium Standard Utilities Result Counts:\n\tRunning Count: 0\n\tSuccess Count: 2\n\tFailed Count: 0\n\tUnknown Count: 0\n\tFinished Count: 2\n\tTotal Count: 2\n\tFinished Count must equal: 2',
     'action_progress_map': {'Completed.': ['jtanium1.localdomain',
                                            'WIN-A12SC6N6T7Q']},
     'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x10e7d5c50>,
     'pre_action_question_results': {'question_object': <taniumpy.object_types.question.Question object at 0x10e670d10>,
                                     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10e1af050>}}
    
    Print of action object: 
    Action, name: 'API Deploy Distribute Tanium Standard Utilities'
    
    CSV Results of response: 
    Action Statuses,Computer Name
    31:Completed.,jtanium1.localdomain
    31:Completed.,WIN-A12SC6N6T7Q
    
