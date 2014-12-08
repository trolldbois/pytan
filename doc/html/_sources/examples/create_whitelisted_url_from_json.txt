
Create whitelisted url from json
====================================================================================================
Export a whitelisted url object to a JSON file, adding ' test1' to the url_regex of the whitelisted url before exporting the JSON file and deleting any pre-existing whitelisted url with the same (new) name, then create a new whitelisted url object from the exported JSON file

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
    attr_name = "url_regex"
    attr_add = " API TEST"
    
    # delete object before creating it?
    delete = True
    
    # setup the arguments for getting an object to export as json file
    get_kwargs = {}
    get_kwargs["objtype"] = u'whitelisted_url'
    get_kwargs["url_regex"] = u'test1'
    
    
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
                del_kwargs['objtype'] = u'whitelisted_url'
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
    create_kwargs = {'objtype': u'whitelisted_url', 'json_file': json_file}
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
    2014-12-07 01:12:11,652 INFO     handler: Deleted 'WhiteListedUrl, id: 16'
    2014-12-07 01:12:11,653 INFO     handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/WhiteListedUrlList_2014_12_07-01_12_11-EST.json' written with 198 bytes
    2014-12-07 01:12:11,664 INFO     handler: New WhiteListedUrl, id: 18 (ID: 18) created successfully!
    
    Type of response:  <class 'taniumpy.object_types.white_listed_url_list.WhiteListedUrlList'>
    
    print of response:
    WhiteListedUrlList, len: 1
    
    print the object returned in JSON format:
    {
      "_type": "white_listed_urls", 
      "white_listed_url": [
        {
          "_type": "white_listed_url", 
          "download_seconds": 86400, 
          "id": 18, 
          "url_regex": "test1 API TEST"
        }
      ]
    }
