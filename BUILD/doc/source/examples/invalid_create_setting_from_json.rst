
Invalid create setting from json
==========================================================================================

Create a setting from json (not supported!)

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
    
    # setup the arguments for getting an object to export as json file
    get_kwargs = {}
    get_kwargs["objtype"] = u'setting'
    get_kwargs["id"] = 1
    
    # get objects to use as an export to JSON file
    orig_objs = handler.get(**get_kwargs)
    
    # export orig_objs to a json file
    json_file, results = handler.export_to_report_file(
        obj=orig_objs,
        export_format='json',
        report_dir=tempfile.gettempdir(),
    )
    
    # call the handler with the create_from_json method, passing in kwargs for arguments
    # this should throw an exception: pytan.exceptions.HandlerError
    import traceback
    
    # create the object from the exported JSON file
    create_kwargs = {'objtype': u'setting', 'json_file': json_file}
    try:
        response = handler.create_from_json(**create_kwargs)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
    
    


Output from Python Code
----------------------------------------------------------------------------------------

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
    2015-08-06 14:56:11,180 INFO     pytan.handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/SystemSettingList_2015_08_06-10_56_11-EDT.json' written with 327 bytes
    Traceback (most recent call last):
      File "<string>", line 67, in <module>
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 547, in create_from_json
        raise pytan.exceptions.HandlerError(m(objtype, json_createable))
    HandlerError: setting is not a json createable object! Supported objects: user, whitelisted_url, saved_question, group, package, question, action, sensor
