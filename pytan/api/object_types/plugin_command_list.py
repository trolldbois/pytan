
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class PluginCommandList(BaseType):

    _soap_tag = 'plugin_command_list'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties={'command': str},
            complex_properties={},
            list_properties={},
        )
        self.command = None
        
        



