
Ask manual question sensor complex
==========================================================================================

This provides an example for asking a manual question without using human strings.

It uses the Computer Name and Folder Name Search with RegEx Match sensors.

The second sensor has a single parameter, dirname, with a value of 'Program Files'.

The second sensor also has 3 sensor filter options that set the max data age to 3600 seconds, does NOT ignore case, and treats all values as string.

There is also a question filter supplied that limits the rows that are displayed to computers that match an Operating System that contains Windows, and has 3 question filter options supplied that set the max data age to 3600 seconds, does NOT ignore case, and uses 'and' to join all question filters.

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
    kwargs["question_filter_defs"] = [{u'filter': {u'not_flag': 0,
                  u'operator': u'RegexMatch',
                  u'value': u'.*Windows.*'},
      u'name': u'Operating System'}]
    kwargs["sensor_defs"] = [u'Computer Name',
     {u'filter': {u'not_flag': 0,
                  u'operator': u'RegexMatch',
                  u'value': u'.*Shared.*'},
      u'name': u'Folder Name Search with RegEx Match',
      u'options': {u'ignore_case_flag': 0,
                   u'max_age_seconds': 3600,
                   u'value_type': u'string'},
      u'params': {u'dirname': u'Program Files'}}]
    kwargs["question_option_defs"] = {u'and_flag': 0, u'ignore_case_flag': 0, u'max_age_seconds': 3600}
    kwargs["qtype"] = u'manual'
    
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
    2015-03-26 11:45:18,920 INFO     question_progress: Results 0% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" matching case from all machines where Operating System contains "Windows" matching case)
    2015-03-26 11:45:23,943 INFO     question_progress: Results 0% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" matching case from all machines where Operating System contains "Windows" matching case)
    2015-03-26 11:45:28,969 INFO     question_progress: Results 50% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" matching case from all machines where Operating System contains "Windows" matching case)
    2015-03-26 11:45:33,994 INFO     question_progress: Results 50% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" matching case from all machines where Operating System contains "Windows" matching case)
    2015-03-26 11:45:39,017 INFO     question_progress: Results 100% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" matching case from all machines where Operating System contains "Windows" matching case)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'question_object': <taniumpy.object_types.question.Question object at 0x10757d750>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x107805e50>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" matching case from all machines where Operating System contains "Windows" matching case
    
    CSV Results of response: 
    Computer Name,"Folder Name Search with RegEx Match[No, Program Files, No, ]"
    jtanium1.localdomain,"C:\Program Files\Common Files\Microsoft Shared\VS7Debug
    C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
    C:\Program Files\Common Files\Microsoft Shared\ink\ru-RU
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\keypad
    C:\Program Files\Common Files\Microsoft Shared\ink
    C:\Program Files\Common Files\Microsoft Shared\ink\sv-SE
    C:\Program Files\Common Files\Microsoft Shared\ink\uk-UA
    C:\Program Files\Common Files\Microsoft Shared\ink\sl-SI
    C:\Program Files\Common Files\Microsoft Shared\ink\hu-HU
    C:\Program Files\Common Files\Microsoft Shared\ink\zh-TW
    C:\Program Files\Common Files\Microsoft Shared\ink\zh-CN
    C:\Program Files\Common Files\Microsoft Shared\ink\fi-FI
    C:\Program Files\Common Files\Microsoft Shared
    C:\Program Files\Common Files\Microsoft Shared\ink\da-DK
    ..trimmed for brevity..
