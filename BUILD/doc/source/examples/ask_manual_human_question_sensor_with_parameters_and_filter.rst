
Ask manual human question sensor with parameters and filter
==========================================================================================

Ask a manual question using human strings by referencing the name of a single sensor that takes parameters, but supplying only two of the four parameters that are used by the sensor.

Also supply a sensor filter that limits the column data that is shown to values that match the regex '.*Shared.*'.

No sensor filter options, question filters, or question options supplied.

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
    
    # setup the arguments for the handler method
    kwargs = {}
    kwargs["sensors"] = u'Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*}, that regex match:.*Shared.*'
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
----------------------------------------------------------------------------------------

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
    2015-03-26 11:42:36,899 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] contains "Shared" from all machines)
    2015-03-26 11:42:41,918 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] contains "Shared" from all machines)
    2015-03-26 11:42:46,933 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] contains "Shared" from all machines)
    2015-03-26 11:42:51,950 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] contains "Shared" from all machines)
    2015-03-26 11:42:56,970 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] contains "Shared" from all machines)
    2015-03-26 11:43:01,988 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] contains "Shared" from all machines)
    2015-03-26 11:43:07,011 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] contains "Shared" from all machines)
    2015-03-26 11:43:12,029 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] contains "Shared" from all machines)
    2015-03-26 11:43:17,053 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] contains "Shared" from all machines)
    2015-03-26 11:43:22,076 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] contains "Shared" from all machines)
    2015-03-26 11:43:27,096 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] contains "Shared" from all machines)
    2015-03-26 11:43:32,118 INFO     question_progress: Results 100% (Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] contains "Shared" from all machines)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'question_object': <taniumpy.object_types.question.Question object at 0x1075b84d0>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10761bc10>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*] contains "Shared" from all machines
    
    CSV Results of response: 
    "Folder Name Search with RegEx Match[No, Program Files, No, , Microsoft.*]"
    [no results]
    C:\Program Files\Common Files\Microsoft Shared\VS7Debug
    C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
    C:\Program Files\Common Files\Microsoft Shared\ink\ru-RU
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\keypad
    C:\Program Files\Common Files\Microsoft Shared\ink
    C:\Program Files\Common Files\Microsoft Shared\ink\sv-SE
    C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\Update Cache\KB2977326\GDR\1033_enu_lp\x64\setup\sqlsupport_msi\pfiles32\sqlservr\110\shared
    C:\Program Files\Common Files\Microsoft Shared\ink\uk-UA
    C:\Program Files\Common Files\Microsoft Shared\ink\sl-SI
    C:\Program Files\Common Files\Microsoft Shared\ink\hu-HU
    C:\Program Files\Common Files\Microsoft Shared\ink\zh-TW
    C:\Program Files\Common Files\Microsoft Shared\ink\zh-CN
    C:\Program Files\Common Files\Microsoft Shared\ink\fi-FI
    ..trimmed for brevity..
