
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class ComputerGroupSpec(BaseType):

    OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag = 'computer_spec',
            simple_properties = {'id': int,
                        'computer_name': str,
                        'ip_address': str,
                        'enabled_flag': int},
            complex_properties = {},
            list_properties = {},
        )
        self.id = None
        self.computer_name = None
        self.ip_address = None
        self.enabled_flag = None
        
        



