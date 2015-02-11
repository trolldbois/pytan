
Deploy action with params against windows computers
==========================================================================================
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
    2015-02-11 12:05:58,335 INFO     question_progress: Results 0% (Get Online = "True" from all machines where Operating System contains "Windows")
    2015-02-11 12:06:03,353 INFO     question_progress: Results 100% (Get Online = "True" from all machines where Operating System contains "Windows")
    2015-02-11 12:06:03,424 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2015-02-11 12:06:04,450 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2015-02-11 12:06:05,477 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2015-02-11 12:06:06,506 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2015-02-11 12:06:07,534 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2015-02-11 12:06:08,564 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2015-02-11 12:06:09,589 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2015-02-11 12:06:10,615 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2015-02-11 12:06:11,642 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2015-02-11 12:06:12,668 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2015-02-11 12:06:13,694 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2015-02-11 12:06:14,725 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2015-02-11 12:06:15,750 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2015-02-11 12:06:16,776 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2015-02-11 12:06:17,802 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2015-02-11 12:06:18,828 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2015-02-11 12:06:19,855 INFO     action_progress: Action Results Passed: 100% (API Deploy Custom Tagging - Add Tags)
    2015-02-11 12:06:19,881 INFO     action_progress: Action Results Completed: 100% (API Deploy Custom Tagging - Add Tags)
    2015-02-11 12:06:19,881 INFO     action_progress: API Deploy Custom Tagging - Add Tags Result Counts:
    	Running Count: 0
    	Success Count: 1
    	Failed Count: 0
    	Unknown Count: 0
    	Finished Count: 1
    	Total Count: 1
    	Finished Count must equal: 1
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'action_object': <taniumpy.object_types.action.Action object at 0x1059c3fd0>,
     'action_progress_human': 'API Deploy Custom Tagging - Add Tags Result Counts:\n\tRunning Count: 0\n\tSuccess Count: 1\n\tFailed Count: 0\n\tUnknown Count: 0\n\tFinished Count: 1\n\tTotal Count: 1\n\tFinished Count must equal: 1',
     'action_progress_map': {'Completed.': ['jtanium1.localdomain']},
     'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x105c94890>,
     'pre_action_question_results': {'question_object': <taniumpy.object_types.question.Question object at 0x107b4bd50>,
                                     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x1059bf590>}}
    
    Print of action object: 
    Action, name: 'API Deploy Custom Tagging - Add Tags'
    
    CSV Results of response: 
    Action Statuses,Computer Name
    1372:Completed.,jtanium1.localdomain
    
