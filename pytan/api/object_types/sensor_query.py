
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class SensorQuery(BaseType):

    OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='query',
            simple_properties={'platform': str,
                        'script': str,
                        'script_type': str,
                        'signature': str},
            complex_properties={},
            list_properties={},
        )
        self.platform = None
        self.script = None
        self.script_type = None
        self.signature = None
        
        



