"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``soap_error``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T02-55-41Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class SoapError(BaseType):

    _soap_tag = 'soap_error'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.object_name = None
        self.exception_name = None
        self.context = None
        self.object_request = None
        # no complex_properties defined
        # no list_properties defined


# no extra imports used

# Simple fix for type differences for text strings: str (3.x) vs unicode (2.x)

import sys
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str  # noqa
else:
    text_type = unicode  # noqa

SIMPLE_ARGS = {}
SIMPLE_ARGS['object_name'] = text_type
SIMPLE_ARGS['exception_name'] = text_type
SIMPLE_ARGS['context'] = text_type
SIMPLE_ARGS['object_request'] = text_type

COMPLEX_ARGS = {}
# no COMPLEX_ARGS defined

LIST_ARGS = {}
# no LIST_ARGS defined
