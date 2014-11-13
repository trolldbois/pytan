
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class PluginSqlResult(BaseType):

    _OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='result_row',
            simple_properties={'value': str},
            complex_properties={},
            list_properties={},
        )
        self.value = None
        
        



