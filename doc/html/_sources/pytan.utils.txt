pytan.utils module
==================

.. automodule:: pytan.utils
    :show-inheritance:


Utility Classes: Logging handlers
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. autoclass:: pytan.utils.SplitStreamHandler
    :members:
    :show-inheritance:
    :undoc-members:
    :private-members:


Utility Classes: Argument Parsers for Command Line Scripts
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. autoclass:: pytan.utils.CustomArgFormat
    :members:
    :show-inheritance:
    :undoc-members:
    :private-members:

.. autoclass:: pytan.utils.CustomArgParse
    :members:
    :show-inheritance:
    :undoc-members:
    :private-members:

Utility Functions: Logging
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. autofunction:: pytan.utils.change_console_format
.. autofunction:: pytan.utils.remove_logging_handler
.. autofunction:: pytan.utils.set_all_loglevels
.. autofunction:: pytan.utils.set_log_levels
.. autofunction:: pytan.utils.setup_console_logging
.. autofunction:: pytan.utils.spew
.. autofunction:: pytan.utils.print_log_levels
.. autofunction:: pytan.utils.get_all_loggers
.. autofunction:: pytan.utils.log_session_communication

Utility Functions: Type Checking
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. autofunction:: pytan.utils.is_dict
.. autofunction:: pytan.utils.is_list
.. autofunction:: pytan.utils.is_num
.. autofunction:: pytan.utils.is_str

Utility Functions: Misc
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. autofunction:: pytan.utils.get_dict_list_len
.. autofunction:: pytan.utils.jsonify
.. autofunction:: pytan.utils.port_check
.. autofunction:: pytan.utils.test_app_port
.. autofunction:: pytan.utils.version_check
.. autofunction:: pytan.utils.xml_pretty
.. autofunction:: pytan.utils.xml_pretty_resultobj
.. autofunction:: pytan.utils.xml_pretty_resultxml
.. autofunction:: pytan.utils.get_percentage
.. autofunction:: pytan.utils.calc_percent

Utility Functions: Time and Date handling
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. autofunction:: pytan.utils.get_now
.. autofunction:: pytan.utils.human_time
.. autofunction:: pytan.utils.seconds_from_now
.. autofunction:: pytan.utils.timestr_to_datetime
.. autofunction:: pytan.utils.datetime_to_timestr
.. autofunction:: pytan.utils.func_timing

Utility Functions: Argument Parsers for Command Line Scripts
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. autofunction:: pytan.utils.setup_parser
.. autofunction:: pytan.utils.setup_get_object_argparser
.. autofunction:: pytan.utils.setup_create_json_object_argparser
.. autofunction:: pytan.utils.setup_delete_object_argparser
.. autofunction:: pytan.utils.setup_ask_saved_argparser
.. autofunction:: pytan.utils.setup_stop_action_argparser
.. autofunction:: pytan.utils.setup_deploy_action_argparser
.. autofunction:: pytan.utils.setup_get_result_argparser
.. autofunction:: pytan.utils.setup_ask_manual_argparser
.. autofunction:: pytan.utils.add_ask_report_argparser
.. autofunction:: pytan.utils.add_report_file_options
.. autofunction:: pytan.utils.add_get_object_report_argparser
.. autofunction:: pytan.utils.get_grp_opts
.. autofunction:: pytan.utils.process_create_json_object_args
.. autofunction:: pytan.utils.process_delete_object_args
.. autofunction:: pytan.utils.process_get_object_args


Utility Functions: Dehumanize human strings
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. autofunction:: pytan.utils.dehumanize_package
.. autofunction:: pytan.utils.dehumanize_question_filters
.. autofunction:: pytan.utils.dehumanize_question_options
.. autofunction:: pytan.utils.dehumanize_sensors
.. autofunction:: pytan.utils.extract_filter
.. autofunction:: pytan.utils.extract_options
.. autofunction:: pytan.utils.extract_params
.. autofunction:: pytan.utils.extract_selector
.. autofunction:: pytan.utils.map_filter
.. autofunction:: pytan.utils.map_option
.. autofunction:: pytan.utils.map_options

Utility Functions: kwargs getters
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. autofunction:: pytan.utils.get_kwargs_int

Utility Functions: Object mappers
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. autofunction:: pytan.utils.get_obj_map
.. autofunction:: pytan.utils.get_q_obj_map

Utility Functions: TaniumPy objects
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. autofunction:: pytan.utils.load_taniumpy_from_json
.. autofunction:: pytan.utils.load_param_json_file
.. autofunction:: pytan.utils.shrink_obj
.. autofunction:: pytan.utils.get_taniumpy_obj
.. autofunction:: pytan.utils.plugin_zip
.. autofunction:: pytan.utils.apply_options_obj
.. autofunction:: pytan.utils.build_group_obj
.. autofunction:: pytan.utils.build_manual_q
.. autofunction:: pytan.utils.build_metadatalist_obj
.. autofunction:: pytan.utils.build_param_obj
.. autofunction:: pytan.utils.build_param_objlist
.. autofunction:: pytan.utils.build_selectlist_obj
.. autofunction:: pytan.utils.derive_param_default
.. autofunction:: pytan.utils.empty_obj
.. autofunction:: pytan.utils.get_filter_obj
.. autofunction:: pytan.utils.get_obj_params

Utility Functions: Definition objects
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. autofunction:: pytan.utils.check_dictkey
.. autofunction:: pytan.utils.chk_def_key
.. autofunction:: pytan.utils.parse_defs
.. autofunction:: pytan.utils.val_package_def
.. autofunction:: pytan.utils.val_q_filter_defs
.. autofunction:: pytan.utils.val_sensor_defs

.. toctree::
