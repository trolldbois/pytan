
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class ParameterList(BaseType):

    _OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='parameter_list',
            simple_properties={},
            complex_properties={},
            list_properties={'parameter': Parameter},
        )
        
        
        self.parameter = []

from parameter import Parameter

