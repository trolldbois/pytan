
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class UserPermissions(BaseType):

    _soap_tag = 'permissions'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties={'permission': str},
            complex_properties={},
            list_properties={},
        )
        self.permission = None
        
        



