
taniumpy.object_types package
*****************************


taniumpy.object_types module
============================


taniumpy.object_types.action module
===================================

**class taniumpy.object_types.action.Action**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.action_list module
========================================

**class taniumpy.object_types.action_list.ActionList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.action_list_info module
=============================================

**class taniumpy.object_types.action_list_info.ActionListInfo**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.action_stop module
========================================

**class taniumpy.object_types.action_stop.ActionStop**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.action_stop_list module
=============================================

**class taniumpy.object_types.action_stop_list.ActionStopList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.all_objects module
========================================


taniumpy.object_types.archived_question module
==============================================

**class taniumpy.object_types.archived_question.ArchivedQuestion**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.archived_question_list module
===================================================

**class
taniumpy.object_types.archived_question_list.ArchivedQuestionList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.audit_data module
=======================================

**class taniumpy.object_types.audit_data.AuditData**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.base module
=================================

**class taniumpy.object_types.base.BaseType(simple_properties,
complex_properties, list_properties)**

   Bases: `object
   <http://docs.python.org/2.7/library/functions.html#object>`_

   **append(n)**

      Allow adding to list.

      Only supported on types that have a single property that is in
      list_properties

   **explode_json(val)**

   **flatten_jsonable(val, prefix)**

   ``classmethod fromSOAPBody(body)``

      Parse body (text) and produce Python tanium objects.

      This method assumes a single result_object, which may be a list
      or a single object.

   ``classmethod fromSOAPElement(el)``

   ``static from_jsonable(jsonable)``

      Inverse of to_jsonable, with explode_json_string_values=False.

      This can be used to import objects from serialized JSON. This
      JSON should come from
      BaseType.to_jsonable(explode_json_string_values=False,
      include+type=True)

      -[ Examples ]-

      >>> with open('question_list.json') as fd:
      ...    questions = json.loads(fd.read())
      ...    # is a list of serialized questions
      ...    question_objects = BaseType.from_jsonable(questions)
      ...    # will return a list of api.Question

   **toSOAPBody(minimal=False)**

   **toSOAPElement(minimal=False)**

   **to_flat_dict(prefix='', explode_json_string_values=False)**

      Convert the object to a dict, flattening any lists or nested
      types

   **to_flat_dict_explode_json(val, prefix='')**

      see if the value is json. If so, flatten it out into a dict

   ``static to_json(jsonable, **kwargs)``

      Convert to a json string.

      jsonable can be a single BaseType instance of a list of BaseType

   **to_jsonable(explode_json_string_values=False,
   include_type=True)**

   ``static write_csv(fd, val, explode_json_string_values=False,
   **kwargs)``

      Write 'val' to CSV. val can be a BaseType instance or a list of
      BaseType

      This does a two-pass, calling to_flat_dict for each object, then
      finding the union of all headers, then writing out the value of
      each column for each object sorted by header name

      explode_json_string_values attempts to see if any of the str
      values are parseable by json.loads, and if so treat each
      property as a column value

      fd is a file-like object

**exception
taniumpy.object_types.base.IncorrectTypeException(property, expected,
actual)**

   Bases: `exceptions.Exception
   <http://docs.python.org/2.7/library/exceptions.html#exceptions.Exception>`_

   Raised when a property is not of the expected type


taniumpy.object_types.cache_filter module
=========================================

**class taniumpy.object_types.cache_filter.CacheFilter**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.cache_filter_list module
==============================================

**class taniumpy.object_types.cache_filter_list.CacheFilterList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.cache_info module
=======================================

**class taniumpy.object_types.cache_info.CacheInfo**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.client_count module
=========================================

**class taniumpy.object_types.client_count.ClientCount**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.client_status module
==========================================

**class taniumpy.object_types.client_status.ClientStatus**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.column module
===================================

**class taniumpy.object_types.column.Column**

   Bases: `object
   <http://docs.python.org/2.7/library/functions.html#object>`_

   ``classmethod fromSOAPElement(el)``


taniumpy.object_types.column_set module
=======================================

**class taniumpy.object_types.column_set.ColumnSet**

   Bases: `object
   <http://docs.python.org/2.7/library/functions.html#object>`_

   ``classmethod fromSOAPElement(el)``


taniumpy.object_types.computer_group module
===========================================

**class taniumpy.object_types.computer_group.ComputerGroup**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.computer_group_list module
================================================

**class taniumpy.object_types.computer_group_list.ComputerGroupList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.computer_group_spec module
================================================

**class taniumpy.object_types.computer_group_spec.ComputerGroupSpec**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.computer_spec_list module
===============================================

**class taniumpy.object_types.computer_spec_list.ComputerSpecList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.error_list module
=======================================

**class taniumpy.object_types.error_list.ErrorList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.filter module
===================================

**class taniumpy.object_types.filter.Filter**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.filter_list module
========================================

**class taniumpy.object_types.filter_list.FilterList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.group module
==================================

**class taniumpy.object_types.group.Group**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.group_list module
=======================================

**class taniumpy.object_types.group_list.GroupList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.metadata_item module
==========================================

**class taniumpy.object_types.metadata_item.MetadataItem**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.metadata_list module
==========================================

**class taniumpy.object_types.metadata_list.MetadataList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.object_list module
========================================

**class taniumpy.object_types.object_list.ObjectList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.object_list_types module
==============================================


taniumpy.object_types.options module
====================================

**class taniumpy.object_types.options.Options**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.package_file module
=========================================

**class taniumpy.object_types.package_file.PackageFile**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.package_file_list module
==============================================

**class taniumpy.object_types.package_file_list.PackageFileList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.package_file_status module
================================================

**class taniumpy.object_types.package_file_status.PackageFileStatus**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.package_file_status_list module
=====================================================

**class
taniumpy.object_types.package_file_status_list.PackageFileStatusList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.package_file_template module
==================================================

**class
taniumpy.object_types.package_file_template.PackageFileTemplate**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.package_file_template_list module
=======================================================

**class
taniumpy.object_types.package_file_template_list.PackageFileTemplateList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.package_spec module
=========================================

**class taniumpy.object_types.package_spec.PackageSpec**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.package_spec_list module
==============================================

**class taniumpy.object_types.package_spec_list.PackageSpecList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.parameter module
======================================

**class taniumpy.object_types.parameter.Parameter**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.parameter_list module
===========================================

**class taniumpy.object_types.parameter_list.ParameterList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.parse_job module
======================================

**class taniumpy.object_types.parse_job.ParseJob**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.parse_job_list module
===========================================

**class taniumpy.object_types.parse_job_list.ParseJobList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.parse_result module
=========================================

**class taniumpy.object_types.parse_result.ParseResult**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.parse_result_group module
===============================================

**class taniumpy.object_types.parse_result_group.ParseResultGroup**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.parse_result_group_list module
====================================================

**class
taniumpy.object_types.parse_result_group_list.ParseResultGroupList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.parse_result_list module
==============================================

**class taniumpy.object_types.parse_result_list.ParseResultList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.plugin module
===================================

**class taniumpy.object_types.plugin.Plugin**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.plugin_argument module
============================================

**class taniumpy.object_types.plugin_argument.PluginArgument**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.plugin_argument_list module
=================================================

**class
taniumpy.object_types.plugin_argument_list.PluginArgumentList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.plugin_command_list module
================================================

**class taniumpy.object_types.plugin_command_list.PluginCommandList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.plugin_list module
========================================

**class taniumpy.object_types.plugin_list.PluginList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.plugin_schedule module
============================================

**class taniumpy.object_types.plugin_schedule.PluginSchedule**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.plugin_schedule_list module
=================================================

**class
taniumpy.object_types.plugin_schedule_list.PluginScheduleList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.plugin_sql module
=======================================

**class taniumpy.object_types.plugin_sql.PluginSql**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.plugin_sql_column module
==============================================

**class taniumpy.object_types.plugin_sql_column.PluginSqlColumn**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.plugin_sql_result module
==============================================

**class taniumpy.object_types.plugin_sql_result.PluginSqlResult**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.question module
=====================================

**class taniumpy.object_types.question.Question**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.question_list module
==========================================

**class taniumpy.object_types.question_list.QuestionList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.question_list_info module
===============================================

**class taniumpy.object_types.question_list_info.QuestionListInfo**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.result_info module
========================================

**class taniumpy.object_types.result_info.ResultInfo**

   Bases: `object
   <http://docs.python.org/2.7/library/functions.html#object>`_

   Wrap the result of GetResultInfo

   ``classmethod fromSOAPElement(el)``

      Deserialize a ResultInfo from a result_info SOAPElement

      Assumes all properties are integer values (true today)


taniumpy.object_types.result_set module
=======================================

**class taniumpy.object_types.result_set.ResultSet**

   Bases: `object
   <http://docs.python.org/2.7/library/functions.html#object>`_

   Wrap the result of GetResultData

   ``classmethod fromSOAPElement(el)``

      Deserialize a ResultInfo from a result_info SOAPElement

      Assumes all properties are integer values (true today)

   ``static to_json(jsonable, **kwargs)``

      Convert to a json string.

      jsonable must be a ResultSet instance

   **to_jsonable(**kwargs)**

   ``static write_csv(fd, val, **kwargs)``


taniumpy.object_types.row module
================================

**class taniumpy.object_types.row.Row(columns)**

   Bases: `object
   <http://docs.python.org/2.7/library/functions.html#object>`_

   A row in a result set.

   Values are stored in column order, also accessible by key using []

   ``classmethod fromSOAPElement(el, columns)``


taniumpy.object_types.saved_action module
=========================================

**class taniumpy.object_types.saved_action.SavedAction**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.saved_action_approval module
==================================================

**class
taniumpy.object_types.saved_action_approval.SavedActionApproval**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.saved_action_list module
==============================================

**class taniumpy.object_types.saved_action_list.SavedActionList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.saved_action_policy module
================================================

**class taniumpy.object_types.saved_action_policy.SavedActionPolicy**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.saved_action_row_id_list module
=====================================================

**class
taniumpy.object_types.saved_action_row_id_list.SavedActionRowIdList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.saved_question module
===========================================

**class taniumpy.object_types.saved_question.SavedQuestion**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.saved_question_list module
================================================

**class taniumpy.object_types.saved_question_list.SavedQuestionList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.select module
===================================

**class taniumpy.object_types.select.Select**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.select_list module
========================================

**class taniumpy.object_types.select_list.SelectList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.sensor module
===================================

**class taniumpy.object_types.sensor.Sensor**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.sensor_list module
========================================

**class taniumpy.object_types.sensor_list.SensorList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.sensor_query module
=========================================

**class taniumpy.object_types.sensor_query.SensorQuery**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.sensor_query_list module
==============================================

**class taniumpy.object_types.sensor_query_list.SensorQueryList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.sensor_string_hints module
================================================

**class taniumpy.object_types.sensor_string_hints.SensorStringHints**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.sensor_subcolumn module
=============================================

**class taniumpy.object_types.sensor_subcolumn.SensorSubcolumn**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.sensor_subcolumn_list module
==================================================

**class
taniumpy.object_types.sensor_subcolumn_list.SensorSubcolumnList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.sensor_types module
=========================================


taniumpy.object_types.soap_error module
=======================================

**class taniumpy.object_types.soap_error.SoapError**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.system_setting module
===========================================

**class taniumpy.object_types.system_setting.SystemSetting**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.system_settings_list module
=================================================

**class
taniumpy.object_types.system_settings_list.SystemSettingsList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.system_status_aggregate module
====================================================

**class
taniumpy.object_types.system_status_aggregate.SystemStatusAggregate**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.system_status_list module
===============================================

**class taniumpy.object_types.system_status_list.SystemStatusList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.upload_file module
========================================

**class taniumpy.object_types.upload_file.UploadFile**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.upload_file_list module
=============================================

**class taniumpy.object_types.upload_file_list.UploadFileList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.upload_file_status module
===============================================

**class taniumpy.object_types.upload_file_status.UploadFileStatus**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.user module
=================================

**class taniumpy.object_types.user.User**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.user_list module
======================================

**class taniumpy.object_types.user_list.UserList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.user_permissions module
=============================================

**class taniumpy.object_types.user_permissions.UserPermissions**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.user_role module
======================================

**class taniumpy.object_types.user_role.UserRole**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.user_role_list module
===========================================

**class taniumpy.object_types.user_role_list.UserRoleList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.version_aggregate module
==============================================

**class taniumpy.object_types.version_aggregate.VersionAggregate**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.version_aggregate_list module
===================================================

**class
taniumpy.object_types.version_aggregate_list.VersionAggregateList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.white_listed_url module
=============================================

**class taniumpy.object_types.white_listed_url.WhiteListedUrl**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.white_listed_url_list module
==================================================

**class
taniumpy.object_types.white_listed_url_list.WhiteListedUrlList**

   Bases: ``taniumpy.object_types.base.BaseType``


taniumpy.object_types.xml_error module
======================================

**class taniumpy.object_types.xml_error.XmlError**

   Bases: ``taniumpy.object_types.base.BaseType``
