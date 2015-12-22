"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``sensor``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T02-55-41Z-0400
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


from .sensor_subcolumn_list import SensorSubcolumnList
from .sensor_query_list import SensorQueryList
from .string_hint_list import StringHintList
from .parameter_list import ParameterList
from .metadata_list import MetadataList

# Simple fix for type differences for text strings: str (3.x) vs unicode (2.x)

import sys
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str  # noqa
else:
    text_type = unicode  # noqa

SIMPLE_ARGS = {}
SIMPLE_ARGS['id'] = int
SIMPLE_ARGS['name'] = text_type
SIMPLE_ARGS['hash'] = int
SIMPLE_ARGS['string_count'] = int
SIMPLE_ARGS['category'] = text_type
SIMPLE_ARGS['description'] = text_type
SIMPLE_ARGS['source_id'] = int
SIMPLE_ARGS['source_hash'] = int
SIMPLE_ARGS['parameter_definition'] = text_type
SIMPLE_ARGS['value_type'] = text_type
SIMPLE_ARGS['max_age_seconds'] = int
SIMPLE_ARGS['ignore_case_flag'] = int
SIMPLE_ARGS['exclude_from_parse_flag'] = int
SIMPLE_ARGS['delimiter'] = text_type
SIMPLE_ARGS['creation_time'] = text_type
SIMPLE_ARGS['modification_time'] = text_type
SIMPLE_ARGS['last_modified_by'] = text_type
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
