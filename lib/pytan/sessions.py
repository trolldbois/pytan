# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Session classes for the :mod:`pytan` module."""
import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import os
import string
import logging
import json
import re
import threading
import time

from datetime import datetime
from base64 import b64encode

try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
path_adds = [parent_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

import pytan
from pytan.xml_clean import xml_cleaner
import requests
import taniumpy
requests.packages.urllib3.disable_warnings()

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Session(object):
    '''
    This is session object uses the requests package instead of the built in httplib library.
    This provides support for keep alive, gzip, cookies, forwarding, and a host of other features
    automatically.

    The Requests Session object allows you to persist certain parameters across requests.
    It also persists cookies across all requests made from the Session instance.
    Any requests that you make within a session will automatically reuse the appropriate connection
    '''
    REQ_SESSION = requests.Session()
    REQ_SESSION.verify = False

    XMLNS = {
        'SOAP-ENV': 'xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"',
        'xsd': 'xmlns:xsd="http://www.w3.org/2001/XMLSchema"',
        'xsi': 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        'typens': 'xmlns:typens="urn:TaniumSOAP"',
    }

    REQUEST_BODY_BASE = ("""<SOAP-ENV:Envelope {SOAP-ENV} {xsd} {xsi}>
<SOAP-ENV:Body>
  <typens:tanium_soap_request {typens}>
    <command>$command</command>
    <object_list>$object_list</object_list>
    $options
  </typens:tanium_soap_request>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>""").format(**XMLNS)

    REQUEST_BODY_TEMPLATE = string.Template(REQUEST_BODY_BASE)

    GET_OBJECT_CMD = 'GetObject'
    UPDATE_OBJECT_CMD = 'UpdateObject'
    ADD_OBJECT_CMD = 'AddObject'
    DELETE_OBJECT_CMD = 'DeleteObject'
    GET_RESULT_INFO_CMD = 'GetResultInfo'
    GET_RESULT_DATA_CMD = 'GetResultData'
    RUN_PLUGIN_CMD = 'RunPlugin'

    AUTH_RES = 'auth'
    SOAP_RES = 'soap'
    INFO_RES = 'info.json'

    AUTH_CONNECT_TIMEOUT_SEC = 5
    AUTH_RESPONSE_TIMEOUT_SEC = 15
    INFO_CONNECT_TIMEOUT_SEC = 5
    INFO_RESPONSE_TIMEOUT_SEC = 15
    SOAP_CONNECT_TIMEOUT_SEC = 15
    SOAP_RESPONSE_TIMEOUT_SEC = 540

    SOAP_REQUEST_HEADERS = {'Content-Type': 'text/xml; charset=utf-8', 'Accept-Encoding': 'gzip'}

    COMMAND_RE = re.compile(r'<command>(.*?)</command>', re.IGNORECASE | re.DOTALL)
    SESSION_RE = re.compile(r'<session>(.*?)</session>', re.IGNORECASE | re.DOTALL)
    VERSION_RE = re.compile(r'<server_version>(.*?)</server_version>', re.IGNORECASE | re.DOTALL)

    HTTP_DEBUG = False
    HTTP_RETRY_COUNT = 5
    HTTP_AUTH_RETRY = True

    SERVER_STATS = False
    SERVER_STATS_SLEEP = 5
    SERVER_STATS_TARGETS = [
        {'Version': 'Settings/Version'},
        {'Active Questions': 'Active Question Cache/Active Question Estimate'},
        {'Clients': 'Active Question Cache/Active Client Estimate'},
        {'Strings': 'String Cache/Total String Count'},
        {'Handles': 'System Performance Info/HandleCount'},
        {'Processes': 'System Performance Info/ProcessCount'},
        {'Memory Available': 'percentage(System Performance Info/PhysicalAvailable,System Performance Info/PhysicalTotal)'},
    ]

    mylog = logging.getLogger("api.session")
    authlog = logging.getLogger("api.session.auth")
    httplog = logging.getLogger("api.session.http")
    bodyhttplog = logging.getLogger("api.session.http.body")
    statslog = logging.getLogger("stats")

    def __init__(self, server, port=443, **kwargs):
        self.server = server
        self.port = port
        self.last = {}
        self.server_version = None
        self._session_id = ''
        self._username = ''
        self._password = ''
        self.qualname = "{}.{}".format(self.__class__.__module__, self.__class__.__name__)
        self.mylog = logging.getLogger(self.qualname)
        self.authlog = logging.getLogger(self.qualname + ".auth")
        self.httplog = logging.getLogger(self.qualname + ".http")
        self.bodyhttplog = logging.getLogger(self.qualname + ".http.body")
        self.HTTP_DEBUG = kwargs.get('http_debug', False)
        self._start_stats_thread()

    def __str__(self):
        class_name = self.__class__.__name__
        str_tpl = "{} to {}:{}, Authenticated: {}".format
        ret = str_tpl(class_name, self.server, self.port, self.is_auth)
        return ret

    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, value):
        if self.session_id != value:
            self._session_id = value
            self.authlog.debug("Session ID updated to: {}".format(value))

    @property
    def is_auth(self):
        auth = False
        if self._session_id:
            auth = True
        elif self._username and self._password:
            auth = True
        return auth

    def logout(self, all_session_ids=False):
        self._check_auth()

        if not self.session_id:
            self.authenticate()

        if all_session_ids:
            logout = 1
        else:
            logout = 0

        headers = {}
        headers['session'] = self.session_id
        headers['logout'] = logout

        req_args = {}
        req_args['url'] = self.AUTH_RES
        req_args['headers'] = headers

        try:
            self.http_post(retry_count=False, **req_args)
        except Exception as e:
            m = "logout exception: {}".format
            self.authlog.debug(m(e))

        if all_session_ids:
            self.authlog.debug("Successfully logged out all session ids for current user")
        else:
            self.authlog.debug("Successfully logged out current session id for current user")

        self.session_id = ''

    def authenticate(self, username=None, password=None, session_id=None, **kwargs):
        '''
        Authenticate against a Tanium Server using a username/password or a session ID

        Can request a persistent session that will last up to 1 week when authenticating
        with username and password.

        New persistent sessions may be handed out by the Tanium server when the session handed
        by this auth call is used to login with that week. The new session must be used to login,
        as no matter what persistent sessions will expire 1 week after issuance (or when logout is
        called with that session, or when logout with all_sessions=True is called for any session
        for this user)

        the way sessions get issued:

         - a POST request to /auth is issued
         - username/password supplied in headers as base64 encoded, or session is supplied in
           headers as string
         - session is returned upon successful auth
         - if there is a header "persistent=1" in the headers, a session that expires after 1 week
           will be issued if username/password was used to auth. persistent is ignored if session
           is used to auth.
         - if there is not a header "persistent=1" in the headers, a session that expires after 5
           minutes will be issued
         - if session is used before it expires, it's expiry will be extended by 5 minutes or 1
           week, depending on the type of persistence
         - while using the SOAP api, new session ID's may be returned as part of the response.
           these new session ID's should be used in lieu of the old session ID

        /auth URL
        This url is used for validating a server user's credentials. It supports a few different
        ways to authenticate and returns a SOAP session ID on success.  These sessions expire
        after 5 minutes by default if they aren't used in SOAP requests.  This expiration is
        configured with the server setting 'session_expiration_seconds'.

        Supported Authentication Methods:
         - HTTP Basic Auth (Clear Text/BASE64)
         - Username/Password/Domain Headers (Clear Text)
         - Negotiate (NTLM Only)

        NTLM is enabled by default in 6.3 or greater and requires a persistent connection until a
        session is generated.
        '''
        persistent = kwargs.get('persistent', False)
        auth_type = 'unknown'

        if session_id:
            auth_type = 'session ID'
            if persistent:
                m = (
                    "Unable to establish a persistent session when authenticating with a session!"
                ).format
                raise pytan.exceptions.AuthorizationError(m())
            self._session_id = session_id
        else:
            auth_type = 'username/password'
            if username:
                self._username = username
            if password:
                self._password = password

        if not session_id:
            if not self._username:
                raise pytan.exceptions.AuthorizationError("Must supply username")

            if not self._password:
                raise pytan.exceptions.AuthorizationError("Must supply password")

        auth_headers = {}

        if persistent:
            auth_headers['persistent'] = 1

        req_args = {}
        req_args['url'] = self.AUTH_RES
        req_args['headers'] = auth_headers
        req_args['retry_count'] = 0
        req_args['connect_timeout'] = kwargs.get('connect_timeout', self.AUTH_CONNECT_TIMEOUT_SEC)
        req_args['response_timeout'] = kwargs.get(
            'response_timeout', self.AUTH_RESPONSE_TIMEOUT_SEC
        )

        try:
            body = self.http_post(**req_args)
        except Exception as e:
            m = "Error while trying to authenticate: {}".format
            raise pytan.exceptions.AuthorizationError(m(e))

        self.session_id = body
        if persistent:
            m = (
                "Successfully authenticated and received a persistent (up to 1 week)"
                "session id using {}"
            ).format
            self.authlog.debug(m(auth_type))
        else:
            m = (
                "Successfully authenticated and received a non-persistent (up to 5 minutes) "
                "session id using {}"
            ).format
            self.authlog.debug(m(auth_type))

    def find(self, object_type, **kwargs):
        request_body = self._create_get_object_body(object_type, **kwargs)
        self.request_body = request_body
        response_body = self._get_response(request_body)
        self.response_body = response_body
        obj = taniumpy.BaseType.fromSOAPBody(response_body)
        return obj

    def save(self, obj, **kwargs):
        request_body = self._create_update_object_body(obj, **kwargs)
        self.request_body = request_body
        response_body = self._get_response(request_body)
        self.response_body = response_body
        obj = taniumpy.BaseType.fromSOAPBody(response_body)
        return obj

    def add(self, obj, **kwargs):
        request_body = self._create_add_object_body(obj, **kwargs)
        self.request_body = request_body
        response_body = self._get_response(request_body)
        self.response_body = response_body
        obj = taniumpy.BaseType.fromSOAPBody(response_body)
        return obj

    def delete(self, obj, **kwargs):
        request_body = self._create_delete_object_body(obj, **kwargs)
        self.request_body = request_body
        response_body = self._get_response(request_body)
        self.response_body = response_body
        obj = taniumpy.BaseType.fromSOAPBody(response_body)
        return obj

    def run_plugin(self, obj, **kwargs):
        request_body = self._create_run_plugin_object_body(obj, **kwargs)
        self.request_body = request_body
        response_body = self._get_response(request_body)
        self.response_body = response_body
        obj = taniumpy.BaseType.fromSOAPBody(response_body)
        return obj

    def get_result_info(self, obj, **kwargs):
        request_body = self._create_get_result_info_body(obj, **kwargs)
        self.request_body = request_body
        response_body = self._get_response(request_body)
        self.response_body = response_body
        cdata_el = self._extract_cdata_el(response_body)
        if pytan.utils.is_str(cdata_el):
            return cdata_el
        obj = taniumpy.ResultInfo.fromSOAPElement(cdata_el)
        return obj

    def get_result_data(self, obj, **kwargs):
        request_body = self._create_get_result_data_body(obj, **kwargs)
        self.request_body = request_body
        response_body = self._get_response(request_body)
        self.response_body = response_body
        cdata_el = self._extract_cdata_el(response_body)
        if pytan.utils.is_str(cdata_el):
            return cdata_el
        obj = taniumpy.ResultSet.fromSOAPElement(cdata_el)
        return obj

    def get_server_info(self, port=None, fallback_port=444, **kwargs):
        self._check_auth()

        # 6.2 /info.json is only available on soap port (default port: 444)
        # 6.5 /info.json is only available on server port (default port: 443)

        url = self.INFO_RES
        if port is None:
            port = self.port

        req_args = {}
        req_args['port'] = port
        req_args['url'] = url
        req_args['retry_count'] = 0
        req_args['connect_timeout'] = kwargs.get('connect_timeout', self.INFO_CONNECT_TIMEOUT_SEC)
        req_args['response_timeout'] = kwargs.get(
            'response_timeout', self.INFO_RESPONSE_TIMEOUT_SEC
        )

        body = {}
        server_info_pass_msgs = []
        server_info_fail_msgs = []
        ok_m = "Successfully retrieved server info from {}:{}/{}".format
        bad_m = "Failed to retrieve server info from {}:{}/{}, {}".format

        try:
            body = self.http_post(**req_args)
            body = json.loads(body)
            server_info_pass_msgs.append(ok_m(self.server, port, self.INFO_RES))
        except Exception as e:
            self.mylog.debug(bad_m(self.server, port, self.INFO_RES, e))
            server_info_fail_msgs.append(bad_m(self.server, port, self.INFO_RES, e))

        if not body:
            req_args['port'] = fallback_port
            try:
                body = self.http_post(**req_args)
                body = json.loads(body)
                server_info_pass_msgs.append(ok_m(self.server, port, self.INFO_RES))
            except Exception as e:
                self.mylog.debug(bad_m(self.server, port, self.INFO_RES, e))
                server_info_fail_msgs.append(bad_m(self.server, port, self.INFO_RES, e))

        body['diags_flat'] = self._flatten_server_info(body.get('Diagnostics', []))
        body['server_info_pass_msgs'] = server_info_pass_msgs
        body['server_info_fail_msgs'] = server_info_fail_msgs
        return body

    def get_server_version(self):
        if getattr(self, 'server_version', ''):
            return self.server_version

        server_version = "Unable to determine"

        if not getattr(self, 'server_info', {}):
            self.server_info = self.get_server_info()

        if not getattr(self, 'server_info', {}):
            return server_version

        version = None
        try:
            version = self.server_info['diags_flat']['Settings']['Version']
        except:
            m = "Unable to find Version key in Settings: {}".format
            self.mylog.warning(m(self.server_info['diags_flat']))

        if version:
            server_version = version
        else:
            m = "Unable to find Version key in Settings: {}".format
            self.mylog.warning(m(self.server_info['diags_flat']))

        if server_version:
            self.server_version = server_version

        return server_version

    def get_server_stats(self):
        si = self.get_server_info()
        try:
            diags = si['diags_flat']
        except:
            pass

        stats_resolved = [self._find_stat_target(t, diags) for t in self.SERVER_STATS_TARGETS]
        stats_text = ", ".join(["{}: {}".format(*i.items()[0]) for i in stats_resolved])
        return stats_text

    def enable_stats_loop(self, sleep=None):
        self.SERVER_STATS = True
        if isinstance(sleep, int):
            self.SERVER_STATS_SLEEP = sleep

    def disable_stats_loop(self, sleep=None):
        self.SERVER_STATS = False
        if isinstance(sleep, int):
            self.SERVER_STATS_SLEEP = sleep

    def http_get(self, url, **kwargs):
        '''
        This is an authenticated HTTP get method, added for getting server side exports
        It will always forcibly use the authentication credentials that are stored in the
        current object.
        '''
        self._check_auth()

        headers = kwargs.get('headers', {})
        headers = self._replace_auth(headers)

        req_args = {}
        req_args['host'] = kwargs.get('server', self.server)
        req_args['port'] = kwargs.get('port', self.port)
        req_args['url'] = url
        req_args['headers'] = headers
        req_args['connect_timeout'] = kwargs.get('connect_timeout', self.SOAP_CONNECT_TIMEOUT_SEC)
        req_args['response_timeout'] = kwargs.get(
            'response_timeout', self.SOAP_RESPONSE_TIMEOUT_SEC
        )
        req_args['debug'] = kwargs.get('debug', self.HTTP_DEBUG)

        auth_retry = kwargs.get('auth_retry', self.HTTP_AUTH_RETRY)
        retry_count = kwargs.get('retry_count', self.HTTP_RETRY_COUNT)

        if not retry_count or type(retry_count) != int:
            retry_count = 0

        current_try = 1

        while True:
            try:
                body = self._http_get(**req_args)
                break
            except pytan.exceptions.AuthorizationError:
                if self._session_id and auth_retry:
                    self._session_id = ''
                    self.authenticate()
                    body = self.http_get(auth_retry=False, **kwargs)
                else:
                    raise
            except Exception as e:
                if retry_count == 0:
                    raise
                m = "http_get failed on attempt {} out of {}: {}".format
                self.mylog.warning(m(current_try, retry_count, e))
                if current_try == retry_count:
                    raise
                current_try += 1

        return body

    def http_post(self, **kwargs):
        '''
        This is an authenticated HTTP post method. It will always forcibly use the authentication
        credentials that are stored in the current object.

        TODO: add params
        '''
        self._check_auth()

        headers = kwargs.get('headers', {})
        headers = self._replace_auth(headers)

        req_args = {}
        req_args['host'] = kwargs.get('server', self.server)
        req_args['port'] = kwargs.get('port', self.port)
        req_args['url'] = kwargs.get('url', self.SOAP_RES)
        req_args['headers'] = headers
        req_args['body'] = kwargs.get('body', None)
        req_args['connect_timeout'] = kwargs.get('connect_timeout', self.SOAP_CONNECT_TIMEOUT_SEC)
        req_args['response_timeout'] = kwargs.get(
            'response_timeout', self.SOAP_RESPONSE_TIMEOUT_SEC
        )
        req_args['debug'] = kwargs.get('debug', self.HTTP_DEBUG)

        auth_retry = kwargs.get('auth_retry', self.HTTP_AUTH_RETRY)
        retry_count = kwargs.get('retry_count', self.HTTP_RETRY_COUNT)

        if not retry_count or type(retry_count) != int:
            retry_count = 0

        current_try = 1

        while True:
            try:
                body = self._http_post(**req_args)
                break
            except pytan.exceptions.AuthorizationError:
                if self._session_id and auth_retry:
                    self._session_id = ''
                    self.authenticate()
                    body = self.http_post(auth_retry=False, **kwargs)
                else:
                    raise
            except Exception as e:
                if retry_count == 0:
                    raise
                m = "http_post failed on attempt {} out of {}: {}".format
                self.mylog.warning(m(current_try, retry_count, e))
                if current_try == retry_count:
                    raise
                current_try += 1

        return body

    def _replace_auth(self, headers):
        for k in dict(headers):
            if k in ['username', 'password', 'session']:
                self.authlog.debug("Removing header {!r}".format(k))
                headers.pop(k)

        if self._session_id:
            headers['session'] = self._session_id
            self.authlog.debug("Using session ID for authentication headers")

        elif self._username and self._password:
            headers['username'] = b64encode(self._username)
            headers['password'] = b64encode(self._password)
            self.authlog.debug("Using Username/Password for authentication headers")
        return headers

    def _full_url(self, url, **kwargs):
        host = kwargs.get('host', self.server)
        port = kwargs.get('port', self.port)
        full_url = "https://{0}:{1}/{2}".format(host, port, url)
        return full_url

    def _http_get(self, host, port, url, headers=None, connect_timeout=15,
                  response_timeout=180, debug=False):

        full_url = self._full_url(host=host, port=port, url=url)

        clean_headers = dict(headers or {})
        if 'password' in clean_headers:
            clean_headers['password'] = '**PASSWORD**'

        req_args = {}
        req_args['headers'] = headers
        req_args['timeout'] = (connect_timeout, response_timeout)

        self.httplog.debug("HTTP request: GET to {}".format(full_url))
        self.httplog.debug("HTTP request: headers: {}".format(clean_headers))

        try:
            response = self.REQ_SESSION.get(full_url, **req_args)
        except Exception as e:
            m = "HTTP response: GET request to {!r} failed: {}".format
            raise pytan.exceptions.HttpError(m(full_url, e))

        self.REQ_RESPONSE = response
        response_body = response.text
        response_headers = response.headers

        m = "HTTP response: from {!r} len:{}, status:{} {}, body type: {}".format

        self.httplog.debug(m(
            full_url,
            len(response_body),
            response.status_code,
            response.reason,
            type(response_body),
        ))

        self.httplog.debug("HTTP response: headers: {}".format(response_headers))

        auth_fail_codes = [401, 403]
        if response.status_code in auth_fail_codes:
            m = "HTTP response: GET request to {!r} returned code: {}, body: {}".format
            raise pytan.exceptions.AuthorizationError(m(
                full_url, response.status_code, response_body))

        if not response.ok:
            m = "HTTP response: GET request to {!r} returned code: {}, body: {}".format
            raise pytan.exceptions.HttpError(m(full_url, response.status_code, response_body))

        self.bodyhttplog.debug("HTTP response: body:\n{}".format(response_body))

        return response_body

    def _http_post(self, host, port, url, body=None, headers=None, connect_timeout=15,
                   response_timeout=180, debug=False):

        full_url = self._full_url(host=host, port=port, url=url)

        clean_headers = dict(headers or {})
        if 'password' in clean_headers:
            clean_headers['password'] = '**PASSWORD**'

        req_args = {}
        req_args['headers'] = headers
        req_args['data'] = body
        req_args['timeout'] = (connect_timeout, response_timeout)

        self.httplog.debug("HTTP request: POST to {}".format(full_url))
        self.httplog.debug("HTTP request: headers: {}".format(clean_headers))
        self.bodyhttplog.debug("HTTP request: body:\n{}".format(body))

        try:
            response = self.REQ_SESSION.post(full_url, **req_args)
        except Exception as e:
            m = "HTTP response: POST request to {!r} failed: {}".format
            raise pytan.exceptions.HttpError(m(full_url, e))

        self.REQ_RESPONSE = response
        response_body = xml_cleaner(response.text)
        response_headers = response.headers

        m = "HTTP response: from {!r} len:{}, status:{} {}, body type: {}".format

        self.httplog.debug(m(
            full_url,
            len(response_body),
            response.status_code,
            response.reason,
            type(response_body),
        ))

        self.httplog.debug("HTTP response: headers: {}".format(response_headers))

        auth_fail_codes = [401, 403]
        if response.status_code in auth_fail_codes:
            m = "HTTP response: POST request to {!r} returned code: {}, body: {}".format
            raise pytan.exceptions.AuthorizationError(m(
                full_url, response.status_code, response_body))

        if not response_body:
            m = "HTTP response: POST request to {!r} returned empty body".format
            raise pytan.exceptions.HttpError(m(full_url))

        if not response.ok:
            m = "HTTP response: POST request to {!r} returned code: {}, body: {}".format
            raise pytan.exceptions.HttpError(m(full_url, response.status_code, response_body))

        self.bodyhttplog.debug("HTTP response: body:\n{}".format(response_body))

        return response_body

    def _start_stats_thread(self):
        self.stats_thread = threading.Thread(target=self._stats_loop)
        self.stats_thread.daemon = True
        self.stats_thread.start()

    def _stats_loop(self):
        while True:
            if self.SERVER_STATS:
                self.statslog.warning(self.get_server_stats())
            time.sleep(self.SERVER_STATS_SLEEP)

    def _flatten_server_info(self, structure):
        flattened = structure
        if isinstance(structure, dict):
            for k, v in flattened.iteritems():
                flattened[k] = self._flatten_server_info(v)
        elif isinstance(structure, (tuple, list)):
            if all([isinstance(x, dict) for x in structure]):
                flattened = {}
                [flattened.update(self._flatten_server_info(i)) for i in structure]
        return flattened

    def _get_percentage(self, part, whole):
        f = 100 * float(part) / float(whole)
        return "{0:.2f}%".format(f)

    def _find_stat_target(self, target, diags):
        try:
            label, search_path = target.items()[0]
        except Exception as e:
            label = "Parse Failure"
            result = "Unable to parse stat target: {}, exception: {}".format(target, e)
            return {label: result}

        if search_path.startswith('percentage('):
            points = search_path.lstrip('percentage(').rstrip(')')
            points = [self._resolve_stat_target(p, diags) for p in points.split(',')]
            try:
                result = self._get_percentage(points[0], points[1])
            except:
                result = ', '.join(points)
        else:
            result = self._resolve_stat_target(search_path, diags)
        return {label: result}

    def _resolve_stat_target(self, search_path, diags):
        try:
            for i in search_path.split('/'):
                diags = diags.get(i)
        except Exception as e:
            return "Unable to find diagnostic: {}, exception: {}".format(search_path, e)
        return diags

    def _build_body(self, command, object_list, **kwargs):
        options_obj = taniumpy.Options()
        for k, v in kwargs.iteritems():
            if hasattr(options_obj, k):
                setattr(options_obj, k, v)
            else:
                m = "Ignoring argument {!r} for options list, not a valid attribute".format
                self.mylog.debug(m(k))

        options = options_obj.toSOAPBody(minimal=True)
        body = self.REQUEST_BODY_TEMPLATE.substitute(
            command=command,
            object_list=object_list,
            options=options,
        )
        return body

    def _create_run_plugin_object_body(self, obj, **kwargs):
        object_list = obj.toSOAPBody(minimal=True)
        obj_body = self._build_body(self.RUN_PLUGIN_CMD, object_list, **kwargs)
        return obj_body

    def _create_add_object_body(self, obj, **kwargs):
        object_list = obj.toSOAPBody(minimal=True)
        obj_body = self._build_body(self.ADD_OBJECT_CMD, object_list, **kwargs)
        return obj_body

    def _create_delete_object_body(self, obj, **kwargs):
        object_list = obj.toSOAPBody(minimal=True)
        obj_body = self._build_body(self.DELETE_OBJECT_CMD, object_list, **kwargs)
        return obj_body

    def _create_get_result_info_body(self, obj, **kwargs):
        object_list = obj.toSOAPBody(minimal=True)
        obj_body = self._build_body(self.GET_RESULT_INFO_CMD, object_list, **kwargs)
        return obj_body

    def _create_get_result_data_body(self, obj, **kwargs):
        object_list = obj.toSOAPBody(minimal=True)
        obj_body = self._build_body(self.GET_RESULT_DATA_CMD, object_list, **kwargs)
        return obj_body

    def _create_get_object_body(self, object_or_type, **kwargs):
        if isinstance(object_or_type, taniumpy.BaseType):
            object_list = object_or_type.toSOAPBody(minimal=True)
        else:
            object_list = '<{}/>'.format(object_or_type._soap_tag)

        obj_body = self._build_body(self.GET_OBJECT_CMD, object_list, **kwargs)
        return obj_body

    def _create_update_object_body(self, obj, **kwargs):
        object_list = obj.toSOAPBody(minimal=True)
        obj_body = self._build_body(self.UPDATE_OBJECT_CMD, object_list, **kwargs)
        return obj_body

    def _check_auth(self):
        if not self.is_auth:
            class_name = self.__class__.__name__
            err = "Not yet authenticated, use {}.authenticate()!".format
            raise pytan.exceptions.AuthorizationError(err(class_name))

    def _parse_response_for_regex(self, body, regex, fail=True):
        # using regex is faster than ET chewing the body in and out
        # this matters on LARGE return bodies
        ret = regex.search(body)
        if not ret and fail:
            m = "Unable to find {} in body: {}".format
            raise Exception(m(regex.pattern, body))
        elif ret:
            ret = str(ret.groups()[0].strip())
        return ret

    def _extract_export_id(self, el):
        ret = None
        # if there is an export_id in the response_body, return just results of that
        export_id_el = el.find('.//export_id')
        if export_id_el is not None and export_id_el.text:
            ret = export_id_el.text
        return ret

    def _extract_cdata_el(self, response_body):
        el = ET.fromstring(response_body)

        # find the ResultXML node
        resultxml_el = el.find('.//ResultXML')

        if resultxml_el is None:
            # if there is an export_id node, return the contents of that
            export_id = self._extract_export_id(el)
            if export_id:
                return export_id

            m = "Unable to find ResultXML element in XML response: {}".format
            raise pytan.exceptions.AuthorizationError(m(response_body))

        resultxml_text = resultxml_el.text

        if not resultxml_text:
            # if there is an export_id node, return the contents of that
            export_id = self._extract_export_id(el)
            if export_id:
                return export_id

            m = "Empty ResultXML element in XML response: {}".format
            raise pytan.exceptions.AuthorizationError(m(response_body))

        # parse the ResultXML node into it's own element
        cdata_el = ET.fromstring(resultxml_text)
        return cdata_el

    def _get_response(self, request_body, **kwargs):
        retry_auth = kwargs.get('retry_auth', True)

        self._check_auth()

        self.last = {}

        request_command = self._parse_response_for_regex(request_body, self.COMMAND_RE)
        self.last['request_command'] = request_command

        req_args = {}
        req_args['body'] = request_body
        req_args['headers'] = dict(self.SOAP_REQUEST_HEADERS)
        req_args['connect_timeout'] = kwargs.get('connect_timeout', self.SOAP_CONNECT_TIMEOUT_SEC)
        req_args['response_timeout'] = kwargs.get(
            'response_timeout', self.SOAP_RESPONSE_TIMEOUT_SEC
        )

        if 'retry_count' in kwargs:
            req_args['retry_count'] = kwargs['retry_count']

        self.last['request_args'] = req_args

        sent = datetime.utcnow()
        self.last['sent'] = sent

        response_body = self.http_post(**req_args)

        received = datetime.utcnow()
        self.last['received'] = received

        elapsed = received - sent
        self.last['elapsed'] = elapsed

        m = "HTTP Response: Timing info -- SENT: {}, RECEIVED: {}, ELAPSED: {}".format
        self.mylog.debug(m(sent, received, elapsed))

        response_command = self._parse_response_for_regex(response_body, self.COMMAND_RE)
        self.last['response_command'] = response_command

        if 'forbidden' in response_command.lower():
            if retry_auth:
                m = "Last request was denied, re-authenticating with user/pass".format
                self.authlog.debug(m())
                # we may have hit the 5 minute expiration for session_id, empty out session ID,
                # re-authenticate, then retry request
                self._session_id = ''
                self.authenticate()

                # re-issue the request
                response_body = self._get_response(request_body, retry_auth=False, **kwargs)
            else:
                m = "Access denied after re-authenticating! Server response: {}".format
                raise pytan.exceptions.AuthorizationError(m(response_command))

        elif response_command != request_command:
            response_prunes = [
                '\n',
                'XML Parse Error: ',
                'SOAPProcessing Exception: class ',
                'ERROR: 400 Bad Request'
            ]
            for p in response_prunes:
                response_command = response_command.replace(p, '').strip()

            m = "Response command {} does not match request command {}".format
            raise pytan.exceptions.BadResponseError(m(response_command, request_command))

        # update session_id, in case new one issued
        self.session_id = self._parse_response_for_regex(response_body, self.SESSION_RE)

        # check to see if server_version set in response (6.5+ only)
        server_version = self._parse_response_for_regex(response_body, self.VERSION_RE, False)
        if server_version:
            self.server_version = server_version

        return response_body
