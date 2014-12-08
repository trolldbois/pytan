
Invalid deploy action run false
====================================================================================================
Deploy an action without run=True, which will only run the pre-deploy action question that matches action_filters, export the results to a file, and raise a RunFalse exception

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
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
    2014-12-08 15:16:44,205 INFO     question_progress: Results 0% (Get Computer Name and Online = "True" from all machines)
    2014-12-08 15:16:49,223 INFO     question_progress: Results 17% (Get Computer Name and Online = "True" from all machines)
    2014-12-08 15:16:54,241 INFO     question_progress: Results 100% (Get Computer Name and Online = "True" from all machines)
    2014-12-08 15:16:54,263 INFO     handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/VERIFY_BEFORE_DEPLOY_ACTION_ResultSet_2014_12_08-15_16_54-EST.csv' written with 159 bytes
    Traceback (most recent call last):
      File "<string>", line 39, in <module>
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1172, in deploy_action_human
        **kwargs
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1003, in deploy_action
        raise RunFalse(m(report_path, len(result)))
    RunFalse: 'Run' is not True!!
    View and verify the contents of /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/VERIFY_BEFORE_DEPLOY_ACTION_ResultSet_2014_12_08-15_16_54-EST.csv (length: 159 bytes)
    Re-run this deploy action with run=True after verifying
