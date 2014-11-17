
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class Plugin(BaseType):

    _soap_tag = 'plugin'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties={'name': str,
                        'bundle': str,
                        'input': str,
                        'script_response': str,
                        'exit_code': int,
                        'type': str,
                        'path': str,
                        'filename': str,
                        'cache_row_id': int,
                        'local_admin_flag': int},
            complex_properties={'arguments': PluginArgumentList,
                        'sql_response': PluginSql,
                        'metadata': MetadataList,
                        'commands': PluginCommandList,
                        'permissions': UserPermissions},
            list_properties={},
        )
        self.name = None
        self.bundle = None
        self.input = None
        self.script_response = None
        self.exit_code = None
        self.type = None
        self.path = None
        self.filename = None
        self.cache_row_id = None
        self.local_admin_flag = None
        self.arguments = None
        self.sql_response = None
        self.metadata = None
        self.commands = None
        self.permissions = None
        

from plugin_argument_list import PluginArgumentList
from plugin_sql import PluginSql
from metadata_list import MetadataList
from plugin_command_list import PluginCommandList
from user_permissions import UserPermissions

