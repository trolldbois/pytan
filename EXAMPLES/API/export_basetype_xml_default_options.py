
"""
Export a BaseType from getting objects as XML with the default options
"""
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
export_kwargs["export_format"] = u'xml'

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


'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258

print the export_str returned from export_obj():
<sensors><cache_info /><sensor><category>Reserved</category><preview_sensor_flag /><hash>3409330187</hash><name>Computer Name</name><hidden_flag>0</hidden_flag><delimiter /><creation_time /><exclude_from_parse_flag>0</exclude_from_parse_flag><last_modified_by /><string_count>7</string_count><source_hash /><modification_time /><ignore_case_flag>1</ignore_case_flag><max_age_seconds>86400</max_age_seconds><value_type>String</value_type><cache_row_id /><source_id>0</source_id><deleted_flag /><parameter_definition /><id>3</id><description>The assigned name of the client machine.
Example: workstation-1.company.com</description><string_hints /><subcolumns /><metadata /><parameters /><queries><query><platform>Windows</platform><script_type>WMIQuery</script_type><signature /><script>select CSName from win32_operatingsystem</script></query></queries></sensor><sensor><category>Network</category><preview_sensor_flag /><hash>435227963</hash><name>IP Route Details</name><hidden_flag>0</hidden_flag><delimiter>|</delimiter><creation_time>2014-12-06T18:00:24</creation_time><exclude_from_parse_flag>1</exclude_from_parse_flag><last_modified_by>Jim Olsen</last_modified_by><string_count>48</string_count><source_hash /><modification_time>2014-12-06T18:00:24</modification_time><ignore_case_flag>1</ignore_case_flag><max_age_seconds>60</max_age_seconds><value_type>String</value_type><cache_row_id /><source_id>0</source_id><deleted_flag /><parameter_definition /><id>737</id><description>Returns IPv4 network routes, filtered to exclude noise. With Flags, Metric, Interface columns.
Example:  172.16.0.0|192.168.1.1|255.255.0.0|UG|100|eth0</description><string_hints /><subcolumns><subcolumn><index>0</index><name>Destination</name><ignore_case_flag>1</ignore_case_flag><exclude_from_parse_flag /><hidden_flag>0</hidden_flag><value_type>IPAddress</value_type></subcolumn><subcolumn><index>1</index><name>Gateway</name><ignore_case_flag>1</ignore_case_flag><exclude_from_parse_flag /><hidden_flag>0</hidden_flag><value_type>IPAddress</value_type></subcolumn><subcolumn><index>2</index><name>Mask</name><ignore_case_flag>1</ignore_case_flag><exclude_from_parse_flag /><hidden_flag>0</hidden_flag><value_type>String</value_type></subcolumn><subcolumn><index>3</index><name>Flags</name><ignore_case_flag>1</ignore_case_flag><exclude_from_parse_flag /><hidden_flag>0</hidden_flag><value_type>String</value_type></subcolumn><subcolumn><index>4</index><name>Metric</name><ignore_case_flag>1</ignore_case_flag><exclude_from_parse_flag /><hidden_flag>0</hidden_flag><value_type>NumericInteger</value_type></subcolumn><subcolumn><index>5</index><name>Interface</name><ignore_case_flag>1</ignore_case_flag><exclude_from_parse_flag /><hidden_flag>0</hidden_flag><value_type>String</value_type></subcolumn></subcolumns><metadata><item><admin_flag>0</admin_flag><name>defined</name><value>Tanium</value></item></metadata><parameters /><queries><query><platform>Windows</platform><script_type>VBScript</script_type><signature /><script>strComputer = &amp;quot;.&amp;quot;
Set objWMIService = GetObject(&amp;quot;winmgmts:&amp;quot; _
    &amp;amp; &amp;quot;{impersonationLevel=impersonate}!\\&amp;quot; &amp;amp; strComputer &amp;amp; &amp;quot;\root\cimv2&amp;quot;)

Set collip = objWMIService.ExecQuery(&amp;quot;select * from win32_networkadapterconfiguration where IPEnabled=&amp;#039;True&amp;#039;&amp;quot;)
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
localhost = &amp;quot;127.0.0.1&amp;quot;

Set colItems = objWMIService.ExecQuery(&amp;quot;Select * from Win32_IP4RouteTable&amp;quot;)

For Each objItem in colItems
    dest = objItem.Destination
    gw = objItem.NextHop
    mask = objItem.Mask
    metric = objItem.Metric1
    flags = objItem.Type
    intf = objItem.InterfaceIndex
    For i = 0 to ipcount
        if gw = ipaddrs(i) and gw &amp;lt;&amp;gt; localhost then
            gw = &amp;quot;0.0.0.0&amp;quot;
        end if
    Next
    if gw &amp;lt;&amp;gt; localhost and dest &amp;lt;&amp;gt; &amp;quot;224.0.0.0&amp;quot; and right(dest,3) &amp;lt;&amp;gt; &amp;quot;255&amp;quot; then
        Wscript.Echo dest &amp;amp; &amp;quot;|&amp;quot; &amp;amp; gw &amp;amp; &amp;quot;|&amp;quot; &amp;amp; mask &amp;amp; &amp;quot;|&amp;quot; &amp;amp; &amp;quot;-&amp;quot; &amp;amp; &amp;quot;|&amp;quot; &amp;amp; metric &amp;amp; &amp;quot;|&amp;quot; &amp;amp; &amp;quot;-&amp;quot;
    end if
Next</script></query><query><platform>Linux</platform><script_type>UnixShell</script_type><signature /><script>route -n | grep -v Kernel | grep -v Destination | awk &amp;#039;{ print $1 &amp;quot;|&amp;quot; $2 &amp;quot;|&amp;quot; $3 &amp;quot;|&amp;quot; $4 &amp;quot;|&amp;quot; $5 &amp;quot;|&amp;quot; $8 }&amp;#039; | grep -v &amp;quot;|127.0.0.1|&amp;quot;
</script></query><query><platform>Mac</platform><script_type>UnixShell</script_type><signature /><script>netstat -rn | grep -v &amp;quot;:&amp;quot; | grep -v Destination | grep -v Routing | grep -v -e &amp;quot;^$&amp;quot; | awk &amp;#039;{ print $1 &amp;quot;|&amp;quot; $2 &amp;quot;||&amp;quot; $3 &amp;quot;||&amp;quot; $6 }&amp;#039; | grep -v &amp;quot;|127.0.0.1|&amp;quot;
</script></query></queries></sensor><sensor><category>Network</category><preview_sensor_flag /><hash>3209138996</hash><name>IP Address</name><hidden_flag>0</hidden_flag><delimiter>,</delimiter><creation_time>2014-12-06T18:00:22</creation_time><exclude_from_parse_flag>1</exclude_from_parse_flag><last_modified_by>Jim Olsen</last_modified_by><string_count>86</string_count><source_hash /><modification_time>2014-12-06T18:00:22</modification_time><ignore_case_flag>1</ignore_case_flag><max_age_seconds>600</max_age_seconds><value_type>IPAddress</value_type><cache_row_id /><source_id>0</source_id><deleted_flag /><parameter_definition /><id>147</id><description>Current IP Addresses of client machine.
Example: 192.168.1.1</description><string_hints /><subcolumns /><metadata><item><admin_flag>0</admin_flag><name>defined</name><value>Tanium</value></item></metadata><parameters /><queries><query><platform>Windows</platform><script_type>WMIQuery</script_type><signature /><script>select IPAddress from win32_networkadapterconfiguration where IPEnabled=&amp;#039;True&amp;#039;</script></query><query><platform>Linux</platform><script_type>UnixShell</script_type><signature /><script>#!/bin/bash
ifconfig | grep -w inet | grep -v 127.0.0.1 | awk &amp;#039;{print $2}&amp;#039; | sed -e &amp;#039;s/addr://&amp;#039;
</script></query><query><platform>Mac</platform><script_type>UnixShell</script_type><signature /><script>#!/bin/bash

ifconfig -a -u |grep &amp;quot;inet&amp;quot; | grep -v &amp;quot;::1&amp;quot; | grep -v &amp;quot;127.0.0.1&amp;quot;| awk &amp;#039;{print $2}&amp;#039; | cut -f1 -d&amp;#039;%&amp;#039;
</script></query></queries></sensor><sensor><category>File System</category><preview_sensor_flag /><hash>1374547302</hash><name>Folder Name Search with RegEx Match</name><hidden_flag>0</hidden_flag><delimiter>,</delimiter><creation_time>2014-12-06T18:00:23</creation_time><exclude_from_parse_flag>1</exclude_from_parse_flag><last_modified_by>Jim Olsen</last_modified_by><string_count>3</string_count><source_hash /><modification_time>2014-12-06T18:00:23</modification_time><ignore_case_flag>1</ignore_case_flag><max_age_seconds>600</max_age_seconds><value_type>String</value_type><cache_row_id /><source_id>0</source_id><deleted_flag /><parameter_definition>{"parameters":[{"restrict":null,"validationExpressions":[{"flags":"","expression":"\\S{3}","helpString":"Value must be at least 3 characters","model":"com.tanium.models::ValidationExpression","parameterType":"com.tanium.models::ValidationExpression"}],"helpString":"Enter the folder name to search for","value":"","promptText":"e.g Program Files","defaultValue":"","label":"Search for Folder Name","maxChars":0,"key":"dirname","model":"com.tanium.components.parameters::TextInputParameter","parameterType":"com.tanium.components.parameters::TextInputParameter"},{"restrict":null,"validationExpressions":[{"flags":"","expression":"\\S{3}","helpString":"Value must be at least 3 characters","model":"com.tanium.models::ValidationExpression","parameterType":"com.tanium.models::ValidationExpression"}],"helpString":"Enter the regular expression to search for.","value":"","promptText":"e.g. test*.exe","defaultValue":"","label":"Regular Expression","maxChars":0,"key":"regexp","model":"com.tanium.components.parameters::TextInputParameter","parameterType":"com.tanium.components.parameters::TextInputParameter"},{"helpString":"Enter Yes/No for case sensitivity of search.","value":"","promptText":"","defaultValue":"","requireSelection":true,"label":"Case sensitive?","key":"casesensitive","values":["No","Yes"],"model":"com.tanium.components.parameters::DropDownParameter","parameterType":"com.tanium.components.parameters::DropDownParameter"},{"helpString":"Enter Yes/No whether the search is global.","value":"","promptText":"","defaultValue":"","requireSelection":true,"label":"Global","key":"global","values":["No","Yes"],"model":"com.tanium.components.parameters::DropDownParameter","parameterType":"com.tanium.components.parameters::DropDownParameter"}],"model":"com.tanium.components.parameters::ParametersArray","parameterType":"com.tanium.components.parameters::ParametersArray"}</parameter_definition><id>381</id><description>Finds the specified folder and provides the full path if the folder exists on the client machine. Takes regular expression to match.
Example: C:\WINDOWS\System32</description><string_hints /><subcolumns /><metadata><item><admin_flag>0</admin_flag><name>defined</name><value>McAfee</value></item></metadata><parameters /><queries><query><platform>Windows</platform><script_type>VBScript</script_type><signature /><script>&amp;#039;========================================
&amp;#039; Folder Name Search with RegEx Match
&amp;#039;========================================
&amp;#039;@INCLUDE=utils/SensorRandomization/SensorRandomizationFunctions.vbs
Option Explicit

SensorRandomize()

Dim Pattern,strRegExp,strGlobalArg,strCaseSensitiveArg
Dim bGlobal,bCaseSensitive

Pattern = unescape(&amp;quot;||dirname||&amp;quot;)
strRegExp = Trim(Unescape(&amp;quot;||regexp||&amp;quot;))
strGlobalArg = Trim(Unescape(&amp;quot;||global||&amp;quot;))
strCaseSensitiveArg = Trim(Unescape(&amp;quot;||casesensitive||&amp;quot;))

bGlobal = GetTrueFalseArg(&amp;quot;global&amp;quot;,strGlobalArg)
bCaseSensitive = GetTrueFalseArg(&amp;quot;casesensitive&amp;quot;,strCaseSensitiveArg)

Const SYSTEM_FOLDER = 1, TEMP_FOLDER = 2, FOR_READING = 1

Dim FSO, WshShell, Drives, Drive, TextStream, OutputFilename, strLine

Set FSO = CreateObject(&amp;quot;Scripting.FileSystemObject&amp;quot;)
Set WshShell = CreateObject(&amp;quot;WScript.Shell&amp;quot;)

OutputFilename = TempName() &amp;#039; a temporary file in system&amp;#039;s temp dir

&amp;#039; Go through file system, refresh output file for filename
If Not FSO.FileExists(OutputFilename) Then
	
	If FSO.FileExists(OutputFilename) Then FSO.DeleteFile OutputFilename

	&amp;#039; Get the collection of local drives.
	Set Drives = FSO.Drives
	For Each Drive in Drives
		If Drive.DriveType = 2 Then &amp;#039; 2 = Fixed drive
			&amp;#039; Run the Dir command that looks for the filename pattern.
			RunCommand &amp;quot;dir &amp;quot; &amp;amp;Chr(34)&amp;amp; Drive.DriveLetter &amp;amp; &amp;quot;:\&amp;quot; &amp;amp; Pattern &amp;amp; Chr(34)&amp;amp;&amp;quot; /a:D /B /S&amp;quot;, OutputFilename, true
		End If
	Next
End If

&amp;#039; Open the output file, echo each line, and then close and delete it.
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

End Function &amp;#039;RegExpMatch


Function GetTrueFalseArg(strArgName,strArgValue)
	&amp;#039; Checks for valid values, will fail with error message
	
	Dim bArgVal
	bArgVal = False
	Select Case LCase(strArgValue)
		Case &amp;quot;true&amp;quot;
			bArgVal = True
		Case &amp;quot;yes&amp;quot;
			bArgVal = True
		Case &amp;quot;false&amp;quot;
			bArgVal = False
		Case &amp;quot;no&amp;quot;
			bArgVal = False
		Case Else
			WScript.Echo &amp;quot;Error: Argument &amp;#039;&amp;quot;&amp;amp;strArgName&amp;amp;&amp;quot;&amp;#039; must be True or False, quitting&amp;quot;
			PrintUsage
	End Select
	GetTrueFalseArg = bArgVal

End Function &amp;#039;GetTrueFalseArg


&amp;#039; Returns the name of a temporary file in the Temp directory.
Function TempName()
	Dim Result
	Do
 		Result = FSO.BuildPath(FSO.GetSpecialFolder(TEMP_FOLDER), FSO.GetTempName())
		WScript.Sleep 200 &amp;#039;avoid potential busy loop
	Loop While FSO.FileExists(Result)
	
	TempName = Result
End Function &amp;#039;TempName

&amp;#039; Runs a command with Cmd.exe and redirects its output to a temporary
&amp;#039; file. The function returns the name of the temporary file that holds
&amp;#039; the command&amp;#039;s output.
Function RunCommand(Command, OutputFilename, b64BitNecessary)
	&amp;#039; 64BitNecessary true when you need to examine the 64-bit areas like system32
	Dim CommandLine,WshShell,strPRogramFilesx86,strDOSCall,objFSO
	Set objFSO = CreateObject(&amp;quot;Scripting.FileSystemObject&amp;quot;)
	Set WshShell = CreateObject(&amp;quot;WScript.Shell&amp;quot;)
	
	strDOSCall = &amp;quot;%ComSpec% /C &amp;quot;
	
	&amp;#039; if 64-bit OS *and* we must examine in 64-bit mode to avoid FS Redirection
	strProgramFilesx86=WshShell.ExpandEnvironmentStrings(&amp;quot;%ProgramFiles%&amp;quot;)
	If objFSO.FolderExists(strProgramFilesx86) And b64BitNecessary Then &amp;#039; quick check for x64
		strDOSCall = FixFileSystemRedirectionForPath(WshShell.ExpandEnvironmentStrings(strDOSCall))
	End If
		
	CommandLine = WshShell.ExpandEnvironmentStrings(strDOSCall &amp;amp; Command &amp;amp; &amp;quot; &amp;gt;&amp;gt; &amp;quot;&amp;quot;&amp;quot; &amp;amp; OutputFileName &amp;amp; &amp;quot;&amp;quot;&amp;quot;&amp;quot;)
	WshShell.Run CommandLine, 0, True
End Function &amp;#039;RunCommand

Function FixFileSystemRedirectionForPath(strFilePath)
&amp;#039; This function will fix a folder location so that
&amp;#039; a 32-bit program can be passed the windows\system32 directory
&amp;#039; as a parameter.
&amp;#039; Even if the sensor or action runs in 64-bit mode, a 32-bit
&amp;#039; program called in a 64-bit environment cannot access
&amp;#039; the system32 directory - it would be redirected to syswow64.
&amp;#039; you would not want to do this for 64-bit programs.
	
	Dim objFSO, strSystem32Location,objShell
	Dim strProgramFilesx86,strNewSystem32Location,strRestOfPath
	Set objFSO = CreateObject(&amp;quot;Scripting.FileSystemObject&amp;quot;)
	Set objShell = CreateObject(&amp;quot;Wscript.Shell&amp;quot;)

	strProgramFilesx86=objShell.ExpandEnvironmentStrings(&amp;quot;%ProgramFiles%&amp;quot;)

	strFilePath = LCase(strFilePath)
	strSystem32Location = LCase(objFSO.GetSpecialFolder(1))
	strProgramFilesx86=objShell.ExpandEnvironmentStrings(&amp;quot;%ProgramFiles(x86)%&amp;quot;)
	
	If objFSO.FolderExists(strProgramFilesx86) Then &amp;#039; quick check for x64
		If InStr(strFilePath,strSystem32Location) = 1 Then
			strRestOfPath = Replace(strFilePath,strSystem32Location,&amp;quot;&amp;quot;)
			strNewSystem32Location = Replace(strSystem32Location,&amp;quot;system32&amp;quot;,&amp;quot;sysnative&amp;quot;)
			strFilePath = strNewSystem32Location&amp;amp;strRestOfPath
		End If
	End If
	FixFileSystemRedirectionForPath = strFilePath
	
	&amp;#039;Cleanup
	Set objFSO = Nothing
End Function &amp;#039;FixFileSystemRedirectionForPath
&amp;#039;------------ INCLUDES after this line. Do not edit past this point -----
&amp;#039;- Begin file: utils/SensorRandomization/SensorRandomizationFunctions.vbs
&amp;#039;&amp;#039; -- Begin Random Sleep Functions -- &amp;#039;&amp;#039;

Dim bSensorRandomizeDebugOutput : bSensorRandomizeDebugOutput = False

Function SensorRandomizeLow()
    Dim intSensorRandomizeWaitLow : intSensorRandomizeWaitLow = 10
    SensorRandomizeRandomSleep(intSensorRandomizeWaitLow)
End Function &amp;#039; SensorRandomizeLow

Function SensorRandomize()
    Dim intSensorRandomizeWaitMed : intSensorRandomizeWaitMed = 20
    SensorRandomizeRandomSleep(intSensorRandomizeWaitMed)
End Function &amp;#039; SensorRandomize

Function SensorRandomizeHigh()
    Dim intSensorRandomizeWaitHigh : intSensorRandomizeWaitHigh = 30
    SensorRandomizeRandomSleep(intSensorRandomizeWaitHigh)
End Function &amp;#039; SensorRandomize

Function SensorRandomizeRandomSleep(intSleepTime)
&amp;#039; sleeps for a random period of time, intSleepTime is in seconds
&amp;#039; if the sensor randomize flag is on
&amp;#039; RandomizeScalingFactor is a multiplier on the values hardcoded in the sensor
&amp;#039; not typically set but can adjust timings per endpoint, optionally
	Dim intSensorRandomizeWaitTime
	Dim objShell,intRandomizeFlag,strRandomizeRegPath,intRandomizeScalingPercentage
	strRandomizeRegPath = SensorRandomizeGetTaniumRegistryPath&amp;amp;&amp;quot;\Sensor Data\Random Sleep&amp;quot;
	
	Set objShell = CreateObject(&amp;quot;WScript.Shell&amp;quot;)
	On Error Resume Next
	intRandomizeFlag = objShell.RegRead(&amp;quot;HKLM\&amp;quot;&amp;amp;strRandomizeRegPath&amp;amp;&amp;quot;\SensorRandomizeFlag&amp;quot;)
	intRandomizeScalingPercentage = objShell.RegRead(&amp;quot;HKLM\&amp;quot;&amp;amp;strRandomizeRegPath&amp;amp;&amp;quot;\SensorRandomizeScalingPercentage&amp;quot;)
	On Error Goto 0
	If intRandomizeFlag &amp;gt; 0 Then
		If intRandomizeScalingPercentage &amp;gt; 0 Then
			intSleepTime = intRandomizeScalingPercentage * .01 * intSleepTime
			SensorRandomizeEcho &amp;quot;Randomize scaling percentage of &amp;quot; _ 
				&amp;amp; intRandomizeScalingPercentage &amp;amp; &amp;quot; applied, new sleep time is &amp;quot; &amp;amp; intSleepTime
		End If
		intSensorRandomizeWaitTime = CLng(intSleepTime) * 1000 &amp;#039; convert to milliseconds
		&amp;#039; wait random interval between 0 and the max
		Randomize(SensorRandomizeTaniumRandomSeed)
		&amp;#039; assign random value to wait time max value
		intSensorRandomizeWaitTime = Int( ( intSensorRandomizeWaitTime + 1 ) * Rnd )
		SensorRandomizeEcho &amp;quot;Sleeping for &amp;quot; &amp;amp; intSensorRandomizeWaitTime &amp;amp; &amp;quot; milliseconds&amp;quot;
		WScript.Sleep(intSensorRandomizeWaitTime)
		SensorRandomizeEcho &amp;quot;Done sleeping, continuing ...&amp;quot;
	Else 
		SensorRandomizeEcho &amp;quot;SensorRandomize Not Enabled - No Op&amp;quot;
	End If
End Function &amp;#039;SensorRandomizeRandomSleep

Function SensorRandomizeTaniumRandomSeed
&amp;#039; for randomizing sensor code, the default seed is not random enough
	Dim timerNum
	timerNum = Timer()
	If timerNum &amp;lt; 1 Then
		SensorRandomizeTaniumRandomSeed = (SensorRandomizeGetTaniumComputerID / Timer() * 10 )
	Else
		SensorRandomizeTaniumRandomSeed = SensorRandomizeGetTaniumComputerID / Timer
	End If
End Function &amp;#039;SensorRandomizeTaniumRandomSeed

Function SensorRandomizeGetTaniumRegistryPath
&amp;#039;SensorRandomizeGetTaniumRegistryPath works in x64 or x32
&amp;#039;looks for a valid Path value

	Dim objShell
	Dim keyNativePath, keyWoWPath, strPath, strFoundTaniumRegistryPath
	  
    Set objShell = CreateObject(&amp;quot;WScript.Shell&amp;quot;)
    
	keyNativePath = &amp;quot;Software\Tanium\Tanium Client&amp;quot;
	keyWoWPath = &amp;quot;Software\Wow6432Node\Tanium\Tanium Client&amp;quot;
    
    &amp;#039; first check the Software key (valid for 32-bit machines, or 64-bit machines in 32-bit mode)
    On Error Resume Next
    strPath = objShell.RegRead(&amp;quot;HKLM\&amp;quot;&amp;amp;keyNativePath&amp;amp;&amp;quot;\Path&amp;quot;)
    On Error Goto 0
	strFoundTaniumRegistryPath = keyNativePath
 
  	If strPath = &amp;quot;&amp;quot; Then
  		&amp;#039; Could not find 32-bit mode path, checking Wow6432Node
  		On Error Resume Next
  		strPath = objShell.RegRead(&amp;quot;HKLM\&amp;quot;&amp;amp;keyWoWPath&amp;amp;&amp;quot;\Path&amp;quot;)
  		On Error Goto 0
		strFoundTaniumRegistryPath = keyWoWPath
  	End If
  	
  	If Not strPath = &amp;quot;&amp;quot; Then
  		SensorRandomizeGetTaniumRegistryPath = strFoundTaniumRegistryPath
  	Else
  		SensorRandomizeGetTaniumRegistryPath = False
  		WScript.Echo &amp;quot;Error: Cannot locate Tanium Registry Path&amp;quot;
  	End If
End Function &amp;#039;SensorRandomizeGetTaniumRegistryPath

Function SensorRandomizeGetTaniumComputerID
&amp;#039;&amp;#039; This function gets the Tanium Computer ID
	Dim objShell
	Dim intClientID,strID,strKeyPath,strValueName
	
    strKeyPath = SensorRandomizeGetTaniumRegistryPath
    strValueName = &amp;quot;ComputerID&amp;quot;
    Set objShell = CreateObject(&amp;quot;WScript.Shell&amp;quot;)
    On Error Resume Next
    intClientID = objShell.RegRead(&amp;quot;HKLM\&amp;quot;&amp;amp;strKeyPath&amp;amp;&amp;quot;\&amp;quot;&amp;amp;strValueName)
    If Err.Number &amp;lt;&amp;gt; 0 Then
    	SensorRandomizeGetTaniumComputerID = 0
    Else
		SensorRandomizeGetTaniumComputerID = SensorRandomizeReinterpretSignedAsUnsigned(intClientID)
	End If
	On Error Goto 0
End Function &amp;#039;SensorRandomizeGetTaniumComputerID

Function SensorRandomizeReinterpretSignedAsUnsigned(ByVal x)
	  If x &amp;lt; 0 Then x = x + 2^32
	  SensorRandomizeReinterpretSignedAsUnsigned = x
End Function &amp;#039;SensorRandomizeReinterpretSignedAsUnsigned

Sub SensorRandomizeEcho(str)
	If bSensorRandomizeDebugOutput = true Then WScript.Echo str
End Sub &amp;#039;SensorRandomizeEcho
&amp;#039; -- End Random Sleep Functions --&amp;#039;
&amp;#039;- End file: utils/SensorRandomization/SensorRandomizationFunctions.vbs</script></query><query><platform>Linux</platform><script_type>UnixShell</script_type><signature /><script>#!/bin/bash
#||dirname||||regexp||||casesensitive||||global||
echo Windows Only
</script></query><query><platform>Mac</platform><script_type>UnixShell</script_type><signature /><script>#!/bin/bash
#||dirname||||regexp||||casesensitive||||global||
echo Windows Only
</script></query></queries></sensor></sensors>

'''
