"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``audit_data``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class AuditData(BaseType):

    _soap_tag = 'audit_data'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.creation_time = None
        self.modification_time = None
        self.last_modified_by = None
        # no complex_properties defined
        # no list_properties defined


# no extra imports used

SIMPLE_ARGS = {}
SIMPLE_ARGS['creation_time'] = str
SIMPLE_ARGS['modification_time'] = str
SIMPLE_ARGS['last_modified_by'] = str

COMPLEX_ARGS = {}
# no COMPLEX_ARGS defined

LIST_ARGS = {}
# no LIST_ARGS defined
