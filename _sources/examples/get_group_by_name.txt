
Get group by name
====================================================================================================
Get a group by name

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
    kwargs["objtype"] = u'group'
    kwargs["name"] = u'All Computers'
    
    # call the handler with the get method, passing in kwargs for arguments
    response = handler.get(**kwargs)
    
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
    print response.to_json(response[0])
    


Output from Python Code
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
    
    Type of response:  <class 'taniumpy.object_types.group_list.GroupList'>
    
    print of response:
    GroupList, len: 1
    
    length of response (number of objects returned): 
    1
    
    print the first object returned in JSON format:
    {
      "_type": "group", 
      "and_flag": 0, 
      "deleted_flag": 0, 
      "filters": {
        "_type": "filters", 
        "filter": []
      }, 
      "id": 1, 
      "name": "All Computers", 
      "not_flag": 0, 
      "sub_groups": {
        "_type": "groups", 
        "group": []
      }, 
      "type": 0
    }
