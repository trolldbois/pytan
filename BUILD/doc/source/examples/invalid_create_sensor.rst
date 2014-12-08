
Invalid create sensor
====================================================================================================
Create a sensor (Unsupported!)

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
    
    
    # call the handler with the create_sensor method, passing in kwargs for arguments
    # this should throw an exception: pytan.utils.HandlerError
    import traceback
    try:
        handler.create_sensor(**kwargs)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
    
    


Output from Python Code
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
    Traceback (most recent call last):
      File "<string>", line 37, in <module>
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 537, in create_sensor
        raise HandlerError(m)
    HandlerError: Sensor creation not supported via PyTan as of yet, too complex
    Use create_sensor_from_json() instead!
