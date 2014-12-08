
Export basetype csv with explode true
====================================================================================================
Export a BaseType from getting objects as CSV with true for explode_json_string_values

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
    export_kwargs["export_format"] = u'csv'
    export_kwargs["explode_json_string_values"] = True
    
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
    category,creation_time,delimiter,description,exclude_from_parse_flag,hash,hidden_flag,id,ignore_case_flag,last_modified_by,max_age_seconds,metadata_item_0_admin_flag,metadata_item_0_name,metadata_item_0_value,modification_time,name,parameter_definition_model,parameter_definition_parameterType,parameter_definition_parameters_0_defaultValue,parameter_definition_parameters_0_helpString,parameter_definition_parameters_0_key,parameter_definition_parameters_0_label,parameter_definition_parameters_0_maxChars,parameter_definition_parameters_0_model,parameter_definition_parameters_0_parameterType,parameter_definition_parameters_0_promptText,parameter_definition_parameters_0_restrict,parameter_definition_parameters_0_validationExpressions_0_expression,parameter_definition_parameters_0_validationExpressions_0_flags,parameter_definition_parameters_0_validationExpressions_0_helpString,parameter_definition_parameters_0_validationExpressions_0_model,parameter_definition_parameters_0_validationExpressions_0_parameterType,parameter_definition_parameters_0_value,parameter_definition_parameters_1_defaultValue,parameter_definition_parameters_1_helpString,parameter_definition_parameters_1_key,parameter_definition_parameters_1_label,parameter_definition_parameters_1_maxChars,parameter_definition_parameters_1_model,parameter_definition_parameters_1_parameterType,parameter_definition_parameters_1_promptText,parameter_definition_parameters_1_restrict,parameter_definition_parameters_1_validationExpressions_0_expression,parameter_definition_parameters_1_validationExpressions_0_flags,parameter_definition_parameters_1_validationExpressions_0_helpString,parameter_definition_parameters_1_validationExpressions_0_model,parameter_definition_parameters_1_validationExpressions_0_parameterType,parameter_definition_parameters_1_value,parameter_definition_parameters_2_defaultValue,parameter_definition_parameters_2_helpString,parameter_definition_parameters_2_key,parameter_definition_parameters_2_label,parameter_definition_parameters_2_model,parameter_definition_parameters_2_parameterType,parameter_definition_parameters_2_promptText,parameter_definition_parameters_2_requireSelection,parameter_definition_parameters_2_value,parameter_definition_parameters_2_values_0,parameter_definition_parameters_2_values_1,parameter_definition_parameters_3_defaultValue,parameter_definition_parameters_3_helpString,parameter_definition_parameters_3_key,parameter_definition_parameters_3_label,parameter_definition_parameters_3_model,parameter_definition_parameters_3_parameterType,parameter_definition_parameters_3_promptText,parameter_definition_parameters_3_requireSelection,parameter_definition_parameters_3_value,parameter_definition_parameters_3_values_0,parameter_definition_parameters_3_values_1,queries_query_0_platform,queries_query_0_script,queries_query_0_script_type,queries_query_1_platform,queries_query_1_script,queries_query_1_script_type,queries_query_2_platform,queries_query_2_script,queries_query_2_script_type,source_id,string_count,subcolumns_subcolumn_0_hidden_flag,subcolumns_subcolumn_0_ignore_case_flag,subcolumns_subcolumn_0_index,subcolumns_subcolumn_0_name,subcolumns_subcolumn_0_value_type,subcolumns_subcolumn_1_hidden_flag,subcolumns_subcolumn_1_ignore_case_flag,subcolumns_subcolumn_1_index,subcolumns_subcolumn_1_name,subcolumns_subcolumn_1_value_type,subcolumns_subcolumn_2_hidden_flag,subcolumns_subcolumn_2_ignore_case_flag,subcolumns_subcolumn_2_index,subcolumns_subcolumn_2_name,subcolumns_subcolumn_2_value_type,subcolumns_subcolumn_3_hidden_flag,subcolumns_subcolumn_3_ignore_case_flag,subcolumns_subcolumn_3_index,subcolumns_subcolumn_3_name,subcolumns_subcolumn_3_value_type,subcolumns_subcolumn_4_hidden_flag,subcolumns_subcolumn_4_ignore_case_flag,subcolumns_subcolumn_4_index,subcolumns_subcolumn_4_name,subcolumns_subcolumn_4_value_type,subcolumns_subcolumn_5_hidden_flag,subcolumns_subcolumn_5_ignore_case_flag,subcolumns_subcolumn_5_index,subcolumns_subcolumn_5_name,subcolumns_subcolumn_5_value_type,value_type
    Reserved,,,"The assigned name of the client machine.
    Example: workstation-1.company.com",0,3409330187,0,3,1,,86400,,,,,Computer Name,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Windows,select CSName from win32_operatingsystem,WMIQuery,,,,,,,0,7,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,String
    Network,2014-12-06T18:00:24,|,"Returns IPv4 network routes, filtered to exclude noise. With Flags, Metric, Interface columns.
    Example:  172.16.0.0|192.168.1.1|255.255.0.0|UG|100|eth0",1,435227963,0,737,1,Jim Olsen,60,0,defined,Tanium,2014-12-06T18:00:24,IP Route Details,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Windows,"strComputer = &quot;.&quot;
    Set objWMIService = GetObject(&quot;winmgmts:&quot; _
        &amp; &quot;{impersonationLevel=impersonate}!\\&quot; &amp; strComputer &amp; &quot;\root\cimv2&quot;)
    
    Set collip = objWMIService.ExecQuery(&quot;select * from win32_networkadapterconfiguration where IPEnabled=&#039;True&#039;&quot;)
    dim ipaddrs()
    ipcount = 0
    for each ipItem in collip
        for each ipaddr in ipItem.IPAddress
            ipcount = ipcount + 1
        next
    next
    redim ipaddrs(ipcount)
    ipcount = 0
    for each ipItem in collip
        for each ipaddr in ipItem.IPAddress
            ipcount = ipcount + 1
            ipaddrs(ipcount) = ipaddr
        next
    next
    localhost = &quot;127.0.0.1&quot;
    
    Set colItems = objWMIService.ExecQuery(&quot;Select * from Win32_IP4RouteTable&quot;)
    
    For Each objItem in colItems
        dest = objItem.Destination
        gw = objItem.NextHop
        mask = objItem.Mask
        metric = objItem.Metric1
        flags = objItem.Type
        intf = objItem.InterfaceIndex
        For i = 0 to ipcount
            if gw = ipaddrs(i) and gw &lt;&gt; localhost then
                gw = &quot;0.0.0.0&quot;
            end if
        Next
        if gw &lt;&gt; localhost and dest &lt;&gt; &quot;224.0.0.0&quot; and right(dest,3) &lt;&gt; &quot;255&quot; then
            Wscript.Echo dest &amp; &quot;|&quot; &amp; gw &amp; &quot;|&quot; &amp; mask &amp; &quot;|&quot; &amp; &quot;-&quot; &amp; &quot;|&quot; &amp; metric &amp; &quot;|&quot; &amp; &quot;-&quot;
        end if
    Next",VBScript,Linux,"route -n | grep -v Kernel | grep -v Destination | awk &#039;{ print $1 &quot;|&quot; $2 &quot;|&quot; $3 &quot;|&quot; $4 &quot;|&quot; $5 &quot;|&quot; $8 }&#039; | grep -v &quot;|127.0.0.1|&quot;
    ",UnixShell,Mac,"netstat -rn | grep -v &quot;:&quot; | grep -v Destination | grep -v Routing | grep -v -e &quot;^$&quot; | awk &#039;{ print $1 &quot;|&quot; $2 &quot;||&quot; $3 &quot;||&quot; $6 }&#039; | grep -v &quot;|127.0.0.1|&quot;
    ",UnixShell,0,48,0,1,0,Destination,IPAddress,0,1,1,Gateway,IPAddress,0,1,2,Mask,String,0,1,3,Flags,String,0,1,4,Metric,NumericInteger,0,1,5,Interface,String,String
    Network,2014-12-06T18:00:22,",","Current IP Addresses of client machine.
    Example: 192.168.1.1",1,3209138996,0,147,1,Jim Olsen,600,0,defined,Tanium,2014-12-06T18:00:22,IP Address,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Windows,select IPAddress from win32_networkadapterconfiguration where IPEnabled=&#039;True&#039;,WMIQuery,Linux,"#!/bin/bash
    ifconfig | grep -w inet | grep -v 127.0.0.1 | awk &#039;{print $2}&#039; | sed -e &#039;s/addr://&#039;
    ",UnixShell,Mac,"#!/bin/bash
    
    ifconfig -a -u |grep &quot;inet&quot; | grep -v &quot;::1&quot; | grep -v &quot;127.0.0.1&quot;| awk &#039;{print $2}&#039; | cut -f1 -d&#039;%&#039;
    ",UnixShell,0,86,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,IPAddress
    File System,2014-12-06T18:00:23,",","Finds the specified folder and provides the full path if the folder exists on the client machine. Takes regular expression to match.
    Example: C:\WINDOWS\System32",1,1374547302,0,381,1,Jim Olsen,600,0,defined,McAfee,2014-12-06T18:00:23,Folder Name Search with RegEx Match,com.tanium.components.parameters::ParametersArray,com.tanium.components.parameters::ParametersArray,,Enter the folder name to search for,dirname,Search for Folder Name,0,com.tanium.components.parameters::TextInputParameter,com.tanium.components.parameters::TextInputParameter,e.g Program Files,,\S{3},,Value must be at least 3 characters,com.tanium.models::ValidationExpression,com.tanium.models::ValidationExpression,,,Enter the regular expression to search for.,regexp,Regular Expression,0,com.tanium.components.parameters::TextInputParameter,com.tanium.components.parameters::TextInputParameter,e.g. test*.exe,,\S{3},,Value must be at least 3 characters,com.tanium.models::ValidationExpression,com.tanium.models::ValidationExpression,,,Enter Yes/No for case sensitivity of search.,casesensitive,Case sensitive?,com.tanium.components.parameters::DropDownParameter,com.tanium.components.parameters::DropDownParameter,,True,,No,Yes,,Enter Yes/No whether the search is global.,global,Global,com.tanium.components.parameters::DropDownParameter,com.tanium.components.parameters::DropDownParameter,,True,,No,Yes,Windows,"&#039;========================================
    &#039; Folder Name Search with RegEx Match
    &#039;========================================
    &#039;@INCLUDE=utils/SensorRandomization/SensorRandomizationFunctions.vbs
    Option Explicit
    
    SensorRandomize()
    
    Dim Pattern,strRegExp,strGlobalArg,strCaseSensitiveArg
    Dim bGlobal,bCaseSensitive
    
    Pattern = unescape(&quot;||dirname||&quot;)
    strRegExp = Trim(Unescape(&quot;||regexp||&quot;))
    strGlobalArg = Trim(Unescape(&quot;||global||&quot;))
    strCaseSensitiveArg = Trim(Unescape(&quot;||casesensitive||&quot;))
    
    bGlobal = GetTrueFalseArg(&quot;global&quot;,strGlobalArg)
    bCaseSensitive = GetTrueFalseArg(&quot;casesensitive&quot;,strCaseSensitiveArg)
    
    Const SYSTEM_FOLDER = 1, TEMP_FOLDER = 2, FOR_READING = 1
    
    Dim FSO, WshShell, Drives, Drive, TextStream, OutputFilename, strLine
    
    Set FSO = CreateObject(&quot;Scripting.FileSystemObject&quot;)
    Set WshShell = CreateObject(&quot;WScript.Shell&quot;)
    
    OutputFilename = TempName() &#039; a temporary file in system&#039;s temp dir
    
    &#039; Go through file system, refresh output file for filename
    If Not FSO.FileExists(OutputFilename) Then
    	
    	If FSO.FileExists(OutputFilename) Then FSO.DeleteFile OutputFilename
    
    	&#039; Get the collection of local drives.
    	Set Drives = FSO.Drives
    	For Each Drive in Drives
    		If Drive.DriveType = 2 Then &#039; 2 = Fixed drive
    			&#039; Run the Dir command that looks for the filename pattern.
    			RunCommand &quot;dir &quot; &amp;Chr(34)&amp; Drive.DriveLetter &amp; &quot;:\&quot; &amp; Pattern &amp; Chr(34)&amp;&quot; /a:D /B /S&quot;, OutputFilename, true
    		End If
    	Next
    End If
    
    &#039; Open the output file, echo each line, and then close and delete it.
    Set TextStream = FSO.OpenTextFile(OutputFileName, FOR_READING)
    Do While Not TextStream.AtEndOfStream
    	strLine = TextStream.ReadLine()
    	If RegExpMatch(strRegExp,strLine,bGlobal,bCaseSensitive) Then
    		WScript.Echo strLine
    	End If
    Loop
    
    
    TextStream.Close()
     
    If FSO.FileExists(OutputFileName) Then
    	On Error Resume Next
    	FSO.DeleteFile OutputFileName, True
    	On Error Goto 0
    End If
    
    Function RegExpMatch(strPattern,strToMatch,bGlobal,bIsCaseSensitive)
    
    	Dim re
    	Set re = New RegExp
    	With re
    	  .Pattern = strPattern
    	  .Global = bGlobal
    	  .IgnoreCase = Not bIsCaseSensitive
    	End With
    	
    	RegExpMatch = re.Test(strToMatch)
    
    End Function &#039;RegExpMatch
    
    
    Function GetTrueFalseArg(strArgName,strArgValue)
    	&#039; Checks for valid values, will fail with error message
    	
    	Dim bArgVal
    	bArgVal = False
    	Select Case LCase(strArgValue)
    		Case &quot;true&quot;
    			bArgVal = True
    		Case &quot;yes&quot;
    			bArgVal = True
    		Case &quot;false&quot;
    			bArgVal = False
    		Case &quot;no&quot;
    			bArgVal = False
    		Case Else
    			WScript.Echo &quot;Error: Argument &#039;&quot;&amp;strArgName&amp;&quot;&#039; must be True or False, quitting&quot;
    			PrintUsage
    	End Select
    	GetTrueFalseArg = bArgVal
    
    End Function &#039;GetTrueFalseArg
    
    
    &#039; Returns the name of a temporary file in the Temp directory.
    Function TempName()
    	Dim Result
    	Do
     		Result = FSO.BuildPath(FSO.GetSpecialFolder(TEMP_FOLDER), FSO.GetTempName())
    		WScript.Sleep 200 &#039;avoid potential busy loop
    	Loop While FSO.FileExists(Result)
    	
    	TempName = Result
    End Function &#039;TempName
    
    &#039; Runs a command with Cmd.exe and redirects its output to a temporary
    &#039; file. The function returns the name of the temporary file that holds
    &#039; the command&#039;s output.
    Function RunCommand(Command, OutputFilename, b64BitNecessary)
    	&#039; 64BitNecessary true when you need to examine the 64-bit areas like system32
    	Dim CommandLine,WshShell,strPRogramFilesx86,strDOSCall,objFSO
    	Set objFSO = CreateObject(&quot;Scripting.FileSystemObject&quot;)
    	Set WshShell = CreateObject(&quot;WScript.Shell&quot;)
    	
    	strDOSCall = &quot;%ComSpec% /C &quot;
    	
    	&#039; if 64-bit OS *and* we must examine in 64-bit mode to avoid FS Redirection
    	strProgramFilesx86=WshShell.ExpandEnvironmentStrings(&quot;%ProgramFiles%&quot;)
    	If objFSO.FolderExists(strProgramFilesx86) And b64BitNecessary Then &#039; quick check for x64
    		strDOSCall = FixFileSystemRedirectionForPath(WshShell.ExpandEnvironmentStrings(strDOSCall))
    	End If
    		
    	CommandLine = WshShell.ExpandEnvironmentStrings(strDOSCall &amp; Command &amp; &quot; &gt;&gt; &quot;&quot;&quot; &amp; OutputFileName &amp; &quot;&quot;&quot;&quot;)
    	WshShell.Run CommandLine, 0, True
    End Function &#039;RunCommand
    
    Function FixFileSystemRedirectionForPath(strFilePath)
    &#039; This function will fix a folder location so that
    &#039; a 32-bit program can be passed the windows\system32 directory
    &#039; as a parameter.
    &#039; Even if the sensor or action runs in 64-bit mode, a 32-bit
    &#039; program called in a 64-bit environment cannot access
    &#039; the system32 directory - it would be redirected to syswow64.
    &#039; you would not want to do this for 64-bit programs.
    	
    	Dim objFSO, strSystem32Location,objShell
    	Dim strProgramFilesx86,strNewSystem32Location,strRestOfPath
    	Set objFSO = CreateObject(&quot;Scripting.FileSystemObject&quot;)
    	Set objShell = CreateObject(&quot;Wscript.Shell&quot;)
    
    	strProgramFilesx86=objShell.ExpandEnvironmentStrings(&quot;%ProgramFiles%&quot;)
    
    	strFilePath = LCase(strFilePath)
    	strSystem32Location = LCase(objFSO.GetSpecialFolder(1))
    	strProgramFilesx86=objShell.ExpandEnvironmentStrings(&quot;%ProgramFiles(x86)%&quot;)
    	
    	If objFSO.FolderExists(strProgramFilesx86) Then &#039; quick check for x64
    		If InStr(strFilePath,strSystem32Location) = 1 Then
    			strRestOfPath = Replace(strFilePath,strSystem32Location,&quot;&quot;)
    			strNewSystem32Location = Replace(strSystem32Location,&quot;system32&quot;,&quot;sysnative&quot;)
    			strFilePath = strNewSystem32Location&amp;strRestOfPath
    		End If
    	End If
    	FixFileSystemRedirectionForPath = strFilePath
    	
    	&#039;Cleanup
    	Set objFSO = Nothing
    End Function &#039;FixFileSystemRedirectionForPath
    &#039;------------ INCLUDES after this line. Do not edit past this point -----
    &#039;- Begin file: utils/SensorRandomization/SensorRandomizationFunctions.vbs
    &#039;&#039; -- Begin Random Sleep Functions -- &#039;&#039;
    
    Dim bSensorRandomizeDebugOutput : bSensorRandomizeDebugOutput = False
    
    Function SensorRandomizeLow()
        Dim intSensorRandomizeWaitLow : intSensorRandomizeWaitLow = 10
        SensorRandomizeRandomSleep(intSensorRandomizeWaitLow)
    End Function &#039; SensorRandomizeLow
    
    Function SensorRandomize()
        Dim intSensorRandomizeWaitMed : intSensorRandomizeWaitMed = 20
        SensorRandomizeRandomSleep(intSensorRandomizeWaitMed)
    End Function &#039; SensorRandomize
    
    Function SensorRandomizeHigh()
        Dim intSensorRandomizeWaitHigh : intSensorRandomizeWaitHigh = 30
        SensorRandomizeRandomSleep(intSensorRandomizeWaitHigh)
    End Function &#039; SensorRandomize
    
    Function SensorRandomizeRandomSleep(intSleepTime)
    &#039; sleeps for a random period of time, intSleepTime is in seconds
    &#039; if the sensor randomize flag is on
    &#039; RandomizeScalingFactor is a multiplier on the values hardcoded in the sensor
    &#039; not typically set but can adjust timings per endpoint, optionally
    	Dim intSensorRandomizeWaitTime
    	Dim objShell,intRandomizeFlag,strRandomizeRegPath,intRandomizeScalingPercentage
    	strRandomizeRegPath = SensorRandomizeGetTaniumRegistryPath&amp;&quot;\Sensor Data\Random Sleep&quot;
    	
    	Set objShell = CreateObject(&quot;WScript.Shell&quot;)
    	On Error Resume Next
    	intRandomizeFlag = objShell.RegRead(&quot;HKLM\&quot;&amp;strRandomizeRegPath&amp;&quot;\SensorRandomizeFlag&quot;)
    	intRandomizeScalingPercentage = objShell.RegRead(&quot;HKLM\&quot;&amp;strRandomizeRegPath&amp;&quot;\SensorRandomizeScalingPercentage&quot;)
    	On Error Goto 0
    	If intRandomizeFlag &gt; 0 Then
    		If intRandomizeScalingPercentage &gt; 0 Then
    			intSleepTime = intRandomizeScalingPercentage * .01 * intSleepTime
    			SensorRandomizeEcho &quot;Randomize scaling percentage of &quot; _ 
    				&amp; intRandomizeScalingPercentage &amp; &quot; applied, new sleep time is &quot; &amp; intSleepTime
    		End If
    		intSensorRandomizeWaitTime = CLng(intSleepTime) * 1000 &#039; convert to milliseconds
    		&#039; wait random interval between 0 and the max
    		Randomize(SensorRandomizeTaniumRandomSeed)
    		&#039; assign random value to wait time max value
    		intSensorRandomizeWaitTime = Int( ( intSensorRandomizeWaitTime + 1 ) * Rnd )
    		SensorRandomizeEcho &quot;Sleeping for &quot; &amp; intSensorRandomizeWaitTime &amp; &quot; milliseconds&quot;
    		WScript.Sleep(intSensorRandomizeWaitTime)
    		SensorRandomizeEcho &quot;Done sleeping, continuing ...&quot;
    	Else 
    		SensorRandomizeEcho &quot;SensorRandomize Not Enabled - No Op&quot;
    	End If
    End Function &#039;SensorRandomizeRandomSleep
    
    Function SensorRandomizeTaniumRandomSeed
    &#039; for randomizing sensor code, the default seed is not random enough
    	Dim timerNum
    	timerNum = Timer()
    	If timerNum &lt; 1 Then
    		SensorRandomizeTaniumRandomSeed = (SensorRandomizeGetTaniumComputerID / Timer() * 10 )
    	Else
    		SensorRandomizeTaniumRandomSeed = SensorRandomizeGetTaniumComputerID / Timer
    	End If
    End Function &#039;SensorRandomizeTaniumRandomSeed
    
    Function SensorRandomizeGetTaniumRegistryPath
    &#039;SensorRandomizeGetTaniumRegistryPath works in x64 or x32
    &#039;looks for a valid Path value
    
    	Dim objShell
    	Dim keyNativePath, keyWoWPath, strPath, strFoundTaniumRegistryPath
    	  
        Set objShell = CreateObject(&quot;WScript.Shell&quot;)
        
    	keyNativePath = &quot;Software\Tanium\Tanium Client&quot;
    	keyWoWPath = &quot;Software\Wow6432Node\Tanium\Tanium Client&quot;
        
        &#039; first check the Software key (valid for 32-bit machines, or 64-bit machines in 32-bit mode)
        On Error Resume Next
        strPath = objShell.RegRead(&quot;HKLM\&quot;&amp;keyNativePath&amp;&quot;\Path&quot;)
        On Error Goto 0
    	strFoundTaniumRegistryPath = keyNativePath
     
      	If strPath = &quot;&quot; Then
      		&#039; Could not find 32-bit mode path, checking Wow6432Node
      		On Error Resume Next
      		strPath = objShell.RegRead(&quot;HKLM\&quot;&amp;keyWoWPath&amp;&quot;\Path&quot;)
      		On Error Goto 0
    		strFoundTaniumRegistryPath = keyWoWPath
      	End If
      	
      	If Not strPath = &quot;&quot; Then
      		SensorRandomizeGetTaniumRegistryPath = strFoundTaniumRegistryPath
      	Else
      		SensorRandomizeGetTaniumRegistryPath = False
      		WScript.Echo &quot;Error: Cannot locate Tanium Registry Path&quot;
      	End If
    End Function &#039;SensorRandomizeGetTaniumRegistryPath
    
    Function SensorRandomizeGetTaniumComputerID
    &#039;&#039; This function gets the Tanium Computer ID
    	Dim objShell
    	Dim intClientID,strID,strKeyPath,strValueName
    	
        strKeyPath = SensorRandomizeGetTaniumRegistryPath
        strValueName = &quot;ComputerID&quot;
        Set objShell = CreateObject(&quot;WScript.Shell&quot;)
        On Error Resume Next
        intClientID = objShell.RegRead(&quot;HKLM\&quot;&amp;strKeyPath&amp;&quot;\&quot;&amp;strValueName)
        If Err.Number &lt;&gt; 0 Then
        	SensorRandomizeGetTaniumComputerID = 0
        Else
    		SensorRandomizeGetTaniumComputerID = SensorRandomizeReinterpretSignedAsUnsigned(intClientID)
    	End If
    	On Error Goto 0
    End Function &#039;SensorRandomizeGetTaniumComputerID
    
    Function SensorRandomizeReinterpretSignedAsUnsigned(ByVal x)
    	  If x &lt; 0 Then x = x + 2^32
    	  SensorRandomizeReinterpretSignedAsUnsigned = x
    End Function &#039;SensorRandomizeReinterpretSignedAsUnsigned
    
    Sub SensorRandomizeEcho(str)
    	If bSensorRandomizeDebugOutput = true Then WScript.Echo str
    End Sub &#039;SensorRandomizeEcho
    &#039; -- End Random Sleep Functions --&#039;
    &#039;- End file: utils/SensorRandomization/SensorRandomizationFunctions.vbs",VBScript,Linux,"#!/bin/bash
    #||dirname||||regexp||||casesensitive||||global||
    echo Windows Only
    ",UnixShell,Mac,"#!/bin/bash
    #||dirname||||regexp||||casesensitive||||global||
    echo Windows Only
    ",UnixShell,0,3,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,String
    
