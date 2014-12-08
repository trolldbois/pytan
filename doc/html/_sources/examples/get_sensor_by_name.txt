
Get sensor by name
====================================================================================================
Get a sensor by name

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
    kwargs["objtype"] = u'sensor'
    kwargs["name"] = u'Computer Name'
    
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
    
    Type of response:  <class 'taniumpy.object_types.sensor_list.SensorList'>
    
    print of response:
    SensorList, len: 1
    
    length of response (number of objects returned): 
    1
    
    print the first object returned in JSON format:
    {
      "_type": "sensor", 
      "category": "Reserved", 
      "description": "The assigned name of the client machine.\nExample: workstation-1.company.com", 
      "exclude_from_parse_flag": 0, 
      "hash": 3409330187, 
      "hidden_flag": 0, 
      "id": 3, 
      "ignore_case_flag": 1, 
      "max_age_seconds": 86400, 
      "name": "Computer Name", 
      "queries": {
        "_type": "queries", 
        "query": [
          {
            "_type": "query", 
            "platform": "Windows", 
            "script": "select CSName from win32_operatingsystem", 
            "script_type": "WMIQuery"
          }
        ]
      }, 
      "source_id": 0, 
      "string_count": 7, 
      "value_type": "String"
    }
