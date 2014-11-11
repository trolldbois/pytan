import httplib
import string
import urllib
import xml.etree.ElementTree as ET

from base64 import b64encode
from .object_types.base import BaseType


class DynamicFormatter(string.Formatter):

    def get_value(self, key, args, kwargs):
        if type(key) == str:
            return kwargs.get(key, '')
        return string.Formatter.get_value(self, key, args, kwargs)

class Session(object):

    GET_OBJECT = 'GetObject'
    UPDATE_OBJECT = 'UpdateObject'

    REQUEST_BODY = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<SOAP-ENV:Body>
    <typens:tanium_soap_request xmlns:typens="urn:TaniumSOAP">
        <session>{0}</session>
        <command>{1}</command>
        <object_list>
            {2}
        </object_list>
        <options><flags>{flags}</flags><hide_errors_flag>{hide_errors_flag}</hide_errors_flag><include_answer_times_flag>{include_answer_times_flag}</include_answer_times_flag><row_counts_only_flag>{row_counts_only_flag}</row_counts_only_flag><aggregate_over_time_flag>{aggregate_over_time_flag}</aggregate_over_time_flag><most_recent_flag>{most_recent_flag}</most_recent_flag><include_hashes_flag>{include_hashes_flag}</include_hashes_flag><hide_no_results_flag>{hide_no_results_flag}</hide_no_results_flag><use_user_context_flag>{use_user_context_flag}</use_user_context_flag><script_data>{script_data}</script_data><return_lists_flag>{return_lists_flag}</return_lists_flag><return_cdata_flag>{return_cdata_flag}</return_cdata_flag><pct_done_limit>{pct_done_limit}</pct_done_limit><context_id>{context_id}</context_id><sample_frequency>{sample_frequency}</sample_frequency><sample_start>{sample_start}</sample_start><sample_count>{sample_count}</sample_count><suppress_scripts>{suppress_scripts}</suppress_scripts><suppress_object_list>{suppress_object_list}</suppress_object_list><row_start>{row_start}</row_start><row_count>{row_count}</row_count><sort_order>{sort_order}</sort_order><filter_string>{filter_string}</filter_string><filter_not_flag>{filter_not_flag}</filter_not_flag><recent_result_buckets>{recent_result_buckets}</recent_result_buckets><cache_id>{cache_id}</cache_id><cache_expiration>{cache_expiration}</cache_expiration><cache_sort_fields>{cache_sort_fields}</cache_sort_fields><include_user_details>{include_user_details}</include_user_details><include_hidden_flag>{include_hidden_flag}</include_hidden_flag><use_error_objects>{use_error_objects}</use_error_objects><use_json>{use_json}</use_json><json_pretty_print>{json_pretty_print}</json_pretty_print><cache_filters/></options>
    </typens:tanium_soap_request>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""
    def __init__(self):
        pass

    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.session_id = ''

    def authenticate(self, username, password):
        self.session_id = ''
        http = httplib.HTTPSConnection(self.server, self.port)
        try:
            http.connect()
            http.request('POST', '/auth', headers={'username': b64encode(username), 'password': b64encode(password)})
            response = http.getresponse()
            if response.status != 200:
                raise Exception(response.read())
            else:
                self.session_id = response.read()
        finally:
            http.close()

    def createGetObjectBody(self, object_type, **kwargs):
        return DynamicFormatter().format(self.REQUEST_BODY, self.session_id, self.GET_OBJECT, '<' + object_type.OBJECT_LIST_TAG + '/>', **kwargs)

    def createUpdateObjectBody(self, obj, **kwargs):
        return DynamicFormatter().format(self.REQUEST_BODY, self.session_id, self.UPDATE_OBJECT, obj.toSOAPBody(), **kwargs)

    def findAll(self, object_type, **kwargs):
        body = self.getResponse(self.createGetObjectBody(object_type, **kwargs))
        return BaseType.fromSOAPBody(body)

    def save(self, obj, **kwargs):
        body = self.createUpdateObjectBody(obj, **kwargs)
        body = self.getResponse(body)
        return BaseType.fromSOAPBody(body)

    def getResponse(self, requestBody):
        try:
            http = httplib.HTTPSConnection(self.server, self.port)
            http.connect()
            http.request('POST', '/soap', body=requestBody, headers={'Content-Type': 'text/xml'})
            response = http.getresponse()
            body = response.read()
            if response.status != 200:
                raise Exception(body)
            # a command of ERROR indicates an exception (vs 401 status, etc.)
            el = ET.fromstring(body)
            command = el.find('.//command')
            if command is not None and 'ERROR:' in command.text:
                raise Exception(command.text)
            return body
        finally:
            http.close()
