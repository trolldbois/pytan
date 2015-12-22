"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``sql_response``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T02-55-41Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class PluginSql(BaseType):

    _soap_tag = 'sql_response'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.rows_affected = None
        self.result_count = None
        self.columns = None
        self.result_row = []


from .plugin_sql_column import PluginSqlColumn
from .plugin_sql_result import PluginSqlResult

# Simple fix for type differences for text strings: str (3.x) vs unicode (2.x)

import sys
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str  # noqa
else:
    text_type = unicode  # noqa

SIMPLE_ARGS = {}
SIMPLE_ARGS['rows_affected'] = int
SIMPLE_ARGS['result_count'] = int

COMPLEX_ARGS = {}
COMPLEX_ARGS['columns'] = PluginSqlColumn

LIST_ARGS = {}
LIST_ARGS['result_row'] = PluginSqlResult
