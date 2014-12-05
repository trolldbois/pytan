
pytan Unit Tests
****************

This contains unit tests for pytan.

These unit tests do not require a connection to a Tanium server in
order to run.

**class
test_pytan_unit.TestDehumanizeExtractionUtils(methodName='runTest')**

   Bases: ``unittest.case.TestCase``

   ``__module__ = 'test_pytan_unit'``

   **test_extract_filter_invalid()**

   **test_extract_filter_nofilter()**

   **test_extract_filter_valid()**

   **test_extract_options_invalid_option()**

   **test_extract_options_many()**

   **test_extract_options_missing_value_max_data_age()**

   **test_extract_options_missing_value_value_type()**

   **test_extract_options_nooptions()**

   **test_extract_options_single()**

   **test_extract_params()**

   **test_extract_params_missing_seperator()**

   **test_extract_params_multiparams()**

   **test_extract_params_noparams()**

   **test_extract_selector()**

   **test_extract_selector_use_name_if_noselector()**

**class
test_pytan_unit.TestDehumanizeQuestionFilterUtils(methodName='runTest')**

   Bases: ``unittest.case.TestCase``

   ``__module__ = 'test_pytan_unit'``

   **test_empty_filterlist()**

   **test_empty_filterstr()**

   **test_invalid_filter1()**

   **test_invalid_filter2()**

   **test_invalid_filter3()**

   **test_multi_filter_list()**

   **test_single_filter_list()**

   **test_single_filter_str()**

**class
test_pytan_unit.TestDehumanizeQuestionOptionUtils(methodName='runTest')**

   Bases: ``unittest.case.TestCase``

   ``__module__ = 'test_pytan_unit'``

   **test_empty_optionlist()**

   **test_empty_optionstr()**

   **test_invalid_option1()**

   **test_invalid_option2()**

   **test_option_list_many()**

   **test_option_list_multi()**

   **test_option_list_single()**

   **test_option_str()**

**class
test_pytan_unit.TestDehumanizeSensorUtils(methodName='runTest')**

   Bases: ``unittest.case.TestCase``

   ``__module__ = 'test_pytan_unit'``

   **test_empty_args_dict()**

   **test_empty_args_list()**

   **test_empty_args_str()**

   **test_multi_list_complex()**

   **test_single_str()**

   **test_single_str_complex1()**

   **test_single_str_complex2()**

   **test_single_str_with_filter()**

   **test_valid_simple_list()**

   **test_valid_simple_str_hash_selector()**

   **test_valid_simple_str_id_selector()**

   **test_valid_simple_str_name_selector()**

**class test_pytan_unit.TestGenericUtils(methodName='runTest')**

   Bases: ``unittest.case.TestCase``

   ``__module__ = 'test_pytan_unit'``

   **test_ask_kwargs()**

   **test_empty_obj()**

   **test_get_now()**

   **test_get_obj_map()**

   **test_get_q_obj_map()**

   **test_invalid_port()**

   **test_is_dict()**

   **test_is_list()**

   **test_is_not_dict()**

   **test_is_not_list()**

   **test_is_not_num()**

   **test_is_not_str()**

   **test_is_num()**

   **test_is_str()**

   **test_jsonify()**

   **test_req_kwargs()**

   **test_version_higher()**

   **test_version_lower()**

**class
test_pytan_unit.TestManualBuildObjectUtils(methodName='runTest')**

   Bases: ``unittest.case.TestCase``

   ``__module__ = 'test_pytan_unit'``

   ``classmethod setUpClass()``

   **test_build_group_obj()**

   **test_build_manual_q()**

   **test_build_selectlist_obj_invalid_filter()**

   **test_build_selectlist_obj_missing_value()**

   **test_build_selectlist_obj_noparamssensorobj_noparams()**

      builds a selectlist object using a sensor obj with no params

   **test_build_selectlist_obj_noparamssensorobj_withparams()**

      builds a selectlist object using a sensor obj with no params,
      but passing in params (which should be ignored)

   **test_build_selectlist_obj_withparamssensorobj_noparams()**

      builds a selectlist object using a sensor obj with 4 params but
      not supplying any values for any of the params

   **test_build_selectlist_obj_withparamssensorobj_withparams()**

      builds a selectlist object using a sensor obj with 4 params but
      supplying a value for only one param

**class
test_pytan_unit.TestManualPackageDefValidateUtils(methodName='runTest')**

   Bases: ``unittest.case.TestCase``

   ``__module__ = 'test_pytan_unit'``

   **test_invalid1()**

   **test_invalid2()**

   **test_valid1()**

   **test_valid2()**

**class
test_pytan_unit.TestManualQuestionFilterDefParseUtils(methodName='runTest')**

   Bases: ``unittest.case.TestCase``

   ``__module__ = 'test_pytan_unit'``

   **test_parse_emptydict()**

   **test_parse_emptylist()**

   **test_parse_emptystr()**

   **test_parse_multi_filter()**

   **test_parse_noargs()**

   **test_parse_none()**

   **test_parse_single_filter()**

   **test_parse_str()**

**class
test_pytan_unit.TestManualQuestionFilterDefValidateUtils(methodName='runTest')**

   Bases: ``unittest.case.TestCase``

   ``__module__ = 'test_pytan_unit'``

   **test_invalid1()**

   **test_valid1()**

   **test_valid2()**

**class
test_pytan_unit.TestManualQuestionOptionDefParseUtils(methodName='runTest')**

   Bases: ``unittest.case.TestCase``

   ``__module__ = 'test_pytan_unit'``

   **test_parse_emptydict()**

   **test_parse_emptylist()**

   **test_parse_emptystr()**

   **test_parse_list()**

   **test_parse_noargs()**

   **test_parse_none()**

   **test_parse_options_dict()**

   **test_parse_str()**

**class
test_pytan_unit.TestManualSensorDefParseUtils(methodName='runTest')**

   Bases: ``unittest.case.TestCase``

   ``__module__ = 'test_pytan_unit'``

   **test_parse_complex()**

      list with many items is parsed into same list

   **test_parse_dict_hash()**

      dict with hash is parsed into list of same dict

   **test_parse_dict_id()**

      dict with id is parsed into list of same dict

   **test_parse_dict_name()**

      dict with name is parsed into list of same dict

   **test_parse_emptydict()**

      args=={} throws exception

   **test_parse_emptylist()**

      args==[] throws exception

   **test_parse_emptystr()**

      args=='' throws exception

   **test_parse_noargs()**

      no args throws exception

   **test_parse_none()**

      args==None throws exception

   **test_parse_str1()**

      simple str is parsed into list of same str

**class
test_pytan_unit.TestManualSensorDefValidateUtils(methodName='runTest')**

   Bases: ``unittest.case.TestCase``

   ``__module__ = 'test_pytan_unit'``

   **test_invalid1()**

   **test_invalid2()**

   **test_invalid3()**

   **test_invalid4()**

   **test_valid1()**

   **test_valid2()**

   **test_valid3()**

   **test_valid4()**
