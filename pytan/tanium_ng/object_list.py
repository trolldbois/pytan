"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``object_list``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T02-55-41Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class ObjectList(BaseType):

    _soap_tag = 'object_list'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.export_id = None
        self.questions = None
        self.actions = None
        self.saved_actions = None
        self.roles = None
        self.system_status = None
        self.system_settings = None
        self.client_count = None
        self.white_listed_urls = None
        self.computer_groups = None
        self.question = []
        self.group = []
        self.groups = []
        self.saved_question = []
        self.saved_questions = []
        self.archived_question = []
        self.archived_questions = []
        self.parse_job = []
        self.parse_jobs = []
        self.parse_result_group = []
        self.parse_result_groups = []
        self.action = []
        self.saved_action = []
        self.action_stop = []
        self.action_stops = []
        self.package_spec = []
        self.package_specs = []
        self.package_file = []
        self.package_files = []
        self.sensor = []
        self.sensors = []
        self.user = []
        self.users = []
        self.client_status = []
        self.system_setting = []
        self.saved_action_approval = []
        self.plugin = []
        self.plugins = []
        self.plugin_schedule = []
        self.plugin_schedules = []
        self.white_listed_url = []
        self.upload_file = []
        self.upload_file_status = []
        self.soap_error = []
        self.computer_group = []


from .soap_error import SoapError
from .computer_group_list import ComputerGroupList
from .parse_result_group import ParseResultGroup
from .saved_question_list import SavedQuestionList
from .package_spec_list import PackageSpecList
from .group import Group
from .sensor import Sensor
from .archived_question_list import ArchivedQuestionList
from .parse_job_list import ParseJobList
from .parse_job import ParseJob
from .package_file import PackageFile
from .white_listed_url_list import WhiteListedUrlList
from .question import Question
from .saved_question import SavedQuestion
from .system_status_list import SystemStatusList
from .plugin_list import PluginList
from .saved_action_approval import SavedActionApproval
from .upload_file_status import UploadFileStatus
from .package_file_list import PackageFileList
from .archived_question import ArchivedQuestion
from .question_list import QuestionList
from .parse_result_group_list import ParseResultGroupList
from .client_status import ClientStatus
from .white_listed_url import WhiteListedUrl
from .action import Action
from .upload_file import UploadFile
from .sensor_list import SensorList
from .system_setting_list import SystemSettingList
from .computer_group import ComputerGroup
from .action_stop import ActionStop
from .plugin_schedule import PluginSchedule
from .package_spec import PackageSpec
from .action_list import ActionList
from .group_list import GroupList
from .plugin_schedule_list import PluginScheduleList
from .action_stop_list import ActionStopList
from .user_list import UserList
from .saved_action_list import SavedActionList
from .system_setting import SystemSetting
from .user_role_list import UserRoleList
from .client_count import ClientCount
from .saved_action import SavedAction
from .plugin import Plugin
from .user import User

# Simple fix for type differences for text strings: str (3.x) vs unicode (2.x)

import sys
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str  # noqa
else:
    text_type = unicode  # noqa

SIMPLE_ARGS = {}
SIMPLE_ARGS['export_id'] = text_type

COMPLEX_ARGS = {}
COMPLEX_ARGS['questions'] = QuestionList
COMPLEX_ARGS['actions'] = ActionList
COMPLEX_ARGS['saved_actions'] = SavedActionList
COMPLEX_ARGS['roles'] = UserRoleList
COMPLEX_ARGS['system_status'] = SystemStatusList
COMPLEX_ARGS['system_settings'] = SystemSettingList
COMPLEX_ARGS['client_count'] = ClientCount
COMPLEX_ARGS['white_listed_urls'] = WhiteListedUrlList
COMPLEX_ARGS['computer_groups'] = ComputerGroupList

LIST_ARGS = {}
LIST_ARGS['question'] = Question
LIST_ARGS['group'] = Group
LIST_ARGS['groups'] = GroupList
LIST_ARGS['saved_question'] = SavedQuestion
LIST_ARGS['saved_questions'] = SavedQuestionList
LIST_ARGS['archived_question'] = ArchivedQuestion
LIST_ARGS['archived_questions'] = ArchivedQuestionList
LIST_ARGS['parse_job'] = ParseJob
LIST_ARGS['parse_jobs'] = ParseJobList
LIST_ARGS['parse_result_group'] = ParseResultGroup
LIST_ARGS['parse_result_groups'] = ParseResultGroupList
LIST_ARGS['action'] = Action
LIST_ARGS['saved_action'] = SavedAction
LIST_ARGS['action_stop'] = ActionStop
LIST_ARGS['action_stops'] = ActionStopList
LIST_ARGS['package_spec'] = PackageSpec
LIST_ARGS['package_specs'] = PackageSpecList
LIST_ARGS['package_file'] = PackageFile
LIST_ARGS['package_files'] = PackageFileList
LIST_ARGS['sensor'] = Sensor
LIST_ARGS['sensors'] = SensorList
LIST_ARGS['user'] = User
LIST_ARGS['users'] = UserList
LIST_ARGS['client_status'] = ClientStatus
LIST_ARGS['system_setting'] = SystemSetting
LIST_ARGS['saved_action_approval'] = SavedActionApproval
LIST_ARGS['plugin'] = Plugin
LIST_ARGS['plugins'] = PluginList
LIST_ARGS['plugin_schedule'] = PluginSchedule
LIST_ARGS['plugin_schedules'] = PluginScheduleList
LIST_ARGS['white_listed_url'] = WhiteListedUrl
LIST_ARGS['upload_file'] = UploadFile
LIST_ARGS['upload_file_status'] = UploadFileStatus
LIST_ARGS['soap_error'] = SoapError
LIST_ARGS['computer_group'] = ComputerGroup
