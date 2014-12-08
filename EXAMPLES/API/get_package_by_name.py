
"""
Get a package by name
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
kwargs["objtype"] = u'package'
kwargs["name"] = u'Distribute Patch Tools'

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

Type of response:  <class 'taniumpy.object_types.package_spec_list.PackageSpecList'>

print of response:
PackageSpecList, len: 1

length of response (number of objects returned): 
1

print the first object returned in JSON format:
{
  "_type": "package_spec", 
  "available_time": "2014-12-08T19:25:53", 
  "command": "cmd /c cscript //T:1800 copy-to-tanium-dir.vbs \"Tools\"", 
  "command_timeout": 1800, 
  "creation_time": "2014-12-08T19:21:06", 
  "deleted_flag": 0, 
  "display_name": "Distribute Patch Tools", 
  "expire_seconds": 2400, 
  "files": {
    "_type": "package_files", 
    "file": [
      {
        "_type": "file", 
        "bytes_downloaded": 3041, 
        "bytes_total": 3041, 
        "cache_status": "CACHED", 
        "download_seconds": 0, 
        "download_start_time": "2014-12-08T19:22:51", 
        "hash": "9bcb986d4be0c4f42ab27df25f8604cac85b90e3a95bf016be519805aba79823", 
        "id": 45, 
        "last_download_progress_time": "2014-12-08T19:23:03", 
        "name": "copy-to-tanium-dir.vbs", 
        "size": 3041, 
        "source": "https://content.tanium.com/files/initialcontent/bundles/2014-11-05_12-56-07-8513/distribute_patch_tools/copy-to-tanium-dir.vbs", 
        "status": 200
      }, 
      {
        "_type": "file", 
        "bytes_downloaded": 2224, 
        "bytes_total": 2224, 
        "cache_status": "CACHED", 
        "download_seconds": 0, 
        "download_start_time": "2014-12-08T19:22:51", 
        "hash": "2642ab14c1dc1b55df076a28a4eadaccb3e0cdb4b8810ca7eb6cd3a6d055b99f", 
        "id": 46, 
        "last_download_progress_time": "2014-12-08T19:23:03", 
        "name": "copy-patch-files.vbs", 
        "size": 2224, 
        "source": "https://content.tanium.com/files/initialcontent/bundles/2014-11-05_12-56-07-8513/distribute_patch_tools/copy-patch-files.vbs", 
        "status": 200
      }, 
      {
        "_type": "file", 
        "bytes_downloaded": 2853, 
        "bytes_total": 2853, 
        "cache_status": "CACHED", 
        "download_seconds": 0, 
        "download_start_time": "2014-12-08T19:22:51", 
        "hash": "09cdcde9d227d991da568b27f90395980472c451aa8d2012a01f22dbade76957", 
        "id": 47, 
        "last_download_progress_time": "2014-12-08T19:23:03", 
        "name": "copy-patch-scanner-and-scan.vbs", 
        "size": 2853, 
        "source": "https://content.tanium.com/files/initialcontent/bundles/2014-11-05_12-56-07-8513/distribute_patch_tools/copy-patch-scanner-and-scan.vbs", 
        "status": 200
      }, 
      {
        "_type": "file", 
        "bytes_downloaded": 128080, 
        "bytes_total": 128080, 
        "cache_status": "CACHED", 
        "download_seconds": 0, 
        "download_start_time": "2014-12-08T19:22:51", 
        "hash": "71bb11a395d0f22c975095475567c36ace86973c8b22b69e8f2c615cbd3eb4f4", 
        "id": 48, 
        "last_download_progress_time": "2014-12-08T19:23:03", 
        "name": "install-patches.vbs", 
        "size": 128080, 
        "source": "https://content.tanium.com/files/initialcontent/bundles/2014-11-05_12-56-07-8513/distribute_patch_tools/install-patches.vbs", 
        "status": 200
      }, 
      {
        "_type": "file", 
        "bytes_downloaded": 130098, 
        "bytes_total": 130098, 
        "cache_status": "CACHED", 
        "download_seconds": 0, 
        "download_start_time": "2014-12-08T19:23:03", 
        "hash": "c66d83bcf491e3df2d7a427718b0ec5c4a471b058141a40473ef4df8e6e9ce08", 
        "id": 49, 
        "last_download_progress_time": "2014-12-08T19:23:13", 
        "name": "run-patch-scan.vbs", 
        "size": 130098, 
        "source": "https://content.tanium.com/files/initialcontent/bundles/2014-11-05_12-56-07-8513/distribute_patch_tools/run-patch-scan.vbs", 
        "status": 200
      }, 
      {
        "_type": "file", 
        "bytes_downloaded": 43162, 
        "bytes_total": 43162, 
        "cache_status": "CACHED", 
        "download_seconds": 0, 
        "download_start_time": "2014-12-08T19:23:03", 
        "hash": "9cc2229dfe2da8a1c629d0232af02f18c9a942e880c0332e88ec4b59a4153bb2", 
        "id": 50, 
        "last_download_progress_time": "2014-12-08T19:23:13", 
        "name": "uninstall-patch.vbs", 
        "size": 43162, 
        "source": "https://content.tanium.com/files/initialcontent/bundles/2014-11-05_12-56-07-8513/distribute_patch_tools/uninstall-patch.vbs", 
        "status": 200
      }, 
      {
        "_type": "file", 
        "bytes_downloaded": 2922, 
        "bytes_total": 2922, 
        "cache_status": "CACHED", 
        "download_seconds": 0, 
        "download_start_time": "2014-12-08T19:23:03", 
        "hash": "b72e877348660979b4886576ace522834ed0fa2b8a401b2c5c647b2c475ea67a", 
        "id": 51, 
        "last_download_progress_time": "2014-12-08T19:23:13", 
        "name": "add-patch-exclusion.vbs", 
        "size": 2922, 
        "source": "https://content.tanium.com/files/initialcontent/bundles/2014-11-05_12-56-07-8513/distribute_patch_tools/add-patch-exclusion.vbs", 
        "status": 200
      }, 
      {
        "_type": "file", 
        "bytes_downloaded": 3205, 
        "bytes_total": 3205, 
        "cache_status": "CACHED", 
        "download_seconds": 0, 
        "download_start_time": "2014-12-08T19:23:03", 
        "hash": "6cbce3cc4d3ea581ca3836151612c8e6e0deecfd7d1af7485ce6995fa60827f8", 
        "id": 52, 
        "last_download_progress_time": "2014-12-08T19:23:13", 
        "name": "remove-patch-exclusion.vbs", 
        "size": 3205, 
        "source": "https://content.tanium.com/files/initialcontent/bundles/2014-11-05_12-56-07-8513/distribute_patch_tools/remove-patch-exclusion.vbs", 
        "status": 200
      }, 
      {
        "_type": "file", 
        "bytes_downloaded": 2888, 
        "bytes_total": 2888, 
        "cache_status": "CACHED", 
        "download_seconds": 0, 
        "download_start_time": "2014-12-08T19:23:13", 
        "hash": "c1ba18b6f5bf7754237a5e6b530cf650ad84ab936c1e49e736998e2ed6779d6c", 
        "id": 53, 
        "last_download_progress_time": "2014-12-08T19:23:23", 
        "name": "add-patch-whitelist-entry.vbs", 
        "size": 2888, 
        "source": "https://content.tanium.com/files/initialcontent/bundles/2014-11-05_12-56-07-8513/distribute_patch_tools/add-patch-whitelist-entry.vbs", 
        "status": 200
      }, 
      {
        "_type": "file", 
        "bytes_downloaded": 3171, 
        "bytes_total": 3171, 
        "cache_status": "CACHED", 
        "download_seconds": 0, 
        "download_start_time": "2014-12-08T19:23:13", 
        "hash": "3c86d99f232755ba4a1edcc4782cdd5ea9f637c2873b137931ced9b86c03f77a", 
        "id": 54, 
        "last_download_progress_time": "2014-12-08T19:23:23", 
        "name": "remove-patch-whitelist-entry.vbs", 
        "size": 3171, 
        "source": "https://content.tanium.com/files/initialcontent/bundles/2014-11-05_12-56-07-8513/distribute_patch_tools/remove-patch-whitelist-entry.vbs", 
        "status": 200
      }, 
      {
        "_type": "file", 
        "bytes_downloaded": 2844, 
        "bytes_total": 2844, 
        "cache_status": "CACHED", 
        "download_seconds": 0, 
        "download_start_time": "2014-12-08T19:23:13", 
        "hash": "55ab7016031bb8a8c4a030e28b21d17fcfba1e05d9e522d473a452daea79a5d2", 
        "id": 55, 
        "last_download_progress_time": "2014-12-08T19:23:23", 
        "name": "delete-queued-patch.vbs", 
        "size": 2844, 
        "source": "https://content.tanium.com/files/initialcontent/bundles/2014-11-05_12-56-07-8513/distribute_patch_tools/delete-queued-patch.vbs", 
        "status": 200
      }, 
      {
        "_type": "file", 
        "bytes_downloaded": 104296332, 
        "bytes_total": 104296332, 
        "cache_status": "CACHED", 
        "download_seconds": 3600, 
        "download_start_time": "2014-12-08T19:25:20", 
        "hash": "7789bacbbd31f45349030e5cb23f46caeb03252d50cc5a30f43f13a54cf40887", 
        "id": 56, 
        "last_download_progress_time": "2014-12-08T19:25:41", 
        "name": "wsusscn2.cab", 
        "size": 104296332, 
        "source": "https://go.microsoft.com/fwlink/?LinkID=74689", 
        "status": 200
      }, 
      {
        "_type": "file", 
        "bytes_downloaded": 305351, 
        "bytes_total": 305351, 
        "cache_status": "CACHED", 
        "download_seconds": 3600, 
        "download_start_time": "2014-12-08T19:23:23", 
        "hash": "203a3da688fed8992d3fbf872a7b02d4a0209f3e47ae3f5512b578820540dfb0", 
        "id": 57, 
        "last_download_progress_time": "2014-12-08T19:23:34", 
        "name": "cveData.html", 
        "size": 305351, 
        "source": "https://cve.mitre.org/data/refs/refmap/source-MS.html", 
        "status": 200
      }
    ]
  }, 
  "hidden_flag": 0, 
  "id": 22, 
  "last_modified_by": "Jim Olsen", 
  "last_update": "2014-12-08T19:21:06", 
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
  "modification_time": "2014-12-08T19:21:06", 
  "name": "Distribute Patch Tools", 
  "source_id": 0, 
  "verify_group_id": 0
}

'''
