"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``system_setting``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class SystemSetting(BaseType):

    _soap_tag = 'system_setting'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.id = None
        self.name = None
        self.value = None
        self.default_value = None
        self.value_type = None
        self.setting_type = None
        self.hidden_flag = None
        self.read_only_flag = None
        self.cache_row_id = None
        self.audit_data = None
        self.metadata = None
        # no list_properties defined


from .metadata_list import MetadataList
from .audit_data import AuditData

SIMPLE_ARGS = {}
SIMPLE_ARGS['id'] = int
SIMPLE_ARGS['name'] = str
SIMPLE_ARGS['value'] = str
SIMPLE_ARGS['default_value'] = str
SIMPLE_ARGS['value_type'] = str
SIMPLE_ARGS['setting_type'] = str
SIMPLE_ARGS['hidden_flag'] = int
SIMPLE_ARGS['read_only_flag'] = int
SIMPLE_ARGS['cache_row_id'] = int

COMPLEX_ARGS = {}
COMPLEX_ARGS['audit_data'] = AuditData
COMPLEX_ARGS['metadata'] = MetadataList

LIST_ARGS = {}
# no LIST_ARGS defined
