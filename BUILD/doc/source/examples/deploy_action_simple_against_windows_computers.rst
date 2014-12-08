
Deploy action simple against windows computers
==========================================================================================
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
    2014-12-08 16:27:21,364 INFO     question_progress: Results 0% (Get Online = "True" from all machines where Operating System contains "Windows")
    2014-12-08 16:27:26,389 INFO     question_progress: Results 0% (Get Online = "True" from all machines where Operating System contains "Windows")
    2014-12-08 16:27:31,409 INFO     question_progress: Results 100% (Get Online = "True" from all machines where Operating System contains "Windows")
    2014-12-08 16:27:31,496 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:32,528 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:33,561 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:34,607 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:35,649 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:36,707 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:37,764 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:38,800 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:39,830 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:40,867 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:41,904 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:42,942 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:43,986 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:45,091 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:46,143 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:47,186 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:48,222 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:49,267 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:50,316 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:51,363 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:52,475 INFO     action_progress: Action Results Passed: 0% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:53,522 INFO     action_progress: Action Results Passed: 100% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:53,563 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:54,610 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:55,648 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:56,697 INFO     action_progress: Action Results Completed: 50% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:58,074 INFO     action_progress: Action Results Completed: 100% (API Deploy Distribute Tanium Standard Utilities)
    2014-12-08 16:27:58,074 INFO     action_progress: API Deploy Distribute Tanium Standard Utilities Result Counts:
    	Running Count: 0
    	Success Count: 2
    	Failed Count: 0
    	Unknown Count: 0
    	Finished Count: 2
    	Total Count: 2
    	Finished Count must equal: 2
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'action_object': <taniumpy.object_types.action.Action object at 0x102120410>,
     'action_progress_human': 'API Deploy Distribute Tanium Standard Utilities Result Counts:\n\tRunning Count: 0\n\tSuccess Count: 2\n\tFailed Count: 0\n\tUnknown Count: 0\n\tFinished Count: 2\n\tTotal Count: 2\n\tFinished Count must equal: 2',
     'action_progress_map': {'Completed.': ['jtanium1.localdomain',
                                            'WIN-A12SC6N6T7Q']},
     'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x102a047d0>,
     'pre_action_question_results': {'question_object': <taniumpy.object_types.question.Question object at 0x1029c97d0>,
                                     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x102186610>}}
    
    Print of action object: 
    Action, name: 'API Deploy Distribute Tanium Standard Utilities'
    
    CSV Results of response: 
    Action Statuses,Computer Name
    48:Completed.,jtanium1.localdomain
    48:Completed.,WIN-A12SC6N6T7Q
    
