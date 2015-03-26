
Create group from json
==========================================================================================

Export a group object to a JSON file, adding ' API TEST' to the name of the group before exporting the JSON file and deleting any pre-existing group with the same (new) name, then create a new group object from the exported JSON file

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
    attr_name = "name"
    attr_add = " API TEST"
    
    # delete object before creating it?
    delete = True
    
    # setup the arguments for getting an object to export as json file
    get_kwargs = {}
    get_kwargs["objtype"] = u'group'
    get_kwargs["name"] = u'All Computers'
    
    
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
                del_kwargs['objtype'] = u'group'
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
    create_kwargs = {'objtype': u'group', 'json_file': json_file}
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
    2015-03-26 11:49:20,053 INFO     handler: Deleted 'Group, id: 19172'
    2015-03-26 11:49:20,054 INFO     handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/GroupList_2015_03_26-11_49_20-EDT.json' written with 383 bytes
    2015-03-26 11:49:20,103 INFO     handler: New Group, name: 'All Computers API TEST' (ID: 19224) created successfully!
    
    Type of response:  <class 'taniumpy.object_types.group_list.GroupList'>
    
    print of response:
    GroupList, len: 1
    
    print the object returned in JSON format:
    {
      "_type": "groups", 
      "group": [
        {
          "_type": "group", 
          "and_flag": 0, 
          "deleted_flag": 0, 
          "filters": {
            "_type": "filters", 
            "filter": []
          }, 
          "id": 19224, 
          "name": "All Computers API TEST", 
          "not_flag": 0, 
          "sub_groups": {
            "_type": "groups", 
            "group": []
          }, 
          "type": 0
        }
      ]
    }
