"""Tanium NG: An object Serializer/Deserializer for the XML used by the Tanium SOAP API

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T02-55-41Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType
from .column import Column
from .column_set import ColumnSet
from .result_info import ResultInfo
from .result_set import ResultSet
from .row import Row
from .action import Action
from .action_list import ActionList
from .action_list_info import ActionListInfo
from .action_stop import ActionStop
from .action_stop_list import ActionStopList
from .archived_question import ArchivedQuestion
from .archived_question_list import ArchivedQuestionList
from .audit_data import AuditData
from .cache_filter import CacheFilter
from .cache_filter_list import CacheFilterList
from .cache_info import CacheInfo
from .client_count import ClientCount
from .client_status import ClientStatus
from .computer_group import ComputerGroup
from .computer_group_list import ComputerGroupList
from .computer_group_spec import ComputerGroupSpec
from .computer_spec_list import ComputerSpecList
from .error_list import ErrorList
from .filter import Filter
from .filter_list import FilterList
from .group import Group
from .group_list import GroupList
from .metadata_item import MetadataItem
from .metadata_list import MetadataList
from .object_list import ObjectList
from .options import Options
from .package_file import PackageFile
from .package_file_list import PackageFileList
from .package_file_status import PackageFileStatus
from .package_file_status_list import PackageFileStatusList
from .package_file_template import PackageFileTemplate
from .package_file_template_list import PackageFileTemplateList
from .package_spec import PackageSpec
from .package_spec_list import PackageSpecList
from .parameter import Parameter
from .parameter_list import ParameterList
from .parse_job import ParseJob
from .parse_job_list import ParseJobList
from .parse_result import ParseResult
from .parse_result_group import ParseResultGroup
from .parse_result_group_list import ParseResultGroupList
from .parse_result_list import ParseResultList
from .permission_list import PermissionList
from .plugin import Plugin
from .plugin_argument import PluginArgument
from .plugin_argument_list import PluginArgumentList
from .plugin_command_list import PluginCommandList
from .plugin_list import PluginList
from .plugin_schedule import PluginSchedule
from .plugin_schedule_list import PluginScheduleList
from .plugin_sql import PluginSql
from .plugin_sql_column import PluginSqlColumn
from .plugin_sql_result import PluginSqlResult
from .question import Question
from .question_list import QuestionList
from .question_list_info import QuestionListInfo
from .saved_action import SavedAction
from .saved_action_approval import SavedActionApproval
from .saved_action_list import SavedActionList
from .saved_action_policy import SavedActionPolicy
from .saved_action_row_id_list import SavedActionRowIdList
from .saved_question import SavedQuestion
from .saved_question_list import SavedQuestionList
from .select import Select
from .select_list import SelectList
from .sensor import Sensor
from .sensor_list import SensorList
from .sensor_query import SensorQuery
from .sensor_query_list import SensorQueryList
from .sensor_subcolumn import SensorSubcolumn
from .sensor_subcolumn_list import SensorSubcolumnList
from .soap_error import SoapError
from .string_hint_list import StringHintList
from .system_setting import SystemSetting
from .system_setting_list import SystemSettingList
from .system_status_aggregate import SystemStatusAggregate
from .system_status_list import SystemStatusList
from .upload_file import UploadFile
from .upload_file_list import UploadFileList
from .upload_file_status import UploadFileStatus
from .user import User
from .user_list import UserList
from .user_role import UserRole
from .user_role_list import UserRoleList
from .version_aggregate import VersionAggregate
from .version_aggregate_list import VersionAggregateList
from .white_listed_url import WhiteListedUrl
from .white_listed_url_list import WhiteListedUrlList
from .xml_error import XmlError

OBJECT_TYPES = {
    'action': Action,
    'actions': ActionList,
    'info': ActionListInfo,
    'action_stop': ActionStop,
    'action_stops': ActionStopList,
    'archived_question': ArchivedQuestion,
    'archived_questions': ArchivedQuestionList,
    'audit_data': AuditData,
    'filter': CacheFilter,
    'cache_filters': CacheFilterList,
    'cache_info': CacheInfo,
    'client_count': ClientCount,
    'client_status': ClientStatus,
    'computer_group': ComputerGroup,
    'computer_groups': ComputerGroupList,
    'computer_spec': ComputerGroupSpec,
    'computer_specs': ComputerSpecList,
    'errors': ErrorList,
    'filter': Filter,
    'filters': FilterList,
    'group': Group,
    'groups': GroupList,
    'item': MetadataItem,
    'metadata': MetadataList,
    'object_list': ObjectList,
    'options': Options,
    'file': PackageFile,
    'package_files': PackageFileList,
    'status': PackageFileStatus,
    'file_status': PackageFileStatusList,
    'file_template': PackageFileTemplate,
    'file_templates': PackageFileTemplateList,
    'package_spec': PackageSpec,
    'package_specs': PackageSpecList,
    'parameter': Parameter,
    'parameters': ParameterList,
    'parse_job': ParseJob,
    'parse_jobs': ParseJobList,
    'parse_result': ParseResult,
    'parse_result_group': ParseResultGroup,
    'parse_result_groups': ParseResultGroupList,
    'parse_results': ParseResultList,
    'permissions': PermissionList,
    'plugin': Plugin,
    'argument': PluginArgument,
    'arguments': PluginArgumentList,
    'commands': PluginCommandList,
    'plugins': PluginList,
    'plugin_schedule': PluginSchedule,
    'plugin_schedules': PluginScheduleList,
    'sql_response': PluginSql,
    'columns': PluginSqlColumn,
    'result_row': PluginSqlResult,
    'question': Question,
    'questions': QuestionList,
    'info': QuestionListInfo,
    'saved_action': SavedAction,
    'saved_action_approval': SavedActionApproval,
    'saved_actions': SavedActionList,
    'policy': SavedActionPolicy,
    'row_ids': SavedActionRowIdList,
    'saved_question': SavedQuestion,
    'saved_questions': SavedQuestionList,
    'select': Select,
    'selects': SelectList,
    'sensor': Sensor,
    'sensors': SensorList,
    'query': SensorQuery,
    'queries': SensorQueryList,
    'subcolumn': SensorSubcolumn,
    'subcolumns': SensorSubcolumnList,
    'soap_error': SoapError,
    'string_hints': StringHintList,
    'system_setting': SystemSetting,
    'system_settings': SystemSettingList,
    'aggregate': SystemStatusAggregate,
    'system_status': SystemStatusList,
    'upload_file': UploadFile,
    'file_parts': UploadFileList,
    'upload_file_status': UploadFileStatus,
    'user': User,
    'users': UserList,
    'role': UserRole,
    'roles': UserRoleList,
    'version': VersionAggregate,
    'versions': VersionAggregateList,
    'white_listed_url': WhiteListedUrl,
    'white_listed_urls': WhiteListedUrlList,
    'error': XmlError,
}

__all__ = [
    'OBJECT_TYPES',
    'BaseType',
    'Column',
    'ColumnSet',
    'ResultInfo',
    'ResultSet',
    'Row',
    'Action',
    'ActionList',
    'ActionListInfo',
    'ActionStop',
    'ActionStopList',
    'ArchivedQuestion',
    'ArchivedQuestionList',
    'AuditData',
    'CacheFilter',
    'CacheFilterList',
    'CacheInfo',
    'ClientCount',
    'ClientStatus',
    'ComputerGroup',
    'ComputerGroupList',
    'ComputerGroupSpec',
    'ComputerSpecList',
    'ErrorList',
    'Filter',
    'FilterList',
    'Group',
    'GroupList',
    'MetadataItem',
    'MetadataList',
    'ObjectList',
    'Options',
    'PackageFile',
    'PackageFileList',
    'PackageFileStatus',
    'PackageFileStatusList',
    'PackageFileTemplate',
    'PackageFileTemplateList',
    'PackageSpec',
    'PackageSpecList',
    'Parameter',
    'ParameterList',
    'ParseJob',
    'ParseJobList',
    'ParseResult',
    'ParseResultGroup',
    'ParseResultGroupList',
    'ParseResultList',
    'PermissionList',
    'Plugin',
    'PluginArgument',
    'PluginArgumentList',
    'PluginCommandList',
    'PluginList',
    'PluginSchedule',
    'PluginScheduleList',
    'PluginSql',
    'PluginSqlColumn',
    'PluginSqlResult',
    'Question',
    'QuestionList',
    'QuestionListInfo',
    'SavedAction',
    'SavedActionApproval',
    'SavedActionList',
    'SavedActionPolicy',
    'SavedActionRowIdList',
    'SavedQuestion',
    'SavedQuestionList',
    'Select',
    'SelectList',
    'Sensor',
    'SensorList',
    'SensorQuery',
    'SensorQueryList',
    'SensorSubcolumn',
    'SensorSubcolumnList',
    'SoapError',
    'StringHintList',
    'SystemSetting',
    'SystemSettingList',
    'SystemStatusAggregate',
    'SystemStatusList',
    'UploadFile',
    'UploadFileList',
    'UploadFileStatus',
    'User',
    'UserList',
    'UserRole',
    'UserRoleList',
    'VersionAggregate',
    'VersionAggregateList',
    'WhiteListedUrl',
    'WhiteListedUrlList',
    'XmlError',
]
