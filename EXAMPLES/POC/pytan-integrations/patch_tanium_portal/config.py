# configure me
config = {
    'pytan_dir': '/Users/jolsen/gh/pytan/lib',
    'tanium_username': 'Tanium User',
    'tanium_password': 'T@n!um',
    'tanium_host': '172.16.31.128',
    'max_data_age': 60,
    'pct_complete_threshold': 98.00,
    'sync_scan_name': 'Run Patch Scan Synchronously',
    'sync_scan_opts': {
        'command': 'cmd /c cscript //T:3600 ..\\..\\Tools\\run-patch-scan.vbs',
        'command_timeout_seconds': 1200,
        'expire_seconds': 1800,
    },
    # 'sync_install_name': 'Install Deployed Patches Synchronously',
    # 'sync_install_opts': {
    #     'command': 'cmd /c cscript //T:3600 ..\\..\\Tools\\install-patches.vbs',
    #     'command_timeout_seconds': 3600,
    #     'expire_seconds': 1200,
    # },
    'max_question_data_retry': 5,
    'patchpkg_name': "Managed Windows Patch Deployment - {KB Article} - {Title}".format,
    'patchpkg_opts': {
        'command': 'cmd /c cscript //T:3600 ..\\..\\Tools\\copy-patch-files.vbs',
        'expire_seconds': 7200,
        'command_timeout_seconds': 3000,
    },
}
