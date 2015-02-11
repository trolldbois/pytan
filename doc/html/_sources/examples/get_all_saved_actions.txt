
Get all saved actions
==========================================================================================
Get all saved actions

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
    kwargs["objtype"] = u'saved_action'
    
    # call the handler with the get_all method, passing in kwargs for arguments
    response = handler.get_all(**kwargs)
    
    print ""
    print "Type of response: ", type(response)
    
    print ""
    print "print of response:"
    print response
    
    print ""
    print "length of response (number of objects returned): "
    print len(response)
    
    print ""
    print "print the first object returned in JSON format:"
    out = response.to_json(response[0])
    if len(out.splitlines()) > 15:
        out = out.splitlines()[0:15]
        out.append('..trimmed for brevity..')
        out = '\n'.join(out)
    
    print out
    
    


Output from Python Code
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
    
    Type of response:  <class 'taniumpy.object_types.saved_action_list.SavedActionList'>
    
    print of response:
    SavedActionList, len: 42
    
    length of response (number of objects returned): 
    42
    
    print the first object returned in JSON format:
    {
      "_type": "saved_action", 
      "action_group_id": 0, 
      "cache_row_id": 0, 
      "comment": "Scans for unmanaged assets on the network.", 
      "creation_time": "2015-01-05T20:23:38", 
      "distribute_seconds": 600, 
      "end_time": "Never", 
      "expire_seconds": 1800, 
      "id": 1, 
      "issue_count": 192, 
      "issue_seconds": 3600, 
      "last_action": {
        "_type": "action", 
        "id": 1366, 
    ..trimmed for brevity..
