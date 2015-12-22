"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``version``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class VersionAggregate(BaseType):

    _soap_tag = 'version'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.version_string = None
        self.count = None
        self.filtered = None
        # no complex_properties defined
        # no list_properties defined


# no extra imports used

SIMPLE_ARGS = {}
SIMPLE_ARGS['version_string'] = str
SIMPLE_ARGS['count'] = int
SIMPLE_ARGS['filtered'] = int

COMPLEX_ARGS = {}
# no COMPLEX_ARGS defined

LIST_ARGS = {}
# no LIST_ARGS defined
