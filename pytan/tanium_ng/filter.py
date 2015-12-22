"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``filter``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T02-55-41Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class Filter(BaseType):

    _soap_tag = 'filter'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.id = None
        self.operator = None
        self.value_type = None
        self.value = None
        self.not_flag = None
        self.max_age_seconds = None
        self.ignore_case_flag = None
        self.all_values_flag = None
        self.substring_flag = None
        self.substring_start = None
        self.substring_length = None
        self.delimiter = None
        self.delimiter_index = None
        self.utf8_flag = None
        self.aggregation = None
        self.all_times_flag = None
        self.start_time = None
        self.end_time = None
        self.sensor = None
        # no list_properties defined


from .sensor import Sensor

# Simple fix for type differences for text strings: str (3.x) vs unicode (2.x)

import sys
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str  # noqa
else:
    text_type = unicode  # noqa

SIMPLE_ARGS = {}
SIMPLE_ARGS['id'] = int
SIMPLE_ARGS['operator'] = text_type
SIMPLE_ARGS['value_type'] = text_type
SIMPLE_ARGS['value'] = text_type
SIMPLE_ARGS['not_flag'] = int
SIMPLE_ARGS['max_age_seconds'] = int
SIMPLE_ARGS['ignore_case_flag'] = int
SIMPLE_ARGS['all_values_flag'] = int
SIMPLE_ARGS['substring_flag'] = int
SIMPLE_ARGS['substring_start'] = int
SIMPLE_ARGS['substring_length'] = int
SIMPLE_ARGS['delimiter'] = text_type
SIMPLE_ARGS['delimiter_index'] = int
SIMPLE_ARGS['utf8_flag'] = int
SIMPLE_ARGS['aggregation'] = text_type
SIMPLE_ARGS['all_times_flag'] = int
SIMPLE_ARGS['start_time'] = text_type
SIMPLE_ARGS['end_time'] = text_type

COMPLEX_ARGS = {}
COMPLEX_ARGS['sensor'] = Sensor

LIST_ARGS = {}
# no LIST_ARGS defined
