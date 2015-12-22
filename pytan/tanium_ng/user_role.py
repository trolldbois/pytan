"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``role``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class UserRole(BaseType):

    _soap_tag = 'role'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.id = None
        self.name = None
        self.description = None
        self.permissions = None
        # no list_properties defined


from .permission_list import PermissionList

SIMPLE_ARGS = {}
SIMPLE_ARGS['id'] = int
SIMPLE_ARGS['name'] = str
SIMPLE_ARGS['description'] = str

COMPLEX_ARGS = {}
COMPLEX_ARGS['permissions'] = PermissionList

LIST_ARGS = {}
# no LIST_ARGS defined
