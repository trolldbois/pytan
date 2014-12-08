
Export basetype json type false
====================================================================================================
Export a BaseType from getting objects as JSON with false for include_type

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
    
    # setup the export_obj kwargs for later
    export_kwargs = {}
    export_kwargs["export_format"] = u'json'
    export_kwargs["include_type"] = False
    
    # get the objects that will provide the basetype that we want to use
    get_kwargs = {
        'name': [
            "Computer Name", "IP Route Details", "IP Address",
            'Folder Name Search with RegEx Match',
        ],
        'objtype': 'sensor',
    }
    response = handler.get(**get_kwargs)
    
    # export the object to a string
    # (we could just as easily export to a file using export_to_report_file)
    export_kwargs['obj'] = response
    export_str = handler.export_obj(**export_kwargs)
    
    
    print ""
    print "print the export_str returned from export_obj():"
    print export_str
    


Output from Python Code
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
    
    print the export_str returned from export_obj():
    {
      "sensor": [
        {
          "category": "Reserved", 
          "description": "The assigned name of the client machine.\nExample: workstation-1.company.com", 
          "exclude_from_parse_flag": 0, 
          "hash": 3409330187, 
          "hidden_flag": 0, 
          "id": 3, 
          "ignore_case_flag": 1, 
          "max_age_seconds": 86400, 
          "name": "Computer Name", 
          "queries": {
            "query": [
              {
                "platform": "Windows", 
                "script": "select CSName from win32_operatingsystem", 
                "script_type": "WMIQuery"
              }
            ]
          }, 
          "source_id": 0, 
          "string_count": 7, 
          "value_type": "String"
        }, 
        {
          "category": "Network", 
          "creation_time": "2014-12-06T18:00:24", 
          "delimiter": "|", 
          "description": "Returns IPv4 network routes, filtered to exclude noise. With Flags, Metric, Interface columns.\nExample:  172.16.0.0|192.168.1.1|255.255.0.0|UG|100|eth0", 
          "exclude_from_parse_flag": 1, 
          "hash": 435227963, 
          "hidden_flag": 0, 
          "id": 737, 
          "ignore_case_flag": 1, 
          "last_modified_by": "Jim Olsen", 
          "max_age_seconds": 60, 
          "metadata": {
            "item": [
              {
                "admin_flag": 0, 
                "name": "defined", 
                "value": "Tanium"
              }
            ]
          }, 
          "modification_time": "2014-12-06T18:00:24", 
          "name": "IP Route Details", 
          "queries": {
            "query": [
              {
                "platform": "Windows", 
                "script": "strComputer = &quot;.&quot;\nSet objWMIService = GetObject(&quot;winmgmts:&quot; _\n    &amp; &quot;{impersonationLevel=impersonate}!\\\\&quot; &amp; strComputer &amp; &quot;\\root\\cimv2&quot;)\n\nSet collip = objWMIService.ExecQuery(&quot;select * from win32_networkadapterconfiguration where IPEnabled=&#039;True&#039;&quot;)\ndim ipaddrs()\nipcount = 0\nfor each ipItem in collip\n    for each ipaddr in ipItem.IPAddress\n        ipcount = ipcount + 1\n    next\nnext\nredim ipaddrs(ipcount)\nipcount = 0\nfor each ipItem in collip\n    for each ipaddr in ipItem.IPAddress\n        ipcount = ipcount + 1\n        ipaddrs(ipcount) = ipaddr\n    next\nnext\nlocalhost = &quot;127.0.0.1&quot;\n\nSet colItems = objWMIService.ExecQuery(&quot;Select * from Win32_IP4RouteTable&quot;)\n\nFor Each objItem in colItems\n    dest = objItem.Destination\n    gw = objItem.NextHop\n    mask = objItem.Mask\n    metric = objItem.Metric1\n    flags = objItem.Type\n    intf = objItem.InterfaceIndex\n    For i = 0 to ipcount\n        if gw = ipaddrs(i) and gw &lt;&gt; localhost then\n            gw = &quot;0.0.0.0&quot;\n        end if\n    Next\n    if gw &lt;&gt; localhost and dest &lt;&gt; &quot;224.0.0.0&quot; and right(dest,3) &lt;&gt; &quot;255&quot; then\n        Wscript.Echo dest &amp; &quot;|&quot; &amp; gw &amp; &quot;|&quot; &amp; mask &amp; &quot;|&quot; &amp; &quot;-&quot; &amp; &quot;|&quot; &amp; metric &amp; &quot;|&quot; &amp; &quot;-&quot;\n    end if\nNext", 
                "script_type": "VBScript"
              }, 
              {
                "platform": "Linux", 
                "script": "route -n | grep -v Kernel | grep -v Destination | awk &#039;{ print $1 &quot;|&quot; $2 &quot;|&quot; $3 &quot;|&quot; $4 &quot;|&quot; $5 &quot;|&quot; $8 }&#039; | grep -v &quot;|127.0.0.1|&quot;\n", 
                "script_type": "UnixShell"
              }, 
              {
                "platform": "Mac", 
                "script": "netstat -rn | grep -v &quot;:&quot; | grep -v Destination | grep -v Routing | grep -v -e &quot;^$&quot; | awk &#039;{ print $1 &quot;|&quot; $2 &quot;||&quot; $3 &quot;||&quot; $6 }&#039; | grep -v &quot;|127.0.0.1|&quot;\n", 
                "script_type": "UnixShell"
              }
            ]
          }, 
          "source_id": 0, 
          "string_count": 48, 
          "subcolumns": {
            "subcolumn": [
              {
                "hidden_flag": 0, 
                "ignore_case_flag": 1, 
                "index": 0, 
                "name": "Destination", 
                "value_type": "IPAddress"
              }, 
              {
                "hidden_flag": 0, 
                "ignore_case_flag": 1, 
                "index": 1, 
                "name": "Gateway", 
                "value_type": "IPAddress"
              }, 
              {
                "hidden_flag": 0, 
                "ignore_case_flag": 1, 
                "index": 2, 
                "name": "Mask", 
                "value_type": "String"
              }, 
              {
                "hidden_flag": 0, 
                "ignore_case_flag": 1, 
                "index": 3, 
                "name": "Flags", 
                "value_type": "String"
              }, 
              {
                "hidden_flag": 0, 
                "ignore_case_flag": 1, 
                "index": 4, 
                "name": "Metric", 
                "value_type": "NumericInteger"
              }, 
              {
                "hidden_flag": 0, 
                "ignore_case_flag": 1, 
                "index": 5, 
                "name": "Interface", 
                "value_type": "String"
              }
            ]
          }, 
          "value_type": "String"
        }, 
        {
          "category": "Network", 
          "creation_time": "2014-12-06T18:00:22", 
          "delimiter": ",", 
          "description": "Current IP Addresses of client machine.\nExample: 192.168.1.1", 
          "exclude_from_parse_flag": 1, 
          "hash": 3209138996, 
          "hidden_flag": 0, 
          "id": 147, 
          "ignore_case_flag": 1, 
          "last_modified_by": "Jim Olsen", 
          "max_age_seconds": 600, 
          "metadata": {
            "item": [
              {
                "admin_flag": 0, 
                "name": "defined", 
                "value": "Tanium"
              }
            ]
          }, 
          "modification_time": "2014-12-06T18:00:22", 
          "name": "IP Address", 
          "queries": {
            "query": [
              {
                "platform": "Windows", 
                "script": "select IPAddress from win32_networkadapterconfiguration where IPEnabled=&#039;True&#039;", 
                "script_type": "WMIQuery"
              }, 
              {
                "platform": "Linux", 
                "script": "#!/bin/bash\nifconfig | grep -w inet | grep -v 127.0.0.1 | awk &#039;{print $2}&#039; | sed -e &#039;s/addr://&#039;\n", 
                "script_type": "UnixShell"
              }, 
              {
                "platform": "Mac", 
                "script": "#!/bin/bash\n\nifconfig -a -u |grep &quot;inet&quot; | grep -v &quot;::1&quot; | grep -v &quot;127.0.0.1&quot;| awk &#039;{print $2}&#039; | cut -f1 -d&#039;%&#039;\n", 
                "script_type": "UnixShell"
              }
            ]
          }, 
          "source_id": 0, 
          "string_count": 86, 
          "value_type": "IPAddress"
        }, 
        {
          "category": "File System", 
          "creation_time": "2014-12-06T18:00:23", 
          "delimiter": ",", 
          "description": "Finds the specified folder and provides the full path if the folder exists on the client machine. Takes regular expression to match.\nExample: C:\\WINDOWS\\System32", 
          "exclude_from_parse_flag": 1, 
          "hash": 1374547302, 
          "hidden_flag": 0, 
          "id": 381, 
          "ignore_case_flag": 1, 
          "last_modified_by": "Jim Olsen", 
          "max_age_seconds": 600, 
          "metadata": {
            "item": [
              {
                "admin_flag": 0, 
                "name": "defined", 
                "value": "McAfee"
              }
            ]
          }, 
          "modification_time": "2014-12-06T18:00:23", 
          "name": "Folder Name Search with RegEx Match", 
          "parameter_definition": "{\"parameters\":[{\"restrict\":null,\"validationExpressions\":[{\"flags\":\"\",\"expression\":\"\\\\S{3}\",\"helpString\":\"Value must be at least 3 characters\",\"model\":\"com.tanium.models::ValidationExpression\",\"parameterType\":\"com.tanium.models::ValidationExpression\"}],\"helpString\":\"Enter the folder name to search for\",\"value\":\"\",\"promptText\":\"e.g Program Files\",\"defaultValue\":\"\",\"label\":\"Search for Folder Name\",\"maxChars\":0,\"key\":\"dirname\",\"model\":\"com.tanium.components.parameters::TextInputParameter\",\"parameterType\":\"com.tanium.components.parameters::TextInputParameter\"},{\"restrict\":null,\"validationExpressions\":[{\"flags\":\"\",\"expression\":\"\\\\S{3}\",\"helpString\":\"Value must be at least 3 characters\",\"model\":\"com.tanium.models::ValidationExpression\",\"parameterType\":\"com.tanium.models::ValidationExpression\"}],\"helpString\":\"Enter the regular expression to search for.\",\"value\":\"\",\"promptText\":\"e.g. test*.exe\",\"defaultValue\":\"\",\"label\":\"Regular Expression\",\"maxChars\":0,\"key\":\"regexp\",\"model\":\"com.tanium.components.parameters::TextInputParameter\",\"parameterType\":\"com.tanium.components.parameters::TextInputParameter\"},{\"helpString\":\"Enter Yes/No for case sensitivity of search.\",\"value\":\"\",\"promptText\":\"\",\"defaultValue\":\"\",\"requireSelection\":true,\"label\":\"Case sensitive?\",\"key\":\"casesensitive\",\"values\":[\"No\",\"Yes\"],\"model\":\"com.tanium.components.parameters::DropDownParameter\",\"parameterType\":\"com.tanium.components.parameters::DropDownParameter\"},{\"helpString\":\"Enter Yes/No whether the search is global.\",\"value\":\"\",\"promptText\":\"\",\"defaultValue\":\"\",\"requireSelection\":true,\"label\":\"Global\",\"key\":\"global\",\"values\":[\"No\",\"Yes\"],\"model\":\"com.tanium.components.parameters::DropDownParameter\",\"parameterType\":\"com.tanium.components.parameters::DropDownParameter\"}],\"model\":\"com.tanium.components.parameters::ParametersArray\",\"parameterType\":\"com.tanium.components.parameters::ParametersArray\"}", 
          "queries": {
            "query": [
              {
                "platform": "Windows", 
                "script": "&#039;========================================\n&#039; Folder Name Search with RegEx Match\n&#039;========================================\n&#039;@INCLUDE=utils/SensorRandomization/SensorRandomizationFunctions.vbs\nOption Explicit\n\nSensorRandomize()\n\nDim Pattern,strRegExp,strGlobalArg,strCaseSensitiveArg\nDim bGlobal,bCaseSensitive\n\nPattern = unescape(&quot;||dirname||&quot;)\nstrRegExp = Trim(Unescape(&quot;||regexp||&quot;))\nstrGlobalArg = Trim(Unescape(&quot;||global||&quot;))\nstrCaseSensitiveArg = Trim(Unescape(&quot;||casesensitive||&quot;))\n\nbGlobal = GetTrueFalseArg(&quot;global&quot;,strGlobalArg)\nbCaseSensitive = GetTrueFalseArg(&quot;casesensitive&quot;,strCaseSensitiveArg)\n\nConst SYSTEM_FOLDER = 1, TEMP_FOLDER = 2, FOR_READING = 1\n\nDim FSO, WshShell, Drives, Drive, TextStream, OutputFilename, strLine\n\nSet FSO = CreateObject(&quot;Scripting.FileSystemObject&quot;)\nSet WshShell = CreateObject(&quot;WScript.Shell&quot;)\n\nOutputFilename = TempName() &#039; a temporary file in system&#039;s temp dir\n\n&#039; Go through file system, refresh output file for filename\nIf Not FSO.FileExists(OutputFilename) Then\n\t\n\tIf FSO.FileExists(OutputFilename) Then FSO.DeleteFile OutputFilename\n\n\t&#039; Get the collection of local drives.\n\tSet Drives = FSO.Drives\n\tFor Each Drive in Drives\n\t\tIf Drive.DriveType = 2 Then &#039; 2 = Fixed drive\n\t\t\t&#039; Run the Dir command that looks for the filename pattern.\n\t\t\tRunCommand &quot;dir &quot; &amp;Chr(34)&amp; Drive.DriveLetter &amp; &quot;:\\&quot; &amp; Pattern &amp; Chr(34)&amp;&quot; /a:D /B /S&quot;, OutputFilename, true\n\t\tEnd If\n\tNext\nEnd If\n\n&#039; Open the output file, echo each line, and then close and delete it.\nSet TextStream = FSO.OpenTextFile(OutputFileName, FOR_READING)\nDo While Not TextStream.AtEndOfStream\n\tstrLine = TextStream.ReadLine()\n\tIf RegExpMatch(strRegExp,strLine,bGlobal,bCaseSensitive) Then\n\t\tWScript.Echo strLine\n\tEnd If\nLoop\n\n\nTextStream.Close()\n \nIf FSO.FileExists(OutputFileName) Then\n\tOn Error Resume Next\n\tFSO.DeleteFile OutputFileName, True\n\tOn Error Goto 0\nEnd If\n\nFunction RegExpMatch(strPattern,strToMatch,bGlobal,bIsCaseSensitive)\n\n\tDim re\n\tSet re = New RegExp\n\tWith re\n\t  .Pattern = strPattern\n\t  .Global = bGlobal\n\t  .IgnoreCase = Not bIsCaseSensitive\n\tEnd With\n\t\n\tRegExpMatch = re.Test(strToMatch)\n\nEnd Function &#039;RegExpMatch\n\n\nFunction GetTrueFalseArg(strArgName,strArgValue)\n\t&#039; Checks for valid values, will fail with error message\n\t\n\tDim bArgVal\n\tbArgVal = False\n\tSelect Case LCase(strArgValue)\n\t\tCase &quot;true&quot;\n\t\t\tbArgVal = True\n\t\tCase &quot;yes&quot;\n\t\t\tbArgVal = True\n\t\tCase &quot;false&quot;\n\t\t\tbArgVal = False\n\t\tCase &quot;no&quot;\n\t\t\tbArgVal = False\n\t\tCase Else\n\t\t\tWScript.Echo &quot;Error: Argument &#039;&quot;&amp;strArgName&amp;&quot;&#039; must be True or False, quitting&quot;\n\t\t\tPrintUsage\n\tEnd Select\n\tGetTrueFalseArg = bArgVal\n\nEnd Function &#039;GetTrueFalseArg\n\n\n&#039; Returns the name of a temporary file in the Temp directory.\nFunction TempName()\n\tDim Result\n\tDo\n \t\tResult = FSO.BuildPath(FSO.GetSpecialFolder(TEMP_FOLDER), FSO.GetTempName())\n\t\tWScript.Sleep 200 &#039;avoid potential busy loop\n\tLoop While FSO.FileExists(Result)\n\t\n\tTempName = Result\nEnd Function &#039;TempName\n\n&#039; Runs a command with Cmd.exe and redirects its output to a temporary\n&#039; file. The function returns the name of the temporary file that holds\n&#039; the command&#039;s output.\nFunction RunCommand(Command, OutputFilename, b64BitNecessary)\n\t&#039; 64BitNecessary true when you need to examine the 64-bit areas like system32\n\tDim CommandLine,WshShell,strPRogramFilesx86,strDOSCall,objFSO\n\tSet objFSO = CreateObject(&quot;Scripting.FileSystemObject&quot;)\n\tSet WshShell = CreateObject(&quot;WScript.Shell&quot;)\n\t\n\tstrDOSCall = &quot;%ComSpec% /C &quot;\n\t\n\t&#039; if 64-bit OS *and* we must examine in 64-bit mode to avoid FS Redirection\n\tstrProgramFilesx86=WshShell.ExpandEnvironmentStrings(&quot;%ProgramFiles%&quot;)\n\tIf objFSO.FolderExists(strProgramFilesx86) And b64BitNecessary Then &#039; quick check for x64\n\t\tstrDOSCall = FixFileSystemRedirectionForPath(WshShell.ExpandEnvironmentStrings(strDOSCall))\n\tEnd If\n\t\t\n\tCommandLine = WshShell.ExpandEnvironmentStrings(strDOSCall &amp; Command &amp; &quot; &gt;&gt; &quot;&quot;&quot; &amp; OutputFileName &amp; &quot;&quot;&quot;&quot;)\n\tWshShell.Run CommandLine, 0, True\nEnd Function &#039;RunCommand\n\nFunction FixFileSystemRedirectionForPath(strFilePath)\n&#039; This function will fix a folder location so that\n&#039; a 32-bit program can be passed the windows\\system32 directory\n&#039; as a parameter.\n&#039; Even if the sensor or action runs in 64-bit mode, a 32-bit\n&#039; program called in a 64-bit environment cannot access\n&#039; the system32 directory - it would be redirected to syswow64.\n&#039; you would not want to do this for 64-bit programs.\n\t\n\tDim objFSO, strSystem32Location,objShell\n\tDim strProgramFilesx86,strNewSystem32Location,strRestOfPath\n\tSet objFSO = CreateObject(&quot;Scripting.FileSystemObject&quot;)\n\tSet objShell = CreateObject(&quot;Wscript.Shell&quot;)\n\n\tstrProgramFilesx86=objShell.ExpandEnvironmentStrings(&quot;%ProgramFiles%&quot;)\n\n\tstrFilePath = LCase(strFilePath)\n\tstrSystem32Location = LCase(objFSO.GetSpecialFolder(1))\n\tstrProgramFilesx86=objShell.ExpandEnvironmentStrings(&quot;%ProgramFiles(x86)%&quot;)\n\t\n\tIf objFSO.FolderExists(strProgramFilesx86) Then &#039; quick check for x64\n\t\tIf InStr(strFilePath,strSystem32Location) = 1 Then\n\t\t\tstrRestOfPath = Replace(strFilePath,strSystem32Location,&quot;&quot;)\n\t\t\tstrNewSystem32Location = Replace(strSystem32Location,&quot;system32&quot;,&quot;sysnative&quot;)\n\t\t\tstrFilePath = strNewSystem32Location&amp;strRestOfPath\n\t\tEnd If\n\tEnd If\n\tFixFileSystemRedirectionForPath = strFilePath\n\t\n\t&#039;Cleanup\n\tSet objFSO = Nothing\nEnd Function &#039;FixFileSystemRedirectionForPath\n&#039;------------ INCLUDES after this line. Do not edit past this point -----\n&#039;- Begin file: utils/SensorRandomization/SensorRandomizationFunctions.vbs\n&#039;&#039; -- Begin Random Sleep Functions -- &#039;&#039;\n\nDim bSensorRandomizeDebugOutput : bSensorRandomizeDebugOutput = False\n\nFunction SensorRandomizeLow()\n    Dim intSensorRandomizeWaitLow : intSensorRandomizeWaitLow = 10\n    SensorRandomizeRandomSleep(intSensorRandomizeWaitLow)\nEnd Function &#039; SensorRandomizeLow\n\nFunction SensorRandomize()\n    Dim intSensorRandomizeWaitMed : intSensorRandomizeWaitMed = 20\n    SensorRandomizeRandomSleep(intSensorRandomizeWaitMed)\nEnd Function &#039; SensorRandomize\n\nFunction SensorRandomizeHigh()\n    Dim intSensorRandomizeWaitHigh : intSensorRandomizeWaitHigh = 30\n    SensorRandomizeRandomSleep(intSensorRandomizeWaitHigh)\nEnd Function &#039; SensorRandomize\n\nFunction SensorRandomizeRandomSleep(intSleepTime)\n&#039; sleeps for a random period of time, intSleepTime is in seconds\n&#039; if the sensor randomize flag is on\n&#039; RandomizeScalingFactor is a multiplier on the values hardcoded in the sensor\n&#039; not typically set but can adjust timings per endpoint, optionally\n\tDim intSensorRandomizeWaitTime\n\tDim objShell,intRandomizeFlag,strRandomizeRegPath,intRandomizeScalingPercentage\n\tstrRandomizeRegPath = SensorRandomizeGetTaniumRegistryPath&amp;&quot;\\Sensor Data\\Random Sleep&quot;\n\t\n\tSet objShell = CreateObject(&quot;WScript.Shell&quot;)\n\tOn Error Resume Next\n\tintRandomizeFlag = objShell.RegRead(&quot;HKLM\\&quot;&amp;strRandomizeRegPath&amp;&quot;\\SensorRandomizeFlag&quot;)\n\tintRandomizeScalingPercentage = objShell.RegRead(&quot;HKLM\\&quot;&amp;strRandomizeRegPath&amp;&quot;\\SensorRandomizeScalingPercentage&quot;)\n\tOn Error Goto 0\n\tIf intRandomizeFlag &gt; 0 Then\n\t\tIf intRandomizeScalingPercentage &gt; 0 Then\n\t\t\tintSleepTime = intRandomizeScalingPercentage * .01 * intSleepTime\n\t\t\tSensorRandomizeEcho &quot;Randomize scaling percentage of &quot; _ \n\t\t\t\t&amp; intRandomizeScalingPercentage &amp; &quot; applied, new sleep time is &quot; &amp; intSleepTime\n\t\tEnd If\n\t\tintSensorRandomizeWaitTime = CLng(intSleepTime) * 1000 &#039; convert to milliseconds\n\t\t&#039; wait random interval between 0 and the max\n\t\tRandomize(SensorRandomizeTaniumRandomSeed)\n\t\t&#039; assign random value to wait time max value\n\t\tintSensorRandomizeWaitTime = Int( ( intSensorRandomizeWaitTime + 1 ) * Rnd )\n\t\tSensorRandomizeEcho &quot;Sleeping for &quot; &amp; intSensorRandomizeWaitTime &amp; &quot; milliseconds&quot;\n\t\tWScript.Sleep(intSensorRandomizeWaitTime)\n\t\tSensorRandomizeEcho &quot;Done sleeping, continuing ...&quot;\n\tElse \n\t\tSensorRandomizeEcho &quot;SensorRandomize Not Enabled - No Op&quot;\n\tEnd If\nEnd Function &#039;SensorRandomizeRandomSleep\n\nFunction SensorRandomizeTaniumRandomSeed\n&#039; for randomizing sensor code, the default seed is not random enough\n\tDim timerNum\n\ttimerNum = Timer()\n\tIf timerNum &lt; 1 Then\n\t\tSensorRandomizeTaniumRandomSeed = (SensorRandomizeGetTaniumComputerID / Timer() * 10 )\n\tElse\n\t\tSensorRandomizeTaniumRandomSeed = SensorRandomizeGetTaniumComputerID / Timer\n\tEnd If\nEnd Function &#039;SensorRandomizeTaniumRandomSeed\n\nFunction SensorRandomizeGetTaniumRegistryPath\n&#039;SensorRandomizeGetTaniumRegistryPath works in x64 or x32\n&#039;looks for a valid Path value\n\n\tDim objShell\n\tDim keyNativePath, keyWoWPath, strPath, strFoundTaniumRegistryPath\n\t  \n    Set objShell = CreateObject(&quot;WScript.Shell&quot;)\n    \n\tkeyNativePath = &quot;Software\\Tanium\\Tanium Client&quot;\n\tkeyWoWPath = &quot;Software\\Wow6432Node\\Tanium\\Tanium Client&quot;\n    \n    &#039; first check the Software key (valid for 32-bit machines, or 64-bit machines in 32-bit mode)\n    On Error Resume Next\n    strPath = objShell.RegRead(&quot;HKLM\\&quot;&amp;keyNativePath&amp;&quot;\\Path&quot;)\n    On Error Goto 0\n\tstrFoundTaniumRegistryPath = keyNativePath\n \n  \tIf strPath = &quot;&quot; Then\n  \t\t&#039; Could not find 32-bit mode path, checking Wow6432Node\n  \t\tOn Error Resume Next\n  \t\tstrPath = objShell.RegRead(&quot;HKLM\\&quot;&amp;keyWoWPath&amp;&quot;\\Path&quot;)\n  \t\tOn Error Goto 0\n\t\tstrFoundTaniumRegistryPath = keyWoWPath\n  \tEnd If\n  \t\n  \tIf Not strPath = &quot;&quot; Then\n  \t\tSensorRandomizeGetTaniumRegistryPath = strFoundTaniumRegistryPath\n  \tElse\n  \t\tSensorRandomizeGetTaniumRegistryPath = False\n  \t\tWScript.Echo &quot;Error: Cannot locate Tanium Registry Path&quot;\n  \tEnd If\nEnd Function &#039;SensorRandomizeGetTaniumRegistryPath\n\nFunction SensorRandomizeGetTaniumComputerID\n&#039;&#039; This function gets the Tanium Computer ID\n\tDim objShell\n\tDim intClientID,strID,strKeyPath,strValueName\n\t\n    strKeyPath = SensorRandomizeGetTaniumRegistryPath\n    strValueName = &quot;ComputerID&quot;\n    Set objShell = CreateObject(&quot;WScript.Shell&quot;)\n    On Error Resume Next\n    intClientID = objShell.RegRead(&quot;HKLM\\&quot;&amp;strKeyPath&amp;&quot;\\&quot;&amp;strValueName)\n    If Err.Number &lt;&gt; 0 Then\n    \tSensorRandomizeGetTaniumComputerID = 0\n    Else\n\t\tSensorRandomizeGetTaniumComputerID = SensorRandomizeReinterpretSignedAsUnsigned(intClientID)\n\tEnd If\n\tOn Error Goto 0\nEnd Function &#039;SensorRandomizeGetTaniumComputerID\n\nFunction SensorRandomizeReinterpretSignedAsUnsigned(ByVal x)\n\t  If x &lt; 0 Then x = x + 2^32\n\t  SensorRandomizeReinterpretSignedAsUnsigned = x\nEnd Function &#039;SensorRandomizeReinterpretSignedAsUnsigned\n\nSub SensorRandomizeEcho(str)\n\tIf bSensorRandomizeDebugOutput = true Then WScript.Echo str\nEnd Sub &#039;SensorRandomizeEcho\n&#039; -- End Random Sleep Functions --&#039;\n&#039;- End file: utils/SensorRandomization/SensorRandomizationFunctions.vbs", 
                "script_type": "VBScript"
              }, 
              {
                "platform": "Linux", 
                "script": "#!/bin/bash\n#||dirname||||regexp||||casesensitive||||global||\necho Windows Only\n", 
                "script_type": "UnixShell"
              }, 
              {
                "platform": "Mac", 
                "script": "#!/bin/bash\n#||dirname||||regexp||||casesensitive||||global||\necho Windows Only\n", 
                "script_type": "UnixShell"
              }
            ]
          }, 
          "source_id": 0, 
          "string_count": 3, 
          "value_type": "String"
        }
      ]
    }
