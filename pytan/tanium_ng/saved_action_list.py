"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``saved_actions``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class SavedActionList(BaseType):

    _soap_tag = 'saved_actions'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        # no simple_properties defined
        self.cache_info = None
        self.saved_action = []


from .saved_action import SavedAction
from .cache_info import CacheInfo

SIMPLE_ARGS = {}
# no SIMPLE_ARGS defined

COMPLEX_ARGS = {}
COMPLEX_ARGS['cache_info'] = CacheInfo

LIST_ARGS = {}
LIST_ARGS['saved_action'] = SavedAction
