
Create package from json
====================================================================================================
Export a package object to a JSON file, adding ' API TEST' to the name of the package before exporting the JSON file and deleting any pre-existing package with the same (new) name, then create a new package object from the exported JSON file

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
    
    # set the attribute name and value we want to add to the original object (if any)
    attr_name = "name"
    attr_add = " API TEST"
    
    # delete object before creating it?
    delete = True
    
    # setup the arguments for getting an object to export as json file
    get_kwargs = {}
    get_kwargs["objtype"] = u'package'
    get_kwargs["id"] = 31
    
    
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
                del_kwargs['objtype'] = u'package'
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
    create_kwargs = {'objtype': u'package', 'json_file': json_file}
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
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
    2014-12-07 01:12:11,257 INFO     handler: Deleted 'PackageSpec, id: 108'
    2014-12-07 01:12:11,258 INFO     handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/PackageSpecList_2014_12_07-01_12_11-EST.json' written with 1833 bytes
    2014-12-07 01:12:11,280 INFO     handler: New PackageSpec, name: 'Custom Tagging - Add Tags API TEST' (ID: 111) created successfully!
    
    Type of response:  <class 'taniumpy.object_types.package_spec_list.PackageSpecList'>
    
    print of response:
    PackageSpecList, len: 1
    
    print the object returned in JSON format:
    {
      "_type": "package_specs", 
      "package_spec": [
        {
          "_type": "package_spec", 
          "available_time": "1900-01-01T00:00:00", 
          "command": "cmd /c cscript //T:60 add-tags.vbs \"$1\"", 
          "command_timeout": 60, 
          "creation_time": "2014-12-07T06:12:11", 
          "deleted_flag": 0, 
          "display_name": "Custom Tagging - Add Tags", 
          "expire_seconds": 660, 
          "hidden_flag": 0, 
          "id": 111, 
          "last_modified_by": "Tanium User", 
          "last_update": "2014-12-07T06:12:11", 
          "metadata": {
            "_type": "metadata", 
            "item": [
              {
                "_type": "item", 
                "admin_flag": 0, 
                "name": "defined", 
                "value": "Tanium"
              }, 
              {
                "_type": "item", 
                "admin_flag": 0, 
                "name": "category", 
                "value": "Tanium"
              }
            ]
          }, 
          "modification_time": "2014-12-07T06:12:11", 
          "name": "Custom Tagging - Add Tags API TEST", 
          "parameter_definition": "{\"parameters\":[{\"restrict\":null,\"validationExpressions\":[{\"flags\":\"\",\"expression\":\"\\\\S\",\"helpString\":\"You must enter a value\",\"model\":\"com.tanium.models::ValidationExpression\",\"parameterType\":\"com.tanium.models::ValidationExpression\"}],\"helpString\":\"Enter tags space-delimited.\",\"value\":\"\",\"promptText\":\"e.g. PCI DMZ Decomm\",\"defaultValue\":\"\",\"label\":\"Add tags (space-delimited)\",\"maxChars\":0,\"key\":\"$1\",\"model\":\"com.tanium.components.parameters::TextInputParameter\",\"parameterType\":\"com.tanium.components.parameters::TextInputParameter\"}],\"model\":\"com.tanium.components.parameters::ParametersArray\",\"parameterType\":\"com.tanium.components.parameters::ParametersArray\"}", 
          "source_id": 0, 
          "verify_group_id": 0
        }
      ]
    }
