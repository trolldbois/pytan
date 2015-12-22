"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``client_status``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T02-55-41Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class ClientStatus(BaseType):

    _soap_tag = 'client_status'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.host_name = None
        self.computer_id = None
        self.ipaddress_client = None
        self.ipaddress_server = None
        self.protocol_version = None
        self.full_version = None
        self.last_registration = None
        self.send_state = None
        self.receive_state = None
        self.status = None
        self.port_number = None
        self.public_key_valid = None
        self.cache_row_id = None
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
SIMPLE_ARGS['host_name'] = text_type
SIMPLE_ARGS['computer_id'] = text_type
SIMPLE_ARGS['ipaddress_client'] = text_type
SIMPLE_ARGS['ipaddress_server'] = text_type
SIMPLE_ARGS['protocol_version'] = int
SIMPLE_ARGS['full_version'] = text_type
SIMPLE_ARGS['last_registration'] = text_type
SIMPLE_ARGS['send_state'] = text_type
SIMPLE_ARGS['receive_state'] = text_type
SIMPLE_ARGS['status'] = text_type
SIMPLE_ARGS['port_number'] = int
SIMPLE_ARGS['public_key_valid'] = int
SIMPLE_ARGS['cache_row_id'] = int

COMPLEX_ARGS = {}
# no COMPLEX_ARGS defined

LIST_ARGS = {}
# no LIST_ARGS defined
