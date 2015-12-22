"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``cache_info``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T02-55-41Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class CacheInfo(BaseType):

    _soap_tag = 'cache_info'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.cache_id = None
        self.page_row_count = None
        self.filtered_row_count = None
        self.cache_row_count = None
        self.expiration = None
        self.errors = None
        # no list_properties defined


from .error_list import ErrorList

# Simple fix for type differences for text strings: str (3.x) vs unicode (2.x)

import sys
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str  # noqa
else:
    text_type = unicode  # noqa

SIMPLE_ARGS = {}
SIMPLE_ARGS['cache_id'] = int
SIMPLE_ARGS['page_row_count'] = int
SIMPLE_ARGS['filtered_row_count'] = int
SIMPLE_ARGS['cache_row_count'] = int
SIMPLE_ARGS['expiration'] = text_type

COMPLEX_ARGS = {}
COMPLEX_ARGS['errors'] = ErrorList

LIST_ARGS = {}
# no LIST_ARGS defined
