
Get sensor by mixed
====================================================================================================
Get multiple sensors by id, name, and hash

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
    kwargs["hash"] = [u'322086833']
    kwargs["name"] = [u'Computer Name']
    kwargs["id"] = [1, 2]
    
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
    SensorList, len: 4
    
    length of response (number of objects returned): 
    4
    
    print the first object returned in JSON format:
    {
      "_type": "sensor", 
      "category": "Reserved", 
      "description": "The recorded state of each download a client has made recently in the form of hash:completion percentage.\nExample: 05839407baccdfccfd8e2c1ffc0ff27541cc053d15b52cfd4ed904510e59b428:100", 
      "exclude_from_parse_flag": 0, 
      "hash": 322086833, 
      "hidden_flag": 0, 
      "id": 4, 
      "ignore_case_flag": 1, 
      "max_age_seconds": 900, 
      "name": "Download Statuses", 
      "queries": {
        "_type": "queries", 
        "query": [
          {
            "_type": "query", 
            "platform": "Windows", 
            "script": "Reserved", 
            "script_type": "WMIQuery"
          }
        ]
      }, 
      "source_id": 0, 
      "string_count": 301, 
      "value_type": "String"
    }
