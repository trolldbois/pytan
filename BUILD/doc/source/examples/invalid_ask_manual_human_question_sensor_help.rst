
Invalid ask manual human question sensor help
====================================================================================================
Have ask_manual_human() return the help for sensors

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
    kwargs["qtype"] = u'manual_human'
    kwargs["sensors_help"] = True
    
    
    # call the handler with the ask method, passing in kwargs for arguments
    # this should throw an exception: pytan.utils.PytanHelp
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
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 376, in ask_manual_human
        raise PytanHelp(utils.help_sensors())
    PytanHelp: 
    Sensors Help
    ============
    
    Supplying sensors controls what columns will be showed when you ask a
    question.
    
    A sensor string is a human string that describes, at a minimum, a sensor.
    It can also optionally define a selector for the sensor, parameters for
    the sensor, a filter for the sensor, and options for the filter for the
    sensor. Sensors can be provided as a string or a list of strings.
    
    Examples for basic sensors
    ---------------------------------
    
    Supplying a single sensor:
    
        'Computer Name'
    
    Supplying two sensors in a list of strings:
    
        ['Computer Name', 'IP Route Details']
    
    Supplying multiple sensors with selectors (name is the default
    selector if none is supplied):
    
        [
            'Computer Name',
            'name:Computer Name',
            'id:1',
            'hash:123456789',
        ]
    
    Sensor Parameters
    -----------------
    
    Supplying parameters to a sensor can control the arguments that are
    supplied to a sensor, if that sensor takes any arguments.
    
    Sensor parameters must be surrounded with curly braces '{}',
    and must have a key and value specified that is separated by
    an equals '='. Multiple parameters must be seperated by
    a comma ','. The key should match up to a valid parameter key
    for the sensor in question.
    
    If a parameter is supplied and the sensor doesn't have a
    corresponding key name, it will be ignored. If the sensor has
    parameters and a parameter is NOT supplied then one of two
    paths will be taken:
    
        * if the parameter does not require a default value, the
        parameter is left blank and not supplied.
        * if the parameter does require a value (pulldowns, for
        example), a default value is derived (for pulldowns,
        the first value available as a pulldown entry is used).
    
    Examples for sensors with parameters
    ------------------------------------
    
    Supplying a single sensor with a single parameter 'dirname':
    
        'Sensor With Params{dirname=Program Files}'
    
    Supplying a single sensor with two parameters, 'param1' and
    'param2':
    
        'Sensor With Params{param1=value1,param2=value2}'
    
    Sensor Filters
    --------------
    
    Supplying a filter to a sensor controls what data will be shown in
    those columns (sensors) you've provided.
    
    Sensor filters can be supplied by adding ', that FILTER:VALUE',
    where FILTER is a valid filter string, and VALUE is the string
    that you want FILTER to match on.
    
    See filter help for a list of all possible FILTER strings.
    
    See options help for a list of options that can control how
    the filter works.
    
    Examples for sensors with filters
    ---------------------------------
    
    Supplying a sensor with a filter that limits the results to only
    show column data that matches the regular expression
    '.*Windows.*' (Tanium does a case insensitive match by default):
    
        'Computer Name, that contains:Windows'
    
    Supplying a sensor with a filter that limits the results to only
    show column data that matches the regular expression
    'Microsoft.*':
    
        'Computer Name, that starts with:Microsoft'
    
    Supply a sensor with a filter that limits the results to only
    show column data that has a version greater or equal to
    '39.0.0.0'. Since this sensor uses Version as its default result
    type, there is no need to change the value type using filter
    options.
    
        'Installed Application Version' \
        '{Application Name=Google Chrome}, that =>:39.0.0.0'
    
    Sensor Options
    --------------
    
    Supplying options to a sensor can change how the filter for
    that sensor works.
    
    Sensor options can be supplied by adding ', opt:OPTION' or
    ', opt:OPTION:VALUE' for those options that require values,
    where OPTION is a valid option string, and VALUE is the
    appropriate value required by accordant OPTION.
    
    See options help for a list of options that can control how
    the filter works.
    
    Examples for sensors with options
    ---------------------------------
    
    Supplying a sensor with an option that forces tanium to
    re-fetch any cached column data that is older than 1 minute:
    
        'Computer Name, opt:max_data_age:60'
    
    Supplying a sensor with filter and an option that causes
    Tanium to match case for the filter value:
    
        'Computer Name, that contains:Windows, opt:match_case'
    
    Supplying a sensor with a filter and an option that causes
    Tanium to match all values supplied:
    
        'Computer Name, that contains:Windows, opt:match_all_values'
    
    Supplying a sensor with a filter and a set of options that
    causes Tanium to recognize the value type as String (which is
    the default type for most sensors), re-fetch data older than
    10 minutes, match any values, and match case:
    
        'Computer Name', that contains:Windows, ' \
        opt:value_type:string, opt:max_data_age:600, ' \
        'opt:match_any_value, opt:match_case'
    
