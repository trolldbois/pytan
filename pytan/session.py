"""Session classes for the :mod:`pytan` module."""

import re
import time
import json
import string
import logging
import threading

from datetime import datetime
from base64 import b64encode

from pytan import b
from pytan import requests, tanium_ng, tickle
from pytan.utils import exceptions, tools, helpstr, xml_cleaner
from pytan.utils.version import __version__

requests.packages.urllib3.disable_warnings()

mylog = logging.getLogger(__name__)
authlog = logging.getLogger(__name__ + ".auth")
httplog = logging.getLogger(__name__ + ".http")
bodylog = logging.getLogger(__name__ + ".body")
statslog = logging.getLogger(__name__ + ".stats")
helplog = logging.getLogger(__name__ + ".help")


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

    _XMLNS = {
        'SOAP-ENV': 'xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"',
        'xsd': 'xmlns:xsd="http://www.w3.org/2001/XMLSchema"',
        'xsi': 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        'typens': 'xmlns:typens="urn:TaniumSOAP"',
    }
    """The namespace mappings for use in XML Request bodies"""

    _REQUEST_BODY_BASE = (
        '<SOAP-ENV:Envelope {SOAP-ENV} {xsd} {xsi}>\n'
        '<SOAP-ENV:Body>\n'
        '  <typens:tanium_soap_request {typens}>\n'
        '    <command>$command</command>\n'
        '    <object_list>$object_list</object_list>\n'
        '    $options\n'
        '  </typens:tanium_soap_request>\n'
        '</SOAP-ENV:Body>\n'
        '</SOAP-ENV:Envelope>\n'
    )
    """The XML template used for all SOAP Requests in string form"""

    _REQUESTS_SESSION = None
    """
    The Requests session allows you to persist certain parameters across requests. It also
    persists cookies across all requests made from the Session instance. Any requests that you
    make within a session will automatically reuse the appropriate connection
    """

    _AUTH_RES = 'auth'
    """The URL to use for authentication requests"""

    _SOAP_RES = 'soap'
    """The URL to use for SOAP requests"""

    _INFO_RES = 'info.json'
    """The URL to use for server info requests"""

    _AUTH_CONNECT_TIMEOUT_SEC = 5
    """number of seconds before timing out for a connection while authenticating"""

    _AUTH_RESPONSE_TIMEOUT_SEC = 15
    """number of seconds before timing out for a response while authenticating"""

    _INFO_CONNECT_TIMEOUT_SEC = 5
    """number of seconds before timing out for a connection while getting server info"""

    _INFO_RESPONSE_TIMEOUT_SEC = 15
    """number of seconds before timing out for a response while getting server info"""

    _SOAP_CONNECT_TIMEOUT_SEC = 15
    """number of seconds before timing out for a connection while sending a SOAP Request"""

    _SOAP_RESPONSE_TIMEOUT_SEC = 540
    """number of seconds before timing out for a response while sending a SOAP request"""

    _REQUEST_HEADERS = {
        'Accept-Encoding': 'gzip',
        'User-Agent': 'PyTan/{}'.format(__version__)
    }
    """dictionary of headers to add to every HTTP GET/POST"""

    _ELEMENT_RE_TXT = r'<{0}>(.*?)</{0}>'
    """regex string to search for an element in XML bodies"""

    _HTTP_RETRY_COUNT = 5
    """number of times to retry HTTP GET/POST's if the connection times out/fails"""

    _HTTP_AUTH_RETRY = True
    """retry HTTP GET/POST's with username/password if session_id fails or not"""

    _BAD_RESPONSE_CMD_PRUNES = [
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

    _BAD_SERVER_VERSIONS = [None, '', 'Unable to determine', 'Not yet determined']
    """List of server versions that are not valid"""

    _HOST = None
    """host to connect to"""

    _PORT = 443
    """port to connect to"""

    _SESSION_ID = ''
    _USERNAME = ''
    _PASSWORD = ''
    _DOMAIN = ''
    _SECONDARY = ''
    _PERSISTENT = False

    RECORD_ALL_REQUESTS = False
    """Controls whether each requests response object is appended to the
    self.ALL_REQUESTS_RESPONSES list
    """

    ALL_REQUESTS_RESPONSES = []
    """Holds ALL of the requests response object that was received"""

    LAST_REQUESTS_RESPONSE = None
    """Holds the last requests response object that was received"""

    LAST_RESPONSE_INFO = {}
    """Holds the information about the last response received by soap_request()"""

    FORCE_SERVER_VERSION = ''
    """In the case where the user wants to have pytan act as if the server is a specific version,
    regardless of what server_version is.
    """

    SERVER_VERSION = "Not yet determined"
    """version string of server, will be updated when get_server_version() is called"""

    SERVER_INFO = {}
    """Holds the return from /info.json"""

    STATS_LOOP_ENABLED = False
    """enable the statistics loop thread or not"""

    STATS_LOOP_SLEEP_SEC = 5
    """seconds to sleep in between printing the statistics when stats_loop_enabled is True
    """

    STATS_LOOP_TARGETS = [
        {'Version': 'Settings/Version'},
        {'Active Questions': 'Active Question Cache/Active Question Estimate'},
        {'Clients': 'Active Question Cache/Active Client Estimate'},
        {'Strings': 'String Cache/Total String Count'},
        {'Handles': 'System Performance Info/HandleCount'},
        {'Processes': 'System Performance Info/ProcessCount'},
        {'Memory Available': (
            'percentage(System Performance Info/PhysicalAvailable,System Performance Info/'
            'PhysicalTotal)'
        )
        },
    ]
    """list of dictionaries with the key being the section of info.json to print info from, and
    the value being the item with in that section to print the value
    """

    def __init__(self, host, **kwargs):
        self._REQUESTS_SESSION = requests.Session()

        # disable SSL cert verification for all requests made in this session
        self._REQUESTS_SESSION.verify = False

        self._HOST = host
        self._PORT = kwargs.get('port', self._PORT)

        # kwargs overrides for object properties
        priv_args = [
            'REQUEST_HEADERS',
            'HTTP_AUTH_RETRY',
            'HTTP_RETRY_COUNT',
            'AUTH_CONNECT_TIMEOUT_SEC',
            'AUTH_RESPONSE_TIMEOUT_SEC',
            'INFO_CONNECT_TIMEOUT_SEC',
            'INFO_RESPONSE_TIMEOUT_SEC',
            'SOAP_CONNECT_TIMEOUT_SEC',
            'SOAP_RESPONSE_TIMEOUT_SEC',
        ]
        [setattr(self, '_' + k, kwargs.get(k.lower(), getattr(self, '_' + k))) for k in priv_args]

        reg_args = [
            'STATS_LOOP_SLEEP_SEC',
            'STATS_LOOP_TARGETS',
            'STATS_LOOP_ENABLED',
            'RECORD_ALL_REQUESTS',
            'FORCE_SERVER_VERSION',
        ]
        [setattr(self, k, kwargs.get(k.lower(), getattr(self, k))) for k in reg_args]

        # re-enforce empty variables for init of session
        self.ALL_REQUESTS_RESPONSES = []
        self.LAST_RESPONSE_INFO = {}
        self.LAST_REQUESTS_RESPONSE = None
        self.SERVER_VERSION = "Not yet determined"

        # test our connectivity to the Tanium server
        tools.test_app_port(self._HOST, self._PORT)

        # authenticate to the Tanium server
        self.authenticate(**kwargs)

    def __str__(self):
        myname = self.__class__.__name__
        ver = self.get_server_version()
        auth_type = self._get_auth_type()
        m = "{} to {}:{}, Auth Type: {}, Platform Version: {}"
        result = m.format(myname, self._HOST, self._PORT, auth_type, ver)
        return result

    def __repr__(self):
        return self.__str__()

    @property
    def session_id(self):
        """Property to fetch the session_id for this object

        Returns
        -------
        self._SESSION_ID : str
        """
        result = self._SESSION_ID
        return result

    @session_id.setter
    def session_id(self, value):
        """Setter to update the session_id for this object"""
        if self.session_id != value:
            self._SESSION_ID = value
            m = "Session ID updated to: {}"
            m = m.format(value)
            authlog.debug(m)

    def logout(self, **kwargs):
        """Logout a given session_id from Tanium. If not session_id currently set, it will
        authenticate to get one.

        Parameters
        ----------
        all_session_ids : bool, optional
            * default: False
            * False: only log out the current session id for the current user
            * True: log out ALL session id's associated for the current user
        """
        all_session_ids = kwargs.get('all_session_ids', False)

        if not self.session_id:
            self.authenticate(**kwargs)

        if all_session_ids:
            logout = 1
        else:
            logout = 0

        headers = {}
        headers['session'] = self.session_id
        headers['logout'] = logout

        kwargs['url'] = self._AUTH_RES
        kwargs['headers'] = headers
        kwargs['retry_count'] = False
        kwargs['request_method'] = 'get'

        try:
            self.http_request_auth(**kwargs)
        except Exception as e:
            m = "logout exception: {}".format
            authlog.info(m(e))

        self.session_id = ''

        if all_session_ids:
            txt = "all"
        else:
            txt = "current"

        m = "Successfully logged out {} session ids for current user"
        m = m.format(txt)
        authlog.info(m)

    def check_auth_args(self):
        """pass."""
        if not self.session_id and not self._USERNAME:
            err = "Must supply username"
            mylog.critical(err)
            raise exceptions.AuthorizationError(err)

        if not self.session_id and not self._PASSWORD:
            err = "Must supply password"
            mylog.critical(err)
            raise exceptions.AuthorizationError(err)

        if self.session_id and self._PERSISTENT:
            err = "Unable to establish a persistent session when authenticating via session_id"
            mylog.critical(err)
            raise exceptions.AuthorizationError(err)

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
        # the 4 fields that /auth takes for non session auth
        # print("auth kwargs:", kwargs)
        auth_args = ['username', 'password', 'domain', 'secondary', 'session_id', 'persistent']
        for k in auth_args:
            # print("self attr name: ", x)
            # v = getattr(self, x)
            # print("self attr val before: ", v)
            if k not in kwargs or not kwargs.get(k, ''):
                continue
            x = '_' + k.upper()
            v = kwargs.get(k)
            setattr(self, x, v)
            # v = getattr(self, x)
            # print("self attr val after: ", v)

        self.check_auth_args()

        # the time outs for authentication attempts
        connect_timeout = kwargs.get('connect_timeout', self._AUTH_CONNECT_TIMEOUT_SEC)
        response_timeout = kwargs.get('response_timeout', self._AUTH_RESPONSE_TIMEOUT_SEC)

        # disable http retry logic by default for auth attempts
        retry_count = kwargs.get('retry_count', 0)

        auth_headers = {}

        if self._PERSISTENT:
            auth_headers['persistent'] = 1

        kwargs['url'] = self._AUTH_RES
        kwargs['headers'] = auth_headers
        kwargs['retry_count'] = retry_count
        kwargs['connect_timeout'] = connect_timeout
        kwargs['response_timeout'] = response_timeout
        kwargs['pytan_help'] = helpstr.AUTH
        kwargs['request_method'] = 'get'

        try:
            self.session_id = self.http_request_auth(**kwargs)
        except exceptions.HttpError as e:
            err = "HTTP Error while trying to authenticate: {}"
            err = err.format(e)
            mylog.exception(err)
            raise
        except exceptions.AuthorizationError as e:
            err = "Authentication Failed: {}"
            err = err.format(e)
            mylog.exception(err)
            raise exceptions.AuthorizationError(err)
        except:
            raise

        m = "Successfully authenticated and received a {} session id using {}"
        m = m.format(self._get_session_type(), self._get_auth_type())
        authlog.info(m)

        # start the stats thread loop in a background thread
        self._start_stats_thread(**kwargs)

    def _get_session_type(self):
        """pass."""
        if self._PERSISTENT:
            result = "persistent (up to 1 week)"
        else:
            result = "non-persistent (up to 5 minutes)"
        return result

    def platform_is_6_5(self, **kwargs):
        """Check to see if self.SERVER_VERSION is less than 6.5

        Returns
        -------
        is6_5 : bool
            * True if self.FORCE_SERVER_VERSION is greater than or equal to 6.5
            * True if self.SERVER_VERSION is greater than or equal to 6.5
            * False if self.SERVER_VERSION is less than 6.5
        """
        if self.FORCE_SERVER_VERSION:
            if self.FORCE_SERVER_VERSION >= '6.5':
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
        kwargs['obj'] = obj
        kwargs['request_body'] = self._create_get_object_body(**kwargs)
        response_body = self.soap_request(**kwargs)
        result = tickle.from_xml(response_body)
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
        kwargs['obj'] = obj
        kwargs['request_body'] = self._create_update_object_body(**kwargs)
        response_body = self.soap_request(**kwargs)
        result = tickle.from_xml(response_body)
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
        kwargs['obj'] = obj
        kwargs['request_body'] = self._create_add_object_body(**kwargs)
        response_body = self.soap_request(**kwargs)
        result = tickle.from_xml(response_body)
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
        kwargs['obj'] = obj
        kwargs['request_body'] = self._create_delete_object_body(**kwargs)
        response_body = self.soap_request(**kwargs)
        result = tickle.from_xml(response_body)
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
        kwargs['obj'] = obj
        kwargs['request_body'] = self._create_run_plugin_object_body(**kwargs)
        response_body = self.soap_request(**kwargs)
        result = tickle.from_xml(response_body)
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
        kwargs['obj'] = obj
        kwargs['request_body'] = self._create_get_result_info_body(**kwargs)
        response_body = self.soap_request(**kwargs)
        result = tickle.from_xml(response_body)
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
        kwargs['obj'] = obj
        kwargs['request_body'] = self._create_get_result_data_body(**kwargs)
        response_body = self.soap_request(**kwargs)
        result = tickle.from_xml(response_body)
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
        kwargs['obj'] = obj
        kwargs['request_body'] = self._create_get_result_data_body(**kwargs)
        response_body = self.soap_request(**kwargs)

        # if there is an export_id node, return the contents of that
        regex_args = {'body': response_body, 'element': 'export_id', 'fail': True}
        result = self._regex_body_for_element(**regex_args)
        return result

    def get_server_info(self, **kwargs):
        """Gets the /info.json

        Parameters
        ----------
        port : int, optional
            * default: None
            * port to attempt getting /info.json from, if not specified will use self._PORT
        fallback_port : int, optional
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
        port = kwargs.get('port', None)
        fallback_port = kwargs.get('fallback_port', 444)

        connect_timeout = kwargs.get('connect_timeout', self._INFO_CONNECT_TIMEOUT_SEC)
        response_timeout = kwargs.get('response_timeout', self._INFO_RESPONSE_TIMEOUT_SEC)

        kwargs['port'] = port or self._PORT
        kwargs['url'] = self._INFO_RES
        kwargs['retry_count'] = 0
        kwargs['connect_timeout'] = connect_timeout
        kwargs['response_timeout'] = response_timeout
        kwargs['pytan_help'] = helpstr.SERVINFO
        kwargs['request_method'] = 'get'

        info_body = ''
        server_info_pass_msgs = []
        server_info_fail_msgs = []
        ok_m = "Successfully retrieved server info from {}:{}/{}".format
        bad_m = "Failed to retrieve server info from {}:{}/{}, {}".format
        json_fail_m = "Failed to parse server info from json, error: {}".format
        diags_flat_fail_m = "Failed to flatten server info from json, error: {}".format

        try:
            info_body = self.http_request_auth(**kwargs)
            server_info_pass_msgs.append(ok_m(self._HOST, port, self._INFO_RES))
        except Exception as e:
            mylog.info(bad_m(self._HOST, port, self._INFO_RES, e))
            server_info_fail_msgs.append(bad_m(self._HOST, port, self._INFO_RES, e))

        if not info_body:
            kwargs['port'] = fallback_port
            try:
                info_body = self.http_request_auth(**kwargs)
                server_info_pass_msgs.append(ok_m(self._HOST, port, self._INFO_RES))
            except Exception as e:
                mylog.info(bad_m(self._HOST, port, self._INFO_RES, e))
                server_info_fail_msgs.append(bad_m(self._HOST, port, self._INFO_RES, e))

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
                mylog.info(m)

        result = str(result)
        self.SERVER_VERSION = result
        return result

    def get_server_stats(self, **kwargs):
        """Creates a str containing a number of stats gathered from /info.json

        Returns
        -------
        str
            * str containing stats from /info.json

        See Also
        --------
        :data:`pytan.sessions.Session.STATS_LOOP_TARGETS` : list of dict containing stat keys to
        pull from /info.json
        """
        try:
            si = self.get_server_info(**kwargs)
            diags = si['diags_flat']
            stats_resolved = [
                self._find_stat_target(target=t, diags=diags)
                for t in self.STATS_LOOP_TARGETS
            ]
            result = ", ".join(["{}: {}".format(*list(i.items())[0]) for i in stats_resolved])
        except Exception as e:
            result = "get_server_stats: Exception {}".format(e)
        return result

    def enable_stats_loop(self, **kwargs):
        """Enables the stats loop thread, which will print out the results of
        :func:`pytan.sessions.Session.get_server_stats` every
        :data:`pytan.sessions.Session.STATS_LOOP_SLEEP_SEC`

        Parameters
        ----------
        sleep : int, optional
            * when enabling the stats loop, update
            :data:`pytan.sessions.Session.STATS_LOOP_SLEEP_SEC` with `sleep`

        See Also
        --------
        :func:`pytan.sessions.Session._stats_loop` : method started as a thread which checks
        self.STATS_LOOP_ENABLED before running :func:`pytan.sessions.Session.get_server_stats`
        """
        sleep = kwargs.get('sleep', None)
        self.STATS_LOOP_ENABLED = True
        if isinstance(sleep, int):
            self.STATS_LOOP_SLEEP_SEC = sleep

    def disable_stats_loop(self, **kwargs):
        """Disables the stats loop thread, which will print out the results of
        :func:`pytan.sessions.Session.get_server_stats` every
        :data:`pytan.sessions.Session.STATS_LOOP_SLEEP_SEC`

        Parameters
        ----------
        sleep : int, optional
            * when disabling the stats loop, update
            :data:`pytan.sessions.Session.STATS_LOOP_SLEEP_SEC` with `sleep`

        See Also
        --------
        :func:`pytan.sessions.Session._stats_loop` : method started as a thread which checks
        self.STATS_LOOP_ENABLED before running :func:`pytan.sessions.Session.get_server_stats`
        """
        sleep = kwargs.get('sleep', None)
        self.STATS_LOOP_ENABLED = False
        if isinstance(sleep, int):
            self.STATS_LOOP_SLEEP_SEC = sleep

    def soap_request(self, request_body, **kwargs):
        """This is a wrapper around :func:`pytan.sessions.Session.http_post` for SOAP XML requests
        and responses.

        This method will update self.session_id if the response contains a different session_id
        than what is currently in this object.

        Parameters
        ----------
        request_body : str
            * the XML request body to send to the server
        retry_auth: bool, optional
            * default: True
            * True: retry authentication with username/password if session_id fails
            * False: throw exception if session_id fails

        Returns
        -------
        body : str
            * str containing body of response from server

        See Also
        --------
        :func:`pytan.sessions.Session.http_post` : wrapper method used to perform the HTTP POST
        """
        headers = kwargs.get('headers', {})
        retry_auth = kwargs.get('retry_auth', True)
        connect_timeout = kwargs.get('connect_timeout', self._SOAP_CONNECT_TIMEOUT_SEC)
        response_timeout = kwargs.get('response_timeout', self._SOAP_RESPONSE_TIMEOUT_SEC)

        headers['Content-Type'] = 'text/xml; charset=utf-8'

        kwargs['headers'] = headers
        kwargs['body'] = request_body
        kwargs['connect_timeout'] = connect_timeout
        kwargs['response_timeout'] = response_timeout
        kwargs['request_method'] = 'post'

        regex_args = {'body': request_body, 'element': 'command', 'fail': True}
        request_command = self._regex_body_for_element(**regex_args)
        sent = datetime.utcnow()

        # use the authenticated http request method to get a response
        result = self.http_request_auth(**kwargs)

        received = datetime.utcnow()
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
        httplog.debug(m(sent, received, elapsed))

        if 'forbidden' in response_command.lower():
            if retry_auth:
                m = "Last request was denied, re-authenticating with user/pass"
                authlog.info(m)

                # we may have hit the 5 minute expiration for session_id, empty out session ID,
                # re-authenticate, then retry request
                self._SESSION_ID = ''
                self.authenticate(**kwargs)

                # re-issue the request
                kwargs['retry_auth'] = False
                kwargs['request_body'] = request_body
                result = self.soap_request(**kwargs)
            else:
                err = "Access denied after re-authenticating! Server response: {}"
                err = err.format(response_command)
                raise exceptions.AuthorizationError(err)

        elif response_command != request_command:
            for p in self._BAD_RESPONSE_CMD_PRUNES:
                response_command = response_command.replace(p, '').strip()

            err = "Response command {} does not match request command {}"
            err = err.format(response_command, request_command)
            raise exceptions.BadResponseError(err)

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

    def _get_auth_type(self):
        """pass."""
        result = []
        if self._SESSION_ID:
            result.append("Session ID")

        elif self._USERNAME and self._PASSWORD:
            result.append("Username")
            result.append("Password")
            if self._DOMAIN:
                result.append("Domain")
            if self._SECONDARY:
                result.append("Secondary")
        else:
            err = "Authentication type unknown!"
            raise exceptions.AuthorizationError(err)

        result = ', '.join(result)
        return result

    # TODO: MOVE TO TOOLS
    def _b64encode(self, val):
        """pass."""
        result = b64encode(b(val))
        return result

    def _replace_credentials(self, headers):
        """pass."""
        removes = ['username', 'password', 'session', 'domain', 'secondary']
        result = {k: v for k, v in headers.items() if k not in removes}

        if self.session_id:
            result['session'] = self.session_id
        elif self._USERNAME and self._PASSWORD:
            result['username'] = self._b64encode(self._USERNAME)
            result['password'] = self._b64encode(self._PASSWORD)
            if self._DOMAIN:
                result['domain'] = self._DOMAIN
            if self._SECONDARY:
                result['secondary'] = self._SECONDARY
        else:
            err = "Authentication type unknown!"
            mylog.critical(err)
            raise exceptions.AuthorizationError(err)
        return result

    def http_request_auth(self, **kwargs):
        """This is an authenticated HTTP method. It will always forcibly use the authentication
        credentials that are stored in the current object when performing an HTTP request.
        """
        headers = kwargs.get('headers', {})
        connect_timeout = kwargs.get('connect_timeout', self._SOAP_CONNECT_TIMEOUT_SEC)
        response_timeout = kwargs.get('response_timeout', self._SOAP_RESPONSE_TIMEOUT_SEC)
        auth_retry = kwargs.get('auth_retry', self._HTTP_AUTH_RETRY) or False
        retry_count = kwargs.get('retry_count', self._HTTP_RETRY_COUNT) or 0
        request_method = kwargs.get('request_method', 'get')
        host = kwargs.get('server', self._HOST)
        port = kwargs.get('port', self._PORT)
        url = kwargs.get('url', self._SOAP_RES)

        headers = self._replace_credentials(headers)

        auth_type = self._get_auth_type()
        m = "Using {} for authentication headers"
        m = m.format(auth_type)
        authlog.info(m)

        kwargs['host'] = host
        kwargs['port'] = port
        kwargs['url'] = url
        kwargs['headers'] = headers
        kwargs['connect_timeout'] = connect_timeout
        kwargs['response_timeout'] = response_timeout
        kwargs['request_method'] = request_method

        try:
            retry_count = int(retry_count)
        except:
            retry_count = 0

        current_try = 1

        while True:
            try:
                result = self.http_request(**kwargs)
                break
            except exceptions.AuthorizationError:
                if self._SESSION_ID and auth_retry:
                    self._SESSION_ID = ''
                    self.authenticate()
                    kwargs['auth_retry'] = False
                    result = self.http_request_auth(**kwargs)
                else:
                    raise
            except Exception as e:
                if retry_count == 0:
                    raise

                err = "{} failed on attempt {} out of {}: {}"
                err = err.format(request_method, current_try, retry_count, e)
                mylog.info(err)

                if current_try >= retry_count:
                    mylog.critical(err)
                    raise

                current_try += 1
        return result

    def http_request(self, host, port, url, **kwargs):
        """This is an HTTP GET / POST method that utilizes the :mod:`requests` package.

        Parameters
        ----------
        host : str
            * host to connect to
        port : int
            * port to connect to
        url : str
            * url to fetch on the server
        headers : dict, optional
            * default: None
            * headers to supply as part of POST request
        connect_timeout : int, optional
            * default: 15
            * timeout in seconds for connection to host
        response_timeout : int, optional
            * default: 180
            * timeout in seconds for response from host
        pytan_help : str, optional
            * default: ''
            * help string to add to self.LAST_REQUESTS_RESPONSE.pytan_help
        perform_xml_clean : bool, optional
            * default: False
            * False: Do not run the response_body through an XML cleaner
            * True: Run the response_body through an XML cleaner before returning it
        clean_restricted : bool, optional
            * default: True
            * True: When XML cleaning the response_body, remove restricted characters as well
            as invalid characters
            * False: When XML cleaning the response_body, remove only invalid characters
        log_clean_messages : bool, optional
            * default: True
            * True: When XML cleaning the response_body, enable logging messages about invalid/
            restricted matches
            * False: When XML cleaning the response_body, disable logging messages about invalid/
            restricted matches
        log_bad_characters : bool, optional
            * default: False
            * False: When XML cleaning the response_body, disable logging messages about the
            actual characters that were invalid/restricted
            * True: When XML cleaning the response_body, enable logging messages about the actual
            characters that were invalid/restricted

        Returns
        -------
        body : str
            * str containing body of response from server
        """
        headers = kwargs.get('headers', {})
        headers.update(self._REQUESTS_SESSION.headers)
        headers.update(self._REQUEST_HEADERS)

        connect_timeout = kwargs.get('connect_timeout', self._SOAP_CONNECT_TIMEOUT_SEC)
        response_timeout = kwargs.get('response_timeout', self._SOAP_RESPONSE_TIMEOUT_SEC)
        request_method = kwargs.get('request_method', 'get')
        empty_ok = kwargs.get('empty_ok', False)
        body = kwargs.get('body', '')
        pytan_help = kwargs.get('pytan_help', "NO HELP SUPPLIED")

        full_url = self._get_full_url(host=host, port=port, url=url)

        pre = "HTTP {} request: '{}': len:{}"
        pre = pre.format(request_method.upper(), full_url, len(body))
        httplog.info(pre)

        clean_headers = {}
        clean_headers.update(headers)
        if 'password' in clean_headers:
            clean_headers['password'] = '**PASSWORD**'

        m = "{}: headers: {}"
        m = m.format(pre, clean_headers)
        httplog.debug(m)

        pytan_help = "{} - {}".format(pytan_help, pre)
        helplog.info(pytan_help)

        req_args = {}
        req_args['headers'] = headers
        req_args['timeout'] = (connect_timeout, response_timeout)

        if request_method.lower() == 'post':
            m = "{}: body:\n{}"
            m = m.format(pre, body)
            bodylog.debug(m)

            req_args['data'] = body
            kwargs['perform_xml_clean'] = kwargs.get('perform_xml_clean', True)

        requests_func = getattr(self._REQUESTS_SESSION, request_method)

        try:
            response = requests_func(full_url, **req_args)
        except Exception as e:
            err = "HTTP response: {} request to '{}' failed: {}"
            err = err.format(request_method.upper(), full_url, e)
            mylog.exception(err)
            raise exceptions.HttpError(err)

        self.LAST_REQUESTS_RESPONSE = response
        if self.RECORD_ALL_REQUESTS:
            self.ALL_REQUESTS_RESPONSES.append(response)

        response.pytan_help = pytan_help
        response_body = response.text

        kwargs['text'] = response_body
        response_body = xml_cleaner(**kwargs)

        pre = "HTTP {} response: '{}'"
        pre = pre.format(request_method.upper(), full_url)

        m = "{0}: len:{1}, status:{2.status_code} {2.reason}"
        m = m.format(pre, len(response_body), response)
        httplog.info(m)

        m = "{0}: headers: {1.headers}"
        m = m.format(pre, response)
        httplog.debug(m)

        m = "{0}: body:\n{1}"
        m = m.format(pre, response_body)
        bodylog.debug(m)

        if response.status_code in self._AUTH_FAIL_CODES:
            err = "{0}: returned code: {1.status_code}, body: {2}"
            err = err.format(pre, response, response_body)
            raise exceptions.AuthorizationError(err)

        if not response.ok:
            err = "{0}: returned code: {1.status_code}, body: {2}"
            err = err.format(pre, response, response_body)
            raise exceptions.HttpError(err)

        if not response_body and not empty_ok:
            err = "{0}: returned empty body"
            err = err.format(pre)
            raise exceptions.HttpError(err)
        return response_body

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
        # TODO MOVE TO TOOLS
        url = kwargs.get('url', '')
        host = kwargs.get('host', self._HOST)
        port = kwargs.get('port', self._PORT)
        schema = kwargs.get('schema', 'https')
        result = "{0}://{1}:{2}/{3}"
        result = result.format(schema, host, port, url)
        return result

    def get_last_bodies(self):
        """Uses :func:`xml_pretty` to pretty print the last request and response bodies from the
        session object

        """
        request_body = self.LAST_REQUESTS_RESPONSE.request.body
        response_body = self.LAST_REQUESTS_RESPONSE.text
        try:
            req = tools.xml_pretty(request_body)
        except Exception as e:
            req = "Failed to prettify xml: {}, raw xml:\n{}".format(e, request_body)

        try:
            resp = tools.xml_pretty(response_body)
        except Exception as e:
            resp = "Failed to prettify xml: {}, raw xml:\n{}".format(e, response_body)
        return req, resp

    def _start_stats_thread(self, **kwargs):
        """Utility method starting the :func:`pytan.sessions.Session._stats_loop` method in a
        threaded daemon"""
        stats_thread = threading.Thread(target=self._stats_loop, args=(), kwargs=kwargs)
        stats_thread.daemon = True
        stats_thread.start()

    def _stats_loop(self, **kwargs):
        """Utility method for logging server stats via
        :func:`pytan.sessions.Session.get_server_stats` every self.STATS_LOOP_SLEEP_SEC"""
        while True:
            if self.STATS_LOOP_ENABLED:
                server_stats = self.get_server_stats(**kwargs)
                statslog.warning(server_stats)
            time.sleep(self.STATS_LOOP_SLEEP_SEC)

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

    def _find_stat_target(self, target, diags):
        """Utility method for finding a target in info.json and returning the value, optionally
        performing a percentage calculation on two values if the target[0] starts with percentage(

        Parameters
        ----------
        target : list
            * index0 : label : human friendly name to refer to search_path
            * index1 : search_path : / seperated search path to find a given value from info.json
        diags : dict
            * flattened dictionary of info.json diagnostics

        Returns
        -------
        dict
            * label : same as provided in `target` index0 (label)
            * result : value resolved from :func:`pytan.sessions.Session._resolve_stat_target` for
            `target` index1 (search_path)
        """
        try:
            label, search_path = target.items()[0]
            if search_path.startswith('percentage('):
                points = search_path.lstrip('percentage(').rstrip(')')
                points = [self._resolve_stat_target(p, diags) for p in points.split(',')]
                try:
                    txt = tools.get_percent(base=points[0], amount=points[1], text=True)
                except:
                    txt = ', '.join(points)
            else:
                txt = self._resolve_stat_target(search_path, diags)
            result = {label: txt}
        except Exception as e:
            label = "Parse Failure"
            txt = "Unable to parse stat target: {}, exception: {}".format(target, e)
            result = {label: txt}
        return result

    def _resolve_stat_target(self, search_path, diags):
        """Utility method for resolving the value of search_path in info.json and returning the value

        Parameters
        ----------
        search_path : str
            * / seperated search path to find a given value from info.json
        diags : dict
            * flattened dictionary of info.json diagnostics

        Returns
        -------
        str
            * value resolved from `diags` for `search_path`
        """
        try:
            for i in search_path.split('/'):
                result = diags.get(i)
        except Exception as e:
            result = "Unable to find diagnostic: {}, exception: {}"
            result = result.format(search_path, e)
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
            * The XML request body created from the string.template self.REQUEST_BODY_TEMPLATE
        """
        options_obj = tickle.create_options_obj(**kwargs)
        options = tickle.to_xml(options_obj)

        body_template = string.Template(self._REQUEST_BODY_BASE.format(**self._XMLNS))
        subs = {'command': command, 'object_list': object_list, 'options': options}
        result = body_template.substitute(**subs)
        return result

    def _create_run_plugin_object_body(self, obj, **kwargs):
        """Utility method for building an XML Request Body to run a plugin

        Parameters
        ----------
        obj : :class:`tanium_ng.BaseType`
            * object to convert into XML
        kwargs : dict, optional
            * any number of attributes that can be set via
            :class:`tanium_ng.Options` that control the servers response.

        Returns
        -------
        obj_body : str
            * The XML request body created from :func:`pytan.sessions.Session._build_body`
        """
        kwargs['object_list'] = tickle.to_xml(obj)
        kwargs['command'] = 'RunPlugin'
        result = self._build_body(**kwargs)
        return result

    def _create_add_object_body(self, obj, **kwargs):
        """Utility method for building an XML Request Body to add an object

        Parameters
        ----------
        obj : :class:`tanium_ng.BaseType`
            * object to convert into XML
        kwargs : dict, optional
            * any number of attributes that can be set via
            :class:`tanium_ng.Options` that control the servers response.

        Returns
        -------
        obj_body : str
            * The XML request body created from :func:`pytan.sessions.Session._build_body`
        """
        kwargs['object_list'] = tickle.to_xml(obj)
        kwargs['command'] = 'AddObject'
        result = self._build_body(**kwargs)
        return result

    def _create_delete_object_body(self, obj, **kwargs):
        """Utility method for building an XML Request Body to delete an object

        Parameters
        ----------
        obj : :class:`tanium_ng.BaseType`
            * object to convert into XML
        kwargs : dict, optional
            * any number of attributes that can be set via
            :class:`tanium_ng.Options` that control the servers response.

        Returns
        -------
        obj_body : str
            * The XML request body created from :func:`pytan.sessions.Session._build_body`
        """
        kwargs['object_list'] = tickle.to_xml(obj)
        kwargs['command'] = 'DeleteObject'
        result = self._build_body(**kwargs)
        return result

    def _create_get_result_info_body(self, obj, **kwargs):
        """Utility method for building an XML Request Body to get result info for an object

        Parameters
        ----------
        obj : :class:`tanium_ng.BaseType`
            * object to convert into XML
        kwargs : dict, optional
            * any number of attributes that can be set via
            :class:`tanium_ng.Options` that control the servers response.

        Returns
        -------
        obj_body : str
            * The XML request body created from :func:`pytan.sessions.Session._build_body`
        """
        kwargs['object_list'] = tickle.to_xml(obj)
        kwargs['command'] = 'GetResultInfo'
        result = self._build_body(**kwargs)
        return result

    def _create_get_result_data_body(self, obj, **kwargs):
        """Utility method for building an XML Request Body to get result data for an object

        Parameters
        ----------
        obj : :class:`tanium_ng.BaseType`
            * object to convert into XML
        kwargs : dict, optional
            * any number of attributes that can be set via
            :class:`tanium_ng.Options` that control the servers response.

        Returns
        -------
        obj_body : str
            * The XML request body created from :func:`pytan.sessions.Session._build_body`
        """
        kwargs['object_list'] = tickle.to_xml(obj)
        kwargs['command'] = 'GetResultData'
        result = self._build_body(**kwargs)
        return result

    def _create_get_object_body(self, obj, **kwargs):
        """Utility method for building an XML Request Body to get an object

        Parameters
        ----------
        obj : :class:`tanium_ng.BaseType`
            * object to convert into XML
        kwargs : dict, optional
            * any number of attributes that can be set via
             :class:`tanium_ng.Options` that control the servers response.

        Returns
        -------
        obj_body : str
            * The XML request body created from :func:`pytan.sessions.Session._build_body`
        """
        if isinstance(obj, tanium_ng.BaseType):
            object_list = tickle.to_xml(obj)
        else:
            object_list = '<{}/>'.format(obj._soap_tag)

        kwargs['command'] = 'GetObject'
        kwargs['object_list'] = object_list
        obj_body = self._build_body(**kwargs)
        return obj_body

    def _create_update_object_body(self, obj, **kwargs):
        """Utility method for building an XML Request Body to update an object

        Parameters
        ----------
        obj : :class:`tanium_ng.BaseType`
            * object to convert into XML
        kwargs : dict, optional
            * any number of attributes that can be set via
            :class:`tanium_ng.Options` that control the servers response.

        Returns
        -------
        obj_body : str
            * The XML request body created from :func:`pytan.sessions.Session._build_body`
        """
        kwargs['object_list'] = tickle.to_xml(obj)
        kwargs['command'] = 'UpdateObject'
        result = self._build_body(**kwargs)
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
        mylog.debug(m)
        return ret

    def _invalid_server_version(self):
        """Utility method to find out if self.SERVER_VERSION is valid or not"""
        result = False
        if getattr(self, 'SERVER_VERSION', '') in self._BAD_SERVER_VERSIONS:
            result = True
        return result