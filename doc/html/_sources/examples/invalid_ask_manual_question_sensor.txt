
Invalid ask manual question sensor
==========================================================================================
Ask a question using a sensor that does not exist

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
    kwargs["sensor_defs"] = u'Dweedle Dee and Dum'
    kwargs["qtype"] = u'manual'
    
    
    # call the handler with the ask method, passing in kwargs for arguments
    # this should throw an exception: pytan.utils.HandlerError
    import traceback
    try:
        handler.ask(**kwargs)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
    
    


Output from Python Code
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
    Traceback (most recent call last):
      File "<string>", line 39, in <module>
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 128, in ask
        result = getattr(self, q_obj_map['handler'])(**kwargs)
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 271, in ask_manual
        sensor_defs = self._get_sensor_defs(sensor_defs)
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1801, in _get_sensor_defs
        d['sensor_obj'] = self.get('sensor', **def_search)[0]
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1584, in get
        return self._get_multi(obj_map, **kwargs)
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1746, in _get_multi
        found = self._find(api_obj_multi, **kwargs)
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1711, in _find
        raise HandlerError(err(search_str))
    HandlerError: No results found searching for Sensor, name: u'Dweedle Dee and Dum'!!
