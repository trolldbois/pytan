
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class UserRole(BaseType):

    _OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='role',
            simple_properties={'id': int,
                        'name': str,
                        'description': str},
            complex_properties={'permissions': UserPermissions},
            list_properties={},
        )
        self.id = None
        self.name = None
        self.description = None
        self.permissions = None
        

from user_permissions import UserPermissions

