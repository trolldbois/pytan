
Ask manual human question sensor with filter and 3 options
==========================================================================================
Ask a manual question using human strings by referencing the name of a single sensor.

Also supply a sensor filter that limits the column data that is shown to values that contain Windows (which is short hand for regex match against .*Windows.*).

Also supply filter options that re-fetches any cached data that is older than 3600 seconds, matches all values supplied in the filter, and ignores case for any value match of the filter.

No sensor paramaters, question filters, or question options supplied.

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
    kwargs["sensors"] = u'Operating System, that contains:Windows, opt:match_all_values, opt:ignore_case, opt:max_data_age:3600'
    kwargs["qtype"] = u'manual_human'
    
    # call the handler with the ask method, passing in kwargs for arguments
    response = handler.ask(**kwargs)
    import pprint, io
    
    print ""
    print "Type of response: ", type(response)
    
    print ""
    print "Pretty print of response:"
    print pprint.pformat(response)
    
    print ""
    print "Equivalent Question if it were to be asked in the Tanium Console: "
    print response['question_object'].query_text
    
    # create an IO stream to store CSV results to
    out = io.BytesIO()
    
    # call the write_csv() method to convert response to CSV and store it in out
    response['question_results'].write_csv(out, response['question_results'])
    
    print ""
    print "CSV Results of response: "
    out = out.getvalue()
    if len(out.splitlines()) > 15:
        out = out.splitlines()[0:15]
        out.append('..trimmed for brevity..')
        out = '\n'.join(out)
    print out
    


Output from Python Code
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
    2014-12-08 16:24:40,124 INFO     question_progress: Results 0% (Get Operating System contains "Windows" from all machines)
    2014-12-08 16:24:45,141 INFO     question_progress: Results 50% (Get Operating System contains "Windows" from all machines)
    2014-12-08 16:24:50,158 INFO     question_progress: Results 100% (Get Operating System contains "Windows" from all machines)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'question_object': <taniumpy.object_types.question.Question object at 0x102130210>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x1021236d0>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Operating System contains "Windows" from all machines
    
    CSV Results of response: 
    Count,Operating System
    4,[no results]
    2,Windows Server 2008 R2 Standard
    
