
Deploy action simple
====================================================================================================
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
    2014-12-07 01:08:53,692 INFO     question_progress: Results 0% (Get Online = "True" from all machines)
    2014-12-07 01:08:58,710 INFO     question_progress: Results 50% (Get Online = "True" from all machines)
    2014-12-07 01:09:03,728 INFO     question_progress: Results 100% (Get Online = "True" from all machines)
    2014-12-07 01:09:03,787 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:04,827 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:05,855 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:06,884 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:07,912 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:08,942 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:09,972 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:11,002 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:12,031 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:13,060 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:14,087 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:15,113 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:16,142 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:17,173 INFO     action_progress: Action Results Passed: 100% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:17,198 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:18,228 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:19,257 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:20,283 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:21,314 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:22,340 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:23,372 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:24,401 INFO     action_progress: Action Results Completed: 100% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-07 01:09:24,401 INFO     action_progress: API Deploy Distribute Tanium Standard Utilities Result Counts:
    	Running Count: 0
    	Success Count: 2
    	Failed Count: 0
    	Unknown Count: 0
    	Finished Count: 2
    	Total Count: 2
    	Finished Count must equal: 2
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'action_object': <taniumpy.object_types.action.Action object at 0x1023f2550>,
     'action_progress_human': 'API Deploy Distribute Tanium Standard Utilities Result Counts:\n\tRunning Count: 0\n\tSuccess Count: 2\n\tFailed Count: 0\n\tUnknown Count: 0\n\tFinished Count: 2\n\tTotal Count: 2\n\tFinished Count must equal: 2',
     'action_progress_map': {'Completed.': ['Casus-Belli.local',
                                            'jtanium1.localdomain']},
     'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x102146390>,
     'pre_action_question_results': {'question_object': <taniumpy.object_types.question.Question object at 0x1023f2fd0>,
                                     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x1025f7950>}}
    
    Print of action object: 
    Action, name: 'API Deploy Distribute Tanium Standard Utilities'
    
    CSV Results of response: 
    Action Statuses,Computer Name
    71:Completed.,Casus-Belli.local
    71:Completed.,jtanium1.localdomain
    
