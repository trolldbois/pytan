
Ask manual human question complex query1
====================================================================================================
Ask a manual question using human strings by referencing the name of a two sensors sensor.

Supply 3 parameters for the second sensor, one of which is not a valid parameter (and will be ignored).

Supply one option to the second sensor.

Supply two question filters that limit the rows returned in the result to computers that match the sensor Operating System that contains Windows and does not contain Windows.

Supply two question options that 'or' the two question filters and ignore the case of any values while matching the question filters.

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
    kwargs["question_filters"] = [u'Operating System, that contains:Windows',
     u'Operating System, that does not contain:Windows']
    kwargs["sensors"] = [u'Computer Name',
     u'Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*, invalidparam=test}, that regex match:.*Shared.*, opt:max_data_age:3600']
    kwargs["question_options"] = [u'ignore_case', u'or']
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
    print out.getvalue()
    
    


Output from Python Code
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
    2014-12-08 15:13:29,990 INFO     question_progress: Results 0% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")
    2014-12-08 15:13:35,014 INFO     question_progress: Results 0% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")
    2014-12-08 15:13:40,039 INFO     question_progress: Results 33% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")
    2014-12-08 15:13:45,061 INFO     question_progress: Results 67% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")
    2014-12-08 15:13:50,083 INFO     question_progress: Results 83% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")
    2014-12-08 15:13:55,107 INFO     question_progress: Results 100% (Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows")
    
    Type of response:  <type 'dict'>
    
    Pretty print of response:
    {'question_object': <taniumpy.object_types.question.Question object at 0x10e539c50>,
     'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10e039a50>}
    
    Equivalent Question if it were to be asked in the Tanium Console: 
    Get Computer Name and Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines where Operating System contains "Windows" or any Operating System does not contain "Windows"
    
    CSV Results of response: 
    Computer Name,"Folder Name Search with RegEx Match[No, Program Files, No, ]"
    Casus-Belli.local,[no results]
    ubuntu.(none),[no results]
    localhost.(none),[no results]
    Jims-Mac.local,[no results]
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
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\oskmenu
    C:\Program Files\Common Files\Microsoft Shared\ink\ko-KR
    C:\Program Files\Common Files\Microsoft Shared\ink\it-IT
    C:\Program Files\Common Files\Microsoft Shared\Triedit
    C:\Program Files\Microsoft SQL Server\110\Shared
    C:\Program Files\Common Files\Microsoft Shared\ink\he-IL
    C:\Program Files\Common Files\Microsoft Shared\ink\ro-RO
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\oskpred
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\numbers
    C:\Program Files\Common Files\Microsoft Shared\ink\nb-NO
    C:\Program Files\Common Files\Microsoft Shared\ink\lv-LV
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\auxpad
    C:\Program Files\Common Files\Microsoft Shared\TextConv
    C:\Program Files\Common Files\Microsoft Shared\MSInfo\en-US
    C:\Program Files\Common Files\Microsoft Shared\ink\nl-NL
    C:\Program Files\Microsoft SQL Server\90\Shared\Resources\1033
    C:\Program Files\Common Files\Microsoft Shared\ink\fr-FR
    C:\Program Files\Common Files\Microsoft Shared\ink\tr-TR
    C:\Program Files\Common Files\Microsoft Shared\VC
    C:\Program Files\Common Files\Microsoft Shared\WF
    C:\Program Files\Microsoft SQL Server\110\Shared\en
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\symbols
    C:\Program Files\Common Files\Microsoft Shared\ink\lt-LT
    C:\Program Files\Common Files\Microsoft Shared\ink\et-EE
    C:\Program Files\Common Files\Microsoft Shared\ink\cs-CZ
    C:\Program Files\Microsoft SQL Server\110\Shared\VS2008
    C:\Program Files\Common Files\Microsoft Shared\ink\en-US
    C:\Program Files\Common Files\Microsoft Shared\ink\bg-BG
    C:\Program Files\Microsoft SQL Server\100\Shared
    C:\Program Files\Common Files\Microsoft Shared\ink\es-ES
    C:\Program Files\Common Files\Microsoft Shared\MSInfo
    C:\Program Files\Microsoft SQL Server\110\Shared\RsFxInstall
    C:\Program Files\Common Files\Microsoft Shared\WF\amd64
    C:\Program Files\Common Files\Microsoft Shared\ink\de-DE
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\main
    C:\Program Files\Microsoft SQL Server\90\Shared\Resources
    C:\Program Files\Common Files\Microsoft Shared\ink\sr-Latn-CS
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\osknumpad
    C:\Program Files\Microsoft SQL Server\110\Shared\Resources\1033
    C:\Program Files\Common Files\Microsoft Shared\MSEnv
    C:\Program Files\Microsoft SQL Server\110\Shared\VS2008\1033
    C:\Program Files\Common Files\Microsoft Shared\ink\pt-BR
    C:\Program Files\Common Files\Microsoft Shared\ink\pt-PT
    C:\Program Files\Common Files\Microsoft Shared\ink\el-GR
    C:\Program Files\Microsoft SQL Server\110\Shared\Resources
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\web
    C:\Program Files\Common Files\Microsoft Shared\ink\ja-JP
    C:\Program Files\Common Files\Microsoft Shared\ink\sk-SK
    C:\Program Files\Common Files\Microsoft Shared\ink\hr-HR
    C:\Program Files\Common Files\Microsoft Shared\VGX
    C:\Program Files\Common Files\Microsoft Shared\Triedit\en-US
    C:\Program Files\Common Files\Microsoft Shared\TextConv\en-US
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions
    C:\Program Files\Common Files\Microsoft Shared\ink\th-TH
    C:\Program Files\Common Files\Microsoft Shared\SQL Debugging
    C:\Program Files\Microsoft SQL Server\90\Shared
    C:\Program Files\Common Files\Microsoft Shared\ink\pl-PL
    C:\Program Files\Common Files\Microsoft Shared\Stationery
    C:\Program Files\Common Files\Microsoft Shared\VS7Debug\1033
    C:\Program Files\Microsoft SQL Server\110\Shared\ErrorDumps"
    WIN-A12SC6N6T7Q,"C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
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
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\oskmenu
    C:\Program Files\Common Files\Microsoft Shared\ink\ko-KR
    C:\Program Files\Common Files\Microsoft Shared\ink\it-IT
    C:\Program Files\Common Files\Microsoft Shared\Triedit
    C:\Program Files\Common Files\Microsoft Shared\ink\he-IL
    C:\Program Files\Common Files\Microsoft Shared\ink\ro-RO
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\oskpred
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\numbers
    C:\Program Files\Common Files\Microsoft Shared\ink\nb-NO
    C:\Program Files\Common Files\Microsoft Shared\ink\lv-LV
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\auxpad
    C:\Program Files\Common Files\Microsoft Shared\TextConv
    C:\Program Files\Common Files\Microsoft Shared\MSInfo\en-US
    C:\Program Files\Common Files\Microsoft Shared\ink\nl-NL
    C:\Program Files\Common Files\Microsoft Shared\ink\fr-FR
    C:\Program Files\Common Files\Microsoft Shared\ink\tr-TR
    C:\Program Files\Common Files\Microsoft Shared\VC
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\symbols
    C:\Program Files\Common Files\Microsoft Shared\ink\lt-LT
    C:\Program Files\Common Files\Microsoft Shared\ink\et-EE
    C:\Program Files\Common Files\Microsoft Shared\ink\cs-CZ
    C:\Program Files\Common Files\Microsoft Shared\ink\en-US
    C:\Program Files\Common Files\Microsoft Shared\ink\bg-BG
    C:\Program Files\Common Files\Microsoft Shared\ink\es-ES
    C:\Program Files\Common Files\Microsoft Shared\MSInfo
    C:\Program Files\Common Files\Microsoft Shared\ink\de-DE
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\main
    C:\Program Files\Common Files\Microsoft Shared\ink\sr-Latn-CS
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\osknumpad
    C:\Program Files\Common Files\Microsoft Shared\ink\pt-BR
    C:\Program Files\Common Files\Microsoft Shared\ink\pt-PT
    C:\Program Files\Common Files\Microsoft Shared\ink\el-GR
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\web
    C:\Program Files\Common Files\Microsoft Shared\ink\ja-JP
    C:\Program Files\Common Files\Microsoft Shared\ink\sk-SK
    C:\Program Files\Common Files\Microsoft Shared\ink\hr-HR
    C:\Program Files\Common Files\Microsoft Shared\VGX
    C:\Program Files\Common Files\Microsoft Shared\Triedit\en-US
    C:\Program Files\Common Files\Microsoft Shared\TextConv\en-US
    C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions
    C:\Program Files\Common Files\Microsoft Shared\ink\th-TH
    C:\Program Files\Common Files\Microsoft Shared\ink\pl-PL
    C:\Program Files\Common Files\Microsoft Shared\Stationery"
    
