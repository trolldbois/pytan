"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``parse_result``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class ParseResult(BaseType):

    _soap_tag = 'parse_result'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.id = None
        self.parameter_definition = None
        self.parameters = None
        # no list_properties defined


from .parameter_list import ParameterList

SIMPLE_ARGS = {}
SIMPLE_ARGS['id'] = int
SIMPLE_ARGS['parameter_definition'] = str

COMPLEX_ARGS = {}
COMPLEX_ARGS['parameters'] = ParameterList

LIST_ARGS = {}
# no LIST_ARGS defined
