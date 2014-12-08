
Ask manual human question sensor with parameters and some supplied parameters
==========================================================================================
Ask a manual question using human strings by referencing the name of a single sensor that takes parameters, but supplying only two of the four parameters that are used by the sensor (and letting pytan automatically determine the appropriate default value for those parameters which require a value and none was supplied).

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
    kwargs["sensors"] = u'Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*}'
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
    2014-12-08 16:20:23,296 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
    2014-12-08 16:20:28,314 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
    2014-12-08 16:20:33,331 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
    2014-12-08 16:20:38,351 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
    2014-12-08 16:20:43,372 INFO     question_progress: Results 17% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
    2014-12-08 16:20:48,394 INFO     question_progress: Results 83% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
    2014-12-08 16:20:53,410 INFO     question_progress: Results 100% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'question_object': <taniumpy.object_types.question.Question object at 0x102b6fd90>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x102bb1810>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines
    
    CSV Results of response: 
    Count,"Folder Name Search with RegEx Match[No, Program Files, No, ]"
    1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\cgi-bin
    2,C:\Program Files\VMware\VMware Tools\plugins\vmsvc
    1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1040_ITA_LP\x64\1040\help
    1,C:\Program Files\Common Files\Microsoft Shared\VS7Debug
    1,C:\Program Files\Tanium\Tanium Server\Apache24\manual\style
    1,C:\Program Files\Tanium\Tanium Server\Apache24\htdocs\console\history
    2,C:\Program Files\Common Files\VMware\Drivers\vmci\sockets\include
    2,C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
    1,C:\Program Files\Tanium\Tanium Server\plugins\console\Dashboards
    1,C:\Program Files\Tanium\Tanium Server\CertificateBackup2014-11-17-11-17-33
    2,C:\Program Files\Common Files\SpeechEngines\Microsoft
    1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\modules
    2,C:\Program Files\Common Files\Microsoft Shared\ink\ru-RU
    1,C:\Program Files\Microsoft SQL Server\110\DTS\ForEachEnumerators\en
    ..trimmed for brevity..
