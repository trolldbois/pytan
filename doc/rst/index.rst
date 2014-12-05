
Welcome to PyTan's documentation!
*********************************


Table of Contents
*****************

* `Description <description>`_
* `Why it was created <description#why-it-was-created>`_
* `Requirements <description#requirements>`_
* `Installation <description#installation>`_
* `pytan package <pytan>`_
  * `pytan.handler module <pytan.handler>`_
    * `Handler Class <pytan.handler#handler-class>`_
      * `Example: Create a Handler object
        <pytan.handler#example-create-a-handler-object>`_
      * `Handler Methods: Questions and Actions
        <pytan.handler#handler-methods-questions-and-actions>`_
      * `Handler Methods: Exporting/Importing Objects
        <pytan.handler#handler-methods-exporting-importing-objects>`_
      * `Handler Methods: Creating Objects
        <pytan.handler#handler-methods-creating-objects>`_
      * `Handler Methods: Deleting Objects
        <pytan.handler#handler-methods-deleting-objects>`_
      * `Handler Methods: Getting Objects
        <pytan.handler#handler-methods-getting-objects>`_
      * `Handler Methods: Getting Result Data / Result Info
        <pytan.handler#handler-methods-getting-result-data-result-info>`_
      * `Handler Methods: Private Methods
        <pytan.handler#handler-methods-private-methods>`_
  * `pytan.constants module <pytan.constants>`_
  * `pytan.utils module <pytan.utils>`_
    * `Utility Classes: Exceptions
      <pytan.utils#utility-classes-exceptions>`_
    * `Utility Classes: Logging handlers
      <pytan.utils#utility-classes-logging-handlers>`_
    * `Utility Classes: Argument Parsers for Command Line Scripts
      <pytan.utils#utility-classes-argument-parsers-for-command-line-scripts>`_
    * `Utility Functions: Logging
      <pytan.utils#utility-functions-logging>`_
    * `Utility Functions: Type Checking
      <pytan.utils#utility-functions-type-checking>`_
    * `Utility Functions: Misc <pytan.utils#utility-functions-misc>`_
    * `Utility Functions: Argument Parsers for Command Line Scripts
      <pytan.utils#utility-functions-argument-parsers-for-command-line-scripts>`_
    * `Utility Functions: Dehumanize human strings
      <pytan.utils#utility-functions-dehumanize-human-strings>`_
    * `Utility Functions: kwargs getters
      <pytan.utils#utility-functions-kwargs-getters>`_
    * `Utility Functions: Object mappers
      <pytan.utils#utility-functions-object-mappers>`_
    * `Utility Functions: TaniumPy objects
      <pytan.utils#utility-functions-taniumpy-objects>`_
    * `Utility Functions: Definition objects
      <pytan.utils#utility-functions-definition-objects>`_
  * `pytan Unit Tests <pytan.unittest>`_
  * `pytan Functional Tests <pytan.functest>`_
* `taniumpy package <taniumpy>`_
  * `taniumpy.session module <taniumpy.session>`_
  * `taniumpy.question_asker module <taniumpy.question_asker>`_
  * `taniumpy.object_types package <taniumpy.object_types>`_
    * `taniumpy.object_types module
      <taniumpy.object_types#module-taniumpy.object_types>`_
    * `taniumpy.object_types.action module
      <taniumpy.object_types#module-taniumpy.object_types.action>`_
    * `taniumpy.object_types.action_list module
      <taniumpy.object_types#module-taniumpy.object_types.action_list>`_
    * `taniumpy.object_types.action_list_info module
      <taniumpy.object_types#module-taniumpy.object_types.action_list_info>`_
    * `taniumpy.object_types.action_stop module
      <taniumpy.object_types#module-taniumpy.object_types.action_stop>`_
    * `taniumpy.object_types.action_stop_list module
      <taniumpy.object_types#module-taniumpy.object_types.action_stop_list>`_
    * `taniumpy.object_types.all_objects module
      <taniumpy.object_types#module-taniumpy.object_types.all_objects>`_
    * `taniumpy.object_types.archived_question module
      <taniumpy.object_types#module-taniumpy.object_types.archived_question>`_
    * `taniumpy.object_types.archived_question_list module
      <taniumpy.object_types#module-taniumpy.object_types.archived_question_list>`_
    * `taniumpy.object_types.audit_data module
      <taniumpy.object_types#module-taniumpy.object_types.audit_data>`_
    * `taniumpy.object_types.base module
      <taniumpy.object_types#module-taniumpy.object_types.base>`_
    * `taniumpy.object_types.cache_filter module
      <taniumpy.object_types#module-taniumpy.object_types.cache_filter>`_
    * `taniumpy.object_types.cache_filter_list module
      <taniumpy.object_types#module-taniumpy.object_types.cache_filter_list>`_
    * `taniumpy.object_types.cache_info module
      <taniumpy.object_types#module-taniumpy.object_types.cache_info>`_
    * `taniumpy.object_types.client_count module
      <taniumpy.object_types#module-taniumpy.object_types.client_count>`_
    * `taniumpy.object_types.client_status module
      <taniumpy.object_types#module-taniumpy.object_types.client_status>`_
    * `taniumpy.object_types.column module
      <taniumpy.object_types#module-taniumpy.object_types.column>`_
    * `taniumpy.object_types.column_set module
      <taniumpy.object_types#module-taniumpy.object_types.column_set>`_
    * `taniumpy.object_types.computer_group module
      <taniumpy.object_types#module-taniumpy.object_types.computer_group>`_
    * `taniumpy.object_types.computer_group_list module
      <taniumpy.object_types#module-taniumpy.object_types.computer_group_list>`_
    * `taniumpy.object_types.computer_group_spec module
      <taniumpy.object_types#module-taniumpy.object_types.computer_group_spec>`_
    * `taniumpy.object_types.computer_spec_list module
      <taniumpy.object_types#module-taniumpy.object_types.computer_spec_list>`_
    * `taniumpy.object_types.error_list module
      <taniumpy.object_types#module-taniumpy.object_types.error_list>`_
    * `taniumpy.object_types.filter module
      <taniumpy.object_types#module-taniumpy.object_types.filter>`_
    * `taniumpy.object_types.filter_list module
      <taniumpy.object_types#module-taniumpy.object_types.filter_list>`_
    * `taniumpy.object_types.group module
      <taniumpy.object_types#module-taniumpy.object_types.group>`_
    * `taniumpy.object_types.group_list module
      <taniumpy.object_types#module-taniumpy.object_types.group_list>`_
    * `taniumpy.object_types.metadata_item module
      <taniumpy.object_types#module-taniumpy.object_types.metadata_item>`_
    * `taniumpy.object_types.metadata_list module
      <taniumpy.object_types#module-taniumpy.object_types.metadata_list>`_
    * `taniumpy.object_types.object_list module
      <taniumpy.object_types#module-taniumpy.object_types.object_list>`_
    * `taniumpy.object_types.object_list_types module
      <taniumpy.object_types#module-taniumpy.object_types.object_list_types>`_
    * `taniumpy.object_types.options module
      <taniumpy.object_types#module-taniumpy.object_types.options>`_
    * `taniumpy.object_types.package_file module
      <taniumpy.object_types#module-taniumpy.object_types.package_file>`_
    * `taniumpy.object_types.package_file_list module
      <taniumpy.object_types#module-taniumpy.object_types.package_file_list>`_
    * `taniumpy.object_types.package_file_status module
      <taniumpy.object_types#module-taniumpy.object_types.package_file_status>`_
    * `taniumpy.object_types.package_file_status_list module
      <taniumpy.object_types#module-taniumpy.object_types.package_file_status_list>`_
    * `taniumpy.object_types.package_file_template module
      <taniumpy.object_types#module-taniumpy.object_types.package_file_template>`_
    * `taniumpy.object_types.package_file_template_list module
      <taniumpy.object_types#module-taniumpy.object_types.package_file_template_list>`_
    * `taniumpy.object_types.package_spec module
      <taniumpy.object_types#module-taniumpy.object_types.package_spec>`_
    * `taniumpy.object_types.package_spec_list module
      <taniumpy.object_types#module-taniumpy.object_types.package_spec_list>`_
    * `taniumpy.object_types.parameter module
      <taniumpy.object_types#module-taniumpy.object_types.parameter>`_
    * `taniumpy.object_types.parameter_list module
      <taniumpy.object_types#module-taniumpy.object_types.parameter_list>`_
    * `taniumpy.object_types.parse_job module
      <taniumpy.object_types#module-taniumpy.object_types.parse_job>`_
    * `taniumpy.object_types.parse_job_list module
      <taniumpy.object_types#module-taniumpy.object_types.parse_job_list>`_
    * `taniumpy.object_types.parse_result module
      <taniumpy.object_types#module-taniumpy.object_types.parse_result>`_
    * `taniumpy.object_types.parse_result_group module
      <taniumpy.object_types#module-taniumpy.object_types.parse_result_group>`_
    * `taniumpy.object_types.parse_result_group_list module
      <taniumpy.object_types#module-taniumpy.object_types.parse_result_group_list>`_
    * `taniumpy.object_types.parse_result_list module
      <taniumpy.object_types#module-taniumpy.object_types.parse_result_list>`_
    * `taniumpy.object_types.plugin module
      <taniumpy.object_types#module-taniumpy.object_types.plugin>`_
    * `taniumpy.object_types.plugin_argument module
      <taniumpy.object_types#module-taniumpy.object_types.plugin_argument>`_
    * `taniumpy.object_types.plugin_argument_list module
      <taniumpy.object_types#module-taniumpy.object_types.plugin_argument_list>`_
    * `taniumpy.object_types.plugin_command_list module
      <taniumpy.object_types#module-taniumpy.object_types.plugin_command_list>`_
    * `taniumpy.object_types.plugin_list module
      <taniumpy.object_types#module-taniumpy.object_types.plugin_list>`_
    * `taniumpy.object_types.plugin_schedule module
      <taniumpy.object_types#module-taniumpy.object_types.plugin_schedule>`_
    * `taniumpy.object_types.plugin_schedule_list module
      <taniumpy.object_types#module-taniumpy.object_types.plugin_schedule_list>`_
    * `taniumpy.object_types.plugin_sql module
      <taniumpy.object_types#module-taniumpy.object_types.plugin_sql>`_
    * `taniumpy.object_types.plugin_sql_column module
      <taniumpy.object_types#module-taniumpy.object_types.plugin_sql_column>`_
    * `taniumpy.object_types.plugin_sql_result module
      <taniumpy.object_types#module-taniumpy.object_types.plugin_sql_result>`_
    * `taniumpy.object_types.question module
      <taniumpy.object_types#module-taniumpy.object_types.question>`_
    * `taniumpy.object_types.question_list module
      <taniumpy.object_types#module-taniumpy.object_types.question_list>`_
    * `taniumpy.object_types.question_list_info module
      <taniumpy.object_types#module-taniumpy.object_types.question_list_info>`_
    * `taniumpy.object_types.result_info module
      <taniumpy.object_types#module-taniumpy.object_types.result_info>`_
    * `taniumpy.object_types.result_set module
      <taniumpy.object_types#module-taniumpy.object_types.result_set>`_
    * `taniumpy.object_types.row module
      <taniumpy.object_types#module-taniumpy.object_types.row>`_
    * `taniumpy.object_types.saved_action module
      <taniumpy.object_types#module-taniumpy.object_types.saved_action>`_
    * `taniumpy.object_types.saved_action_approval module
      <taniumpy.object_types#module-taniumpy.object_types.saved_action_approval>`_
    * `taniumpy.object_types.saved_action_list module
      <taniumpy.object_types#module-taniumpy.object_types.saved_action_list>`_
    * `taniumpy.object_types.saved_action_policy module
      <taniumpy.object_types#module-taniumpy.object_types.saved_action_policy>`_
    * `taniumpy.object_types.saved_action_row_id_list module
      <taniumpy.object_types#module-taniumpy.object_types.saved_action_row_id_list>`_
    * `taniumpy.object_types.saved_question module
      <taniumpy.object_types#module-taniumpy.object_types.saved_question>`_
    * `taniumpy.object_types.saved_question_list module
      <taniumpy.object_types#module-taniumpy.object_types.saved_question_list>`_
    * `taniumpy.object_types.select module
      <taniumpy.object_types#module-taniumpy.object_types.select>`_
    * `taniumpy.object_types.select_list module
      <taniumpy.object_types#module-taniumpy.object_types.select_list>`_
    * `taniumpy.object_types.sensor module
      <taniumpy.object_types#module-taniumpy.object_types.sensor>`_
    * `taniumpy.object_types.sensor_list module
      <taniumpy.object_types#module-taniumpy.object_types.sensor_list>`_
    * `taniumpy.object_types.sensor_query module
      <taniumpy.object_types#module-taniumpy.object_types.sensor_query>`_
    * `taniumpy.object_types.sensor_query_list module
      <taniumpy.object_types#module-taniumpy.object_types.sensor_query_list>`_
    * `taniumpy.object_types.sensor_string_hints module
      <taniumpy.object_types#module-taniumpy.object_types.sensor_string_hints>`_
    * `taniumpy.object_types.sensor_subcolumn module
      <taniumpy.object_types#module-taniumpy.object_types.sensor_subcolumn>`_
    * `taniumpy.object_types.sensor_subcolumn_list module
      <taniumpy.object_types#module-taniumpy.object_types.sensor_subcolumn_list>`_
    * `taniumpy.object_types.sensor_types module
      <taniumpy.object_types#module-taniumpy.object_types.sensor_types>`_
    * `taniumpy.object_types.soap_error module
      <taniumpy.object_types#module-taniumpy.object_types.soap_error>`_
    * `taniumpy.object_types.system_setting module
      <taniumpy.object_types#module-taniumpy.object_types.system_setting>`_
    * `taniumpy.object_types.system_settings_list module
      <taniumpy.object_types#module-taniumpy.object_types.system_settings_list>`_
    * `taniumpy.object_types.system_status_aggregate module
      <taniumpy.object_types#module-taniumpy.object_types.system_status_aggregate>`_
    * `taniumpy.object_types.system_status_list module
      <taniumpy.object_types#module-taniumpy.object_types.system_status_list>`_
    * `taniumpy.object_types.upload_file module
      <taniumpy.object_types#module-taniumpy.object_types.upload_file>`_
    * `taniumpy.object_types.upload_file_list module
      <taniumpy.object_types#module-taniumpy.object_types.upload_file_list>`_
    * `taniumpy.object_types.upload_file_status module
      <taniumpy.object_types#module-taniumpy.object_types.upload_file_status>`_
    * `taniumpy.object_types.user module
      <taniumpy.object_types#module-taniumpy.object_types.user>`_
    * `taniumpy.object_types.user_list module
      <taniumpy.object_types#module-taniumpy.object_types.user_list>`_
    * `taniumpy.object_types.user_permissions module
      <taniumpy.object_types#module-taniumpy.object_types.user_permissions>`_
    * `taniumpy.object_types.user_role module
      <taniumpy.object_types#module-taniumpy.object_types.user_role>`_
    * `taniumpy.object_types.user_role_list module
      <taniumpy.object_types#module-taniumpy.object_types.user_role_list>`_
    * `taniumpy.object_types.version_aggregate module
      <taniumpy.object_types#module-taniumpy.object_types.version_aggregate>`_
    * `taniumpy.object_types.version_aggregate_list module
      <taniumpy.object_types#module-taniumpy.object_types.version_aggregate_list>`_
    * `taniumpy.object_types.white_listed_url module
      <taniumpy.object_types#module-taniumpy.object_types.white_listed_url>`_
    * `taniumpy.object_types.white_listed_url_list module
      <taniumpy.object_types#module-taniumpy.object_types.white_listed_url_list>`_
    * `taniumpy.object_types.xml_error module
      <taniumpy.object_types#module-taniumpy.object_types.xml_error>`_
* `xmltodict module <xmltodict>`_
* `ddt module <ddt>`_
* `threaded_http module <threaded_http>`_

Indices and tables
******************

* `Index <genindex>`_

* `Module Index <py-modindex>`_

* `Search Page <search>`_
