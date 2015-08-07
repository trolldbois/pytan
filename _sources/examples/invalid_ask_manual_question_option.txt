
Invalid ask manual question option
==========================================================================================

Ask a question using an invalid option.

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
    
    # setup the arguments for the handler method
    kwargs = {}
    kwargs["sensors"] = u'Operating system, opt:bad'
    kwargs["qtype"] = u'manual'
    
    
    # call the handler with the ask method, passing in kwargs for arguments
    # this should throw an exception: pytan.exceptions.HumanParserError
    import traceback
    try:
        handler.ask(**kwargs)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
    
    


Output from Python Code
----------------------------------------------------------------------------------------

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
    Traceback (most recent call last):
      File "<string>", line 55, in <module>
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 130, in ask
        result = getattr(self, q_obj_map['handler'])(**kwargs)
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 297, in ask_manual
        sensor_defs = pytan.utils.dehumanize_sensors(sensors)
      File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 1477, in dehumanize_sensors
        s, parsed_options = extract_options(s)
      File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 1721, in extract_options
        parsed_options = map_options(parsed_options, ['filter'])
      File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 1751, in map_options
        raise pytan.exceptions.HumanParserError(err(option))
    HumanParserError: Option u'bad' is not a valid option!
