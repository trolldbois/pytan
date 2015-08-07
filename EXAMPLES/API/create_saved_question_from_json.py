
"""
Export a saved question object to a JSON file, adding ' API TEST' to the name of the saved question before exporting the JSON file and deleting any pre-existing saved question with the same (new) name, then create a new saved question object from the exported JSON file
"""

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
PORT = "443"

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

# set the attribute name and value we want to add to the original object (if any)
attr_name = "name"
attr_add = " API TEST"

# delete object before creating it?
delete = True

# setup the arguments for getting an object to export as json file
get_kwargs = {}
get_kwargs["objtype"] = u'saved_question'
get_kwargs["id"] = 1


# get objects to use as an export to JSON file
orig_objs = handler.get(**get_kwargs)

# if attr_name and attr_add exists, modify the orig_objs to add attr_add to the attribute
# attr_name
if attr_name:
    for x in orig_objs:
        new_attr = getattr(x, attr_name)
        new_attr += attr_add
        setattr(x, attr_name, new_attr)
        if delete:
            # delete the object in case it already exists
            del_kwargs = {}
            del_kwargs[attr_name] = new_attr
            del_kwargs['objtype'] = u'saved_question'
            try:
                handler.delete(**del_kwargs)
            except Exception as e:
                print e

# export orig_objs to a json file
json_file, results = handler.export_to_report_file(
    obj=orig_objs,
    export_format='json',
    report_dir=tempfile.gettempdir(),
)

# create the object from the exported JSON file
create_kwargs = {'objtype': u'saved_question', 'json_file': json_file}
response = handler.create_from_json(**create_kwargs)


print ""
print "Type of response: ", type(response)

print ""
print "print of response:"
print response

print ""
print "print the object returned in JSON format:"
print response.to_json(response)


'''Output from running this:
Handler for Session to 172.16.31.128:443, Authenticated: True, Version: Not yet determined!
2015-08-07 19:46:14,432 INFO     pytan.handler: Deleted 'SavedQuestion, id: 109'
2015-08-07 19:46:14,433 INFO     pytan.handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/SavedQuestionList_2015_08_07-15_46_14-EDT.json' written with 11903 bytes
2015-08-07 19:46:14,460 INFO     pytan.handler: New SavedQuestion, name: 'Has Tanium Standard Utilities API TEST', id: 111 (ID: 111) created successfully!

Type of response:  <class 'taniumpy.object_types.saved_question_list.SavedQuestionList'>

print of response:
SavedQuestionList, len: 1

print the object returned in JSON format:
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
      "id": 111, 
      "issue_seconds": 120, 
      "issue_seconds_never_flag": 0, 
      "keep_seconds": 0, 
      "mod_time": "2015-08-07T19:46:14", 
      "mod_user": {
        "_type": "user", 
        "name": "Tanium User"
      }, 
      "most_recent_question_id": 1256, 
      "name": "Has Tanium Standard Utilities API TEST", 
      "packages": {
        "_type": "package_specs", 
        "package_spec": [
          {
            "_type": "package_spec", 
            "id": 20, 
            "name": "Distribute Tanium Standard Utilities"
          }
        ]
      }, 
      "public_flag": 1, 
      "query_text": "Get Has Tanium Standard Utilities from all machines", 
      "question": {
        "_type": "question", 
        "action_tracking_flag": 0, 
        "expiration": "2015-08-07T19:32:37", 
        "expire_seconds": 0, 
        "force_computer_id_flag": 0, 
        "hidden_flag": 0, 
        "id": 1256, 
        "management_rights_group": {
          "_type": "group", 
          "id": 0
        }, 
        "query_text": "Get Has Tanium Standard Utilities from all machines", 
        "saved_question": {
          "_type": "saved_question", 
          "id": 110
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
                "creation_time": "2015-08-07T13:22:09", 
                "delimiter": ",", 
                "description": "Returns whether a machine has the Tanium Standard Utilities\nExample: Yes", 
                "exclude_from_parse_flag": 1, 
                "hash": 1782389954, 
                "hidden_flag": 0, 
                "id": 194, 
                "ignore_case_flag": 1, 
                "last_modified_by": "Jim Olsen", 
                "max_age_seconds": 900, 
                "modification_time": "2015-08-07T13:22:09", 
                "name": "Has Tanium Standard Utilities", 
                "queries": {
                  "_type": "queries", 
                  "query": [
                    {
                      "_type": "query", 
                      "platform": "Windows", 
                      "script": "&#039;========================================\n&#039; Has Tanium Standard Utilities\n&#039;========================================\n\n&#039; this action will look to see if the client has\n&#039; all necessary standard utilities files\n\nOption Explicit\n&#039;--------------------\n&#039; Set These Variables\nDim strDesiredVersion,strDesiredFCIVVersion,strDesiredGrepBinaryVersion\nDim strDesiredGrepDepVersion,strGrepDepFileVersion,strGrepBinaryFileVersion\n\n&#039; a string value which is a version like\n&#039; 4.2.314.7111\n&#039; which is used to determine whether the bundle has the correct version\n&#039; updating the content will cause the bundle number to change and all files will\n&#039; be sent to the endpoint again. This is to handle the case where\n&#039; binary files are not versioned, such as with Yara\n\n&#039; The top line of the version file\n&#039;Tanium File Version: &lt;version string below&gt;\nstrDesiredVersion = &quot;6.5.1.0011&quot;\n\n&#039; -------------------\n&#039; Binaries we can version\nstrDesiredGrepBinaryVersion = &quot;2.5.4.3331&quot;\nstrDesiredGrepDepVersion = &quot;1.12.2872.39125&quot;\n\nDim objFSO\nDim strDirToCheck,objTextFile\nDim bHasAllLatestFiles,arrTextFilesToCheck,strFile,strVersionLine,strFileVersion\nDim strFCIVFile,strFCIVFileVersion,strGrepBinary,strGrepDep,strHandleTool,strListDLLs2\nDim strListDLLs,strStreamsTool,strAutorunsTool\nDim strYara,strYarac\n\nSet objFSO = CreateObject(&quot;Scripting.FileSystemObject&quot;)\n\nstrDirToCheck = GetTaniumDir(&quot;Tools\\StdUtils&quot;)\n\narrTextFilesToCheck = Array(&quot;copy-to-tanium-dir-predist.vbs&quot;,&quot;runas-allusers-wrapper.vbs&quot;,&quot;ver\\bundle.cfg&quot;)\n\n&#039; Grep is required\nstrGrepBinary=strDirToCheck&amp;&quot;grep\\bin\\grep.exe&quot;\nstrGrepDep=strDirToCheck&amp;&quot;grep\\bin\\libiconv2.dll&quot;\n\n&#039;Yara binaries are required\nstrYara=strDirToCheck&amp;&quot;yara\\yara&quot;&amp;GetBitness&amp;&quot;.exe&quot;\nstrYarac=strDirToCheck&amp;&quot;yara\\yarac&quot;&amp;GetBitness&amp;&quot;.exe&quot;\n\nbHasAllLatestFiles = True\nFor Each strFile In arrTextFilesToCheck\n\tIf Not objFSO.FileExists(strDirToCheck&amp;strFile) Then\n\t\tWScript.Echo &quot;Missing &quot; &amp; strFile\n\t\tbHasAllLatestFiles = False\n\tEnd If\n\tIf objFSO.FileExists(strDirToCheck&amp;strFile) Then\n\t\tSet objTextFile = objFSO.OpenTextFile(strDirToCheck&amp;strFile)\n\t\tstrVersionLine = LCase(objTextFile.ReadLine()) &#039; version is at top of line\n\t\tIf Not InStr(strVersionLine,&quot;tanium file version:&quot;) &gt; 0 Then &#039; must have a version number in top line\n\t\t\tWScript.Echo strFile&amp;&quot; is not versioned on line 1&quot;\n\t\t\tbHasAllLatestFiles = False\n\t\tElse &#039; we have a version number, not split to check\n\t\t\tstrFileVersion = Split(strVersionLine,&quot;tanium file version:&quot;)(1)\n\t\t\tIf Trim(strFileVersion) &lt;&gt; Trim(strDesiredVersion) Then\n\t\t\t\tWScript.Echo strFile&amp;&quot; version: &quot;&amp;strFileVersion&amp;&quot;, needs: &quot;&amp;strDesiredVersion\n\t\t\t\tbHasAllLatestFiles = False\n\t\t\tEnd If\n\t\tEnd If\n\t\tobjTextFile.Close\n\tEnd If\nNext\n\n&#039; check a Grep dependency\nIf Not objFSO.FileExists(strGrepDep) Then\n\tWScript.Echo &quot;Missing &quot; &amp; strGrepDep\n\tbHasAllLatestFiles = False\nEnd If\nIf objFSO.FileExists(strGrepDep) Then\n\n\tstrGrepDepFileVersion = objFSO.GetFileVersion(strGrepDep)\n\tIf Not strGrepDepFileVersion = strDesiredGrepDepVersion Then\n\t\tbHasAllLatestFiles = False\n\t\tWScript.Echo strGrepDep &amp;&quot; version: &quot;&amp;strGrepDepFileVersion&amp;&quot;, needs: &quot;&amp;strDesiredGrepDepVersion\n\tEnd If\nEnd If\n\n\n&#039; check Grep binary\nIf Not objFSO.FileExists(strGrepBinary) Then\n\tWScript.Echo &quot;Missing &quot; &amp; strGrepBinary\n\tbHasAllLatestFiles = False\nEnd If\nIf objFSO.FileExists(strGrepBinary) Then\n\tstrGrepBinaryFileVersion = GetFileVersion(strGrepBinary)\n\tIf Not strGrepBinaryFileVersion = strDesiredGrepBinaryVersion Then\n\t\tbHasAllLatestFiles = False\n\t\tWScript.Echo strGrepBinary &amp;&quot; version: &quot;&amp;strGrepBinaryFileVersion&amp;&quot;, needs: &quot;&amp;strDesiredGrepBinaryVersion\n\tEnd If\nEnd If\n\nIf Not objFSO.FileExists(strYara) Then\n\tbHasAllLatestFiles = False\n\tWScript.Echo &quot;Missing &quot; &amp; strYara\nEnd If\n\nIf Not objFSO.FileExists(strYarac) Then\n\tbHasAllLatestFiles = False\n\tWScript.Echo &quot;Missing &quot; &amp; strYarac\nEnd If\n\nIf bHasAllLatestFiles Then\n\tWScript.Echo &quot;Yes&quot;\nElse\n\tWScript.Echo &quot;No&quot;\nEnd If\n\nFunction GetFileVersion(strPath)\n\tDim objFSO\n\tSet objFSO = CreateObject(&quot;Scripting.FileSystemObject&quot;)\n\tIf objFSO.FileExists(strPath) Then\n\t\tGetFileVersion = objFSO.GetFileVersion(strPath)\n\tElse\n\t\tGetFileVerison = -1\n\tEnd If\nEnd Function &#039;GetFileVersion\n\nFunction GetTaniumDir(strSubDir)\n\tDim strComputer, key32path, key64path, keyPath, reg\n\tDim strPath\n\tstrComputer = &quot;.&quot;\n\tConst HKLM = &amp;h80000002\n    \n\tkey32Path = &quot;Software\\Tanium\\Tanium Client&quot;\n\tkey64Path = &quot;Software\\Wow6432Node\\Tanium\\Tanium Client&quot;\n    \n\tSet reg=GetObject(&quot;winmgmts:{impersonationLevel=impersonate}!\\\\&quot; &amp; strComputer &amp; &quot;\\root\\default:StdRegProv&quot;)\n    \n\tIf RegKeyExists(reg, HKLM, key64Path) Then\n\t\tkeyPath = key64Path\n\tElseIf RegKeyExists(reg, HKLM, key32Path) Then\n\t\tkeyPath = key32Path\n\tEnd If\n    \n\treg.GetStringValue HKLM,keyPath,&quot;Path&quot;, strPath\n\n\tIf strSubDir &lt;&gt; &quot;&quot; Then\n\t\tstrSubDir = &quot;\\&quot; &amp; strSubDir\n\tEnd If\t\n\n\tDim fso\n\tSet fso = WScript.CreateObject(&quot;Scripting.FileSystemObject&quot;)\n\tIf fso.FolderExists(strPath) Then\n\t\tIf Not fso.FolderExists(strPath &amp; strSubDir) Then\n\t\t\tfso.CreateFolder(strPath &amp; strSubDir)\n\t\tEnd If\n\t\tGetTaniumDir = strPath &amp; strSubDir &amp; &quot;\\&quot;\n\tEnd If\nEnd Function\n\nFunction RegKeyExists(objRegistry, sHive, sRegKey)\n\tDim aValueNames, aValueTypes\n\tIf objRegistry.EnumValues(sHive, sRegKey, aValueNames, aValueTypes) = 0 Then\n\t\tRegKeyExists = True\n\tElse\n\t\tRegKeyExists = False\n\tEnd If\nEnd Function\n\n\nFunction GetBitness\n\tIf Not Is64 Then\n\t\tGetBitness = &quot;32&quot;\n\tElse\n\t\tGetBitness = &quot;64&quot;\n\tEnd If\nEnd Function &#039;GetBitness\n\nFunction Is64 \n\tDim objWMIService, colItems, objItem\n\tSet objWMIService = GetObject(&quot;winmgmts:\\\\.\\root\\CIMV2&quot;)\n\tSet colItems = objWMIService.ExecQuery(&quot;Select SystemType from Win32_ComputerSystem&quot;)    \n\tFor Each objItem In colItems\n\t\tIf InStr(LCase(objItem.SystemType), &quot;x64&quot;) &gt; 0 Then\n\t\t\tIs64 = True\n\t\tElse\n\t\t\tIs64 = False\n\t\tEnd If\n\tNext\nEnd Function &#039; Is64", 
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
                "string_count": 16, 
                "value_type": "String"
              }
            }
          ]
        }, 
        "skip_lock_flag": 0, 
        "user": {
          "_type": "user", 
          "id": 1, 
          "name": "Jim Olsen"
        }
      }, 
      "row_count_flag": 0, 
      "sort_column": 0, 
      "user": {
        "_type": "user", 
        "id": 2, 
        "name": "Tanium User"
      }
    }
  ]
}

'''
