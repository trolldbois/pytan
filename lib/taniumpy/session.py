# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Session handler for Tanium API'''

import os
import httplib
import string

try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

import logging
import json
# needed for python 2.7.9 to revert SSL verification
import ssl
# 1.04: added for xml_fix()
import re
from datetime import datetime
# needed to support gzip encoding
from cStringIO import StringIO
import gzip

from base64 import b64encode
from .object_types.base import BaseType
from .object_types.result_info import ResultInfo
from .object_types.result_set import ResultSet

# fix for UTF encoding
import sys
reload(sys)
sys.setdefaultencoding('latin-1')

# 1.0.4: added for xml_fix(), declare a regex that identifies invalid characters in unicode
invalid_xml = re.compile(u'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]')

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
mylog = logging.getLogger("api.session")
authlog = logging.getLogger("api.session.auth")
httplog = logging.getLogger("api.session.http")
bodyhttplog = logging.getLogger("api.session.http.body")

# to support py2exe compiled scripts
my_dir = my_dir.replace('\\library.zip\\taniumpy', '')
request_body_template_file = os.path.join(my_dir, 'request_body_template.xml')


class NoLogging(object):

    count = 0

    """Disable logging while executing code block"""
    def __enter__(self):
        NoLogging.count += 1
        logging.disable(logging.CRITICAL)

    def __exit__(self, exc_type, exc_value, traceback):
        NoLogging.count -= 1
        if NoLogging.count == 0:
            logging.disable(logging.NOTSET)


def nologging(func):
    """decorator to disable logging on a function"""
    def func_wrapper(*args, **kwargs):
        with NoLogging():
            return func(*args, **kwargs)
    return func_wrapper


class HttpError(Exception):
    pass


class AuthorizationError(Exception):
    pass


class BadResponseError(Exception):
    pass


def load_file(filename):
    with open(filename) as fd:
        content = fd.read().decode('utf-8')
    return content


def xml_fix(s):
    """
    # 1.0.4: added this function

    this supports better handling of invalid XML, removing invalid control characters and
    re-encoding to utf-8 with xmlcharrefreplace
    """
    # string that will be used to replace any invalid characters
    fixer_str = "???"
    # encode the string as utf-8
    utf_str = s.encode('utf-8', 'xmlcharrefreplace')
    # decode the string from utf-8 into unicode
    unicode_str = utf_str.decode('utf-8', 'xmlcharrefreplace')
    # replace any invalid characters that match the invalid_xml regex with the fixer_str
    clean_str, count = invalid_xml.subn(fixer_str, unicode_str)
    # if any invalid characters found, print out a debug message saying how many were replaced
    if count:
        mylog.debug("Replaced {} invalid characters in the XML with {}".format(count, fixer_str))
    # re-encode the string as utf-8
    utf_str = clean_str.encode('utf-8', 'xmlcharrefreplace')
    return utf_str


def http_post(host, port, url, body=None, headers=None, timeout=15):
    # revert SSL verification for python 2.7.9
    try:
        http = httplib.HTTPSConnection(
            host, port, timeout=timeout, context=ssl._create_unverified_context()
        )
    except:
        http = httplib.HTTPSConnection(host, port, timeout=timeout)

    req_args = {}
    req_args['method'] = 'POST'
    req_args['url'] = url
    if body is not None:
        req_args['body'] = body
    if headers is not None:
        req_args['headers'] = headers

    full_url = "https://{0}:{1}/{2}".format(host, port, url)

    clean_headers = dict(headers)
    if 'password' in clean_headers:
        clean_headers['password'] = '**PASSWORD**'

    httplog.debug("HTTP request: Post to {}".format(full_url))
    httplog.debug("HTTP request: headers: {}".format(clean_headers))
    bodyhttplog.debug("HTTP request: body: {}".format(body))

    try:
        http.connect()
        http.request(**req_args)
        response = http.getresponse()
        response_body = response.read()
    except Exception as e:
        raise HttpError("HTTP response: POST request to {!r} failed: {}".format(full_url, e))
    finally:
        http.close()

    headers = dict(response.getheaders())
    content_encoding = headers.get('content-encoding', '').lower()

    m = "HTTP response: from {0!r} len:{1}, status:{2.status} {2.reason}, body type: {3}".format
    httplog.debug(m(full_url, len(response_body), response, type(response_body)))
    httplog.debug("HTTP response: headers: {}".format(headers))

    if not response_body:
        raise HttpError("HTTP response: POST request to {!r} returned empty body".format(full_url))

    ok_codes = [200]
    if response.status not in ok_codes:
        m = "HTTP response: POST request to {!r} returned code: {}, body: {}".format
        raise HttpError(m(full_url, response.status, response_body))

    if content_encoding == 'gzip':
        try:
            before_len = len(response_body)
            buf = StringIO(response_body)
            f = gzip.GzipFile(fileobj=buf)
            response_body = f.read()
            after_len = len(response_body)
            m = "HTTP response: gzip encoding detected, decompressed body from {} to {}".format
            httplog.debug(m(before_len, after_len))
        except Exception as e:
            m = (
                "HTTP response: POST request to {!r} returned gzipped response that failed "
                "to decompress: {}"
            ).format
            raise HttpError(m(full_url, e))

    bodyhttplog.debug("HTTP response: body:\n{}".format(response_body))

    return response_body


class DynamicFormatter(string.Formatter):

    def get_value(self, key, args, kwargs):
        if type(key) in [str, unicode]:
            return kwargs.get(key, '')
        return string.Formatter.get_value(self, key, args, kwargs)


class Session(object):

    GET_OBJECT = 'GetObject'
    UPDATE_OBJECT = 'UpdateObject'
    ADD_OBJECT = 'AddObject'
    DELETE_OBJECT = 'DeleteObject'
    GET_RESULT_INFO = 'GetResultInfo'
    GET_RESULT_DATA = 'GetResultData'
    REQUEST_BODY = load_file(request_body_template_file)
    FORMATTER = DynamicFormatter().format
    AUTH_RES = '/auth'
    SOAP_RES = '/soap'
    INFO_RES = '/info.json'
    SOAP_RESPONSE_TIMEOUT_SEC = 60
    SOAP_REQUEST_HEADERS = {
        'Content-Type': 'text/xml; charset=utf-8',
        'Accept-Encoding': 'gzip',
    }
    COMMAND_RE = re.compile(r'<command>(.*?)</command>', re.IGNORECASE | re.DOTALL)
    SESSION_RE = re.compile(r'<session>(.*?)</session>', re.IGNORECASE | re.DOTALL)

    def __init__(self, server, port=443):
        self.server = server
        self.port = port
        self.last = {}
        self.server_version = "Not yet determined"

    def __str__(self):
        class_name = self.__class__.__name__
        str_tpl = "{} to {}:{}, Authenticated: {}".format
        ret = str_tpl(
            class_name,
            self.server,
            self.port,
            self.is_auth,
        )
        return ret

    def logout(self, all_session_ids=False):
        self._check_auth()

        if all_session_ids:
            logout = 1
        else:
            logout = 0

        headers = {}
        headers['session'] = self.session_id
        headers['logout'] = logout

        post_args = {}
        post_args['url'] = self.AUTH_RES
        post_args['headers'] = headers

        with NoLogging():
            try:
                self._http_post(**post_args)
            except Exception as e:
                m = "logout response: {}".format
                authlog.debug(m(e))

        if all_session_ids:
            authlog.debug("Successfully logged out all session ids for current user")
        else:
            authlog.debug("Successfully logged out current session id for current user")

        self.session_id = ''

    def authenticate(self, username=None, password=None, session_id=None, **kwargs):
        auth_headers = getattr(self, '_auth_headers', {})

        # can request a persistent session that will last up to 1 week when authenticating
        # with username and password. new persistent sessions may be handed out by tanium
        # server when the session handed by this auth call is used to login with that week
        # the new session must be used to login, as no matter what persistent sessions
        # will expire 1 week after issuance (or when logout is called with that session, or
        # when logout with all_sessions=True is called for any session for this user)
        persistent = kwargs.get('persistent', False)

        if session_id:
            # can't request a persistent session when authenticating with a session
            persistent = False
            auth_headers['session'] = session_id
            try:
                del(auth_headers['username'])
                del(auth_headers['password'])
            except:
                pass
        else:
            if username or password:
                try:
                    del(auth_headers['session'])
                except:
                    pass

            if username:
                auth_headers['username'] = b64encode(username)

            if password:
                auth_headers['password'] = b64encode(password)

            if 'username' not in auth_headers:
                raise AuthorizationError("Must supply username")

            if 'password' not in auth_headers:
                raise AuthorizationError("Must supply password")

        if persistent:
            auth_headers['persistent'] = 1

        post_args = {}
        post_args['url'] = self.AUTH_RES
        post_args['headers'] = auth_headers
        post_args['timeout'] = kwargs.get('timeout', 5)

        with NoLogging():
            try:
                body = self._http_post(**post_args)
            except Exception as e:
                raise AuthorizationError(e)

        self._auth_headers = auth_headers
        self.session_id = body
        if persistent:
            m = "Successfully authenticated and received a persistent (up to 1 week) session id"
            authlog.debug(m)
        else:
            authlog.debug("Successfully authenticated and received a 5 minute session id")

    def find(self, object_type, **kwargs):
        self.request_body = self._createGetObjectBody(object_type, **kwargs)
        self.response_body = self._getResponse(self.request_body)
        obj = BaseType.fromSOAPBody(self.response_body)
        return obj

    def save(self, obj, **kwargs):
        self.request_body = self._createUpdateObjectBody(obj, **kwargs)
        self.response_body = self._getResponse(self.request_body)
        obj = BaseType.fromSOAPBody(self.response_body)
        return obj

    def add(self, obj, **kwargs):
        self.request_body = self._createAddObjectBody(obj, **kwargs)
        self.response_body = self._getResponse(self.request_body)
        obj = BaseType.fromSOAPBody(self.response_body)
        return obj

    def delete(self, obj, **kwargs):
        self.request_body = self._createDeleteObjectBody(obj, **kwargs)
        self.response_body = self._getResponse(self.request_body)
        obj = BaseType.fromSOAPBody(self.response_body)
        return obj

    def getResultInfo(self, obj, **kwargs): # noqa
        self.request_body = self._createGetResultInfoBody(obj, **kwargs)
        self.response_body = self._getResponse(self.request_body)
        # parse the single result_info into an Element and create a ResultInfo
        el = ET.fromstring(self.response_body)
        cdata = el.find('.//ResultXML')
        # 1.0.4: fix for utf-8 issues
        result_info = ET.fromstring(xml_fix(cdata.text))
        # TODO: maybe this should be ResultInfoList
        obj = ResultInfo.fromSOAPElement(result_info)
        return obj

    def getResultData(self, obj, **kwargs): # noqa
        self.request_body = self._createGetResultDataBody(obj, **kwargs)
        self.response_body = self._getResponse(self.request_body)
        # parse the single result_info into an Element and create a ResultData
        el = ET.fromstring(self.response_body)
        cdata = el.find('.//ResultXML')
        # 1.0.4: fix for utf-8 issues
        result_info = ET.fromstring(xml_fix(cdata.text))
        # TODO: maybe this should be ResultSetList
        obj = ResultSet.fromSOAPElement(result_info)
        return obj

    def get_server_info(self, port=None, fallback_port=444, **kwargs):
        self._check_auth()

        # 6.2 /info.json is only available on soap port (default port: 444)
        # 6.5 /info.json is only available on server port (default port: 443)

        url = self.INFO_RES
        timeout = kwargs.get('timeout', 5)
        headers = self._auth_headers
        if port is None:
            port = self.port

        body = {}
        server_info_pass_msgs = []
        server_info_fail_msgs = []
        ok_m = "Successfully retrieved server info from {}:{}{}".format
        bad_m = "Failed to retrieve server info from {}:{}{}, {}".format

        try:
            body = self._http_post(port=port, url=url, headers=headers, timeout=timeout)
            body = json.loads(body)
            server_info_pass_msgs.append(ok_m(self.server, port, self.INFO_RES))
        except Exception as e:
            server_info_fail_msgs.append(bad_m(self.server, port, self.INFO_RES, e))

        if not body:
            port = fallback_port
            try:
                body = self._http_post(port=port, url=url, headers=headers, timeout=timeout)
                body = json.loads(body)
                server_info_pass_msgs.append(ok_m(self.server, port, self.INFO_RES))
            except Exception as e:
                server_info_fail_msgs.append(bad_m(self.server, port, self.INFO_RES, e))

        body['server_info_pass_msgs'] = server_info_pass_msgs
        body['server_info_fail_msgs'] = server_info_fail_msgs
        return body

    def get_server_version_from_info(self):
        server_version = "Unable to determine"

        if not getattr(self, 'server_info', {}):
            self.server_info = self.get_server_info()

        if not getattr(self, 'server_info', {}):
            return server_version

        try:
            diagnostics = self.server_info['Diagnostics']
        except Exception as e:
            m = "Unable to find Diagnostics section in server info: {}, server_info: {}".format
            mylog.warning(m(e, self.server_info))
            return server_version

        try:
            settings = [x for x in diagnostics if 'Settings' in x][0]['Settings']
        except Exception as e:
            m = "Unable to find Settings sub-section in Diagnostics: {}, diagnostics: {}".format
            mylog.warning(m(e, diagnostics))
            return server_version

        version = None
        if 'Version' in settings:
            # 6.2
            version = settings['Version']
        else:
            # 6.5
            try:
                version = [x for x in settings if 'Version' in x][0]['Version']
            except:
                pass

        if version:
            server_version = version
        else:
            m = "Unable to find Version key in Settings: {}".format
            mylog.warning(m(settings))

        return server_version

    @property
    def session_id(self):
        if not hasattr(self, '_session_id'):
            return ''
        return self._session_id

    @session_id.setter
    def session_id(self, value):
        if self.session_id != value:
            self._session_id = value
            authlog.debug("Session ID updated to: {}".format(value))

    @property
    def is_auth(self):
        if self.session_id:
            return True
        else:
            return False

    def _http_post(self, **kwargs):
        post_args = {}
        post_args['host'] = kwargs.get('server', self.server)
        post_args['port'] = kwargs.get('port', self.port)
        post_args['url'] = kwargs.get('url', self.SOAP_RES)
        post_args['headers'] = kwargs.get('headers', {})
        post_args['body'] = kwargs.get('body', None)
        post_args['timeout'] = kwargs.get('timeout', self.SOAP_RESPONSE_TIMEOUT_SEC)
        body = http_post(**post_args)
        body = xml_fix(body)
        return body

    def _createAddObjectBody(self, obj, **kwargs): # noqa
        obj_soap = obj.toSOAPBody(minimal=True)

        obj_body = self.FORMATTER(
            self.REQUEST_BODY,
            self.session_id,
            self.ADD_OBJECT,
            obj_soap,
            **kwargs
        )
        return obj_body

    def _createDeleteObjectBody(self, obj, **kwargs): # noqa
        obj_soap = obj.toSOAPBody(minimal=True)

        obj_body = self.FORMATTER(
            self.REQUEST_BODY,
            self.session_id,
            self.DELETE_OBJECT,
            obj_soap,
            **kwargs
        )
        return obj_body

    def _createGetResultInfoBody(self, obj, **kwargs): # noqa
        obj_soap = obj.toSOAPBody(minimal=True)

        obj_body = self.FORMATTER(
            self.REQUEST_BODY,
            self.session_id,
            self.GET_RESULT_INFO,
            obj_soap,
            **kwargs
        )
        return obj_body

    def _createGetResultDataBody(self, obj, **kwargs): # noqa
        obj_soap = obj.toSOAPBody(minimal=True)

        obj_body = self.FORMATTER(
            self.REQUEST_BODY,
            self.session_id,
            self.GET_RESULT_DATA,
            obj_soap,
            **kwargs
        )
        return obj_body

    def _createGetObjectBody(self, object_or_type, **kwargs): # noqa
        if isinstance(object_or_type, BaseType):
            obj_soap = object_or_type.toSOAPBody(minimal=True)
        else:
            obj_soap = '<{}/>'.format(object_or_type._soap_tag)

        obj_body = self.FORMATTER(
            self.REQUEST_BODY,
            self.session_id,
            self.GET_OBJECT,
            obj_soap,
            **kwargs
        )
        return obj_body

    def _createUpdateObjectBody(self, obj, **kwargs): # noqa
        obj_soap = obj.toSOAPBody(minimal=True)

        obj_body = self.FORMATTER(
            self.REQUEST_BODY,
            self.session_id,
            self.UPDATE_OBJECT,
            obj_soap,
            **kwargs
        )
        return obj_body

    def _check_auth(self):
        if not self.is_auth:
            class_name = self.__class__.__name__
            err = "Not yet authenticated, use {}.authenticate()!".format
            raise AuthorizationError(err(class_name))

    def _get_command_text(self, body):
        # using regex is faster than ET chewing the body in and out
        # this matters on LARGE return bodies
        command = re.search(self.COMMAND_RE, body)
        if not command:
            m = "Unable to find <command>.*</command> in body: {}".format
            raise Exception(m(body))

        command = str(command.groups()[0].strip())
        return command

    def _get_session_id_text(self, body):
        # using regex is faster than ET chewing the body in and out
        # this matters on LARGE return bodies
        session_id = re.search(self.SESSION_RE, body)
        if not session_id:
            m = "Unable to find <session>.*</session> in body: {}".format
            raise Exception(m(body))

        session_id = str(session_id.groups()[0].strip())
        return session_id

    def _update_session_id(self, body):
        el = ET.fromstring(body)
        el.find('.//session').text = self.session_id
        body = ET.tostring(el)
        return body

    def _getResponse(self, request_body, **kwargs): # noqa
        retry_auth = kwargs.get('retry_auth', True)

        self._check_auth()

        self.last = {}

        request_command = self._get_command_text(request_body)
        self.last['request_command'] = request_command

        post_args = {}
        post_args['body'] = request_body
        post_args['headers'] = self.SOAP_REQUEST_HEADERS
        post_args['timeout'] = kwargs.get('timeout', self.SOAP_RESPONSE_TIMEOUT_SEC)
        self.last['request_args'] = post_args

        sent = datetime.now()
        self.last['sent'] = sent

        response_body = self._http_post(**post_args)

        received = datetime.now()
        self.last['received'] = received

        elapsed = received - sent
        self.last['elapsed'] = elapsed

        m = "Timing info -- SENT: {}, RECEIVED: {}, ELAPSED: {}".format
        mylog.debug(m(sent, received, elapsed))

        response_command = self._get_command_text(response_body)
        self.last['response_command'] = response_command

        if 'forbidden' in response_command.lower():
            if retry_auth:
                authlog.debug("Last request failed, re-authenticating with user/pass")

                # we may have hit the 5 minute expiration for session_id
                # re-auth with self._auth_headers and re-try
                self.authenticate()

                # Update session id in request body
                request_body = self._update_session_id(request_body)

                # re-issue the request
                response_body = self._getResponse(request_body, retry_auth=False, **kwargs)
            else:
                raise AuthorizationError(response_command)

        elif response_command != request_command:
            m = "Response command {} does not match request command {}".format
            raise BadResponseError(m(response_command, request_command))

        # update session_id, in case new one issued
        self.session_id = self._get_session_id_text(response_body)

        return response_body
