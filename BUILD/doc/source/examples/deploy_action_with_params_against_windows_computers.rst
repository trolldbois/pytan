
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
    kwargs["action_filters"] = u'Operating System, that contains Windows'
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
    2014-12-07 01:10:02,665 INFO     question_progress: Results 0% (Get Online = "True" from all machines where Operating System contains "Windows")
    2014-12-07 01:10:07,682 INFO     question_progress: Results 100% (Get Online = "True" from all machines where Operating System contains "Windows")
    2014-12-07 01:10:07,754 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:08,780 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:09,808 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:10,837 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:11,867 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:12,893 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:13,924 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:14,953 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:15,981 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:17,012 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:18,039 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:19,069 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:20,097 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:21,124 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:22,155 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:23,182 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:24,212 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:25,237 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:26,263 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:27,288 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:28,319 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:29,347 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:30,375 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:31,402 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:32,430 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:33,461 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:34,490 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:35,520 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:36,547 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:37,574 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:38,604 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:39,633 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:40,662 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:41,691 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:42,720 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:43,752 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:44,786 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:45,811 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:46,841 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:47,872 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:48,902 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:49,932 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:50,961 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:51,992 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:53,021 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:54,049 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:55,080 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:56,111 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:57,137 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:58,169 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:10:59,198 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:00,226 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:01,254 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:02,285 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:03,314 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:04,345 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:05,374 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:06,406 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:07,432 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:08,461 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:09,492 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:10,523 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:11,552 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:12,580 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:13,610 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:14,641 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:15,672 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:16,701 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:17,730 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:18,762 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:19,790 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:20,818 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:21,850 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:22,875 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:23,905 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:24,936 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:25,965 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:26,992 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:28,022 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:29,053 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:30,079 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:31,111 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:32,144 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:33,174 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:34,204 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:35,233 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:36,261 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:37,290 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:38,317 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:39,347 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:40,375 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:41,404 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:42,433 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:43,464 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:44,490 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:45,520 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:46,552 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:47,581 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:48,608 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:49,635 INFO     action_progress: Action Results Passed: 0% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:50,667 INFO     action_progress: Action Results Passed: 100% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:50,692 INFO     action_progress: Action Results Completed: 100% (API Deploy Custom Tagging - Add Tags)
    2014-12-07 01:11:50,692 INFO     action_progress: API Deploy Custom Tagging - Add Tags Result Counts:
    	Running Count: 0
    	Success Count: 1
    	Failed Count: 0
    	Unknown Count: 0
    	Finished Count: 1
    	Total Count: 1
    	Finished Count must equal: 1
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'action_object': <taniumpy.object_types.action.Action object at 0x1022fa050>,
     'action_progress_human': 'API Deploy Custom Tagging - Add Tags Result Counts:\n\tRunning Count: 0\n\tSuccess Count: 1\n\tFailed Count: 0\n\tUnknown Count: 0\n\tFinished Count: 1\n\tTotal Count: 1\n\tFinished Count must equal: 1',
     'action_progress_map': {'Completed.': ['jtanium1.localdomain']},
     'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x1022ad310>,
     'pre_action_question_results': {'question_object': <taniumpy.object_types.question.Question object at 0x102040a50>,
                                     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x102054c90>}}
    
    Print of action object: 
    Action, name: 'API Deploy Custom Tagging - Add Tags'
    
    CSV Results of response: 
    Action Statuses,Computer Name
    74:Completed.,jtanium1.localdomain
    
