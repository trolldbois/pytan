
Create whitelisted url
====================================================================================================
Create a whitelisted url

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
    
    # setup the arguments for the delete method (to remove the package in case it exists)
    delete_kwargs = {}
    delete_kwargs["objtype"] = 'whitelisted_url'
    delete_kwargs["url_regex"] = 'regex:http://test.com/.*API_Test.*URL'
    
    
    # setup the arguments for the handler method
    kwargs = {}
    kwargs["url"] = u'http://test.com/.*API_Test.*URL'
    kwargs["regex"] = True
    kwargs["properties"] = [[u'property1', u'value1']]
    kwargs["download_seconds"] = 3600
    
    # delete the object in case it already exists
    try:
        handler.delete(**delete_kwargs)
    except Exception as e:
        print e
    
    # call the handler with the create_whitelisted_url method, passing in kwargs for arguments
    response = handler.create_whitelisted_url(**kwargs)
    
    
    print ""
    print "Type of response: ", type(response)
    
    print ""
    print "print of response:"
    print response
    
    print ""
    print "print the object returned in JSON format:"
    print response.to_json(response)
    
    # delete the object, we are done with it now
    try:
        handler.delete(**delete_kwargs)
    except Exception as e:
        print e
    
    


Output from Python Code
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
    No results found searching for whitelisted_url with {'url_regex': 'regex:http://test.com/.*API_Test.*URL'}!!
    2014-12-07 01:12:11,203 INFO     handler: New Whitelisted URL 'regex:http://test.com/.*API_Test.*URL' created with ID 17
    
    Type of response:  <class 'taniumpy.object_types.white_listed_url.WhiteListedUrl'>
    
    print of response:
    WhiteListedUrl, id: 17
    
    print the object returned in JSON format:
    {
      "_type": "white_listed_url", 
      "download_seconds": 3600, 
      "id": 17, 
      "metadata": {
        "_type": "metadata", 
        "item": [
          {
            "_type": "item", 
            "admin_flag": 0, 
            "name": "TConsole.WhitelistedURL.property1", 
            "value": "value1"
          }
        ]
      }, 
      "url_regex": "regex:http://test.com/.*API_Test.*URL"
    }
    2014-12-07 01:12:11,216 INFO     handler: Deleted 'WhiteListedUrl, id: 17'
