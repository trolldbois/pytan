
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class SensorSubcolumn(BaseType):

    _OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='subcolumn',
            simple_properties={'name': str,
                        'index': int,
                        'value_type': str,
                        'ignore_case_flag': int,
                        'hidden_flag': int,
                        'exclude_from_parse_flag': int},
            complex_properties={},
            list_properties={},
        )
        self.name = None
        self.index = None
        self.value_type = None
        self.ignore_case_flag = None
        self.hidden_flag = None
        self.exclude_from_parse_flag = None
        
        



