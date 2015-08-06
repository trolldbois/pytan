
Export basetype csv default options
==========================================================================================

Export a BaseType from getting objects as CSV with the default options

Example Python Code
----------------------------------------------------------------------------------------

.. code-block:: python
    :linenos:


    
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
    PORT = "444"
    
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
    
    # setup the export_obj kwargs for later
    export_kwargs = {}
    export_kwargs["export_format"] = u'csv'
    
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
    
    out = export_str
    if len(out.splitlines()) > 15:
        out = out.splitlines()[0:15]
        out.append('..trimmed for brevity..')
        out = '\n'.join(out)
    
    print out
    


Output from Python Code
----------------------------------------------------------------------------------------

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
    
    print the export_str returned from export_obj():
    category,creation_time,delimiter,description,exclude_from_parse_flag,hash,hidden_flag,id,ignore_case_flag,last_modified_by,max_age_seconds,metadata_item_0_admin_flag,metadata_item_0_name,metadata_item_0_value,modification_time,name,parameter_definition,queries_query_0_platform,queries_query_0_script,queries_query_0_script_type,queries_query_1_platform,queries_query_1_script,queries_query_1_script_type,queries_query_2_platform,queries_query_2_script,queries_query_2_script_type,source_id,string_count,subcolumns_subcolumn_0_hidden_flag,subcolumns_subcolumn_0_ignore_case_flag,subcolumns_subcolumn_0_index,subcolumns_subcolumn_0_name,subcolumns_subcolumn_0_value_type,subcolumns_subcolumn_1_hidden_flag,subcolumns_subcolumn_1_ignore_case_flag,subcolumns_subcolumn_1_index,subcolumns_subcolumn_1_name,subcolumns_subcolumn_1_value_type,subcolumns_subcolumn_2_hidden_flag,subcolumns_subcolumn_2_ignore_case_flag,subcolumns_subcolumn_2_index,subcolumns_subcolumn_2_name,subcolumns_subcolumn_2_value_type,subcolumns_subcolumn_3_hidden_flag,subcolumns_subcolumn_3_ignore_case_flag,subcolumns_subcolumn_3_index,subcolumns_subcolumn_3_name,subcolumns_subcolumn_3_value_type,subcolumns_subcolumn_4_hidden_flag,subcolumns_subcolumn_4_ignore_case_flag,subcolumns_subcolumn_4_index,subcolumns_subcolumn_4_name,subcolumns_subcolumn_4_value_type,subcolumns_subcolumn_5_hidden_flag,subcolumns_subcolumn_5_ignore_case_flag,subcolumns_subcolumn_5_index,subcolumns_subcolumn_5_name,subcolumns_subcolumn_5_value_type,value_type
    Reserved,,,"The assigned name of the client machine.
    Example: workstation-1.company.com",0,3409330187,0,3,1,,86400,,,,,Computer Name,,Windows,select CSName from win32_operatingsystem,WMIQuery,,,,,,,0,9,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,String
    Network,2015-03-03T19:03:36,|,"Returns IPv4 network routes, filtered to exclude noise. With Flags, Metric, Interface columns.
    Example:  172.16.0.0|192.168.1.1|255.255.0.0|UG|100|eth0",1,435227963,0,737,1,Jim Olsen,60,0,defined,Tanium,2015-03-03T19:03:36,IP Route Details,,Windows,"strComputer = &quot;.&quot;
    Set objWMIService = GetObject(&quot;winmgmts:&quot; _
        &amp; &quot;{impersonationLevel=impersonate}!\\&quot; &amp; strComputer &amp; &quot;\root\cimv2&quot;)
    
    Set collip = objWMIService.ExecQuery(&quot;select * from win32_networkadapterconfiguration where IPEnabled=&#039;True&#039;&quot;)
    dim ipaddrs()
    ipcount = 0
    for each ipItem in collip
        for each ipaddr in ipItem.IPAddress
            ipcount = ipcount + 1
        next
    ..trimmed for brevity..
