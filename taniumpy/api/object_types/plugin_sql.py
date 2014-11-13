
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class PluginSql(BaseType):

    _OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='plugin_sql',
            simple_properties={'rows_affected': int,
                        'result_count': int},
            complex_properties={'columns': PluginSqlColumn},
            list_properties={'result_row': PluginSqlResult},
        )
        self.rows_affected = None
        self.result_count = None
        self.columns = None
        self.result_row = []

from plugin_sql_column import PluginSqlColumn
from plugin_sql_result import PluginSqlResult

