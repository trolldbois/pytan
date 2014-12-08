
Ask manual human question sensor with parameters and no supplied parameters
==========================================================================================
Ask a manual question using human strings by referencing the name of a single sensor that takes parameters, but not supplying any parameters (and letting pytan automatically determine the appropriate default value for those parameters which require a value).

No sensor filters, sensor parameters, sensor filter options, question filters, or question options supplied.

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
    kwargs["sensors"] = u'Folder Name Search with RegEx Match'
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
    2014-12-08 16:22:09,102 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2014-12-08 16:22:14,122 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2014-12-08 16:22:19,141 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2014-12-08 16:22:24,157 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2014-12-08 16:22:29,173 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2014-12-08 16:22:34,194 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2014-12-08 16:22:39,212 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2014-12-08 16:22:44,230 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2014-12-08 16:22:49,247 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2014-12-08 16:22:54,270 INFO     question_progress: Results 33% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2014-12-08 16:22:59,299 INFO     question_progress: Results 67% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2014-12-08 16:23:04,324 INFO     question_progress: Results 67% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2014-12-08 16:23:09,344 INFO     question_progress: Results 83% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2014-12-08 16:23:14,368 INFO     question_progress: Results 100% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'question_object': <taniumpy.object_types.question.Question object at 0x1021a5ad0>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x102b2e110>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Folder Name Search with RegEx Match[No, , No, ] from all machines
    
    CSV Results of response: 
    Count,"Folder Name Search with RegEx Match[No, , No, ]"
    40981,[too many results]
    2,C:\Windows\winsxs\amd64_microsoft-windows-s..structure.resources_31bf3856ad364e35_6.1.7600.16385_en-us_faf46e6f502e00e8
    2,C:\Windows\winsxs\x86_microsoft-windows-e..-host-authenticator_31bf3856ad364e35_6.1.7601.17514_none_a7c68343f07f776f
    1,C:\Windows\winsxs\amd64_microsoft-windows-ocspsvc_31bf3856ad364e35_6.1.7601.22807_none_3bfeae7293092e4b
    1,C:\Windows\winsxs\amd64_microsoft-windows-c..ityclient.resources_31bf3856ad364e35_6.1.7601.22865_en-us_c339d6d6cfb99c39
    1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_192\grep\share\locale\bg\LC_MESSAGES
    2,C:\Windows\assembly\NativeImages_v2.0.50727_64\System.Xml
    1,C:\Users\Jim Olsen\Desktop\SysinternalsSuite
    2,C:\Windows\winsxs\amd64_microsoft-windows-scripting.resources_31bf3856ad364e35_6.1.7600.16385_en-us_e72192b67124ad43
    2,C:\Windows\winsxs\x86_microsoft-windows-mlang.resources_31bf3856ad364e35_6.1.7600.16385_ru-ru_cf3a10abc52740f6
    1,C:\Windows\winsxs\x86_microsoft-windows-directshow-dvdsupport_31bf3856ad364e35_6.1.7601.21987_none_566a88a44b6e5342
    1,C:\Windows\winsxs\amd64_microsoft-windows-ie-internetexplorer_31bf3856ad364e35_11.2.9600.17041_none_11e6f4b92ee9bf19
    1,C:\Users\Jim Olsen\AppData\Local\Google
    2,C:\Windows\winsxs\x86_microsoft-windows-e..nt-client.resources_31bf3856ad364e35_6.1.7600.16385_en-us_e5c3d3ec6ff64de3
    ..trimmed for brevity..
