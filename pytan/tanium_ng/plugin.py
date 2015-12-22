"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``plugin``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T02-55-41Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class Plugin(BaseType):

    _soap_tag = 'plugin'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.name = None
        self.bundle = None
        self.plugin_server = None
        self.input = None
        self.script_response = None
        self.exit_code = None
        self.type = None
        self.path = None
        self.filename = None
        self.plugin_url = None
        self.run_detached_flag = None
        self.execution_id = None
        self.timeout_seconds = None
        self.cache_row_id = None
        self.local_admin_flag = None
        self.allow_rest = None
        self.raw_http_response = None
        self.raw_http_request = None
        self.use_json_flag = None
        self.status = None
        self.status_file_content = None
        self.arguments = None
        self.sql_response = None
        self.metadata = None
        self.commands = None
        self.permissions = None
        # no list_properties defined


from .plugin_sql import PluginSql
from .plugin_argument_list import PluginArgumentList
from .permission_list import PermissionList
from .plugin_command_list import PluginCommandList
from .metadata_list import MetadataList

# Simple fix for type differences for text strings: str (3.x) vs unicode (2.x)

import sys
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str  # noqa
else:
    text_type = unicode  # noqa

SIMPLE_ARGS = {}
SIMPLE_ARGS['name'] = text_type
SIMPLE_ARGS['bundle'] = text_type
SIMPLE_ARGS['plugin_server'] = text_type
SIMPLE_ARGS['input'] = text_type
SIMPLE_ARGS['script_response'] = text_type
SIMPLE_ARGS['exit_code'] = int
SIMPLE_ARGS['type'] = text_type
SIMPLE_ARGS['path'] = text_type
SIMPLE_ARGS['filename'] = text_type
SIMPLE_ARGS['plugin_url'] = text_type
SIMPLE_ARGS['run_detached_flag'] = int
SIMPLE_ARGS['execution_id'] = int
SIMPLE_ARGS['timeout_seconds'] = int
SIMPLE_ARGS['cache_row_id'] = int
SIMPLE_ARGS['local_admin_flag'] = int
SIMPLE_ARGS['allow_rest'] = int
SIMPLE_ARGS['raw_http_response'] = int
SIMPLE_ARGS['raw_http_request'] = int
SIMPLE_ARGS['use_json_flag'] = int
SIMPLE_ARGS['status'] = text_type
SIMPLE_ARGS['status_file_content'] = text_type

COMPLEX_ARGS = {}
COMPLEX_ARGS['arguments'] = PluginArgumentList
COMPLEX_ARGS['sql_response'] = PluginSql
COMPLEX_ARGS['metadata'] = MetadataList
COMPLEX_ARGS['commands'] = PluginCommandList
COMPLEX_ARGS['permissions'] = PermissionList

LIST_ARGS = {}
# no LIST_ARGS defined
