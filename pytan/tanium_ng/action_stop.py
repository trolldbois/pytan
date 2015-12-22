"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``action_stop``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class ActionStop(BaseType):

    _soap_tag = 'action_stop'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.id = None
        self.action = None
        # no list_properties defined


from .action import Action

SIMPLE_ARGS = {}
SIMPLE_ARGS['id'] = int

COMPLEX_ARGS = {}
COMPLEX_ARGS['action'] = Action

LIST_ARGS = {}
# no LIST_ARGS defined
