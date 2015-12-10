#!/usr/bin/env python
"""
Export a BaseType from getting objects as CSV with true for explode_json_string_values
"""
# import the basic python packages we need
import os
import sys
import tempfile
import pprint
import traceback

# disable python from generating a .pyc file
sys.dont_write_bytecode = True

# change me to the path of pytan if this script is not running from EXAMPLES/PYTAN_API
pytan_loc = "~/gh/pytan"
pytan_static_path = os.path.join(os.path.expanduser(pytan_loc), 'lib')

# Determine our script name, script dir
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)

# try to automatically determine the pytan lib directory by assuming it is in '../../lib/'
parent_dir = os.path.dirname(my_dir)
pytan_root_dir = os.path.dirname(parent_dir)
lib_dir = os.path.join(pytan_root_dir, 'lib')

# add pytan_loc and lib_dir to the PYTHONPATH variable
path_adds = [lib_dir, pytan_static_path]
[sys.path.append(aa) for aa in path_adds if aa not in sys.path]

# import pytan
import pytan

# create a dictionary of arguments for the pytan handler
handler_args = {}

# establish our connection info for the Tanium Server
handler_args['username'] = "Administrator"
handler_args['password'] = "Tanium2015!"
handler_args['host'] = "10.0.1.240"
handler_args['port'] = "443"  # optional

# optional, level 0 is no output except warnings/errors
# level 1 through 12 are more and more verbose
handler_args['loglevel'] = 1

# optional, use a debug format for the logging output (uses two lines per log entry)
handler_args['debugformat'] = False

# optional, this saves all response objects to handler.session.ALL_REQUESTS_RESPONSES
# very useful for capturing the full exchange of XML requests and responses
handler_args['record_all_requests'] = True

# instantiate a handler using all of the arguments in the handler_args dictionary
print "...CALLING: pytan.handler() with args: {}".format(handler_args)
handler = pytan.Handler(**handler_args)

# print out the handler string
print "...OUTPUT: handler string: {}".format(handler)

# setup the arguments for the handler() class
kwargs = {}
kwargs["export_format"] = u'csv'
kwargs["explode_json_string_values"] = True

# setup the arguments for handler.get()
get_kwargs = {
    'name': [
        "Computer Name", "IP Route Details", "IP Address",
        'Folder Contents',
    ],
    'objtype': 'sensor',
}

# get the objects that will provide the basetype that we want to export
print "...CALLING: handler.get() with args: {}".format(get_kwargs)
response = handler.get(**get_kwargs)

# store the basetype object as the obj we want to export
kwargs['obj'] = response

# export the object to a string
# (we could just as easily export to a file using export_to_report_file)
print "...CALLING: handler.export_obj() with args {}".format(kwargs)
out = handler.export_obj(**kwargs)

# trim the output if it is more than 15 lines long
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\n'.join(out)

print "...OUTPUT: print the export_str returned from export_obj():"
print out

'''STDOUT from running this:
...CALLING: pytan.handler() with args: {'username': 'Administrator', 'record_all_requests': True, 'loglevel': 1, 'debugformat': False, 'host': '10.0.1.240', 'password': 'Tanium2015!', 'port': '443'}
...OUTPUT: handler string: PyTan v2.1.4 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
...CALLING: handler.get() with args: {'objtype': 'sensor', 'name': ['Computer Name', 'IP Route Details', 'IP Address', 'Folder Contents']}
...CALLING: handler.export_obj() with args {'export_format': u'csv', 'explode_json_string_values': True, 'obj': <taniumpy.object_types.sensor_list.SensorList object at 0x104b15210>}
...OUTPUT: print the export_str returned from export_obj():
category,creation_time,delimiter,description,exclude_from_parse_flag,hash,hidden_flag,id,ignore_case_flag,last_modified_by,max_age_seconds,metadata_item_0_admin_flag,metadata_item_0_name,metadata_item_0_value,modification_time,name,parameter_definition_model,parameter_definition_parameterType,parameter_definition_parameters_0_defaultValue,parameter_definition_parameters_0_helpString,parameter_definition_parameters_0_key,parameter_definition_parameters_0_label,parameter_definition_parameters_0_maxChars,parameter_definition_parameters_0_model,parameter_definition_parameters_0_parameterType,parameter_definition_parameters_0_promptText,parameter_definition_parameters_0_restrict,parameter_definition_parameters_0_validationExpressions_0_expression,parameter_definition_parameters_0_validationExpressions_0_flags,parameter_definition_parameters_0_validationExpressions_0_helpString,parameter_definition_parameters_0_validationExpressions_0_model,parameter_definition_parameters_0_validationExpressions_0_parameterType,parameter_definition_parameters_0_value,queries_query_0_platform,queries_query_0_script,queries_query_0_script_type,queries_query_1_platform,queries_query_1_script,queries_query_1_script_type,queries_query_2_platform,queries_query_2_script,queries_query_2_script_type,queries_query_3_platform,queries_query_3_script,queries_query_3_script_type,queries_query_4_platform,queries_query_4_script,queries_query_4_script_type,source_id,string_count,subcolumns_subcolumn_0_hidden_flag,subcolumns_subcolumn_0_ignore_case_flag,subcolumns_subcolumn_0_index,subcolumns_subcolumn_0_name,subcolumns_subcolumn_0_value_type,subcolumns_subcolumn_1_hidden_flag,subcolumns_subcolumn_1_ignore_case_flag,subcolumns_subcolumn_1_index,subcolumns_subcolumn_1_name,subcolumns_subcolumn_1_value_type,subcolumns_subcolumn_2_hidden_flag,subcolumns_subcolumn_2_ignore_case_flag,subcolumns_subcolumn_2_index,subcolumns_subcolumn_2_name,subcolumns_subcolumn_2_value_type,subcolumns_subcolumn_3_hidden_flag,subcolumns_subcolumn_3_ignore_case_flag,subcolumns_subcolumn_3_index,subcolumns_subcolumn_3_name,subcolumns_subcolumn_3_value_type,subcolumns_subcolumn_4_hidden_flag,subcolumns_subcolumn_4_ignore_case_flag,subcolumns_subcolumn_4_index,subcolumns_subcolumn_4_name,subcolumns_subcolumn_4_value_type,subcolumns_subcolumn_5_hidden_flag,subcolumns_subcolumn_5_ignore_case_flag,subcolumns_subcolumn_5_index,subcolumns_subcolumn_5_name,subcolumns_subcolumn_5_value_type,value_type
Reserved,,,"The assigned name of the client machine.
Example: workstation-1.company.com",0,3409330187,0,3,1,,86400,,,,,Computer Name,,,,,,,,,,,,,,,,,,Windows,select CSName from win32_operatingsystem,WMIQuery,,,,,,,,,,,,,0,5,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,String
Network,2015-09-14T13:39:12,|,"Returns IPv4 network routes, filtered to exclude noise. With Flags, Metric, Interface columns.
Example:  172.16.0.0|192.168.1.1|255.255.0.0|UG|100|eth0",1,435227963,0,568,1,Administrator,60,0,defined,Tanium,2015-09-14T13:39:12,IP Route Details,,,,,,,,,,,,,,,,,,Windows,"strComputer = &quot;.&quot;
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

'''

'''STDERR from running this:

'''
