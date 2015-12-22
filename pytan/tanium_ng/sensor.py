"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``sensor``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class Sensor(BaseType):

    _soap_tag = 'sensor'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.id = None
        self.name = None
        self.hash = None
        self.string_count = None
        self.category = None
        self.description = None
        self.source_id = None
        self.source_hash = None
        self.parameter_definition = None
        self.value_type = None
        self.max_age_seconds = None
        self.ignore_case_flag = None
        self.exclude_from_parse_flag = None
        self.delimiter = None
        self.creation_time = None
        self.modification_time = None
        self.last_modified_by = None
        self.preview_sensor_flag = None
        self.hidden_flag = None
        self.deleted_flag = None
        self.cache_row_id = None
        self.queries = None
        self.parameters = None
        self.subcolumns = None
        self.string_hints = None
        self.metadata = None
        # no list_properties defined


from .metadata_list import MetadataList
from .parameter_list import ParameterList
from .sensor_query_list import SensorQueryList
from .sensor_subcolumn_list import SensorSubcolumnList
from .string_hint_list import StringHintList

SIMPLE_ARGS = {}
SIMPLE_ARGS['id'] = int
SIMPLE_ARGS['name'] = str
SIMPLE_ARGS['hash'] = int
SIMPLE_ARGS['string_count'] = int
SIMPLE_ARGS['category'] = str
SIMPLE_ARGS['description'] = str
SIMPLE_ARGS['source_id'] = int
SIMPLE_ARGS['source_hash'] = int
SIMPLE_ARGS['parameter_definition'] = str
SIMPLE_ARGS['value_type'] = str
SIMPLE_ARGS['max_age_seconds'] = int
SIMPLE_ARGS['ignore_case_flag'] = int
SIMPLE_ARGS['exclude_from_parse_flag'] = int
SIMPLE_ARGS['delimiter'] = str
SIMPLE_ARGS['creation_time'] = str
SIMPLE_ARGS['modification_time'] = str
SIMPLE_ARGS['last_modified_by'] = str
SIMPLE_ARGS['preview_sensor_flag'] = int
SIMPLE_ARGS['hidden_flag'] = int
SIMPLE_ARGS['deleted_flag'] = int
SIMPLE_ARGS['cache_row_id'] = int

COMPLEX_ARGS = {}
COMPLEX_ARGS['queries'] = SensorQueryList
COMPLEX_ARGS['parameters'] = ParameterList
COMPLEX_ARGS['subcolumns'] = SensorSubcolumnList
COMPLEX_ARGS['string_hints'] = StringHintList
COMPLEX_ARGS['metadata'] = MetadataList

LIST_ARGS = {}
# no LIST_ARGS defined
