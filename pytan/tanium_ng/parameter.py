"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``parameter``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class Parameter(BaseType):

    _soap_tag = 'parameter'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.key = None
        self.value = None
        self.type = None
        # no complex_properties defined
        # no list_properties defined


# no extra imports used

SIMPLE_ARGS = {}
SIMPLE_ARGS['key'] = str
SIMPLE_ARGS['value'] = str
SIMPLE_ARGS['type'] = int

COMPLEX_ARGS = {}
# no COMPLEX_ARGS defined

LIST_ARGS = {}
# no LIST_ARGS defined
