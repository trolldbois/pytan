"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``options``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class Options(BaseType):

    _soap_tag = 'options'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.export_flag = None
        self.export_format = None
        self.export_leading_text = None
        self.export_trailing_text = None
        self.flags = None
        self.hide_errors_flag = None
        self.include_answer_times_flag = None
        self.row_counts_only_flag = None
        self.aggregate_over_time_flag = None
        self.most_recent_flag = None
        self.include_hashes_flag = None
        self.hide_no_results_flag = None
        self.use_user_context_flag = None
        self.script_data = None
        self.return_lists_flag = None
        self.return_cdata_flag = None
        self.pct_done_limit = None
        self.context_id = None
        self.sample_frequency = None
        self.sample_start = None
        self.sample_count = None
        self.suppress_scripts = None
        self.suppress_object_list = None
        self.row_start = None
        self.row_count = None
        self.sort_order = None
        self.filter_string = None
        self.filter_not_flag = None
        self.recent_result_buckets = None
        self.cache_id = None
        self.cache_expiration = None
        self.cache_sort_fields = None
        self.include_user_details = None
        self.include_hidden_flag = None
        self.use_error_objects = None
        self.use_json = None
        self.json_pretty_print = None
        self.cache_filters = None
        # no list_properties defined


from .cache_filter_list import CacheFilterList

SIMPLE_ARGS = {}
SIMPLE_ARGS['export_flag'] = int
SIMPLE_ARGS['export_format'] = int
SIMPLE_ARGS['export_leading_text'] = str
SIMPLE_ARGS['export_trailing_text'] = str
SIMPLE_ARGS['flags'] = int
SIMPLE_ARGS['hide_errors_flag'] = int
SIMPLE_ARGS['include_answer_times_flag'] = int
SIMPLE_ARGS['row_counts_only_flag'] = int
SIMPLE_ARGS['aggregate_over_time_flag'] = int
SIMPLE_ARGS['most_recent_flag'] = int
SIMPLE_ARGS['include_hashes_flag'] = int
SIMPLE_ARGS['hide_no_results_flag'] = int
SIMPLE_ARGS['use_user_context_flag'] = int
SIMPLE_ARGS['script_data'] = str
SIMPLE_ARGS['return_lists_flag'] = int
SIMPLE_ARGS['return_cdata_flag'] = int
SIMPLE_ARGS['pct_done_limit'] = int
SIMPLE_ARGS['context_id'] = int
SIMPLE_ARGS['sample_frequency'] = int
SIMPLE_ARGS['sample_start'] = int
SIMPLE_ARGS['sample_count'] = int
SIMPLE_ARGS['suppress_scripts'] = int
SIMPLE_ARGS['suppress_object_list'] = int
SIMPLE_ARGS['row_start'] = int
SIMPLE_ARGS['row_count'] = int
SIMPLE_ARGS['sort_order'] = str
SIMPLE_ARGS['filter_string'] = str
SIMPLE_ARGS['filter_not_flag'] = int
SIMPLE_ARGS['recent_result_buckets'] = str
SIMPLE_ARGS['cache_id'] = int
SIMPLE_ARGS['cache_expiration'] = int
SIMPLE_ARGS['cache_sort_fields'] = str
SIMPLE_ARGS['include_user_details'] = int
SIMPLE_ARGS['include_hidden_flag'] = int
SIMPLE_ARGS['use_error_objects'] = int
SIMPLE_ARGS['use_json'] = int
SIMPLE_ARGS['json_pretty_print'] = int

COMPLEX_ARGS = {}
COMPLEX_ARGS['cache_filters'] = CacheFilterList

LIST_ARGS = {}
# no LIST_ARGS defined
