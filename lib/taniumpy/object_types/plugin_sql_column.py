
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class PluginSqlColumn(BaseType):

    _soap_tag = 'columns'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties={'name': str},
            complex_properties={},
            list_properties={},
        )
        self.name = None
        
        



