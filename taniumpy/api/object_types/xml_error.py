
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class XmlError(BaseType):

    _OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='error',
            simple_properties={'type': str,
                        'exception': str,
                        'error_context': str},
            complex_properties={},
            list_properties={},
        )
        self.type = None
        self.exception = None
        self.error_context = None
        
        



