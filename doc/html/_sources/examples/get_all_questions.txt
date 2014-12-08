
Get all questions
====================================================================================================
Get all questions

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
    kwargs["objtype"] = u'question'
    
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
    
    Type of response:  <class 'taniumpy.object_types.question_list.QuestionList'>
    
    print of response:
    QuestionList, len: 830
    
    length of response (number of objects returned): 
    830
    
    print the first object returned in JSON format:
    {
      "_type": "question", 
      "action_tracking_flag": 0, 
      "cache_row_id": 0, 
      "context_group": {
        "_type": "group", 
        "id": 0
      }, 
      "expiration": "2014-12-06T18:08:58", 
      "expire_seconds": 600, 
      "hidden_flag": 0, 
      "id": 1, 
      "management_rights_group": {
        "_type": "group", 
        "id": 0
      }, 
      "query_text": "Get Action Statuses matches \"Nil\" from all machines", 
      "saved_question": {
        "_type": "saved_question", 
        "id": 4294967295
      }, 
      "skip_lock_flag": 0, 
      "user": {
        "_type": "user", 
        "group_id": 0, 
        "id": 1, 
        "name": "Jim Olsen"
      }
    }
