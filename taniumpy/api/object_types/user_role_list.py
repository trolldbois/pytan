
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class UserRoleList(BaseType):

    OBJECT_LIST_TAG = 'roles'

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag = 'roles',
            simple_properties = {},
            complex_properties = {},
            list_properties = {'role': UserRole},
        )
        
        
        self.role = []

from user_role import UserRole

