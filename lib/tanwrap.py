#!/usr/bin/python -i
#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Tanium Python Wrapper Class

Like saran wrap. But not.

This requires Python 2.7 and Suds.
Suds can be found at: https://fedorahosted.org/suds/

Reference for Suds: https://fedorahosted.org/suds/wiki/Documentation
Reference for Tanium's SOAP API: http://kb.tanium.com/SOAP
'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '0.1'

# static variable for how many minutes a session id will be valid
SESSION_TIMEOUT = 5

# static variable to control whether or not SOAP Session IDs are included
# in any outputs
SHOW_SESSION_ID = False

import os
import sys
import logging
import getpass
#import inspect
#import tempfile
import socket
import time
import csv
import StringIO
from datetime import datetime
from collections import defaultdict
from xml.etree import cElementTree as ET

try:
    import suds
except:
    logging.critical(
        "Suds python library not available in PYTHONPATH, please download "
        "and install from https://fedorahosted.org/suds"
    )
    raise

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
path_adds = [my_dir]

for x in path_adds:
    if x not in sys.path:
        sys.path.append(x)

# for debugging support
from console_support import *

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

# debug log format; rather verbose, used for files only unless loglevel >= 1
lfdebug = logging.Formatter(
    '[%(lineno)-5d - %(filename)20s:%(funcName)s()] %(asctime)s\n'
    '%(levelname)-8s %(message)s'
)

# info log format; used for console output when loglevel = 0
lfinfo = logging.Formatter('%(levelname)-8s %(message)s')

# create a logger called apiwrap and set it's default level to DEBUG
logger = logging.getLogger("apiwrap")
logger.setLevel(logging.DEBUG)


def version_check(reqver):
    LOG_TPL = (
        "{}: {} version {}, required {}").format
    if not __version__ >= reqver:
        s = "Script and API Version mismatch!"
        logging.error(LOG_TPL(s, __file__, __version__, reqver))
        sys.exit(100)
    s = "Script and API Version match"
    logging.debug(LOG_TPL(s, __file__, __version__, reqver))


def logging_setup(loglevel=0):
    '''setup console logging'''
    # remove any old handlers, we're going to re-setup new handlers
    [logger.removeHandler(x) for x in logger.handlers]

    # add a console handler that goes to STDOUT
    console_handler = logging.StreamHandler(sys.__stdout__)
    console_handler.set_name('console')
    if loglevel == 0:
        # if loglevel is 0, set console handler to info level
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(lfinfo)
    else:
        # if loglevel is 1 or higher, set console handler to debug level
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(lfdebug)
    logging.getLogger().addHandler(console_handler)

    log_level_map = {
        # see soap messages (in & out) and http headers at lvl 2
        'suds.client': 2,
        # see more details about soap messages and http headers at lvl 3
        'suds.transport': 3,
        # see digestion of the schema at lvl 4
        'suds.xsd.schema': 4,
        # see digestion WSDL at lvl 5
        'suds.wsdl': 5,
    }

    for loggername, loggerlvl in log_level_map.iteritems():
        if loglevel >= loggerlvl:
            #print 'setting %s to DEBUG' % loggername
            logging.getLogger(loggername).setLevel(logging.DEBUG)
        else:
            #print 'setting %s to INFO' % loggername
            logging.getLogger(loggername).setLevel(logging.INFO)

'''
    # setup file logging
    if logfile:
        add_file_log(logfile)


def add_file_log(logfile=None, logdir=None):
    if not logfile:
        if not logdir:
            logdir = tempfile.gettempdir()
        parent_func = inspect.stack()[1][3]
        now = get_now()
        logfilename = ('{}_{}.log').format(parent_func, now)
        logfile = os.path.join(logdir, logfilename)
    basename = os.path.basename(logfile)
    try:
        [L.removeHandler(x) for x in L.handlers if x.name is basename]
        file_handler = logging.FileHandler(logfile)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(lfdebug)
        L.addHandler(file_handler)
        logging.info(('Logging to: {}').format(logfile))
        return logfile
    except Exception as e:
        logging.error((
            'Problem setting up file logging to {}: {}'
        ).format(logfile, e))
'''


def get_now():
    return human_time(time.localtime())


def human_time(t, format='%Y_%m_%d-%H_%M_%S-%Z'):
    if type(t) in [type(float()), type(int())]:
        t = time.localtime(t)
    return time.strftime(format, t)


def datetime_diff(t=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    datetime diff of now - time
    """
    now = datetime.now()

    if type(t) in [type(int()), type(float())]:
        dtdiff = now - datetime.fromtimestamp(t)
    elif isinstance(t, datetime):
        dtdiff = now - t
    else:
        dtdiff = now - now

    #second_dtdiff = dtdiff.seconds
    #minute_dtdiff = dtdiff.seconds / 60
    #hour_dtdiff = minute_dtdiff / 60
    #day_dtdiff = dtdiff.days
    return dtdiff


def port_check(address, port, timeout=5):
    try:
        return socket.create_connection((address, port), timeout)
    except:
        return False


def prompt_username():
    print('Username: '),
    username = sys.stdin.readline()
    return username.strip()


def prompt_password():
    password = getpass.getpass(('Password: '))
    return password.strip()


def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.iteritems():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


class SoapRequest(object):
    def __init__(self, query_type, query_params, query_object_list, command):
        super(SoapRequest, self).__init__()
        self.query_type = query_type
        self.query_params = query_params
        self.query_object_list = query_object_list
        self.command = command

    def __str__(self):
        sent = self.sent_human or "Not Yet Sent"
        STR_TPL = (
            "SoapRequest for {}: {}, Sent: {}"
        ).format
        ret = STR_TPL(self.query_type, self.query_params, sent)
        return ret

    def get_params(self, token):
        '''return a request parameters dictionary'''
        params = {}
        params.update(token)
        params['object_list'] = self.query_object_list
        params['command'] = self.command
        return params

    @property
    def sent_human(self):
        '''returns the time the request was sent in human friendly format
        '''
        if not hasattr(self, '_sent'):
            return None
        return human_time(self._sent)

    @property
    def sent(self):
        '''returns the time the request was sent'''
        if not hasattr(self, '_sent'):
            return None
        return self._sent

    @sent.setter
    def sent(self, value):
        '''sets the time the request was sent'''
        self._sent = value


class SoapResponse(object):

    def __init__(self, soap_uri, request, **kwargs):
        super(SoapResponse, self).__init__()
        self.soap_uri = soap_uri
        self.request = request
        for k, v in kwargs:
            setattr(self, k, v)

    def __str__(self):
        received = self.received_human or "Not Yet Sent"
        STR_TPL = (
            "SoapResponse from {}, Received: {}, Request: {}"
        ).format
        ret = STR_TPL(self.soap_uri, received, self.request)
        return ret

    @property
    def xml_raw(self):
        '''returns the xml for the response in raw text form'''
        xml_raw = '<noresponse/>'
        if hasattr(self.response, 'ResultXML'):
            xml_raw = self.response.ResultXML
        return xml_raw

    @property
    def xml_pretty(self):
        '''returns the xml for the response as a pretty XML string'''
        xml_pretty = ET.fromstring(self.xml_raw)
        indent(xml_pretty)
        xml_pretty = ET.tostring(xml_pretty)
        return xml_pretty

    @property
    def xml_tree(self):
        '''returns the xml for the response as an ElementTree object'''
        xml_tree = ET.XML(self.xml_raw)
        return xml_tree

    @property
    def xml_dict(self):
        '''returns the xml for the response as a dictionary object'''
        xml_dict = etree_to_dict(self.xml_tree)
        return xml_dict

    @property
    def xml_rows(self):
        '''returns the xml for the response as a list of lists, one
        for each row, headers in the first row
        '''
        xml_dict = self.xml_dict
        result_sets = xml_dict.get('result_sets', {})
        result_set = result_sets.get('result_set', {})

        # get headers from xml response result_set
        cs = result_set.get('cs', {})
        xml_headers = cs.get('c', [])

        # extract the name for the header of each column
        headers = [x.get('dn', None) for x in xml_headers]

        # get rows from xml response result_set
        rs = result_set.get('rs', {})
        r = rs.get('r', [])
        xml_rows = [x.get('c', []) for x in r]

        # extract the row values for each column
        rows = [[y.get('v', None) for y in x] for x in xml_rows]

        # prepend headers to rows
        rows.insert(0, headers)
        return rows

    @property
    def xml_csv(self):
        '''returns the xml for the response as a CSV string'''
        # TODO
        xml_rows = self.xml_rows
        csv_io = StringIO.StringIO()
        writer = csv.writer(csv_io, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(xml_rows)
        csv_io.seek(0)
        xml_csv = csv_io.read()
        return xml_csv

    @property
    def xml_excel(self):
        '''returns the xml for the response as an XML doc in StringIO obj'''
        logger.warn('NOT YET SUPPORTED')
        xml_excel = StringIO.StringIO()
        return xml_excel

    @property
    def response(self):
        if not hasattr(self, '_response'):
            return None
        return self._response

    @response.setter
    def response(self, value):
        self._response = value
        self.received = time.time()

    @property
    def session_id(self):
        '''returns the session ID from response'''
        if self.response is None:
            return None

        if not hasattr(self.response, 'session'):
            return None

        if not self.response.session:
            return None

        return self.response.session

    @property
    def authok(self):
        '''returns False if 'Forbidden' is in the 'command' attr returned
        from a SOAP response'''
        if not hasattr(self.response, 'command'):
            return None

        if 'Forbidden' in self.response.command:
            return False

        return True

    @property
    def received_human(self):
        '''returns the time the response was received in human friendly format
        '''
        if not hasattr(self, '_received'):
            return None
        return human_time(self._received)

    @property
    def received(self):
        '''returns the time the response was received
        '''
        if not hasattr(self, '_received'):
            return None
        return self._received

    @received.setter
    def received(self, value):
        '''sets the time the response was received
        '''
        self._received = value


class SoapAuth(object):
    def __init__(self, client):
        super(SoapAuth, self).__init__()
        self.client = client
        self._token = {}
        self.SESSION_TIMEOUT = SESSION_TIMEOUT

    def __str__(self):
        STR_TPL = (
            "SoapAuth {}"
        ).format
        ret = STR_TPL(self.token_type_details)
        return ret

    def update_token(self):
        '''updates self.token with either session ID or user/pass auth'''
        UPD_TPL = ("SOAP Token updated to: {}").format
        if self.session_id_valid:
            token = self.token_session_id
        else:
            token = self.token_userpass
        if self._token != token:
            self._token = token
            logger.debug(UPD_TPL(self.token_type_details))

    def auth_fallback(self):
        '''removes the session ID from the token, and reverts back to
        user and password auth'''
        self.session_id = None
        self.update_token()

    def session_from_response(self, response):
        '''Checks if SOAP response returned a session ID, and sets that to
        self.session_id if so
        n.b. session ID's issued from the SOAP API expire after 5 minutes
        '''
        UPD_TPL = (
            "Updating session ID from last SOAP Response [ID: {!r}]"
        ).format

        if not response.session_id:
            return

        if self.session_id != response.session_id:
            self.session_id = response.session_id
            id_text = self.session_id_text(self.session_id)
            logger.debug(UPD_TPL(id_text))

    def session_id_text(self, session_id):
        '''returns session ID if SHOW_SESSION_ID = True'''
        if SHOW_SESSION_ID:
            id_text = session_id
        else:
            id_text = "..."
        return id_text

    @property
    def username(self):
        '''returns the username'''
        if not hasattr(self, '_username'):
            return None
        return self._username

    @username.setter
    def username(self, value):
        '''sets the username'''
        self._username = value

    @property
    def password(self):
        '''returns the password'''
        if not hasattr(self, '_password'):
            return None
        return self._password

    @password.setter
    def password(self, value):
        '''sets the password'''
        self._password = value

    @property
    def token(self):
        '''returns the token'''
        if not hasattr(self, '_token'):
            return None
        return self._token

    @token.setter
    def token(self, value):
        '''sets the token'''
        self._token = value

    @property
    def session_id(self):
        '''returns the session_id'''
        if not hasattr(self, '_session_id'):
            return None
        return self._session_id

    @session_id.setter
    def session_id(self, value):
        '''sets the session_id'''
        needs_update = False
        if hasattr(self, '_session_id'):
            if self._session_id != value:
                needs_update = True

        self._session_id = value
        if value is None:
            self._session_id_issued = None
        else:
            self._session_id_issued = time.time()

        if needs_update:
            self.update_token()

    @property
    def session_id_issued(self):
        '''returns the session_id_issued'''
        if not hasattr(self, '_session_id_issued'):
            return None
        return self._session_id_issued

    @session_id_issued.setter
    def session_id_issued(self, value):
        '''sets the session_id_issued'''
        self._session_id_issued = value

    @property
    def session_id_valid(self):
        '''returns True if self.session_id is not empty and not yet expired,
        False otherwise - expiration is validated by looking at
        self.session_id_issued
        '''
        SESSION_TPL = (
            "Session ID {}: issued {}, minutes ago: {}, timeout: {} minutes"
        ).format

        if not self.session_id:
            return False

        dtdiff = datetime_diff(self.session_id_issued)
        minutes_dtdiff = dtdiff.seconds / 60
        hf_issued = human_time(self.session_id_issued)

        if self.SESSION_TIMEOUT < minutes_dtdiff:
            logger.debug(SESSION_TPL(
                'EXPIRED', hf_issued, minutes_dtdiff, self.SESSION_TIMEOUT,
            ))
            self._session_id = None
            self._session_id_issued = None
            return False

        logger.debug(SESSION_TPL(
            'VALID', hf_issued, minutes_dtdiff, self.SESSION_TIMEOUT,
        ))
        return True

    @property
    def via_session_id(self):
        '''returns True if self.token dict has 'session' in it'''
        return 'session' in self._token.keys()

    @property
    def via_userpass(self):
        '''returns True if token dict has 'auth' in it'''
        return 'auth' in self._token.keys()

    @property
    def token_type_details(self):
        '''returns token type and details in text form'''
        TOK_TPL = ('auth type: {} [{}: "{}"]').format
        token_details = "NONE"
        token_type = "UNKNOWN"
        if self.via_session_id:
            token_predetails = 'ID'
            token_details = self.session_id_text(self._token.get('session'))
            token_type = 'session ID'
        elif self.via_userpass:
            token_predetails = 'username'
            token_details = self._token.get('auth').username
            token_type = 'username/password'

        token_type_details = TOK_TPL(
            token_type, token_predetails, token_details
        )
        return token_type_details

    @property
    def token_userpass(self):
        '''returns a dictionary that has 'auth': SOAP element: auth,
        $username, $password
        '''
        auth_factory = self.client.factory.create('auth')
        auth_factory.username = self.username
        auth_factory.password = self.password
        token = {'auth': auth_factory}
        return token

    @property
    def token_session_id(self):
        '''returns a dictionary that has 'session': '$session_id' '''
        token = {'session': self.session_id}
        return token


class SoapWrap:
    def __init__(self, username, password, host, port="443", loglevel=0,
                 logfile=None, wsdl="HOSTED", soap_location="/soap"):

        logging_setup(loglevel)

        self.soap_host = host
        self.soap_port = port
        self.soap_location = soap_location

        self._wsdl_uri = wsdl
        self.request = None
        self.response = None
        self.all_msgs = []

        self.env_overrides()
        self.test_port()

        self.client = self.get_suds_client(self.wsdl_uri, self.soap_uri)

        self.soap_auth = SoapAuth(self.client)
        self.soap_auth.username = username
        self.soap_auth.password = password

    def __str__(self):
        STR_TPL = (
            "SoapWrap to {}:{}, WSDL URI: {}, SOAP URI: {}"
        ).format
        ret = STR_TPL(
            self.soap_host, self.soap_port, self.wsdl_uri, self.soap_uri,
        )
        return ret

    def env_overrides(self):
        '''looks for OS environment variables and overrides the corresponding
        attribute if they exist'''
        OR_TPL = ("Overriding {!r} with OS environment variable {!r}").format
        OS_ENV_MAP = {
            'SOAP_USERNAME': 'self.__soap_username',
            'SOAP_PASSWORD': 'self.__soap_password',
            'SOAP_HOSTNAME': 'self.soap_host',
            'SOAP_PORT': 'self.soap_port',
            'WSDL': 'self._wsdl_uri',
        }

        for os_env_var, class_var in OS_ENV_MAP.iteritems():
            if not os_env_var in os.environ.keys():
                continue

            if not os.environ[os_env_var]:
                continue

            logger.debug(OR_TPL(os.environ[os_env_var], os_env_var))
            setattr(self, class_var, os.environ[os_env_var])

    def test_port(self):
        '''validates that the SOAP port on the SOAP host can be reached'''
        CHK_TPL = ("Port test to {}:{} {}").format
        if port_check(self.soap_host, self.soap_port):
            logger.debug(CHK_TPL(self.soap_host, self.soap_port, "SUCCESS"))
            return True
        else:
            logger.error(CHK_TPL(self.soap_host, self.soap_port, "FAILED"))
            sys.exit(100)

    def get_suds_client(self, wsdl_uri, soap_uri):
        client = suds.client.Client(
            wsdl_uri,
            location=soap_uri,
            cache=None,
        )
        return client

    def ask_saved_question(self, saved_question):
        '''sends a saved question Request and returns a Response object'''
        sc_object1 = self.client.factory.create('saved_question')
        sc_object1.name = saved_question

        object_list = self.client.factory.create('object_list')
        object_list.saved_question = sc_object1

        self.request = SoapRequest(
            query_type='Saved Question',
            query_params=saved_question,
            query_object_list=object_list,
            command="GetResultData",
        )
        return self.call_api()

    def call_api(self):
        AUTH_TPL = (
            'Authorization {} for last request '
            '(query: {!r}, params {!r}, {})').format

        # set token to user/pass or session ID accordingly
        self.soap_auth.update_token()

        # get the SOAP response and store it in self.msg
        self.__send_request()

        # if auth failed and we are using a session ID, fallback to user/pass
        # and retry the request
        if not self.response.authok and self.soap_auth.via_session_id:
            logging.debug(
                "Last request failed due to expired/invalid session ID, "
                "retrying request with username/password"
            )
            self.soap_auth.auth_fallback()
            self.__send_request()

        # if auth is STILL failed, even if request was re-issued,
        # log an auth failure
        if not self.response.authok:
            logger.error(AUTH_TPL(
                'FAILED',
                self.request.query_type,
                self.request.query_params,
                self.soap_auth.token_type_details))
        else:
            logger.debug(AUTH_TPL(
                'SUCCESS',
                self.request.query_type,
                self.request.query_params,
                self.soap_auth.token_type_details))

        return self.response

    @property
    def wsdl_uri(self):
        '''returns the WSDL URI'''
        WSDL_TPL = ("https://{}:{}/console/console.wsdl").format
        wsdl_uri = WSDL_TPL(self.soap_host, self.soap_port)

        if not hasattr(self, '_wsdl_uri'):
            return wsdl_uri

        if self._wsdl_uri in [None, 'HOSTED']:
            return wsdl_uri

        # TODO: if wsdl_uri == file, test that it exists, else exit with error
        return self._wsdl_uri

    @property
    def soap_uri(self):
        '''returns the SOAP URI'''
        SOAP_TPL = ("https://{}:{}{}").format
        self._soap_uri = SOAP_TPL(
            self.soap_host, self.soap_port, self.soap_location
        )
        return self._soap_uri

    @property
    def wsdl_methods(self):
        '''Returns the methods from the WSDL in string format'''
        return self.client.__str__()

    def __send_request(self):
        '''sends the request to the SOAP API'''
        # TODO: Figure out request sent time for multiple requests
        SEND_TPL = ("Sending {}, SOAP URI: {}").format

        params = self.request.get_params(self.soap_auth.token)
        self.request.sent = time.time()

        self.response = SoapResponse(
            soap_uri=self.soap_uri,
            request=self.request,
        )

        logger.debug(SEND_TPL(self.request, self.soap_uri))

        self.response.response = self.client.service.Request(**params)
        self.soap_auth.session_from_response(self.response)
        self.all_msgs.append(self.response)
        # TODO: ADD LOGIC FOR WAITING FOR FULL RESULT SET


if __name__ == '__main__':
    soap_user = 'JTANIUM1\Jim Olsen'
    soap_pass = 'Evinc3d!'
    soap_host = '172.16.31.128'
    loglevel = 1

    sw = SoapWrap(soap_user, soap_pass, soap_host, loglevel=loglevel)
    sq1_result = sw.ask_saved_question('Installed Applications')
