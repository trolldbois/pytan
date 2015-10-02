Create Saved Question From JSON Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Help for Create Saved Question From JSON](#user-content-help-for-create-saved-question-from-json)
  * [Export saved_question id 1 as JSON](#user-content-export-saved_question-id-1-as-json)
  * [Change name or url_regex in the JSON](#user-content-change-name-or-url_regex-in-the-json)
  * [Create a new saved_question from the modified JSON file](#user-content-create-a-new-saved_question-from-the-modified-json-file)

---------------------------

# Help for Create Saved Question From JSON

  * Print the help for create_saved_question_from_json.py
  * All scripts in bin/ will supply help if -h is on the command line
  * If passing in a parameter with a space or a special character, you need to surround it with quotes properly. On Windows this means double quotes. On Linux/Mac, this means single or double quotes, depending on what kind of character escaping you need.
  * If running this script on Linux or Mac, use the python scripts directly as the bin/create_saved_question_from_json.py
  * If running this script on Windows, use the batch script in the winbin/create_saved_question_from_json.bat so that python is called correctly.

```bash
create_saved_question_from_json.py -h
```

```
usage: create_saved_question_from_json.py [-h] [-u USERNAME] [-p PASSWORD]
                                          [--session_id SESSION_ID]
                                          [--host HOST] [--port PORT]
                                          [-l LOGLEVEL] [--debugformat]
                                          [--debug_method_locals]
                                          [--record_all_requests]
                                          [--stats_loop_enabled]
                                          [--http_auth_retry]
                                          [--http_retry_count HTTP_RETRY_COUNT]
                                          [--pytan_user_config PYTAN_USER_CONFIG]
                                          [--force_server_version FORCE_SERVER_VERSION]
                                          -j JSON_FILE

Create an object of type: saved_question from a JSON file

optional arguments:
  -h, --help            show this help message and exit

Handler Authentication:
  -u USERNAME, --username USERNAME
                        Name of user (default: None)
  -p PASSWORD, --password PASSWORD
                        Password of user (default: None)
  --session_id SESSION_ID
                        Session ID to authenticate with instead of
                        username/password (default: None)
  --host HOST           Hostname/ip of SOAP Server (default: None)
  --port PORT           Port to use when connecting to SOAP Server (default:
                        443)

Handler Options:
  -l LOGLEVEL, --loglevel LOGLEVEL
                        Logging level to use, increase for more verbosity
                        (default: 0)
  --debugformat         Enable debug format for logging (default: False)
  --debug_method_locals
                        Enable debug logging for each methods local variables
                        (default: False)
  --record_all_requests
                        Record all requests in
                        handler.session.ALL_REQUESTS_RESPONSES (default:
                        False)
  --stats_loop_enabled  Enable the statistics loop (default: False)
  --http_auth_retry     Disable retry on HTTP authentication failures
                        (default: True)
  --http_retry_count HTTP_RETRY_COUNT
                        Retry count for HTTP failures/invalid responses
                        (default: 5)
  --pytan_user_config PYTAN_USER_CONFIG
                        PyTan User Config file to use for PyTan arguments
                        (defaults to: ~/.pytan_config.json) (default: )
  --force_server_version FORCE_SERVER_VERSION
                        Force PyTan to consider the server version as this,
                        instead of relying on the server version derived from
                        the server info page. (default: )

Create Saved question from JSON Options:
  -j JSON_FILE, --json JSON_FILE
                        JSON file to use for creating the object (default: )
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Export saved_question id 1 as JSON

  * Get the first saved_question object
  * Save the results to a JSON file

```bash
bin/get_saved_question.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 --id 1 --file "/tmp/out.json" --export_format json
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
Found items:  SavedQuestionList, len: 1
Report file '/tmp/out.json' written with 11886 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /tmp/out.json exists, content:

```
{
  "_type": "saved_questions", 
  "saved_question": [
    {
      "_type": "saved_question", 
      "action_tracking_flag": 0, 
      "archive_enabled_flag": 0, 
      "archive_owner": {
        "_type": "user"
      }, 
...trimmed for brevity...
```

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Change name or url_regex in the JSON

  * Add CMDLINE TEST to name or url_regex in the JSON file

```bash
perl -p -i -e 's/^(      "(name|url_regex)": ".*)"/$1 CMDLINE TEST 3211"/gm' /tmp/out.json && cat /tmp/out.json
```

```
{
  "_type": "saved_questions", 
  "saved_question": [
    {
      "_type": "saved_question", 
      "action_tracking_flag": 0, 
      "archive_enabled_flag": 0, 
      "archive_owner": {
        "_type": "user"
      }, 
      "expire_seconds": 600, 
      "hidden_flag": 0, 
      "id": 1, 
      "issue_seconds": 120, 
      "issue_seconds_never_flag": 0, 
      "keep_seconds": 0, 
      "mod_time": "2015-09-14T13:39:17", 
      "mod_user": {
        "_type": "user", 
        "name": "Administrator"
      }, 
      "most_recent_question_id": 16056, 
      "name": "Has Tanium Standard Utilities CMDLINE TEST 3211", 
      "packages": {
        "_type": "package_specs", 
        "package_spec": [
          {
            "_type": "package_spec", 
            "id": 23, 
            "name": "Distribute Tanium Standard Utilities"
          }
        ]
      }, 
      "public_flag": 1, 
      "query_text": "Get Has Tanium Standard Utilities from all machines", 
      "question": {
        "_type": "question", 
        "action_tracking_flag": 0, 
        "expiration": "2015-10-02T19:49:24", 
        "expire_seconds": 0, 
        "force_computer_id_flag": 0, 
        "hidden_flag": 0, 
        "id": 16056, 
        "management_rights_group": {
          "_type": "group", 
          "id": 0
        }, 
        "query_text": "Get Has Tanium Standard Utilities from all machines", 
        "saved_question": {
          "_type": "saved_question", 
          "id": 1
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
                "category": "Tanium", 
                "creation_time": "2015-09-14T13:39:11", 
                "delimiter": ",", 
                "description": "Returns whether a machine has the Tanium Standard Utilities\nExample: Yes", 
                "exclude_from_parse_flag": 1, 
                "hash": 1782389954, 
                "hidden_flag": 0, 
                "id": 190, 
                "ignore_case_flag": 1, 
                "last_modified_by": "Administrator", 
                "max_age_seconds": 900, 
                "modification_time": "2015-09-14T13:39:11", 
                "name": "Has Tanium Standard Utilities", 
                "queries": {
                  "_type": "queries", 
                  "query": [
                    {
                      "_type": "query", 
                      "platform": "Windows", 
                      "script": "&#039;========================================\n&#039; Has Tanium Standard Utilities\n&#039;========================================\n\n&#039; this action will look to see if the client has\n&#039; all necessary standard utilities files\n\nOption Explicit\n&#039;--------------------\n&#039; Set These Variables\nDim strDesiredVersion,strDesiredFCIVVersion,strDesiredGrepBinaryVersion\nDim strDesiredGrepDepVersion,strGrepDepFileVersion,strGrepBinaryFileVersion\n\n&#039; a string value which is a version like\n&#039; 4.2.314.7111\n&#039; which is used to determine whether the bundle has the correct version\n&#039; updating the content will cause the bundle number to change and all files will\n&#039; be sent to the endpoint again. This is to handle the case where\n&#039; binary files are not versioned, such as with Yara\n\n&#039; The top line of the version file\n&#039;Tanium File Version: &lt;version string below&gt;\nstrDesiredVersion = &quot;6.5.2.0164&quot;\n\n&#039; -------------------\n&#039; Binaries we can version\nstrDesiredGrepBinaryVersion = &quot;2.5.4.3331&quot;\nstrDesiredGrepDepVersion = &quot;1.12.2872.39125&quot;\n\nDim objFSO\nDim strDirToCheck,objTextFile\nDim bHasAllLatestFiles,arrTextFilesToCheck,strFile,strVersionLine,strFileVersion\nDim strFCIVFile,strFCIVFileVersion,strGrepBinary,strGrepDep,strHandleTool,strListDLLs2\nDim strListDLLs,strStreamsTool,strAutorunsTool\nDim strYara,strYarac\n\nSet objFSO = CreateObject(&quot;Scripting.FileSystemObject&quot;)\n\nstrDirToCheck = GetTaniumDir(&quot;Tools\\StdUtils&quot;)\n\narrTextFilesToCheck = Array(&quot;copy-to-tanium-dir-predist.vbs&quot;,&quot;runas-allusers-wrapper.vbs&quot;,&quot;ver\\bundle.cfg&quot;)\n\n&#039; Grep is required\nstrGrepBinary=strDirToCheck&amp;&quot;grep\\bin\\grep.exe&quot;\nstrGrepDep=strDirToCheck&amp;&quot;grep\\bin\\libiconv2.dll&quot;\n\n&#039;Yara binaries are required\nstrYara=strDirToCheck&amp;&quot;yara\\yara&quot;&amp;GetBitness&amp;&quot;.exe&quot;\nstrYarac=strDirToCheck&amp;&quot;yara\\yarac&quot;&amp;GetBitness&amp;&quot;.exe&quot;\n\nbHasAllLatestFiles = True\nFor Each strFile In arrTextFilesToCheck\n\tIf Not objFSO.FileExists(strDirToCheck&amp;strFile) Then\n\t\tWScript.Echo &quot;Missing &quot; &amp; strFile\n\t\tbHasAllLatestFiles = False\n\tEnd If\n\tIf objFSO.FileExists(strDirToCheck&amp;strFile) Then\n\t\tSet objTextFile = objFSO.OpenTextFile(strDirToCheck&amp;strFile)\n\t\tstrVersionLine = LCase(objTextFile.ReadLine()) &#039; version is at top of line\n\t\tIf Not InStr(strVersionLine,&quot;tanium file version:&quot;) &gt; 0 Then &#039; must have a version number in top line\n\t\t\tWScript.Echo strFile&amp;&quot; is not versioned on line 1&quot;\n\t\t\tbHasAllLatestFiles = False\n\t\tElse &#039; we have a version number, not split to check\n\t\t\tstrFileVersion = Split(strVersionLine,&quot;tanium file version:&quot;)(1)\n\t\t\tIf Trim(strFileVersion) &lt;&gt; Trim(strDesiredVersion) Then\n\t\t\t\tWScript.Echo strFile&amp;&quot; version: &quot;&amp;strFileVersion&amp;&quot;, needs: &quot;&amp;strDesiredVersion\n\t\t\t\tbHasAllLatestFiles = False\n\t\t\tEnd If\n\t\tEnd If\n\t\tobjTextFile.Close\n\tEnd If\nNext\n\n&#039; check a Grep dependency\nIf Not objFSO.FileExists(strGrepDep) Then\n\tWScript.Echo &quot;Missing &quot; &amp; strGrepDep\n\tbHasAllLatestFiles = False\nEnd If\nIf objFSO.FileExists(strGrepDep) Then\n\n\tstrGrepDepFileVersion = objFSO.GetFileVersion(strGrepDep)\n\tIf Not strGrepDepFileVersion = strDesiredGrepDepVersion Then\n\t\tbHasAllLatestFiles = False\n\t\tWScript.Echo strGrepDep &amp;&quot; version: &quot;&amp;strGrepDepFileVersion&amp;&quot;, needs: &quot;&amp;strDesiredGrepDepVersion\n\tEnd If\nEnd If\n\n\n&#039; check Grep binary\nIf Not objFSO.FileExists(strGrepBinary) Then\n\tWScript.Echo &quot;Missing &quot; &amp; strGrepBinary\n\tbHasAllLatestFiles = False\nEnd If\nIf objFSO.FileExists(strGrepBinary) Then\n\tstrGrepBinaryFileVersion = GetFileVersion(strGrepBinary)\n\tIf Not strGrepBinaryFileVersion = strDesiredGrepBinaryVersion Then\n\t\tbHasAllLatestFiles = False\n\t\tWScript.Echo strGrepBinary &amp;&quot; version: &quot;&amp;strGrepBinaryFileVersion&amp;&quot;, needs: &quot;&amp;strDesiredGrepBinaryVersion\n\tEnd If\nEnd If\n\nIf Not objFSO.FileExists(strYara) Then\n\tbHasAllLatestFiles = False\n\tWScript.Echo &quot;Missing &quot; &amp; strYara\nEnd If\n\nIf Not objFSO.FileExists(strYarac) Then\n\tbHasAllLatestFiles = False\n\tWScript.Echo &quot;Missing &quot; &amp; strYarac\nEnd If\n\nIf bHasAllLatestFiles Then\n\tWScript.Echo &quot;Yes&quot;\nElse\n\tWScript.Echo &quot;No&quot;\nEnd If\n\nFunction GetFileVersion(strPath)\n\tDim objFSO\n\tSet objFSO = CreateObject(&quot;Scripting.FileSystemObject&quot;)\n\tIf objFSO.FileExists(strPath) Then\n\t\tGetFileVersion = objFSO.GetFileVersion(strPath)\n\tElse\n\t\tGetFileVersion = -1\n\tEnd If\nEnd Function &#039;GetFileVersion\n\nFunction GetTaniumDir(strSubDir)\n\tDim strComputer, key32path, key64path, keyPath, reg\n\tDim strPath\n\tstrComputer = &quot;.&quot;\n\tConst HKLM = &amp;h80000002\n\n\tkey32Path = &quot;Software\\Tanium\\Tanium Client&quot;\n\tkey64Path = &quot;Software\\Wow6432Node\\Tanium\\Tanium Client&quot;\n\n\tSet reg=GetObject(&quot;winmgmts:{impersonationLevel=impersonate}!\\\\&quot; &amp; strComputer &amp; &quot;\\root\\default:StdRegProv&quot;)\n\n\tIf RegKeyExists(reg, HKLM, key64Path) Then\n\t\tkeyPath = key64Path\n\tElseIf RegKeyExists(reg, HKLM, key32Path) Then\n\t\tkeyPath = key32Path\n\tEnd If\n\n\treg.GetStringValue HKLM,keyPath,&quot;Path&quot;, strPath\n\n\tIf strSubDir &lt;&gt; &quot;&quot; Then\n\t\tstrSubDir = &quot;\\&quot; &amp; strSubDir\n\tEnd If\n\n\tDim fso\n\tSet fso = WScript.CreateObject(&quot;Scripting.FileSystemObject&quot;)\n\tIf fso.FolderExists(strPath) Then\n\t\tIf Not fso.FolderExists(strPath &amp; strSubDir) Then\n\t\t\tfso.CreateFolder(strPath &amp; strSubDir)\n\t\tEnd If\n\t\tGetTaniumDir = strPath &amp; strSubDir &amp; &quot;\\&quot;\n\tEnd If\nEnd Function\n\nFunction RegKeyExists(objRegistry, sHive, sRegKey)\n\tDim aValueNames, aValueTypes\n\tIf objRegistry.EnumValues(sHive, sRegKey, aValueNames, aValueTypes) = 0 Then\n\t\tRegKeyExists = True\n\tElse\n\t\tRegKeyExists = False\n\tEnd If\nEnd Function\n\n\nFunction GetBitness\n\tIf Not Is64 Then\n\t\tGetBitness = &quot;32&quot;\n\tElse\n\t\tGetBitness = &quot;64&quot;\n\tEnd If\nEnd Function &#039;GetBitness\n\nFunction Is64\n\tDim objWMIService, colItems, objItem\n\tSet objWMIService = GetObject(&quot;winmgmts:\\\\.\\root\\CIMV2&quot;)\n\tSet colItems = objWMIService.ExecQuery(&quot;Select SystemType from Win32_ComputerSystem&quot;)\n\tFor Each objItem In colItems\n\t\tIf InStr(LCase(objItem.SystemType), &quot;x64&quot;) &gt; 0 Then\n\t\t\tIs64 = True\n\t\tElse\n\t\t\tIs64 = False\n\t\tEnd If\n\tNext\nEnd Function &#039; Is64", 
                      "script_type": "VBScript"
                    }, 
                    {
                      "_type": "query", 
                      "platform": "Linux", 
                      "script": "#!/bin/sh\n\n# THIS IS A STUB - NOT INTENDED AS FUNCTIONAL - NA\n# \n# \n\necho &quot;N/A on Linux&quot;\n", 
                      "script_type": "UnixShell"
                    }, 
                    {
                      "_type": "query", 
                      "platform": "Mac", 
                      "script": "#!/bin/sh\n\n# THIS IS A STUB - NOT INTENDED AS FUNCTIONAL - NA\n# \n# \n\necho &quot;N/A on Mac&quot;\n", 
                      "script_type": "UnixShell"
                    }, 
                    {
                      "_type": "query", 
                      "platform": "Solaris", 
                      "script": "#!/bin/sh\n\n# THIS IS A STUB - NOT INTENDED AS FUNCTIONAL - NA\n# \n# \n\necho &quot;N/A on Solaris&quot;\n", 
                      "script_type": "UnixShell"
                    }, 
                    {
                      "_type": "query", 
                      "platform": "AIX", 
                      "script": "#!/bin/sh\n\n# THIS IS A STUB - NOT INTENDED AS FUNCTIONAL - NA\n# \n# \n\necho &quot;N/A on AIX&quot;\n", 
                      "script_type": "UnixShell"
                    }
                  ]
                }, 
                "source_id": 0, 
                "string_count": 5, 
                "value_type": "String"
              }
            }
          ]
        }, 
        "skip_lock_flag": 0, 
        "user": {
          "_type": "user", 
          "id": 1, 
          "name": "Administrator"
        }
      }, 
      "row_count_flag": 0, 
      "sort_column": 0, 
      "user": {
        "_type": "user", 
        "id": 1, 
        "name": "Administrator"
      }
    }
  ]
}
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist
    * Valid: **True**
    * Messages: File /tmp/out.json exists

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


# Create a new saved_question from the modified JSON file

```bash
bin/create_saved_question_from_json.py -u Administrator -p 'Tanium2015!' --host 10.0.1.240 --port 443 --loglevel 1 -j "/tmp/out.json"
```

```
PyTan v2.1.6 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
Created item: SavedQuestion, name: 'Has Tanium Standard Utilities CMDLINE TEST 3211', id: 126, ID: 126
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: noerror
    * Valid: **True**
    * Messages: No error texts found in stderr/stdout



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v2.1.0`, date: Fri Oct  2 16:06:23 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**