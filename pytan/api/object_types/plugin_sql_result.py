
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class PluginSqlResult(BaseType):

    _soap_tag = 'result_row'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties={'value': str},
            complex_properties={},
            list_properties={},
        )
        self.value = None
        
        



