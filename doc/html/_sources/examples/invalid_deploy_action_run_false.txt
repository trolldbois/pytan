
Invalid deploy action run false
==========================================================================================

Deploy an action without run=True, which will only run the pre-deploy action question that matches action_filters, export the results to a file, and raise a RunFalse exception

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
    kwargs['report_dir'] = tempfile.gettempdir()
    kwargs["package"] = u'Distribute Tanium Standard Utilities'
    
    
    # call the handler with the deploy_action_human method, passing in kwargs for arguments
    # this should throw an exception: pytan.utils.RunFalse
    import traceback
    try:
        handler.deploy_action_human(**kwargs)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
    
    


Output from Python Code
----------------------------------------------------------------------------------------

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
    2015-03-26 11:48:58,305 INFO     question_progress: Results 0% (Get Computer Name and Online = "True" from all machines)
    2015-03-26 11:49:03,333 INFO     question_progress: Results 50% (Get Computer Name and Online = "True" from all machines)
    2015-03-26 11:49:08,354 INFO     question_progress: Results 100% (Get Computer Name and Online = "True" from all machines)
    2015-03-26 11:49:08,376 INFO     handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/VERIFY_BEFORE_DEPLOY_ACTION_ResultSet_2015_03_26-11_49_08-EDT.csv' written with 73 bytes
    Traceback (most recent call last):
      File "<string>", line 55, in <module>
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1193, in deploy_action_human
        **kwargs
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1034, in deploy_action
        raise RunFalse(m(report_path, len(result)))
    RunFalse: 'Run' is not True!!
    View and verify the contents of /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/VERIFY_BEFORE_DEPLOY_ACTION_ResultSet_2015_03_26-11_49_08-EDT.csv (length: 73 bytes)
    Re-run this deploy action with run=True after verifying
