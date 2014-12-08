
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class SensorStringHints(BaseType):

    _soap_tag = 'string_hints'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties={'hint': str},
            complex_properties={},
            list_properties={},
        )
        self.hint = None
        
        



