"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``user``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class User(BaseType):

    _soap_tag = 'user'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.id = None
        self.name = None
        self.domain = None
        self.group_id = None
        self.deleted_flag = None
        self.last_login = None
        self.active_session_count = None
        self.local_admin_flag = None
        self.permissions = None
        self.roles = None
        self.metadata = None
        # no list_properties defined


from .metadata_list import MetadataList
from .user_role_list import UserRoleList
from .permission_list import PermissionList

SIMPLE_ARGS = {}
SIMPLE_ARGS['id'] = int
SIMPLE_ARGS['name'] = str
SIMPLE_ARGS['domain'] = str
SIMPLE_ARGS['group_id'] = int
SIMPLE_ARGS['deleted_flag'] = int
SIMPLE_ARGS['last_login'] = str
SIMPLE_ARGS['active_session_count'] = int
SIMPLE_ARGS['local_admin_flag'] = int

COMPLEX_ARGS = {}
COMPLEX_ARGS['permissions'] = PermissionList
COMPLEX_ARGS['roles'] = UserRoleList
COMPLEX_ARGS['metadata'] = MetadataList

LIST_ARGS = {}
# no LIST_ARGS defined
