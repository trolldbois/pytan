"""Session class for the :mod:`pytan` module."""

import re
import json
import string
import socket
import logging
import datetime

from pytan import PytanError, requests, tanium_ng
from pytan.store import Store
from pytan.version import VERSION_INFO
from pytan.xml_clean import xml_cleaner
from pytan.tickle.tools import to_xml, from_xml, b64encode, xml_pretty, obfuscate, deobfuscate

from pytan.constants import (
    SOAP_REQUEST_BODY, SOAP_CONTENT_TYPE, XMLNS, SESSION_DEFAULTS, CRED_DEFAULTS, PYTAN_KEY
)

MYLOG = logging.getLogger(__name__)
AUTHLOG = logging.getLogger(__name__ + ".auth")
HTTPLOG = logging.getLogger(__name__ + ".http")
BODYLOG = logging.getLogger(__name__ + ".body")
HELPLOG = logging.getLogger(__name__ + ".help")

HELPS = Store()
HELPS.servinfo = "Get the server version via /info.json"
HELPS.auth = "Authenticate to the SOAP API via /auth"
HELPS.logout = "Logout from the SOAP API via /auth"
HELPS.getuser = "Get user object from the User ID stored in the Session ID"

requests.packages.urllib3.disable_warnings()


class SessionError(PytanError):
    pass


class AuthorizationError(SessionError):
    pass


class HttpError(SessionError):
    pass


class BadResponseError(SessionError):
    pass


class NetworkError(SessionError):
    pass


class CredStore(dict):

    _NORMAL_CREDS = ['username', 'password', 'domain', 'secondary']

    def __init__(self):
        self.username = CRED_DEFAULTS['username']
        self.password = CRED_DEFAULTS['password']
        self.domain = CRED_DEFAULTS['domain']
        self.secondary = CRED_DEFAULTS['secondary']
        self.persistent = CRED_DEFAULTS['persistent']
        self.session_id = CRED_DEFAULTS['session_id']
        self.session_dt = None
        self.user_obj = None

    def __str__(self):
        me = self.__class__.__name__
        ret = ["    ** {} '{}': '{}'".format(me, k, getattr(self, k, '')) for k in sorted(self)]
        ret = '\n'.join(ret)
        return ret

    def __repr__(self):
        return self.__str__()

    def __getattr__(self, name):
        if name == 'password' and self.get(name, ''):
            value = '**PASSWORD**'
        else:
            value = self.get(name, '')
        return value

    def __setattr__(self, name, value):
        old_value = self.get(name, '')
        old_attr_value = getattr(self, name, '')

        if name == 'password':
            value = obfuscate(key=PYTAN_KEY, string=value)

        if name == 'session_id':
            if not value:
                self.session_dt = None
                self.user_obj = None
            elif old_value != value:
                self.session_dt = datetime.datetime.utcnow()

        if old_value != value:
            self[name] = value
            new_attr_value = getattr(self, name, '')
            m = "    ** {}: {!r} updated from '{}' to '{}'"
            m = m.format(self.__class__.__name__, name, old_attr_value, new_attr_value)
            AUTHLOG.debug(m)

    def __delattr__(self, name):
        if name in self:
            self[name] = ''

    def auth_type(self):
        if self.has_session_creds:
            if self.has_normal_creds:
                result = 'session_id (received by authenticating with {})'
                result = result.format(', '.join(self.normal_creds))
            else:
                result = 'session_id (supplied manually)'
        elif self.has_normal_creds:
            result = ', '.join(self.normal_creds)
        else:
            err = "Need username, password, domain, and/or secondary if not supplying session_id"
            raise AuthorizationError(err)
        return result

    def persist_type(self):
        if self.has_session_creds and not self.has_normal_creds and self.persistent:
            err = "Unable to establish a persistent session when authenticating via session_id"
            raise AuthorizationError(err)

        if self.persistent:
            result = "persistent (up to 1 week)"
        else:
            result = "non-persistent (up to 5 minutes)"
        return result

    @property
    def normal_creds(self):
        result = [k for k in self._NORMAL_CREDS if self.get(k, '')]
        return result

    @property
    def session_creds(self):
        result = [k for k in ['session_id'] if self.get(k, '')]
        return result

    @property
    def has_normal_creds(self):
        result = any(self.normal_creds)
        return result

    @property
    def has_session_creds(self):
        result = any(self.session_creds)
        return result

    @property
    def headers(self):
        """pass."""
        result = {}

        # if session_id is in creds, add that to the result
        if self.has_session_creds:
            m = "Using Session ID for authentication headers"
            AUTHLOG.debug(m)
            result['session'] = self.session_id
        elif self.has_normal_creds:
            adds = []
            for k in self._NORMAL_CREDS:
                if not self.get(k):
                    continue
                if k == 'username':
                    result[k] = b64encode(self.get(k))
                elif k == 'password':
                    result[k] = b64encode(self._true_password)
                else:
                    result[k] = self.get(k)
                adds.append(k)

            m = "Using {} for authentication headers"
            m = m.format(', '.join(adds))
            AUTHLOG.debug(m)
        else:
            err = "Need username, password, domain, and/or secondary if not supplying session_id"
            raise AuthorizationError(err)
        return result

    @property
    def _true_password(self):
        return deobfuscate(key=PYTAN_KEY, string=self.get('password'))

    def session_seconds(self):
        if self.session_dt:
            result = (datetime.datetime.utcnow() - self.session_dt).seconds
        else:
            result = -1
        m = "session id issued {} seconds ago"
        m = m.format(result)
        AUTHLOG.debug(m)
        return result

    def session_is_expired(self):
        if not self.session_id or self.session_seconds() > 260:
            result = True
            self.session_id = ''
        else:
            result = False
        return result


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

    _ARGS = {}

    _CREDS = None

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
        self._ARGS = {k: kwargs.get(k, v) for k, v in SESSION_DEFAULTS.items()}

        if not self._ARGS['host']:
            raise SessionError("Must supply argument 'host'!")

        if not self._ARGS['port']:
            raise SessionError("Must supply argument 'port'!")

        try:
            self._ARGS['port'] = int(self._ARGS['port'])
        except ValueError:
            raise SessionError("Argument 'port' must be an integer!")

        self._REQUESTS_SESSION = requests.Session()
        self.MYLOG = MYLOG
        self.AUTHLOG = AUTHLOG
        self.HTTPLOG = HTTPLOG
        self.BODYLOG = BODYLOG
        self.HELPLOG = HELPLOG

        # disable SSL cert verification for all requests made in this session
        self._REQUESTS_SESSION.verify = False

        # re-enforce empty variables for init of session
        self._CREDS = CredStore()
        self.ALL_RESPONSES = []
        self.LAST_RESPONSE_INFO = {}
        self.LAST_RESPONSE = None
        self.SERVER_VERSION = "Not yet determined"

        # test our connectivity to the Tanium server
        self._test_app_port()

        # authenticate to the Tanium server
        self.authenticate(**kwargs)
        self.get_userinfo()

    def __str__(self):
        myname = self.__class__.__name__
        ver = self.get_server_version()
        normal_creds = self._CREDS.has_normal_creds
        session_creds = self._CREDS.has_session_creds
        persist_type = self._CREDS.persist_type()
        m = "{} to {host}:{port}, Normal Creds: {}, Session ID: {}, {}, Platform Version: {}"
        result = m.format(myname, normal_creds, session_creds, persist_type, ver, **self._ARGS)
        return result

    def __repr__(self):
        myname = self.__class__.__name__
        ver = getattr(self, 'SERVER_VERSION', '')
        ver = self.get_server_version()
        normal_creds = self._CREDS.has_normal_creds
        session_creds = self._CREDS.has_session_creds
        persist_type = self._CREDS.persist_type()
        m = "{} to {host}:{port}, Normal Creds: {}, Session ID: {}, {}, Platform Version: {}"
        result = m.format(myname, normal_creds, session_creds, persist_type, ver, **self._ARGS)
        return result

    @property
    def session_id(self):
        """Property to fetch the session_id for this object

        Returns
        -------
        self._SESSION_ID : str
        """
        result = self._CREDS.session_id
        return result

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
        self.authenticate(**kwargs)

        all_sessions = kwargs.get('all_sessions', False)
        state = "all session ids" if all_sessions else "current session id"

        supplied_headers = kwargs.get('headers', {}) or {}
        headers = {}
        headers['session'] = self.session_id
        headers['logout'] = int(all_sessions)

        headers.update(supplied_headers)

        kwargs['host'] = kwargs.get('host', self._ARGS.get('host'))
        kwargs['port'] = kwargs.get('port', self._ARGS.get('port'))
        kwargs['url'] = self._AUTH_RES
        kwargs['headers'] = headers
        kwargs['pytan_help'] = HELPS.logout

        m = "Attempting to log out {} for current user"
        m = m.format(state)
        self.AUTHLOG.info(m)

        # try:
        self.http_request(**kwargs)
        # except Exception as e:
        #     err = "logout exception: {}"
        #     err = err.format(e)
        #     self.AUTHLOG.info(err)

        self._CREDS.session_id = ''

        m = "Successfully logged out {} for current user"
        m = m.format(state)
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
        for k in self._CREDS._NORMAL_CREDS:
            if k not in kwargs or not kwargs.get(k, ''):
                continue
            setattr(self._CREDS, k, kwargs[k])
            self._CREDS.session_id = ''

        self._CREDS.session_id = kwargs.get('session_id', self._CREDS.session_id)
        self._CREDS.persistent = kwargs.get('persistent', self._CREDS.persistent)

        if self._CREDS.session_id and not self._CREDS.session_is_expired():
            return

        m = "authenticate creds:\n{}"
        m = m.format(self._CREDS)
        self.AUTHLOG.debug(m)

        auth_type = self._CREDS.auth_type()
        persist_type = self._CREDS.persist_type()

        m = "Attempting to authenticate and receive a {} session id using {}"
        m = m.format(persist_type, auth_type)
        self.AUTHLOG.info(m)

        supplied_headers = kwargs.get('headers', {}) or {}

        kwargs['headers'] = {}
        kwargs['headers'].update(self._CREDS.headers)
        kwargs['headers']['persistent'] = int(self._CREDS.persistent)
        kwargs['headers'].update(supplied_headers)

        kwargs['host'] = kwargs.get('host', self._ARGS.get('host'))
        kwargs['port'] = kwargs.get('port', self._ARGS.get('port'))
        kwargs['url'] = self._AUTH_RES
        kwargs['pytan_help'] = HELPS.auth

        if self._CREDS.has_session_creds:
            try:
                self._CREDS.session_id = self.http_request(**kwargs)
            except AuthorizationError:
                self._CREDS.session_id = ''
                kwargs['headers'] = {}
                kwargs['headers'].update(self._CREDS.headers)
                kwargs['headers']['persistent'] = int(self._CREDS.persistent)
                kwargs['headers'].update(supplied_headers)
                self._CREDS.session_id = self.http_request(**kwargs)
        else:
            self._CREDS.session_id = self.http_request(**kwargs)

        if self._CREDS.has_session_creds:
            m = "Successfully authenticated and received a {} session id using {}"
            m = m.format(persist_type, auth_type)
            self.AUTHLOG.info(m)
        else:
            err = "Authentication failed, no {} session id received using {}"
            err = err.format(persist_type, auth_type)
            raise AuthorizationError(err)

        self.get_userinfo()

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
        kwargs['command'] = 'GetObject'
        kwargs['obj'] = obj
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
        kwargs['command'] = 'UpdateObject'
        kwargs['obj'] = obj
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
        kwargs['command'] = 'AddObject'
        kwargs['obj'] = obj
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
        kwargs['command'] = 'DeleteObject'
        kwargs['obj'] = obj
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
        kwargs['command'] = 'RunPlugin'
        kwargs['obj'] = obj
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
        kwargs['command'] = 'GetResultInfo'
        kwargs['obj'] = obj
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
        kwargs['command'] = 'GetResultData'
        kwargs['obj'] = obj
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
        kwargs['command'] = 'GetResultData'
        kwargs['obj'] = obj
        response_body = self.soap_request(**kwargs)

        # if there is an export_id node, return the contents of that
        regex_args = {'body': response_body, 'element': 'export_id'}
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
        self.authenticate(**kwargs)
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
            self.get_userinfo(**kwargs)

        if self._invalid_server_version():
            self._get_version_from_info(**kwargs)

        result = self.SERVER_VERSION
        return result

    def soap_request(self, command, obj, **kwargs):
        """xxx."""
        self.authenticate(**kwargs)

        a = [
            'clean_xml_restricted', 'clean_xml_invalid',
            'connect_secs_soap', 'response_secs_soap',
        ]
        kwargs.update({k: kwargs.get(k, self._ARGS[k]) for k in a})

        extract_version = kwargs.get('extract_version', False)

        # build the options XML for the XML request body
        options_obj = tanium_ng.Options(values=kwargs)
        options = to_xml(options_obj)

        # turn obj into XML for the XML request body
        object_list = to_xml(obj, **kwargs)

        # build the XML request body
        subs = {'command': command, 'object_list': object_list, 'options': options}
        body_str = SOAP_REQUEST_BODY.format(**XMLNS)
        body_template = string.Template(body_str)
        body = body_template.substitute(**subs)

        headers = {}
        headers['Content-Type'] = SOAP_CONTENT_TYPE
        headers.update(kwargs.get('headers', {}))

        kwargs['url'] = kwargs.get('url', self._SOAP_RES)
        kwargs['headers'] = headers
        kwargs['body'] = body
        kwargs['connect_secs'] = kwargs['connect_secs_soap']
        kwargs['response_secs'] = kwargs['response_secs_soap']
        kwargs['request_method'] = 'post'

        sent = datetime.datetime.utcnow()

        # use the authenticated http request method to get a response
        result = self.http_request_auth(**kwargs)

        received = datetime.datetime.utcnow()
        elapsed = received - sent

        if extract_version:
            regex_args = {'body': result, 'element': 'server_version', 'fail': False}
            version = self._regex_body_for_element(**regex_args)
            if version:
                self.SERVER_VERSION = version

        regex_args = {'body': result, 'element': 'command'}
        response_command = self._regex_body_for_element(**regex_args).replace('\n', ' ').strip()

        self.LAST_RESPONSE_INFO = {}
        self.LAST_RESPONSE_INFO['request_command'] = command
        self.LAST_RESPONSE_INFO['request_args'] = kwargs
        self.LAST_RESPONSE_INFO['request_obj'] = obj
        self.LAST_RESPONSE_INFO['sent'] = sent
        self.LAST_RESPONSE_INFO['received'] = received
        self.LAST_RESPONSE_INFO['elapsed'] = elapsed
        self.LAST_RESPONSE_INFO['response_command'] = response_command

        # m = "HTTP Response: Timing info -- SENT: {}, RECEIVED: {}, ELAPSED: {}".format
        # self.HTTPLOG.debug(m(sent, received, elapsed))

        if 'forbidden' in response_command.lower():
            err = "Access forbidden when performing command {}! Server response: {}"
            err = err.format(command, response_command)
            raise AuthorizationError(err)

        if response_command != command:
            for p in self._CMD_PRUNES:
                response_command = response_command.replace(p, '').strip()

            err = "Response command {} does not match request command {}"
            err = err.format(response_command, command)
            raise BadResponseError(err)

        return result

    def http_request_auth(self, **kwargs):
        current_try = 0
        a = ['session_fallback', 'retry_count', 'host', 'port']
        kwargs.update({k: kwargs.get(k, self._ARGS[k]) for k in a})
        supplied_headers = kwargs.get('headers', {}) or {}

        while True:
            current_try += 1

            kwargs['headers'] = {}
            kwargs['headers'].update(self._CREDS.headers)
            kwargs['headers'].update(supplied_headers)

            auth_error = None
            http_error = None

            try:
                result = self.http_request(**kwargs)
                break
            except AuthorizationError as e:
                auth_error = e
            except HttpError as e:
                http_error = e

            if http_error:
                err = "HttpError on attempt {} out of {}: {}"
                err = err.format(current_try, kwargs['retry_count'], http_error)
                self.MYLOG.info(err)

                if current_try > kwargs['retry_count'] or not kwargs['retry_count']:
                    raise HttpError(err)

            if auth_error:
                has_normal_creds = self._CREDS.has_normal_creds
                has_session_creds = self._CREDS.has_session_creds
                session_fallback = kwargs.get('session_fallback', True)

                err = "Auth failed with session fallback = {}, msg: {}, credentials:\n{}"
                err = err.format(session_fallback, auth_error, self._CREDS)
                self.AUTHLOG.info(err)

                if has_session_creds and has_normal_creds and session_fallback:
                    self._CREDS.session_id = ''
                    self.authenticate(**kwargs)
                    continue

                raise AuthorizationError(err)
        return result

    def http_request(self, host, port, url, **kwargs):
        """This is an HTTP GET / POST method that utilizes the :mod:`requests` package."""
        # get any headers that may have been supplied
        supplied_headers = kwargs.get('headers', {}) or {}

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

        if not response.ok or response.status_code in self._AUTH_FAIL_CODES:
            err = "{0}: returned code: {1.status_code}, body: {2}"
            err = err.format(pre, response, response_body)
            raise AuthorizationError(err)

        if not response_body and not empty_ok:
            err = "{0}: returned empty body"
            err = err.format(pre)
            raise HttpError(err)

        return response_body

    def get_pretty_bodies(self, **kwargs):
        """Uses :func:`xml_pretty` to pretty print the last request and response bodies from the
        session object

        """
        response = kwargs.get('response', self.LAST_RESPONSE)

        request_body = response.request.body
        response_body = response.text

        try:
            req = xml_pretty(request_body)
        except Exception as e:
            req = "Failed to prettify xml: {}, raw xml:\n{}".format(e, request_body)

        try:
            resp = xml_pretty(response_body)
        except Exception as e:
            resp = "Failed to prettify xml: {}, raw xml:\n{}".format(e, response_body)

        result = (req, resp)
        return result

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

    def _regex_body_for_element(self, body, element, **kwargs):
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
        fail = kwargs.get('fail', True)
        char_limit = kwargs.get('char_limit', 500)

        regex_txt = self._ELEMENT_RE_TXT.format(element)
        regex = re.compile(regex_txt, re.IGNORECASE | re.DOTALL)

        result = regex.search(body[0:char_limit])

        if not result and fail:
            err = "Unable to find {} in body: {}"
            err = err.format(regex.pattern, body)
            raise BadResponseError(err)

        if result:
            result = str(result.groups()[0].strip())
        else:
            result = ''

        m = "Value of element '{}': '{}' (using pattern: '{}') in 0:{} of body with {}"
        m = m.format(element, result, regex.pattern, char_limit, len(body))
        self.MYLOG.debug(m)
        return result

    def _invalid_server_version(self):
        """Utility method to find out if self.SERVER_VERSION is valid or not"""
        result = False
        if getattr(self, 'SERVER_VERSION', '') in self._INVALID_VERSIONS:
            result = True
        return result

    def _get_version_from_info(self, **kwargs):
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

    def get_userinfo(self, **kwargs):
        result = self._CREDS.user_obj
        if not result:
            session_user_id = self.session_id.split('-')[0]
            user_obj = tanium_ng.User(values={'id': session_user_id})
            kwargs['extract_version'] = True
            kwargs['pytan_help'] = HELPS.getuser
            result = self.find(user_obj, **kwargs)
            m = "Successfully retrieved user info: {}"
            m = m.format(result)
            self.AUTHLOG.info(m)
            self._CREDS.user_obj = result
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
            raise NetworkError(err)
