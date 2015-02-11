
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
    2015-02-11 12:00:32,694 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2015-02-11 12:00:37,712 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2015-02-11 12:00:42,726 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2015-02-11 12:00:47,744 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2015-02-11 12:00:52,762 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2015-02-11 12:00:57,780 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2015-02-11 12:01:02,797 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2015-02-11 12:01:07,813 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2015-02-11 12:01:12,831 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2015-02-11 12:01:17,849 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2015-02-11 12:01:22,868 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2015-02-11 12:01:27,884 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2015-02-11 12:01:32,899 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2015-02-11 12:01:37,914 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2015-02-11 12:01:42,932 INFO     question_progress: Results 50% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2015-02-11 12:01:47,951 INFO     question_progress: Results 50% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    2015-02-11 12:01:52,968 INFO     question_progress: Results 100% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'question_object': <taniumpy.object_types.question.Question object at 0x105c2aa90>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x105b37c90>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Folder Name Search with RegEx Match[No, , No, ] from all machines
    
    CSV Results of response: 
    Count,"Folder Name Search with RegEx Match[No, , No, ]"
    23133,[too many results]
    1,C:\Windows\winsxs\amd64_microsoft-windows-s..structure.resources_31bf3856ad364e35_6.1.7600.16385_en-us_faf46e6f502e00e8
    1,C:\Windows\winsxs\x86_microsoft-windows-e..-host-authenticator_31bf3856ad364e35_6.1.7601.17514_none_a7c68343f07f776f
    1,C:\Windows\winsxs\amd64_microsoft-windows-ocspsvc_31bf3856ad364e35_6.1.7601.22807_none_3bfeae7293092e4b
    1,C:\Windows\winsxs\amd64_microsoft-windows-c..ityclient.resources_31bf3856ad364e35_6.1.7601.22865_en-us_c339d6d6cfb99c39
    1,C:\Windows\assembly\NativeImages_v2.0.50727_64\System.Xml
    1,C:\Windows\winsxs\amd64_microsoft-windows-scripting.resources_31bf3856ad364e35_6.1.7600.16385_en-us_e72192b67124ad43
    1,C:\Windows\winsxs\x86_microsoft-windows-mlang.resources_31bf3856ad364e35_6.1.7600.16385_ru-ru_cf3a10abc52740f6
    1,C:\Windows\winsxs\x86_microsoft-windows-directshow-dvdsupport_31bf3856ad364e35_6.1.7601.21987_none_566a88a44b6e5342
    1,C:\Windows\winsxs\amd64_microsoft-windows-ie-internetexplorer_31bf3856ad364e35_11.2.9600.17041_none_11e6f4b92ee9bf19
    1,C:\Users\Jim Olsen\AppData\Local\Google
    1,C:\Windows\winsxs\x86_microsoft-windows-e..nt-client.resources_31bf3856ad364e35_6.1.7600.16385_en-us_e5c3d3ec6ff64de3
    1,C:\Windows\winsxs\amd64_microsoft-windows-d..e-eashared-kjshared_31bf3856ad364e35_6.1.7600.16385_none_99b74194b7347cab
    1,C:\Windows\assembly\NativeImages_v4.0.30319_32\RadLangSvc
    ..trimmed for brevity..
