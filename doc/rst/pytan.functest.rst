
pytan Functional Tests
**********************

This contains functional tests for pytan.

These functional tests require a connection to a Tanium server in
order to run. The connection info is pulled from the SERVER_INFO
dictionary in test/API_INFO.py.

**class test_pytan_func.CreateObjFromJsonTests(methodName='runTest')**

   Bases: ``unittest.case.TestCase``

   ``__module__ = 'test_pytan_func'``

   ``classmethod setUpClass()``

   **setup_test()**

   **test_create_from_json_action()**

   **test_create_from_json_client()**

   **test_create_from_json_group()**

   **test_create_from_json_package()**

   **test_create_from_json_question()**

   **test_create_from_json_saved_action()**

   **test_create_from_json_saved_question()**

   **test_create_from_json_sensor()**

   **test_create_from_json_setting()**

   **test_create_from_json_user()**

   **test_create_from_json_userrole()**

   **test_create_from_json_whitelisted_url()**

**class test_pytan_func.CreateObjectTests(methodName='runTest')**

   Bases: ``unittest.case.TestCase``

   ``__module__ = 'test_pytan_func'``

   ``classmethod setUpClass()``

   **setup_test()**

   **test_create_group()**

   **test_create_package()**

   **test_create_sensor()**

   **test_create_user()**

   **test_create_whitelisted_url()**

**class test_pytan_func.ExportObjTests(methodName='runTest')**

   Bases: ``unittest.case.TestCase``

   ``__module__ = 'test_pytan_func'``

   ``classmethod setUpClass()``

   **setup_test()**

   **test_export_basetype()**

   **test_export_resultset()**

**class test_pytan_func.InvalidServerTests(methodName='runTest')**

   Bases: ``unittest.case.TestCase``

   ``__module__ = 'test_pytan_func'``

   ``classmethod setUpClass()``

   **test_invalid_connect_1_bad_username()**

   **test_invalid_connect_2_bad_host_and_non_ssl_port()**

   **test_invalid_connect_3_bad_password()**

   **test_invalid_connect_4_bad_host_and_bad_port()**

**class test_pytan_func.ValidServerTests(methodName='runTest')**

   Bases: ``unittest.case.TestCase``

   ``__module__ = 'test_pytan_func'``

   ``classmethod setUpClass()``

   **setup_test()**

   **test_deploy_action_missing_package()**

   **test_deploy_action_missing_params()**

   **test_deploy_action_no_run()**

   **test_invalid_get_object_1_get_question_object_fail_by_name()**

   **test_invalid_get_object_2_get_action_object_single_by_name()**

   **test_invalid_question_1_ask_manual_human_question_param_missing_keysplit()**

   **test_invalid_question_2_ask_manual_question_invalid_sensor()**

   **test_invalid_question_3_ask_manual_question_filterhelp()**

   **test_invalid_question_4_ask_manual_human_question_invalid_sensor()**

   **test_invalid_question_5_ask_manual_human_question_invalid_filter()**

   **test_invalid_question_6_ask_manual_question_optionhelp()**

   **test_invalid_question_7_ask_manual_human_question_toomanyparams()**

   **test_valid_deploy_action()**

   **test_valid_deploy_action_no_results()**

   **test_valid_get_object_10_get_leader_clients()**

   **test_valid_get_object_11_get_all_saved_questions()**

   **test_valid_get_object_12_get_user_single_by_id()**

   **test_valid_get_object_13_get_saved_action_single_by_name()**

   **test_valid_get_object_14_get_all_settings()**

   **test_valid_get_object_15_get_sensor_multiple_selectors()**

   **test_valid_get_object_16_get_setting_single_by_name()**

   **test_valid_get_object_17_get_all_userroless()**

   **test_valid_get_object_18_get_all_questions()**

   **test_valid_get_object_19_get_all_groups()**

   **test_valid_get_object_1_get_all_users()**

   **test_valid_get_object_20_get_all_sensors()**

   **test_valid_get_object_21_get_action_single_by_id()**

   **test_valid_get_object_22_get_all_whitelisted_urls()**

   **test_valid_get_object_23_get_saved_question_single_by_name()**

   **test_valid_get_object_24_get_sensor_multiple()**

   **test_valid_get_object_25_get_user_single_by_name()**

   **test_valid_get_object_26_get_all_clients()**

   **test_valid_get_object_27_get_group_single_by_name()**

   **test_valid_get_object_28_get_all_packages()**

   **test_valid_get_object_29_get_all_actions()**

   **test_valid_get_object_2_get_question_single_by_id()**

   **test_valid_get_object_30_get_userrole_single_by_id()**

   **test_valid_get_object_3_get_sensor_single_by_hash()**

   **test_valid_get_object_4_get_sensor_single_by_id()**

   **test_valid_get_object_5_get_package_single_by_name()**

   **test_valid_get_object_6_get_sensor_single_by_name()**

   **test_valid_get_object_7_get_saved_question_multiple()**

   **test_valid_get_object_8_get_whitelisted_url_single_by_id()**

   **test_valid_get_object_9_get_all_saved_actions()**

   **test_valid_question_10_ask_manual_human_question_filter()**

   **test_valid_question_11_ask_manual_human_question_params_single()**

   **test_valid_question_12_ask_manual_human_question_simple()**

   **test_valid_question_13_ask_manual_human_question_param_sensor_noparams()**

   **test_valid_question_14_ask_manual_human_question_params_multiple()**

   **test_valid_question_15_ask_manual_human_question_complex()**

   **test_valid_question_16_ask_manual_human_question_paramsandfilterandoptions()**

   **test_valid_question_1_ask_manual_human_question_options()**

   **test_valid_question_2_ask_manual_human_question_nonparamsensor_params()**

   **test_valid_question_3_ask_manual_human_question_multiple()**

   **test_valid_question_4_ask_manual_human_question_filterandoptions()**

   **test_valid_question_5_ask_manual_question_sensor_complex()**

   **test_valid_question_6_ask_saved_question_single_list()**

   **test_valid_question_7_ask_saved_question_single_str()**

   **test_valid_question_8_ask_manual_human_question_paramsandfilter()**

   **test_valid_question_9_ask_manual_human_question_multiple_selector()**

**test_pytan_func.spew(m)**
