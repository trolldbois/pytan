
Get saved question by name
==========================================================================================
Get saved question by name

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
    kwargs["objtype"] = u'saved_question'
    kwargs["name"] = u'Installed Applications'
    
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
    
    Type of response:  <class 'taniumpy.object_types.saved_question_list.SavedQuestionList'>
    
    print of response:
    SavedQuestionList, len: 1
    
    length of response (number of objects returned): 
    1
    
    print the first object returned in JSON format:
    {
      "_type": "saved_question", 
      "action_tracking_flag": 0, 
      "archive_enabled_flag": 0, 
      "archive_owner": {
        "_type": "user", 
        "id": 1, 
        "name": "Jim Olsen"
      }, 
      "expire_seconds": 600, 
      "hidden_flag": 0, 
      "id": 92, 
      "issue_seconds": 120, 
      "issue_seconds_never_flag": 0, 
      "keep_seconds": 3600, 
    ..trimmed for brevity..
