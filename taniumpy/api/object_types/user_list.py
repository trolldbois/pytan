
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class UserList(BaseType):

    OBJECT_LIST_TAG = 'users'

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag = 'users',
            simple_properties = {},
            complex_properties = {},
            list_properties = {'user': User},
        )
        
        
        self.user = []

from user import User

