"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``aggregate``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class SystemStatusAggregate(BaseType):

    _soap_tag = 'aggregate'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.send_forward_count = None
        self.send_backward_count = None
        self.send_none_count = None
        self.send_ok_count = None
        self.receive_forward_count = None
        self.receive_backward_count = None
        self.receive_none_count = None
        self.receive_ok_count = None
        self.slowlink_count = None
        self.blocked_count = None
        self.leader_count = None
        self.normal_count = None
        self.versions = None
        # no list_properties defined


from .version_aggregate_list import VersionAggregateList

SIMPLE_ARGS = {}
SIMPLE_ARGS['send_forward_count'] = int
SIMPLE_ARGS['send_backward_count'] = int
SIMPLE_ARGS['send_none_count'] = int
SIMPLE_ARGS['send_ok_count'] = int
SIMPLE_ARGS['receive_forward_count'] = int
SIMPLE_ARGS['receive_backward_count'] = int
SIMPLE_ARGS['receive_none_count'] = int
SIMPLE_ARGS['receive_ok_count'] = int
SIMPLE_ARGS['slowlink_count'] = int
SIMPLE_ARGS['blocked_count'] = int
SIMPLE_ARGS['leader_count'] = int
SIMPLE_ARGS['normal_count'] = int

COMPLEX_ARGS = {}
COMPLEX_ARGS['versions'] = VersionAggregateList

LIST_ARGS = {}
# no LIST_ARGS defined
