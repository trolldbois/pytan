
Get all clients
====================================================================================================
Get all clients

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
    kwargs["objtype"] = u'client'
    
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
    print response.to_json(response[0])
    


Output from Python Code
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
    
    Type of response:  <class 'taniumpy.object_types.system_status_list.SystemStatusList'>
    
    print of response:
    SystemStatusList, len: 6
    
    length of response (number of objects returned): 
    6
    
    print the first object returned in JSON format:
    {
      "_type": "client_status", 
      "cache_row_id": 0, 
      "computer_id": "660621737", 
      "full_version": "5.1.314.7724", 
      "host_name": "Casus-Belli.local", 
      "ipaddress_client": "172.16.31.1", 
      "ipaddress_server": "172.16.31.1", 
      "last_registration": "2014-12-08T20:14:15", 
      "port_number": 17472, 
      "protocol_version": 314, 
      "send_state": "Forward Only", 
      "status": "Leader, Slow Link Behind"
    }
