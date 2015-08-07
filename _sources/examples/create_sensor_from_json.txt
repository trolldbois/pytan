
Create sensor from json
==========================================================================================

Export a sensor object to a JSON file, adding ' API TEST' to the name of the sensor before exporting the JSON file and deleting any pre-existing sensor with the same (new) name, then create a new sensor object from the exported JSON file

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
    attr_name = "name"
    attr_add = " API TEST"
    
    # delete object before creating it?
    delete = True
    
    # setup the arguments for getting an object to export as json file
    get_kwargs = {}
    get_kwargs["objtype"] = u'sensor'
    get_kwargs["id"] = 381
    
    
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
                del_kwargs['objtype'] = u'sensor'
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
    create_kwargs = {'objtype': u'sensor', 'json_file': json_file}
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
    2015-08-07 19:46:14,551 INFO     pytan.handler: Deleted 'Sensor, id: 639'
    2015-08-07 19:46:14,551 INFO     pytan.handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/SensorList_2015_08_07-15_46_14-EDT.json' written with 1944 bytes
    2015-08-07 19:46:14,577 INFO     pytan.handler: New Sensor, name: 'Is Mac API TEST', id: 642 (ID: 642) created successfully!
    
    Type of response:  <class 'taniumpy.object_types.sensor_list.SensorList'>
    
    print of response:
    SensorList, len: 1
    
    print the object returned in JSON format:
    {
      "_type": "sensors", 
      "sensor": [
        {
          "_type": "sensor", 
          "category": "Operating System", 
          "creation_time": "2015-08-07T19:46:14", 
          "delimiter": ",", 
          "description": "Returns whether the machine is a Mac.  True if so, False if not.\nExample: True", 
          "exclude_from_parse_flag": 0, 
          "hash": 2387245230, 
          "hidden_flag": 0, 
          "id": 642, 
          "ignore_case_flag": 1, 
          "last_modified_by": "Tanium User", 
          "max_age_seconds": 86400, 
          "modification_time": "2015-08-07T19:46:14", 
          "name": "Is Mac API TEST", 
          "queries": {
            "_type": "queries", 
            "query": [
              {
                "_type": "query", 
                "platform": "Windows", 
                "script": "&#039;========================================\n&#039; Is Mac\n&#039;========================================\n\nWscript.echo &quot;False&quot;", 
                "script_type": "VBScript"
              }, 
              {
                "_type": "query", 
                "platform": "Linux", 
                "script": "#!/bin/bash\necho False\n", 
                "script_type": "UnixShell"
              }, 
              {
                "_type": "query", 
                "platform": "Mac", 
                "script": "#!/bin/bash\necho True\n", 
                "script_type": "UnixShell"
              }, 
              {
                "_type": "query", 
                "platform": "Solaris", 
                "script": "#!/bin/sh\n\n# THIS IS A STUB - NOT INTENDED AS FUNCTIONAL - NA\n# \n# \n\necho &quot;N/A on Solaris&quot;\n", 
                "script_type": "UnixShell"
              }, 
              {
                "_type": "query", 
                "platform": "AIX", 
                "script": "#!/bin/sh\n\n# THIS IS A STUB - NOT INTENDED AS FUNCTIONAL - NA\n# \n# \n\necho &quot;N/A on AIX&quot;\n", 
                "script_type": "UnixShell"
              }
            ]
          }, 
          "source_id": 0, 
          "string_count": 0, 
          "value_type": "String"
        }
      ]
    }
