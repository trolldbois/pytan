
"""
Ask a manual question using human strings by referencing the name of a single sensor that takes parameters, but not supplying any parameters (and letting pytan automatically determine the appropriate default value for those parameters which require a value).

No sensor filters, sensor parameters, sensor filter options, question filters, or question options supplied.
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
print out.getvalue()



'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
2014-12-07 01:04:48,586 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:04:53,604 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:04:58,620 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:05:03,638 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:05:08,654 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:05:13,672 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:05:18,693 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:05:23,706 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:05:28,725 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:05:33,745 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:05:38,760 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:05:43,775 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:05:48,794 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:05:53,811 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:05:58,828 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:06:03,844 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:06:08,862 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:06:13,881 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:06:18,899 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:06:23,919 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)
2014-12-07 01:06:28,936 INFO     question_progress: Results 100% (Get Folder Name Search with RegEx Match[No, , No, ] from all machines)

Type of response:  <type 'dict'>

Pretty print of response:
{'question_object': <taniumpy.object_types.question.Question object at 0x10204fb90>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x102334ed0>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Folder Name Search with RegEx Match[No, , No, ] from all machines

CSV Results of response: 
Count,"Folder Name Search with RegEx Match[No, , No, ]"
25044,[too many results]
1,C:\Windows\winsxs\amd64_microsoft-windows-s..structure.resources_31bf3856ad364e35_6.1.7600.16385_en-us_faf46e6f502e00e8
1,C:\Windows\winsxs\x86_microsoft-windows-e..-host-authenticator_31bf3856ad364e35_6.1.7601.17514_none_a7c68343f07f776f
1,C:\Windows\winsxs\amd64_microsoft-windows-ocspsvc_31bf3856ad364e35_6.1.7601.22807_none_3bfeae7293092e4b
1,C:\Windows\winsxs\amd64_microsoft-windows-c..ityclient.resources_31bf3856ad364e35_6.1.7601.22865_en-us_c339d6d6cfb99c39
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\System.Xml
1,C:\Users\Jim Olsen\Desktop\SysinternalsSuite
1,C:\Windows\winsxs\amd64_microsoft-windows-scripting.resources_31bf3856ad364e35_6.1.7600.16385_en-us_e72192b67124ad43
1,C:\Windows\winsxs\x86_microsoft-windows-mlang.resources_31bf3856ad364e35_6.1.7600.16385_ru-ru_cf3a10abc52740f6
1,C:\Windows\winsxs\x86_microsoft-windows-directshow-dvdsupport_31bf3856ad364e35_6.1.7601.21987_none_566a88a44b6e5342
1,C:\Windows\winsxs\amd64_microsoft-windows-ie-internetexplorer_31bf3856ad364e35_11.2.9600.17041_none_11e6f4b92ee9bf19
1,C:\Users\Jim Olsen\AppData\Local\Google
1,C:\Windows\winsxs\x86_microsoft-windows-e..nt-client.resources_31bf3856ad364e35_6.1.7600.16385_en-us_e5c3d3ec6ff64de3
1,C:\Windows\winsxs\amd64_microsoft-windows-d..e-eashared-kjshared_31bf3856ad364e35_6.1.7600.16385_none_99b74194b7347cab
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\RadLangSvc
1,C:\Windows\winsxs\amd64_microsoft-windows-p..ginworker.resources_31bf3856ad364e35_6.1.7600.16385_en-us_ae3287fe59b4af28
1,C:\Windows\winsxs\amd64_microsoft-windows-i..riptcollectionagent_31bf3856ad364e35_11.2.9600.17041_none_984c3cbdadb5a971
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\System.ServiceProce#
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_63\grep
1,C:\Windows\Microsoft.NET\assembly\GAC_32\Microsoft.SqlServer.BulkInsertTaskConnections
1,C:\ProgramData\Microsoft\Device Stage\Task\{e35be42d-f742-4d96-a50a-1775fb1a7a42}\en-US
1,C:\Windows\assembly\NativeImages_v4.0.30319_64\Microsoft.S8d1a6405#
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\napsnap
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.B22c61a69#\9a56520d8321e899683663fc7b00b739
1,C:\Windows\winsxs\amd64_microsoft-windows-baseapinamespace_31bf3856ad364e35_6.1.7601.17514_none_a4272f399040a523
1,C:\Windows\System32\inetsrv\config\Export
1,C:\Windows\winsxs\amd64_microsoft-windows-wininit_31bf3856ad364e35_6.1.7600.16385_none_8ce7aa761e01ad49
1,C:\Windows\winsxs\amd64_microsoft-windows-d..x-directxdiagnostic_31bf3856ad364e35_6.1.7601.17514_none_81e99da174638311
1,C:\Windows\winsxs\amd64_netfx-accessibility_b03f5f7f11d50a3a_6.1.7601.22733_none_a079af8fec10f97e
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.Dynamic.Runtime
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\System.Workflow.Run#
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_56\grep\share\locale\vi\LC_MESSAGES
1,C:\Windows\winsxs\amd64_microsoft-windows-i..l-keyboard-00050409_31bf3856ad364e35_6.1.7600.16385_none_765aa38f38767686
1,C:\Windows\winsxs\amd64_microsoft-windows-s..ty-spp-ux.resources_31bf3856ad364e35_6.1.7600.16385_en-us_54dae2e5153375ce
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\System.Runtime.Remo#\875c35969785fa170d186e7ca546ac9e
1,C:\Windows\winsxs\amd64_microsoft-windows-inetres-adm.resources_31bf3856ad364e35_11.2.9600.17239_en-us_520b80ca92793283
1,C:\Windows\winsxs\amd64_microsoft-windows-b..vironment-os-loader_31bf3856ad364e35_6.1.7601.21655_none_b9ac1d069c83936e
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\WindowsForm0b574481#
1,C:\Windows\winsxs\amd64_microsoft-windows-l..webserver.resources_31bf3856ad364e35_6.1.7601.17514_en-us_c9b90df8dc48cf89
1,C:\Windows\winsxs\wow64_microsoft-windows-scripting-vbscript_31bf3856ad364e35_6.1.7601.18337_none_b0c1f98278f4f2bf
1,C:\Windows\winsxs\amd64_microsoft-windows-f..truetype-lucidasans_31bf3856ad364e35_6.1.7600.16385_none_d0e8774fa1155a53
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_21\grep\share\locale\ja\LC_MESSAGES
1,C:\Windows\winsxs\amd64_microsoft-windows-d..s-ime-japanese-core_31bf3856ad364e35_6.1.7600.16385_none_cb604f1aa758e6b6
1,C:\Program Files (x86)\Common Files\microsoft shared\MSEnv\PublicAssemblies
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.S6402eefa#\57e4c4b79ab9ff13194fff26fd4cb81e
1,C:\Windows\Media\Calligraphy
1,C:\Windows\System32\DriverStore
1,C:\Windows\winsxs\amd64_microsoft-windows-m..do-backcompat-tlb20_31bf3856ad364e35_6.1.7601.22012_none_49c4ab6d21d4e912
1,C:\Windows\winsxs\x86_microsoft-windows-x..ocess-mui.resources_31bf3856ad364e35_6.1.7600.16385_en-us_51e4cd07e2a390ca
1,C:\Windows\winsxs\Temp\PendingRenames
1,C:\Windows\winsxs\amd64_microsoft-windows-m..ents-mdac-ado15-dll_31bf3856ad364e35_6.1.7601.22012_none_6ade6200a065d2ea
1,C:\Windows\assembly\GAC_MSIL\PresentationFramework\3.0.0.0__31bf3856ad364e35
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_24\grep\share\locale\de\LC_MESSAGES
1,C:\Windows\winsxs\amd64_prnlx00x.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_34edc3c5e185ed82
1,C:\Windows\winsxs\x86_microsoft-windows-s..-binaries.resources_31bf3856ad364e35_6.1.7601.17514_sk-sk_3f6dfbca0c1ae0a6
1,C:\Windows\winsxs\x86_system.printing_31bf3856ad364e35_6.1.7601.22309_none_75e11e57ed6f8b6a
1,C:\Windows\winsxs\amd64_microsoft-windows-g..admintools-admfiles_31bf3856ad364e35_6.1.7600.16385_none_0d041ab5a8298266
1,C:\Windows\winsxs\x86_microsoft-windows-n..-security.resources_31bf3856ad364e35_6.1.7600.16385_en-us_4e0c2004a5e71cbd
1,C:\Windows\Microsoft.NET\Framework\v2.0.50727\ASP.NETWebAdminFiles\App_GlobalResources
1,C:\Windows\Microsoft.NET\Framework\v2.0.50727\CONFIG\Browsers
1,C:\Windows\winsxs\x86_microsoft-windows-comctl32-v5.resources_31bf3856ad364e35_6.1.7600.16385_ru-ru_abc131a3483b963e
1,C:\Windows\winsxs\x86_microsoft-windows-i..tional-codepage-858_31bf3856ad364e35_6.1.7600.16385_none_cebddca2fc8602ec
1,C:\Windows\winsxs\amd64_microsoft-windows-t..instationextensions_31bf3856ad364e35_6.1.7601.17828_none_f83075d781b149cb
1,C:\Windows\winsxs\amd64_microsoft-windows-comctl32-v5.resources_31bf3856ad364e35_6.1.7600.16385_th-th_48e4d94ee906cf10
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_19\grep\share\locale\tr\LC_MESSAGES
1,C:\Windows\System32\DriverStore\FileRepository\qd3x64.inf_amd64_neutral_e8903726d63a3f07
1,C:\Windows\winsxs\amd64_sdbus.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_86b03fe7f8988681
1,C:\Windows\winsxs\x86_netfx-netfxsbs10_exe_31bf3856ad364e35_6.1.7601.18514_none_3d9642980c369d84
1,C:\Windows\winsxs\x86_microsoft-windows-r..ne-editor.resources_31bf3856ad364e35_6.1.7600.16385_en-us_b372f75f60a7c3cb
1,C:\Windows\winsxs\amd64_microsoft-windows-pcwdiagnostic_31bf3856ad364e35_6.1.7600.16385_none_5120bf8b19591afa
1,C:\Windows\winsxs\amd64_microsoft-windows-f..overcluster-wizards_31bf3856ad364e35_6.1.7601.17514_none_9e78ebf51945212a
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_23\grep\share\locale\ky\LC_MESSAGES
1,C:\Windows\winsxs\amd64_microsoft-windows-eventviewer.resources_31bf3856ad364e35_6.1.7600.16385_en-us_809afd26837a22dc
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_24\grep\share\locale\pt_BR\LC_MESSAGES
1,C:\Windows\winsxs\amd64_microsoft-windows-themeservice_31bf3856ad364e35_6.1.7600.16385_none_05f77252e20d9cfd
1,C:\Windows\winsxs\amd64_microsoft-windows-n..ce_datastore_srvsku_31bf3856ad364e35_6.1.7600.16385_none_7ea671bdffc2c389
1,C:\Windows\assembly\GAC_MSIL\Microsoft.ApplicationId.RuleWizard.Resources
1,C:\Windows\winsxs\amd64_srpuxnativesnapin_31bf3856ad364e35_6.1.7600.16385_none_447807b31b9d298e
1,C:\Windows\assembly\GAC\VSLangProj\7.0.3300.0__b03f5f7f11d50a3a
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.S1eb28fa5#\5661d649208ef3a720c99e1e4271c07a
1,C:\Windows\SysWOW64\en-US\Licenses\OEM\ServerStorageWorkgroup
1,C:\Windows\winsxs\wow64_microsoft-windows-n..etcapture.resources_31bf3856ad364e35_6.1.7600.16385_en-us_243202836fa93a1a
1,C:\Windows\winsxs\x86_microsoft-windows-lsa-msprivs.resources_31bf3856ad364e35_6.1.7600.16385_sv-se_4c5086c9a2727fc3
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\cgi-bin
1,C:\Windows\winsxs\amd64_microsoft-windows-i..rver2008compat-data_31bf3856ad364e35_6.1.7600.16385_none_07263572e5ebcd9d
1,C:\Windows\System32\DriverStore\FileRepository\adpu320.inf_amd64_neutral_4ea3d42a9839982a
1,C:\Windows\System32\WindowsPowerShell\v1.0\Modules\AppLocker
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.Bfc9dc24d#\5b153cb12d982242817d816f01e63cb4
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_56\grep\share\locale\da\LC_MESSAGES
1,C:\Windows\winsxs\amd64_microsoft-windows-t..framework-migration_31bf3856ad364e35_6.1.7600.16385_none_4ce62d7fd1cb54eb
1,C:\Windows\winsxs\x86_microsoft.windows.c..-controls.resources_6595b64144ccf1df_5.82.7600.16385_th-th_8c299c84d28e8005
1,C:\Windows\winsxs\x86_microsoft-windows-mediaplayer-migration_31bf3856ad364e35_6.1.7601.17514_none_e02729035a3379c1
1,C:\Windows\winsxs\x86_microsoft-windows-tapiadmin_31bf3856ad364e35_6.1.7601.17514_none_5fbc6ff536eb243e
1,C:\Windows\winsxs\wow64_microsoft-windows-security-kerberos_31bf3856ad364e35_6.1.7601.18606_none_4f5e488afbc409b9
1,C:\Windows\winsxs\x86_microsoft-windows-sendmail.resources_31bf3856ad364e35_6.1.7600.16385_en-us_ef49195de3a2e11b
1,C:\Windows\winsxs\amd64_microsoft-windows-i..onal-codepage-20423_31bf3856ad364e35_6.1.7600.16385_none_ae5b1276ffc4917e
1,C:\Windows\assembly\GAC_MSIL\Microsoft.SqlServer.Management.RegisteredServers\10.0.0.0__89845dcd8080cc91
1,C:\Windows\winsxs\amd64_microsoft-windows-mediaplayer-wmvsdk_31bf3856ad364e35_6.1.7601.17514_none_04514cd13d40a393
1,C:\Windows\winsxs\amd64_microsoft-windows-m..readwrite.resources_31bf3856ad364e35_6.1.7600.16385_en-us_b212b9dc94b41b2e
1,C:\Windows\winsxs\msil_microsoft.visualbasic_b03f5f7f11d50a3a_6.1.7601.22733_none_6b1e5248d77e003d
1,C:\Windows\winsxs\amd64_server-help-h1s.perfmon.resources_31bf3856ad364e35_6.1.7600.16385_en-us_e6c040e564a18de0
1,C:\Users\Jim Olsen\AppData\Local\Microsoft\Internet Explorer
1,C:\Program Files\VMware\VMware Tools\plugins\vmsvc
1,C:\Windows\winsxs\x86_microsoft-windows-p..age-codec.resources_31bf3856ad364e35_7.1.7601.16492_fr-fr_4522938c0ba39055
1,C:\Windows\winsxs\amd64_microsoft-windows-t..teconnectionmanager_31bf3856ad364e35_6.1.7601.22750_none_ed1f8e488425629d
1,C:\Windows\winsxs\amd64_microsoft-windows-fmifs_31bf3856ad364e35_6.1.7600.16385_none_b303632c4b483c6c
1,C:\Windows\winsxs\amd64_microsoft-windows-f..rcluster-powershell_31bf3856ad364e35_6.1.7601.17514_none_f273f11a257acc7b
1,C:\Windows\winsxs\amd64_netfx-mscorpe_dll_b03f5f7f11d50a3a_6.1.7601.17514_none_8492ec5f045f17f3
1,C:\Windows\winsxs\amd64_mdmusrg.inf_31bf3856ad364e35_6.1.7600.16385_none_ef6d0c5fba40766d
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_53\grep\share\locale\es\LC_MESSAGES
1,C:\Windows\winsxs\amd64_microsoft-windows-b..tiondata-com-server_31bf3856ad364e35_6.1.7601.17514_none_3dc961517b5bd485
1,C:\Windows\winsxs\amd64_netfx-system.xml_b03f5f7f11d50a3a_6.1.7601.22740_none_4a87840c55cea28e
1,C:\Windows\winsxs\x86_microsoft-windows-com-dtc-setup_31bf3856ad364e35_6.1.7600.16385_none_8da1fd210f4e6422
1,C:\Windows\winsxs\amd64_microsoft-windows-iis-aspbinaries_31bf3856ad364e35_6.1.7601.17514_none_eaaa53b67e14526e
1,C:\Windows\System32\wbem\Logs
1,C:\Windows\winsxs\amd64_microsoft-windows-usp_31bf3856ad364e35_6.1.7601.22666_none_0b75f5788860623d
1,C:\Windows\winsxs\amd64_wcf-icardagt_exe_31bf3856ad364e35_6.1.7600.16385_none_8dcc9c6f8b58a5eb
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.Diagnostics.Debug
1,C:\Python27\Lib\encodings
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.A7373a429#\ab9e962308894f7a534dd3aaa055c576
1,C:\Windows\winsxs\amd64_microsoft-windows-server-editions-matrix_31bf3856ad364e35_6.1.7601.17514_none_567c82324e93b3ba
1,C:\Windows\winsxs\amd64_fdwsd_31bf3856ad364e35_6.1.7600.16385_none_d99d751adbd6df3c
1,C:\Windows\SysWOW64\migration\WSMT\rras\dlmanifests\Microsoft-Windows-RasServer-MigPlugin
1,C:\Windows\winsxs\x86_microsoft-windows-p..soundservice-server_31bf3856ad364e35_6.1.7600.16385_none_cdbd3bd8d282195f
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\System.Runteb92aa12#
1,C:\Windows\winsxs\amd64_microsoft-windows-t..n-nonmsil.resources_31bf3856ad364e35_6.1.7601.17514_en-us_1a644c96b184b0fd
1,C:\Windows\assembly\GAC_MSIL\System.Runtime.Serialization.Formatters.Soap\2.0.0.0__b03f5f7f11d50a3a
1,C:\Windows\winsxs\amd64_microsoft-windows-scrnsave_31bf3856ad364e35_6.1.7600.16385_none_3d3492aaf415de8e
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_26\grep\share\locale\fi\LC_MESSAGES
1,C:\Windows\winsxs\amd64_microsoft-windows-scripting-jscript9_31bf3856ad364e35_11.2.9600.17239_none_26972afdd2aea099
1,C:\pytan
1,C:\Windows\winsxs\amd64_microsoft-windows-m..ds-ce-rll.resources_31bf3856ad364e35_6.1.7600.16385_en-us_6a0dd7ce3b0d1786
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_24\grep\share\locale\ga\LC_MESSAGES
1,C:\Windows\winsxs\wow64_microsoft-windows-i..isapifilterbinaries_31bf3856ad364e35_6.1.7600.16385_none_d2e2c5a7872ef5b5
1,C:\Windows\winsxs\amd64_microsoft-windows-d..anagement.resources_31bf3856ad364e35_6.1.7600.16385_en-us_70bd2df49cbcc5d7
1,C:\Windows\winsxs\wow64_microsoft-windows-p..ll-preloc.resources_31bf3856ad364e35_6.1.7600.16385_en-us_27fbee50ef7f6588
1,C:\Windows\winsxs\x86_microsoft-windows-msmpeg2enc_31bf3856ad364e35_6.1.7601.17514_none_0b450351a4424f06
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9035\grep\share\locale\be\LC_MESSAGES
1,C:\Windows\winsxs\wow64_microsoft-windows-i..l-keyboard-00010439_31bf3856ad364e35_6.1.7601.17514_none_f6670d2d9f81941a
1,C:\Windows\winsxs\amd64_microsoft-windows-d2d.resources_31bf3856ad364e35_7.1.7601.16492_de-de_3dc539e9fdc54eb8
1,C:\Users\Jim Olsen\AppData\Local\Google\Chrome\User Data\Default\Extensions\apdfllckaahabafndbhieahigkjlhalf\6.3_0\_metadata
1,C:\Windows\winsxs\amd64_microsoft-windows-k..distribution-center_31bf3856ad364e35_6.1.7601.18658_none_e9b67a55aafd5915
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_63\grep\share\locale\nb\LC_MESSAGES
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.Workflow.ComponentModel\v4.0_4.0.0.0__31bf3856ad364e35
1,C:\Windows\winsxs\amd64_microsoft-windows-f..uster-rhs.resources_31bf3856ad364e35_6.1.7600.16385_en-us_bfb550e4d357a13c
1,C:\Python27\Lib\multiprocessing\dummy
1,C:\Windows\winsxs\amd64_microsoft-windows-windowscodec_31bf3856ad364e35_7.1.7601.16492_none_e5bfce1d42e6e71d
1,C:\Windows\System32\migration
1,C:\Windows\winsxs\x86_microsoft-windows-media-mp3acm.resources_31bf3856ad364e35_6.1.7600.16385_en-us_2b0d4dbaf241f90a
1,C:\Windows\assembly\GAC_MSIL\Microsoft.SqlServer.Smo\10.0.0.0__89845dcd8080cc91
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\System.Printing
1,C:\Windows\winsxs\x86_microsoft-windows-wab-app_31bf3856ad364e35_6.1.7601.17514_none_44b0c76c35d4b76d
1,C:\Windows\winsxs\amd64_microsoft-windows-telephonyserver_31bf3856ad364e35_6.1.7600.16385_none_2a18b42e4b4fec52
1,C:\Windows\System32\migration\en-US
1,C:\Windows\PCHEALTH\ERRORREP
1,C:\Windows\winsxs\amd64_microsoft.windows.c..-controls.resources_6595b64144ccf1df_5.82.7600.16385_ar-sa_25b69e51bf9d09dc
1,C:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\SqlWorkbenchProjectItems\Sql\Earlier Versions\Create Statistics
1,C:\Windows\winsxs\x86_microsoft-windows-s..t-tracker.resources_31bf3856ad364e35_6.1.7600.16385_en-us_25cb0eedc2efe3f8
1,C:\Windows\winsxs\amd64_wcf-icardres_dll_vista_31bf3856ad364e35_6.1.7601.22733_none_6fa639389aa6848a
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.Linq.Queryable
1,C:\Windows\assembly\NativeImages_v4.0.30319_64\System.Wind0de890be#
1,C:\Windows\winsxs\amd64_adfs-upgrademb-files_31bf3856ad364e35_6.1.7600.16385_none_fbd0c34fcbe686a6
1,C:\Windows\winsxs\amd64_microsoft-windows-cryptnet-dll_31bf3856ad364e35_6.1.7601.22380_none_7579163e2bcf63b6
1,C:\Windows\winsxs\x86_microsoft-windows-m..river-rll.resources_31bf3856ad364e35_6.1.7600.16385_en-us_5ad10fe903ded84f
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.Linq.Parallel\v4.0_4.0.0.0__b03f5f7f11d50a3a
1,C:\Windows\winsxs\amd64_mdmsun1.inf_31bf3856ad364e35_6.1.7600.16385_none_1f7c98965ef22a0b
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9025\grep\share\locale\cs\LC_MESSAGES
1,C:\Windows\assembly\GAC_32\Policy.1.2.Microsoft.Interop.Security.AzRoles
1,C:\Users\Default\Pictures
1,C:\ProgramData\Microsoft\User Account Pictures
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\MSBuild
1,C:\Windows\Microsoft.NET\assembly\GAC_32\WebDev.WebHost40
1,C:\Windows\winsxs\x86_microsoft-windows-v..kprovider.resources_31bf3856ad364e35_6.1.7600.16385_en-us_310eba4283ecd151
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_35\grep\share\locale\sr\LC_MESSAGES
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\System.Data.Entity
1,C:\Windows\assembly\GAC_MSIL\Microsoft.SqlServer.Management.SystemMetadataProvider
1,C:\Windows\System32\DriverStore\FileRepository\mdmati.inf_amd64_neutral_ded8f26cdee953c3
1,C:\Windows\winsxs\amd64_microsoft-windows-s..ssmanager.resources_31bf3856ad364e35_6.1.7600.16385_en-us_df658d4857ad8da5
1,C:\Python27\Lib\json\tests
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.VisualStudio.DataDesign.WpfDataTool\v4.0_10.0.0.0__b03f5f7f11d50a3a
1,C:\Windows\winsxs\amd64_wiaca00c.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_2a6c49c557aaa43a
1,C:\Windows\winsxs\x86_microsoft-windows-w..ywmdmshellextension_31bf3856ad364e35_6.1.7601.17514_none_8ff5b6498cc24750
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_46\grep\share\locale\el\LC_MESSAGES
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\napsnap\a015e4dd451330be62225abb563d0de0
1,C:\Windows\winsxs\msil_microsoft.certificateservices.common_31bf3856ad364e35_6.1.7600.16385_none_806221b8143468d9
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.SqlServer.ManagedConnections\v4.0_11.0.0.0__89845dcd8080cc91
1,C:\Windows\System32\config\systemprofile\AppData\LocalLow
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.S01b51732#\c912998df34aa3f47d20a058bd34d099
1,C:\Windows\winsxs\x86_microsoft-windows-i..er-engine.resources_31bf3856ad364e35_6.1.7601.17514_sv-se_2e455c2305308809
1,C:\Windows\winsxs\x86_microsoft.windows.common-controls_6595b64144ccf1df_5.82.7601.18201_none_ec80f00e8593ece5
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\WindowsBase
1,C:\Windows\ServiceProfiles\NetworkService\AppData\Local\Microsoft
1,C:\Windows\winsxs\x86_microsoft.windows.c..-controls.resources_6595b64144ccf1df_6.0.7600.16385_it-it_e4c79be92250cb6e
1,C:\Windows\winsxs\amd64_microsoft-windows-nfs-openportmapper_31bf3856ad364e35_6.1.7601.17514_none_920a130a60c213ff
1,C:\Windows\winsxs\wow64_microsoft-windows-security-kerberos_31bf3856ad364e35_6.1.7601.17514_none_4f518cecfbcddc34
1,C:\Program Files\Microsoft SQL Server\110\Setup Bootstrap\SQLServer2012\1040_ITA_LP\x64\1040\help
1,C:\Windows\assembly\GAC_MSIL\Microsoft.Security.ApplicationId.Wizards.AutomaticRuleGenerationWizard
1,C:\Windows\winsxs\amd64_microsoft-windows-ie-imagesupport_31bf3856ad364e35_8.0.7600.16385_none_b4a401b283c17ad1
1,C:\Windows\winsxs\amd64_tsprint.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_94fa9583519bc058
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9035\grep\share\locale\sr\LC_MESSAGES
1,C:\Windows\System32\en-US\Licenses\OEM\ServerSBSStandard
1,C:\Windows\assembly\GAC_MSIL\EventViewer.Resources\6.1.0.0_en_31bf3856ad364e35
1,C:\Users\Jim Olsen\Recent
1,C:\Windows\winsxs\amd64_microsoft-windows-s..lders-adm.resources_31bf3856ad364e35_6.1.7600.16385_en-us_306353129db95bdd
1,C:\Windows\assembly\GAC_MSIL\System.DirectoryServices.Protocols\2.0.0.0__b03f5f7f11d50a3a
1,C:\Windows\winsxs\amd64_netrndis.inf_31bf3856ad364e35_6.1.7601.17887_none_259febb55ca2345a
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\Microsoft.Security.#\1966e104b20c7ee0537ec94244c6eb05
1,C:\Windows\winsxs\amd64_networking-mpssvc.resources_31bf3856ad364e35_6.1.7600.16385_en-us_24b3cfe4ff928bea
1,C:\Windows\winsxs\wow64_microsoft-windows-p..ll-events.resources_31bf3856ad364e35_6.1.7600.16385_en-us_493296f9a8635002
1,C:\Windows\winsxs\amd64_microsoft-windows-d..-charcodedictionary_31bf3856ad364e35_6.1.7600.16385_none_8555c0891265db3e
1,C:\Windows\winsxs\x86_microsoft-windows-i..tional-codepage-500_31bf3856ad364e35_6.1.7600.16385_none_ceda0134fc71635e
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.ServiceModel.Channels\v4.0_4.0.0.0__31bf3856ad364e35
1,C:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\SqlWorkbenchProjectItems\Sql\Audit
1,C:\Windows\System32\en-US\Licenses\eval\ServerWinSBV
1,C:\Windows\winsxs\x86_wpf-presentationframework.luna_31bf3856ad364e35_6.1.7601.17514_none_33660260677d7e6a
1,C:\Windows\winsxs\wow64_microsoft-windows-com-complus-admin_31bf3856ad364e35_6.1.7600.16385_none_43b350887adefc43
1,C:\Windows\winsxs\amd64_microsoft-windows-dims-autoenroll_31bf3856ad364e35_6.1.7600.16385_none_5004a8665487390e
1,C:\Windows\winsxs\wow64_microsoft-windows-uianimation.resources_31bf3856ad364e35_7.1.7601.16492_es-es_30e64d79b18289db
1,C:\Windows\winsxs\amd64_microsoft-windows-g..me-snapin.resources_31bf3856ad364e35_6.1.7600.16385_en-us_4753f21e9fa662df
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.D09177692#
1,C:\Windows\SoftwareDistribution\PostRebootEventCache
1,C:\Windows\winsxs\x86_microsoft-windows-xmllite_31bf3856ad364e35_6.1.7601.17633_none_8b2c4a4201a1c2f4
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9024\grep\share\locale\nl\LC_MESSAGES
1,C:\Program Files\Common Files\Microsoft Shared\VS7Debug
1,C:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\SqlWorkbenchProjectItems\Sql\SQL Azure Database\Trigger
1,C:\Windows\winsxs\amd64_microsoft-windows-ie-jscriptdebugui_31bf3856ad364e35_8.0.7601.17514_none_334c9b845b46bf8d
1,C:\Windows\winsxs\amd64_ql40xx.inf_31bf3856ad364e35_6.1.7600.16385_none_574ac369ea0b9135
1,C:\Windows\winsxs\x86_microsoft-windows-n..ion-agent.resources_31bf3856ad364e35_6.1.7600.16385_en-us_15bf7202267cb05f
1,C:\Windows\System32\DriverStore\FileRepository\netxex64.inf_amd64_neutral_77b02fd738dca150
1,C:\Windows\winsxs\amd64_netfx-system_tlb_b03f5f7f11d50a3a_6.1.7601.22740_none_4871ba84575f992c
1,C:\Windows\winsxs\wow64_microsoft-windows-webio_31bf3856ad364e35_6.1.7601.17514_none_c564e9df29b386b8
1,C:\Windows\winsxs\wow64_microsoft-windows-migrationengine_31bf3856ad364e35_6.1.7601.17514_none_c122877426404910
1,C:\Windows\winsxs\amd64_microsoft-windows-b..dlinetool.resources_31bf3856ad364e35_6.1.7600.16385_en-us_7d02b5319200e88c
1,C:\Windows\winsxs\amd64_microsoft-windows-nwifi.resources_31bf3856ad364e35_6.1.7600.16385_en-us_6e0ae8581c7910f9
1,C:\Windows\winsxs\wow64_microsoft-windows-i..l-keyboard-0001045d_31bf3856ad364e35_6.1.7600.16385_none_0747808f9651066f
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.SqlServer.WebServiceTaskUI
1,C:\Windows\winsxs\wow64_microsoft-windows-taskscheduler-service_31bf3856ad364e35_6.1.7601.17514_none_977bce52e202c4f4
1,C:\Windows\winsxs\x86_addinprocess32_b77a5c561934e089_6.1.7601.17514_none_83171a284b28fcec
1,C:\Windows\winsxs\amd64_netl260a.inf_31bf3856ad364e35_6.1.7600.16385_none_d603843483dfa9aa
1,C:\Windows\winsxs\amd64_microsoft-windows-ie-hotmailapi_31bf3856ad364e35_6.1.7600.16385_none_c640cdfa5e9e8384
1,C:\Windows\winsxs\amd64_microsoft-windows-w..edtracing.resources_31bf3856ad364e35_6.1.7600.16385_en-us_1b774243b18f0918
1,C:\Windows\winsxs\amd64_microsoft-windows-crypt32-dll.resources_31bf3856ad364e35_6.1.7600.16385_en-us_2a1bcf35d3f77b46
1,C:\Windows\winsxs\msil_microsoft.virtualiz..ent.rdpclientaxhost_31bf3856ad364e35_6.1.7600.16385_none_a718774ed6eab4b1
1,C:\Windows\assembly\GAC_MSIL\Microsoft.SqlServer.CustomControls.resources\11.0.0.0_fr_89845dcd8080cc91
1,C:\Program Files\Tanium\Tanium Server\Apache24\manual\style
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.SqlServer.MSMQTask
1,C:\Windows\winsxs\x86_microsoft-windows-m..cursor-library-ansi_31bf3856ad364e35_6.1.7601.21747_none_50bddeac182a2738
1,C:\Windows\winsxs\amd64_microsoft-windows-c..rtadm-dll.resources_31bf3856ad364e35_6.1.7600.16385_en-us_c2e353c5eb005391
1,C:\Windows\System32\en-US\Licenses\_Default\ServerSolutionsPremium
1,C:\Windows\winsxs\amd64_microsoft-windows-cdosys.resources_31bf3856ad364e35_6.1.7601.17514_he-il_a5134adfb1f79c3a
1,C:\Windows\SysWOW64\drivers\en-US
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_48\grep\share\locale\ga\LC_MESSAGES
1,C:\Windows\winsxs\amd64_microsoft-windows-i..l-keyboard-00020437_31bf3856ad364e35_6.1.7600.16385_none_8c1c84c0615562b0
1,C:\Program Files (x86)\Microsoft Visual Studio 10.0\Common7\IDE\CommonExtensions\Platform\NavigateTo\FileProvider
1,C:\Windows\winsxs\amd64_microsoft-windows-f..toragereportservice_31bf3856ad364e35_6.1.7601.17514_none_88d677c4cbf02778
1,C:\Windows\diagnostics
1,C:\Windows\winsxs\amd64_microsoft-windows-ocsetup_31bf3856ad364e35_6.1.7601.17514_none_41a3376575e751b4
1,C:\Windows\winsxs\amd64_server-help-h1s.dfs2_lh.resources_31bf3856ad364e35_6.1.7600.16385_en-us_5e44ab16f4bd545b
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\System.Xml.Linq\3063abda312516739bc808360071bad9
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\PresentationFramewo#\f7fd822d5eda18da4ad1095020b42963
1,C:\Windows\System32\DriverStore\FileRepository\mdmnttme.inf_amd64_neutral_ece4b1cc5aee6a38
1,C:\Windows\winsxs\x86_microsoft-windows-os-kernel_31bf3856ad364e35_6.1.7601.18247_none_6e1a402c127aed77
1,C:\Windows\winsxs\msil_microsoft.windows.s..migration.downlevel_31bf3856ad364e35_6.1.7601.17514_none_acc3cb32fb786780
1,C:\Windows\winsxs\amd64_microsoft.windows.d..eshootingpackmodule_31bf3856ad364e35_6.1.7600.16385_none_7d19911b0fafbb5f
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_35\grep\share\locale\ko\LC_MESSAGES
1,C:\Windows\winsxs\amd64_iirsp.inf_31bf3856ad364e35_6.1.7600.16385_none_02496439a3048835
1,C:\Program Files (x86)\Tanium\Tanium Client\Tools\StdUtils\grep\share\locale\sv\LC_MESSAGES
1,C:\Windows\winsxs\x86_microsoft-windows-i..tocolimplementation_31bf3856ad364e35_11.2.9600.17358_none_882f3db7fe78ff91
1,C:\Windows\winsxs\amd64_wiahp001.inf_31bf3856ad364e35_6.1.7600.16385_none_ebc6374fdcadec8c
1,C:\Windows\winsxs\msil_microsoft.web.secur..gement.ws.resources_31bf3856ad364e35_6.1.7600.16385_en-us_c8db2fb334b222ab
1,C:\Windows\winsxs\amd64_microsoft-windows-d..-adamsync.resources_31bf3856ad364e35_6.1.7601.17514_en-us_fc7c0416355056ab
1,C:\Windows\winsxs\amd64_netfx-sys_data_oraclient_perfcoun_b03f5f7f11d50a3a_6.1.7600.16385_none_12b230ea15a9e57a
1,C:\Users\Jim Olsen\AppData\Local\Google\Chrome\User Data\Default\Storage\ext\chrome-signin\def
1,C:\Windows\winsxs\amd64_prnts002.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_06c0629adda1a73f
1,C:\Python27\tcl\tcl8.5\tzdata\Brazil
1,C:\Windows\winsxs\amd64_microsoft-windows-media-mp3acm.resources_31bf3856ad364e35_6.1.7600.16385_en-us_872be93eaa9f6a40
1,C:\Windows\winsxs\x86_microsoft-windows-m..s-mdac-odbc-cpxl437_31bf3856ad364e35_6.1.7600.16385_none_5d617cc7e53174c0
1,C:\Windows\winsxs\x86_microsoft-windows-m..uxiliarydisplay-api_31bf3856ad364e35_6.1.7600.16385_none_f87a6669d7d0ab48
1,C:\Windows\winsxs\amd64_microsoft-windows-r..licensing-component_31bf3856ad364e35_6.1.7601.17514_none_fd3debee02c1ae74
1,C:\Program Files (x86)\Microsoft SQL Server\90
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9028\grep\share\locale\ko\LC_MESSAGES
1,C:\Windows\winsxs\msil_system.web.routing_31bf3856ad364e35_6.1.7601.17514_none_1a58be6d26032dfe
1,C:\Program Files (x86)\Microsoft SQL Server\80
1,C:\Windows\winsxs\amd64_microsoft-windows-security-schannel-mof_31bf3856ad364e35_6.1.7600.16385_none_41b1a1917f0b6acd
1,C:\Windows\winsxs\wow64_microsoft-windows-audio-audiocore_31bf3856ad364e35_6.1.7601.17514_none_df1a73e82fa00c16
1,C:\Windows\winsxs\amd64_netfx-system.directoryservices_b03f5f7f11d50a3a_6.1.7601.22126_none_ffe9f729ba3ac93e
1,C:\Program Files (x86)\Microsoft SDKs\Windows\v7.0A
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_26\grep\share\locale\pt\LC_MESSAGES
1,C:\Windows\winsxs\amd64_netfx-mscorwks_dll_b03f5f7f11d50a3a_6.1.7601.17514_none_bf0c7965d70a0677
1,C:\Windows\winsxs\amd64_microsoft-windows-b..os-loader.resources_31bf3856ad364e35_6.1.7601.22736_en-us_d534a81a13cf81d6
1,C:\Windows\winsxs\msil_napinit_31bf3856ad364e35_6.1.7600.16385_none_0c1c21010a6f7ac2
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.DataTransformationServices.Controls\v4.0_11.0.0.0__89845dcd8080cc91
1,C:\Windows\inf\TermService\0409
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\System.Messaging
1,C:\Windows\winsxs\amd64_microsoft-windows-d2d.resources_31bf3856ad364e35_7.1.7601.16492_pt-pt_e93415d358c6c7f8
1,C:\Windows\winsxs\msil_aagmmc_31bf3856ad364e35_6.1.7601.17514_none_898dc291b8e98573
1,C:\Windows\winsxs\amd64_microsoft-windows-adfs-webagentclaims_31bf3856ad364e35_6.1.7600.16385_none_b1d49ce86105b3b0
1,C:\Windows\winsxs\amd64_server-help-chm.tpmadmin.resources_31bf3856ad364e35_6.1.7600.16385_en-us_f4a21ac6fd93957d
1,C:\Windows\winsxs\amd64_microsoft-windows-font-truetype-miriam_31bf3856ad364e35_6.1.7600.16385_none_7b7a9e11df9f30a1
1,C:\Windows\assembly\GAC_MSIL\Microsoft.ReportViewer.WebForms.resources
1,C:\Windows\winsxs\x86_microsoft-windows-muicachebuilder_31bf3856ad364e35_6.1.7601.17514_none_1c140627131a6df3
1,C:\Windows\winsxs\x86_microsoft-windows-i..er-engine.resources_31bf3856ad364e35_6.1.7601.17514_sl-si_3077981303bb82bb
1,C:\Windows\winsxs\amd64_microsoft-windows-errorreportingcore_31bf3856ad364e35_6.1.7601.22584_none_7eda8c2e35da4605
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_18\grep\share\locale\da\LC_MESSAGES
1,C:\Users\Jim Olsen\AppData\Local\Microsoft\Internet Explorer\IECompatData
1,C:\Windows\winsxs\wow64_microsoft-windows-i..etexplorer-optional_31bf3856ad364e35_11.2.9600.17041_none_858ffb5bf711c81f
1,C:\Windows\winsxs\amd64_microsoft-windows-a..ility-assistant-adm_31bf3856ad364e35_6.1.7600.16385_none_7b487ca06770a648
1,C:\Windows\winsxs\amd64_microsoft-windows-mlang.resources_31bf3856ad364e35_6.1.7600.16385_zh-hk_4068f777147d0327
1,C:\Windows\winsxs\amd64_microsoft-windows-i..l-keyboard-0000045a_31bf3856ad364e35_6.1.7600.16385_none_587ffcaa703a19a6
1,C:\Windows\winsxs\msil_microsoft.security...agement.policymodel_31bf3856ad364e35_6.1.7600.16385_none_a590f64d5cfc5ee6
1,C:\Windows\winsxs\amd64_server-help-h1s.ts_workspace.resources_31bf3856ad364e35_6.1.7600.16385_en-us_5ac6cdee8e955606
1,C:\Windows\winsxs\msil_smsvchost_b03f5f7f11d50a3a_6.1.7601.22743_none_cfeb95652ab9a380
1,C:\Windows\winsxs\amd64_microsoft-windows-ie-f12-provider_31bf3856ad364e35_11.2.9600.17420_none_bd94efe47e8cda1f
1,C:\Windows\winsxs\amd64_microsoft-windows-l..verwinsbv.resources_31bf3856ad364e35_6.1.7600.16385_en-us_123629cbcb3c1d84
1,C:\Windows\assembly\NativeImages_v4.0.30319_64\System.Comp7dda8007#\4b684fa1cf890ed47d5a722193b11d37
1,C:\Windows\SysWOW64\en-US\Licenses\_Default\ServerStorageEnterprise
1,C:\Windows\winsxs\x86_microsoft-windows-m..server-provider-rll_31bf3856ad364e35_6.1.7600.16385_none_64ce4cfce74e3347
1,C:\Windows\winsxs\x86_microsoft-windows-photoviewer.resources_31bf3856ad364e35_6.1.7600.16385_en-us_1f351a21979e0848
1,C:\Windows\winsxs\amd64_microsoft-windows-n..n_service_licensing_31bf3856ad364e35_6.1.7600.16385_none_6e4d66798d098a3d
1,C:\Windows\winsxs\amd64_microsoft-windows-b..nager-efi.resources_31bf3856ad364e35_6.1.7600.16385_zh-tw_3e4f8e47e730ab98
1,C:\Windows\assembly\GAC_MSIL\Microsoft.Web.Administration\7.0.0.0__31bf3856ad364e35
1,C:\Windows\winsxs\x86_netfx-aspnet_wp_exe_b03f5f7f11d50a3a_6.1.7601.18205_none_99441e0948ed8ae7
1,C:\Windows\winsxs\amd64_microsoft-windows-msxml30_31bf3856ad364e35_6.1.7601.17514_none_e6944609ad75ac7d
1,C:\Program Files (x86)\Microsoft SQL Server\110\Tools\Templates
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_37\grep\share\locale\nl\LC_MESSAGES
1,C:\Windows\winsxs\wow64_microsoft-windows-i..etexplorer-optional_31bf3856ad364e35_11.2.9600.17358_none_856fec69f729e8b0
1,C:\Windows\winsxs\x86_microsoft-windows-l..gementsvc.resources_31bf3856ad364e35_6.1.7600.16385_en-us_bdce5e8f2057dbf5
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9042\grep\man
1,C:\Windows\winsxs\amd64_microsoft-windows-qos.resources_31bf3856ad364e35_6.1.7600.16385_en-us_97579d95c8092c0f
1,C:\Windows\winsxs\amd64_microsoft-windows-g..-computer.resources_31bf3856ad364e35_6.1.7601.17514_en-us_b08d7490ca2188cd
1,C:\Windows\winsxs\x86_microsoft-windows-fdeploy.resources_31bf3856ad364e35_6.1.7600.16385_en-us_0d70be959d80ac53
1,C:\Windows\winsxs\amd64_microsoft-windows-fax-service.resources_31bf3856ad364e35_6.1.7600.16385_en-us_36e0de390f55ac1d
1,C:\Windows\winsxs\msil_system.data.sqlxml_b77a5c561934e089_6.1.7601.18529_none_05d526a261a2bd9d
1,C:\Windows\winsxs\msil_microsoft.visualbasic.compatibility_b03f5f7f11d50a3a_6.1.7601.17514_none_c1c1077951dca19a
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_35\grep\share\locale\fr\LC_MESSAGES
1,C:\Windows\assembly\NativeImages_v4.0.30319_64\Microsoft.S6a1f6e12#\f400877b07f0bce50e102093835631b4
1,C:\Windows\assembly\GAC_MSIL\napsnap
1,C:\Users\Default\AppData\Roaming\Microsoft
1,C:\Windows\Downloaded Program Files
1,C:\Windows\winsxs\x86_microsoft-windows-d..g-adminui.resources_31bf3856ad364e35_6.1.7600.16385_en-us_b82c74eec637335f
1,C:\Windows\Installer\{BED1EA3D-592D-4305-9D1F-20F03726EFC1}
1,C:\Windows\System32\en-US\Licenses\eval\ServerEssentialAdditional
1,C:\Windows\winsxs\wow64_microsoft-windows-ie-ieetwcollector_31bf3856ad364e35_11.2.9600.17239_none_afd8df784c24b3b6
1,C:\Windows\winsxs\x86_microsoft-windows-m..onents-mdac-odbcbcp_31bf3856ad364e35_6.1.7600.16385_none_b0d14a16af76d049
1,C:\Windows\winsxs\x86_microsoft-windows-ncrypt-dll_31bf3856ad364e35_6.1.7601.22010_none_606b38f468ff8cd3
1,C:\Windows\winsxs\amd64_mdmpace.inf_31bf3856ad364e35_6.1.7600.16385_none_1fe2fc8d4a1d4f7d
1,C:\Windows\assembly\NativeImages_v4.0.30319_64\System.Data.Linq\d8ac424adb7b7b4483bcf3aacb595ddf
1,C:\Windows\winsxs\amd64_microsoft-windows-w..-provider.resources_31bf3856ad364e35_6.1.7600.16385_en-us_572656a8a53c6a63
1,C:\Windows\winsxs\amd64_microsoft-windows-com-dtc-tracing_31bf3856ad364e35_6.1.7600.16385_none_73d43c6a0c805ae7
1,C:\Windows\winsxs\x86_microsoft-windows-basedependencies_31bf3856ad364e35_6.1.7600.16385_none_027847e78a22fdb1
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.Xaml\v4.0_4.0.0.0__b77a5c561934e089
1,C:\Windows\winsxs\x86_microsoft-windows-l2na.resources_31bf3856ad364e35_6.1.7600.16385_en-us_a62167de39951d5f
1,C:\Windows\winsxs\amd64_scsidev.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_de2a981bd7e66585
1,C:\Windows\winsxs\amd64_microsoft-windows-d..iagnostic.resources_31bf3856ad364e35_6.1.7600.16385_en-us_ddf81a85f99d6d20
1,C:\Windows\winsxs\x86_microsoft.windows.c..-controls.resources_6595b64144ccf1df_5.82.7600.16385_sk-sk_ea3f9509df3aaa93
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.Vd5001c35#\84eeb098e86a18b2dbf471975427083b
1,C:\Windows\winsxs\x86_microsoft-windows-ie-controls.resources_31bf3856ad364e35_11.2.9600.16428_en-us_34218f701493f41c
1,C:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\schemas\sqlserver\2004\SOAP\types\SqlResultStream
1,C:\Windows\winsxs\x86_microsoft-windows-s..-binaries.resources_31bf3856ad364e35_6.1.7601.17514_bg-bg_68d21d71f179ba4c
1,C:\Windows\winsxs\wow64_microsoft-windows-ie-htmlrendering_31bf3856ad364e35_8.0.7601.18571_none_96341266e45f3517
1,C:\Windows\winsxs\x86_microsoft-windows-i..rityzones.resources_31bf3856ad364e35_11.2.9600.17239_en-us_f4d1b46a3e1920f7
1,C:\Windows\winsxs\x86_microsoft-windows-t..ager-snapin-nonmsil_31bf3856ad364e35_6.1.7601.17514_none_8ddf701800eea858
1,C:\Windows\winsxs\amd64_wcf-system.servicemodel.washosting_b03f5f7f11d50a3a_6.1.7601.22733_none_eb759ec5609ff00b
1,C:\Windows\winsxs\amd64_microsoft-windows-b..gertransport-serial_31bf3856ad364e35_6.1.7601.21655_none_703aeff2dc87a23b
1,C:\Windows\winsxs\amd64_microsoft-windows-f..vices-bpa.resources_31bf3856ad364e35_7.1.7600.16422_en-us_badf5eb9b8b2a0e3
1,C:\Windows\Microsoft.NET\Framework64\v4.0.30319\ASP.NETWebAdminFiles\AppConfig\App_LocalResources
1,C:\Users\All Users\Microsoft\Vault
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.V969c9247#
1,C:\Users\Default\AppData\Roaming\Microsoft\Windows\Start Menu\Programs
1,C:\Windows\winsxs\x86_microsoft-windows-d..ing-management-core_31bf3856ad364e35_6.1.7601.17514_none_2d3b8ff08901343f
1,C:\Windows\System32\DriverStore\FileRepository\prnsa002.inf_amd64_neutral_d9df1d04d8cbe336\Amd64
1,C:\Windows\winsxs\x86_microsoft-windows-p..age-codec.resources_31bf3856ad364e35_7.1.7601.16492_hu-hu_8c9313d3f0035f71
1,C:\Windows\winsxs\amd64_microsoft-windows-com-dtc-client_31bf3856ad364e35_6.1.7600.16385_none_a8e7df5dd2fecf4e
1,C:\Windows\System32\DriverStore\FileRepository\netb57va.inf_amd64_neutral_6264e97d4fc12211
1,C:\Windows\winsxs\x86_microsoft-windows-c..ityclient.resources_31bf3856ad364e35_6.1.7601.22705_en-us_675c18f5172b8636
1,C:\Windows\assembly\GAC_MSIL\Microsoft.Windows.Diagnosis.TroubleshootingPack\6.1.0.0__31bf3856ad364e35
1,C:\Windows\winsxs\amd64_microsoft-windows-ndisuio_31bf3856ad364e35_6.1.7601.17514_none_ca170d32fd7da822
1,C:\Windows\winsxs\amd64_microsoft-windows-t..tkeyboard.resources_31bf3856ad364e35_6.1.7600.16385_en-us_441e533e5fd46b57
1,C:\Windows\winsxs\amd64_microsoft-windows-ie-ratings.resources_31bf3856ad364e35_8.0.7600.16385_en-us_d06c65741a79bece
1,C:\Windows\winsxs\amd64_microsoft-windows-kernel32.resources_31bf3856ad364e35_6.1.7601.22125_en-us_9bc075d0550900c8
1,C:\Windows\winsxs\amd64_netg664.inf_31bf3856ad364e35_6.1.7600.16385_none_3e838f62f7e92ab2
1,C:\Windows\winsxs\amd64_microsoft-windows-tcpip-adm.resources_31bf3856ad364e35_6.1.7601.22124_en-us_35aca0a73d918fae
1,C:\Windows\assembly\GAC_MSIL\Microsoft.Windows.Diagnosis.TroubleshootingPack.Resources\6.1.0.0_en_31bf3856ad364e35
1,C:\Windows\winsxs\amd64_wcf-m_svc_mod_op_perf_c_reg_31bf3856ad364e35_6.1.7600.16385_none_23b47b1a46320a55
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\UIAutomationClient
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9026\grep
1,C:\Windows\winsxs\amd64_netbvbda.inf_31bf3856ad364e35_6.1.7600.16385_none_fa388bc43a1db8d8
1,C:\Windows\winsxs\amd64_netfx-vb_compiler_ui_b03f5f7f11d50a3a_6.1.7600.16385_none_281aa88152564d62
1,C:\Windows\winsxs\x86_netfx35linq-system.core_31bf3856ad364e35_6.1.7601.17514_none_6161fc35ed136622
1,C:\Windows\winsxs\amd64_microsoft-windows-blb-engine-main_31bf3856ad364e35_6.1.7601.17514_none_4207fb67165f731a
1,C:\Windows\winsxs\amd64_microsoft.windows.s..ermanager.resources_31bf3856ad364e35_6.1.7601.17514_en-us_acfc1bedef374d3e
1,C:\Windows\assembly\GAC_MSIL\Microsoft.VisualStudio.TextManager.Interop.10.0\10.0.0.0__b03f5f7f11d50a3a
1,C:\Windows\assembly\NativeImages_v4.0.30319_64\Microsoft.Seae4f488#
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9033\grep\share\locale\bg\LC_MESSAGES
1,C:\Python27\Lib\json
1,C:\Windows\winsxs\amd64_wcf-system.servicemodel_b03f5f7f11d50a3a_6.1.7601.18532_none_a1aa0c9e9399ac00
1,C:\Users\Jim Olsen\AppData\Local
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_18\grep\man
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.Dynamic.Runtime\v4.0_4.0.0.0__b03f5f7f11d50a3a
1,C:\Windows\winsxs\amd64_microsoft-windows-s..llercommandlinetool_31bf3856ad364e35_6.1.7600.16385_none_d0632cbfee5db937
1,C:\Windows\winsxs\amd64_microsoft-windows-dns-client-winrnr_31bf3856ad364e35_6.1.7600.16385_none_b543449669c73e11
1,C:\Windows\winsxs\amd64_tpm.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_5cf8a45092f4398d
1,C:\Windows\winsxs\x86_netfx35linq-microso..ild.conversion.v3.5_31bf3856ad364e35_6.1.7600.16385_none_397c457d247d92a0
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\System.Windows.Pres#
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.V78b5b27e#\5a605232baa4a7d29ba3132780da8388
1,C:\Windows\winsxs\x86_microsoft-windows-t..vices-configbackend_31bf3856ad364e35_6.1.7600.16385_none_d66b4dbb52eb8cae
1,C:\Windows\winsxs\x86_microsoft-windows-i..nal-nlsdownleveldll_31bf3856ad364e35_6.1.7600.16385_none_087f597fb956baeb
1,C:\Windows\winsxs\amd64_microsoft-windows-a..rvice-adm.resources_31bf3856ad364e35_6.1.7600.16385_en-us_68408642f41ba602
1,C:\Windows\winsxs\x86_netfx-_vc_assembly_linker_messages_b03f5f7f11d50a3a_6.1.7601.18523_none_398e4a7961a6d332
1,C:\Windows\winsxs\amd64_microsoft-windows-w..eakerstemmer-korean_31bf3856ad364e35_7.0.7600.16385_none_a7ca197ff4659c3d
1,C:\Program Files\Tanium\Tanium Server\Apache24\htdocs\console\history
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_37\grep\share\locale\ko\LC_MESSAGES
1,C:\Windows\winsxs\amd64_microsoft-windows-smss_31bf3856ad364e35_6.1.7601.22411_none_0ae72ec548f19d13
1,C:\Windows\assembly\GAC_MSIL\Microsoft.SqlServer.Management.MultiServerConnection
1,C:\Windows\winsxs\msil_smdiagnostics_b77a5c561934e089_6.1.7601.18532_none_72f0e00b6ca38779
1,C:\Windows\winsxs\wow64_microsoft-windows-ie-sysprep_31bf3856ad364e35_11.2.9600.16428_none_083dd731036b79d4
1,C:\Windows\winsxs\amd64_microsoft-windows-i..trolpanel.resources_31bf3856ad364e35_8.0.7601.17514_en-us_9b6af1fe75cda5cc
1,C:\Windows\SysWOW64\config\systemprofile\AppData\Local\Microsoft\Windows\Temporary Internet Files\Content.IE5\A5OS7C95
1,C:\Program Files (x86)\Tanium\Tanium Client\Tools\StdUtils\grep\share\locale\ca\LC_MESSAGES
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9032\grep\share\locale\pt\LC_MESSAGES
1,C:\Windows\winsxs\x86_microsoft-windows-c..tionauthorityclient_31bf3856ad364e35_6.1.7601.22653_none_d9e26570b428b109
1,C:\Windows\assembly\GAC_MSIL\System.Windows.Presentation
1,C:\Windows\winsxs\amd64_microsoft-windows-l..geexpress.resources_31bf3856ad364e35_6.1.7600.16385_en-us_f9a5260e9a61f34a
1,C:\Windows\winsxs\amd64_mdmbr007.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_186c2c8ed691aa61
1,C:\Windows\winsxs\amd64_microsoft-windows-advapi32_31bf3856ad364e35_6.1.7601.22436_none_41e43a0cb64d6c9e
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_18\grep\share\locale\ru\LC_MESSAGES
1,C:\Windows\winsxs\amd64_microsoft-windows-c..complus-runtime-qfe_31bf3856ad364e35_6.1.7600.16385_none_c7582028923fd980
1,C:\Windows\winsxs\x86_microsoft-windows-security-credssp_31bf3856ad364e35_6.1.7601.22865_none_c61415d8191776a1
1,C:\Windows\winsxs\x86_microsoft-windows-d..ervicing-management_31bf3856ad364e35_6.1.7600.16385_none_5e7ff93b6f0000b7
1,C:\Windows\System32\WindowsPowerShell\v1.0\Modules
1,C:\Windows\diagnostics\system\PCW\en-US
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.Ddc0c32eb#
1,C:\Windows\winsxs\amd64_microsoft-windows-shdocvw.resources_31bf3856ad364e35_6.1.7601.22403_en-us_267c18cf89f1b2b9
1,C:\Windows\winsxs\amd64_microsoft-windows-a..es-interface-router_31bf3856ad364e35_6.1.7600.16385_none_b3eaf84f983a33ee
1,C:\Windows\winsxs\amd64_microsoft-hyper-v-clustering-vmclusex_31bf3856ad364e35_6.1.7600.16385_none_7269d6cc3517cad1
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.S2712f5ba#
1,C:\Windows\winsxs\amd64_microsoft-windows-g..validatefntcache-03_31bf3856ad364e35_6.1.7600.21258_none_a56ffdd44d4053c0
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\SrpUxSnapIn\ed407e1bee9113f340584de83ad7692c
1,C:\Windows\winsxs\x86_wpf-uiautomationclientsideproviders_31bf3856ad364e35_6.1.7600.16385_none_54926688afb9f1e9
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\System.Runtime.Remo#
1,C:\Windows\winsxs\msil_microsoft.bestpractices_31bf3856ad364e35_6.1.7600.16385_none_900eab16ba805783
1,C:\Windows\System32\DriverStore\FileRepository\tsusbhubfilter.inf_amd64_neutral_d0615d6fd67bad03
1,C:\Windows\winsxs\x86_microsoft-windows-d..computers.resources_31bf3856ad364e35_6.1.7601.17514_en-us_8f1f3a4e13edfb30
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.VisualStudio.Editors\v4.0_10.0.0.0__b03f5f7f11d50a3a
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.Sae9b8ed1#
1,C:\Windows\winsxs\x86_microsoft-windows-i..er-engine.resources_31bf3856ad364e35_6.1.7601.17514_pl-pl_4871a5da2b2cebc2
1,C:\Windows\winsxs\amd64_microsoft-windows-sud_31bf3856ad364e35_6.1.7601.17514_none_05cbfa317289b4af
1,C:\Windows\winsxs\amd64_microsoft-windows-registry-editor_31bf3856ad364e35_6.1.7600.16385_none_5023a70bf589ad3e
1,C:\Windows\winsxs\amd64_ql40xx.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_d3a27a362b551c07
1,C:\Windows\winsxs\x86_microsoft-windows-d..ommandline-redirect_31bf3856ad364e35_6.1.7600.16385_none_2d3a368613e27ef0
1,C:\Windows\winsxs\x86_microsoft-windows-video-for-windows16_31bf3856ad364e35_6.1.7600.16385_none_5fd0557cd88ef5bd
1,C:\Windows\winsxs\x86_microsoft-windows-d..ices-boot-files-x64_31bf3856ad364e35_6.1.7601.22736_none_bea4c27935b328e9
1,C:\Windows\winsxs\amd64_microsoft-windows-i..ttpprotocolbinaries_31bf3856ad364e35_6.1.7600.16385_none_f5c9ab3453234070
1,C:\Windows\winsxs\amd64_microsoft-windows-ocspsvc.resources_31bf3856ad364e35_6.1.7601.22712_en-us_b37fd6fae5a1ce7d
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.VisualStudio.Platform.VSEditor\v4.0_10.0.0.0__b03f5f7f11d50a3a
1,C:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\SqlWorkbenchProjectItems\Sql\Database
1,C:\Windows\System32\DriverStore\FileRepository\mshdc.inf_amd64_neutral_552ea5111ec825a6
1,C:\Users\Jim Olsen\AppData\Local\Microsoft\Internet Explorer\VersionManager
1,C:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\SqlWorkbenchProjectItems\Sql\Function
1,C:\Windows\winsxs\x86_system.web.security..non.claimtransforms_31bf3856ad364e35_6.1.7600.16385_none_653a2bcb369d63be
1,C:\Windows\winsxs\x86_microsoft-windows-w..-infrastructure-bsp_31bf3856ad364e35_6.1.7601.18254_none_ba2f64c78bae6989
1,C:\Windows\winsxs\x86_microsoft-windows-cdosys.resources_31bf3856ad364e35_6.1.7601.17514_sv-se_476e370068602811
1,C:\Windows\winsxs\amd64_microsoft-windows-m..ow-gadget.resources_31bf3856ad364e35_6.1.7600.16385_en-us_e45ff59acede6483
1,C:\Windows\winsxs\x86_presentationcore_31bf3856ad364e35_6.1.7601.17755_none_ae0e4090ee55e5f0
1,C:\Windows\winsxs\amd64_microsoft-windows-d..aanalyzer.resources_31bf3856ad364e35_6.1.7601.17514_en-us_81c4acf1faf29d3d
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.Data.DataSetExtensions
1,C:\Windows\winsxs\wow64_microsoft-windows-coreos_31bf3856ad364e35_6.1.7601.18288_none_8d852b428986de92
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_51\grep\manifest
1,C:\Windows\winsxs\x86_wpf-presentationcffrasterizernative_31bf3856ad364e35_6.1.7600.16385_none_c96bb53eefa606a7
1,C:\Windows\winsxs\x86_microsoft-windows-setx_31bf3856ad364e35_6.1.7600.16385_none_ac4d2bf27a63f85f
1,C:\Windows\winsxs\amd64_microsoft-windows-ie-antiphishfilter_31bf3856ad364e35_8.0.7600.16385_none_72414f35fc718b5d
1,C:\Windows\winsxs\wow64_microsoft-windows-i..stfilteringbinaries_31bf3856ad364e35_6.1.7600.16385_none_38daa6d0fa5c3fac
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.VisualStudio.TextTemplating.Modeling.10.0\v4.0_10.0.0.0__b03f5f7f11d50a3a
1,C:\Users\Jim Olsen\AppData\Local\Google\Chrome\User Data\Default\Extensions\aohghmighlieiainnegkcijnfilokake\0.7_0\_locales\en_US
1,C:\Windows\winsxs\x86_netfx-web_engine_dll_b03f5f7f11d50a3a_6.1.7601.18410_none_0afbfa6df48eab41
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_52\grep\share\locale\bg\LC_MESSAGES
1,C:\Windows\winsxs\msil_microsoft.storage.sancommon.resources_31bf3856ad364e35_6.1.7601.17514_en-us_93efbccba2864c06
1,C:\Windows\winsxs\msil_system.runtime.remoting_b77a5c561934e089_6.1.7601.18410_none_99f1269f01d59174
1,C:\Windows\winsxs\amd64_microsoft-windows-wab-core.resources_31bf3856ad364e35_6.1.7600.16385_en-us_0c4d010cb13d4746
1,C:\Windows\winsxs\amd64_microsoft-windows-iologgingdll.resources_31bf3856ad364e35_6.1.7601.18386_en-us_52e76a5df068c2f9
1,C:\Program Files (x86)\Tanium\Tanium Client\Tools\StdUtils\grep\share\locale\sk\LC_MESSAGES
1,C:\Windows\winsxs\x86_microsoft-windows-advapi32_31bf3856ad364e35_6.1.7601.17514_none_e54fbb95e4c3d1bb
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9029\grep\share\locale\id\LC_MESSAGES
1,C:\Windows\winsxs\amd64_microsoft-windows-ie-adminkitbranding_31bf3856ad364e35_11.2.9600.17280_none_56c3d9416c74f49a
1,C:\Windows\winsxs\x86_netfx-shared_netfx_20_mscorwks_31bf3856ad364e35_6.1.7601.22724_none_8234995dbdb9c5f5
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\UIAutomatio4e153cb6#\d46a55d0e870a8ad2cb0b1d6d7b7f6e6
1,C:\Windows\winsxs\x86_microsoft-windows-l..nspremium.resources_31bf3856ad364e35_6.1.7600.16385_en-us_368ed530484c96ae
1,C:\Windows\winsxs\x86_microsoft-windows-console.resources_31bf3856ad364e35_6.1.7600.16385_en-us_7df7d893a3a353f9
1,C:\Users\Jim Olsen\AppData\Local\Temp\nsg79B3.tmp
1,C:\Windows\winsxs\wow64_microsoft-windows-s..ty-protectedstorage_31bf3856ad364e35_6.1.7600.16385_none_ae92b0937e708d46
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_37\grep\share\locale\fr\LC_MESSAGES
1,C:\Windows\SysWOW64\en-US\Licenses\_Default\ServerWinFoundation
1,C:\Program Files\Common Files\VMware\Drivers\vmci\sockets\include
1,C:\Windows\Microsoft.NET\Framework64\v4.0.30319\SetupCache
1,C:\Windows\System32\DriverStore\FileRepository\mshdc.inf_amd64_neutral_aad30bdeec04ea5e
1,C:\Windows\winsxs\x86_microsoft-windows-browserservice-netapi_31bf3856ad364e35_6.1.7601.17887_none_2f4c24e0f632f0d7
1,C:\Windows\winsxs\x86_microsoft-windows-lsa-msprivs.resources_31bf3856ad364e35_6.1.7600.16385_zh-cn_c6baef0e416653d3
1,C:\Users\Jim Olsen\Music
1,C:\Windows\winsxs\amd64_microsoft-windows-ie-jscriptdebugui_31bf3856ad364e35_8.0.7601.18571_none_3308a4565b7a34cf
1,C:\Users\Jim Olsen\AppData\Local\Google\Chrome\User Data\Default\Extensions\aohghmighlieiainnegkcijnfilokake\0.7_0\_locales\en_GB
1,C:\Windows\winsxs\amd64_microsoft-windows-n.._service_runtimeapi_31bf3856ad364e35_6.1.7600.16385_none_e789f0e67a8cb67d
1,C:\Windows\winsxs\amd64_microsoft-windows-w..onservice.resources_31bf3856ad364e35_6.1.7600.16385_en-us_f39c7dc580011c1c
1,C:\Windows\winsxs\x86_microsoft-windows-i..o4-codecs.resources_31bf3856ad364e35_6.1.7600.16385_en-us_fdd5773ab7f778a7
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_48\grep\share\locale\be\LC_MESSAGES
1,C:\Windows\winsxs\amd64_microsoft-windows-i..rityzones.resources_31bf3856ad364e35_11.2.9600.17041_en-us_5107a64ff664a69a
1,C:\Windows\winsxs\amd64_prnca00c.inf_31bf3856ad364e35_6.1.7600.16385_none_ddc7f96bf68e339f\Amd64
1,C:\Windows\winsxs\amd64_prnin003.inf_31bf3856ad364e35_6.1.7600.16385_none_11a5503ce5abb7ec
1,C:\Windows\winsxs\amd64_microsoft-windows-i..libraries.resources_31bf3856ad364e35_6.1.7600.16385_en-us_ac2f25e3d4ed4318
1,C:\Windows\winsxs\amd64_microsoft-windows-help-sharing.resources_31bf3856ad364e35_6.1.7600.16385_en-us_c09c55124df2c34c
1,C:\Windows\winsxs\x86_microsoft-windows-vssproxystub_31bf3856ad364e35_6.1.7600.16385_none_3092767d8b44f463
1,C:\Windows\winsxs\x86_microsoft-windows-dot3gpclient_31bf3856ad364e35_6.1.7600.16385_none_7a2a3d711dcb2bb3
1,C:\Windows\winsxs\amd64_microsoft-windows-s..ngine-adm.resources_31bf3856ad364e35_6.1.7600.16385_en-us_92ae7bc7fccaab93
1,C:\Windows\SysWOW64\Tasks\Microsoft\Windows\PLA\System
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\EnvDTE\e49bbbb530f07efcd89ea2e679fed2b3
1,C:\Windows\assembly\NativeImages_v4.0.30319_64\System.Dire573b08f5#
1,C:\Windows\winsxs\amd64_microsoft-windows-e..otocol-host-service_31bf3856ad364e35_6.1.7600.16385_none_e63ed98817cf16b1
1,C:\Windows\winsxs\amd64_microsoft-windows-help-ics.resources_31bf3856ad364e35_6.1.7600.16385_en-us_bd437fd8ba6789d7
1,C:\Windows\inf\StarterGPOs\{B52976F5-3EE4-4C77-80B9-11911F065EF7}\Machine
1,C:\inetpub\history\CFGHISTORY_0000000002
1,C:\inetpub\history\CFGHISTORY_0000000003
1,C:\inetpub\history\CFGHISTORY_0000000001
1,C:\inetpub\history\CFGHISTORY_0000000006
1,C:\inetpub\history\CFGHISTORY_0000000004
1,C:\inetpub\history\CFGHISTORY_0000000005
1,C:\Windows\winsxs\amd64_microsoft-windows-securitycenter-adm_31bf3856ad364e35_6.1.7600.16385_none_423ff0e3a3f91a83
1,C:\Windows\winsxs\amd64_microsoft-windows-nap-oobshv_31bf3856ad364e35_6.1.7600.16385_none_efd6cac15d5cf99e
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\ComSvcConfig
1,C:\Windows\winsxs\amd64_mstape.inf_31bf3856ad364e35_6.1.7600.16385_none_89fe250f2f057e08
1,C:\Windows\winsxs\amd64_microsoft.windows.c..-controls.resources_6595b64144ccf1df_6.0.7600.16385_de-de_677ec5ef54cba91e
1,C:\Windows\winsxs\amd64_tape.inf_31bf3856ad364e35_6.1.7600.16385_none_426fc940972f24c6
1,C:\Users\Jim Olsen\AppData\Local\Temporary Internet Files
1,C:\Windows\winsxs\amd64_microsoft-windows-dhcp-client-dll_31bf3856ad364e35_6.1.7601.22130_none_35f00a945e60f3e9
1,C:\Windows\assembly\NativeImages_v4.0.30319_64\System.Ente96d83b35#\c44702fea0bcbd8e4b3e930f1f5ec2b7
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\System.Serv14b62006#\50ad6d7905012a0b6803293630998352
1,C:\Windows\winsxs\amd64_megasas.inf_31bf3856ad364e35_6.1.7600.16385_none_8c3546e368634d85
1,C:\Windows\winsxs\x86_microsoft-windows-msmq-runtime_31bf3856ad364e35_6.1.7601.17514_none_a2e93e679472903c
1,C:\Windows\winsxs\amd64_microsoft-windows-dfsr-readonly_31bf3856ad364e35_6.1.7601.17514_none_adac10295a6399ef
1,C:\Windows\winsxs\x86_microsoft-windows-cdosys.resources_31bf3856ad364e35_6.1.7601.17514_de-de_b9615ede3154164a
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.Reflection\v4.0_4.0.0.0__b03f5f7f11d50a3a
1,C:\Windows\winsxs\msil_microsoft.jscript_b03f5f7f11d50a3a_6.1.7601.22733_none_8fbdcd1c5957f508
1,C:\Program Files (x86)\Microsoft SQL Server\100\Shared
1,C:\Windows\assembly\GAC_32\System.Transactions
1,C:\Windows\winsxs\x86_microsoft-windows-m..s-components-jetole_31bf3856ad364e35_6.1.7600.16385_none_7726de8ef25840f2
1,C:\Windows\winsxs\wow64_microsoft-windows-pnpdevicemanager_31bf3856ad364e35_6.1.7600.16385_none_7a20366b6d92814f
1,C:\Windows\winsxs\amd64_microsoft-windows-sort_31bf3856ad364e35_6.1.7600.16385_none_07b314fa3333f10d
1,C:\Program Files (x86)\Tanium\Tanium Client\Tools\StdUtils\grep\contrib\grep\2.5.4\grep-2.5.4-src\doc
1,C:\Windows\winsxs\amd64_microsoft-windows-i..timezones.resources_31bf3856ad364e35_6.1.7601.18588_en-us_e1539265989b5275
1,C:\Windows\winsxs\msil_microsoft.build.engine_b03f5f7f11d50a3a_6.1.7601.17514_none_0cfd67f8cb24384c
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\PresentationBuildTasks
1,C:\Windows\winsxs\x86_microsoft-windows-comctl32-v5.resources_31bf3856ad364e35_6.1.7600.16385_da-dk_bc83aeba06823a38
1,C:\Windows\winsxs\amd64_microsoft-windows-d..cking-adm.resources_31bf3856ad364e35_6.1.7600.16385_en-us_817cd4dab042e1f5
1,C:\Windows\SysWOW64\migration\WSMT\rras\dlmanifests
1,C:\Windows\winsxs\amd64_microsoft-windows-a..ence-mitigations-c3_31bf3856ad364e35_6.1.7601.18076_none_6a0b3ef309192aee
1,C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
1,C:\Windows\System32\DriverStore\FileRepository\mdmgl001.inf_amd64_neutral_9209e816461a1a73
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_63\grep\share\locale\hr\LC_MESSAGES
1,C:\Windows\winsxs\amd64_microsoft-windows-ie-f12_31bf3856ad364e35_11.2.9600.17041_none_d0392feefd4e1c62
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\SecurityAuditPolici#
1,C:\Windows\assembly\GAC_MSIL\Microsoft.SqlServer.GridControl.resources\11.0.0.0_ko_89845dcd8080cc91
1,C:\Windows\System32\DriverStore\FileRepository\hdaudio.inf_amd64_neutral_ce7bc199c85ae0a0
1,C:\Windows\winsxs\amd64_netfx-system.management_b03f5f7f11d50a3a_6.1.7601.17514_none_f6397b438cd5e46b
1,C:\Windows\winsxs\amd64_microsoft-windows-w..enger-adm.resources_31bf3856ad364e35_6.1.7600.16385_en-us_eca185f03b488843
1,C:\Windows\winsxs\x86_microsoft-windows-m..ds-ce-rll.resources_31bf3856ad364e35_6.1.7600.16385_en-us_0def3c4a82afa650
1,C:\Windows\winsxs\amd64_microsoft-windows-t..cheduler-apis-proxy_31bf3856ad364e35_6.1.7600.16385_none_31a8e7113546f43e
1,C:\Windows\inf\StarterGPOs\{9C03F88D-8608-44B7-A3E7-7316D1CAC152}
1,C:\Windows\winsxs\amd64_microsoft-windows-bcrypt-primitives-dll_31bf3856ad364e35_6.1.7601.17514_none_70577ed42da9d71d
1,C:\Windows\System32\DriverStore\FileRepository\prnep00c.inf_amd64_neutral_f0d9ddf52f04765c
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_47\grep\share\locale\be\LC_MESSAGES
1,C:\Windows\winsxs\amd64_microsoft-windows-o..s-service.resources_31bf3856ad364e35_6.1.7600.16385_en-us_b478b9e3e9b9a4f4
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.V48e48ead#
1,C:\Windows\winsxs\wow64_windowssearchengine.resources_31bf3856ad364e35_7.0.7600.16385_en-us_1eb04467622ff377
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_23\grep\share\locale\es\LC_MESSAGES
1,C:\Python27\Lib\sqlite3\test
1,C:\Windows\winsxs\x86_microsoft-windows-wdc-events_31bf3856ad364e35_6.1.7600.16385_none_d3d56c8ea90213c5
1,C:\Windows\winsxs\amd64_microsoft-windows-b..vironment-os-loader_31bf3856ad364e35_6.1.7601.17514_none_b94cbfa183466a89
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_48\grep\share\locale\af\LC_MESSAGES
1,C:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\SqlWorkbenchProjectItems\Sql\Recursive Queries
1,C:\Windows\winsxs\amd64_netb57va.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_33385dd47fa88b38
1,C:\Windows\System32\DriverStore\FileRepository\netbc664.inf_amd64_neutral_673d3dfb961e9b17
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\System.Drawing
1,C:\Windows\winsxs\wow64_microsoft-windows-powershell_31bf3856ad364e35_6.1.7601.17514_none_65ab62a5f1bba14b
1,C:\Windows\winsxs\amd64_netfx-dfdll_dll_b03f5f7f11d50a3a_6.1.7601.22794_none_fe39bfb4165583e2
1,C:\Windows\winsxs\amd64_microsoft-windows-wpd-portabledevicesqm_31bf3856ad364e35_6.1.7601.17514_none_b11b7e2cfd8c4d39
1,C:\Windows\winsxs\amd64_microsoft-windows-dfsclient-netapi_31bf3856ad364e35_6.1.7600.16385_none_bc912cf74a28a647
1,C:\Windows\winsxs\amd64_microsoft-windows-ie-sysprep_31bf3856ad364e35_8.0.7600.16385_none_924152af4aaf8557
1,C:\Windows\winsxs\amd64_microsoft-windows-i..er-engine.resources_31bf3856ad364e35_6.1.7601.17514_ja-jp_d4183db432a5f29d
1,C:\Windows\System32\DriverStore\FileRepository\vhdmp.inf_amd64_neutral_c3910bbf4fbccf97
1,C:\Windows\assembly\GAC_MSIL\Microsoft.SqlServer.SqlClrProvider\10.0.0.0__89845dcd8080cc91
1,C:\Program Files\Tanium\Tanium Server\plugins\console\Dashboards
1,C:\Windows\winsxs\x86_microsoft-windows-g..licymaker.resources_31bf3856ad364e35_6.1.7600.16385_en-us_59436eb028717570
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_37\grep\share\locale\pt_BR\LC_MESSAGES
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\Microsoft.SqlServer#\c988156754e88888de422478835f01a8
1,C:\Windows\System32\DriverStore\FileRepository\faxcn002.inf_amd64_neutral_3d392ccc357e04db
1,C:\Windows\winsxs\x86_wcf-system.runtime.serialization_b03f5f7f11d50a3a_6.1.7601.18532_none_db9f3389dd561754
1,C:\Windows\winsxs\amd64_microsoft.windows.s...smart_card_library_31bf3856ad364e35_6.1.7600.16385_none_55f89e9f01688dc0
1,C:\Windows\winsxs\x86_microsoft-windows-wusa.resources_31bf3856ad364e35_6.1.7600.16385_en-us_6a01eebaaaf68204
1,C:\Windows\winsxs\amd64_microsoft-windows-cryptsvc-dll_31bf3856ad364e35_6.1.7601.22322_none_d4a24ea4ca968363
1,C:\Windows\winsxs\x86_microsoft-windows-ncrypt-dll_31bf3856ad364e35_6.1.7601.18606_none_5ff27b1b4fd45533
1,C:\Windows\winsxs\wow64_microsoft-windows-iis-ftpsvc.resources_31bf3856ad364e35_6.1.7600.16385_en-us_d2857e8176c21a5b
1,C:\Windows\Microsoft.NET\assembly\GAC_32\ISymWrapper\v4.0_4.0.0.0__b03f5f7f11d50a3a
1,C:\Windows\winsxs\x86_netfx35linq-vb_compiler_orcas_31bf3856ad364e35_6.1.7601.17514_none_9809be824da2c173
1,C:\Windows\winsxs\amd64_microsoft-windows-winrsplugins.resources_31bf3856ad364e35_6.1.7600.16385_en-us_159345c6da1672e1
1,C:\Windows\System32\DriverStore\FileRepository\mdmelsa.inf_amd64_neutral_374f9d31af832d6b
1,C:\Windows\winsxs\wow64_microsoft-windows-kernel32_31bf3856ad364e35_6.1.7601.17965_none_fc038d48a1736e92
1,C:\Windows\System32\DriverStore\FileRepository\mdmdgitn.inf_amd64_neutral_09132735f1063a47
1,C:\Windows\winsxs\amd64_microsoft-windows-workstationservice_31bf3856ad364e35_6.1.7601.17514_none_2a601d5ced714bb5
1,C:\Users\Jim Olsen\AppData\Roaming\Macromedia
1,C:\Windows\winsxs\amd64_microsoft-windows-f..ruetype-iskoolapota_31bf3856ad364e35_6.1.7600.16385_none_2a668cf479ef0388
1,C:\Windows\winsxs\amd64_prnbr005.inf_31bf3856ad364e35_6.1.7600.16385_none_4b6471420f8b03d9\Amd64
1,C:\Windows\winsxs\x86_microsoft-windows-comdlg32.resources_31bf3856ad364e35_6.1.7601.17514_pt-pt_ef7b9e173a536f62
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.SqlServer.WebServiceTask
1,C:\Windows\winsxs\msil_microsoft.windows.smc_31bf3856ad364e35_6.1.7601.17514_none_ab698c2bf8d20bb5
1,C:\Windows\winsxs\amd64_server-help-h1s.dmi_start.resources_31bf3856ad364e35_6.1.7600.16385_en-us_3fb41a083651d00e
1,C:\Windows\winsxs\amd64_microsoft-windows-w..-installer-provider_31bf3856ad364e35_6.1.7601.17514_none_88af1cb8f0d0a95d
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\Microsoft.SqlServer#\a61d501848683192591feaada27f8d6a
1,C:\Windows\winsxs\amd64_netfx-system.directoryservices.protocols_b03f5f7f11d50a3a_6.1.7600.16385_none_f65534c04a41b956
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_34\sqlite
1,C:\Windows\System32\en-US\Licenses\OEM\ServerForSBSolutions
1,C:\Windows\winsxs\amd64_server-help-chm.uim_psync.resources_31bf3856ad364e35_6.1.7600.16385_en-us_1594fbfb8c92ba76
1,C:\Windows\winsxs\amd64_microsoft.windows.c..-controls.resources_6595b64144ccf1df_5.82.7600.16385_ru-ru_03775985d5a48f63
1,C:\Windows\SoftwareDistribution\Download
1,C:\Windows\winsxs\amd64_microsoft-windows-dhcpserverrolescript_31bf3856ad364e35_6.1.7600.16385_none_1d6f9bab4827506e
1,C:\Windows\winsxs\amd64_microsoft-windows-t..extension.resources_31bf3856ad364e35_6.1.7600.16385_en-us_a2058f1afade009d
1,C:\Windows\winsxs\msil_system.design_b03f5f7f11d50a3a_6.1.7601.22191_none_72e0ff71d9629a76
1,C:\Windows\winsxs\amd64_microsoft-windows-m..ilerepair.resources_31bf3856ad364e35_6.1.7600.16385_en-us_9ed373c17361cf1b
1,C:\Windows\winsxs\amd64_netfx-aspnet_wp_exe_b03f5f7f11d50a3a_6.1.7601.21884_none_3ad156f04e11776c
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9031\grep\share\locale\gl\LC_MESSAGES
1,C:\Windows\winsxs\x86_microsoft-windows-smss.resources_31bf3856ad364e35_6.1.7600.16385_en-us_e4408e86c08891fe
1,C:\Windows\winsxs\amd64_microsoft-windows-dumpata_31bf3856ad364e35_6.1.7600.16385_none_c5330fa587ba01cb
1,C:\Windows\winsxs\wow64_microsoft-windows-iis-httperrorsbinaries_31bf3856ad364e35_6.1.7600.16385_none_645d1c1b24ec87a4
1,C:\Windows\winsxs\amd64_microsoft-windows-kernelbase_31bf3856ad364e35_6.1.7601.22436_none_859e60b5e45fc488
1,C:\Windows\System32\DriverStore\FileRepository\mdmmotou.inf_amd64_neutral_eb1d978f38f35bca
1,C:\Windows\assembly\GAC_MSIL\PresentationBuildTasks
1,C:\Windows\winsxs\x86_microsoft-windows-o..tend-apis.resources_31bf3856ad364e35_6.1.7601.17514_en-us_a1eb9485bb71c8ff
1,C:\Windows\winsxs\x86_microsoft-windows-d..asks-sync.resources_31bf3856ad364e35_6.1.7600.16385_en-us_ebe6abced058440e
1,C:\Windows\winsxs\amd64_microsoft-windows-acledit.resources_31bf3856ad364e35_6.1.7600.16385_en-us_853b0789da5b1e2a
1,C:\Windows\assembly\GAC_MSIL\PresentationUI
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9026\grep\share\locale\sr\LC_MESSAGES
1,C:\Windows\winsxs\x86_microsoft.windows.c..-controls.resources_6595b64144ccf1df_6.0.7600.16385_bg-bg_69bd10c883a3a560
1,C:\Windows\winsxs\amd64_nulhpopr.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_9bbc515b6b831d6c
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.S63fb36fa#
1,C:\Windows\winsxs\amd64_microsoft-windows-directx-directinput_31bf3856ad364e35_6.1.7600.16385_none_798d0be3255fc46e
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.Runtime.InteropServices\v4.0_4.0.0.0__b03f5f7f11d50a3a
1,C:\Windows\winsxs\amd64_prnca00x.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_20983167eda7589c
1,C:\Windows\winsxs\x86_microsoft-windows-a..ce-useractionrecord_31bf3856ad364e35_6.1.7600.16385_none_32c4b0bc55387f75
1,C:\Windows\winsxs\x86_microsoft-windows-u..erservice.resources_31bf3856ad364e35_6.1.7600.16385_en-us_f09dccd4f32812c2
1,C:\Windows\winsxs\amd64_microsoft-windows-e..-enforcement-client_31bf3856ad364e35_6.1.7600.16385_none_3efbe964e010a5aa
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.SqlServer.DTSUtilities\v4.0_11.0.0.0__89845dcd8080cc91
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.S0677a649#\1084b6e3c3f1ca2e0c25c6526e62654c
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.ServiceModel.Activation
1,C:\Windows\winsxs\x86_microsoft-windows-a..managerui.resources_31bf3856ad364e35_6.1.7600.16385_en-us_443db5647679d4a2
1,C:\Windows\winsxs\amd64_microsoft-windows-comctl32-v5.resources_31bf3856ad364e35_6.1.7600.16385_es-es_be8a1256afbafd72
1,C:\Windows\SysWOW64\config\systemprofile\AppData\Local\Microsoft\Windows\History
1,C:\Program Files\Tanium\Tanium Server\CertificateBackup2014-11-17-11-17-33
1,C:\Windows\winsxs\x86_microsoft-windows-l..oundation.resources_31bf3856ad364e35_6.1.7601.17514_en-us_ed0314fe47faf776
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\Microsoft.Build.Uti#\bdd68f916d6b74807e688e18cab5eb12
1,C:\Windows\winsxs\x86_microsoft-windows-t..p-utility.resources_31bf3856ad364e35_6.1.7601.17514_en-us_f6719a27fd39b2db
1,C:\Windows\winsxs\amd64_microsoft-windows-i..onal-codepage-20005_31bf3856ad364e35_6.1.7600.16385_none_ad62bf63006659ce
1,C:\Windows\Boot\EFI
1,C:\Windows\SoftwareDistribution
1,C:\Windows\winsxs\amd64_microsoft-windows-smss_31bf3856ad364e35_6.1.7601.18113_none_0a5f8ec22fd235a9
1,C:\Users\Jim Olsen\AppData\LocalLow\Microsoft\Windows\AppCache
1,C:\Windows\winsxs\x86_microsoft-windows-i..er-engine.resources_31bf3856ad364e35_6.1.7601.17514_en-us_492959f9bd028207
1,C:\Windows\winsxs\x86_microsoft.grouppoli..t.interop.resources_31bf3856ad364e35_6.1.7601.17514_en-us_864e7d76ac8023f8
1,C:\Windows\winsxs\wow64_microsoft-windows-ieframe_31bf3856ad364e35_11.2.9600.17358_none_515bfcaff7832a25
1,C:\Windows\winsxs\wow64_microsoft-windows-w..lient-aux.resources_31bf3856ad364e35_7.5.7601.17514_en-us_292a8b37a9ef3b8c
1,C:\Windows\winsxs\amd64_microsoft-windows-lmhsvc_31bf3856ad364e35_6.1.7601.17514_none_b0e6edd606f5c524
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.SqlServer.FileSystemTask
1,C:\Windows\System32\DriverStore\FileRepository\netw5v64.inf_amd64_neutral_a6b778ba802632cc
1,C:\Windows\winsxs\amd64_microsoft-windows-fax-service_31bf3856ad364e35_6.1.7601.17514_none_0b499f2c96e8f6b2
1,C:\Windows\winsxs\amd64_policy.1.2.microsof..op.security.azroles_31bf3856ad364e35_6.1.7600.16385_none_48aef4ef4511d002
1,C:\Windows\winsxs\amd64_microsoft-windows-n..entclient.resources_31bf3856ad364e35_6.1.7600.16385_en-us_556b4448d5492f53
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9039\grep\share\locale\ko\LC_MESSAGES
1,C:\Windows\winsxs\x86_microsoft-windows-s..iprovider.resources_31bf3856ad364e35_6.1.7600.16385_en-us_d661f15bff622f11
1,C:\Windows\assembly\GAC\Microsoft.VisualStudio.TextManager.Interop.8.0\8.0.0.0__b03f5f7f11d50a3a
1,C:\Windows\winsxs\amd64_microsoft-windows-help-efs.resources_31bf3856ad364e35_6.1.7600.16385_en-us_7b42dfac415afe76
1,C:\Windows\winsxs\amd64_server-help-chm.cluadmin.resources_31bf3856ad364e35_6.1.7600.16385_en-us_c295debf1a270b88
1,C:\Windows\winsxs\msil_microsoft.storage.sancommon.ui_31bf3856ad364e35_6.1.7600.16385_none_ae1ac5ca1447e687
1,C:\Windows\assembly\GAC_MSIL\Microsoft.ReportViewer.WebForms.resources\11.0.0.0_ru_89845dcd8080cc91
1,C:\Windows\winsxs\x86_microsoft-windows-l..nterprise.resources_31bf3856ad364e35_6.1.7600.16385_en-us_2519d7bb63a0a215
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.ServiceModel.Discovery
1,C:\Windows\winsxs\amd64_microsoft-windows-i..l-keyboard-0000046d_31bf3856ad364e35_6.1.7601.22739_none_5c7e78b78577319d
1,C:\Windows\winsxs\amd64_prnle003.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_e295a15dbf1fb4e2
1,C:\Windows\winsxs\amd64_microsoft-windows-msauditevtlog_31bf3856ad364e35_6.1.7601.22814_none_25f2098ca82ab2b6
1,C:\Windows\winsxs\amd64_microsoft-windows-directory-services-sam_31bf3856ad364e35_6.1.7601.17514_none_10145eccb79418a5
1,C:\Windows\winsxs\amd64_prnrc004.inf_31bf3856ad364e35_6.1.7600.16385_none_21e7809d8e910def
1,C:\Windows\SysWOW64\en-US\Licenses\eval\ServerWinFoundation
1,C:\Windows\winsxs\amd64_microsoft-windows-t..rvices-rdp-direct3d_31bf3856ad364e35_6.1.7601.17514_none_ce0cf746a97a2699
1,C:\Windows\winsxs\amd64_netfx-microsoft.build.framework_b03f5f7f11d50a3a_6.1.7601.17514_none_4c9eab58e2f91183
1,C:\Windows\assembly\GAC_MSIL\Microsoft.Vsa.Vb.CodeDOMProcessor
1,C:\Windows\winsxs\amd64_microsoft-windows-snmp-evntcmd_31bf3856ad364e35_6.1.7600.16385_none_14f9b9481db6293b
1,C:\Windows\winsxs\amd64_microsoft-windows-crypt32-dll_31bf3856ad364e35_6.1.7601.18205_none_b9a17b06f46a70ad
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9032\grep\share\locale\cs\LC_MESSAGES
1,C:\Windows\winsxs\x86_microsoft-windows-services-svchost_31bf3856ad364e35_6.1.7600.16385_none_b591afc466a15356
1,C:\Windows\winsxs\amd64_microsoft-windows-crypt32-dll_31bf3856ad364e35_6.1.7601.22736_none_ba0baff00d9f723d
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.V44fb6cc1#\c22a9c70fab67e42ae3261bb7f4f161a
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\Microsoft.Security.#
1,C:\Windows\winsxs\amd64_microsoft-windows-i..nternetcontrolpanel_31bf3856ad364e35_8.0.7601.17514_none_0819f2b6df7a1335
1,C:\Windows\assembly\GAC_64\PresentationCore
1,C:\Windows\winsxs\amd64_microsoft-windows-c..ityclient.resources_31bf3856ad364e35_6.1.7601.22705_en-us_c37ab478cf88f76c
1,C:\Windows\winsxs\amd64_microsoft-windows-t..appserver-licensing_31bf3856ad364e35_6.1.7601.22843_none_05443aa46b33e0f6
1,C:\Windows\winsxs\wow64_microsoft-windows-linkinfo_31bf3856ad364e35_6.1.7600.16385_none_9eaece15f365da54
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\UIAutomationProvider\v4.0_4.0.0.0__31bf3856ad364e35
1,C:\Windows\winsxs\amd64_microsoft-windows-help-medexp.resources_31bf3856ad364e35_6.1.7600.16385_en-us_befb9293a1b699ff
1,C:\Windows\winsxs\amd64_wcf-infocardcpl_cpl_31bf3856ad364e35_6.1.7600.16385_none_f578352b168f8a4a
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9029\grep\share\locale\ru\LC_MESSAGES
1,C:\Windows\winsxs\wow64_microsoft-windows-rpc-local_31bf3856ad364e35_6.1.7601.17514_none_1c754ed890149b9b
1,C:\Windows\winsxs\x86_microsoft-windows-s..s-svchost.resources_31bf3856ad364e35_6.1.7600.16385_en-us_511f46fd08cd38e1
1,C:\Windows\winsxs\amd64_microsoft-windows-n..formance_monitoring_31bf3856ad364e35_6.1.7600.16385_none_56431363e2cb6652
1,C:\Windows\winsxs\amd64_microsoft-windows-s..-downlevel.binaries_31bf3856ad364e35_6.3.9600.17280_none_5f668c1aff756211
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9024
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9025
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9026
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9027
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9028
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9029
1,C:\Windows\winsxs\wow64_microsoft-windows-b..ions-upload-manager_31bf3856ad364e35_6.1.7600.16385_none_55c5e6b6f1327ce8
1,C:\Windows\winsxs\amd64_microsoft-windows-l..priseia64.resources_31bf3856ad364e35_6.1.7601.17514_en-us_efc948f916800d2c
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9033
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9032
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9031
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9035
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9039
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9038
1,C:\Windows\winsxs\x86_microsoft-windows-m..ss-components-jetes_31bf3856ad364e35_6.1.7600.16385_none_36886cdd2e3bf7e4
1,C:\Windows\winsxs\amd64_microsoft-windows-performancetoolsgui_31bf3856ad364e35_6.1.7601.17514_none_fa2fc39ab7937a51
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9069
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9065
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9066
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9067
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9062
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9063
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9076
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9075
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9074
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9073
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9072
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9071
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9070
1,C:\Program Files (x86)\Microsoft Visual Studio 10.0\Common7\IDE\CommonExtensions\Microsoft\VB\LanguageService\10.0
1,C:\Windows\winsxs\amd64_microsoft-windows-scripting-jscript_31bf3856ad364e35_8.0.7601.17866_none_fb8c2be784ec8fa3
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.Sdc7a71f3#\14662593f5706e2a4e0656c44910b5a7
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9042
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9041
1,C:\Users\Jim Olsen\Documents\SQL Server Management Studio\Templates\ItemTemplates
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.Windows.Controls.Ribbon\v4.0_4.0.0.0__b77a5c561934e089
1,C:\Windows\winsxs\x86_microsoft-windows-m..do-backcompat-tlb20_31bf3856ad364e35_6.1.7601.17514_none_ed1e95de5057e009
1,C:\Windows\winsxs\x86_wcf-m_svc_mod_end_perf_vrg_31bf3856ad364e35_6.1.7600.16385_none_cc6e74aeed7ec870
1,C:\Windows\winsxs\msil_dfsmgmt_31bf3856ad364e35_6.1.7601.21844_none_90f2cf948a12956a
1,C:\Program Files (x86)\Microsoft SQL Server\110\DAC\bin\1033
1,C:\Windows\winsxs\x86_microsoft-windows-e..yphenation.binaries_31bf3856ad364e35_6.3.9600.16428_none_eb9b0f6fb3a13f1e
1,C:\Windows\winsxs\amd64_microsoft-windows-ncrypt-dll_31bf3856ad364e35_6.1.7601.22099_none_bc3c57b22195c1a0
1,C:\Windows\winsxs\amd64_server-help-h1s.tpmadmin.resources_31bf3856ad364e35_6.1.7600.16385_en-us_8224af4d6f3430df
1,C:\Windows\winsxs\amd64_microsoft-windows-t..r-tlntsvr.resources_31bf3856ad364e35_6.1.7600.16385_en-us_ae3d0be2b1c4024c
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_23\grep\share\locale\id\LC_MESSAGES
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_48\grep\share\locale\sl\LC_MESSAGES
1,C:\Windows\winsxs\x86_microsoft-windows-diantz_31bf3856ad364e35_6.1.7600.16385_none_a69c6a8f23f521f3
1,C:\Windows\winsxs\amd64_microsoft-windows-ie-behaviors.resources_31bf3856ad364e35_11.2.9600.16428_en-us_09ce26d2c0c6976f
1,C:\Windows\assembly\NativeImages_v4.0.30319_64\System.Xaml.Hosting
1,C:\Windows\winsxs\amd64_microsoft-windows-font-bitmap-fixed_31bf3856ad364e35_6.1.7600.16385_none_db04d3f548508fd9
1,C:\Windows\winsxs\wow64_microsoft-windows-audio-audiocore_31bf3856ad364e35_6.1.7601.18619_none_df1f60782f9ba191
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\PresentationFramework.Aero\v4.0_4.0.0.0__31bf3856ad364e35
1,C:\Windows\winsxs\amd64_microsoft-windows-b..vironment-os-loader_31bf3856ad364e35_6.1.7601.22780_none_b98696ee9ca07f56
1,C:\Windows\System32\DriverStore\FileRepository\netathrx.inf_amd64_neutral_905772087ff288af
1,C:\Windows\assembly\NativeImages_v4.0.30319_64\System.Runt93d54979#
1,C:\Windows\winsxs\x86_microsoft-windows-qedit.resources_31bf3856ad364e35_6.1.7600.16385_en-us_1c748d197640a543
1,C:\Windows\winsxs\amd64_microsoft-windows-p..unterinfrastructure_31bf3856ad364e35_6.1.7600.16385_none_cd7aeeff1897d018
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9042\grep\share\locale\sv\LC_MESSAGES
1,C:\Windows\winsxs\amd64_mdmcxpv6.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_d07101ecaa44c4af
1,C:\Windows\winsxs\amd64_microsoft-windows-f..type-leelawadeebold_31bf3856ad364e35_6.1.7600.16385_none_4b86f8e6a3279ad0
1,C:\Windows\winsxs\amd64_microsoft-windows-font-truetype-batang_31bf3856ad364e35_6.1.7600.16385_none_13de7dc07ffbe591
1,C:\Windows\winsxs\amd64_microsoft-windows-f..etype-timesnewroman_31bf3856ad364e35_6.1.7601.17514_none_3b958c66aff6cdb7
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\DTSInstall\2f59443741e5c4caa4994e63993688d3
1,C:\Windows\Help\Windows\en-US
1,C:\Windows\winsxs\amd64_microsoft-windows-i..onal-codepage-28592_31bf3856ad364e35_6.1.7600.16385_none_b188802cfdb67997
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9028\grep\share\locale\el\LC_MESSAGES
1,C:\Windows\winsxs\amd64_netr28x.inf_31bf3856ad364e35_6.1.7600.16385_none_f6bd180f0177aea7
1,C:\Program Files\Common Files\SpeechEngines\Microsoft
1,C:\Windows\winsxs\x86_microsoft-windows-fmifs_31bf3856ad364e35_6.1.7600.16385_none_56e4c7a892eacb36
1,C:\ProgramData\Microsoft\Windows\Ringtones
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.Se29577f5#
1,C:\Windows\winsxs\amd64_microsoft-windows-s..iprovider.resources_31bf3856ad364e35_6.1.7600.16385_en-us_9f12d80e121cae5a
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\Accessibility\0483c93466914f3fbd5b44454b0c8a98
1,C:\Windows\winsxs\x86_microsoft-windows-servicingstack_31bf3856ad364e35_6.1.7600.16385_none_0935b76c289e0fd5
1,C:\Windows\winsxs\amd64_microsoft-windows-servicingstack_31bf3856ad364e35_6.1.7601.17514_none_678566b7ddea04a5
1,C:\Windows\System32\DriverStore\FileRepository\prnsa002.inf_amd64_neutral_d9df1d04d8cbe336
1,C:\Windows\SoftwareDistribution\SelfUpdate\Handler
1,C:\Windows\winsxs\x86_netfx-mscorwks_dll_b03f5f7f11d50a3a_6.1.7601.17514_none_06b9b03ceb862f7d
1,C:\Windows\ServiceProfiles\LocalService\AppData\Roaming\Microsoft\Network\Connections
1,C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9026\grep\share\locale\gl\LC_MESSAGES
1,C:\Windows\winsxs\amd64_microsoft-windows-d..fontcache.resources_31bf3856ad364e35_7.1.7601.16492_cs-cz_dcc5802a4c09b643
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.VisualStudio.Language.CallHierarchy\v4.0_10.0.0.0__b03f5f7f11d50a3a
1,C:\Windows\winsxs\amd64_server-help-chm.uim_snis.resources_31bf3856ad364e35_6.1.7600.16385_en-us_46b28c625df92198
1,C:\Windows\winsxs\amd64_microsoft-windows-ntdll_31bf3856ad364e35_6.1.7601.18247_none_b6df585112e2f85b
1,C:\Windows\winsxs\msil_blbmmc_31bf3856ad364e35_6.1.7600.16385_none_1e0d17ddf7df43c4
1,C:\Windows\winsxs\amd64_microsoft-windows-terminalservices-rdpdr_31bf3856ad364e35_6.1.7601.17514_none_5f60151d5fa6ce24
1,C:\Windows\winsxs\amd64_microsoft-windows-storport_31bf3856ad364e35_6.1.7601.18386_none_85588aa4470585ac
1,C:\Windows\winsxs\msil_napsnap_31bf3856ad364e35_6.1.7600.16385_none_0c6dbb690a333628
1,C:\Windows\assembly\NativeImages_v4.0.30319_64\Microsoft.Sfab66633#
1,C:\Windows\assembly\GAC_64\Microsoft.Security.ApplicationId.PolicyManagement.PolicyEngineApi.Interop\6.1.0.0__31bf3856ad364e35
1,C:\Windows\winsxs\amd64_wpf-presentationhostdll_31bf3856ad364e35_6.1.7601.17514_none_ce3172a8369ec608
1,C:\Windows\Microsoft.NET\Framework\v2.0.50727\ASP.NETWebAdminFiles\Security\Users
1,C:\Windows\winsxs\x86_microsoft.windows.c..-controls.resources_6595b64144ccf1df_5.82.7600.16385_sl-si_e951b6c1dfd4bd76
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9035\grep\share\locale\zh_TW
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_63\grep\share\locale\hu\LC_MESSAGES
1,C:\Windows\assembly\NativeImages_v2.0.50727_64\Narrator
1,C:\Windows\assembly\GAC_MSIL\Microsoft.PowerShell.ConsoleHost\1.0.0.0__31bf3856ad364e35
1,C:\Windows\System32\DriverStore\FileRepository\clusdisk.inf_amd64_neutral_517fb8e5b41452c5
1,C:\Windows\winsxs\x86_microsoft-windows-a..tigations.resources_31bf3856ad364e35_6.1.7601.22248_zh-hk_7a625d3eef48924c
1,C:\Program Files (x86)\Microsoft Visual Studio 10.0\Web\Snippets\HTML\1033
1,C:\Windows\winsxs\amd64_microsoft-windows-s..-vbscript.resources_31bf3856ad364e35_6.1.7600.16385_en-us_6bd0dc3389c765b1
1,C:\Windows\winsxs\amd64_microsoft-windows-t..torclient.resources_31bf3856ad364e35_7.1.7601.16398_en-us_8de2d8fedf1df9ff
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\EnvDTE90\d45d934fb4f734451fae61288d59ee9b
1,C:\Windows\winsxs\amd64_microsoft-windows-oleaccrc.resources_31bf3856ad364e35_6.1.7600.16385_en-us_5c4db2c1103b4a92
1,C:\Windows\winsxs\amd64_microsoft-windows-t..es-commandlinetools_31bf3856ad364e35_6.1.7601.17514_none_42d65ed50fa3c682
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.ServiceModel.Primitives
1,C:\Windows\winsxs\amd64_microsoft-windows-p..ll-events.resources_31bf3856ad364e35_6.1.7600.16385_en-us_3eddeca774028e07
1,C:\Windows\winsxs\x86_caspol_b03f5f7f11d50a3a_6.1.7601.22733_none_29677a47c628119e
1,C:\Windows\winsxs\amd64_tsusbhubfilter.inf_31bf3856ad364e35_6.1.7601.17514_none_776b19f55ac34470
1,C:\Windows\winsxs\amd64_microsoft-windows-g..rveradmintools-gpmc_31bf3856ad364e35_6.1.7601.17514_none_1458f05bc75eb3f4
1,C:\Program Files\Tanium\Tanium Server\ApacheBackup2014-09-16-20-44-23\modules
1,C:\Windows\winsxs\amd64_prnrc006.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_39360e96965fde25
1,C:\Windows\winsxs\amd64_microsoft-windows-a..mecontrol.resources_31bf3856ad364e35_6.1.7600.16385_en-us_392ce9a7ba4fe7e8
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9028\grep\share\locale\pt_BR\LC_MESSAGES
1,C:\Windows\winsxs\x86_microsoft-windows-c..us-runtime-stclient_31bf3856ad364e35_6.1.7600.16385_none_a9649d04c661942c
1,C:\Windows\winsxs\wow64_microsoft-windows-ie-htmlapplication_31bf3856ad364e35_8.0.7601.22777_none_dcda8f78e4ab7dd6
1,C:\Windows\winsxs\amd64_microsoft-windows-wmilib_31bf3856ad364e35_6.1.7600.16385_none_b549ebfe1dddb7f1
1,C:\Windows\winsxs\amd64_microsoft-windows-s..packerror.resources_31bf3856ad364e35_6.1.7600.16385_en-us_d2f18e90bddce0c2
1,C:\Windows\winsxs\amd64_microsoft-windows-p..track-adm.resources_31bf3856ad364e35_6.1.7600.16385_en-us_c13d58e431d898bb
1,C:\Windows\winsxs\amd64_prnca00h.inf_31bf3856ad364e35_6.1.7600.16385_none_e0755475742561ac
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9035\yara
1,C:\Windows\winsxs\amd64_microsoft-windows-winsrv-adm.resources_31bf3856ad364e35_6.1.7600.16385_en-us_c01e7ca36d3191ee
1,C:\Windows\winsxs\x86_microsoft-windows-m..al-backcompat-tlb28_31bf3856ad364e35_6.1.7601.22012_none_ac6ebffcc80ba2a2
1,C:\Windows\winsxs\amd64_microsoft-windows-c..dtc-runtime-cluster_31bf3856ad364e35_6.1.7601.17514_none_f4ae54a1a351cc34
1,C:\Windows\winsxs\amd64_microsoft-windows-p..randprintui-asyncui_31bf3856ad364e35_6.1.7600.16385_none_d7d643c30bd72bf4
1,C:\Windows\winsxs\amd64_microsoft-windows-i..tional-codepage-949_31bf3856ad364e35_6.1.7600.16385_none_2ad09128b4ec905d
1,C:\Windows\winsxs\amd64_microsoft-windows-m..do-backcompat-tlb28_31bf3856ad364e35_6.1.7601.17857_none_48be78e20913e405
1,C:\Windows\assembly\NativeImages_v4.0.30319_64\System.Activities
1,C:\Windows\winsxs\amd64_microsoft-windows-scripting-vbscript_31bf3856ad364e35_11.2.9600.17280_none_2acd701742dec536
1,C:\Windows\winsxs\amd64_microsoft-windows-videoport_31bf3856ad364e35_6.1.7600.16385_none_180f3dba1e158073
1,C:\Windows\winsxs\amd64_microsoft-windows-d..andlinepropertytool_31bf3856ad364e35_6.1.7601.17514_none_696354579779eadf
1,C:\Windows\winsxs\amd64_microsoft-windows-n..-domain-clients-svc_31bf3856ad364e35_6.1.7601.17514_none_a2347d4102a4c8ad
1,C:\Windows\winsxs\wow64_microsoft-windows-ie-datacontrol_31bf3856ad364e35_11.2.9600.16428_none_00b2e64ae9989845
1,C:\Windows\assembly\GAC_MSIL\Microsoft.SqlServer.Management.SqlParser\11.0.0.0__89845dcd8080cc91
1,C:\Windows\winsxs\amd64_microsoft-windows-wmi-core-svc_31bf3856ad364e35_6.1.7601.17514_none_fed8c13f0d90a8cf
1,C:\Windows\System32\DriverStore\FileRepository\prnbr004.inf_amd64_neutral_a78e168d6944619a
1,C:\Windows\winsxs\amd64_microsoft-windows-e..rformancemonitoring_31bf3856ad364e35_6.1.7600.16385_none_0d7e44ffcdcf5676
1,C:\Program Files\Common Files\Microsoft Shared\ink\ru-RU
1,C:\Windows\SysWOW64\IME\imekr8\dicts
1,C:\Windows\winsxs\x86_microsoft-windows-s..-binaries.resources_31bf3856ad364e35_6.1.7601.17514_ja-jp_8602279f8341f235
1,C:\Windows\winsxs\x86_microsoft-windows-tapi2xclient.resources_31bf3856ad364e35_6.1.7600.16385_en-us_e8e4d27156d257c9
1,C:\Windows\winsxs\amd64_wpf-presentationhostdll_31bf3856ad364e35_6.1.7601.17755_none_ce07370e36be4971
1,C:\Windows\winsxs\msil_system.messaging_b03f5f7f11d50a3a_6.1.7601.18523_none_020fbc17e044566c
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_53\grep\share\locale\sr\LC_MESSAGES
1,C:\Users\MSSQL$SQLEXPRESS\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch
1,C:\Windows\winsxs\amd64_microsoft-windows-tabletpc-uihub_31bf3856ad364e35_6.1.7600.16385_none_6f7e04cab5e74750
1,C:\Program Files\Microsoft SQL Server\110\DTS\ForEachEnumerators\en
1,C:\Windows\winsxs\amd64_microsoft-windows-msf.resources_31bf3856ad364e35_6.1.7601.17514_en-us_810c155fd815ebfc
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\Microsoft.GroupPoli#\fb058c5e3b9d3af4bfa69811b3a498c1
1,C:\Windows\SysWOW64\en-US\Licenses\_Default\ServerMediumBusinessSecurity
1,C:\Windows\winsxs\wow64_microsoft-windows-mfmjpegdec_31bf3856ad364e35_6.1.7600.16385_none_7fa793baa201214e
1,C:\Windows\winsxs\amd64_microsoft-windows-i..riptedsandboxplugin_31bf3856ad364e35_11.2.9600.17420_none_3e33a8dd806ae83c
1,C:\Windows\winsxs\x86_microsoft-windows-m..ac-sql-cliconfg-rll_31bf3856ad364e35_6.1.7600.16385_none_6a546f37bbab5475
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_21\grep\share\locale\lt\LC_MESSAGES
1,C:\Program Files (x86)\Tanium\Tanium Client\Tools\StdUtils\grep\share\locale\zh_TW
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_64\grep\share\locale\pt_BR\LC_MESSAGES
1,C:\Windows\winsxs\amd64_microsoft-windows-s..y-spp-wmi.resources_31bf3856ad364e35_6.1.7600.16385_en-us_4185c7bb7887e34e
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_34\hash
1,C:\Windows\winsxs\amd64_microsoft-windows-d..s-ime-japanese-core_31bf3856ad364e35_6.1.7601.18556_none_cd680cfea4662663
1,C:\Windows\winsxs\amd64_microsoft-windows-p..rtmonitor.resources_31bf3856ad364e35_6.1.7600.16385_en-us_a317442b915afa21
1,C:\Program Files (x86)\Common Files\microsoft shared\MSEnv\1033
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Presentatio84a6349c#\63e9d81bd805aea8f8690fee2efc9a9e
1,C:\Windows\winsxs\x86_microsoft-windows-m..do-backcompat-tlb25_31bf3856ad364e35_6.1.7601.17514_none_ece8864250806bbe
1,C:\Windows\winsxs\amd64_microsoft-windows-help-adm_31bf3856ad364e35_6.1.7600.16385_none_893d90cda53294d1
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\StorageMgmt
1,C:\Windows\winsxs\amd64_microsoft-windows-ie-memoryanalyzer_31bf3856ad364e35_11.2.9600.17420_none_a54ee356089ed8d3
1,C:\Windows\winsxs\amd64_microsoft-windows-gc-usbforcereboot_31bf3856ad364e35_6.1.7601.18328_none_92f16c0a70dcfacc
1,C:\Windows\winsxs\x86_microsoft-windows-f..temcompareutilities_31bf3856ad364e35_6.1.7600.16385_none_009cfaa696afe78b
1,C:\Windows\winsxs\amd64_microsoft.vc80.mfc_1fc8b3b9a1e18e3b_8.0.50727.1833_none_8442d417329336b1
1,C:\Windows\winsxs\amd64_microsoft-windows-ie-antiphishfilter_31bf3856ad364e35_11.2.9600.17420_none_dde9e18b80cbedfe
1,C:\Windows\winsxs\amd64_prnkm004.inf_31bf3856ad364e35_6.1.7600.16385_none_50ff82015b97b704
1,C:\Windows\winsxs\wow64_microsoft-windows-msxml60_31bf3856ad364e35_6.1.7601.17514_none_f0e8ac03e1d6bb5b
1,C:\Windows\winsxs\amd64_prnep00b.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_6cfd9c5115587d13
1,C:\Windows\Migration\WTR
1,C:\Windows\winsxs\amd64_microsoft.windows.c..-controls.resources_6595b64144ccf1df_5.82.7600.16385_ro-ro_010f0df9d729cc93
1,C:\Windows\winsxs\amd64_microsoft-windows-installer-engine_31bf3856ad364e35_6.1.7601.18604_none_61ab3ea4ca1c4419
1,C:\Windows\winsxs\amd64_microsoft-windows-u..assdriver.resources_31bf3856ad364e35_6.1.7600.16385_en-us_e5eb83baa658d423
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.SqlServer.FTPTaskUI
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.IdentityModel.Services\v4.0_4.0.0.0__b77a5c561934e089
1,C:\Users\All Users\Microsoft\Windows\Sqm\Sessions
1,C:\Windows\winsxs\x86_microsoft-windows-p..topeercollab-client_31bf3856ad364e35_6.1.7600.16385_none_9d0ba9d0ec2082dd
1,C:\Windows\winsxs\x86_microsoft-windows-nddeapi.resources_31bf3856ad364e35_6.1.7600.16385_en-us_de6a8036f7c9134b
1,C:\Windows\System32\ko-KR
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9027\grep\share\locale
1,C:\Windows\winsxs\x86_microsoft-windows-authentication-authui_31bf3856ad364e35_6.1.7601.18276_none_0dbbeb9453d8f782
1,C:\Windows\winsxs\x86_netfx-mscorsn_dll_b03f5f7f11d50a3a_6.1.7600.16385_none_6adff9151d65c2d5
1,C:\Windows\winsxs\amd64_microsoft-windows-e..yphenation.binaries_31bf3856ad364e35_6.3.9600.16428_none_47b9aaf36bfeb054
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_47\grep\share\locale\hu\LC_MESSAGES
1,C:\Windows\winsxs\amd64_microsoft-windows-help-netwl.resources_31bf3856ad364e35_6.1.7600.16385_en-us_6d1db8e7c7a5a558
1,C:\Windows\winsxs\amd64_microsoft-windows-i..eyboard-korean_101c_31bf3856ad364e35_6.1.7600.16385_none_e1bb6033344e9a8a
1,C:\Windows\winsxs\amd64_microsoft-windows-t..languages.resources_31bf3856ad364e35_6.1.7601.17514_it-it_9dadd996d9880aa1
1,C:\Windows\winsxs\x86_microsoft-windows-comdlg32.resources_31bf3856ad364e35_6.1.7601.17514_sl-si_d44bd64014e9029b
1,C:\Windows\winsxs\wow64_microsoft-windows-powershell-sip_31bf3856ad364e35_6.1.7600.16385_none_ceb83cd750c49126
1,C:\Windows\winsxs\x86_netfx35linq-framework_assemblylist_31bf3856ad364e35_6.1.7600.16385_none_d2345696aab11309
1,C:\Windows\assembly\GAC_MSIL\Microsoft.VisualBasic
1,C:\Program Files (x86)\Tanium\Tanium Client\Tools\StdUtils\grep\share\locale\vi\LC_MESSAGES
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9029\grep\manifest
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\SQLEditors\5923730fbc3770c5d8c2dda267336f97
1,C:\Windows\winsxs\amd64_wcf-m_tx_bridge_perf_c_vrg_31bf3856ad364e35_6.1.7600.16385_none_de4eced846c25e95
1,C:\Windows\winsxs\amd64_microsoft-windows-i..osticstap.resources_31bf3856ad364e35_11.2.9600.17041_en-us_6d7f2f07f9bd6ab2
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\Microsoft.Exception#
1,C:\Windows\winsxs\amd64_microsoft-windows-cdosys_31bf3856ad364e35_6.1.7601.22012_none_7cf37f9a55237f75
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.V016a48a9#\dca518bff4a7b719811ff4404a5f9a66
1,C:\Windows\winsxs\x86_microsoft-windows-iscsi_initiator_ui_31bf3856ad364e35_6.1.7600.16385_none_d7c180d4bd657495
1,C:\Windows\winsxs\wow64_microsoft-windows-p..st-common.resources_31bf3856ad364e35_6.1.7600.16385_en-us_d0db429429b01e85
1,C:\Windows\assembly\GAC_32\Microsoft.Interop.Security.AzRoles\2.0.0.0__31bf3856ad364e35
1,C:\inetpub
1,C:\Windows\assembly\GAC_32\Microsoft.Security.ApplicationId.PolicyManagement.PolicyEngineApi.Interop\6.1.0.0__31bf3856ad364e35
1,C:\Windows\System32\DriverStore\FileRepository\ehstorcertdrv.inf_amd64_neutral_2e1cecffae9c899a
1,C:\Windows\winsxs\amd64_microsoft-windows-webio_31bf3856ad364e35_6.1.7601.21861_none_bb60cfaa0e9b9e85
1,C:\Windows\assembly\NativeImages_v4.0.30319_64\WindowsForm0b574481#\2834e3e61ca12bfe75e0db1ab843f0d3
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_51\grep\share\locale\tr\LC_MESSAGES
1,C:\Windows\winsxs\msil_microsoft.windows.s..downlevel.resources_31bf3856ad364e35_6.1.7600.16385_en-us_a0646737018f58e9
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9032\grep\share\locale\ky\LC_MESSAGES
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\DBMaintenanceProper#
1,C:\Windows\winsxs\amd64_microsoft-windows-i..tional-codepage-855_31bf3856ad364e35_6.1.7600.16385_none_2adcbc7eb4e3273f
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.SqlServer.ForEachSMOEnumerator
1,C:\Windows\Resources\Themes\aero\en-US
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.VisualStudio.Language.CallHierarchy.Implementation\v4.0_10.0.0.0__b03f5f7f11d50a3a
1,C:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\Tools\VDT
1,C:\Windows\winsxs\amd64_microsoft-windows-f..client-applications_31bf3856ad364e35_6.1.7601.17514_none_d71fb1d63f05ef22
1,C:\Windows\winsxs\x86_microsoft-windows-directwrite.resources_31bf3856ad364e35_7.1.7601.16492_en-us_84a1c2c3b7a81cf3
1,C:\Windows\winsxs\amd64_ql2300.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_5504a7062024cd6a
1,C:\Windows\Boot\PCAT\tr-TR
1,C:\Windows\winsxs\x86_microsoft-windows-rasapi.resources_31bf3856ad364e35_6.1.7600.16385_en-us_5ca843a91ebaba76
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.Sbc3e7d8b#\1db0016f8610618627a09787dfeadfac
1,C:\Windows\winsxs\wow64_microsoft-windows-scripting-jscript9_31bf3856ad364e35_11.2.9600.17041_none_31032bb206fd7701
1,C:\Windows\winsxs\x86_netfx-dw_b03f5f7f11d50a3a_6.1.7600.16385_none_a223bd3dd785391a
1,C:\Windows\winsxs\amd64_microsoft-windows-ntshrui.resources_31bf3856ad364e35_6.1.7600.16385_en-us_544475ff2d69ee9f
1,C:\Windows\winsxs\x86_microsoft-windows-m..ents-mdac-ado15-dll_31bf3856ad364e35_6.1.7601.22012_none_0ebfc67ce80861b4
1,C:\Windows\winsxs\msil_system.design_b03f5f7f11d50a3a_6.1.7601.18027_none_89a71b7bbfc222d5
1,C:\Windows\winsxs\x86_microsoft.windows.c..-controls.resources_6595b64144ccf1df_5.82.7600.16385_ar-sa_6d63d528d41932e2
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\Microsoft.SqlServer#\6757f938c588faa0c4adadaf13e99d82
1,C:\Windows\winsxs\msil_microsoft.web.manag..davclient.resources_31bf3856ad364e35_6.1.7600.16385_en-us_acee5ff0a4855329
1,C:\Windows\winsxs\x86_microsoft-windows-ie-ieproxy_31bf3856ad364e35_11.2.9600.17280_none_1683b5a3a72aed1c
1,C:\Windows\winsxs\x86_microsoft-windows-t..s-clientactivexcore_31bf3856ad364e35_6.1.7601.22252_none_3251afcf3d2a516d
1,C:\Windows\winsxs\x86_microsoft-windows-l..anagement.resources_31bf3856ad364e35_6.1.7600.16385_en-us_6c43d2b67bf26136
1,C:\Windows\winsxs\x86_microsoft-windows-m..drivermanager-trace_31bf3856ad364e35_6.1.7601.17514_none_817af6649fbc1ed4
1,C:\Windows\System32\DriverStore\FileRepository\mdmtexas.inf_amd64_neutral_7572473d88d69307
1,C:\Windows\winsxs\amd64_netb57va.inf_31bf3856ad364e35_6.1.7600.16385_none_581eb8ede4375d14
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.V6b191eba#\1a7713f13762d91d7a81ffbcc5af1b91
1,C:\Windows\winsxs\amd64_microsoft-windows-wpfcorecomp.resources_31bf3856ad364e35_6.1.7601.18523_en-us_102e1681a6f8daa0
1,C:\Windows\winsxs\amd64_microsoft-windows-wmi-provider-common_31bf3856ad364e35_6.1.7600.16385_none_0434b662f2d183a0
1,C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Temporary ASP.NET Files
1,C:\Windows\winsxs\x86_microsoft-windows-b..oad-isapi.resources_31bf3856ad364e35_6.1.7600.16385_en-us_5a4b9d403c1122c9
1,C:\Windows\winsxs\amd64_microsoft-windows-csrsrv_31bf3856ad364e35_6.1.7601.22780_none_27e713c1d55740d7
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\Microsoft.SqlServer#\f6d66dfe197ba500d1bfc2ba819d1de1
1,C:\Windows\winsxs\amd64_usbprint.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_754e23e2d81789cd
1,C:\Windows\winsxs\amd64_microsoft-windows-powercpl_31bf3856ad364e35_6.1.7601.17514_none_c006f86a8ad7ce0f
1,C:\Windows\winsxs\x86_system.data.oracleclient_b77a5c561934e089_6.1.7601.22733_none_b0c6aa2ab370fef0
1,C:\Windows\winsxs\amd64_microsoft-windows-i..henticationbinaries_31bf3856ad364e35_6.1.7600.16385_none_39dd2292c22c1d9e
1,C:\Users\Jim Olsen\AppData\Local\Microsoft\Internet Explorer\Recovery
1,C:\ProgramData\Package Cache\{ca67548a-5ebe-413a-b50c-4b9ceb6d66c6}
1,C:\Windows\winsxs\amd64_microsoft-windows-p..ng-server-isolation_31bf3856ad364e35_6.1.7600.16385_none_f8a40495785334a9
1,C:\Windows\winsxs\x86_microsoft-windows-upnpssdp.resources_31bf3856ad364e35_6.1.7600.16385_en-us_9fada492807dfef9
1,C:\Windows\assembly\NativeImages_v2.0.50727_32\Microsoft.SqlServer#\db94f1de3f94749e5e9cbe3eeee67e39
1,C:\Windows\winsxs\x86_microsoft-windows-photoscreensaver_31bf3856ad364e35_6.1.7601.17514_none_6dd5e8c3b6b81894
1,C:\Windows\winsxs\amd64_prnbr007.inf_31bf3856ad364e35_6.1.7600.16385_none_4c7695ac41c77cab\Amd64
1,C:\Windows\winsxs\amd64_microsoft-windows-s..-downlevel.binaries_31bf3856ad364e35_6.3.9600.16428_none_5faf8886ff3d65d0
1,C:\Windows\Boot\PCAT\sv-SE
1,C:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\SqlWorkbenchProjectItems\Sql\Earlier Versions\Create View
1,C:\Windows\Microsoft.NET\assembly\GAC_32\Microsoft.VisualStudio.Modeling.Sdk.Diagrams.GraphObject.10.0\v4.0_10.0.0.0__b03f5f7f11d50a3a
1,C:\Windows\winsxs\amd64_ds-ui-ext.resources_31bf3856ad364e35_6.1.7600.16385_en-us_7a2b039113f0c5bf
1,C:\Windows\Installer\{83F2B8F4-5CF3-4BE9-9772-9543EAE4AC5F}
1,C:\Windows\SysWOW64\NetworkList\Icons\StockIcons
1,C:\Windows\winsxs\amd64_microsoft-windows-com-dtc-runtime-tm_31bf3856ad364e35_6.1.7601.17514_none_f7be9391315f6cc3
1,C:\Windows\winsxs\x86_microsoft-windows-r..-commandline-editor_31bf3856ad364e35_6.1.7600.16385_none_316a8a208c030e56
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_9026\grep\share\locale\ja\LC_MESSAGES
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.Diagnostics.Debug\v4.0_4.0.0.0__b03f5f7f11d50a3a
1,C:\Program Files (x86)\Tanium\Tanium Client\Downloads\Action_46\grep\share\locale\zh_TW\LC_MESSAGES
1,C:\Windows\winsxs\amd64_microsoft-windows-webdavredir-mrxdav_31bf3856ad364e35_6.1.7601.17514_none_72d0eaa6dc5b2edb
1,C:\Windows\winsxs\amd64_tsportalweb_31bf3856ad364e35_6.1.7600.16385_none_9dbdffcbeee4e7d9
1,C:\Windows\assembly\GAC_MSIL\Microsoft.SqlServer.Management.Utility\11.0.0.0__89845dcd8080cc91
1,C:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\SQL\Snippets\1033\User Defined Table Type
1,C:\Windows\winsxs\amd64_netfx-peverify_dll_b03f5f7f11d50a3a_6.1.7601.18523_none_2946b69ff1fd271f
1,C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.VisualStudio.Modeling.Sdk.Integration.Shell.10.0
1,C:\Program Files\Tanium\Tanium Server\Apache24\htdocs\php\Auth
1,C:\Windows\winsxs\amd64_display.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_8bb90e0956a02ab0
1,C:\Windows\assembly\NativeImages_v4.0.30319_32\Microsoft.V4c263b4e#\dcfa989c56af05d940045161f24c45af
1,C:\Windows\winsxs\amd64_wiasa002.inf.resources_31bf3856ad364e35_6.1.7600.16385_en-us_499baeb321ffb611
1,C:\Windows\assembly\NativeImages_v4.0.30319_64\Microsoft.S01b51732#\6ddb0f166671ce822952710f5ca0ed21
1,C:\Windows\winsxs\x86_microsoft-windows-crypt32-dll_31bf3856ad364e35_6.1.7601.22736_none_5ded146c55420107
1,C:\Windows\winsxs\amd64_microsoft-windows-whea-troubleshooter_31bf3856ad364e35_6.1.7600.16385_none_124dff546524b2a8
1,C:\Program Files\MSBuild\Microsoft\Windows Workflow Foundation\v3.0
1,C:\Program Files\MSBuild\Microsoft\Windows Workflow Foundation\v3.5
1,C:\Windows\winsxs\amd64_microsoft-windows-ie-htmlrendering_31bf3856ad364e35_11.2.9600.17280_none_f5b67f6437213d09
1,C:\Windows\winsxs\amd64_prnrc00c.inf_31bf3856ad364e35_6.1.7600.16385_none_3b11d85d2b1e2536\Amd64
1,C:\Windows\winsxs\x86_microsoft-windows-i..emsupport.resources_31bf3856ad364e35_6.1.7600.16385_en-us_ffbf5574b0e45521
1,C:\Windows\winsxs\wow64_microsoft-windows-webio_31bf3856ad364e35_6.1.7601.17725_none_c55b1e0929bab64e
1,Windows Only


'''
