from action import Action
from action_stop import ActionStop
from action_stop_list import ActionStopList
from action_list import ActionList
from archived_question import ArchivedQuestion
from archived_question_list import ArchivedQuestionList
from client_count import ClientCount
from client_status import ClientStatus
from computer_group import ComputerGroup
from computer_group_list import ComputerGroupList
from group import Group
from group_list import GroupList
from package_file import PackageFile
from package_file_list import PackageFileList
from package_spec import PackageSpec
from package_spec_list import PackageSpecList
from parse_job import ParseJob
from parse_job_list import ParseJobList
from parse_result_group import ParseResultGroup
from parse_result_group_list import ParseResultGroupList
from plugin import Plugin
from plugin_schedule import PluginSchedule
from plugin_schedule_list import PluginScheduleList
from plugin_list import PluginList
from question import Question
from question_list import QuestionList
from user_role_list import UserRoleList
from saved_action import SavedAction
from saved_action_approval import SavedActionApproval
from saved_action_list import SavedActionList
from saved_question import SavedQuestion
from saved_question_list import SavedQuestionList
from sensor import Sensor
from sensor_list import SensorList
from soap_error import SoapError
from system_setting import SystemSetting
from system_settings_list import SystemSettingsList
from system_status_list import SystemStatusList
from upload_file import UploadFile
from upload_file_status import UploadFileStatus
from user import User
from user_list import UserList
from white_listed_url import WhiteListedUrl
from white_listed_url_list import WhiteListedUrlList


OBJECT_LIST_TYPES = {
	'action': Action,
	'action_stop': ActionStop,
	'action_stops': ActionStopList,
	'actions': ActionList,
	'archived_question': ArchivedQuestion,
	'archived_questions': ArchivedQuestionList,
	'client_count': ClientCount,
	'client_status': ClientStatus,
	'computer_group': ComputerGroup,
	'computer_groups': ComputerGroupList,
	'group': Group,
	'groups': GroupList,
	'package_file': PackageFile,
	'package_files': PackageFileList,
	'package_spec': PackageSpec,
	'package_specs': PackageSpecList,
	'parse_job': ParseJob,
	'parse_jobs': ParseJobList,
	'parse_result_group': ParseResultGroup,
	'parse_result_groups': ParseResultGroupList,
	'plugin': Plugin,
	'plugin_schedule': PluginSchedule,
	'plugin_schedules': PluginScheduleList,
	'plugins': PluginList,
	'question': Question,
	'questions': QuestionList,
	'roles': UserRoleList,
	'saved_action': SavedAction,
	'saved_action_approval': SavedActionApproval,
	'saved_actions': SavedActionList,
	'saved_question': SavedQuestion,
	'saved_questions': SavedQuestionList,
	'sensor': Sensor,
	'sensors': SensorList,
	'soap_error': SoapError,
	'system_setting': SystemSetting,
	'system_settings': SystemSettingsList,
	'system_status': SystemStatusList,
	'upload_file': UploadFile,
	'upload_file_status': UploadFileStatus,
	'user': User,
	'users': UserList,
	'white_listed_url': WhiteListedUrl,
	'white_listed_urls': WhiteListedUrlList,
}