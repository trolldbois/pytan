"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``group``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class Group(BaseType):

    _soap_tag = 'group'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.id = None
        self.name = None
        self.text = None
        self.and_flag = None
        self.not_flag = None
        self.type = None
        self.source_id = None
        self.deleted_flag = None
        self.sub_groups = None
        self.filters = None
        self.parameters = None
        # no list_properties defined


from .filter_list import FilterList
from .parameter_list import ParameterList
from .group_list import GroupList

SIMPLE_ARGS = {}
SIMPLE_ARGS['id'] = int
SIMPLE_ARGS['name'] = str
SIMPLE_ARGS['text'] = str
SIMPLE_ARGS['and_flag'] = int
SIMPLE_ARGS['not_flag'] = int
SIMPLE_ARGS['type'] = int
SIMPLE_ARGS['source_id'] = int
SIMPLE_ARGS['deleted_flag'] = int

COMPLEX_ARGS = {}
COMPLEX_ARGS['sub_groups'] = GroupList
COMPLEX_ARGS['filters'] = FilterList
COMPLEX_ARGS['parameters'] = ParameterList

LIST_ARGS = {}
# no LIST_ARGS defined
