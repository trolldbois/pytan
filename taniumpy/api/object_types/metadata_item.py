
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class MetadataItem(BaseType):

    _OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='item',
            simple_properties={'name': str,
                        'value': str,
                        'admin_flag': int},
            complex_properties={},
            list_properties={},
        )
        self.name = None
        self.value = None
        self.admin_flag = None
        
        



