
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class PluginCommandList(BaseType):

    OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag = 'plugin_command_list',
            simple_properties = {'command': str},
            complex_properties = {},
            list_properties = {},
        )
        self.command = None
        
        



