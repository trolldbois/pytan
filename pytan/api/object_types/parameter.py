
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class Parameter(BaseType):

    OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='parameter',
            simple_properties={'key': str,
                        'value': str,
                        'type': int},
            complex_properties={},
            list_properties={},
        )
        self.key = None
        self.value = None
        self.type = None
        
        



