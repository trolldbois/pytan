# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Session handler for Tanium API'''

import os
import httplib
import string
import xml.etree.ElementTree as ET
import logging
from datetime import datetime

from base64 import b64encode
from .object_types.base import BaseType

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
mylog = logging.getLogger("api.session")

request_body_template_file = os.path.join(my_dir, 'request_body_template.xml')


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


def http_post(host, port, url, body=None, headers=None, timeout=5):
    http = httplib.HTTPSConnection(host, port, timeout=timeout)

    req_args = {}
    req_args['method'] = 'POST'
    req_args['url'] = url
    if body is not None:
        req_args['body'] = body
    if headers is not None:
        req_args['headers'] = headers

    try:
        http.connect()
        http.request(**req_args)
        response = http.getresponse()
        response_body = response.read()
    finally:
        http.close()

    full_url = "https://{0}:{1}/{2}".format(host, port, url)
    mylog.debug((
        "HTTP response from {0!r} len:{1}, status:{2.status} {2.reason}"
    ).format(full_url, len(response_body), response))

    if not response_body:
        mylog.debug("Full body of request:\n{}".format(body))
        raise HttpError("No body returned from request to {}".format(full_url))
    if response.status not in [200]:
        raise HttpError(response_body)
    return response_body


class DynamicFormatter(string.Formatter):

    def get_value(self, key, args, kwargs):
        if type(key) in [str, unicode]:
            return kwargs.get(key, '')
        return string.Formatter.get_value(self, key, args, kwargs)


class Session(object):

    GET_OBJECT = 'GetObject'
    UPDATE_OBJECT = 'UpdateObject'
    REQUEST_BODY = load_file(request_body_template_file)
    FORMATTER = DynamicFormatter().format
    AUTH_RES = '/auth'
    SOAP_RES = '/soap'

    def __init__(self, server, port=443):
        self.server = server
        self.port = port
        self.last = {}

    def authenticate(self, username=None, password=None):
        if not hasattr(self, '_auth_headers'):
            if username is None:
                raise AuthorizationError("Must supply username")
            if password is None:
                raise AuthorizationError("Must supply username")

            self._auth_headers = {
                'username': b64encode(username),
                'password': b64encode(password),
            }

        try:
            body = self._http_post(
                url=self.AUTH_RES, headers=self._auth_headers,
            )
        except Exception as e:
            raise AuthorizationError(e)

        self.session_id = body
        mylog.debug("Successfully authenticated")

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

    @property
    def session_id(self):
        if not hasattr(self, '_session_id'):
            return ''
        return self._session_id

    @session_id.setter
    def session_id(self, value):
        self._session_id = value
        mylog.debug("Session ID updated to: {}".format(value))

    def _http_post(self, url, body=None, headers=None):
        body = http_post(self.server, self.port, url, body, headers)
        return body

    def _createGetObjectBody(self, object_or_type, **kwargs):
        if isinstance(object_or_type, BaseType):
            obj = object_or_type.toSOAPBody(minimal=True)
        else:
            obj = '<{}/>'.format(object_or_type.OBJECT_LIST_TAG)
        obj_body = self.FORMATTER(
            self.REQUEST_BODY,
            self.session_id,
            self.GET_OBJECT,
            obj,
            **kwargs
        )
        return obj_body

    def _createUpdateObjectBody(self, obj, **kwargs):
        obj_body = self.FORMATTER(
            self.REQUEST_BODY,
            self.session_id,
            self.UPDATE_OBJECT,
            obj.toSOAPBody(),
            **kwargs
        )
        return obj_body

    def _getResponse(self, request_body):
        self.last = {}
        request_body_el = ET.fromstring(request_body)
        request_command = request_body_el.find('.//command').text
        self.last['request_command'] = request_command

        self.last['sent'] = datetime.now()
        headers = {'Content-Type': 'text/xml'}
        response_body = self._http_post(
            url=self.SOAP_RES, body=request_body, headers=headers,
        )
        self.last['received'] = datetime.now()
        elapsed = self.last['received'] - self.last['sent']
        self.last['elapsed'] = elapsed

        response_body_el = ET.fromstring(response_body)
        response_command = response_body_el.find('.//command').text
        self.last['response_command'] = response_command

        if 'forbidden' in response_command.lower():
            mylog.debug(
                "Last request failed, re-authenticating with user/pass"
            )

            # we may have hit the 5 minute expiration for session_id
            # re-auth with self._auth_headers and re-try
            self.authenticate()

            # Update session id in request body
            request_body_el.find('.//session').text = self.session_id
            request_body = ET.tostring(request_body_el)

            # resend request_body
            self.last['sent'] = datetime.now()
            response_body = self._http_post(
                url=self.SOAP_RES, body=request_body, headers=headers,
            )
            self.last['response_body'] = response_body
            self.last['received'] = datetime.now()
            elapsed = self.last['received'] - self.last['sent']
            self.last['elapsed'] = elapsed
            response_body_el = ET.fromstring(response_body)
            response_command = response_body_el.find('.//command').text
            self.last['response_command'] = response_command
            if 'forbidden' in response_command.lower():
                raise AuthorizationError(response_command)

        if response_command != request_command:
            raise BadResponseError(response_command)

        # update session_id, in case new one issued
        self.session_id = response_body_el.find('.//session').text

        return response_body
