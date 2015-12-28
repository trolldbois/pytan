"""Session class for the :mod:`pytan` module."""

import re
import json
import string
import socket
import logging
import datetime

from pytan import PytanError, requests, tanium_ng, Store
from pytan.version import VERSION_INFO
from pytan.xml_clean import xml_cleaner
from pytan.tickle import to_xml, from_xml
from pytan.tickle.tools import b64encode, xml_pretty

from pytan.constants import (
    SOAP_REQUEST_BODY, SOAP_CONTENT_TYPE, XMLNS, SESSION_DEFAULTS, CRED_DEFAULTS
)

requests.packages.urllib3.disable_warnings()

MYLOG = logging.getLogger(__name__)
AUTHLOG = logging.getLogger(__name__ + ".auth")
HTTPLOG = logging.getLogger(__name__ + ".http")
BODYLOG = logging.getLogger(__name__ + ".body")
HELPLOG = logging.getLogger(__name__ + ".help")


class Session(object):

    """Provide connection layer to Tanium Server.

    This session object uses the :mod:`requests` package instead of the built in httplib library.

    This provides support for keep alive, gzip, cookies, forwarding, and a host of other features
    automatically.

    Examples
    --------

    Setup a Session() object::

        >>> import sys
        >>> sys.path.append('/path/containing/pytan/')
        >>> import pytan
        >>> session = pytan.Session(host='host', username='username', password='password')
    """

    _REQUESTS_SESSION = None
    """
    The Requests session allows you to persist certain parameters across requests. It also
    persists cookies across all requests made from the Session instance. Any requests that you
    make within a session will automatically reuse the appropriate connection
    """

    _ARGS = SESSION_DEFAULTS

    _CREDS = CRED_DEFAULTS

    _AUTH_RES = 'auth'
    """The URL to use for authentication requests"""

    _SOAP_RES = 'soap'
    """The URL to use for SOAP requests"""

    _INFO_RES = 'info.json'
    """The URL to use for server info requests"""

    _ELEMENT_RE_TXT = r'<{0}>(.*?)</{0}>'
    """regex string to search for an element in XML bodies"""

    _CMD_PRUNES = [
        '\n',
        'XML Parse Error: ',
        'SOAPProcessing Exception: class ',
        'ERROR: 400 Bad Request'
    ]
    """List of strings to remove from commands in responses that do not match the response in the
    request
    """

    _NORMAL_CREDS = ['username', 'password', 'domain', 'secondary']

    _AUTH_FAIL_CODES = [401, 403]
    """List of HTTP response codes that equate to authorization failures"""

    _INVALID_VERSIONS = [None, '', 'Unable to determine', 'Not yet determined']
    """List of server versions that are not valid"""

    ALL_RESPONSES = []
    """Holds ALL of the requests response object that was received"""

    LAST_RESPONSE = None
    """Holds the last requests response object that was received"""

    LAST_RESPONSE_INFO = {}
    """Holds the information about the last response received by soap_request()"""

    SERVER_VERSION = "Not yet determined"
    """version string of server, will be updated when get_server_version() is called"""

    SERVER_INFO = {}
    """Holds the return from /info.json"""

    def __init__(self, **kwargs):
        self._ARGS = {k: kwargs.get(k, v) for k, v in self._ARGS.items()}
        self._REQUESTS_SESSION = requests.Session()
        self.MYLOG = MYLOG
        self.AUTHLOG = AUTHLOG
        self.HTTPLOG = HTTPLOG
        self.BODYLOG = BODYLOG
        self.HELPLOG = HELPLOG

        # disable SSL cert verification for all requests made in this session
        self._REQUESTS_SESSION.verify = False

        # re-enforce empty variables for init of session
        self.ALL_RESPONSES = []
        self.LAST_RESPONSE_INFO = {}
        self.LAST_RESPONSE = None
        self.SERVER_VERSION = "Not yet determined"

        # test our connectivity to the Tanium server
        self._test_app_port()

        # authenticate to the Tanium server
        self.authenticate(**kwargs)

    def __str__(self):
        myname = self.__class__.__name__
        ver = self.get_server_version()
        m = "{} to {host}:{port}, Auth Type: {}, {}, Platform Version: {}"
        result = m.format(myname, self.auth_type, self.persist_type, ver, **self._ARGS)
        return result

    def __repr__(self):
        myname = self.__class__.__name__
        ver = getattr(self, 'SERVER_VERSION', '')
        m = "{} to {host}:{port}, Auth Type: {}, {}, Platform Version: {}"
        result = m.format(myname, self.auth_type, self.persist_type, ver, **self._ARGS)
        return result

    @property
    def session_id(self):
        """Property to fetch the session_id for this object

        Returns
        -------
        self._SESSION_ID : str
        """
        result = self._CREDS['session_id']
        return result

    @session_id.setter
    def session_id(self, value):
        """Setter to update the session_id for this object"""
        if self.session_id != value:
            self._CREDS['session_id'] = value
            m = "Session ID updated to: {}"
            m = m.format(value)
            self.AUTHLOG.debug(m)

    def logout(self, **kwargs):
        """Logout a given session_id from Tanium. If not session_id currently set, it will
        authenticate to get one.

        Parameters
        ----------
        all_sessions : bool, optional
            * default: False
            * False: only log out the current session id for the current user
            * True: log out ALL session id's associated for the current user
        """
        self.session_id = kwargs.get('session_id', self.session_id)
        all_sessions = kwargs.get('all_sessions', False)

        if not self.session_id:
            self.authenticate(**kwargs)

        if all_sessions:
            txt = "all session ids"
            logout = 1
        else:
            logout = 0
            txt = "current session id"

        kwargs['url'] = self._AUTH_RES
        kwargs['headers'] = kwargs.get('headers', {})
        kwargs['headers'].update({'session': self.session_id, 'logout': logout})
        kwargs['retry_count'] = 0

        try:
            self.http_request_auth(**kwargs)
        except Exception as e:
            err = "logout exception: {}"
            err = err.format(e)
            self.AUTHLOG.info(err)

        self.session_id = ''

        # TODO: extract user ID from session ID
        m = "Successfully logged out {} for current user"
        m = m.format(txt)
        self.AUTHLOG.info(m)

    def authenticate(self, **kwargs):
        """Authenticate against a Tanium Server using a username/password or a session ID

        Parameters
        ----------
        username : str, optional
            * default: None
            * username to authenticate as
        password : str, optional
            * default: None
            * password for `username`
        session_id : str, optional
            * default: None
            * session_id to authenticate with, this will be used in favor of username/password
        persistent: bool, optional
            * default: False
            * False: do not request a persistent session
             (returns a session_id that expires 5 minutes after last use)
            * True: do request a persistent
             (returns a session_id that expires 1 week after last use)

        Notes
        -----
        Can request a persistent session that will last up to 1 week when authenticating
        with username and password.

        New persistent sessions may be handed out by the Tanium server when the session handed
        by this auth call is used to login with that week. The new session must be used to login,
        as no matter what persistent sessions will expire 1 week after issuance (or when logout is
        called with that session, or when logout with all_sessions=True is called for any session
        for this user)

        the way sessions get issued:

         - a GET request to /auth is issued
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
        """
        self._CREDS.update({k: kwargs.get(k, v) for k, v in self._CREDS.items()})
        self._check_auth_args()

        auth_type = self.auth_type
        persist_type = self.persist_type

        kwargs['url'] = self._AUTH_RES
        kwargs['headers'] = kwargs.get('headers', {})
        kwargs['retry_count'] = 0  # disable http retries for authentication
        kwargs['pytan_help'] = HELPS.auth

        if self._CREDS['persistent']:
            kwargs['headers'].update({'persistent': 1})

        try:
            self.session_id = self.http_request_auth(**kwargs)
        except HttpError as e:
            err = "HTTP Error while trying to authenticate using {}: {}"
            err = err.format(auth_type, e)
            self.MYLOG.exception(err)
            raise
        except AuthorizationError as e:
            err = "Authentication Failed using {}: {}"
            err = err.format(auth_type, e)
            self.MYLOG.exception(err)
            raise AuthorizationError(err)
        except Exception as e:
            err = "Unknown error while trying to authenticate using {}: {}"
            err = err.format(auth_type, e)
            self.MYLOG.exception(err)
            raise

        m = "Successfully authenticated and received a {} session id using {}"
        m = m.format(persist_type, auth_type)
        self.AUTHLOG.info(m)

    def platform_is_6_5(self, **kwargs):
        """Check to see if self.SERVER_VERSION is less than 6.5

        Returns
        -------
        is6_5 : bool
            * True if self.FORCE_SERVER_VERSION is greater than or equal to 6.5
            * True if self.SERVER_VERSION is greater than or equal to 6.5
            * False if self.SERVER_VERSION is less than 6.5
        """
        if self._ARGS['force_version']:
            if self._ARGS['force_version'] >= '6.5':
                result = True
            else:
                result = False
        else:
            if self._invalid_server_version():
                # server version is not valid, force a refresh right now
                self.get_server_version(**kwargs)

            if self._invalid_server_version():
                # server version is STILL invalid, we will assume its 6.2 since port 444 may be
                # inaccessible
                result = False
            else:
                result = self.SERVER_VERSION >= '6.5'
        return result

    def find(self, obj, **kwargs):
        """Creates and sends a GetObject XML Request body from `object_type` and parses the
        response into an appropriate :mod:`tanium_ng` object

        Parameters
        ----------
        obj : :class:`tanium_ng.BaseType`
            * object to find

        Returns
        -------
        obj : :class:`tanium_ng.BaseType`
            * found objects
        """
        if isinstance(obj, tanium_ng.BaseType):
            # obj is an instantiated BaseType
            kwargs['object_list'] = to_xml(obj)
        else:
            # obj is a non instantiated BaseType
            kwargs['object_list'] = '<{}/>'.format(obj._soap_tag)

        kwargs['command'] = 'GetObject'
        kwargs['request_body'] = self._build_body(**kwargs)
        response_body = self.soap_request(**kwargs)
        result = from_xml(response_body)
        return result

    def save(self, obj, **kwargs):
        """Creates and sends a UpdateObject XML Request body from `obj` and parses the response
        into an appropriate :mod:`tanium_ng` object

        Parameters
        ----------
        obj : :class:`tanium_ng.BaseType`
            * object to save

        Returns
        -------
        obj : :class:`tanium_ng.BaseType`
            * saved object
        """
        kwargs['object_list'] = to_xml(obj)
        kwargs['command'] = 'UpdateObject'
        kwargs['request_body'] = self._build_body(**kwargs)
        response_body = self.soap_request(**kwargs)
        result = from_xml(response_body)
        return result

    def add(self, obj, **kwargs):
        """Creates and sends a AddObject XML Request body from `obj` and parses the response into
        an appropriate :mod:`tanium_ng` object

        Parameters
        ----------
        obj : :class:`tanium_ng.BaseType`
            * object to add

        Returns
        -------
        obj : :class:`tanium_ng.BaseType`
            * added object
        """
        kwargs['object_list'] = to_xml(obj)
        kwargs['command'] = 'AddObject'
        kwargs['request_body'] = self._build_body(**kwargs)
        response_body = self.soap_request(**kwargs)
        result = from_xml(response_body)
        return result

    def delete(self, obj, **kwargs):
        """Creates and sends a DeleteObject XML Request body from `obj` and parses the response
        into an appropriate :mod:`tanium_ng` object

        Parameters
        ----------
        obj : :class:`tanium_ng.BaseType`
            * object to delete

        Returns
        -------
        obj : :class:`tanium_ng.BaseType`
            * deleted object
        """
        kwargs['object_list'] = to_xml(obj)
        kwargs['command'] = 'DeleteObject'
        kwargs['request_body'] = self._build_body(**kwargs)
        response_body = self.soap_request(**kwargs)
        result = from_xml(response_body)
        return result

    def run_plugin(self, obj, **kwargs):
        """Creates and sends a RunPlugin XML Request body from `obj` and parses the response into
        an appropriate :mod:`tanium_ng` object

        Parameters
        ----------
        obj : :class:`tanium_ng.BaseType`
            * object to run

        Returns
        -------
        obj : :class:`tanium_ng.BaseType`
            * results from running object
        """
        kwargs['object_list'] = to_xml(obj)
        kwargs['command'] = 'RunPlugin'
        kwargs['request_body'] = self._build_body(**kwargs)
        response_body = self.soap_request(**kwargs)
        result = from_xml(response_body)
        return result

    def get_result_info(self, obj, **kwargs):
        """Creates and sends a GetResultInfo XML Request body from `obj` and parses the response
        into an appropriate :mod:`tanium_ng` object

        Parameters
        ----------
        obj : :class:`tanium_ng.BaseType`
            * object to get result info for

        Returns
        -------
        obj : :class:`tanium_ng.ResultInfo`
            * ResultInfo for `obj`
        """
        kwargs['object_list'] = to_xml(obj)
        kwargs['command'] = 'GetResultInfo'
        kwargs['request_body'] = self._build_body(**kwargs)
        response_body = self.soap_request(**kwargs)
        result = from_xml(response_body)
        return result

    def get_result_data(self, obj, **kwargs):
        """Creates and sends a GetResultData XML Request body from `obj` and parses the response
        into an appropriate :mod:`tanium_ng` object

        Parameters
        ----------
        obj : :class:`tanium_ng.BaseType`
            * object to get result set for

        Returns
        -------
        obj : :class:`tanium_ng.ResultSet`
            * otherwise, `obj` will be the ResultSet for `obj`
        """
        kwargs['object_list'] = to_xml(obj)
        kwargs['command'] = 'GetResultData'
        kwargs['request_body'] = self._build_body(**kwargs)
        response_body = self.soap_request(**kwargs)
        result = from_xml(response_body)
        return result

    def get_result_data_sse(self, obj, **kwargs):
        """Creates and sends a GetResultData XML Request body that starts a server side export
        from `obj` and parses the response for an export_id.

        Parameters
        ----------
        obj : :class:`tanium_ng.BaseType`
            * object to start server side export

        Returns
        -------
        export_id : str
            * value of export_id element found in response
        """
        kwargs['object_list'] = to_xml(obj)
        kwargs['command'] = 'GetResultData'
        kwargs['request_body'] = self._build_body(**kwargs)
        response_body = self.soap_request(**kwargs)
        # if there is an export_id node, return the contents of that
        regex_args = {'body': response_body, 'element': 'export_id', 'fail': True}
        result = self._regex_body_for_element(**regex_args)
        return result

    def get_server_info(self, **kwargs):
        """Gets the /info.json

        Parameters
        ----------
        port_fallback : int, optional
            * default: 444
            * fallback port to attempt getting /info.json from if `port` fails

        Returns
        -------
        info_dict : dict
            * raw json response converted into python dict
            * 'diags_flat': info.json flattened out into an easier to use structure for python
            * 'server_info_pass_msgs': messages about successfully retrieving info.json
            * 'server_info_fail_msgs': messages about failing to retrieve info.json

        See Also
        --------
        :func:`pytan.sessions.Session._flatten_server_info` : method to flatten the dictionary
        received from info.json into a python friendly format

        Notes
        -----
            * 6.2 /info.json is only available on soap port (default port: 444)
            * 6.5 /info.json is only available on server port (default port: 443)
        """
        port_fallback = kwargs.get('port_fallback', self._ARGS['port_fallback'])

        kwargs['url'] = self._INFO_RES
        kwargs['retry_count'] = 0
        kwargs['pytan_help'] = HELPS.servinfo

        info_body = ''
        server_info_pass_msgs = []
        server_info_fail_msgs = []
        ok_m = "Successfully retrieved server info from {}".format
        bad_m = "Failed to retrieve server info from {}, {}".format
        json_fail_m = "Failed to parse server info from json, error: {}".format
        diags_flat_fail_m = "Failed to flatten server info from json, error: {}".format

        full_url = self._get_full_url(**kwargs)

        try:
            info_body = self.http_request_auth(**kwargs)
            server_info_pass_msgs.append(ok_m(full_url))
        except Exception as e:
            server_info_fail_msgs.append(bad_m(full_url, e))

        if not info_body:
            kwargs['port'] = port_fallback
            full_url = self._get_full_url(**kwargs)
            try:
                info_body = self.http_request_auth(**kwargs)
                server_info_pass_msgs.append(ok_m(full_url))
            except Exception as e:
                server_info_fail_msgs.append(bad_m(full_url, e))

        try:
            info_dict = json.loads(info_body)
        except Exception as e:
            info_dict = {'info_body_failed_json': info_body}
            server_info_fail_msgs.append(json_fail_m(e))

        try:
            diagnostics = info_dict.get('Diagnostics', [])
            info_dict['diags_flat'] = self._flatten_server_info(structure=diagnostics)
        except Exception as e:
            info_dict['diags_flat'] = {}
            server_info_fail_msgs.append(diags_flat_fail_m(e))

        info_dict['server_info_pass_msgs'] = server_info_pass_msgs
        info_dict['server_info_fail_msgs'] = server_info_fail_msgs
        self.SERVER_INFO = info_dict
        return info_dict

    def get_server_version(self, **kwargs):
        """Tries to parse the server version from /info.json

        Returns
        -------
        str
            * str containing server version from /info.json
        """
        if self._invalid_server_version():
            self._determine_server_version(**kwargs)
        result = self.SERVER_VERSION
        return result

    def soap_request(self, request_body, **kwargs):
        """xxx."""
        a = [
            'clean_xml_restricted', 'clean_xml_invalid', 'session_fallback',
            'connect_secs_soap', 'response_secs_soap',
        ]
        kwargs.update({k: kwargs.get(k, self._ARGS[k]) for k in a})

        headers = {}
        headers['Content-Type'] = SOAP_CONTENT_TYPE
        headers.update(kwargs.get('headers', {}))

        kwargs['url'] = kwargs.get('url', self._SOAP_RES)
        kwargs['headers'] = headers
        kwargs['body'] = request_body
        kwargs['connect_secs'] = kwargs['connect_secs_soap']
        kwargs['response_secs'] = kwargs['response_secs_soap']
        kwargs['request_method'] = 'post'

        regex_args = {'body': request_body, 'element': 'command', 'fail': True}
        request_command = self._regex_body_for_element(**regex_args)
        sent = datetime.datetime.utcnow()

        # use the authenticated http request method to get a response
        result = self.http_request_auth(**kwargs)

        received = datetime.datetime.utcnow()
        elapsed = received - sent
        regex_args = {'body': result, 'element': 'command', 'fail': True}
        response_command = self._regex_body_for_element(**regex_args)

        self.LAST_RESPONSE_INFO = {}
        self.LAST_RESPONSE_INFO['request_command'] = request_command
        self.LAST_RESPONSE_INFO['request_args'] = kwargs
        self.LAST_RESPONSE_INFO['sent'] = sent
        self.LAST_RESPONSE_INFO['received'] = received
        self.LAST_RESPONSE_INFO['elapsed'] = elapsed
        self.LAST_RESPONSE_INFO['response_command'] = response_command

        m = "HTTP Response: Timing info -- SENT: {}, RECEIVED: {}, ELAPSED: {}".format
        self.HTTPLOG.debug(m(sent, received, elapsed))

        if 'forbidden' in response_command.lower():
            if kwargs['session_fallback']:
                m = "Last request was denied, re-authenticating with user/pass"
                self.AUTHLOG.info(m)

                # we may have hit the 5 minute expiration for session_id, empty out session ID,
                # re-authenticate, then retry request
                self.session_id = ''
                self.authenticate(**kwargs)

                # re-issue the request
                kwargs['session_fallback'] = False
                kwargs['request_body'] = request_body
                result = self.soap_request(**kwargs)
            else:
                err = "Access denied after re-authenticating! Server response: {}"
                err = err.format(response_command)
                raise AuthorizationError(err)

        elif response_command != request_command:
            for p in self._CMD_PRUNES:
                response_command = response_command.replace(p, '').strip()

            err = "Response command {} does not match request command {}"
            err = err.format(response_command, request_command)
            raise BadResponseError(err)

        # update session_id, in case new one issued
        regex_args = {'body': result, 'element': 'session', 'fail': True}
        self.session_id = self._regex_body_for_element(**regex_args)

        # TODO: REMOVE, BUT FIX _REGEX_BODY_FOR_ELEMENT FAIL=FALSE FIRST
        # check to see if server_version set in response (6.5+ only)
        if self._invalid_server_version():
            regex_args = {'body': result, 'element': 'server_version', 'fail': False}
            server_version = self._regex_body_for_element(**regex_args)
            if server_version and self.SERVER_VERSION != server_version:
                self.SERVER_VERSION = server_version
        return result

    def _replace_credentials(self, **kwargs):
        """pass."""
        headers = kwargs.get('headers', {})

        # get the credentials that have been passed in with self._CREDS as defaults
        creds = {k: kwargs.get(k, v) for k, v in self._CREDS.items()}

        # remove the credential keys from the headers that were passed in
        removes = ['username', 'password', 'session_id', 'domain', 'secondary']
        result = {k: v for k, v in headers.items() if k not in removes}

        added = []
        # if session_id is in creds, add that to the result
        if creds['session_id']:
            result['session'] = creds['session_id']
            added.append('session_id')
        else:
            need_b64 = ['username', 'password']
            for k in self._NORMAL_CREDS:
                if not creds[k]:
                    continue
                if k in need_b64:
                    result[k] = b64encode(creds[k])
                else:
                    result[k] = creds[k]
                added.append(k)

        if not added:
            err = "No credentials defined in session or in kwargs!!"
            raise AuthorizationError(err)

        m = "Using {} for authentication headers"
        m = m.format(', '.join(added))
        self.AUTHLOG.info(m)
        return result

    def http_request_auth(self, **kwargs):
        kwargs['headers'] = self._replace_credentials(**kwargs)

        a = ['session_fallback', 'retry_count', 'host', 'port']
        kwargs.update({k: kwargs.get(k, self._ARGS[k]) for k in a})

        current_try = 1

        while True:
            try:
                result = self.http_request(**kwargs)
                break
            except AuthorizationError as e:
                if self.session_id and kwargs['session_fallback']:
                    err = "AuthorizationError with session_id {}, falling back to user creds!"
                    err = err.format(self.session_id)
                    self.MYLOG.info(err)

                    self.session_id = ''
                    self.authenticate(**kwargs)
                    kwargs['session_fallback'] = False
                    result = self.http_request_auth(**kwargs)
                else:
                    err = "AuthorizationError with session_id {}, session_fallback: {}!"
                    err = err.format(self.session_id, kwargs['session_fallback'])
                    self.MYLOG.exception(err)
                    raise
            except HttpError as e:
                if not kwargs['retry_count']:
                    err = "HttpError and retry_count is {}: {}"
                    err = err.format(e, kwargs['retry_count'])
                    self.MYLOG.exception(err)
                    raise

                err = "HttpError on attempt {} out of {}: {}"
                err = err.format(current_try, kwargs['retry_count'], e)

                if current_try > kwargs['retry_count']:
                    self.MYLOG.exception(err)
                    raise
                else:
                    self.MYLOG.info(err)
            except Exception as e:
                err = "Unexpected error: {}"
                err = err.format(e)
                self.MYLOG.exception(err)
                raise

                current_try += 1
        return result

    def http_request(self, host, port, url, **kwargs):
        """This is an HTTP GET / POST method that utilizes the :mod:`requests` package."""
        # get any headers that may have been supplied
        supplied_headers = kwargs.get('headers', {})

        # get the connect timeout seconds, defaulting to self._ARGS if not supplied here
        connect_secs = kwargs.get('connect_secs', self._ARGS['connect_secs'])

        # get the resposne timeout seconds, defaulting to self._ARGS if not supplied here
        response_secs = kwargs.get('response_secs', self._ARGS['response_secs'])

        # determine the supplied request method, default to get
        request_method = kwargs.get('request_method', 'get').lower()

        # determine whether or not response body can be empty
        empty_ok = kwargs.get('empty_ok', False)

        # get the body supplied
        body = kwargs.get('body', '')

        # get the pytan_help string supplied
        pytan_help = kwargs.get('pytan_help', "NO HELP SUPPLIED")

        # construct the full url for this request
        full_url = self._get_full_url(host=host, port=port, url=url)

        # get the global request headers that are defined and format them with VERSION_INFO
        subs = {}
        subs.update(VERSION_INFO)
        req_headers = {k: v.format(**subs) for k, v in self._ARGS['request_headers'].items()}

        # create our headers for this request, letting supplied_headers overried req_headers
        headers = {}
        headers.update(req_headers)
        headers.update(supplied_headers)

        # print an info log message about this request
        pre = "HTTP {} request: '{}': len:{}"
        pre = pre.format(request_method.upper(), full_url, len(body))
        self.HTTPLOG.info(pre)

        # print a debug log message about this requests headers, hiding password string
        clean_headers = {}
        clean_headers.update(headers)
        if 'password' in clean_headers:
            clean_headers['password'] = '**PASSWORD**'

        m = "{}: headers: {}"
        m = m.format(pre, clean_headers)
        self.HTTPLOG.debug(m)

        # print an info log message to the HELPLOG
        pytan_help = "{} - {}".format(pytan_help, pre)
        self.HELPLOG.info(pytan_help)

        # create our request args
        req_args = {}
        req_args['headers'] = headers
        req_args['timeout'] = (connect_secs, response_secs)

        # if doing a post, add the body to the request args and print a debug log message with body
        if request_method == 'post':
            req_args['data'] = body
            m = "{}: body:\n{}"
            m = m.format(pre, body)
            self.BODYLOG.debug(m)

        # get the requests function for request_method from the requests session object
        requests_func = getattr(self._REQUESTS_SESSION, request_method)

        # perform the request
        try:
            response = requests_func(full_url, **req_args)
        except Exception as e:
            err = "HTTP response: {} request to '{}' failed: {}"
            err = err.format(request_method.upper(), full_url, e)
            self.MYLOG.exception(err)
            raise HttpError(err)

        # set the response as LAST_RESPONSE
        self.LAST_RESPONSE = response

        # if recrod_all is set, add the response to ALL_RESPONSES
        if self._ARGS['record_all']:
            self.ALL_RESPONSES.append(response)

        # add the pytan_help arg as an attribute to the response
        response.pytan_help = pytan_help

        # get the text from the response
        response_body = response.text

        # run the xml_cleaner against the response
        kwargs['text'] = response_body
        response_body = xml_cleaner(**kwargs)

        # print a bunch of messages to a bunch of different logs & levels
        pre = "HTTP {} response: '{}'"
        pre = pre.format(request_method.upper(), full_url)

        m = "{0}: len:{1}, status:{2.status_code} {2.reason}"
        m = m.format(pre, len(response_body), response)
        self.HTTPLOG.info(m)

        m = "{0}: headers: {1.headers}"
        m = m.format(pre, response)
        self.HTTPLOG.debug(m)

        m = "{0}: body:\n{1}"
        m = m.format(pre, response_body)
        self.BODYLOG.debug(m)

        if response.status_code in self._AUTH_FAIL_CODES:
            err = "{0}: returned code: {1.status_code}, body: {2}"
            err = err.format(pre, response, response_body)
            raise AuthorizationError(err)

        if not response.ok:
            err = "{0}: returned code: {1.status_code}, body: {2}"
            err = err.format(pre, response, response_body)
            raise HttpError(err)

        if not response_body and not empty_ok:
            err = "{0}: returned empty body"
            err = err.format(pre)
            raise HttpError(err)

        return response_body

    def get_last_bodies(self):
        """Uses :func:`xml_pretty` to pretty print the last request and response bodies from the
        session object

        """
        request_body = self.LAST_RESPONSE.request.body
        response_body = self.LAST_RESPONSE.text
        try:
            req = xml_pretty(request_body)
        except Exception as e:
            req = "Failed to prettify xml: {}, raw xml:\n{}".format(e, request_body)

        try:
            resp = xml_pretty(response_body)
        except Exception as e:
            resp = "Failed to prettify xml: {}, raw xml:\n{}".format(e, response_body)
        return req, resp

    def _flatten_server_info(self, structure):
        """Utility method for flattening the JSON structure for info.json into a more python usable format

        Parameters
        ----------
        structure
            * dict/tuple/list to flatten

        Returns
        -------
        result
            * the dict/tuple/list flattened out
        """
        result = structure
        if isinstance(structure, dict):
            for k, v in result.items():
                result[k] = self._flatten_server_info(structure=v)
        elif isinstance(structure, (tuple, list)):
            if all([isinstance(x, dict) for x in structure]):
                result = {}
                [result.update(self._flatten_server_info(structure=i)) for i in structure]
        return result

    def _build_body(self, command, object_list, **kwargs):
        """Utility method for building an XML Request Body

        Parameters
        ----------
        command : str
            * text to use in command node when building template
        object_list : str
            * XML string to use in object list node when building template
        kwargs : dict, optional
            * any number of attributes that can be set via
            :class:`tanium_ng.Options` that control the servers response.

        Returns
        -------
        body : str
            * The XML request body created from the string.template SOAP_REQUEST_BODY
        """
        options_obj = tanium_ng.Options(values=kwargs)
        options = to_xml(options_obj)

        body_str = SOAP_REQUEST_BODY.format(**XMLNS)
        body_template = string.Template(body_str)

        subs = {'command': command, 'object_list': object_list, 'options': options}
        result = body_template.substitute(**subs)
        return result

    def _regex_body_for_element(self, body, element, fail=True):
        """Utility method to use a regex to get an element from an XML body

        Parameters
        ----------
        body : str
            * XML to search
        element : str
            * element name to search for in body
        fail : bool, optional
            * default: True
            * True: throw exception if unable to find any matches for `regex` in `body`
            * False do not throw exception if unable to find any matches for `regex` in `body`

        Returns
        -------
        ret : str
            * The first value that matches the regex ELEMENT_RE_TXT with element
        """
        regex_txt = self._ELEMENT_RE_TXT.format(element)
        regex = re.compile(regex_txt, re.IGNORECASE | re.DOTALL)

        ret = regex.search(body)

        if not ret and fail:
            err = "Unable to find {} in body: {}"
            err = err.format(regex.pattern, body)
            raise Exception(err)  # TODO
        else:
            ret = str(ret.groups()[0].strip())

        m = "Value of element '{}': '{}' (using pattern: '{}'"
        m = m.format(element, ret, regex.pattern)
        self.MYLOG.debug(m)
        return ret

    def _invalid_server_version(self):
        """Utility method to find out if self.SERVER_VERSION is valid or not"""
        result = False
        if getattr(self, 'SERVER_VERSION', '') in self._INVALID_VERSIONS:
            result = True
        return result

    def _determine_server_version(self, **kwargs):
        """pass."""
        result = "Unable to determine"

        if not getattr(self, 'SERVER_INFO', {}):
            self.get_server_info(**kwargs)

        if getattr(self, 'SERVER_INFO', {}):
            try:
                result = self.SERVER_INFO['diags_flat']['Settings']['Version']
            except:
                m = "Unable to find Version key in Settings: {}"
                m = m.format(self.SERVER_INFO['diags_flat'])
                self.MYLOG.info(m)

        result = str(result)
        self.SERVER_VERSION = result
        return result

    @property
    def auth_type(self):
        """pass."""
        if not self.normal_creds and not self.session_id:
            err = "Authentication type unknown!"
            self.MYLOG.critical(err)
            raise AuthorizationError(err)

        creds = [k for k in self._NORMAL_CREDS if self._CREDS.get(k, None)]

        if self.session_id:
            creds.append('session_id')

        result = ', '.join(creds)
        return result

    @property
    def persist_type(self):
        """pass."""
        if self._CREDS['persistent']:
            result = "persistent (up to 1 week)"
        else:
            result = "non-persistent (up to 5 minutes)"
        return result

    def _get_full_url(self, **kwargs):
        """Utility method for constructing a full url

        Parameters
        ----------
        url : str
            * url to use in string
        host : str, optional
            * default: self._HOST
            * hostname/IP address to use in string
        port : str, optional
            * default: self._PORT
            * port to use in string

        Returns
        -------
        full_url : str
            * full url in the form of https://$host:$port/$url
        """
        url = kwargs.get('url', '')
        host = kwargs.get('host', self._ARGS['host'])
        port = kwargs.get('port', self._ARGS['port'])
        protocol = kwargs.get('protocol', self._ARGS['protocol'])
        result = "{0}://{1}:{2}/{3}"
        result = result.format(protocol, host, port, url)
        return result

    @property
    def normal_creds(self):
        normal_creds = [self._CREDS.get(k, None) for k in self._NORMAL_CREDS]
        result = any(normal_creds)
        return result

    def _check_auth_args(self):
        """pass."""

        if not self.session_id and not self.normal_creds:
            err = "Need username, password, domain, and/or secondary if not supplying session_id"
            self.MYLOG.critical(err)
            raise AuthorizationError(err)

        if self.session_id and not self.normal_creds and self._CREDS['persistent']:
            err = "Unable to establish a persistent session when authenticating via session_id"
            self.MYLOG.critical(err)
            raise AuthorizationError(err)

    def _test_app_port(self):
        """Validates that `host`:`port` can be reached using :func:`port_check`

        Parameters
        ----------
        host : str
            * hostname/ip address to check `port` on
        port : int
            * port to check on `host`

        Raises
        ------
        exceptions.HandlerError : :exc:`exceptions.HandlerError`
            * if `host`:`port` can not be reached
        """
        m = "{state} Port test to {host}:{port} with timeout: {connect_secs}{err}"

        host = self._ARGS['host']
        port = self._ARGS['port']
        timeout = self._ARGS['connect_secs']

        try:
            socket.create_connection((host, port), timeout)
            self.MYLOG.debug(m.format(state="[SUCCESS]", err='', **self._ARGS))
        except socket.error as e:
            err = m.format(state="[FAILURE]", err=e, **self._ARGS)
            self.MYLOG.critical(err)
            raise NetworkError(err)


class AuthorizationError(PytanError):
    pass


class HttpError(PytanError):
    pass


class BadResponseError(PytanError):
    pass


class NetworkError(PytanError):
    pass


HELPS = Store()
HELPS.servinfo = "Get the server version via /info.json"
HELPS.auth = "Authenticate to the SOAP API via /auth"
