
Deploy action with params against windows computers
====================================================================================================
Deploy an action with parameters against only windows computers using human strings.

This will use the Package 'Custom Tagging - Add Tags' and supply two parameters. The second parameter will be ignored because the package in question only requires one parameter.

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
    kwargs["package"] = u'Custom Tagging - Add Tags{$1=tag_should_be_added,$2=tag_should_be_ignore}'
    
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
    2014-12-08 15:16:07,230 INFO     question_progress: Results 0% (Get Online = "True" from all machines where Operating System contains "Windows")
    2014-12-08 15:16:12,246 INFO     question_progress: Results 33% (Get Online = "True" from all machines where Operating System contains "Windows")
    2014-12-08 15:16:17,264 INFO     question_progress: Results 100% (Get Online = "True" from all machines where Operating System contains "Windows")
    2014-12-08 15:16:17,344 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:18,376 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:19,403 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:20,432 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:21,459 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:22,491 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:23,517 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:24,546 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:25,574 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:26,602 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:27,629 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:28,659 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:29,690 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:30,718 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:31,746 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:32,772 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:33,798 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:34,829 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:35,858 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:36,892 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:37,922 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:38,951 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:39,980 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:41,006 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:42,037 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:43,063 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:44,089 INFO     action_progress: Action Results Passed: 100% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:44,113 INFO     action_progress: Action Results Completed: 100% (API Deploy Custom Tagging - Add Tags)
    2014-12-08 15:16:44,113 INFO     action_progress: API Deploy Custom Tagging - Add Tags Result Counts:
    	Running Count: 0
    	Success Count: 2
    	Failed Count: 0
    	Unknown Count: 0
    	Finished Count: 2
    	Total Count: 2
    	Finished Count must equal: 2
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'action_object': <taniumpy.object_types.action.Action object at 0x10e1bd7d0>,
     'action_progress_human': 'API Deploy Custom Tagging - Add Tags Result Counts:\n\tRunning Count: 0\n\tSuccess Count: 2\n\tFailed Count: 0\n\tUnknown Count: 0\n\tFinished Count: 2\n\tTotal Count: 2\n\tFinished Count must equal: 2',
     'action_progress_map': {'Completed.': ['jtanium1.localdomain',
                                            'WIN-A12SC6N6T7Q']},
     'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x10e36e110>,
     'pre_action_question_results': {'question_object': <taniumpy.object_types.question.Question object at 0x10e29fb90>,
                                     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10e049290>}}
    
    Print of action object: 
    Action, name: 'API Deploy Custom Tagging - Add Tags'
    
    CSV Results of response: 
    Action Statuses,Computer Name
    32:Completed.,jtanium1.localdomain
    32:Completed.,WIN-A12SC6N6T7Q
    
