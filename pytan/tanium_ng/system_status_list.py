"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``system_status``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T02-55-41Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class SystemStatusList(BaseType):

    _soap_tag = 'system_status'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        # no simple_properties defined
        self.aggregate = None
        self.cache_info = None
        self.client_status = []


from .system_status_aggregate import SystemStatusAggregate
from .cache_info import CacheInfo
from .client_status import ClientStatus

# Simple fix for type differences for text strings: str (3.x) vs unicode (2.x)

import sys
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str  # noqa
else:
    text_type = unicode  # noqa

SIMPLE_ARGS = {}
# no SIMPLE_ARGS defined

COMPLEX_ARGS = {}
COMPLEX_ARGS['aggregate'] = SystemStatusAggregate
COMPLEX_ARGS['cache_info'] = CacheInfo

LIST_ARGS = {}
LIST_ARGS['client_status'] = ClientStatus
