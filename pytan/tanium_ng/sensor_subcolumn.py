"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``subcolumn``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class SensorSubcolumn(BaseType):

    _soap_tag = 'subcolumn'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.name = None
        self.index = None
        self.value_type = None
        self.ignore_case_flag = None
        self.hidden_flag = None
        self.exclude_from_parse_flag = None
        # no complex_properties defined
        # no list_properties defined


# no extra imports used

SIMPLE_ARGS = {}
SIMPLE_ARGS['name'] = str
SIMPLE_ARGS['index'] = int
SIMPLE_ARGS['value_type'] = str
SIMPLE_ARGS['ignore_case_flag'] = int
SIMPLE_ARGS['hidden_flag'] = int
SIMPLE_ARGS['exclude_from_parse_flag'] = int

COMPLEX_ARGS = {}
# no COMPLEX_ARGS defined

LIST_ARGS = {}
# no LIST_ARGS defined
