
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class VersionAggregate(BaseType):

    OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='version',
            simple_properties={'version_string': str,
                        'count': int,
                        'filtered': int},
            complex_properties={},
            list_properties={},
        )
        self.version_string = None
        self.count = None
        self.filtered = None
        
        



