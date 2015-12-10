
PyTan API Python Examples
========================================================================================

This directory contains a number of python scripts that show how to use PyTan in
various ways.

They can be run immediately after changing the username, password, host, and maybe port
variables defined in each.

If you copy them outside of the EXAMPLE/PYTAN_API directory to edit and run them, you will
also need to update the pytan_loc variable to point to the directory where pytan lives.

  * pytan_api_basic_handler_example.py: This is an example for how to instantiate a :class:`pytan.Handler` object.  The username, password, host, and maybe port as well need to be provided on a per Tanium server basis.
  * create_user.py: Create a user called API Test User
  * create_package.py: Create a package called package49
  * create_group.py: Create a group called All Windows Computers API Test
  * create_whitelisted_url.py: Create a whitelisted url
  * create_package_from_json.py: Export a package object to a JSON file, adding ' API TEST' to the name of the package before exporting the JSON file and deleting any pre-existing package with the same (new) name, then create a new package object from the exported JSON file
  * create_user_from_json.py: Export a user object to a JSON file, adding ' API TEST' to the name of the user before exporting the JSON file and deleting any pre-existing user with the same (new) name, then create a new user object from the exported JSON file
  * create_saved_question_from_json.py: Export a saved question object to a JSON file, adding ' API TEST' to the name of the saved question before exporting the JSON file and deleting any pre-existing saved question with the same (new) name, then create a new saved question object from the exported JSON file
  * create_action_from_json.py: Export an action object to a JSON file, then create a new action object from the exported JSON file. Actions can not be deleted, so do not delete it. This will, in effect, 're-deploy' an action.
  * create_sensor_from_json.py: Export a sensor object to a JSON file, adding ' API TEST' to the name of the sensor before exporting the JSON file and deleting any pre-existing sensor with the same (new) name, then create a new sensor object from the exported JSON file
  * create_question_from_json.py: Export a question object to a JSON file, then create a new question object from the exported JSON file. Questions can not be deleted, so do not delete it. This will, in effect, 're-ask' a question.
  * create_whitelisted_url_from_json.py: Export a whitelisted url object to a JSON file, adding ' test1' to the url_regex of the whitelisted url before exporting the JSON file and deleting any pre-existing whitelisted url with the same (new) name, then create a new whitelisted url object from the exported JSON file
  * create_group_from_json.py: Export a group object to a JSON file, adding ' API TEST' to the name of the group before exporting the JSON file and deleting any pre-existing group with the same (new) name, then create a new group object from the exported JSON file
  * deploy_action_simple.py: Deploy an action against all computers using human strings and use Server Side Export when performing a GetResultData
  * deploy_action_simple_without_results.py: Deploy an action against all computers using human strings, but do not get the completed results of the job -- return right away with the deploy action object.
  * deploy_action_simple_against_windows_computers.py: Deploy an action against only windows computers using human strings. This requires passing in an action filter
  * deploy_action_with_params_against_windows_computers.py: Deploy an action with parameters against only windows computers using human strings.  This will use the Package 'Custom Tagging - Add Tags' and supply two parameters. The second parameter will be ignored because the package in question only requires one parameter.
  * export_basetype_csv_default_options.py: Export a BaseType from getting objects as CSV with the default options
  * export_basetype_json_type_false.py: Export a BaseType from getting objects as JSON with false for include_type
  * export_basetype_json_explode_false.py: Export a BaseType from getting objects as JSON with false for explode_json_string_values
  * export_basetype_json_explode_true.py: Export a BaseType from getting objects as JSON with true for explode_json_string_values
  * export_basetype_xml_default_options.py: Export a BaseType from getting objects as XML with the default options
  * export_basetype_xml_minimal_false.py: Export a BaseType from getting objects as XML with false for minimal
  * export_basetype_xml_minimal_true.py: Export a BaseType from getting objects as XML with true for minimal
  * export_basetype_csv_with_explode_false.py: Export a BaseType from getting objects as CSV with false for explode_json_string_values
  * export_basetype_csv_with_explode_true.py: Export a BaseType from getting objects as CSV with true for explode_json_string_values
  * export_basetype_csv_with_sort_empty_list.py: Export a BaseType from getting objects as CSV with an empty list for header_sort
  * export_basetype_csv_with_sort_true.py: Export a BaseType from getting objects as CSV with true for header_sort
  * export_basetype_csv_with_sort_list.py: Export a BaseType from getting objects as CSV with name and description for header_sort
  * export_basetype_json_default_options.py: Export a BaseType from getting objects as JSON with the default options
  * export_basetype_json_type_true.py: Export a BaseType from getting objects as JSON with true for include_type
  * export_resultset_csv_default_options.py: Export a ResultSet from asking a question as CSV with the default options
  * export_resultset_csv_expand_false.py: Export a ResultSet from asking a question as CSV with false for expand_grouped_columns
  * export_resultset_csv_expand_true.py: Export a ResultSet from asking a question as CSV with true for expand_grouped_columns
  * export_resultset_csv_all_options.py: Export a ResultSet from asking a question as CSV with true for header_add_sensor, true for header_add_type, true for header_sort, and true for expand_grouped_columns
  * export_resultset_json.py: Export a ResultSet from asking a question as JSON with the default options
  * export_resultset_csv_sort_empty.py: Export a ResultSet from asking a question as CSV with an empty list for header_sort
  * export_resultset_csv_sort_true.py: Export a ResultSet from asking a question as CSV with true for header_sort
  * export_resultset_csv_sort_false.py: Export a ResultSet from asking a question as CSV with false for header_sort
  * export_resultset_csv_sort_list.py: Export a ResultSet from asking a question as CSV with Computer Name and IP Address for the header_sort
  * export_resultset_csv_type_false.py: Export a ResultSet from asking a question as CSV with false for header_add_type
  * export_resultset_csv_type_true.py: Export a ResultSet from asking a question as CSV with true for header_add_type
  * export_resultset_csv_sensor_false.py: Export a ResultSet from asking a question as CSV with false for header_add_sensor
  * export_resultset_csv_sensor_true.py: Export a ResultSet from asking a question as CSV with true for header_add_sensor
  * get_action_by_id.py: Get an action by id
  * get_question_by_id.py: Get a question by id
  * get_saved_question_by_names.py: Get two saved questions by name
  * get_userrole_by_id.py: Get a user role by id.
  * get_leader_clients.py: Get all clients that are Leader status
  * get_setting_by_name.py: Get a system setting by name
  * get_user_by_name.py: Get a user by name
  * get_sensor_by_id.py: Get a sensor by id
  * get_sensor_by_mixed.py: Get multiple sensors by id, name, and hash
  * get_whitelisted_url_by_id.py: Get a whitelisted url by id
  * get_group_by_name.py: Get a group by name
  * get_sensor_by_hash.py: Get a sensor by hash
  * get_package_by_name.py: Get a package by name
  * get_sensor_by_names.py: Get multiple sensors by name
  * get_saved_question_by_name.py: Get saved question by name
  * get_user_by_id.py: Get a user by id
  * get_sensor_by_name.py: Get a sensor by name
  * get_saved_action_by_name.py: Get a saved action by name
  * get_all_users.py: Get all users
  * get_all_saved_actions.py: Get all saved actions
  * get_all_settings.py: Get all system settings
  * get_all_saved_questions.py: Get all saved questions
  * get_all_userroless.py: Get all user roles
  * get_all_questions.py: Get all questions
  * get_all_groups.py: Get all groups
  * get_all_sensors.py: Get all sensors
  * get_all_whitelisted_urls.py: Get all whitelisted urls
  * get_all_clients.py: Get all clients
  * get_all_packages.py: Get all packages
  * get_all_actions.py: Get all actions
  * ask_parsed_question_pick_first_no_results.py: Ask the server to parse the question text 'computer name and ip route details' and choose the first parsed result as the question to run, return right away and do not wait for results to complete/do not get result data at all
  * ask_parsed_question_pick_first_sse.py: Ask the server to parse the question text 'computer name and ip route details' and choose the first parsed result as the question to run and use server side export when performing a GetResultData
  * ask_parsed_question_pick_first.py: Ask the server to parse the question text 'computer name and ip route details' and choose the first parsed result as the question to run
  * ask_manual_question_simple_single_sensor_no_results.py: Ask a manual question using human strings by referencing the name of a single sensor in a string, return right away and do not wait for results to complete/do not get result data at all.  No sensor filters, sensor parameters, sensor filter options, question filters, or question options supplied.
  * ask_manual_question_simple_multiple_sensors.py: Ask a manual question using human strings by referencing the name of multiple sensors in a list.  No sensor filters, sensor parameters, sensor filter options, question filters, or question options supplied.
  * ask_manual_question_simple_single_sensor_sse.py: Ask a manual question using human strings by referencing the name of a single sensor in a string and use server side export when getting result data.
  * ask_manual_question_simple_single_sensor.py: Ask a manual question using human strings by referencing the name of a single sensor in a string.  No sensor filters, sensor parameters, sensor filter options, question filters, or question options supplied.
  * ask_manual_question_multiple_sensors_identified_by_name.py: Ask a manual question using human strings by referencing the name of multiple sensors and providing a selector that tells pytan explicitly that we are providing a name of a sensor.  No sensor filters, sensor parameters, sensor filter options, question filters, or question options supplied.
  * ask_manual_question_sensor_with_parameters_and_some_supplied_parameters.py: Ask a manual question using human strings by referencing the name of a single sensor that takes parameters, but supplying only two of the four parameters that are used by the sensor (and letting pytan automatically determine the appropriate default value for those parameters which require a value and none was supplied).  No sensor filters, sensor parameters, sensor filter options, question filters, or question options supplied.
  * ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters.py: Ask a manual question using human strings by referencing the name of multiple sensors, one that takes parameters, but supplying only two of the four parameters that are used by the sensor (and letting pytan automatically determine the appropriate default value for those parameters which require a value and none was supplied), and one that does not take parameters.  No sensor filters, question filters, or question options supplied.
  * ask_manual_question_sensor_without_parameters_and_supplied_parameters.py: Ask a manual question using human strings by referencing the name of a single sensor that does NOT take parameters, but supplying parameters anyways (which will be ignored since the sensor does not take parameters).  No sensor filters, sensor filter options, question filters, or question options supplied.
  * ask_manual_question_sensor_with_parameters_and_filter.py: Ask a manual question using human strings by referencing the name of a single sensor that takes parameters, but supplying only two of the four parameters that are used by the sensor.  Also supply a sensor filter that limits the column data that is shown to values that match the regex '.*Shared.*'.  No sensor filter options, question filters, or question options supplied.
  * ask_manual_question_sensor_with_filter_and_2_options.py: Ask a manual question using human strings by referencing the name of a single sensor.  Also supply a sensor filter that limits the column data that is shown to values that contain Windows (which is short hand for regex match against .*Windows.*).  Also supply filter options that re-fetches any cached data that is older than 3600 seconds and treats the values as type string.  No question filters or question options supplied.
  * ask_manual_question_sensor_with_filter.py: Ask a manual question using human strings by referencing the name of a single sensor.  Also supply a sensor filter that limits the column data that is shown to values that contain Windows (which is short hand for regex match against .*Windows.*).  No sensor parameters, sensor filter options, question filters or question options supplied.
  * ask_manual_question_sensor_with_parameters_and_filter_and_options.py: Ask a manual question using human strings by referencing the name of a single sensor that takes parameters, but supplying only two of the four parameters that are used by the sensor.  Also supply a sensor filter that limits the column data that is shown to values that match the regex '.*Shared.*', and a sensor filter option that re-fetches any cached data that is older than 3600 seconds.  No question filters or question options supplied.
  * ask_manual_question_sensor_with_filter_and_3_options.py: Ask a manual question using human strings by referencing the name of a single sensor.  Also supply a sensor filter that limits the column data that is shown to values that contain Windows (which is short hand for regex match against .*Windows.*).  Also supply filter options that re-fetches any cached data that is older than 3600 seconds, matches all values supplied in the filter, and ignores case for any value match of the filter.  No sensor paramaters, question filters, or question options supplied.
  * ask_manual_question_complex_query1.py: Ask a manual question using human strings by referencing the name of a two sensors sensor.  Supply 3 parameters for the second sensor, one of which is not a valid parameter (and will be ignored).  Supply one option to the second sensor.  Supply two question filters that limit the rows returned in the result to computers that match the sensor Operating System that contains Windows and does not contain Windows.  Supply two question options that 'or' the two question filters and ignore the case of any values while matching the question filters.
  * ask_manual_question_complex_query2.py: This is another complex query that gets the Computer Name and Last Logged in User and Installed Applications that contains Google Search or Google Chrome and limits the rows that are displayed to computers that contain the Installed Applications of Google Search or Google Chrome
  * _ask_manual_question_sensor_complex.py: This provides an example for asking a manual question without using human strings.  It uses the Computer Name and Folder Contents sensors.  The second sensor has a single parameter, folderPath, with a value of 'c:\Program Files'.  The second sensor also has 3 sensor filter options that set the max data age to 3600 seconds, does NOT ignore case, and treats all values as string.  There is also a question filter supplied that limits the rows that are displayed to computers that match an Operating System that contains Windows, and has 3 question filter options supplied that set the max data age to 3600 seconds, does NOT ignore case, and uses 'and' to join all question filters.
  * ask_saved_question_refresh_data.py: Ask a saved question and refresh the data for the saved question (asks a new question)
  * ask_saved_question_by_name_sse.py: Ask a saved question by referencing the name of a saved question in a string and use Server Side Export when performing a GetResultData
  * ask_saved_question_by_name.py: Ask a saved question by referencing the name of a saved question in a string.
  * ask_saved_question_by_name_in_list.py: Ask a saved question by referencing the name of a saved question in a list of strings.
  * invalid_create_sensor.py: Create a sensor (Unsupported!)
  * invalid_create_saved_action_from_json.py: Create a saved action from json (not supported!)
  * invalid_create_client_from_json.py: Create a client from json (not supported!)
  * invalid_create_userrole_from_json.py: Create a user role from json (not supported!)
  * invalid_create_setting_from_json.py: Create a setting from json (not supported!)
  * invalid_deploy_action_run_false.py: Deploy an action without run=True, which will only run the pre-deploy action question that matches action_filters, export the results to a file, and raise a RunFalse exception
  * invalid_deploy_action_package_help.py: Have deploy_action() return the help for package
  * invalid_deploy_action_package.py: Deploy an action using a non-existing package.
  * invalid_deploy_action_options_help.py: Have deploy_action() return the help for options
  * invalid_deploy_action_empty_package.py: Deploy an action using an empty package string.
  * invalid_deploy_action_filters_help.py: Have deploy_action() return the help for filters
  * invalid_deploy_action_missing_parameters.py: Deploy an action using a package that requires parameters but do not supply any parameters.
  * invalid_export_basetype_csv_bad_explode_type.py: Export a BaseType from getting objects using a bad explode_json_string_values
  * invalid_export_basetype_csv_bad_sort_sub_type.py: Export a BaseType from getting objects using a bad header_sort
  * invalid_export_basetype_csv_bad_sort_type.py: Export a BaseType from getting objects using a bad header_sort
  * invalid_export_basetype_xml_bad_minimal_type.py: Export a BaseType from getting objects using a bad minimal
  * invalid_export_basetype_json_bad_include_type.py: Export a BaseType from getting objects using a bad include_type
  * invalid_export_basetype_json_bad_explode_type.py: Export a BaseType from getting objects using a bad explode_json_string_values
  * invalid_export_basetype_bad_format.py: Export a BaseType from getting objects using a bad export_format
  * invalid_export_resultset_csv_bad_sort_sub_type.py: Export a ResultSet from asking a question using a bad header_sort
  * invalid_export_resultset_csv_bad_sort_type.py: Export a ResultSet from asking a question using a bad header_sort
  * invalid_export_resultset_csv_bad_expand_type.py: Export a ResultSet from asking a question using a bad expand_grouped_columns
  * invalid_export_resultset_csv_bad_sensors_sub_type.py: Export a ResultSet from asking a question using a bad sensors
  * invalid_export_resultset_bad_format.py: Export a ResultSet from asking a question using a bad export_format
  * invalid_get_action_single_by_name.py: Get an action by name (name is not a supported selector for action)
  * invalid_get_question_by_name.py: Get a question by name (name is not a supported selector for question)
  * invalid_ask_manual_question_sensor_help.py: Have ask_manual() return the help for sensors
  * invalid_ask_manual_question_filter_help.py: Have ask_manual() return the help for filters
  * invalid_ask_manual_question_option_help.py: Have ask_manual() return the help for options
  * invalid_ask_manual_question_bad_filter.py: Ask a question using an invalid filter.
  * invalid_ask_parsed_question_no_picker.py: Ask a parsed question without supplying a picker
  * invalid_ask_manual_question_bad_sensorname.py: Ask a question using a sensor that does not exist
  * invalid_ask_manual_question_too_many_parameter_blocks.py: Ask a question that supplies too many parameter blocks ({}).
  * invalid_ask_manual_question_bad_option.py: Ask a question using an invalid option.
  * invalid_ask_manual_question_missing_parameter_split.py: Ask a question with parameters that are missing a splitter (=) to designate the key from value.
