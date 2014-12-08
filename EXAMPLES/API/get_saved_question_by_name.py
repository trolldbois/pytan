
"""
Get saved question by name
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

# setup the arguments for the handler method
kwargs = {}
kwargs["objtype"] = u'saved_question'
kwargs["name"] = u'Installed Applications'

# call the handler with the get method, passing in kwargs for arguments
response = handler.get(**kwargs)

print ""
print "Type of response: ", type(response)

print ""
print "print of response:"
print response

print ""
print "length of response (number of objects returned): "
print len(response)

print ""
print "print the first object returned in JSON format:"
print response.to_json(response[0])


'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258

Type of response:  <class 'taniumpy.object_types.saved_question_list.SavedQuestionList'>

print of response:
SavedQuestionList, len: 1

length of response (number of objects returned): 
1

print the first object returned in JSON format:
{
  "_type": "saved_question", 
  "action_tracking_flag": 0, 
  "archive_enabled_flag": 0, 
  "archive_owner": {
    "_type": "user", 
    "id": 1, 
    "name": "Jim Olsen"
  }, 
  "expire_seconds": 600, 
  "hidden_flag": 0, 
  "id": 92, 
  "issue_seconds": 120, 
  "issue_seconds_never_flag": 0, 
  "keep_seconds": 3600, 
  "metadata": {
    "_type": "metadata", 
    "item": [
      {
        "_type": "item", 
        "admin_flag": 0, 
        "name": "defined", 
        "value": "Tanium"
      }, 
      {
        "_type": "item", 
        "admin_flag": 0, 
        "name": "category", 
        "value": "Tanium"
      }
    ]
  }, 
  "mod_time": "2014-12-06T18:01:38", 
  "mod_user": {
    "_type": "user", 
    "name": "Jim Olsen"
  }, 
  "most_recent_question_id": 989, 
  "name": "Installed Applications", 
  "packages": {
    "_type": "package_specs", 
    "package_spec": []
  }, 
  "public_flag": 1, 
  "query_text": "Get Installed Applications from all machines", 
  "question": {
    "_type": "question", 
    "action_tracking_flag": 0, 
    "expiration": "2014-12-07T06:12:22", 
    "expire_seconds": 0, 
    "force_computer_id_flag": 0, 
    "hidden_flag": 0, 
    "id": 989, 
    "management_rights_group": {
      "_type": "group", 
      "id": 0
    }, 
    "query_text": "Get Installed Applications from all machines", 
    "saved_question": {
      "_type": "saved_question", 
      "id": 92
    }, 
    "selects": {
      "_type": "selects", 
      "select": [
        {
          "_type": "select", 
          "filter": {
            "_type": "filter", 
            "all_times_flag": 0, 
            "all_values_flag": 0, 
            "delimiter_index": 0, 
            "end_time": "2001-01-01T00:00:00", 
            "ignore_case_flag": 1, 
            "max_age_seconds": 0, 
            "not_flag": 0, 
            "operator": "Less", 
            "start_time": "2001-01-01T00:00:00", 
            "substring_flag": 0, 
            "substring_length": 0, 
            "substring_start": 0, 
            "utf8_flag": 0, 
            "value_type": "String"
          }, 
          "sensor": {
            "_type": "sensor", 
            "category": "Applications", 
            "creation_time": "2014-12-06T18:00:21", 
            "delimiter": "|", 
            "description": "List of the applications and versions of those applications installed on the client machine.\nExample: Mozilla Firefox | 16.0.1", 
            "exclude_from_parse_flag": 1, 
            "hash": 1511329504, 
            "hidden_flag": 0, 
            "id": 41, 
            "ignore_case_flag": 1, 
            "last_modified_by": "Jim Olsen", 
            "max_age_seconds": 600, 
            "metadata": {
              "_type": "metadata", 
              "item": [
                {
                  "_type": "item", 
                  "admin_flag": 0, 
                  "name": "defined", 
                  "value": "Tanium"
                }
              ]
            }, 
            "modification_time": "2014-12-06T18:00:21", 
            "name": "Installed Applications", 
            "queries": {
              "_type": "queries", 
              "query": [
                {
                  "_type": "query", 
                  "platform": "Windows", 
                  "script": "&#039;========================================\n&#039; Installed Applications\n&#039;========================================\n&#039;@INCLUDE=utils/SensorRandomization/SensorRandomizationFunctions.vbs\n&#039; This sensor will return information in the uninstall areas of the registry.\n&#039; There are two hidden columns which can be filtered on despite the fact that\n&#039; they&#039;re hidden, and can also feed actions.\n&#039; if the uninstallstring is msi based, it is altered to show the\n&#039; silent uninstall options and marked as &quot;Is Uninstallable&quot;\n&#039; finally, if it&#039;s a user installed application, it will note that\n&#039; The columns look like:\n&#039; Name|Version|Silent Uninstall String|Uninstallable\n\nSensorRandomize()\n\nSet objRegistry = Getx64RegistryProvider()\n\nkeyPath = &quot;SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall&quot;\nkey64Path = &quot;SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall&quot;\n\nConst HKLM = &amp;H80000002\nConst HKEY_USERS = &amp;H80000003\n\n&#039; list out 32-bit applications on a 64-bit system\nIf RegKeyExists(HKLM, key64Path) Then\n\tobjRegistry.EnumKey HKLM, key64Path, arrSubKeys\n\tGetApplications HKLM,key64path,arrSubKeys\nEnd If\n\n&#039; list out 32-bit applications on a 32-bit system, or 64-bit applications\n&#039; on a 64-bit system.\nIf RegKeyExists(HKLM, keyPath) Then\n\tobjRegistry.EnumKey HKLM, keypath, arrSubKeys\n\tGetApplications HKLM,keypath,arrSubKeys\nEnd If\n\n&#039; Also list out applications installed to HKEY_Users areas\n&#039; which will be appended to the arrSubKeys\nobjRegistry.EnumKey HKEY_USERS, &quot;&quot;, arrUserKeys\nFor Each strSIDkey In arrUserKeys\n\tIf RegKeyExists(HKEY_USERS, strSIDKEY&amp;&quot;\\&quot;&amp;keyPath) Then\n\t\tobjRegistry.EnumKey HKEY_USERS, strSIDkey&amp;&quot;\\&quot;&amp;keyPath, arrSubKeys\n\t\tGetApplications HKEY_USERS,strSIDKey&amp;&quot;\\&quot;&amp;keyPath,arrSubKeys\n\tEnd If\nNext\n\n\nFunction GetApplications(HIVE, keypath,arrSubKeys)\n\tSet applications = CreateObject(&quot;Scripting.Dictionary&quot;)\n\tOn Error Resume Next\n\tFor Each key in arrSubKeys\n\t\tobjRegistry.GetStringValue HIVE,keyPath &amp; &quot;\\&quot; &amp; key,&quot;DisplayName&quot;, displayName\n\t\tobjRegistry.GetStringValue HIVE,keyPath &amp; &quot;\\&quot; &amp; key,&quot;DisplayVersion&quot;, version\n\t\tobjRegistry.GetDWORDValue HIVE,keyPath &amp; &quot;\\&quot; &amp; key,&quot;SystemComponent&quot;, systemComponent\t\n\t\tobjRegistry.GetStringValue HIVE,keyPath &amp; &quot;\\&quot; &amp; key,&quot;UninstallString&quot;, uninstallString\t\n\t\tobjRegistry.GetStringValue HIVE,keyPath &amp; &quot;\\&quot; &amp; key,&quot;ParentKeyName&quot;, parentKey\t\n\t\t&#039; on error goto 0\n\t\t&#039; assume it&#039;s not uninstallable\n\t\tbUninstallable = &quot;Not Uninstallable&quot;\n\t\t\t\t\n\t\tIf displayName &lt;&gt; &quot;&quot; _\n\t\t\tAnd Not IsNull(uninstallString) _ \n\t\t\tAnd IsNull(parentKey) _\n\t\t\tAnd InStr(displayName, &quot;Hotfix&quot;) = 0 _\n\t\t\tAnd InStr(displayName, &quot;Update for&quot;) = 0 _\n\t \t\tAnd InStr(displayName, &quot;Security Update for&quot;) = 0 _\n\t \tThen \n\t \t\tIf InStr(LCase(uninstallString), &quot;msiexec&quot;) Then\n\t \t\t\t&#039; replace any /I with /X and add silent flags\n\t \t\t\tuninstallString = Replace(uninstallString,&quot;/I&quot;,&quot;/X&quot;) &amp; &quot; /qn /noreboot&quot; \n\t  \t\t\tbUninstallable = &quot;Is Uninstallable&quot;\n\t  \t\tEnd If\n\t \t\tIf IsNull(systemComponent) Or systemComponent = 0 Then\n\t\t\t\tIf IsNull(version) Then\n\t\t\t\t\tversion = GetVersionInString(displayName)\n\t\t\t\tEnd If\n\t\t\t\t&#039; This is a multi-column sensor.  Last two columns are hidden.\n\n\t\t\t\tdisplayString = displayName &amp; &quot;|&quot; &amp; version &amp; &quot;|&quot; &amp; uninstallString &amp; &quot;|&quot; &amp; bUninstallable\n\n\t\t\t\t&#039; treat displayString as the unique value - cannot be listed twice.\n\t\t\t\tIf Not applications.Exists(displayString) Then\n\t\t\t\t\tapplications.Add displayString, &quot;&quot;\n\t\t\t\tEnd If \t\n\t\t\tEnd If \t\n\t\tEnd If \n\tNext\n\tOn Error Goto 0\n\t\n\tSortDictionary applications, 1 &#039; This calls a sorting function specific to dictionaries\n\tarrApplicationsKeys = applications.Keys\n\tFor Each application In arrApplicationsKeys\n\t\t&#039; final output of the sensor\n\t\tWScript.Echo CleanCharacters(application)\n\tNext\nEnd Function &#039;GetApplications\n\nFunction RegKeyExists(sHive, sRegKey)\n\tDim aValueNames, aValueTypes\n\tIf objRegistry.EnumValues(sHive, sRegKey, aValueNames, aValueTypes) = 0 Then\n\t\tRegKeyExists = True\n\tElse\n\t\tRegKeyExists = False\n\tEnd If\nEnd Function\n\nFunction SortDictionary(objDict, intSort)\n &#039;   objDict - the dictionary to sort\n &#039;   intSort - the field to sort (1=key, 2=item)\n \n   &#039; declare constants\n   Const dictKey  = 1\n   Const dictItem = 2\n \n   &#039; declare our variables\n   Dim strDict()\n   Dim objKey\n   Dim strKey,strItem\n   Dim X,Y,Z\n \n   &#039; get the dictionary count\n   Z = objDict.Count\n \n   &#039; we need more than one item to warrant sorting\n   If Z &gt; 1 Then\n     &#039; create an array to store dictionary information\n     ReDim strDict(Z,2)\n     X = 0\n     &#039; populate the string array\n     For Each objKey In objDict\n         strDict(X,dictKey)  = CStr(objKey)\n         strDict(X,dictItem) = CStr(objDict(objKey))\n         X = X + 1\n     Next\n \n     &#039; perform a a shell sort of the string array\n     For X = 0 To (Z - 2)\n       For Y = X To (Z - 1)\n         If StrComp(strDict(X,intSort),strDict(Y,intSort),vbTextCompare) &gt; 0 Then\n             strKey  = strDict(X,dictKey)\n             strItem = strDict(X,dictItem)\n             strDict(X,dictKey)  = strDict(Y,dictKey)\n             strDict(X,dictItem) = strDict(Y,dictItem)\n             strDict(Y,dictKey)  = strKey\n             strDict(Y,dictItem) = strItem\n         End If\n       Next\n     Next\n \n     &#039; erase the contents of the dictionary object\n     objDict.RemoveAll\n \n     &#039; repopulate the dictionary with the sorted information\n     For X = 0 To (Z - 1)\n       objDict.Add strDict(X,dictKey), strDict(X,dictItem)\n     Next\n \n   End If\n End Function &#039;SortDictionary\n\nFunction GetVersionInString(ByVal strTemp)\n&#039; examines a string and returns a version string at the end of it\n\tDim strOut\n\tstrOut = &quot;&quot;\n\tIf Not IsNull(strTemp) Then\n\t\tstrTemp = StrReverse(strTemp)\n\t\tDim strLookAtChar,intCurPos\n\t\tDim bNumbersStartMarked : bNumbersStartMarked = False\n\n\t\tFor intCurPos = 1 To Len(strTemp)\t\t\n\t\t\tstrLookAtChar = Mid(strTemp,intCurPos,1)\n\t\t\tIf IsNumeric(strLookAtChar) Or strLookAtChar = &quot;.&quot; Or strLookAtChar = &quot;-&quot; Then\n\t\t\t\tbNumbersStartMarked = True\n\t\t\t\tstrOut = strOut &amp; strLookAtChar\n\t\t\tEnd If\n\t\tIf bNumbersStartMarked And ( (Not IsNumeric(strLookAtChar) And strLookAtChar &lt;&gt; &quot;.&quot; And strLookAtChar &lt;&gt; &quot;-&quot;) ) Then\n\t\t\tExit For\n\t\tEnd If\t\n\t\tNext\n\t\tstrOut = StrReverse(strOut)\n\tElse\n\t\tstrOut = &quot;&quot;\n\tEnd If\n\t\n\tIf Len(strOut) = 0 Then strOut = &quot;N/A&quot;\n\t\n\tGetVersionInString = strOut\n\t\nEnd Function &#039;GetVersionInString\n\nFunction CleanCharacters(strTest)\n&#039; String returned will not have characters in the output which\n&#039; are not friendly to the console app\n\tstrPattern = &quot;[^\\x20-\\x7E]&quot;\n\tstrReplace = &quot;&quot;\n\tSet objRegExp = New RegExp\n\tobjRegExp.Global = True\n\tobjRegExp.IgnoreCase = True\n\tobjRegExp.Pattern = strPattern\n\tobjRegExp.Global = True\n\tCleanCharacters = objRegExp.Replace(strTest, strReplace)\nEnd Function\n\nFunction Getx64RegistryProvider\n    &#039; Returns the best available registry provider:  32 bit on 32 bit systems, 64 bit on 64 bit systems\n    Dim objWMIService, colItems, objItem, iArchType, objCtx, objLocator, objServices, objRegProv\n    Set objWMIService = GetObject(&quot;winmgmts:\\\\.\\root\\CIMV2&quot;)\n    Set colItems = objWMIService.ExecQuery(&quot;Select SystemType from Win32_ComputerSystem&quot;)    \n    For Each objItem In colItems\n        If InStr(LCase(objItem.SystemType), &quot;x64&quot;) &gt; 0 Then\n            iArchType = 64\n        Else\n            iArchType = 32\n        End If\n    Next\n    \n    Set objCtx = CreateObject(&quot;WbemScripting.SWbemNamedValueSet&quot;)\n    objCtx.Add &quot;__ProviderArchitecture&quot;, iArchType\n    Set objLocator = CreateObject(&quot;Wbemscripting.SWbemLocator&quot;)\n    Set objServices = objLocator.ConnectServer(&quot;&quot;,&quot;root\\default&quot;,&quot;&quot;,&quot;&quot;,,,,objCtx)\n    Set objRegProv = objServices.Get(&quot;StdRegProv&quot;)   \n    \n    Set Getx64RegistryProvider = objRegProv\nEnd Function &#039; Getx64RegistryProvider\n&#039;------------ INCLUDES after this line. Do not edit past this point -----\n&#039;- Begin file: utils/SensorRandomization/SensorRandomizationFunctions.vbs\n&#039;&#039; -- Begin Random Sleep Functions -- &#039;&#039;\n\nDim bSensorRandomizeDebugOutput : bSensorRandomizeDebugOutput = False\n\nFunction SensorRandomizeLow()\n    Dim intSensorRandomizeWaitLow : intSensorRandomizeWaitLow = 10\n    SensorRandomizeRandomSleep(intSensorRandomizeWaitLow)\nEnd Function &#039; SensorRandomizeLow\n\nFunction SensorRandomize()\n    Dim intSensorRandomizeWaitMed : intSensorRandomizeWaitMed = 20\n    SensorRandomizeRandomSleep(intSensorRandomizeWaitMed)\nEnd Function &#039; SensorRandomize\n\nFunction SensorRandomizeHigh()\n    Dim intSensorRandomizeWaitHigh : intSensorRandomizeWaitHigh = 30\n    SensorRandomizeRandomSleep(intSensorRandomizeWaitHigh)\nEnd Function &#039; SensorRandomize\n\nFunction SensorRandomizeRandomSleep(intSleepTime)\n&#039; sleeps for a random period of time, intSleepTime is in seconds\n&#039; if the sensor randomize flag is on\n&#039; RandomizeScalingFactor is a multiplier on the values hardcoded in the sensor\n&#039; not typically set but can adjust timings per endpoint, optionally\n\tDim intSensorRandomizeWaitTime\n\tDim objShell,intRandomizeFlag,strRandomizeRegPath,intRandomizeScalingPercentage\n\tstrRandomizeRegPath = SensorRandomizeGetTaniumRegistryPath&amp;&quot;\\Sensor Data\\Random Sleep&quot;\n\t\n\tSet objShell = CreateObject(&quot;WScript.Shell&quot;)\n\tOn Error Resume Next\n\tintRandomizeFlag = objShell.RegRead(&quot;HKLM\\&quot;&amp;strRandomizeRegPath&amp;&quot;\\SensorRandomizeFlag&quot;)\n\tintRandomizeScalingPercentage = objShell.RegRead(&quot;HKLM\\&quot;&amp;strRandomizeRegPath&amp;&quot;\\SensorRandomizeScalingPercentage&quot;)\n\tOn Error Goto 0\n\tIf intRandomizeFlag &gt; 0 Then\n\t\tIf intRandomizeScalingPercentage &gt; 0 Then\n\t\t\tintSleepTime = intRandomizeScalingPercentage * .01 * intSleepTime\n\t\t\tSensorRandomizeEcho &quot;Randomize scaling percentage of &quot; _ \n\t\t\t\t&amp; intRandomizeScalingPercentage &amp; &quot; applied, new sleep time is &quot; &amp; intSleepTime\n\t\tEnd If\n\t\tintSensorRandomizeWaitTime = CLng(intSleepTime) * 1000 &#039; convert to milliseconds\n\t\t&#039; wait random interval between 0 and the max\n\t\tRandomize(SensorRandomizeTaniumRandomSeed)\n\t\t&#039; assign random value to wait time max value\n\t\tintSensorRandomizeWaitTime = Int( ( intSensorRandomizeWaitTime + 1 ) * Rnd )\n\t\tSensorRandomizeEcho &quot;Sleeping for &quot; &amp; intSensorRandomizeWaitTime &amp; &quot; milliseconds&quot;\n\t\tWScript.Sleep(intSensorRandomizeWaitTime)\n\t\tSensorRandomizeEcho &quot;Done sleeping, continuing ...&quot;\n\tElse \n\t\tSensorRandomizeEcho &quot;SensorRandomize Not Enabled - No Op&quot;\n\tEnd If\nEnd Function &#039;SensorRandomizeRandomSleep\n\nFunction SensorRandomizeTaniumRandomSeed\n&#039; for randomizing sensor code, the default seed is not random enough\n\tDim timerNum\n\ttimerNum = Timer()\n\tIf timerNum &lt; 1 Then\n\t\tSensorRandomizeTaniumRandomSeed = (SensorRandomizeGetTaniumComputerID / Timer() * 10 )\n\tElse\n\t\tSensorRandomizeTaniumRandomSeed = SensorRandomizeGetTaniumComputerID / Timer\n\tEnd If\nEnd Function &#039;SensorRandomizeTaniumRandomSeed\n\nFunction SensorRandomizeGetTaniumRegistryPath\n&#039;SensorRandomizeGetTaniumRegistryPath works in x64 or x32\n&#039;looks for a valid Path value\n\n\tDim objShell\n\tDim keyNativePath, keyWoWPath, strPath, strFoundTaniumRegistryPath\n\t  \n    Set objShell = CreateObject(&quot;WScript.Shell&quot;)\n    \n\tkeyNativePath = &quot;Software\\Tanium\\Tanium Client&quot;\n\tkeyWoWPath = &quot;Software\\Wow6432Node\\Tanium\\Tanium Client&quot;\n    \n    &#039; first check the Software key (valid for 32-bit machines, or 64-bit machines in 32-bit mode)\n    On Error Resume Next\n    strPath = objShell.RegRead(&quot;HKLM\\&quot;&amp;keyNativePath&amp;&quot;\\Path&quot;)\n    On Error Goto 0\n\tstrFoundTaniumRegistryPath = keyNativePath\n \n  \tIf strPath = &quot;&quot; Then\n  \t\t&#039; Could not find 32-bit mode path, checking Wow6432Node\n  \t\tOn Error Resume Next\n  \t\tstrPath = objShell.RegRead(&quot;HKLM\\&quot;&amp;keyWoWPath&amp;&quot;\\Path&quot;)\n  \t\tOn Error Goto 0\n\t\tstrFoundTaniumRegistryPath = keyWoWPath\n  \tEnd If\n  \t\n  \tIf Not strPath = &quot;&quot; Then\n  \t\tSensorRandomizeGetTaniumRegistryPath = strFoundTaniumRegistryPath\n  \tElse\n  \t\tSensorRandomizeGetTaniumRegistryPath = False\n  \t\tWScript.Echo &quot;Error: Cannot locate Tanium Registry Path&quot;\n  \tEnd If\nEnd Function &#039;SensorRandomizeGetTaniumRegistryPath\n\nFunction SensorRandomizeGetTaniumComputerID\n&#039;&#039; This function gets the Tanium Computer ID\n\tDim objShell\n\tDim intClientID,strID,strKeyPath,strValueName\n\t\n    strKeyPath = SensorRandomizeGetTaniumRegistryPath\n    strValueName = &quot;ComputerID&quot;\n    Set objShell = CreateObject(&quot;WScript.Shell&quot;)\n    On Error Resume Next\n    intClientID = objShell.RegRead(&quot;HKLM\\&quot;&amp;strKeyPath&amp;&quot;\\&quot;&amp;strValueName)\n    If Err.Number &lt;&gt; 0 Then\n    \tSensorRandomizeGetTaniumComputerID = 0\n    Else\n\t\tSensorRandomizeGetTaniumComputerID = SensorRandomizeReinterpretSignedAsUnsigned(intClientID)\n\tEnd If\n\tOn Error Goto 0\nEnd Function &#039;SensorRandomizeGetTaniumComputerID\n\nFunction SensorRandomizeReinterpretSignedAsUnsigned(ByVal x)\n\t  If x &lt; 0 Then x = x + 2^32\n\t  SensorRandomizeReinterpretSignedAsUnsigned = x\nEnd Function &#039;SensorRandomizeReinterpretSignedAsUnsigned\n\nSub SensorRandomizeEcho(str)\n\tIf bSensorRandomizeDebugOutput = true Then WScript.Echo str\nEnd Sub &#039;SensorRandomizeEcho\n&#039; -- End Random Sleep Functions --&#039;\n&#039;- End file: utils/SensorRandomization/SensorRandomizationFunctions.vbs", 
                  "script_type": "VBScript"
                }, 
                {
                  "_type": "query", 
                  "platform": "Linux", 
                  "script": "#!/bin/sh\n# Detects which OS and if it is Linux then it will detect which Linux\n# Distribution.\n\n# Can be used as a starting point for shell scripts that need to work differently on\n# Mac, and various flavors of Linux\n\nOS=`uname -s`\n\nGetVersionFromFile()\n{\n    VERSION=`cat $1 | tr &quot;\\n&quot; &#039; &#039; | sed s/.*VERSION.*=\\ // `\n}\n\nif [ &quot;${OS}&quot; = &quot;Linux&quot; ] ; then\n    KERNEL=`uname -r`\n    if [ -f /etc/redhat-release ] ; then\n        # Redhat based system\n        rpm -qa --queryformat &quot;%{NAME}|%{VERSION}|nothing|Not Uninstallable\\n&quot;\n    elif [ -f /etc/SuSE-release ] ; then\n        # SuSE / OpenSuSE based system\n        rpm -qa --queryformat &quot;%{NAME}|%{VERSION}|nothing|Not Uninstallable\\n&quot;\n    elif [ -f /etc/lsb-release ] ; then\n        # Usually Ubuntu -- this is a Linux Standard Based system, which\n        # Ubuntu is by far the biggest.  But general LSB commands should work\n        dpkg -l | awk &#039;{print $2&quot;|&quot;$3&quot;|nothing|Not Uninstallable&quot;}&#039;\n    elif [ -f /etc/debian_version ] ; then\n        # Debian -- note that Ubuntu is Debian based, but Debian does not have a\n        # lsb-release file\n        dpkg -l | awk &#039;{print $2&quot;|&quot;$3&quot;|nothing|Not Uninstallable&quot;}&#039;\n        #else\n\t# a less common distribution.  Most all really popular distributions will\n        # be caught by the tree above.\n    fi\n#else\n   # not Linux -- could be anything, BSD / Solaris / AIX / etc\nfi\n\necho ${OSSTR}\n", 
                  "script_type": "UnixShell"
                }, 
                {
                  "_type": "query", 
                  "platform": "Mac", 
                  "script": "#!/bin/bash\n\nnotcontains() {\n    string=&quot;$1&quot;\n    substring=&quot;$2&quot;\n    if test &quot;${string#*$substring}&quot; != &quot;$string&quot;\n    then\n        return 1    # $substring is not in $string\n    else\n        return 0    # $substring is in $string\n    fi\n}\n\nftemp=$(mktemp -t &#039;apps.xml&#039;)\nsystem_profiler -xml SPApplicationsDataType &gt; &quot;$ftemp&quot;\n\ncount=1\n\nwhile true\ndo\n        app=`/usr/libexec/PlistBuddy -c &quot;Print :0:_items:$count:_name&quot; $ftemp 2&gt;/dev/null`\n        version=`/usr/libexec/PlistBuddy -c &quot;Print :0:_items:$count:version&quot; $ftemp 2&gt;/dev/null`\n        if [ -z &quot;$app&quot; ]; then\n                break\n        fi\n        test=&quot;VMware&quot;\n        if notcontains &quot;$version&quot; &quot;$test&quot;; then\n                echo $app&quot;|&quot;$version&quot;|nothing|Not Uninstallable&quot;\n        fi\n        let count=count+1\ndone\nrm -rf &quot;$ftemp&quot;\n", 
                  "script_type": "UnixShell"
                }
              ]
            }, 
            "source_id": 0, 
            "string_count": 3215, 
            "subcolumns": {
              "_type": "subcolumns", 
              "subcolumn": [
                {
                  "_type": "subcolumn", 
                  "hidden_flag": 0, 
                  "ignore_case_flag": 1, 
                  "index": 0, 
                  "name": "Name", 
                  "value_type": "String"
                }, 
                {
                  "_type": "subcolumn", 
                  "hidden_flag": 0, 
                  "ignore_case_flag": 1, 
                  "index": 1, 
                  "name": "Version", 
                  "value_type": "Version"
                }, 
                {
                  "_type": "subcolumn", 
                  "hidden_flag": 1, 
                  "ignore_case_flag": 1, 
                  "index": 2, 
                  "name": "Silent Uninstall String", 
                  "value_type": "String"
                }, 
                {
                  "_type": "subcolumn", 
                  "hidden_flag": 1, 
                  "ignore_case_flag": 1, 
                  "index": 3, 
                  "name": "Uninstallable", 
                  "value_type": "String"
                }
              ]
            }, 
            "value_type": "String"
          }
        }
      ]
    }, 
    "skip_lock_flag": 0, 
    "user": {
      "_type": "user", 
      "id": 2, 
      "name": "Tanium User"
    }
  }, 
  "row_count_flag": 0, 
  "sort_column": 0, 
  "user": {
    "_type": "user", 
    "id": 1, 
    "name": "Jim Olsen"
  }
}

'''
