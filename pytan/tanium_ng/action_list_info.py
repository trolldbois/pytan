"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``info``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T02-55-41Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType

# Simple fix for type differences for text strings: str (3.x) vs unicode (2.x)
import sys
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str  # noqa
else:
    text_type = unicode  # noqa


class ActionListInfo(BaseType):

    _soap_tag = 'info'

    _SIMPLE_ARGS = {}
    _SIMPLE_ARGS['highest_id'] = int
    _SIMPLE_ARGS['total_count'] = int

    _COMPLEX_ARGS = {}
    # no COMPLEX_ARGS defined

    _LIST_ARGS = {}
    # no LIST_ARGS defined

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties=self._SIMPLE_ARGS,
            complex_properties=self._COMPLEX_ARGS,
            list_properties=self._LIST_ARGS,
        )
        self.highest_id = None
        self.total_count = None
        # no complex_properties defined
        # no list_properties defined
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


# no extra imports used
