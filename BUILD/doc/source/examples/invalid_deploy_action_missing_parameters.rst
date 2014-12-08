
Invalid deploy action missing parameters
====================================================================================================
Deploy an action using a package that requires parameters but do not supply any parameters.

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
    kwargs["run"] = True
    kwargs["package"] = u'Custom Tagging - Add Tags'
    
    
    # call the handler with the deploy_action_human method, passing in kwargs for arguments
    # this should throw an exception: pytan.utils.HandlerError
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
    2014-12-07 01:11:50,769 INFO     question_progress: Results 0% (Get Online = "True" from all machines)
    2014-12-07 01:11:55,787 INFO     question_progress: Results 50% (Get Online = "True" from all machines)
    2014-12-07 01:12:00,804 INFO     question_progress: Results 100% (Get Online = "True" from all machines)
    Traceback (most recent call last):
      File "<string>", line 40, in <module>
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1109, in deploy_action_human
        **kwargs
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 982, in deploy_action
        empty_ok=False,
      File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2071, in build_param_objlist
        raise HandlerError(err(obj_name, p_key, jsonify(obj_param)))
    HandlerError: PackageSpec, name: 'Custom Tagging - Add Tags' parameter key '$1' requires a value, parameter definition:
    {
      "defaultValue": "", 
      "helpString": "Enter tags space-delimited.", 
      "key": "$1", 
      "label": "Add tags (space-delimited)", 
      "maxChars": 0, 
      "model": "com.tanium.components.parameters::TextInputParameter", 
      "parameterType": "com.tanium.components.parameters::TextInputParameter", 
      "promptText": "e.g. PCI DMZ Decomm", 
      "restrict": null, 
      "validationExpressions": [
        {
          "expression": "\\S", 
          "flags": "", 
          "helpString": "You must enter a value", 
          "model": "com.tanium.models::ValidationExpression", 
          "parameterType": "com.tanium.models::ValidationExpression"
        }
      ], 
      "value": ""
    }
