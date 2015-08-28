
Invalid ask manual question sensor
==========================================================================================

Ask a question using a sensor that does not exist

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
    kwargs["sensors"] = u'Dweedle Dee and Dum'
    kwargs["qtype"] = u'manual'
    
    
    # call the handler with the ask method, passing in kwargs for arguments
    # this should throw an exception: pytan.exceptions.HandlerError
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
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 305, in ask_manual
        **kwargs
      File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2699, in wrap
        ret = f(*args, **kwargs)
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1882, in _ask_manual
        sensor_defs = self._get_sensor_defs(sensor_defs)
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1418, in _get_sensor_defs
        d['sensor_obj'] = self.get('sensor', **def_search)[0]
      File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2699, in wrap
        ret = f(*args, **kwargs)
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1250, in get
        return self._get_multi(obj_map, **kwargs)
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1363, in _get_multi
        found = self._find(api_obj_multi, **kwargs)
      File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2699, in wrap
        ret = f(*args, **kwargs)
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1327, in _find
        raise pytan.exceptions.HandlerError(err(search_str))
    HandlerError: No results found searching for Sensor, name: u'Dweedle Dee and Dum'!!
