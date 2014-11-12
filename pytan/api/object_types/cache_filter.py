
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class CacheFilter(BaseType):

    OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='filter',
            simple_properties={'field': str,
                        'value': str,
                        'type': str,
                        'operator': str,
                        'not_flag': int},
            complex_properties={},
            list_properties={},
        )
        self.field = None
        self.value = None
        self.type = None
        self.operator = None
        self.not_flag = None
        
        



