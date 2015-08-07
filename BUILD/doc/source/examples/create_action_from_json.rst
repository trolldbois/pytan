
Create action from json
==========================================================================================

Export an action object to a JSON file, then create a new action object from the exported JSON file. Actions can not be deleted, so do not delete it. This will, in effect, 're-deploy' an action.

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
    PORT = "443"
    
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
    get_kwargs["objtype"] = u'action'
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
                del_kwargs['objtype'] = u'action'
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
    create_kwargs = {'objtype': u'action', 'json_file': json_file}
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


    Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
    2015-08-07 19:46:14,474 INFO     pytan.handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/ActionList_2015_08_07-15_46_14-EDT.json' written with 1294 bytes
    2015-08-07 19:46:14,496 INFO     pytan.handler: New Action, name: 'Distribute Tanium Standard Utilities', id: 60 (ID: 60) created successfully!
    
    Type of response:  <class 'taniumpy.object_types.action_list.ActionList'>
    
    print of response:
    ActionList, len: 1
    
    print the object returned in JSON format:
    {
      "_type": "actions", 
      "action": [
        {
          "_type": "action", 
          "action_group": {
            "_type": "group", 
            "id": 0, 
            "name": "Default"
          }, 
          "approver": {
            "_type": "user", 
            "id": 2, 
            "name": "Tanium User"
          }, 
          "comment": "Distribute Tanium Standard Utilities", 
          "creation_time": "2015-08-07T19:46:14", 
          "distribute_seconds": 3200, 
          "expiration_time": "2015-08-07T20:41:16", 
          "expire_seconds": 3300, 
          "history_saved_question": {
            "_type": "saved_question", 
            "id": 102
          }, 
          "id": 60, 
          "name": "Distribute Tanium Standard Utilities", 
          "package_spec": {
            "_type": "package_spec", 
            "command": "cmd /c cscript install-standard-utils.vbs \"Tools\\StdUtils\"", 
            "id": 20, 
            "name": "Distribute Tanium Standard Utilities"
          }, 
          "saved_action": {
            "_type": "saved_action", 
            "id": 46
          }, 
          "skip_lock_flag": 0, 
          "start_time": "2015-08-07T19:46:16", 
          "status": "Open", 
          "stopped_flag": 0, 
          "target_group": {
            "_type": "group", 
            "id": 37, 
            "name": "Default"
          }, 
          "user": {
            "_type": "user", 
            "group_id": 0, 
            "id": 2, 
            "last_login": "2015-08-07T19:46:14", 
            "name": "Tanium User"
          }
        }
      ]
    }
