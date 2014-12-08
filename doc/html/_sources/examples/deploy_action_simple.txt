
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
    2014-12-08 16:26:39,899 INFO     question_progress: Results 0% (Get Online = "True" from all machines)
    2014-12-08 16:26:44,920 INFO     question_progress: Results 50% (Get Online = "True" from all machines)
    2014-12-08 16:26:49,936 INFO     question_progress: Results 100% (Get Online = "True" from all machines)
    2014-12-08 16:26:50,011 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:26:51,045 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:26:52,079 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:26:53,112 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:26:54,152 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:26:55,185 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:26:56,219 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:26:57,251 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:26:58,286 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:26:59,329 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:00,372 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:01,482 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:02,523 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:03,559 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:04,603 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:05,647 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:06,688 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:07,731 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:08,770 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:09,813 INFO     action_progress: Action Results Passed: 33% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:10,851 INFO     action_progress: Action Results Passed: 33% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:11,889 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:12,925 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:13,968 INFO     action_progress: Action Results Passed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:15,005 INFO     action_progress: Action Results Passed: 83% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:16,041 INFO     action_progress: Action Results Passed: 100% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:16,077 INFO     action_progress: Action Results Completed: 100% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:16,077 INFO     action_progress: API Deploy Distribute Tanium Standard Utilities Result Counts:
    	Running Count: 0
    	Success Count: 6
    	Failed Count: 0
    	Unknown Count: 0
    	Finished Count: 6
    	Total Count: 6
    	Finished Count must equal: 6
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'action_object': <taniumpy.object_types.action.Action object at 0x102967d10>,
     'action_progress_human': 'API Deploy Distribute Tanium Standard Utilities Result Counts:\n\tRunning Count: 0\n\tSuccess Count: 6\n\tFailed Count: 0\n\tUnknown Count: 0\n\tFinished Count: 6\n\tTotal Count: 6\n\tFinished Count must equal: 6',
     'action_progress_map': {'Completed.': ['Casus-Belli.local',
                                            'jtanium1.localdomain',
                                            'ubuntu.(none)',
                                            'localhost.(none)',
                                            'Jims-Mac.local',
                                            'WIN-A12SC6N6T7Q']},
     'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x1025a2050>,
     'pre_action_question_results': {'question_object': <taniumpy.object_types.question.Question object at 0x1022ee8d0>,
                                     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x1022ae390>}}
    
    Print of action object: 
    Action, name: 'API Deploy Distribute Tanium Standard Utilities'
    
    CSV Results of response: 
    Action Statuses,Computer Name
    46:Completed.,Casus-Belli.local
    46:Completed.,jtanium1.localdomain
    46:Completed.,ubuntu.(none)
    46:Completed.,localhost.(none)
    46:Completed.,Jims-Mac.local
    46:Completed.,WIN-A12SC6N6T7Q
    
