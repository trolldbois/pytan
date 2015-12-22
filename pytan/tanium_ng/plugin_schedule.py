"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``plugin_schedule``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class PluginSchedule(BaseType):

    _soap_tag = 'plugin_schedule'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.id = None
        self.name = None
        self.plugin_name = None
        self.plugin_bundle = None
        self.plugin_server = None
        self.start_hour = None
        self.end_hour = None
        self.start_date = None
        self.end_date = None
        self.run_on_days = None
        self.run_interval_seconds = None
        self.enabled = None
        self.deleted_flag = None
        self.input = None
        self.last_run_time = None
        self.last_exit_code = None
        self.last_run_text = None
        self.arguments = None
        self.user = None
        self.last_run_sql = None
        # no list_properties defined


from .user import User
from .plugin_argument_list import PluginArgumentList
from .plugin_sql import PluginSql

SIMPLE_ARGS = {}
SIMPLE_ARGS['id'] = int
SIMPLE_ARGS['name'] = str
SIMPLE_ARGS['plugin_name'] = str
SIMPLE_ARGS['plugin_bundle'] = str
SIMPLE_ARGS['plugin_server'] = str
SIMPLE_ARGS['start_hour'] = int
SIMPLE_ARGS['end_hour'] = int
SIMPLE_ARGS['start_date'] = int
SIMPLE_ARGS['end_date'] = int
SIMPLE_ARGS['run_on_days'] = str
SIMPLE_ARGS['run_interval_seconds'] = int
SIMPLE_ARGS['enabled'] = int
SIMPLE_ARGS['deleted_flag'] = int
SIMPLE_ARGS['input'] = str
SIMPLE_ARGS['last_run_time'] = str
SIMPLE_ARGS['last_exit_code'] = int
SIMPLE_ARGS['last_run_text'] = str

COMPLEX_ARGS = {}
COMPLEX_ARGS['arguments'] = PluginArgumentList
COMPLEX_ARGS['user'] = User
COMPLEX_ARGS['last_run_sql'] = PluginSql

LIST_ARGS = {}
# no LIST_ARGS defined
