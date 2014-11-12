
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class SoapError(BaseType):

    OBJECT_LIST_TAG = 'soap_error'

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag = 'soap_error',
            simple_properties = {'object_name': str,
                        'exception_name': str,
                        'context': str,
                        'object_request': str},
            complex_properties = {},
            list_properties = {},
        )
        self.object_name = None
        self.exception_name = None
        self.context = None
        self.object_request = None
        
        



