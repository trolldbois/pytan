
Deploy action simple without results
==========================================================================================

Deploy an action against all computers using human strings, but do not get the completed results of the job -- return right away with the deploy action object.

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
    kwargs["get_results"] = False
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
    2015-08-06 14:52:20,736 DEBUG    pytan.handler.ActionPoller: ID 36368: id resolved to 36368
    2015-08-06 14:52:20,736 DEBUG    pytan.handler.ActionPoller: ID 36368: package_spec resolved to PackageSpec, name: 'Distribute Tanium Standard Utilities', id: 20
    2015-08-06 14:52:20,745 DEBUG    pytan.handler.ActionPoller: ID 36368: target_group resolved to Group, name: 'Default'
    2015-08-06 14:52:20,745 DEBUG    pytan.handler.ActionPoller: ID 36368: Result Map resolved to {'failed': {'36368:Failed.': [], '36368:NotSucceeded.': [], '36368:Expired.': [], 'total': 0, '36368:Stopped.': []}, 'finished': {'36368:Completed.': [], '36368:Verified.': [], '36368:Stopped.': [], '36368:Failed.': [], '36368:Succeeded.': [], '36368:Expired.': [], '36368:NotSucceeded.': [], 'total': 0}, 'running': {'36368:Waiting.': [], '36368:Copying.': [], '36368:PendingVerification.': [], '36368:Running.': [], '36368:Downloading.': [], 'total': 0}, 'success': {'total': 0, '36368:Completed.': [], '36368:Verified.': []}, 'unknown': {'total': 0}}
    2015-08-06 14:52:20,745 DEBUG    pytan.handler.ActionPoller: ID 36368: expiration_time resolved to 2015-08-06T16:32:21
    2015-08-06 14:52:20,745 DEBUG    pytan.handler.ActionPoller: ID 36368: status resolved to Active
    2015-08-06 14:52:20,745 DEBUG    pytan.handler.ActionPoller: ID 36368: stopped_flag resolved to 0
    2015-08-06 14:52:20,745 DEBUG    pytan.handler.ActionPoller: ID 36368: Object Info resolved to ID 36368: Package: 'Distribute Tanium Standard Utilities', Target: 'None', Verify: False, Stopped: False, Status: Active
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'action_info': <taniumpy.object_types.result_info.ResultInfo object at 0x1115fbf90>,
     'action_object': <taniumpy.object_types.action.Action object at 0x1115fb710>,
     'action_result_map': None,
     'action_results': None,
     'group_object': None,
     'package_object': <taniumpy.object_types.package_spec.PackageSpec object at 0x120937550>,
     'poller_object': <pytan.pollers.ActionPoller object at 0x1115fbb90>,
     'poller_success': None,
     'saved_action_object': None}
    
    Print of action object: 
    Action, name: 'API Deploy Distribute Tanium Standard Utilities', id: 36368
