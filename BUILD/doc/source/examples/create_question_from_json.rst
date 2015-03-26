
Create question from json
==========================================================================================

Export a question object to a JSON file, then create a new question object from the exported JSON file. Questions can not be deleted, so do not delete it. This will, in effect, 're-ask' a question.

Example Python Code
----------------------------------------------------------------------------------------

.. code-block:: python
    :linenos:


    
    import os
    import sys
    sys.dont_write_bytecode = True
    
    # Determine our script name, script dir
    my_file = os.path.abspath(sys.argv[0])
    my_dir = os.path.dirname(my_file)
    
    # determine the pytan lib dir and add it to the path
    parent_dir = os.path.dirname(my_dir)
    pytan_root_dir = os.path.dirname(parent_dir)
    lib_dir = os.path.join(pytan_root_dir, 'lib')
    path_adds = [lib_dir]
    
    for aa in path_adds:
        if aa not in sys.path:
            sys.path.append(aa)
    
    
    # connection info for Tanium Server
    USERNAME = "Tanium User"
    PASSWORD = "T@n!um"
    HOST = "172.16.31.128"
    PORT = "444"
    
    # Logging conrols
    LOGLEVEL = 2
    DEBUGFORMAT = False
    
    import tempfile
    
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
    
    # set the attribute name and value we want to add to the original object (if any)
    attr_name = ""
    attr_add = ""
    
    # delete object before creating it?
    delete = False
    
    # setup the arguments for getting an object to export as json file
    get_kwargs = {}
    get_kwargs["objtype"] = u'question'
    get_kwargs["id"] = 1
    
    
    # get objects to use as an export to JSON file
    orig_objs = handler.get(**get_kwargs)
    
    # if attr_name and attr_add exists, modify the orig_objs to add attr_add to the attribute
    # attr_name
    if attr_name:
        for x in orig_objs:
            new_attr = getattr(x, attr_name)
            new_attr += attr_add
            setattr(x, attr_name, new_attr)
            if delete:
                # delete the object in case it already exists
                del_kwargs = {}
                del_kwargs[attr_name] = new_attr
                del_kwargs['objtype'] = u'question'
                try:
                    handler.delete(**del_kwargs)
                except Exception as e:
                    print e
    
    # export orig_objs to a json file
    json_file, results = handler.export_to_report_file(
        obj=orig_objs,
        export_format='json',
        report_dir=tempfile.gettempdir(),
    )
    
    # create the object from the exported JSON file
    create_kwargs = {'objtype': u'question', 'json_file': json_file}
    response = handler.create_from_json(**create_kwargs)
    
    
    print ""
    print "Type of response: ", type(response)
    
    print ""
    print "print of response:"
    print response
    
    print ""
    print "print the object returned in JSON format:"
    print response.to_json(response)
    


Output from Python Code
----------------------------------------------------------------------------------------

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
    2015-03-26 11:49:19,898 INFO     handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/QuestionList_2015_03_26-11_49_19-EDT.json' written with 775 bytes
    2015-03-26 11:49:19,928 INFO     handler: New Question, id: 32660 (ID: 32660) created successfully!
    
    Type of response:  <class 'taniumpy.object_types.question_list.QuestionList'>
    
    print of response:
    QuestionList, len: 1
    
    print the object returned in JSON format:
    {
      "_type": "questions", 
      "question": [
        {
          "_type": "question", 
          "action_tracking_flag": 0, 
          "context_group": {
            "_type": "group", 
            "id": 0
          }, 
          "expiration": "2015-03-26T15:59:20", 
          "expire_seconds": 0, 
          "force_computer_id_flag": 0, 
          "hidden_flag": 0, 
          "id": 32660, 
          "management_rights_group": {
            "_type": "group", 
            "id": 0
          }, 
          "query_text": "Get number of machines", 
          "saved_question": {
            "_type": "saved_question", 
            "id": 0
          }, 
          "selects": {
            "_type": "selects", 
            "select": []
          }, 
          "skip_lock_flag": 0, 
          "user": {
            "_type": "user", 
            "id": 2, 
            "name": "Tanium User"
          }
        }
      ]
    }
