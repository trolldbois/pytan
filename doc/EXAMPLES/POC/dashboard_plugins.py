# this is a very raw and rough example of how to use the Plugin object in the SOAP API
# to create / get / delete dashboards

def plugin_zip(p):
    '''maps columns to values for each row in a plugins sql_response and returns a list of dicts'''
    return [
        dict(zip(p.sql_response.columns, x)) for x in p.sql_response.result_row
    ]


####### Create a Dashboard named 'API Test Dashboard' using the plugin system
# First some variables
dashboard_name = 'API Test Dashboard'
dashboard_text = ''
dashboard_filter = handler.get('group', name='All Computers')[0].id
dashboard_public = 1

# create the plugin parent
plugin = taniumpy.Plugin()
plugin.name = 'CreateDashboard'
plugin.bundle = 'Dashboards'

# create the plugin arguments
plugin.arguments = taniumpy.PluginArgumentList()

arg1 = taniumpy.PluginArgument()
arg1.name = 'dash_name'
arg1.type = 'String'
arg1.value = dashboard_name
plugin.arguments.append(arg1)

arg2 = taniumpy.PluginArgument()
arg2.name = 'dash_text'
arg2.type = 'String'
arg2.value = dashboard_text
plugin.arguments.append(arg2)

arg3 = taniumpy.PluginArgument()
arg3.name = 'group_id'
arg3.type = 'Number'
arg3.value = dashboard_filter
plugin.arguments.append(arg3)

arg4 = taniumpy.PluginArgument()
arg4.name = 'public_flag'
arg4.type = 'Number'
arg4.value = dashboard_public
plugin.arguments.append(arg4)

arg5 = taniumpy.PluginArgument()
arg5.name = 'sqid_xml'
arg5.type = 'String'
arg5.value = ''
plugin.arguments.append(arg5)

# run the plugin
plugin_result = session.run_plugin(plugin)

# print the results
print plugin_zip(plugin_result)

####### Get the list of dashboards using the plugin system:
# create the plugin parent
plugin = taniumpy.Plugin()
plugin.name = 'GetDashboards'
plugin.bundle = 'Dashboards'

# run the plugin
plugin_result = session.run_plugin(plugin)

# print the results
print plugin_zip(plugin_result)

####### Delete all Dashboards named 'API Test Dashboard' using the plugin system:
# First some variables
dashboard_name = 'API Test Dashboard'

# get the list of dashboards to find out which ones match the name provided
plugin = taniumpy.Plugin()
plugin.name = 'GetDashboards'
plugin.bundle = 'Dashboards'
plugin_result = session.run_plugin(plugin)
plugin_dict = plugin_zip(plugin_result)

# get the id's of the dashboards to delete if they match the dashboard_name
dashboards_to_del = [x['id'] for x in plugin_dict if x['name'] == dashboard_name]

# create the plugin parent
plugin = taniumpy.Plugin()
plugin.name = 'DeleteDashboards'
plugin.bundle = 'Dashboards'

# create the plugin arguments
plugin.arguments = taniumpy.PluginArgumentList()
arg1 = taniumpy.PluginArgument()
arg1.name = 'dashboard_ids'
arg1.type = 'Number_Set'
arg1.value = ','.join(dashboards_to_del)
plugin.arguments.append(arg1)

# run the plugin
plugin_result = session.run_plugin(plugin)

# print the results
print plugin_zip(plugin_result)

